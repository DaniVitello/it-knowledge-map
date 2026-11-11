
"""Run only MISSING concepts (no estado.json) with Groq LLM."""
import asyncio, argparse, os, sys, json
from pathlib import Path
os.chdir(r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
sys.path.insert(0, os.getcwd())
import cli, runner as RN
from llm_groq import groq_llm

cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
concepts = cli._load_concepts(cfg)
workdir = cfg.get("workdir")
workdir_dirs = set(os.listdir(workdir + "/concepts")) if os.path.exists(workdir + "/concepts") else set()
missing = [c for c in concepts if c.id not in workdir_dirs]

parser = argparse.ArgumentParser()
parser.add_argument("--area", default=None)
parser.add_argument("--limit", type=int, default=None)
parser.add_argument("--force", action="store_true")
args = parser.parse_args()

if args.area:
    missing = [c for c in missing if c.area == args.area]
if args.limit:
    missing = missing[:args.limit]

print(f"Processing {len(missing)} missing concepts (area={args.area}) with Groq LLM...", flush=True)

async def main():
    completed = 0; failed = 0
    for c in missing:
        try:
            rep = await RN.run_concept(c, cfg=cfg, llm=groq_llm, force=args.force, workdir=workdir)
            print(f"{rep.concept_id}: {rep.status} ({rep.duration_ms}ms) phases={rep.phases_completed}", flush=True)
            if rep.error:
                print(f"  error: {rep.error}", flush=True)
            if rep.status == "completed":
                completed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"{c.id}: EXCEPTION {e}", flush=True)
            failed += 1
    print(f"TOTAL: {len(missing)} | completed: {completed} | failed: {failed}", flush=True)

asyncio.run(main())
