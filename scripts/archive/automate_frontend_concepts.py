#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
automate_frontend_concepts.py
=============================
Automatiza, para uno o varios conceptos del área Frontend:
  1. Crear un notebook en NotebookLM.
  2. Research deep + importar fuentes.
  3. Generar un study guide.
  4. Descargarlo.
  5. Integrarlo en la nota markdown del vault (seccion "Mis notas").

Uso:
    py automate_frontend_concepts.py              # conceptos 2..6
    py automate_frontend_concepts.py 2 3 4         # conceptos especificos
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(r"C:\Users\DGVit\Proyectos\IT Career")
VAULT_FRONTEND = BASE / "IT-Mind-Map" / "02 - Frontend"
TEMP = Path(r"C:\Users\DGVit\AppData\Local\Temp\opencode")
TEMP.mkdir(parents=True, exist_ok=True)

CLI = [sys.executable, "-m", "notebooklm"]


def run_cli(args, timeout=120, label=""):
    print(f"  > {' '.join(args)}", flush=True)
    try:
        r = subprocess.run(CLI + args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] {label or ' '.join(args)}", flush=True)
        return None
    if r.returncode != 0:
        print(f"  [ERR rc={r.returncode}] {label}", flush=True)
        if r.stderr.strip():
            print("   stderr:", r.stderr.strip()[:500], flush=True)
        if r.stdout.strip():
            print("   stdout:", r.stdout.strip()[:500], flush=True)
        return None
    return r.stdout


def parse_concept(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*"(.+?)"', text, re.M)
    title = m.group(1) if m else md_path.stem
    # items bajo "## Que abarca" / "## Qué abarca"
    items = []
    m2 = re.search(r"##\s*Qu.+?abarca\s*\n(.*?)(?=\n##|\n---|\Z)", text, re.S | re.I)
    if m2:
        for line in m2.group(1).splitlines():
            line = line.strip()
            if line.startswith("-"):
                items.append(line.lstrip("- ").strip())
    return title, items


def find_md(num):
    for p in VAULT_FRONTEND.glob("*.md"):
        m = re.match(r"^(\d+)\s*-\s*.+\.md$", p.name)
        if m and int(m.group(1)) == num:
            return p
    return None


def create_notebook(title, num):
    out = run_cli(["create", f"IT - Frontend {num:02d} {title}"], timeout=120, label="create")
    if not out:
        return None
    m = re.search(r"Created notebook:\s*([0-9a-f-]+)", out)
    return m.group(1) if m else None


def do_research(nb_id, query):
    run_cli(["use", nb_id], timeout=60, label="use")
    out = run_cli(
        ["source", "add-research", query, "--mode", "deep", "--import-all"],
        timeout=600, label="research",
    )
    return out is not None


def do_generate(nb_id):
    run_cli(["use", nb_id], timeout=60, label="use")
    out = run_cli(["generate", "report", "--format", "study-guide", "--wait"], timeout=600, label="generate")
    return out is not None and "ready" in (out or "").lower()


def do_download(nb_id, guide_path):
    run_cli(["use", nb_id], timeout=60, label="use")
    out = run_cli(["download", "report", str(guide_path)], timeout=120, label="download")
    return guide_path.exists()


def merge(md_path, guide_path):
    md = md_path.read_text(encoding="utf-8")
    guide = guide_path.read_text(encoding="utf-8").strip()
    for old in ("## Mis notas\n- \n", "## Mis notas\n-\n", "## Mis notas\n-"):
        if old in md:
            new = "## Mis notas\n" + guide + "\n"
            md_path.write_text(md.replace(old, new, 1), encoding="utf-8", newline="\n")
            return True
    return False


def process(num):
    print(f"\n===== Concepto {num:02d} =====", flush=True)
    md_path = find_md(num)
    if not md_path:
        print(f"  No se encontro md para concepto {num}", flush=True)
        return False
    title, items = parse_concept(md_path)
    print(f"  Titulo: {title}", flush=True)
    print(f"  Items: {items}", flush=True)

    query = f"{title}: {', '.join(items)}" if items else title
    query += " fundamentals web development"

    nb_id = create_notebook(title, num)
    if not nb_id:
        print("  Fallo creando notebook", flush=True)
        return False
    print(f"  Notebook: {nb_id}", flush=True)

    if not do_research(nb_id, query):
        print("  Fallo research, continuo igual", flush=True)

    if not do_generate(nb_id):
        print("  Fallo generate", flush=True)
        return False

    guide_path = TEMP / f"study_guide_fe{num:02d}.md"
    if not do_download(nb_id, guide_path):
        print("  Fallo download", flush=True)
        return False

    if merge(md_path, guide_path):
        print(f"  OK: integrado en {md_path.name}", flush=True)
        return True
    else:
        print("  Fallo merge (bloque 'Mis notas' no encontrado)", flush=True)
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nums", nargs="*", type=int, default=[2, 3, 4, 5, 6])
    args = ap.parse_args()

    results = {}
    for n in args.nums:
        ok = process(n)
        results[n] = ok
        time.sleep(2)

    print("\n===== RESUMEN =====", flush=True)
    for n, ok in results.items():
        print(f"  Concepto {n:02d}: {'OK' if ok else 'FAIL'}", flush=True)


if __name__ == "__main__":
    main()
