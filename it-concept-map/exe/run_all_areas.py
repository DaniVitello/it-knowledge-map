
import subprocess
import json
import time
import sys
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../main'))
from pathlib import Path
from datetime import datetime

AREAS = [
    "Software Engineering",
    "Frontend",
    "Backend",
    "Database / Data Analytics",
    "Networking / Internet",
    "Operating Systems / Linux",
    "AI Engineering",
    "UX / UI",
    "Product Management",
    "Project Management",
]

WORKDIR = Path(r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
VAULT = Path(r"C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map")
PROGRESS_FILE = WORKDIR / "progress.json"
VENV_PYTHON = WORKDIR / ".venv" / "Scripts" / "python.exe"

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"areas": {}, "started_at": datetime.now().isoformat(), "last_update": None}

def save_progress(progress):
    progress["last_update"] = datetime.now().isoformat()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")

def count_completed():
    """Count concepts with AI block in vault. Reads files directly (no subprocess)."""
    count = 0
    for md_file in VAULT.rglob("*.md"):
        if "00 -" in md_file.name or md_file.name.startswith("_"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            if "<!-- ai:start -->" in content:
                count += 1
        except:
            pass
    return count

def main():
    progress = load_progress()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Master runner started", flush=True)
    print(f"Progress file: {PROGRESS_FILE}", flush=True)
    
    for area in AREAS:
        area_status = progress["areas"].get(area, {})
        if area_status.get("status") == "completed":
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {area}: already completed, skipping", flush=True)
            continue
        
        print(f"\n{'='*60}", flush=True)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting area: {area}", flush=True)
        print(f"{'='*60}", flush=True)
        
        progress["areas"][area] = {"status": "running", "started_at": datetime.now().isoformat()}
        save_progress(progress)
        
        before = count_completed()
        print(f"Concepts completed before: {before}/255", flush=True)
        
        try:
            result = subprocess.run(
                [str(VENV_PYTHON), "run_pipeline.py", "--area", area],
                capture_output=True, text=True, cwd=str(WORKDIR),
                timeout=3600
            )
            
            after = count_completed()
            new_concepts = after - before
            
            print(f"\nSTDOUT (last 300 chars):", flush=True)
            print(result.stdout[-300:] if result.stdout else "(empty)", flush=True)
            if result.stderr:
                print(f"\nSTDERR (last 300 chars):", flush=True)
                print(result.stderr[-300:], flush=True)
            
            progress["areas"][area] = {
                "status": "completed" if result.returncode == 0 else "failed",
                "started_at": area_status.get("started_at", datetime.now().isoformat()),
                "finished_at": datetime.now().isoformat(),
                "returncode": result.returncode,
                "concepts_before": before,
                "concepts_after": after,
                "new_concepts": new_concepts,
            }
            save_progress(progress)
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {area}: {'COMPLETED' if result.returncode == 0 else 'FAILED'}", flush=True)
            print(f"  New: {new_concepts}, Total: {after}/255", flush=True)
            
        except subprocess.TimeoutExpired:
            after = count_completed()
            progress["areas"][area] = {
                "status": "timeout",
                "started_at": area_status.get("started_at", datetime.now().isoformat()),
                "finished_at": datetime.now().isoformat(),
                "concepts_before": before,
                "concepts_after": after,
            }
            save_progress(progress)
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {area}: TIMEOUT", flush=True)
        
        except Exception as e:
            after = count_completed()
            progress["areas"][area] = {
                "status": "error",
                "error": str(e),
                "started_at": area_status.get("started_at", datetime.now().isoformat()),
                "finished_at": datetime.now().isoformat(),
                "concepts_before": before,
                "concepts_after": after,
            }
            save_progress(progress)
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {area}: ERROR - {e}", flush=True)
    
    final_count = count_completed()
    progress["finished_at"] = datetime.now().isoformat()
    progress["final_count"] = final_count
    save_progress(progress)
    
    print(f"\n{'='*60}", flush=True)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ALL AREAS DONE", flush=True)
    print(f"Final count: {final_count}/255", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == "__main__":
    main()
