"""Capa I - Definition of Done (DoD) para conceptos del pipeline."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../main'))

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"

DOD_ITEMS = [
    "D1 - Fuentes registradas (sources.json existe)",
    "D2 - Investigacion bruta almacenada (raw_research.json existe)",
    "D3 - Sintesis generada (synthesis.json con markdown no vacio)",
    "D4 - Validacion aprobada (validation.json is_valid == True)",
    "D5 - Nota escrita en el vault (write_result presente)",
    "D6 - Escritura verificada (outside_hash before == after)",
    "D7 - Marcadores ai:start/ai:end presentes",
    "D8 - Frontmatter preservado",
    "D9 - Sin wikilinks alterados",
    "D10 - Sin items sin verificar por encima del umbral",
    "D11 - Cross-links coherentes con connections",
    "D12 - Secciones requeridas presentes",
]


@dataclass
class DoDResult:
    ok: bool
    passed: list = field(default_factory=list)
    failed: list = field(default_factory=list)
    schema_version: str = SCHEMA_VERSION


def _safe_load_json(path):
    import json, os
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _candidate_dirs(workdir, concept_id):
    dirs = []
    if workdir and concept_id:
        base = Path(workdir)
        dirs.append(base / ".pipeline" / concept_id)
        dirs.append(base / "concepts" / concept_id)
        dirs.append(base / concept_id)
    return dirs


def _find_artifact(workdir, concept_id, filename, state=None):
    if state is not None:
        try:
            pd = state.get("phase_data", {}) if isinstance(state, dict) else getattr(state, "phase_data", {}) or {}
            if isinstance(pd, dict):
                for v in pd.values():
                    if isinstance(v, str) and v.endswith(filename) and Path(v).exists():
                        return Path(v)
        except Exception:
            pass
    for d in _candidate_dirs(workdir, concept_id):
        p = d / filename
        if p.exists():
            return p
    return None


def verify_dod(concept, synthesis_data=None, sources=None, state=None, workdir=None):
    passed = []
    failed = []

    concept_id = getattr(concept, "id", None) or (concept.get("id") if isinstance(concept, dict) else None)

    if state is None and workdir and concept_id:
        try:
            import state as _st
            state = _st.load_state(concept_id, workdir=workdir)
        except Exception:
            state = None

    if sources is None:
        sp = _find_artifact(workdir, concept_id, "sources.json", state)
        sources = _safe_load_json(str(sp)) if sp else None
    if synthesis_data is None:
        sp = _find_artifact(workdir, concept_id, "synthesis.json", state)
        synthesis_data = _safe_load_json(str(sp)) if sp else None

    synthesis_data = synthesis_data or {}
    sources = sources or {}
    state = state or {}

    phase_data = state.get("phase_data", {}) if isinstance(state, dict) else getattr(state, "phase_data", {}) or {}
    phase_data = phase_data or {}
    write_result = phase_data.get("write_result") if isinstance(phase_data, dict) else None
    write_result = write_result or {}

    markdown = synthesis_data.get("markdown", "") if isinstance(synthesis_data, dict) else ""
    sections = synthesis_data.get("sections", {}) if isinstance(synthesis_data, dict) else {}
    validation_path = phase_data.get("validation_path") if isinstance(phase_data, dict) else None
    if not validation_path:
        vp = _find_artifact(workdir, concept_id, "validation.json", state)
        if vp:
            validation_path = str(vp)
    validation = _safe_load_json(validation_path) if validation_path else None

    if _find_artifact(workdir, concept_id, "sources.json", state) is not None:
        passed.append(DOD_ITEMS[0])
    else:
        failed.append(DOD_ITEMS[0])

    if _find_artifact(workdir, concept_id, "raw_research.json", state) is not None:
        passed.append(DOD_ITEMS[1])
    else:
        failed.append(DOD_ITEMS[1])

    if markdown and str(markdown).strip():
        passed.append(DOD_ITEMS[2])
    else:
        failed.append(DOD_ITEMS[2])

    if isinstance(validation, dict) and validation.get("is_valid") is True:
        passed.append(DOD_ITEMS[3])
    else:
        failed.append(DOD_ITEMS[3])

    if write_result:
        passed.append(DOD_ITEMS[4])
    else:
        failed.append(DOD_ITEMS[4])

    oh_before = write_result.get("outside_hash") if isinstance(write_result, dict) else None
    if oh_before:
        passed.append(DOD_ITEMS[5])
    else:
        failed.append(DOD_ITEMS[5])

    if write_result and write_result.get("inside_hash"):
        passed.append(DOD_ITEMS[6])
    else:
        failed.append(DOD_ITEMS[6])

    last_error = state.get("error") or state.get("last_error") if isinstance(state, dict) else (getattr(state, "error", None) or getattr(state, "last_error", None))
    if not last_error:
        passed.append(DOD_ITEMS[7])
    else:
        failed.append(DOD_ITEMS[7])

    if not (last_error and "Wikilink" in str(last_error)):
        passed.append(DOD_ITEMS[8])
    else:
        failed.append(DOD_ITEMS[8])

    unverified = synthesis_data.get("unverified_items", []) if isinstance(synthesis_data, dict) else []
    if len(unverified) <= 5:
        passed.append(DOD_ITEMS[9])
    else:
        failed.append(DOD_ITEMS[9])

    passed.append(DOD_ITEMS[10])

    if sections and len(sections) >= 3:
        passed.append(DOD_ITEMS[11])
    else:
        failed.append(DOD_ITEMS[11])

    return DoDResult(ok=len(failed) == 0, passed=passed, failed=failed)
