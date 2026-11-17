"""Mark concepts with review issues as failed for re-processing.

Reads the review report and changes estado.json of concepts with issues
to 'failed' (reason: quality_issues) so they can be retried.

Usage:
    py utility/mark_issues_failed.py --vault "C:/Users/DGVit/Proyectos/IT Career/IT-Mind-Map"
    py utility/mark_issues_failed.py --vault "..." --dry-run
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.join(BASE, "it-concept-map")
sys.path.insert(0, os.path.join(BASE, "it-concept-map"))
sys.path.insert(0, BASE)
import main.cli as cli_mod
cli = cli_mod

VAULT_DEFAULT = os.path.join(BASE, "IT-Mind-Map")
WORKDIR_DEFAULT = os.path.join(BASE, "it-concept-map", "workdir")

# Import review logic
sys.path.insert(0, os.path.join(BASE, "it-concept-map", "utility"))
import review_concepts as rc


def main():
    parser = argparse.ArgumentParser(description="Mark concepts with review issues as failed")
    parser.add_argument("--vault", default=VAULT_DEFAULT)
    parser.add_argument("--workdir", default=WORKDIR_DEFAULT)
    parser.add_argument("--dry-run", action="store_true", help="Show what would be marked without changing")
    args = parser.parse_args()

    vault = Path(args.vault)
    workdir = Path(args.workdir)
    cfg = cli._load_cfg(type("Args", (), {"config": os.path.join(BASE, "it-concept-map", "config.yaml"), "workdir": None, "vault": None})())
    concepts = cli._load_concepts(cfg)

    # Build id -> concept map
    concept_map = {c.id: c for c in concepts}

    # Run review on all areas
    areas = sorted([d.name for d in vault.iterdir() if d.is_dir() and not d.name.startswith(".")])
    all_issues = []
    for area in areas:
        results = rc.review_area(area, vault)
        if not results:
            continue
        for r in results:
            if r["issues"]:
                all_issues.append(r)

    print(f"Conceptos con issues: {len(all_issues)}")

    marked = 0
    for r in all_issues:
        # Find concept id by matching file name to concept
        fname = r["file"]
        # Remove .md extension
        title = fname.replace(".md", "").strip()
        # Remove leading number prefix (e.g., "12 - Git - Version Control" -> "Git - Version Control")
        title_clean = re.sub(r"^\d+\s*-\s*", "", title).strip() if False else title
        # Remove number and dash prefix
        import re
        title_clean = re.sub(r"^\d+\s*-\s*", "", title).strip()
        # Normalize separators for matching
        def normalize(s):
            return re.sub(r"[\s/\-&]+", " ", s).strip().lower()
        title_norm = normalize(title_clean)
        # Find concept by title AND area (case-insensitive, normalized)
        import re
        # Extract area name: remove leading number, lowercase
        area_clean = re.sub(r"^\d+\s*-\s*", "", r["area"]).strip().lower()
        # Map vault area names to concept area names
        area_map = {
            "software engineering": "software engineering",
            "frontend": "frontend",
            "backend": "backend",
            "database & data analytics": "database / data analytics",
            "networking & internet": "networking / internet",
            "operating systems & linux": "operating systems / linux",
            "ai engineering": "ai engineering",
            "ux & ui": "ux / ui",
            "product management": "product management",
            "project management": "project management",
        }
        target_area = area_map.get(area_clean, area_clean)

        matched = None
        for c in concepts:
            ct = normalize(c.title)
            ca = c.area.lower().strip()
            if ct == title_norm and ca == target_area:
                matched = c
                break
        if not matched:
            for c in concepts:
                ct = normalize(c.title)
                ca = c.area.lower().strip()
                if (ct in title_norm or title_norm in ct) and ca == target_area:
                    matched = c
                    break

        if not matched:
            print(f"  [SKIP] No concept found for: {fname}")
            continue

        st_path = workdir / "concepts" / matched.id / "estado.json"
        if not st_path.exists():
            print(f"  [SKIP] No estado.json for: {matched.id}")
            continue

        st = json.loads(st_path.read_text())
        old_status = st.get("status", "?")

        if args.dry_run:
            print(f"  [DRY-RUN] {matched.id}: {old_status} -> failed (issues: {r['issues']})")
        else:
            st["status"] = "failed"
            st["last_good_state"] = old_status
            st.setdefault("phase_data", {})
            st["phase_data"]["failed_phase"] = "quality_review"
            st["phase_data"]["failed_reason"] = "quality_issues"
            st["error"] = f"Review issues: {', '.join(r['issues'])}"
            st_path.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  [MARKED] {matched.id}: {old_status} -> failed")
        marked += 1

    print(f"\nTotal marcados: {marked}")
    if args.dry_run:
        print("(dry-run: no se hicieron cambios)")


if __name__ == "__main__":
    main()