
"""monitor.py — Monitoreo rapido del pipeline para Hermes.

Uso: py monitor.py
Output: JSON con estado actual (para Hermes leer via HTTP API)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

workdir = Path(r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
progress_file = workdir / "progress.json"

result = {"timestamp": datetime.now().isoformat(), "pipeline_running": False, "progress": None, "log_tail": [], "errors": []}

# Check progress
if progress_file.exists():
    try:
        progress = json.loads(progress_file.read_text(encoding="utf-8"))
        result["progress"] = progress
        result["pipeline_running"] = progress.get("final_count") is None
    except:
        result["errors"].append("Corrupt progress.json")

# Check log tail
log_file = workdir / "run_all_areas.log"
if log_file.exists():
    lines = log_file.read_text(encoding="utf-8", errors="replace").split("\n")
    result["log_tail"] = [l.strip() for l in lines[-10:] if l.strip()]
    # Count errors in log
    error_count = sum(1 for l in lines if "error" in l.lower() or "exception" in l.lower() or "fail" in l.lower())
    result["log_error_count"] = error_count

# Check if process is running
import subprocess
try:
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV", "/NH"], capture_output=True, text=True)
    python_procs = [l for l in r.stdout.split("\n") if "python" in l.lower()]
    result["python_processes"] = len(python_procs)
except:
    result["python_processes"] = -1

print(json.dumps(result, indent=2, ensure_ascii=False))
