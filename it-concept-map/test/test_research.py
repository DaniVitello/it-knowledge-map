"""Tests de Capa 5 (investigacion) sin red: ResearchPhase sobre FakeBackend."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import backend as B
import research as R
import state
from models import ConceptMeta

WORK = Path(__file__).parent / ".tmp-workdir-research"

CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("x/Internet.md"),
)


def _reset():
    if WORK.exists():
        shutil.rmtree(WORK)


def _cfg():
    return {"workdir": str(WORK), "backend": {"provider": "fake"}}


# ---------------------------------------------------------------------------


def test_research_phase_persiste_artefactos():
    _reset()
    cfg = _cfg()
    phase = R.ResearchPhase(B.FakeBackend(), cfg)
    res = asyncio.run(phase.run(CONCEPT))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.RESEARCHED
    cdir = B.pipeline_dir(CONCEPT.id, WORK)
    assert (cdir / "sources.json").is_file()
    assert (cdir / "raw_research.json").is_file()
    assert res.raw_path is not None and res.sources_path is not None
    assert res.coverage == 1.0


def test_idempotencia_segunda_corrida():
    _reset()
    cfg = _cfg()
    phase = R.ResearchPhase(B.FakeBackend(), cfg)
    asyncio.run(phase.run(CONCEPT))
    fake = B.FakeBackend()
    phase2 = R.ResearchPhase(fake, cfg)
    res = asyncio.run(phase2.run(CONCEPT))
    assert not fake.was_called("research")
    assert res.coverage == 1.0


def test_force_reejecuta_y_backupea():
    _reset()
    cfg = _cfg()
    phase = R.ResearchPhase(B.FakeBackend(), cfg)
    asyncio.run(phase.run(CONCEPT))
    phase2 = R.ResearchPhase(B.FakeBackend(), cfg)
    asyncio.run(phase2.run(CONCEPT, force=True))
    backups = WORK / "backups" / CONCEPT.id
    assert backups.is_dir()


def test_fallo_marca_failed():
    _reset()
    cfg = _cfg()

    class Boom(B.FakeBackend):
        async def research(self, concept, context=None):
            raise B.BackendAuthError("credenciales expiradas")

    phase = R.ResearchPhase(Boom(), cfg)
    try:
        asyncio.run(phase.run(CONCEPT))
        raise AssertionError("debia lanzar")
    except B.BackendAuthError:
        pass
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.FAILED
    assert st.phase_data.get("failed_reason") == "auth"


def test_retry_desde_failed():
    _reset()
    cfg = _cfg()

    class Boom(B.FakeBackend):
        async def research(self, concept, context=None):
            raise B.BackendAuthError("credenciales expiradas")

    phase = R.ResearchPhase(Boom(), cfg)
    try:
        asyncio.run(phase.run(CONCEPT))
    except B.BackendAuthError:
        pass
    phase2 = R.ResearchPhase(B.FakeBackend(), cfg)
    res = asyncio.run(phase2.run(CONCEPT, force=True))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.RESEARCHED
    assert res.notebook_id is not None


def test_transicion_invalida_desde_validated():
    _reset()
    cfg = _cfg()
    phase = R.ResearchPhase(B.FakeBackend(), cfg)
    asyncio.run(phase.run(CONCEPT))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    st.transition_to(state.ConceptStatus.SYNTHESIZED, checkpoint="researching")
    state.save_state(st, workdir=WORK)
    st.transition_to(state.ConceptStatus.VALIDATED, checkpoint="synthesizing")
    state.save_state(st, workdir=WORK)
    phase2 = R.ResearchPhase(B.FakeBackend(), cfg)
    try:
        asyncio.run(phase2.run(CONCEPT, force=True))
        raise AssertionError("debia lanzar InvalidTransitionError")
    except state.InvalidTransitionError:
        pass


def test_request_minimo_desde_concept():
    _reset()
    cfg = _cfg()
    phase = R.ResearchPhase(B.FakeBackend(), cfg)
    res = asyncio.run(phase.run(CONCEPT))
    assert res.concept_id == CONCEPT.id
    assert res.coverage == 1.0


def test_fake_fixtures_y_claims():
    _reset()
    cfg = _cfg()
    fixtures = Path(__file__).parent / ".tmp-fixtures-research"
    fixtures.mkdir(exist_ok=True)
    (fixtures / f"{CONCEPT.id}.json").write_text(
        '{"a1": "respuesta de fixture"}', encoding="utf-8"
    )
    fake = B.FakeBackend(fixtures_dir=fixtures)
    phase = R.ResearchPhase(fake, cfg)
    res = asyncio.run(phase.run(CONCEPT))
    assert any(a.answer_md == "respuesta de fixture" for a in res.answers)
    shutil.rmtree(fixtures)


def test_cleanup_idempotente():
    _reset()
    cfg = _cfg()
    fake = B.FakeBackend()
    phase = R.ResearchPhase(fake, cfg)
    asyncio.run(phase.run(CONCEPT))
    asyncio.run(fake.cleanup())
    asyncio.run(fake.cleanup())
    assert True


def test_latency_y_llamadas():
    _reset()
    cfg = _cfg()
    fake = B.FakeBackend(latency_ms=1)
    phase = R.ResearchPhase(fake, cfg)
    asyncio.run(phase.run(CONCEPT))
    metodos = {c["method"] for c in fake.calls}
    assert {"create_notebook", "add_sources", "research"} <= metodos


def test_factory_backend():
    cfg = _cfg()
    b = B.create_backend(cfg)
    assert isinstance(b, B.FakeBackend)
    try:
        B.create_backend(cfg, provider="ollama")
        raise AssertionError("debia lanzar")
    except B.BackendConfigError:
        pass


def test_protocolo_cumplido():
    cfg = _cfg()
    b = B.create_backend(cfg)
    assert isinstance(b, B.ResearchBackend)


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
