# -*- coding: utf-8 -*-
"""Adaptador Groq para el chat (L8). OpenAI-compatible via urllib (sin SDK).

Reusa las mismas keys de la etapa de sintesis: GROQ_API_KEYS (coma-separadas)
o GROQ_API_KEY, con rotacion automatica ante 429. Modelo openai/gpt-oss-120b.
Portable a Hugging Face Spaces (las keys van como secrets del Space).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from ikm.contracts.config import PlanModelo
from ikm.contracts.errors import AbortStage


class LLMError(AbortStage):
    pass


class LLMTimeoutError(LLMError):
    pass


class LLMRateLimitError(LLMError):
    pass


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def _load_groq_keys() -> List[str]:
    """Carga las keys igual que la sintesis (env -> User env en Windows)."""
    raw = os.environ.get("GROQ_API_KEYS", "").strip()
    if not raw:
        raw = os.environ.get("GROQ_API_KEY", "").strip()
    if not raw and sys.platform == "win32":
        for var in ("GROQ_API_KEYS", "GROQ_API_KEY"):
            try:
                res = subprocess.run(
                    ["powershell", "-Command",
                     f'[Environment]::GetEnvironmentVariable("{var}", "User")'],
                    capture_output=True, text=True, timeout=10,
                )
                raw = res.stdout.strip()
                if raw:
                    break
            except Exception:
                pass
    return [k.strip() for k in raw.split(",") if k.strip()]


class LLMAdapter:
    """Adaptador Groq con rotacion de keys y modo JSON."""

    def __init__(self, config: PlanModelo):
        self.config = config
        self.keys = _load_groq_keys()
        self._idx = 0
        self.model = config.modelo or "openai/gpt-oss-120b"
        self.base_url = os.environ.get("OPENAI_BASE_URL", GROQ_URL)
        if "groq" in (config.provider or "").lower() and "openai.com" in self.base_url:
            self.base_url = GROQ_URL

    @property
    def disponible(self) -> bool:
        return bool(self.keys)

    def _key(self) -> str:
        if not self.keys:
            return ""
        return self.keys[self._idx % len(self.keys)]

    def _rotate(self) -> bool:
        if len(self.keys) <= 1:
            return False
        self._idx = (self._idx + 1) % len(self.keys)
        return True

    def chat(self, messages: List[Dict[str, str]], json_mode: bool = False,
             **kwargs: Any) -> Dict[str, Any]:
        if not self.keys:
            raise LLMError("no_keys", etapa="llm", detalle={"motivo": "GROQ_API_KEY(S) no configuradas"})

        # gpt-oss es un modelo de razonamiento: necesita headroom de salida.
        max_tokens = 1500  # gpt-oss: headroom para razonamiento + respuesta
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.temperatura,
            "max_tokens": max_tokens,
        }
        if "gpt-oss" in self.model:
            payload["reasoning_effort"] = self.config.reasoning_effort or "low"
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        data = json.dumps(payload).encode("utf-8")

        last_exc: Optional[Exception] = None
        for _ in range(len(self.keys) + 1):
            req = urllib.request.Request(
                self.base_url, data=data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self._key()}",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=self.config.timeout_segundos + 40) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"] if body.get("choices") else ""
                usage = body.get("usage", {}) or {}
                return {
                    "content": content,
                    "usage": {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0),
                    },
                }
            except urllib.error.HTTPError as exc:
                last_exc = exc
                if exc.code == 429:
                    if self._rotate():
                        continue
                    time.sleep(2)
                    continue
                detalle = exc.read().decode("utf-8", "replace")[:300] if hasattr(exc, "read") else str(exc)
                raise LLMError("provider_error", etapa="llm", detalle={"status": exc.code, "motivo": detalle}) from exc
            except urllib.error.URLError as exc:
                last_exc = exc
                if "timeout" in str(exc).lower():
                    raise LLMTimeoutError("timeout", etapa="llm", detalle={"motivo": str(exc)}) from exc
                raise LLMError("network_error", etapa="llm", detalle={"motivo": str(exc)}) from exc
            except Exception as exc:
                last_exc = exc
                raise LLMError("provider_error", etapa="llm", detalle={"motivo": str(exc)}) from exc

        raise LLMRateLimitError("rate_limit", etapa="llm", detalle={"motivo": str(last_exc)})

    def chat_json(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        result = self.chat(messages, json_mode=True, **kwargs)
        content = result.get("content", "") or ""
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group(0))
                except json.JSONDecodeError:
                    raise LLMError("invalid_json", etapa="llm", detalle={"content": content[:200]})
            else:
                raise LLMError("invalid_json", etapa="llm", detalle={"content": content[:200]})
        if isinstance(parsed, dict):
            parsed.setdefault("usage", result.get("usage", {}))
        return parsed