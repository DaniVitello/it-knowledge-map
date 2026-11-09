"""Reintenta conceptos en estado failed, area por area."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cli
import runner as RN
from llm_groq import groq_llm
import json
import state

cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
workdir = cfg.get("workdir")

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--area", default=None)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    concepts = cli._load_concepts(cfg)
    if args.area:
        concepts = [c for c in concepts if c.area == args.area]

    # Filtrar solo failed
    failed = []
    for c in concepts:
        st_path = Path(workdir) / "concepts" / c.id / "estado.json"
        if st_path.exists():
            st = json.loads(st_path.read_text(encoding="utf-8"))
            if st.get("status") in ("failed", "researching", "synthesized", "validated", "written"):
                failed.append(c)
    if args.limit:
        failed = failed[:args.limit]

    print(f"Reintentando {len(failed)} conceptos failed...")
    ok = 0
    fail = 0
    for c in failed:
        rep = await RN.run_concept(c, cfg=cfg, llm=groq_llm, force=True, workdir=workdir)
        print(f"  {rep.concept_id}: {rep.status} ({rep.duration_ms}ms)")
        if rep.error:
            print(f"    error: {rep.error}")
        if rep.status == "completed":
            ok += 1
        else:
            fail += 1
    print(f"\nTotal: {len(failed)} | completed: {ok} | failed: {fail}")

if __name__ == "__main__":
    asyncio.run(main())
PY