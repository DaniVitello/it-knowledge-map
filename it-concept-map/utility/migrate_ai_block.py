"""Migracion: sacar el bloque <!-- ai:start -->...<!-- ai:end --> de dentro de
## Mis notas y ponerlo en una seccion propia.

USO: py utility\\migrate_ai_block.py --vault "IT-Mind-Map" [--dry-run]

No modifica archivos sin --apply. Por defecto solo reporta.
"""
from __future__ import annotations
import argparse, re
from pathlib import Path

START = "<!-- ai:start -->"
END = "<!-- ai:end -->"

def migrate_text(text: str) -> tuple[str, bool]:
    if START not in text or END not in text:
        return text, False
    # Extraer el bloque completo (incluyendo marcadores)
    m = re.search(re.escape(START) + r".*?" + re.escape(END), text, re.S)
    if not m:
        return text, False
    block = m.group(0)
    # Quitar el bloque del texto original
    without = text[:m.start()] + text[m.end():]
    # Quitar el heading "## Mis notas" si quedo vacio/inmediato
    # Insertar el bloque despues del frontmatter + titulo + navegacion inicial.
    # Estrategia: insertar antes de "## Relacionados" si existe, sino al final.
    if "## Relacionados" in without:
        new = without.replace("## Relacionados", block + "\n\n## Relacionados", 1)
    else:
        new = without.rstrip() + "\n\n" + block + "\n"
    # Limpiar lineas vacias dobles
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
        # Solo migrar si el bloque esta dentro de Mis notas
        if "## Mis notas" not in text:
            continue
        # Verificar que el bloque este dentro de Mis notas
        idx_mis = text.find("## Mis notas")
        idx_start = text.find(START)
        if idx_start < idx_mis:
            continue  # bloque ya esta fuera
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
