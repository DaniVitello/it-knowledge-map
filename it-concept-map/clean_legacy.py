
import json, re, os
from pathlib import Path

manifest = json.loads(Path("workdir/manifest.json").read_text(encoding="utf-8"))
vault = Path("C:/Users/DGVit/Proyectos/IT Career/IT-Mind-Map").resolve()
# Actually, let me use config
import yaml
cfg = yaml.safe_load(open("config.yaml"))
vault = Path(cfg["vault_path"])

legacy = [c for c in manifest["concepts"] if c.get("status") == "legacy"]
print(f"Legacy concepts to clean: {len(legacy)}")

cleaned = 0
for c in legacy:
    fpath = vault / c["path"]
    if not fpath.exists():
        print(f"  NOT FOUND: {fpath}")
        continue
    content = fpath.read_text(encoding="utf-8")
    # Replace everything between ai:start and ai:end with empty
    new_content = re.sub(r'(<!-- ai:start -->).*?(<!-- ai:end -->)', r'\1\n\2', content, flags=re.S)
    if new_content != content:
        fpath.write_text(new_content, encoding="utf-8")
        cleaned += 1
    else:
        print(f"  No AI block found: {c['id']}")

print(f"Cleaned: {cleaned}/{len(legacy)}")
