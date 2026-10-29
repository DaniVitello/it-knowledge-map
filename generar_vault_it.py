#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_vault_it.py
===================
Genera un vault de Obsidian (mind map del mercado IT) a partir de los .txt
con los conceptos de cada área.

Uso:
    python generar_vault_it.py                      # lee los .txt de la carpeta actual
    python generar_vault_it.py ./mis_txt            # carpeta de entrada
    python generar_vault_it.py ./mis_txt -o ./IT    # carpeta de salida
    python generar_vault_it.py --force              # pisa también las notas de concepto

Notas:
  * Los índices (por área y maestro) se regeneran siempre.
  * Las notas de concepto NO se pisan si ya existen (para no perder lo que
    hayas escrito en "Mis notas"), salvo que uses --force.
  * Los títulos se leen tal cual de los .txt: no se reescribe ninguno.
  * Solo usa la librería estándar (Python 3.8+).
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# 1) ÁREAS  (prefijo del título normalizado, id, carpeta, nombre, slug de tag)
# ---------------------------------------------------------------------------
AREAS = [
    ("software engineering", "se",  "01 - Software Engineering",         "Software Engineering",      "software-engineering"),
    ("frontend",             "fe",  "02 - Frontend",                     "Frontend",                  "frontend"),
    ("backend",              "be",  "03 - Backend",                      "Backend",                   "backend"),
    ("database",             "db",  "04 - Database & Data Analytics",    "Database / Data Analytics", "database-data-analytics"),
    ("networking",           "net", "05 - Networking & Internet",        "Networking / Internet",     "networking-internet"),
    ("operating systems",    "os",  "06 - Operating Systems & Linux",    "Operating Systems / Linux", "operating-systems-linux"),
    ("ai engineering",       "ai",  "07 - AI Engineering",               "AI Engineering",            "ai-engineering"),
    ("ux",                   "ux",  "08 - UX & UI",                      "UX / UI",                   "ux-ui"),
    ("product management",   "pdm", "09 - Product Management",           "Product Management",        "product-management"),
    ("project management",   "prj", "10 - Project Management",           "Project Management",        "project-management"),
]

MASTER_NAME = "00 - Índice Maestro IT"

# ---------------------------------------------------------------------------
# 2) RELACIONES CURADAS ENTRE CONCEPTOS
#    Cada línea es un grupo: todos los miembros se enlazan entre sí.
#    Formato: <id de área><número de concepto>  (ej: be12 = Backend #12 = SQL)
# ---------------------------------------------------------------------------
GROUPS = """
# --- Web / HTTP / cliente-servidor ---
fe1 be1 net1
fe1 be2 net16 net18 net19 net20 net21
net16 net17 net21 net22
fe16 be6
fe10 fe11 be7 se9
net22 os14
fe24 fe23 net25

# --- Concurrencia / asincronía / procesos ---
se11 be20 os4 fe9
os3 os4 os5 se11
be3 os3 os20
os13 os14 os19

# --- Datos / SQL / modelado ---
be12 db4 db5 db6
be15 db10 db11
be13 db2 db3 db7 db8
be11 db3 db12 db13
be14 db3 be13
db9 db12 be11
db14 db15 db16 db17
db16 db17 ai17
db18 db19 db20
db20 db21 db22 db23 db24
db22 pdm17 ux23 prj24
db23 db24 ux12
ai15 ai9 db13

# --- Seguridad / auth ---
fe19 be16 be17
be16 be17 be18 se24
be18 se24 ai21 net17 net24
net23 net24 net25

# --- Caching / performance / escalado ---
be19 net25 fe23 fe18
be21 be25 se28 db25
be25 se28 se27 net25

# --- Observabilidad / testing / entrega ---
be22 se26 ai22 os23
se17 be23 fe22
be24 se25 os24 os25 ai23
se12 se25
os24 os25 be24

# --- Arquitectura / diseño de software ---
se22 be10 fe25 ai25
se22 se23 se8 se7
se13 se14 se15 se16 se19 se20
se2 se3 se4
se5 se6 se7
se10 be8 be9
se1 be4 be5 ai2
se9 ai12 be7

# --- Frontend interno ---
fe2 fe3 fe4 fe5
fe6 fe7 fe8 fe9
fe13 fe14 fe15 fe25
fe15 fe18 fe11
fe17 fe19 fe20

# --- Networking interno ---
net2 net3 net8 net10 net14
net4 net5 net6
net11 net12 net13 net14
net15 net2 net4 net16
net7 net2 net1
os22 net6 net4 os14

# --- Sistemas operativos interno ---
os1 os2 os11
os3 os6 os7
os8 os9 os10
os16 os17 os18 os19
os15 os16 os21

# --- AI interno ---
ai1 ai4 ai5 ai3
ai5 ai6 ai7 ai8 ai9
ai10 ai11 ai13 ai18 ai19
ai14 ai15 ai9 ai18
ai16 ai17 ai13 ai19
ai20 ai21 ai22
ai7 ai24 ai23
ai1 ai4 db21

# --- UX / UI ---
fe20 ux20
fe13 fe25 ux16 ux17
fe4 ux19
ux18 fe18
ux2 ux3 ux4 ux5 pdm3 pdm5
ux6 ux7 ux9
ux10 ux11 ux8
ux12 ux13 ux14 ux15
ux21 ux22 ux23
ux24 ux12 ux21
ux25 pdm1 pdm6

# --- Product ---
pdm1 pdm2 pdm3 pdm4
pdm6 pdm7 pdm8 pdm9 pdm10 pdm25
pdm14 pdm15 pdm16
pdm17 pdm18 pdm19 pdm20
pdm21 pdm15 pdm22 pdm24
pdm11 prj11
pdm12 pdm13 prj3
pdm23 prj21 se29
pdm10 prj9 prj10 prj19

# --- Project ---
prj1 prj2 prj3 prj4
prj5 prj6 prj7 prj8 prj9 prj10
prj13 prj14 prj15
prj16 prj17 prj18 se30
prj25 se30 prj24
prj12 prj23
prj20 prj21 prj22
prj8 se30 prj24
se29 se30 prj22
"""

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def safe(s):
    """Nombre de archivo seguro (Obsidian/Windows/Mac/Linux)."""
    s = s.replace("/", "-")
    s = re.sub(r'[\\:*?"<>|#^\[\]]', "", s)
    s = re.sub(r"\s+", " ", s).strip().rstrip(".")
    return s


def yq(s):
    """String YAML entre comillas dobles."""
    return json.dumps(s, ensure_ascii=False)


class Area:
    def __init__(self, prefix, aid, folder, name, slug, order):
        self.prefix, self.id, self.folder = prefix, aid, folder
        self.name, self.slug, self.order = name, slug, order
        self.notes = []       # texto introductorio del .txt
        self.concepts = []

    @property
    def index_stem(self):
        return f"00 - Índice {safe(self.name)}"

    @property
    def index_link(self):
        return f"[[{self.folder}/{self.index_stem}|Índice {self.name}]]"


class Concept:
    def __init__(self, area, num, title, abarca):
        self.area, self.num, self.title, self.abarca = area, num, title, abarca

    @property
    def stem(self):
        return f"{self.num:02d} - {safe(self.title)}"

    @property
    def link(self):
        return f"[[{self.area.folder}/{self.stem}|{self.title}]]"

    @property
    def key(self):
        return (self.area.id, self.num)


def detect_area(first_line):
    n = norm(first_line)
    for i, (prefix, aid, folder, name, slug) in enumerate(AREAS):
        if n == prefix or n.startswith(prefix + " "):
            return Area(prefix, aid, folder, name, slug, i)
    return None


def parse_txt(path):
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    first_idx = next((i for i, l in enumerate(lines) if l.strip()), None)
    if first_idx is None:
        return None, [], []
    area = detect_area(lines[first_idx])
    if area is None:
        return None, [], []

    rows, notes = [], []
    for i, line in enumerate(lines):
        if i == first_idx or not line.strip():
            continue
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) >= 3 and parts[0].isdigit():
            rows.append((int(parts[0]), parts[1], parts[2]))
            continue
        if parts[0] == "#":  # fila de encabezado
            continue
        m = re.match(r"^(\d+)\s+(.+?)\s{2,}(.+)$", line.strip())
        if m:
            rows.append((int(m.group(1)), m.group(2).strip(), m.group(3).strip()))
            continue
        notes.append(line.strip())
    return area, sorted(rows), notes


# ---------------------------------------------------------------------------
# Relaciones
# ---------------------------------------------------------------------------

def build_relations(areas):
    by_key = {c.key: c for a in areas for c in a.concepts}
    rel = defaultdict(set)

    # grupos curados
    for raw in GROUPS.splitlines():
        raw = raw.split("#", 1)[0].strip()
        if not raw:
            continue
        members = []
        for tok in raw.split():
            m = re.fullmatch(r"([a-z]+)(\d+)", tok)
            if not m:
                print(f"  ! token inválido en GROUPS: {tok}", file=sys.stderr)
                continue
            key = (m.group(1), int(m.group(2)))
            if key in by_key:
                members.append(key)
            elif any(a.id == key[0] for a in areas):
                print(f"  ! relación a concepto inexistente: {tok}", file=sys.stderr)
        for a in members:
            for b in members:
                if a != b:
                    rel[a].add(b)

    # mismo título normalizado en áreas distintas
    same = defaultdict(list)
    for c in by_key.values():
        same[norm(c.title)].append(c)
    for group in same.values():
        for a in group:
            for b in group:
                if a.area is not b.area:
                    rel[a.key].add(b.key)

    return by_key, rel


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_concept(c, area, by_key, rel):
    total = len(area.concepts)
    items = [x.strip() for x in c.abarca.split(",") if x.strip()]
    related = sorted(
        (by_key[k] for k in rel.get(c.key, ())),
        key=lambda x: (x.area.order, x.num),
    )

    out = [
        "---",
        f"title: {yq(c.title)}",
        f"area: {yq(area.name)}",
        f"numero: {c.num}",
        f"aliases: [{yq(c.title)}]",
        f"tags: [concepto, it/{area.slug}]",
        "---",
        f"# {c.title}",
        "",
        f"> **Área:** {area.index_link} · **Concepto {c.num} de {total}**",
        "",
        "## Qué abarca",
    ]
    out += [f"- {i}" for i in items]
    out += ["", "## Mis notas", "- ", ""]

    if related:
        out += ["## Relacionados"]
        for r in related:
            tag = "" if r.area is area else f" · *{r.area.name}*"
            out.append(f"- {r.link}{tag}")
        out.append("")

    idx = c.num - 1
    prev_c = area.concepts[idx - 1] if idx > 0 else None
    next_c = area.concepts[idx + 1] if idx < total - 1 else None
    nav = []
    nav.append(f"← {prev_c.link}" if prev_c else "")
    nav.append(area.index_link)
    nav.append(f"{next_c.link} →" if next_c else "")
    out += ["---", " · ".join(p for p in nav if p), ""]
    return "\n".join(out)


def render_area_index(area, by_key, rel):
    counts = Counter()
    for c in area.concepts:
        for k in rel.get(c.key, ()):
            other = by_key[k]
            if other.area is not area:
                counts[other.area] += 1

    out = [
        "---",
        f"title: {yq('Índice — ' + area.name)}",
        f"tags: [indice, it/{area.slug}]",
        "---",
        f"# {area.name}",
        "",
        f"↑ [[{MASTER_NAME}|Índice Maestro IT]]",
        "",
    ]
    for n in area.notes:
        out.append(f"> {n}")
    if area.notes:
        out.append("")
    out.append(f"## Conceptos ({len(area.concepts)})")
    for c in area.concepts:
        out.append(f"- {c.num:02d} · {c.link} — {c.abarca}")
    if counts:
        out += ["", "## Áreas conectadas"]
        for other, n in counts.most_common():
            out.append(f"- {other.index_link} ({n} enlaces)")
    out.append("")
    return "\n".join(out)


def render_master(areas):
    total = sum(len(a.concepts) for a in areas)
    out = [
        "---",
        'title: "Índice Maestro IT"',
        "tags: [indice, it]",
        "---",
        "# Índice Maestro IT",
        "",
        f"Mapa de {total} conceptos fundamentales del mercado IT, en {len(areas)} áreas. "
        "Abrí la **Graph view** para ver el mind map completo.",
        "",
        "## Áreas",
    ]
    for a in areas:
        out.append(f"- {a.index_link} — {len(a.concepts)} conceptos")
    for a in areas:
        out += ["", f"## {a.name}", f"↳ {a.index_link}", ""]
        for c in a.concepts:
            out.append(f"- {c.num:02d} · {c.link}")
    out.append("")
    return "\n".join(out)


def write(path, content, overwrite=True):
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Genera el vault de Obsidian del mind map IT.")
    ap.add_argument("input", nargs="?", default=".", help="carpeta con los .txt (default: .)")
    ap.add_argument("-o", "--output", default="IT-Mind-Map", help="carpeta de salida (default: IT-Mind-Map)")
    ap.add_argument("--force", action="store_true", help="pisar notas de concepto existentes")
    args = ap.parse_args()

    in_dir, out_dir = Path(args.input), Path(args.output)
    if not in_dir.is_dir():
        sys.exit(f"No existe la carpeta de entrada: {in_dir}")

    areas = []
    for f in sorted(in_dir.glob("*.txt")):
        area, rows, notes = parse_txt(f)
        if area is None:
            print(f"- Ignorado (no reconozco el área): {f.name}")
            continue
        area.notes = notes
        area.concepts = [Concept(area, n, t, a) for n, t, a in rows]
        nums = [c.num for c in area.concepts]
        if nums != list(range(1, len(nums) + 1)):
            print(f"  ! Numeración irregular en {area.name}: {nums}", file=sys.stderr)
        areas.append(area)
        print(f"+ {area.name}: {len(area.concepts)} conceptos ({f.name})")

    if not areas:
        sys.exit("No encontré ningún .txt válido.")
    areas.sort(key=lambda a: a.order)

    by_key, rel = build_relations(areas)

    created = skipped = 0
    for a in areas:
        folder = out_dir / a.folder
        write(folder / f"{a.index_stem}.md", render_area_index(a, by_key, rel))
        for c in a.concepts:
            ok = write(folder / f"{c.stem}.md", render_concept(c, a, by_key, rel), overwrite=args.force)
            created += ok
            skipped += not ok
    write(out_dir / f"{MASTER_NAME}.md", render_master(areas))

    links = sum(len(v) for v in rel.values())
    print(f"\nListo → {out_dir.resolve()}")
    print(f"  {len(areas)} áreas · {created} notas creadas · {skipped} existentes sin tocar · {links} enlaces cruzados")
    print(f"  Abrí '{MASTER_NAME}.md' para empezar.")


if __name__ == "__main__":
    main()
