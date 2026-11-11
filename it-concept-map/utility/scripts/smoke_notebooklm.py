#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke test del backend real (NotebookLM).

Prueba cada operacion contra una cuenta real y mide tiempos.
Uso: python scripts/smoke_notebooklm.py
Requiere: notebooklm-py instalado y sesion activa (notebooklm login).
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend import NotebookLMBackend, _notebooklm_module
from models import ConceptMeta

CONCEPT = ConceptMeta(
    id="smoke-test-concept",
    title="Smoke Test",
    area="Frontend",
    note_path=Path("smoke.md"),
)


async def timed(label, coro):
    t0 = time.monotonic()
    try:
        r = await coro
        dt = (time.monotonic() - t0) * 1000
        print(f"  OK   {label}: {dt:.0f} ms")
        return r, dt
    except Exception as e:
        dt = (time.monotonic() - t0) * 1000
        print(f"  FAIL {label}: {type(e).__name__}: {e} ({dt:.0f} ms)")
        return None, dt


async def main():
    report = {}
    async with NotebookLMBackend() as backend:
        # 1. create notebook
        nb_id, dt = await timed("create_notebook", backend.create_notebook("smoke-test-nb"))
        if not nb_id:
            print("No se pudo crear notebook; abortando.")
            return
        report["create_notebook_ms"] = dt

        # 2. add urls (seed)
        urls = ["https://developer.mozilla.org/en-US/docs/Web/HTTP"]
        r, dt = await timed("add_urls", backend.add_urls(nb_id, urls))
        report["add_urls_ms"] = dt

        # 3. discover (research)
        try:
            disc = await timed("discover", backend.discover(nb_id, "HTTP fundamentals", "fast", 120))
            report["discover_ms"] = disc[1]
        except Exception as e:
            print(f"  discover error: {e}")

        # 4. list sources
        srcs, dt = await timed("list_sources", backend.list_sources(nb_id))
        report["list_sources_ms"] = dt

        # 5. wait sources ready
        try:
            await timed("wait_sources_ready", backend.wait_sources_ready(nb_id, 60))
        except Exception as e:
            print(f"  wait_sources_ready error: {e}")

        # 6. ask
        try:
            ans = await timed("ask", backend.ask(nb_id, "Que es HTTP?"))
            report["ask_ms"] = ans[1]
        except Exception as e:
            print(f"  ask error: {e}")

        # 7. delete notebook
        await timed("delete_notebook", backend.delete_notebook(nb_id))
        report["delete_notebook_ms"] = None

    out = Path(__file__).resolve().parent.parent / "workdir" / "smoke_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReporte guardado en {out}")


if __name__ == "__main__":
    asyncio.run(main())
