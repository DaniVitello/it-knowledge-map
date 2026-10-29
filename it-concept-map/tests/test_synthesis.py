"""Tests de Capa 6 (sintesis) sin red: SynthesisPhase con mock LLM."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import state
import synthesis as S
from models import ConceptMeta

WORK = Path(__file__).parent / ".tmp-workdir-synth"

CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("x/Internet.md"),
    key_ideas=["HTTP", "HTTPS", "URLs"],
    connections=["Cliente-Servidor", "HTTP"],
)

MOCK_MD = """## Objetivo
Para que sirve HTTP.

## Esqueleto (el 20% esencial)
1. Request/response.
2. Metodos y status codes.

## Como funciona
El cliente envia un request.

## Detalles
HTTP/1.1, HTTP/2, HTTP/3.

## Ejemplo minimo
GET / HTTP/1.1

## Errores comunes
Olvidar headers.

## Estado actual
HTTP/3 vigente.

## Conexiones
[[HTTP]] complementa [[HTTPS]].

## Ruta de estudio
Antes: redes. Despues: APIs.

## Preguntas de repaso
1. Que es HTTP?
"""


def _mock_llm(prompt):
    return MOCK_MD


async def _mock_llm_async(prompt):
    return MOCK_MD


def _reset():
    if WORK.exists():
        shutil.rmtree(WORK)


def _cfg():
    return {"workdir": str(WORK)}


def _seed_research():
    """Crea los artefactos de investigacion para que la sintesis pueda leerlos."""
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "raw_research.json").write_text(json.dumps({
        "concept_id": CONCEPT.id,
        "coverage": 1.0,
        "answers": [{"qid": "a1", "group": "a", "answer_md": "HTTP es un protocolo", "claims": []}],
        "source_ids": ["src-1"],
    }), encoding="utf-8")
    (cdir / "sources.json").write_text(json.dumps({
        "count": 1,
        "sources": [{"source_id": "src-1", "title": "MDN", "url": "https://mdn", "kind": "url"}],
    }), encoding="utf-8")
    # estado researched
    st = state.ConceptState(concept_id=CONCEPT.id)
    st.status = state.ConceptStatus.RESEARCHED
    state.save_state(st, workdir=WORK)


# ---------------------------------------------------------------------------


def test_build_prompt_incluye_concepto_y_reglas():
    raw = {"answers": [{"qid": "a1", "group": "a", "answer_md": "HTTP es un protocolo", "claims": []}]}
    sources = {"sources": [{"source_id": "src-1", "title": "MDN", "url": "https://mdn", "kind": "url"}]}
    p = S.build_prompt(CONCEPT, raw, sources)
    assert "Internet & Web" in p
    assert "Frontend" in p
    assert "HTTP, HTTPS, URLs" in p
    assert "Reglas inegociables" not in p or "REGLAS INNEGOCIABLES" in p
    assert "Objetivo" in p


def test_sintesis_persiste_artefactos():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    res = asyncio.run(phase.run(CONCEPT))
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    assert (cdir / "synthesis.json").is_file()
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.SYNTHESIZED
    assert res.markdown == MOCK_MD
    assert "Objetivo" in res.sections
    assert res.synthesis_path is not None


def test_idempotencia_segunda_corrida():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    asyncio.run(phase.run(CONCEPT))
    # segunda corrida sin force no debe llamar al LLM
    calls = {"n": 0}

    def counting_llm(prompt):
        calls["n"] += 1
        return MOCK_MD

    phase2 = S.SynthesisPhase(llm=counting_llm, cfg=cfg)
    res = asyncio.run(phase2.run(CONCEPT))
    assert calls["n"] == 0
    assert res.markdown == MOCK_MD


def test_force_reejecuta_y_backupea():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    asyncio.run(phase.run(CONCEPT))
    phase2 = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    asyncio.run(phase2.run(CONCEPT, force=True))
    backups = Path(WORK) / "backups" / CONCEPT.id
    assert backups.is_dir() and list(backups.glob("synthesis.json.*.bak"))


def test_fallo_marca_failed():
    _reset()
    _seed_research()
    cfg = _cfg()

    def boom_llm(prompt):
        raise RuntimeError("llm caido")

    phase = S.SynthesisPhase(llm=boom_llm, cfg=cfg)
    try:
        asyncio.run(phase.run(CONCEPT))
        raise AssertionError("debia lanzar")
    except RuntimeError:
        pass
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.FAILED
    assert st.phase_data.get("failed_reason") == "error"


def test_transicion_invalida_desde_pending():
    _reset()
    cfg = _cfg()
    # sin seed_research → estado pending, sintesis requiere researched
    phase = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    try:
        asyncio.run(phase.run(CONCEPT))
        raise AssertionError("debia lanzar")
    except state.InvalidTransitionError:
        pass


def test_async_llm():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=_mock_llm_async, cfg=cfg)
    res = asyncio.run(phase.run(CONCEPT))
    assert res.markdown == MOCK_MD


def test_sin_llm_lanza_error():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=None, cfg=cfg)
    try:
        asyncio.run(phase.run(CONCEPT))
        raise AssertionError("debia lanzar")
    except RuntimeError:
        pass


def test_parseo_secciones():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    res = asyncio.run(phase.run(CONCEPT))
    assert "Objetivo" in res.sections
    assert "Preguntas de repaso" in res.sections
    assert len(res.sections) >= 8


def test_run_synthesis_funcion():
    _reset()
    _seed_research()
    cfg = _cfg()
    res = asyncio.run(S.run_synthesis(CONCEPT, cfg, llm=_mock_llm))
    assert res.markdown == MOCK_MD
    assert res.synthesis_path is not None


def test_protocolo_estados():
    _reset()
    _seed_research()
    cfg = _cfg()
    phase = S.SynthesisPhase(llm=_mock_llm, cfg=cfg)
    asyncio.run(phase.run(CONCEPT))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.SYNTHESIZED
    assert "synthesis_path" in st.phase_data


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
