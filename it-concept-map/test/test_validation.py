"""Tests de Capa 7 (validacion) sin red."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import state
import validation as V
from models import ConceptMeta

WORK = Path(__file__).parent / ".tmp-workdir-val"

CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("x/Internet.md"),
    key_ideas=["HTTP", "HTTPS", "URLs"],
    connections=["Cliente-Servidor", "HTTP"],
)

GOOD_MD = "\n".join(f"## {s}\n" + ("Contenido suficiente para la seccion. " * 3) for s in V.REQUIRED_SECTIONS) + "\n## Preguntas de repaso\n1. Que es HTTP?\n2. Como funciona?\n3. Ejemplo?\n"


def _reset():
    if WORK.exists():
        shutil.rmtree(WORK)


def _cfg():
    return {"workdir": str(WORK)}


def _seed_synthesis():
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "synthesis.json").write_text(json.dumps({
        "concept_id": CONCEPT.id,
        "markdown": GOOD_MD,
        "sections": {**{s: "Contenido suficiente para la seccion. " * 3 for s in V.REQUIRED_SECTIONS if s != "Preguntas de repaso"}, "Preguntas de repaso": "1. Que es HTTP?\n2. Como funciona?\n3. Ejemplo?"},
    }), encoding="utf-8")
    (cdir / "sources.json").write_text(json.dumps({"count": 1, "sources": []}), encoding="utf-8")
    st = state.ConceptState(concept_id=CONCEPT.id)
    st.status = state.ConceptStatus.SYNTHESIZED
    state.save_state(st, workdir=WORK)


# ---------------------------------------------------------------------------


def test_validate_pass_con_contenido_completo():
    synth = {"markdown": GOOD_MD, "sections": {s: ("Contenido suficiente para la seccion. " * 3) for s in V.REQUIRED_SECTIONS}}
    # asegurar 3 preguntas de repaso
    synth["sections"]["Preguntas de repaso"] = "1. Que es HTTP?\n2. Como funciona?\n3. Ejemplo?"
    is_valid, issues, warnings = V.validate(CONCEPT, synth, {})
    assert is_valid is True
    assert issues == []


def test_validate_fail_seccion_faltante():
    sections = {s: "Contenido suficiente. " * 3 for s in V.REQUIRED_SECTIONS if s != "Objetivo"}
    synth = {"markdown": GOOD_MD, "sections": sections}
    is_valid, issues, warnings = V.validate(CONCEPT, synth, {})
    assert is_valid is False
    assert any("Objetivo" in i for i in issues)


def test_validate_fail_seccion_corta():
    sections = {s: ("Contenido suficiente. " * 3) for s in V.REQUIRED_SECTIONS}
    sections["Detalles"] = "x"
    synth = {"markdown": GOOD_MD, "sections": sections}
    is_valid, issues, warnings = V.validate(CONCEPT, synth, {})
    assert is_valid is False
    assert any("Detalles" in i for i in issues)


def test_validate_fail_muy_corto():
    synth = {"markdown": "## Objetivo\nx", "sections": {"Objetivo": "x"}}
    is_valid, issues, warnings = V.validate(CONCEPT, synth, {})
    assert is_valid is False


def test_validate_fail_pocas_preguntas():
    sections = {s: "Contenido suficiente. " * 3 for s in V.REQUIRED_SECTIONS}
    sections["Preguntas de repaso"] = "1. Que es HTTP?"
    synth = {"markdown": GOOD_MD, "sections": sections}
    is_valid, issues, warnings = V.validate(CONCEPT, synth, {})
    assert is_valid is False
    assert any("Preguntas de repaso" in i for i in issues)


def test_validation_phase_persiste_artefactos():
    _reset()
    _seed_synthesis()
    cfg = _cfg()
    phase = V.ValidationPhase(cfg=cfg)
    res = asyncio.run(phase.run(CONCEPT))
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    assert (cdir / "validation.json").is_file()
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.VALIDATED
    assert res.is_valid is True
    assert res.report_path is not None


def test_idempotencia_segunda_corrida():
    _reset()
    _seed_synthesis()
    cfg = _cfg()
    phase = V.ValidationPhase(cfg=cfg)
    asyncio.run(phase.run(CONCEPT))
    phase2 = V.ValidationPhase(cfg=cfg)
    res = asyncio.run(phase2.run(CONCEPT))
    assert res.is_valid is True
    assert res.report_path is not None


def test_force_reejecuta():
    _reset()
    _seed_synthesis()
    cfg = _cfg()
    phase = V.ValidationPhase(cfg=cfg)
    asyncio.run(phase.run(CONCEPT))
    phase2 = V.ValidationPhase(cfg=cfg)
    res = asyncio.run(phase2.run(CONCEPT, force=True))
    assert res.is_valid is True


def test_fallo_marca_failed():
    _reset()
    _seed_synthesis()
    # Corromper la sintesis para que falle validacion
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    (cdir / "synthesis.json").write_text(json.dumps({
        "concept_id": CONCEPT.id,
        "markdown": "## Objetivo\nx",
        "sections": {"Objetivo": "x"},
    }), encoding="utf-8")
    cfg = _cfg()
    phase = V.ValidationPhase(cfg=cfg)
    res = asyncio.run(phase.run(CONCEPT))
    assert res.is_valid is False
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.FAILED


def test_transicion_invalida_desde_pending():
    _reset()
    cfg = _cfg()
    phase = V.ValidationPhase(cfg=cfg)
    try:
        asyncio.run(phase.run(CONCEPT))
        raise AssertionError("debia lanzar")
    except state.InvalidTransitionError:
        pass


def test_run_validation_funcion():
    _reset()
    _seed_synthesis()
    cfg = _cfg()
    res = asyncio.run(V.run_validation(CONCEPT, cfg))
    assert res.is_valid is True
    assert res.report_path is not None


def test_protocolo_estados():
    _reset()
    _seed_synthesis()
    cfg = _cfg()
    phase = V.ValidationPhase(cfg=cfg)
    asyncio.run(phase.run(CONCEPT))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.VALIDATED
    assert "validation_path" in st.phase_data


if __name__ == "__main__":
    _reset()
    fallos = 0
    for name, fn in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        try:
            fn()
            print(f"OK   {name}")
        except AssertionError as exc:
            fallos += 1
            print(f"FAIL {name}: {exc}")
        except Exception as exc:
            fallos += 1
            print(f"ERR  {name}: {type(exc).__name__}: {exc}")
    _reset()
    print("TODOS OK" if fallos == 0 else f"{fallos} fallos")
    raise SystemExit(1 if fallos else 0)
