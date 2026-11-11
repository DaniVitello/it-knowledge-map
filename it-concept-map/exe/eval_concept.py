
"""eval_concept.py — Evalua la calidad de un concepto completado por el pipeline.

Uso:
    py eval_concept.py <concept-id>
    py eval_concept.py --all
    py eval_concept.py --area "Software Engineering"

Retorna score 0-100 y lista de issues.
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map")
import cli

cfg = cli._load_cfg(type("Args", (), {"config": "config.yaml", "workdir": None, "vault": None})())
concepts = {c.id: c for c in cli._load_concepts(cfg)}
vault = Path(cfg.vault_path)
workdir = Path(cfg.workdir)

REQUIRED_SECTIONS = ["que abarca", "key ideas", "relacionados", "fuentes"]
MARKERS = {"start": "<!-- ai:start -->", "end": "<!-- ai:end -->"}

def eval_concept(concept_id):
    issues = []
    score = 100
    
    concept = concepts.get(concept_id)
    if not concept:
        return {"concept_id": concept_id, "score": 0, "issues": ["Concept not in registry"], "status": "not_found"}
    
    file_path = vault / concept_id
    if not file_path.exists():
        return {"concept_id": concept_id, "score": 0, "issues": ["File not found in vault"], "status": "missing"}
    
    content = file_path.read_text(encoding="utf-8")
    
    # Check 1: AI block markers present
    if MARKERS["start"] not in content:
        issues.append("MISSING_AI_BLOCK: No <!-- ai:start --> marker found")
        score -= 20
    if MARKERS["end"] not in content:
        issues.append("MISSING_AI_END: No <!-- ai:end --> marker found")
        score -= 20
    
    # Check 2: Extract AI block
    ai_block = ""
    if MARKERS["start"] in content and MARKERS["end"] in content:
        start_idx = content.index(MARKERS["start"]) + len(MARKERS["start"])
        end_idx = content.index(MARKERS["end"])
        ai_block = content[start_idx:end_idx].strip()
    
    if not ai_block:
        issues.append("EMPTY_AI_BLOCK: AI block is empty")
        score -= 30
    
    # Check 3: Required sections in AI block
    ai_lower = ai_block.lower()
    for section in REQUIRED_SECTIONS:
        if section not in ai_lower:
            issues.append(f"MISSING_SECTION: '{section}' not found in AI block")
            score -= 10
    
    # Check 4: Minimum content length
    if len(ai_block) < 200:
        issues.append(f"TOO_SHORT: AI block is only {len(ai_block)} chars (min 200)")
        score -= 15
    
    # Check 5: Wikilinks outside AI block preserved (check that manual wikilinks exist)
    outside_ai = content
    if MARKERS["start"] in content:
        outside_ai = content[:content.index(MARKERS["start"])]
    if MARKERS["end"] in content:
        outside_end = content[content.index(MARKERS["end"]) + len(MARKERS["end"]):]
        outside_ai = outside_ai + outside_end
    
    manual_wikilinks = re.findall(r'\[\[([^\]]+)\]\]', outside_ai)
    if not manual_wikilinks:
        issues.append("NO_MANUAL_WIKILINKS: No wikilinks found outside AI block (may be OK for some concepts)")
        score -= 5
    
    # Check 6: No wikilinks inside AI block (v1 spec: LLM does not generate wikilinks)
    ai_wikilinks = re.findall(r'\[\[([^\]]+)\]\]', ai_block)
    if ai_wikilinks:
        issues.append(f"AI_WIKILINKS_FOUND: LLM generated {len(ai_wikilinks)} wikilinks in AI block (spec says v1 should not)")
        score -= 10
    
    # Check 7: Frontmatter valid
    if content.startswith("---"):
        fm_end = content.find("---", 3)
        if fm_end > 0:
            frontmatter = content[3:fm_end].strip()
            if "title:" not in frontmatter and "concept_id:" not in frontmatter:
                issues.append("WEAK_FRONTMATTER: No title or concept_id in frontmatter")
                score -= 5
        else:
            issues.append("BROKEN_FRONTMATTER: Unclosed frontmatter")
            score -= 10
    else:
        issues.append("NO_FRONTMATTER: File does not start with ---")
        score -= 10
    
    # Check 8: Pipeline state
    state_file = workdir / ".pipeline" / concept_id / "state.json"
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
            if state.get("status") != "completed":
                issues.append(f"PIPELINE_STATUS: {state.get('status', 'unknown')} (expected completed)")
                score -= 10
        except:
            issues.append("CORRUPT_STATE: Cannot parse state.json")
            score -= 5
    else:
        issues.append("NO_STATE_FILE: No pipeline state found")
        score -= 5
    
    # Check 9: Research artifacts
    research_dir = workdir / ".pipeline" / concept_id / "research"
    if research_dir.exists():
        sources = list(research_dir.glob("*.json"))
        if len(sources) < 4:
            issues.append(f"FEW_SOURCES: Only {len(sources)} research artifacts (min 4)")
            score -= 10
    else:
        issues.append("NO_RESEARCH: No research artifacts found")
        score -= 15
    
    score = max(0, score)
    status = "pass" if score >= 70 else "warn" if score >= 50 else "fail"
    
    return {
        "concept_id": concept_id,
        "score": score,
        "status": status,
        "issues": issues,
        "ai_block_chars": len(ai_block),
        "manual_wikilinks": len(manual_wikilinks),
        "ai_wikilinks": len(ai_wikilinks),
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: py eval_concept.py <concept-id> | --all | --area <name>")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        results = []
        for cid in concepts:
            r = eval_concept(cid)
            results.append(r)
        # Summary
        scores = [r["score"] for r in results]
        avg = sum(scores) / len(scores) if scores else 0
        pass_count = sum(1 for r in results if r["status"] == "pass")
        warn_count = sum(1 for r in results if r["status"] == "warn")
        fail_count = sum(1 for r in results if r["status"] == "fail")
        print(f"\n{'='*60}")
        print(f"EVAL SUMMARY: {len(results)} concepts")
        print(f"  Average score: {avg:.1f}/100")
        print(f"  Pass (>=70): {pass_count}")
        print(f"  Warn (50-69): {warn_count}")
        print(f"  Fail (<50): {fail_count}")
        print(f"{'='*60}")
        # Save results
        out_file = workdir / "eval_results.json"
        out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Results saved to: {out_file}")
        
    elif sys.argv[1] == "--area":
        area = sys.argv[2]
        area_concepts = [c for c in concepts.values() if c.area == area]
        results = []
        for c in area_concepts:
            r = eval_concept(c.id)
            results.append(r)
            status_icon = "OK" if r["status"] == "pass" else "WARN" if r["status"] == "warn" else "FAIL"
            print(f"  [{status_icon}] {c.id}: {r['score']}/100 - {len(r['issues'])} issues")
        avg = sum(r["score"] for r in results) / len(results) if results else 0
        print(f"\nArea: {area} | Avg: {avg:.1f}/100 | {len(results)} concepts")
        
    else:
        cid = sys.argv[1]
        result = eval_concept(cid)
        print(f"\nConcept: {result['concept_id']}")
        print(f"Score: {result['score']}/100 ({result['status']})")
        print(f"AI block: {result['ai_block_chars']} chars")
        print(f"Manual wikilinks: {result['manual_wikilinks']}")
        print(f"AI wikilinks: {result['ai_wikilinks']}")
        if result["issues"]:
            print(f"\nIssues ({len(result['issues'])}):")
            for issue in result["issues"]:
                print(f"  - {issue}")
        else:
            print("\nNo issues found.")

if __name__ == "__main__":
    main()
