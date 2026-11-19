import os
import re
import sys

sys.path.insert(0, r"C:/Users/DGVit/Proyectos/IT Career")
from ikm.content.parse import _secciones_de, _canon_seccion, _extraer_frontmatter
from ikm.content.publish_config import PublishConfig

ROOT = r"C:/Users/DGVit/Proyectos/IT Career/IT-Mind-Map"
cfg = PublishConfig()

cat = {"completas": 0, "bloque_vacio": 0, "solo_guion": 0, "otro_sin_secciones": 0}
ejemplos = {"bloque_vacio": [], "solo_guion": [], "otro_sin_secciones": []}

for dirpath, _, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        if not fn.lower().endswith(".md") or fn.startswith("00 - "):
            continue
        p = os.path.join(dirpath, fn)
        t = open(p, encoding="utf-8", errors="replace").read()
        _, cuerpo, _ = _extraer_frontmatter(t)
        m = re.search(r"<!--\s*ai:start\s*-->(.*?)<!--\s*ai:end\s*-->", cuerpo, re.S | re.I)
        b = m.group(1) if m else ""
        _, ausentes = _secciones_de(b)
        if not ausentes:
            cat["completas"] += 1
        elif not b.strip():
            cat["bloque_vacio"] += 1
            ejemplos["bloque_vacio"].append((fn, repr(b[:40])))
        elif b.strip() in ("-", "—", "–"):
            cat["solo_guion"] += 1
            ejemplos["solo_guion"].append((fn, repr(b[:40])))
        else:
            cat["otro_sin_secciones"] += 1
            ejemplos["otro_sin_secciones"].append((fn, repr(b[:60]), len(b)))

print("CATEGORIAS:", cat)
for k, v in ejemplos.items():
    print(f"--- {k} ({len(v)}) ---")
    for e in v[:4]:
        print("   ", e)
