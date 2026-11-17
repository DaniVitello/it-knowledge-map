"""Review all concept .md files in the vault for completeness.

Checks each concept markdown against quality criteria:
- Not empty (has content beyond frontmatter)
- Has required sections
- "Mis notas" has content between ai:start/ai:end markers
- Content is in Spanish (not English)
- Has wikilinks (connections)
- Has minimum length

Usage:
    py utility/review_concepts.py                    # all areas
    py utility/review_concepts.py "Frontend"         # single area
    py utility/review_concepts.py --report report.md # save report
"""

import os
import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAULT = os.path.join(BASE, "IT-Mind-Map")

REQUIRED_SECTIONS = [
    "Mis notas",
    "Objetivo",
    "Esqueleto",
    "Como funciona",
    "Detalles",
    "Ejemplo",
    "Conexiones",
]

# English words that strongly indicate English content (not Spanish)
ENGLISH_INDICATORS = [
    "the ", "and ", "of the", "is a", "are the", "with the",
    "document", "element", "browser", "rendering", "mode",
    "function", "variable", "type", "class", "interface",
    "module", "component", "server", "client", "request",
    "response", "database", "query", "table", "column",
    "Section ", "Module ", "Chapter ", "Figure ",
]

MIN_CONTENT_LENGTH = 500  # minimum chars beyond frontmatter
MIN_NOTES_LENGTH = 50     # minimum chars in "Mis notas" section


def parse_frontmatter(text):
    """Extract frontmatter and body."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def check_sections(body):
    """Check which required sections are present."""
    found = []
    missing = []
    for sec in REQUIRED_SECTIONS:
        # Flexible match: section name can have variations
        pattern = re.compile(r"^##\s+.*" + re.escape(sec.split()[0]), re.MULTILINE | re.IGNORECASE)
        if pattern.search(body):
            found.append(sec)
        else:
            missing.append(sec)
    return found, missing


def check_notes_content(body):
    """Check if 'Mis notas' has content between ai:start/ai:end."""
    m = re.search(r"<!--\s*ai:start\s*-->(.*?)<!--\s*ai:end\s*-->", body, re.S)
    if not m:
        return False, 0
    content = m.group(1).strip()
    return len(content) >= MIN_NOTES_LENGTH, len(content)


def check_spanish(body):
    """Heuristic: check if content is mostly Spanish, not English."""
    # Remove code blocks
    text = re.sub(r"```.*?```", "", body, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text_lower = text.lower()
    
    en_count = sum(1 for w in ENGLISH_INDICATORS if w in text_lower)
    # Spanish indicators
    es_indicators = ["el ", "la ", "los ", "las ", "de ", "en ", "que ", "por ", "para ", "con "]
    es_count = sum(1 for w in es_indicators if w in text_lower)
    
    # If many English indicators and few Spanish, likely English
    if en_count >= 8 and es_count < 5:
        return False, en_count, es_count
    return True, en_count, es_count


def check_wikilinks(body):
    """Count wikilinks."""
    return len(re.findall(r"\[\[[^\]]+\]\]", body))


def check_uncertainty_markers(body):
    """Check for uncertainty markers that shouldn't be in the output."""
    issues = []
    if re.search(r"\?\?\s*verificar", body, re.IGNORECASE):
        issues.append("uncertainty_marker (?? verificar)")
    if re.search(r"\*{1,2}\s*[Ss]in verificar\s*\*{0,2}\s*:", body):
        issues.append("uncertainty_marker (Sin verificar)")
    if re.search(r"\(sin verificar\)", body, re.IGNORECASE):
        issues.append("uncertainty_marker ((sin verificar))")
    return issues


def review_concept(filepath):
    """Review a single concept file. Returns dict with issues."""
    issues = []
    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e), "issues": ["cannot read file"]}

    fm, body = parse_frontmatter(text)

    # 1. Not empty
    if len(body.strip()) < MIN_CONTENT_LENGTH:
        issues.append(f"empty_or_short ({len(body.strip())} chars)")

    # 2. Required sections
    found, missing = check_sections(body)
    if missing:
        issues.append(f"missing_sections: {', '.join(missing)}")

    # 3. Notes content
    has_notes, notes_len = check_notes_content(body)
    if not has_notes:
        issues.append(f"empty_notes ({notes_len} chars)")

    # 4. Spanish check
    is_es, en_count, es_count = check_spanish(body)
    if not is_es:
        issues.append(f"likely_english (en={en_count}, es={es_count})")

    # 5. Wikilinks
    wl_count = check_wikilinks(body)
    if wl_count < 3:
        issues.append(f"few_wikilinks ({wl_count})")

    # 6. Uncertainty markers
    um_issues = check_uncertainty_markers(body)
    issues.extend(um_issues)

    # 6. Frontmatter
    if "title:" not in fm:
        issues.append("missing_frontmatter_title")
    if "area:" not in fm:
        issues.append("missing_frontmatter_area")

    return {
        "issues": issues,
        "sections_found": len(found),
        "sections_missing": len(missing),
        "notes_len": notes_len,
        "wikilinks": wl_count,
        "body_len": len(body.strip()),
        "is_spanish": is_es,
    }


def review_area(area_name, vault_path):
    """Review all concepts in an area."""
    area_dir = Path(vault_path) / area_name
    if not area_dir.exists():
        return None

    results = []
    for md_file in sorted(area_dir.glob("*.md")):
        if md_file.name.startswith("00 -"):
            continue  # skip index files
        result = review_concept(md_file)
        result["file"] = md_file.name
        result["area"] = area_name
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Review concept .md files for completeness")
    parser.add_argument("area", nargs="?", help="Area name to review (optional, default: all)")
    parser.add_argument("--vault", default=VAULT, help="Path to vault")
    parser.add_argument("--report", help="Save report to file")
    parser.add_argument("--min-notes", type=int, default=MIN_NOTES_LENGTH, help="Min chars in notes")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.exists():
        print(f"Vault not found: {vault}")
        sys.exit(1)

    # Find areas
    areas = []
    if args.area:
        areas = [args.area]
    else:
        areas = sorted([d.name for d in vault.iterdir() if d.is_dir() and not d.name.startswith(".")])

    all_results = []
    summary = defaultdict(lambda: {"total": 0, "ok": 0, "issues": 0})

    for area in areas:
        results = review_area(area, vault)
        if not results:
            continue
        all_results.extend(results)

        area_issues = 0
        for r in results:
            summary[area]["total"] += 1
            if r["issues"]:
                area_issues += 1
            else:
                summary[area]["ok"] += 1
        summary[area]["issues"] = area_issues

    # Print report
    lines = []
    lines.append("=" * 70)
    lines.append("REVIEW DE CONCEPTOS DEL VAULT")
    lines.append("=" * 70)
    lines.append("")

    for area in areas:
        area_results = [r for r in all_results if r["area"] == area]
        if not area_results:
            continue
        s = summary[area]
        lines.append(f"\n## {area}: {s['ok']}/{s['total']} OK, {s['issues']} con issues")
        lines.append("-" * 50)

        for r in area_results:
            if r["issues"]:
                lines.append(f"  [FAIL] {r['file']}")
                for issue in r["issues"]:
                    lines.append(f"         - {issue}")
            else:
                lines.append(f"  [OK]   {r['file']} (notes={r['notes_len']}, wl={r['wikilinks']}, len={r['body_len']})")

    # Totals
    total = sum(s["total"] for s in summary.values())
    ok = sum(s["ok"] for s in summary.values())
    issues = sum(s["issues"] for s in summary.values())
    lines.append("")
    lines.append("=" * 70)
    lines.append(f"TOTAL: {ok}/{total} OK, {issues} con issues")
    lines.append("=" * 70)

    # Issue type breakdown
    issue_types = Counter()
    for r in all_results:
        for issue in r.get("issues", []):
            # extract issue type (before details)
            itype = issue.split("(")[0].split(":")[0].strip()
            issue_types[itype] += 1

    if issue_types:
        lines.append("")
        lines.append("TIPOS DE ISSUES:")
        for itype, count in issue_types.most_common():
            lines.append(f"  {itype}: {count}")

    report = "\n".join(lines)
    print(report)

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"\nReporte guardado en: {args.report}")


if __name__ == "__main__":
    main()