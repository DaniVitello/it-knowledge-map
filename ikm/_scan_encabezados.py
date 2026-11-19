import os
import re
import collections

ROOT = r"C:/Users/DGVit/Proyectos/IT Career/IT-Mind-Map"
enc = collections.Counter()
niveles = collections.Counter()
por_nota = collections.Counter()

for dirpath, _, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        if not fn.lower().endswith(".md") or fn.startswith("00 - "):
            continue
        t = open(os.path.join(dirpath, fn), encoding="utf-8", errors="replace").read()
        m = re.search(r"<!--\s*ai:start\s*-->(.*?)<!--\s*ai:end\s*-->", t, re.S | re.I)
        b = m.group(1) if m else ""
        n = 0
        for mm in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", b, re.M):
            niveles[len(mm.group(1))] += 1
            enc[mm.group(2).strip()] += 1
            n += 1
        por_nota[n] += 1

print("--- encabezados dentro del bloque AI (frecuencia) ---")
for k, v in enc.most_common(30):
    print(f"  {v:4d}  {k!r}")
print("--- niveles ---", dict(niveles))
print("--- encabezados por nota ---", dict(sorted(por_nota.items())))
