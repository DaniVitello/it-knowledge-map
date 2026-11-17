
import subprocess, difflib
pairs = [
  ("it-concept-map/backend.py","it-concept-map/main/backend.py"),
  ("it-concept-map/runner.py","it-concept-map/main/runner.py"),
  ("it-concept-map/synthesis.py","it-concept-map/main/synthesis.py"),
  ("it-concept-map/writer.py","it-concept-map/main/writer.py"),
  ("it-concept-map/llm_groq.py","it-concept-map/main/llm_groq.py"),
  ("it-concept-map/cli.py","it-concept-map/main/cli.py"),
  ("it-concept-map/models.py","it-concept-map/main/models.py"),
  ("it-concept-map/registry.py","it-concept-map/main/registry.py"),
  ("it-concept-map/research.py","it-concept-map/main/research.py"),
  ("it-concept-map/state.py","it-concept-map/main/state.py"),
  ("it-concept-map/validation.py","it-concept-map/main/validation.py"),
  ("it-concept-map/areas.py","it-concept-map/main/areas.py"),
  ("it-concept-map/log.py","it-concept-map/main/log.py"),
  ("it-concept-map/pilot.py","it-concept-map/exe/pilot.py"),
  ("it-concept-map/run_pipeline.py","it-concept-map/exe/run_pipeline.py"),
  ("it-concept-map/run_all_areas.py","it-concept-map/exe/run_all_areas.py"),
  ("it-concept-map/run_area.py","it-concept-map/exe/run_area.py"),
  ("it-concept-map/run_missing.py","it-concept-map/exe/run_missing.py"),
  ("it-concept-map/run_pending.py","it-concept-map/exe/run_pending.py"),
  ("it-concept-map/retry_failed.py","it-concept-map/exe/retry_failed.py"),
  ("it-concept-map/eval_concept.py","it-concept-map/exe/eval_concept.py"),
]
for old_path, new_path in pairs:
    old = subprocess.run(["git","cat-file","blob",f"refs/backup/main:{old_path}"], capture_output=True).stdout
    new = subprocess.run(["git","cat-file","blob",f"HEAD:{new_path}"], capture_output=True).stdout
    if old == new:
        print("OK  ", new_path)
        continue
    old_lines = old.decode("utf-8", errors="replace").splitlines()
    new_lines = new.decode("utf-8", errors="replace").splitlines()
    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    print(f"DIFF {new_path} old={len(old_lines)} new={len(new_lines)} +{added} -{removed}")
