"""Tests de Capa 4 (backend) sin red: FakeBackend + integracion de estado.

Corre con pytest (``py -m pytest tests/test_backend.py``) o directo
(``py tests/test_backend.py``), porque ``pytest`` puede no estar
instalado. Los artefactos se escriben en ``tests/.tmp-workdir`` (desechable).
"""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import backend as B
import state
from models import ConceptMeta, ResearchQuestion, Source

WORK = Path(__file__).parent / ".tmp-workdir"

CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("x/Internet.md"),
)

QUESTIONS = [
    ResearchQuestion(qid="a1", group="a", text="Que es Internet y la Web"),
    ResearchQuestion(qid="b1", group="b", text="Estado del arte de Internet y la Web"),
    ResearchQuestion(qid="c1", group="c", text="Relaciones de Internet y la Web"),
]

SOURCES = [
    Source(source_id="https://developer.mozilla.org", url="https://developer.mozilla.org",
           title="MDN", kind="url"),
    Source(source_id="nota-autor", title="Nota del autor", kind="text",
           snippet="resumen manual"),
]

CFG = {"workdir": str(WORK), "backend": {"provider": "fake"}}


def _reset() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)


def _req():
    return {"questions": QUESTIONS, "sources": SOURCES}


# ---------------------------------------------------------------------------
# FakeBackend
# ---------------------------------------------------------------------------


def test_fake_research_determinista() -> None:
    a = asyncio.run(B.FakeBackend().research(CONCEPT, _req()))
    b = asyncio.run(B.FakeBackend().research(CONCEPT, _req()))
    assert a.coverage == 1.0
    assert [s.source_id for s in a.sources] == ["src-1", "src-2"]
    assert len(a.answers) == 3
    assert all(not ans.claims[0].unverified for ans in a.answers)
    assert a.answers[0].answer_md == b.answers[0].answer_md
    assert a.notebook_id is None  # delete_notebook_after=True


def test_fake_request_minimo_desde_concept() -> None:
    fake = B.FakeBackend()
    res = asyncio.run(fake.research(CONCEPT, None))
    assert res.concept_id == CONCEPT.id
    assert res.answers == [] and res.coverage == 1.0
    assert fake.was_called("create_notebook")


def test_fake_fixtures_y_claims_unverified() -> None:
    fixtures = Path(__file__).parent / ".tmp-fixtures"
    fixtures.mkdir(exist_ok=True)
    (fixtures / "frontend-01-internet-web.json").write_text(
        json.dumps({"a1": "respuesta de fixture para a1"}), encoding="utf-8"
    )
    fake = B.FakeBackend(fixtures_dir=fixtures)
    res = asyncio.run(fake.research(CONCEPT, {"questions": QUESTIONS[:1]}))
    assert res.answers[0].answer_md == "respuesta de fixture para a1"
    # sin fuentes => claims unverified
    assert res.answers[0].claims[0].unverified is True
    shutil.rmtree(fixtures)


def test_fake_cleanup_idempotente() -> None:
    fake = B.FakeBackend()
    asyncio.run(fake.research(CONCEPT, {"delete_notebook_after": False}))
    asyncio.run(fake.cleanup())
    pendientes = [nb for nb in fake.notebooks.values() if nb.deleted_at is None]
    assert pendientes == []
    asyncio.run(fake.cleanup())  # idempotente: no falla


def test_fake_latency_y_llamadas() -> None:
    fake = B.FakeBackend(latency_ms=1)
    asyncio.run(fake.research(CONCEPT, _req()))
    metodos = {c["method"] for c in fake.calls}
    assert {"create_notebook", "add_sources", "research", "delete"} <= metodos


# ---------------------------------------------------------------------------
# Persistencia .pipeline
# ---------------------------------------------------------------------------


def test_run_phase_researched_y_artefactos() -> None:
    _reset()
    res = asyncio.run(B.run_research_phase(B.FakeBackend(), CONCEPT, CFG, request=_req()))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.RESEARCHED
    cdir = B.pipeline_dir(CONCEPT.id, WORK)
    sources_path = cdir / "sources.json"
    raw_path = cdir / "raw_research.json"
    assert sources_path.is_file() and raw_path.is_file()
    assert st.phase_data["sources_path"] == str(sources_path)
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    assert raw["concept_id"] == CONCEPT.id
    assert raw["coverage"] == 1.0
    assert raw["backend_provider"] == "fake"
    assert len(raw["answers"]) == 3
    srcs = json.loads(sources_path.read_text(encoding="utf-8"))
    assert srcs["count"] == 2
    assert raw["source_ids"] == ["src-1", "src-2"]
    assert res.duration_ms >= 0


def test_cache_segunda_corrida_no_reejecuta() -> None:
    _reset()
    asyncio.run(B.run_research_phase(B.FakeBackend(), CONCEPT, CFG, request=_req()))
    fake = B.FakeBackend()
    res = asyncio.run(B.run_research_phase(fake, CONCEPT, CFG, request=_req()))
    assert not fake.was_called("research")  # idempotencia: cache
    assert res.answers and res.coverage == 1.0


def test_force_reejecuta_y_backupea() -> None:
    _reset()
    asyncio.run(B.run_research_phase(B.FakeBackend(), CONCEPT, CFG, request=_req()))
    asyncio.run(B.run_research_phase(B.FakeBackend(), CONCEPT, CFG, request=_req(), force=True))
    backups = WORK / "backups" / CONCEPT.id
    assert backups.is_dir() and list(backups.glob("raw_research.json.*.bak"))


# ---------------------------------------------------------------------------
# Errores y transiciones de estado
# ---------------------------------------------------------------------------


def test_fallo_marca_failed_con_razon() -> None:
    _reset()
    class Boom(B.FakeBackend):
        async def research(self, concept, context=None):
            raise B.BackendAuthError("credenciales expiradas")

    try:
        asyncio.run(B.run_research_phase(Boom(), CONCEPT, CFG, request=_req()))
        raise AssertionError("debia lanzar BackendAuthError")
    except B.BackendAuthError:
        pass
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.FAILED
    assert st.phase_data["failed_phase"] == "researching"
    assert st.phase_data["failed_reason"] == "auth"
    assert "credenciales" in (st.error or "")


def test_retry_desde_failed_llega_researched() -> None:
    _reset()

    class Boom(B.FakeBackend):
        async def research(self, concept, context=None):
            raise B.BackendAuthError("credenciales expiradas")

    try:
        asyncio.run(B.run_research_phase(Boom(), CONCEPT, CFG, request=_req()))
    except B.BackendAuthError:
        pass
    res = asyncio.run(B.run_research_phase(B.FakeBackend(), CONCEPT, CFG, request=_req(), force=True))
    st = state.load_state(CONCEPT.id, workdir=WORK)
    assert st.status is state.ConceptStatus.RESEARCHED
    assert res.notebook_id is None


def test_transicion_invalida_desde_validated() -> None:
    st = state.load_state(CONCEPT.id, workdir=WORK)
    st.transition_to(state.ConceptStatus.SYNTHESIZED, checkpoint="researching")
    state.save_state(st, workdir=WORK)
    st.transition_to(state.ConceptStatus.VALIDATED, checkpoint="synthesizing")
    state.save_state(st, workdir=WORK)
    try:
        asyncio.run(B.run_research_phase(B.FakeBackend(), CONCEPT, CFG, request=_req(), force=True))
        raise AssertionError("debia lanzar InvalidTransitionError")
    except state.InvalidTransitionError:
        pass


# ---------------------------------------------------------------------------
# Factory y mapeo de errores
# ---------------------------------------------------------------------------


def test_factory() -> None:
    assert isinstance(B.create_backend(CFG, provider="fake"), B.FakeBackend)
    try:
        B.create_backend(CFG, provider="ollama")
        raise AssertionError("debia lanzar BackendConfigError")
    except B.BackendConfigError:
        pass


def test_map_errores_notebooklm() -> None:
    import notebooklm as nlm

    assert isinstance(
        B._map_library_error(nlm.RateLimitError("429"), "op", "t"),
        B.BackendRateLimitError,
    )
    assert isinstance(
        B._map_library_error(nlm.AuthError("sin cookies"), "op", "t"),
        B.BackendAuthError,
    )
    assert isinstance(
        B._map_library_error(nlm.RPCTimeoutError("t"), "op", "t"),
        B.BackendTimeout,
    )
    assert isinstance(
        B._map_library_error(nlm.NotebookNotFoundError("x"), "op", "t"),
        B.BackendNotFoundError,
    )
    assert isinstance(
        B._map_library_error(nlm.ServerError("5xx"), "op", "t"),
        B.BackendNetworkError,
    )


def test_protocolo_cumplido() -> None:
    assert isinstance(B.create_backend(CFG), B.ResearchBackend)
    # NotebookLMBackend sin pasar por __init__ no satisface (metodos faltan),
    # creamos una instancia mockeando el modulo notebooklm:
    nlm_fake = type("_NLMStub", (), {})()
    stored = B._notebooklm_module()

    def stub_module() -> object:
        return nlm_fake

    B._notebooklm_module = lambda: stored  # noop para restaurar
    backend = B.NotebookLMBackend.__new__(B.NotebookLMBackend)
    backend._nlm = stub_module  # type: ignore[assignment]
    backend._pending = {}
    backend.provider = "notebooklm"
    assert isinstance(backend, B.ResearchBackend)


if __name__ == "__main__":
    _reset()
    fallos = 0
    for name, fn in sorted(
        (n, f) for n, f in sorted(globals().items())
        if n.startswith("test_") and callable(f)
    ):
        try:
            fn()
            print(f"OK   {name}")
        except AssertionError as exc:
            fallos += 1
            print(f"FAIL {name}: {exc}")
    _reset() if not fallos else None
    print("TODOS OK" if fallos == 0 else f"{fallos} fallos")
    raise SystemExit(1 if fallos else 0)
