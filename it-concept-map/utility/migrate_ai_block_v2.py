"""Migracion v2: sacar el encabezado '## Mis notas' de delante del bloque AI
y ponerlo como seccion independiente despues del bloque (antes de Relacionados).

USO: py utility\migrate_ai_block_v2.py --vault "IT-Mind-Map" [--dry-run|--apply]
"""
from __future__ import annotations
import argparse, re
from pathlib import Path

START = "<!-- ai:start -->"
END = "<!-- ai:end -->"

def migrate_text(text: str) -> tuple[str, bool]:
    # Patron: '## Mis notas' inmediatamente seguido (con blanks) por el bloque AI
    pat = re.compile(r"## Mis notas\s*\n\s*(<!-- ai:start -->.*?<!-- ai:end -->)", re.S)
    m = pat.search(text)
    if not m:
        return text, False
    block = m.group(1)
    # Quitar '## Mis notas' + bloque de su posicion original
    without = text[:m.start()] + text[m.end():]
    # Insertar '## Mis notas' como seccion independiente antes de '## Relacionados'
    if "## Relacionados" in without:
        new = without.replace("## Relacionados", "## Mis notas\n\n## Relacionados", 1)
    else:
        new = without.rstrip() + "\n\n## Mis notas\n"
    new = re.sub(r"\n{3,}", "\n\n", new)
    return new, True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    vault = Path(args.vault)
    changed = 0
    for md in vault.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        new, did = migrate_text(text)
        if not did:
            continue
        changed += 1
        if args.apply:
            md.write_text(new, encoding="utf-8")
            print(f"MIGRATED: {md}")
        else:
            print(f"WOULD MIGRATE: {md}")
    print(f"\nTotal: {changed} archivos")

if __name__ == "__main__":
    main()
