import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
import cli, runner as RN
from llm_groq import groq_llm
cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
concepts = cli._load_concepts(cfg)
area = "Backend"
concepts = [c for c in concepts if c.area == area]
print(f"Found {len(concepts)} concepts for area '{area}'")
for c in concepts[:3]:
    print(f"  {c.id}")
