
import json
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

WORKDIR = Path(r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
PROGRESS_FILE = WORKDIR / "progress.json"
ALERTS_FILE = WORKDIR / "alerts.log"
LOG_FILE = WORKDIR / "run_all_areas.log"

def log_alert(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    with open(ALERTS_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def check_process_alive():
    try:
        r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV", "/NH"],
                          capture_output=True, text=True)
        procs = [l for l in r.stdout.split("\n") if "python" in l.lower() and "run_all" in l.lower() or "run_pipeline" in l.lower()]
        # Also check for any python process with significant CPU
        all_python = [l for l in r.stdout.split("\n") if "python" in l.lower()]
        return len(all_python), len(procs)
    except:
        return -1, -1

def main():
    log_alert("OVERNIGHT MONITOR STARTED")
    log_alert(f"Monitoring: {PROGRESS_FILE}")
    log_alert(f"Alerts: {ALERTS_FILE}")
    
    last_update = None
    stale_checks = 0
    check_count = 0
    
    while True:
        check_count += 1
        time.sleep(300)  # 5 minutes
        
        try:
            if not PROGRESS_FILE.exists():
                log_alert("WARNING: progress.json not found. Pipeline may not have started.")
                continue
            
            progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            current_update = progress.get("last_update")
            
            # Check if pipeline is complete
            if progress.get("final_count") is not None:
                final = progress["final_count"]
                log_alert(f"PIPELINE COMPLETE: {final}/255 concepts processed.")
                log_alert("Monitor stopping. Good morning!")
                break
            
            # Check for progress
            if current_update != last_update:
                last_update = current_update
                stale_checks = 0
                areas = progress.get("areas", {})
                done = sum(1 for a in areas.values() if a.get("status") == "completed")
                running = [a for a, info in areas.items() if info.get("status") == "running"]
                failed = [a for a, info in areas.items() if info.get("status") in ("failed", "error", "timeout")]
                log_alert(f"Check #{check_count}: {done}/{len(areas)} areas done. Running: {running}. Failed: {failed}.")
            else:
                stale_checks += 1
                log_alert(f"Check #{check_count}: NO PROGRESS in {stale_checks * 5} minutes. Last update: {current_update}")
                
                if stale_checks >= 2:  # 10 minutes without progress
                    # Check if process is alive
                    total_procs, pipeline_procs = check_process_alive()
                    log_alert(f"Process check: {total_procs} python processes, {pipeline_procs} pipeline-related")
                    
                    if total_procs < 2:
                        log_alert("ALERT: Pipeline process may have died! Consider restarting.")
                        # Try to find errors in log
                        if LOG_FILE.exists():
                            log_lines = LOG_FILE.read_text(encoding="utf-8", errors="replace").split("\n")
                            recent_errors = [l for l in log_lines[-20:] if "error" in l.lower() or "exception" in l.lower()]
                            if recent_errors:
                                log_alert(f"Recent errors: {recent_errors[-3:]}")
            
            # Check for area failures
            areas = progress.get("areas", {})
            for area, info in areas.items():
                if info.get("status") in ("failed", "error", "timeout"):
                    if not info.get("_alerted"):
                        log_alert(f"ALERT: Area '{area}' failed with status '{info.get('status')}'. Error: {info.get('error', 'N/A')}")
                        info["_alerted"] = True
                        PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
        
        except json.JSONDecodeError:
            log_alert("ERROR: progress.json is corrupt. Will retry next cycle.")
        except Exception as e:
            log_alert(f"ERROR: {e}")
    
    log_alert("OVERNIGHT MONITOR STOPPED")

if __name__ == "__main__":
    main()
