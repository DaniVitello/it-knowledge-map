#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_ai_markers.py
Agrega <!-- ai:start --> / <!-- ai:end --> alrededor del contenido de "Mis notas"
en todas las notas .md del vault IT-Mind-Map.
"""
import re
from pathlib import Path

VAULT = Path(r"C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map")
START = "<!-- ai:start -->"
END = "<!-- ai:end -->"

def process(path):
    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        return "skip (already has markers)"
    # Buscar la seccion "Mis notas"
    m = re.search(r"(## Mis notas\s*\n)(.*?)(?=\n## |\n---|\Z)", text, re.S)
    if not m:
        return "skip (no 'Mis notas' section)"
    header = m.group(1)
    body = m.group(2)
    # Construir nuevo bloque: header + start + body + end
    new_body = header + START + "\n" + body.strip("\n") + "\n" + END + "\n"
    text = text[:m.start()] + new_body + text[m.end():]
    path.write_text(text, encoding="utf-8", newline="\n")
    return "ok"

def main():
    count = {"ok":0, "skip":0, "err":0}
    for p in sorted(VAULT.rglob("*.md")):
        try:
            r = process(p)
            if r.startswith("ok"):
                count["ok"] += 1
            else:
                count["skip"] += 1
            print(f"{r}: {p.relative_to(VAULT)}")
        except Exception as e:
            count["err"] += 1
            print(f"ERR: {p} -> {e}")
    print(f"\nResumen: ok={count['ok']} skip={count['skip']} err={count['err']}")

if __name__ == "__main__":
    main()
