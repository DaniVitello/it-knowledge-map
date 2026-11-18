"""Regenerar bloque AI en .md que lo perdieron, usando synthesis.json.

USO: py utility\regen_ai_block.py --vault "IT-Mind-Map" --workdir "it-concept-map/workdir" [--dry-run|--apply]
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--workdir", default="workdir")
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    vault = Path(args.vault)
    workdir = Path(args.workdir)
    concepts_dir = workdir / "concepts"
    # Build title -> synthesis markdown map
    title_map = {}
    for cdir in concepts_dir.iterdir():
        if not cdir.is_dir():
            continue
        sp = cdir / "synthesis.json"
        if not sp.exists():
            continue
        try:
            d = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        title = d.get("title")
        md = d.get("markdown", "")
        if title and md:
            title_map[title] = md

    fixed = 0
    for md_path in vault.rglob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        if "<!-- ai:start -->" in text:
            continue  # already has block
        # extract title from frontmatter
        m = re.search(r'^title:\s*"(.+?)"', text, re.MULTILINE)
        if not m:
            continue
        title = m.group(1)
        if title not in title_map:
            continue
        ai_md = title_map[title]
        block = "<!-- ai:start -->\n" + ai_md.strip() + "\n<!-- ai:end -->"
        # Insert after "## Mis notas"
        if "## Mis notas" in text:
            new = text.replace("## Mis notas", "## Mis notas\n\n" + block, 1)
        else:
            new = text.rstrip() + "\n\n" + block + "\n"
        fixed += 1
        if args.apply:
            md_path.write_text(new, encoding="utf-8")
            print(f"FIXED: {md_path}")
        else:
            print(f"WOULD FIX: {md_path}")
    print(f"\nTotal: {fixed} archivos")

if __name__ == "__main__":
    main()
