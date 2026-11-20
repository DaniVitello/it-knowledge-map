"""Arma el directorio de deploy para HF Spaces: subset de ikm + release completo."""
import json, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # ikm/
dst_ikm = HERE / "ikm"
if dst_ikm.exists(): shutil.rmtree(dst_ikm)
dst_ikm.mkdir()
(dst_ikm / "__init__.py").write_text("")  # ikm es namespace package en el repo; package regular en el deploy
for sub in ("contracts", "api"):
    shutil.copytree(ROOT / sub, dst_ikm / sub, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
rel_src = ROOT / "web" / "public" / "release"
rid = json.loads((rel_src / "manifest.json").read_text(encoding="utf-8"))["release_id"]
if (HERE / "release").exists(): shutil.rmtree(HERE / "release")
shutil.copytree(rel_src, HERE / "release" / rid)
print("Deploy armado: ikm/ (contracts+api) + release/" + rid)
