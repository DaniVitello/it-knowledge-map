
"""diagnose.py — Diagnostica por que fallaron conceptos del pipeline.

Uso:
    py diagnose.py                    # diagnostico completo
    py diagnose.py <concept-id>       # diagnostico de un concepto
    py diagnose.py --area "X"         # diagnostico de un area

Lee progress.json, state files, logs, y produce un reporte de causas raiz.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
import cli

cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
concepts = {c.id: c for c in cli._load_concepts(cfg)}
vault = Path(cfg["vault_path"])
workdir = Path(cfg["workdir"])
progress_file = workdir / "progress.json"
log_file = workdir / "run_all_areas.log"

# Known failure patterns and their root causes
FAILURE_PATTERNS = [
    ("Free usage limit", "OpenCode free tier exhausted. Pipeline uses Groq, not OpenCode, so this shouldn't happen. Check if something is calling OpenCode."),
    ("rate limit", "Groq rate limit (7000 tokens/min). Pipeline has backoff [2,4,8]s. If persistent, reduce batch size or add longer delays."),
    ("WikilinksChangedError", "Writer detected wikilink changes. Spec says LLM should NOT generate wikilinks in v1. Check synthesis prompt."),
    ("TimeoutError", "Operation exceeded timeout. NotebookLM research can take up to 120s. Check network stability."),
    ("ConnectionError", "Network error connecting to NotebookLM or Groq. Check internet connection."),
    ("FileNotFoundError", "Expected file not found. May be a path issue or missing artifact."),
    ("JSONDecodeError", "Corrupt JSON file. May be a write interruption. Delete and re-run with --force."),
    ("PermissionError", "File permission issue. Check that the process has write access to vault and workdir."),
    ("ModuleNotFoundError", "Missing Python dependency. Run: .venv\\Scripts\\activate && pip install -r requirements.txt"),
    ("Invalid API Key", "Groq API key invalid or expired. Check llm_groq.py and GROQ_API_KEY env var."),
    ("Request too large", "Groq request exceeds token limit. Reduce prompt size or switch model."),
    ("auth", "Authentication issue. NotebookLM cookies may have expired. Re-authenticate."),
    ("Encabezado faltante", "Validacion fallo por secciones faltantes. Revisar sintesis o arreglar validador (trailing spaces)."),
    ("interrupted", "Investigacion interrumpida (quedo en researching). Reintentar con --retry --failed."),
    ("Transicion invalida", "Transicion de estado no permitida. Revisar logica de reanudacion en research.py."),
]

def find_root_cause(error_text):
    for pattern, cause in FAILURE_PATTERNS:
        if pattern.lower() in error_text.lower():
            return cause
    return "Unknown cause. Check the full log and state files for details."

def diagnose_concept(concept_id):
    result = {"concept_id": concept_id, "issues": [], "root_causes": [], "state": None, "pipeline_files": []}

    concept = concepts.get(concept_id)

    # Check vault file
    if concept is not None and getattr(concept, "note_path", None):
        file_path = Path(concept.note_path)
    else:
        file_path = vault / concept_id
    if not file_path.exists():
        result["issues"].append("File not found in vault")
    else:
        content = file_path.read_text(encoding="utf-8")
        if "<!-- ai:start -->" not in content:
            result["issues"].append("AI block not written (pipeline did not complete write phase)")

    # Check pipeline state (estado.json en workdir/concepts/<id>/)
    state_file = workdir / "concepts" / concept_id / "estado.json"
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
            result["state"] = state
            status = state.get("status", "unknown")
            if status != "completed":
                result["issues"].append(f"Pipeline status: {status}")
                if "error" in state:
                    result["root_causes"].append(find_root_cause(state["error"]))
                if "failure" in state and state["failure"]:
                    result["root_causes"].append(find_root_cause(str(state["failure"])))
                pd = state.get("phase_data", {}) or {}
                if pd.get("failed_phase"):
                    result["issues"].append(f"Failed phase: {pd['failed_phase']} ({pd.get('failed_reason', '')})")
        except json.JSONDecodeError:
            result["issues"].append("Corrupt estado.json")
            result["root_causes"].append("JSON parse error in state file. Delete and re-run with --force.")
    else:
        result["issues"].append("No pipeline state file found")

    # Check pipeline artifacts
    pipeline_dir = workdir / ".pipeline" / concept_id
    if pipeline_dir.exists():
        result["pipeline_files"] = [f.name for f in pipeline_dir.rglob("*") if f.is_file()]
    else:
        result["issues"].append("No pipeline directory found")
    
    # Check log for this concept
    if log_file.exists():
        log_content = log_file.read_text(encoding="utf-8", errors="replace")
        concept_errors = []
        for line in log_content.split("\n"):
            if concept_id in line and ("error" in line.lower() or "fail" in line.lower() or "exception" in line.lower()):
                concept_errors.append(line.strip())
        if concept_errors:
            result["log_errors"] = concept_errors[-5:]  # last 5
            for err in concept_errors[-5:]:
                rc = find_root_cause(err)
                if rc not in result["root_causes"]:
                    result["root_causes"].append(rc)
    
    if not result["root_causes"]:
        result["root_causes"].append("No specific root cause identified. Check logs manually.")
    
    return result

def diagnose_area(area):
    area_concepts = [c for c in concepts.values() if c.area == area]
    results = []
    for c in area_concepts:
        r = diagnose_concept(c.id)
        if r["issues"]:
            results.append(r)
    return results

def main():
    if len(sys.argv) < 2:
        # Full diagnosis
        print(f"\n{'='*60}")
        print("FULL DIAGNOSIS")
        print(f"{'='*60}")
        
        # Check progress.json
        if progress_file.exists():
            progress = json.loads(progress_file.read_text(encoding="utf-8"))
            print(f"\nProgress file: {progress_file}")
            print(f"Started: {progress.get('started_at', 'N/A')}")
            print(f"Last update: {progress.get('last_update', 'N/A')}")
            print(f"Final count: {progress.get('final_count', 'N/A')}")
            
            for area, info in progress.get("areas", {}).items():
                status = info.get("status", "unknown")
                new = info.get("new_concepts", "?")
                icon = "OK" if status == "completed" else "FAIL" if status in ("failed", "error", "timeout") else "..."
                print(f"  [{icon}] {area}: {status} (new: {new})")
        else:
            print("\nNo progress.json found. Pipeline may not have started.")
        
        # Check for failed concepts
        failed = []
        for cid in concepts:
            r = diagnose_concept(cid)
            if r["issues"]:
                failed.append(r)
        
        if failed:
            print(f"\n{'='*60}")
            print(f"FAILED/INCOMPLETE CONCEPTS: {len(failed)}")
            print(f"{'='*60}")
            for r in failed[:20]:  # show first 20
                print(f"\n  {r['concept_id']}:")
                for issue in r["issues"]:
                    print(f"    - {issue}")
                for rc in r["root_causes"]:
                    print(f"    ROOT CAUSE: {rc}")
        else:
            print("\nNo failed concepts found.")
        
        # Check log for errors
        if log_file.exists():
            log_content = log_file.read_text(encoding="utf-8", errors="replace")
            error_lines = [l for l in log_content.split("\n") if "error" in l.lower() or "exception" in l.lower() or "traceback" in l.lower()]
            if error_lines:
                print(f"\n{'='*60}")
                print(f"ERROR LINES IN LOG: {len(error_lines)}")
                print(f"{'='*60}")
                for line in error_lines[-10:]:
                    print(f"  {line.strip()}")
        
        # Check tests
        print(f"\n{'='*60}")
        print("RECOMMENDED NEXT STEPS:")
        print(f"{'='*60}")
        if failed:
            print("  1. Review root causes above")
            print("  2. Fix the underlying issue")
            print("  3. Re-run failed concepts: py run_pipeline.py --concept <id> --force")
            print("  4. Re-run diagnosis: py diagnose.py")
        else:
            print("  1. Run evals: py eval_concept.py --all")
            print("  2. Run tests: py -m pytest -q")
            print("  3. Verify count: 255/255")
        
    elif sys.argv[1] == "--area":
        area = sys.argv[2]
        results = diagnose_area(area)
        print(f"\nArea: {area} | Failed/incomplete: {len(results)}")
        for r in results:
            print(f"\n  {r['concept_id']}:")
            for issue in r["issues"]:
                print(f"    - {issue}")
            for rc in r["root_causes"]:
                print(f"    ROOT CAUSE: {rc}")
    
    else:
        cid = sys.argv[1]
        r = diagnose_concept(cid)
        print(f"\nConcept: {r['concept_id']}")
        print(f"Issues: {r['issues']}")
        print(f"Root causes: {r['root_causes']}")
        print(f"Pipeline files: {r['pipeline_files']}")
        if r.get("log_errors"):
            print(f"Log errors: {r['log_errors']}")
        if r["state"]:
            print(f"State: {json.dumps(r['state'], indent=2)}")

if __name__ == "__main__":
    main()
