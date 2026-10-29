"""LLM adapter for Groq API. Provides an async callable for the synthesis phase."""
import os
import json
import urllib.request
import asyncio
import subprocess

# Try to get GROQ_API_KEY from environment (user-level on Windows)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
if not GROQ_API_KEY:
    try:
        result = subprocess.run(
            ["powershell", "-Command", '[Environment]::GetEnvironmentVariable("GROQ_API_KEY", "User")'],
            capture_output=True, text=True, timeout=10
        )
        GROQ_API_KEY = result.stdout.strip()
    except Exception:
        pass

GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


async def groq_llm(prompt: str) -> str:
    """Async LLM callable using Groq API. Returns the generated text."""
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")

    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert technical writer. Generate well-structured markdown documentation following the requested format exactly."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(
        GROQ_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
        method="POST",
    )

    loop = asyncio.get_event_loop()
    def _do_request():
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    return await loop.run_in_executor(None, _do_request)
