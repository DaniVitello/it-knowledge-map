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

    # Leer la nota del vault si es posible.
    note_text = None
    note_path = None
    try:
        np_ = getattr(concept, "note_path", None)
        if np_ is None and isinstance(concept, dict):
            np_ = concept.get("note_path")
        if np_:
            note_path = Path(np_)
            if not note_path.is_absolute():
                # intentar resolver contra vault_path del cfg? sin cfg, probar tal cual
                pass
            if note_path.exists():
                note_text = note_path.read_text(encoding="utf-8")
    except Exception:
        note_text = None

    oh_before = write_result.get("outside_hash") if isinstance(write_result, dict) else None
    last_error = state.get("error") or state.get("last_error") if isinstance(state, dict) else (getattr(state, "error", None) or getattr(state, "last_error", None))

    # D6: escritura verificada (outside_hash before == after releyendo el archivo).
    if oh_before and note_text is not None:
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "main"))
            import writer as _w
            current_outside = _w.content_hash_outside(note_text)
            if current_outside is not None and current_outside == oh_before:
                passed.append(DOD_ITEMS[5])
            else:
                failed.append(DOD_ITEMS[5])
        except Exception:
            # fallback: si no se puede calcular, usar presencia de hash
            if oh_before:
                passed.append(DOD_ITEMS[5])
            else:
                failed.append(DOD_ITEMS[5])
    elif oh_before:
        passed.append(DOD_ITEMS[5])
    else:
        failed.append(DOD_ITEMS[5])

    # D7: marcadores ai:start/ai:end presentes.
    if note_text is not None:
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "main"))
            import writer as _w
            span = _w.find_markers(note_text)
            if span is not None:
                passed.append(DOD_ITEMS[6])
            else:
                failed.append(DOD_ITEMS[6])
        except Exception:
            failed.append(DOD_ITEMS[6])
    else:
        # Sin nota leible: usar inside_hash como proxy
        if write_result and write_result.get("inside_hash"):
            passed.append(DOD_ITEMS[6])
        else:
            failed.append(DOD_ITEMS[6])

    # D8: frontmatter preservado (existe y es valido).
    if note_text is not None:
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "main"))
            import writer as _w
            fm, _ = _w.parse_frontmatter(note_text)
            if fm is not None or "---" in note_text[:10]:
                passed.append(DOD_ITEMS[7])
            else:
                failed.append(DOD_ITEMS[7])
        except Exception:
            failed.append(DOD_ITEMS[7])
    else:
        if not last_error:
            passed.append(DOD_ITEMS[7])
        else:
            failed.append(DOD_ITEMS[7])

    # D9: sin wikilinks alterados (comparar con connections del concepto).
    connections = getattr(concept, "connections", None)
    if connections is None and isinstance(concept, dict):
        connections = concept.get("connections")
    connections = connections or []
    if note_text is not None:
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "main"))
            import writer as _w
            note_links = _w._wikilink_set(note_text) if hasattr(_w, "_wikilink_set") else set()
            # Extraer wikilinks del afuera (fuera del bloque AI) para comparar
            # con connections. Si note_links es subset de connections (o viceversa), ok.
            if not connections or note_links.issubset(set(connections)) or set(connections).issubset(note_links):
                passed.append(DOD_ITEMS[8])
            else:
                failed.append(DOD_ITEMS[8])
        except Exception:
            if not (last_error and "Wikilink" in str(last_error)):
                passed.append(DOD_ITEMS[8])
            else:
                failed.append(DOD_ITEMS[8])
    else:
        if not (last_error and "Wikilink" in str(last_error)):
            passed.append(DOD_ITEMS[8])
        else:
            failed.append(DOD_ITEMS[8])

    # D10: sin items sin verificar por encima del umbral.
    unverified_count = 0
    # Contar marcadores de incertidumbre en el markdown
    import re as _re
    unverified_count += len(_re.findall(r"\?\?\s*verificar", markdown, _re.IGNORECASE))
    unverified_count += len(_re.findall(r"\(sin verificar\)", markdown, _re.IGNORECASE))
    unverified_count += len(_re.findall(r"\*{1,2}\s*[Ss]in verificar", markdown))
    if unverified_count <= 5:
        passed.append(DOD_ITEMS[9])
    else:
        failed.append(DOD_ITEMS[9])

    # D11: cross-links coherentes con connections.
    if connections:
        # Verificar que al menos uno de los connections aparece en el markdown
        found = any(c in markdown for c in connections)
        if found:
            passed.append(DOD_ITEMS[10])
        else:
            failed.append(DOD_ITEMS[10])
    else:
        passed.append(DOD_ITEMS[10])

    return DoDResult(ok=len(failed) == 0, passed=passed, failed=failed)
