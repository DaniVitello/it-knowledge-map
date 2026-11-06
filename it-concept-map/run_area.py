import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
import cli, runner as RN
from llm_groq import groq_llm
cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
area = sys.argv[1] if len(sys.argv) > 1 else "Backend"
concepts = cli._load_concepts(cfg)
concepts = [c for c in concepts if c.area == area]
print(f"Processing {len(concepts)} concepts in '{area}'...")
if len(concepts) == 1:
    rep = asyncio.run(RN.run_concept(concepts[0], cfg=cfg, llm=groq_llm, force=False, workdir=cfg.get("workdir")))
    print(f"{rep.concept_id}: {rep.status} ({rep.duration_ms}ms)")
else:
    batch = asyncio.run(RN.run_batch(concepts, cfg=cfg, llm=groq_llm, force=False, workdir=cfg.get("workdir")))
    print(f"Total: {batch.total} | completed: {batch.completed} | failed: {batch.failed} | skipped: {batch.skipped}")
    for r in batch.results:
        print(f"  {r.concept_id}: {r.status}")
