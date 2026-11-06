
"""Run PENDING concepts (missing estado OR status failed) with Groq LLM."""
import asyncio, argparse, os, sys, json
from pathlib import Path
os.chdir(r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
sys.path.insert(0, os.getcwd())
import cli, runner as RN
from llm_groq import groq_llm

cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
concepts = cli._load_concepts(cfg)
workdir = cfg.get("workdir")
concept_dir = os.path.join(workdir, "concepts")

def get_status(cid):
    ep = os.path.join(concept_dir, cid, "estado.json")
    if not os.path.exists(ep):
        return None
    try:
        with open(ep, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except Exception:
        return "parse_error"
    for key in ("status", "state", "phase", "last_good_state", "current_phase"):
        if key in data:
            return data[key]
    return "unknown"

pending = []
for c in concepts:
    st = get_status(c.id)
    if st is None or "fail" in str(st).lower():
        pending.append(c)

parser = argparse.ArgumentParser()
parser.add_argument("--area", default=None)
parser.add_argument("--limit", type=int, default=None)
parser.add_argument("--force", action="store_true")
args = parser.parse_args()

if args.area:
    pending = [c for c in pending if c.area == args.area]
if args.limit:
    pending = pending[:args.limit]

print(f"Processing {len(pending)} pending concepts (area={args.area}) with Groq LLM...", flush=True)

async def main():
    completed = 0; failed = 0
    for c in pending:
        try:
            rep = await RN.run_concept(c, cfg=cfg, llm=groq_llm, force=True, workdir=workdir)
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
    print(f"TOTAL: {len(pending)} | completed: {completed} | failed: {failed}", flush=True)

asyncio.run(main())
