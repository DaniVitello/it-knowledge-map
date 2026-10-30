"""Capa K - Modulo de logging/trazabilidad para el pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"


def now_iso():
    try:
        import state as _state
        if hasattr(_state, "now_iso"):
            return _state.now_iso()
    except Exception:
        pass
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def log_event(workdir, concept_id, event, run_id=None, **kwargs):
    cdir = Path(workdir) / "concepts" / concept_id
    cdir.mkdir(parents=True, exist_ok=True)
    entry = {"ts": now_iso(), "run_id": run_id, "concept_id": concept_id, "event": event}
    entry.update(kwargs)
    with open(cdir / "events.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def log_run_start(workdir, run_id, total):
    Path(workdir).mkdir(parents=True, exist_ok=True)
    with open(Path(workdir) / "run.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now_iso(), "run_id": run_id, "event": "run_start", "total": total}, ensure_ascii=False) + "\n")


def log_run_end(workdir, run_id, completed, failed, duration_ms):
    Path(workdir).mkdir(parents=True, exist_ok=True)
    with open(Path(workdir) / "run.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now_iso(), "run_id": run_id, "event": "run_end", "completed": completed, "failed": failed, "duration_ms": duration_ms}, ensure_ascii=False) + "\n")


class RunLogger:
    def __init__(self, workdir, run_id):
        self.workdir = workdir
        self.run_id = run_id

    def event(self, concept_id, event, **kwargs):
        return log_event(self.workdir, concept_id, event, run_id=self.run_id, **kwargs)

    def run_start(self, total):
        return log_run_start(self.workdir, self.run_id, total)

    def run_end(self, completed, failed, duration_ms):
        return log_run_end(self.workdir, self.run_id, completed, failed, duration_ms)
