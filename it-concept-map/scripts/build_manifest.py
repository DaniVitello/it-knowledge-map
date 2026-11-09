
import os, json
from pathlib import Path
from collections import Counter

vault = Path("C:/Users/DGVit/Proyectos/IT Career/IT-Mind-Map")
workdir = Path("C:/Users/DGVit/Proyectos/IT Career/it-concept-map/workdir")
manifest_path = workdir / "manifest.json"

concepts = []
for md in vault.rglob("*.md"):
    rel = md.relative_to(vault)
    parts = str(rel).replace("\\", "/")
    if any(p.startswith("00 -") for p in parts.split("/")):
        continue
    if md.name.startswith("_") or md.name == "README.md":
        continue
    
    try:
        text = md.read_text(encoding="utf-8", errors="replace")
    except:
        continue
    
    has_marker = "<!-- ai:start -->" in text
    
    concept_id = str(rel).replace("\\", "/").replace(".md", "")
    area = parts.split("/")[0] if "/" in parts else "root"
    
    pipeline_dir = workdir / ".pipeline" / concept_id.replace("/", "-").replace(" ", "-")
    has_pipeline_dir = pipeline_dir.exists()
    
    if has_marker:
        status = "marked"
    else:
        status = "pending"
    
    concepts.append({
        "id": concept_id,
        "path": parts,
        "area": area,
        "has_marker": has_marker,
        "has_pipeline_dir": has_pipeline_dir,
        "status": status,
        "phases": {
            "research": {"status": "done" if (has_pipeline_dir or has_marker) else "pending", "artifact": None},
            "synthesis": {"status": "pending", "artifact": None},
            "validation": {"status": "pending", "score": None, "issues": []},
            "write": {"status": "done" if has_marker else "pending", "file": parts}
        },
        "last_error": None,
        "last_run": None
    })

manifest = {
    "version": "1.0",
    "created": __import__("datetime").datetime.now().isoformat(),
    "total_concepts": len(concepts),
    "status_counts": {},
    "concepts": concepts
}
manifest["status_counts"] = dict(Counter(c["status"] for c in concepts))

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Manifest created: {len(concepts)} concepts")
print(f"Status counts: {manifest['status_counts']}")
# Print area breakdown
areas = Counter(c["area"] for c in concepts)
for a, n in sorted(areas.items()):
    statuses = Counter(c["status"] for c in concepts if c["area"] == a)
    print(f"  {a}: {n} ({dict(statuses)})")
