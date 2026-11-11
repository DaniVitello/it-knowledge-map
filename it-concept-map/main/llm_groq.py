"""LLM adapter for Groq API. Provides an async callable for the synthesis phase.

Soporta rotacion automatica entre multiples API keys. Lee las keys desde
config.yaml (groq.api_keys o llm_groq.api_keys) primero; fallback a env
GROQ_API_KEYS (coma-separadas) o GROQ_API_KEY unica.
"""
import os
import json
import urllib.request
import urllib.error
import asyncio
import subprocess


def _load_keys() -> list[str]:
    # 1. Proyecto: config.yaml
    try:
        import yaml
        with open("config.yaml", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        for path in (("groq", "api_keys"), ("llm_groq", "api_keys"),
                     ("backend", "groq", "api_keys")):
            node = cfg
            for key in path:
                if isinstance(node, dict):
                    node = node.get(key)
                else:
                    node = None
                    break
            if isinstance(node, list) and node:
                return [str(k).strip() for k in node if str(k).strip()]
            if isinstance(node, str) and node.strip():
                return [k.strip() for k in node.split(",") if k.strip()]
    except Exception:
        pass
    # 2. Env var global (fallback)
    raw = os.environ.get("GROQ_API_KEYS", "").strip()
    if not raw:
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 '[Environment]::GetEnvironmentVariable("GROQ_API_KEYS", "User")'],
                capture_output=True, text=True, timeout=10,
            )
            raw = result.stdout.strip()
        except Exception:
            pass
    if not raw:
        single = os.environ.get("GROQ_API_KEY", "").strip()
        if not single:
            try:
                result = subprocess.run(
                    ["powershell", "-Command",
                     '[Environment]::GetEnvironmentVariable("GROQ_API_KEY", "User")'],
                    capture_output=True, text=True, timeout=10,
                )
                single = result.stdout.strip()
            except Exception:
                pass
        raw = single
    return [k.strip() for k in raw.split(",") if k.strip()]


GROQ_KEYS = _load_keys()
_current_key_idx = 0

GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def _current_key() -> str:
    global _current_key_idx
    if not GROQ_KEYS:
        return ""
    if _current_key_idx >= len(GROQ_KEYS):
        _current_key_idx = 0
    return GROQ_KEYS[_current_key_idx]


def _rotate_key() -> bool:
    global _current_key_idx
    if len(GROQ_KEYS) <= 1:
        return False
    _current_key_idx = (_current_key_idx + 1) % len(GROQ_KEYS)
    return _current_key_idx != 0


async def groq_llm(prompt: str) -> str:
    if not GROQ_KEYS:
        raise RuntimeError("GROQ_API_KEY(S) not set")

    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert technical writer. Generate well-structured markdown documentation following the requested format exactly."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }).encode("utf-8")

    last_exc = None
    for _ in range(len(GROQ_KEYS)):
        key = _current_key()
        req = urllib.request.Request(
            GROQ_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            method="POST",
        )

        loop = asyncio.get_event_loop()

        def _do_request():
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]

        try:
            return await loop.run_in_executor(None, _do_request)
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code == 429:
                if _rotate_key():
                    continue
                raise RuntimeError("Todas las keys de Groq agotadas (429)") from exc
            raise
        except Exception as exc:
            last_exc = exc
            raise

    if last_exc is not None:
        raise last_exc
    raise RuntimeError("Groq: sin keys disponibles")
