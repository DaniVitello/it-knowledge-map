"""Run the IT Career pipeline with Groq LLM for synthesis."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cli
import runner as RN
from llm_groq import groq_llm

# Load config
cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--area", default=None)
    parser.add_argument("--concept", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    concepts = cli._load_concepts(cfg)
    if args.concept:
        concepts = [c for c in concepts if c.id == args.concept or args.concept in c.id]
    elif args.area:
        concepts = [c for c in concepts if c.area == args.area]
    if args.limit:
        concepts = concepts[:args.limit]

    print(f"Processing {len(concepts)} concepts with Groq LLM...")

    if len(concepts) == 1:
        rep = await RN.run_concept(concepts[0], cfg=cfg, llm=groq_llm, force=args.force, workdir=cfg.get("workdir"))
        print(f"{rep.concept_id}: {rep.status} ({rep.duration_ms}ms) phases={rep.phases_completed}")
        if rep.error:
            print(f"  error: {rep.error}")
    else:
        batch = await RN.run_batch(concepts, cfg=cfg, llm=groq_llm, force=args.force, workdir=cfg.get("workdir"))
        print(f"Total: {batch.total} | completed: {batch.completed} | failed: {batch.failed} | skipped: {batch.skipped}")
        for r in batch.results:
            print(f"  {r.concept_id}: {r.status}")

if __name__ == "__main__":
    asyncio.run(main())
