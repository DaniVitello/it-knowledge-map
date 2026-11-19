# -*- coding: utf-8 -*-
"""Adaptador de proveedor de modelos (L3, capa 18)."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from ikm.contracts.config import PlanModelo
from ikm.contracts.errors import AbortStage


class LLMError(AbortStage):
    pass


class LLMTimeoutError(LLMError):
    pass


class LLMRateLimitError(LLMError):
    pass


class LLMAdapter:
    """Adaptador de proveedor de modelos (estilo OpenAI/Groq)."""

    def __init__(self, config: PlanModelo):
        self.config = config
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import openai
                self._client = openai.OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY", ""),
                    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
                )
            except ImportError:
                self._client = None
        return self._client

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """Envia una conversacion al modelo y devuelve la respuesta."""
        client = self._get_client()
        if client is None:
            raise LLMError("no_client", etapa="llm", detalle={"motivo": "openai no disponible"})

        try:
            response = client.chat.completions.create(
                model=self.config.modelo,
                messages=messages,
                temperature=self.config.temperatura,
                max_tokens=self.config.max_output_tokens,
                timeout=self.config.timeout_segundos,
            )
            content = response.choices[0].message.content if response.choices else ""
            return {
                "content": content,
                "usage": {
                    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0) if response.usage else 0,
                    "completion_tokens": getattr(response.usage, "completion_tokens", 0) if response.usage else 0,
                },
            }
        except Exception as exc:
            if "timeout" in str(exc).lower():
                raise LLMTimeoutError("timeout", etapa="llm", detalle={"motivo": str(exc)}) from exc
            if "rate" in str(exc).lower() or "429" in str(exc):
                raise LLMRateLimitError("rate_limit", etapa="llm", detalle={"motivo": str(exc)}) from exc
            raise LLMError("provider_error", etapa="llm", detalle={"motivo": str(exc)}) from exc

    def chat_json(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """Envia una conversacion y parsea la respuesta como JSON."""
        result = self.chat(messages, **kwargs)
        content = result.get("content", "")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Intentar extraer JSON del texto
            import re
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            raise LLMError("invalid_json", etapa="llm", detalle={"content": content[:200]})
