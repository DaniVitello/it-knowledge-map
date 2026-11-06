"""Golden set selector: picks 8-10 diverse concepts for prompt iteration."""
import json
from pathlib import Path
from collections import defaultdict

def select_golden_set(manifest_path, n=8):
    m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    by_area = defaultdict(list)
    for c in m["concepts"]:
        by_area[c["area"]].append(c)
    
    selected = []
    areas = sorted(by_area.keys())
    # Round-robin across areas, picking first from each
    i = 0
    while len(selected) < n and areas:
        progressed = False
        for a in areas:
            if by_area[a] and len(selected) < n:
                selected.append(by_area[a].pop(0))
                progressed = True
        if not progressed:
            break
    return selected

if __name__ == "__main__":
    import sys
    manifest = sys.argv[1] if len(sys.argv) > 1 else "workdir/manifest.json"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    selected = select_golden_set(manifest, n)
    print(f"Golden set: {len(selected)} conceptos")
    for c in selected:
        print(f"  {c['id']} | {c['area']} | {c['status']}")
    # Save to file
    out = Path("workdir/golden_set.json")
    out.write_text(json.dumps(selected, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Guardado en {out}")
