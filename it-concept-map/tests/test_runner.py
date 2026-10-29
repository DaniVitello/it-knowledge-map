"""Tests de Capa 8 (orquestador) sin red: Runner sobre FakeBackend + mock LLM."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import backend as B
import research as R
import runner as RN
import state
import synthesis as S
import validation as V
import writer
from models import ConceptMeta, Synthesis

WORK = Path(__file__).parent / ".tmp-workdir-runner"
VAULT = Path(__file__).parent / ".tmp-vault-runner"

CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("02 - Frontend/01 - Internet & Web.md"),
    key_ideas=["HTTP", "HTTPS", "URLs"],
    connections=["Cliente-Servidor", "HTTP"],
)

MOCK_MD = """## Objetivo
Para que sirve HTTP en el desarrollo web moderno.

## Esqueleto (el 20% esencial)
1. Request/response.
2. Metodos y status codes.

## Como funciona
El cliente envia un request.

## Detalles
HTTP/1.1, HTTP/2, HTTP/3.

## Ejemplo minimo
GET / HTTP/1.1 con headers basicos.

## Errores comunes
Olvidar headers o status codes.

## Estado actual
HTTP/3 vigente y recomendado.

## Conexiones
HTTP complementa HTTPS en seguridad.

## Ruta de estudio
Antes: redes. Despues: APIs.

## Preguntas de repaso
1. Que es HTTP?
2. Como funciona?
3. Ejemplo?
"""


def _reset():
    if WORK.exists():
        shutil.rmtree(WORK)
    if VAULT.exists():
        shutil.rmtree(VAULT)


def _cfg():
    return {"workdir": str(WORK), "vault_path": str(VAULT), "backend": {"provider": "fake"}}


def _seed_vault():
    """Crea la nota con marcadores ai:start/end."""
    note = VAULT / "02 - Frontend" / "01 - Internet & Web.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\ntitle: \"Internet & Web\"\narea: \"Frontend\"\n---\n"
        "# Internet & Web\n\n## Mis notas\n<!-- ai:start -->\n- \n<!-- ai:end -->\n",
        encoding="utf-8",
    )


def _seed_research():
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "raw_research.json").write_text(json.dumps({
        "concept_id": CONCEPT.id, "coverage": 1.0,
        "answers": [{"qid": "a1", "group": "a", "answer_md": "HTTP es un protocolo", "claims": []}],
        "source_ids": ["src-1"],
    }), encoding="utf-8")
    (cdir / "sources.json").write_text(json.dumps({"count": 1, "sources": []}), encoding="utf-8")
    st = state.ConceptState(concept_id=CONCEPT.id)
    st.status = state.ConceptStatus.RESEARCHED
    state.save_state(st, workdir=WORK)


def _seed_synthesis():
    _seed_research()
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    (cdir / "synthesis.json").write_text(json.dumps({
        "concept_id": CONCEPT.id, "title": CONCEPT.title,
        "markdown": MOCK_MD,
        "sections": {s: ("Contenido suficiente. " * 3) for s in ["Objetivo", "Esqueleto (el 20% esencial)", "Como funciona", "Detalles", "Ejemplo minimo", "Errores comunes", "Estado actual", "Conexiones", "Ruta de estudio"]} | {"Preguntas de repaso": "1. Que es HTTP?\n2. Como funciona?\n3. Ejemplo?"},
    }), encoding="utf-8")
    st = state.load_state(CONCEPT.id, workdir=WORK)
    st.status = state.ConceptStatus.SYNTHESIZED
    state.save_state(st, workdir=WORK)


def _seed_validation():
    _seed_synthesis()
    cdir = Path(WORK) / "concepts" / CONCEPT.id
    (cdir / "validation.json").write_text(json.dumps({
        "concept_id": CONCEPT.id, "is_valid": True, "issues": [], "warnings": [], "score": 1.0,
    }), encoding="utf-8")
    st = state.load_state(CONCEPT.id, workdir=WORK)
    st.status = state.ConceptStatus.VALIDATED
    state.save_state(st, workdir=WORK)


def _mock_llm(prompt):
    return MOCK_MD


# ---------------------------------------------------------------------------


def test_run_concept_completo():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    rep = asyncio.run(runner.run_concept(CONCEPT))
    assert rep.status == "completed"
    assert "research" in rep.phases_completed
    assert "synthesis" in rep.phases_completed
    assert "validation" in rep.phases_completed
    assert "writing" in rep.phases_completed


def test_idempotencia_segunda_corrida():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    asyncio.run(runner.run_concept(CONCEPT))
    rep2 = asyncio.run(runner.run_concept(CONCEPT))
    assert rep2.status == "completed"


def test_fallo_en_research_marca_failed():
    _reset()
    _seed_vault()
    cfg = _cfg()
    orig_create = B.create_backend
    class Boom(B.FakeBackend):
        async def research(self, concept, context=None):
            raise B.BackendAuthError("credenciales expiradas")
    B.create_backend = lambda cfg, provider=None: Boom()
    try:
        runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
        rep = asyncio.run(runner.run_concept(CONCEPT))
        assert rep.status == "failed"
    finally:
        B.create_backend = orig_create


def test_run_concept_desde_researched():
    _reset()
    _seed_vault()
    _seed_research()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    rep = asyncio.run(runner.run_concept(CONCEPT))
    assert rep.status == "completed"
    assert "research" not in rep.phases_completed  # ya estaba researched


def test_run_concept_desde_synthesized():
    _reset()
    _seed_vault()
    _seed_synthesis()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    rep = asyncio.run(runner.run_concept(CONCEPT))
    assert rep.status == "completed"


def test_run_concept_desde_validated():
    _reset()
    _seed_vault()
    _seed_validation()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    rep = asyncio.run(runner.run_concept(CONCEPT))
    assert rep.status == "completed"


def test_run_batch():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    batch = asyncio.run(runner.run_batch([CONCEPT]))
    assert batch.total == 1
    assert batch.completed == 1
    assert len(batch.results) == 1


def test_logging_events():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = RN.Runner(cfg=cfg, llm=_mock_llm, workdir=str(WORK))
    asyncio.run(runner.run_concept(CONCEPT))
    events_path = Path(WORK) / "concepts" / CONCEPT.id / "events.jsonl"
    assert events_path.is_file()
    lines = events_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 3


def test_run_concept_funcion():
    _reset()
    _seed_vault()
    cfg = _cfg()
    rep = asyncio.run(RN.run_concept(CONCEPT, cfg=cfg, llm=_mock_llm, workdir=str(WORK)))
    assert rep.status == "completed"


def test_run_batch_funcion():
    _reset()
    _seed_vault()
    cfg = _cfg()
    batch = asyncio.run(RN.run_batch([CONCEPT], cfg=cfg, llm=_mock_llm, workdir=str(WORK)))
    assert batch.total == 1
    assert batch.completed == 1


def test_protocolo_runner():
    runner = RN.Runner(cfg={"workdir": str(WORK)}, llm=_mock_llm, workdir=str(WORK))
    assert runner is not None
    assert hasattr(runner, "run_concept")
    assert hasattr(runner, "run_batch")


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
