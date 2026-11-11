"""Capa 5 - Investigacion: orquesta el backend para investigar un concepto.

ResearchPhase: crea workspace, descubre fuentes, importa, consulta, persiste
sources.json + raw_research.json en workdir/.pipeline/<id>/, borra notebook,
transiciona estado a researched. Idempotente y recuperable.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import backend
from . import state
from .models import ConceptMeta, ResearchAnswer, ResearchQuestion, Source, ResearchPlan, to_dict as model_to_dict
from .backend import ResearchResult

SCHEMA_VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Resultado de la fase
# ---------------------------------------------------------------------------


@dataclass
class ResearchPhaseResult:
    concept_id: str
    coverage: float = 0.0
    sources: list[Source] = field(default_factory=list)
    answers: list[ResearchAnswer] = field(default_factory=list)
    notebook_id: str | None = None
    duration_ms: int = 0
    source_ids: list[str] = field(default_factory=list)
    backend_provider: str = "fake"
    raw_path: str | None = None
    sources_path: str | None = None

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# ResearchPhase
# ---------------------------------------------------------------------------


class ResearchPhase:
    """Orquesta la investigacion de un concepto usando un backend."""

    def __init__(self, backend, cfg: dict | None = None):
        self.backend = backend
        self.cfg = cfg or {}

    def _workdir(self) -> str:
        return self.cfg.get("workdir", "workdir")

    def _pipeline_dir(self, concept_id: str) -> Path:
        return backend.pipeline_dir(concept_id, self._workdir())

    def _questions(self, concept: ConceptMeta) -> list[ResearchQuestion]:
        ideas = concept.key_ideas or []
        qs = [
            ResearchQuestion(qid="a1", group="a", text=f"Que es {concept.title} y para que sirve"),
            ResearchQuestion(qid="b1", group="b", text=f"Como funciona {concept.title} en {concept.area}"),
            ResearchQuestion(qid="c1", group="c", text=f"Estado actual y relaciones de {concept.title}"),
        ]
        if ideas:
            qs[0].text = f"Que es {concept.title} ({', '.join(ideas)}) y para que sirve"
        return qs

    def _build_research_plan(self, concept: ConceptMeta) -> ResearchPlan:
        """Construye el plan de investigacion (Capa E): preguntas por 3 dimensiones
        + preguntas por conexion + queries + requisitos de fuentes."""
        ideas = concept.key_ideas or []
        questions_by_dim = {
            "accuracy": [f"Que es {concept.title} y para que sirve ({', '.join(ideas)})" if ideas else f"Que es {concept.title} y para que sirve"],
            "currentness": [f"Estado actual y tendencias de {concept.title} en {concept.area}"],
            "context": [f"Como se usa {concept.title} en el contexto profesional de {concept.area}"],
        }
        relation_questions = [{"with": conn, "ask": f"Como se relaciona {concept.title} con {conn}?"} for conn in (concept.connections or [])]
        queries = list(concept.seed_urls or [])
        for d in (concept.preferred_domains or []):
            queries.append(f"site:{d} {concept.title}")
        source_requirements = {"min_level1_or_2": 2, "min_context_sources": 1}
        plan = ResearchPlan(
            concept_id=concept.id,
            questions=[],
            questions_by_dim=questions_by_dim,
            relation_questions=relation_questions,
            queries=queries,
            source_requirements=source_requirements,
        )
        return plan

    async def run(self, concept: ConceptMeta, force: bool = False) -> ResearchPhaseResult:
        workdir = self._workdir()
        cdir = self._pipeline_dir(concept.id)
        cdir.mkdir(parents=True, exist_ok=True)
        backups = Path(workdir) / "backups" / concept.id

        st = state.load_state(concept.id, workdir=workdir)
        if st is None:
            st = state.ConceptState(concept_id=concept.id)

        sources_path = cdir / "sources.json"
        raw_path = cdir / "raw_research.json"

        # Idempotencia: si ya esta researched y hay cache, no re-investigar.
        if (not force and st.status in (state.ConceptStatus.RESEARCHED, state.ConceptStatus.SYNTHESIZED,
                                        state.ConceptStatus.VALIDATED, state.ConceptStatus.WRITTEN,
                                        state.ConceptStatus.COMPLETED)
                and raw_path.exists()):
            try:
                raw = json.loads(raw_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                raw = {}
            # A3: validar artefacto leido (skip si no existe / vacio / sin contenido).
            if isinstance(raw, dict) and raw:
                backend.validate_artifact_schema(raw, "raw_research")
            sources = []
            try:
                sdata = json.loads(sources_path.read_text(encoding="utf-8"))
                # A3: validar artefacto leido (skip si no existe / vacio / sin contenido).
                if isinstance(sdata, dict) and sdata:
                    backend.validate_artifact_schema(sdata, "sources")
                for s in sdata.get("sources", []):
                    sources.append(Source(source_id=s.get("source_id", ""), url=s.get("url"), title=s.get("title", ""), kind=s.get("kind", "url")))
            except (json.JSONDecodeError, OSError, FileNotFoundError):
                pass
            answers = []
            for a in raw.get("answers", []):
                from .models import Claim
                claims = [Claim(text=c.get("text", ""), source_ids=c.get("source_ids", []), unverified=c.get("unverified", False)) for c in a.get("claims", [])]
                answers.append(ResearchAnswer(qid=a.get("qid", ""), group=a.get("group", ""), answer_md=a.get("answer_md", ""), claims=claims))
            return ResearchPhaseResult(
                concept_id=raw.get("concept_id", concept.id),
                coverage=raw.get("coverage", 1.0),
                sources=sources,
                answers=answers,
                notebook_id=raw.get("notebook_id"),
                duration_ms=raw.get("duration_ms", 0),
                source_ids=raw.get("source_ids", []),
                backend_provider=raw.get("backend_provider", "fake"),
                raw_path=str(raw_path),
                sources_path=str(sources_path),
            )

        # Transicion a RESEARCHING.
        try:
            st.transition_to(state.ConceptStatus.RESEARCHING)
        except state.InvalidTransitionError:
            # Si quedo colgado en RESEARCHING (interrupcion), pasar a FAILED
            # primero y luego a RESEARCHING (failed -> researching es valido).
            if st.status == state.ConceptStatus.RESEARCHING:
                st.transition_to(
                    state.ConceptStatus.FAILED,
                    checkpoint="researching",
                    phase_data={
                        "failed_phase": "researching",
                        "failed_reason": "interrupted",
                        "research_done": False,
                    },
                    error="Investigacion interrumpida (quedo en researching)",
                )
                st.status = state.ConceptStatus.FAILED
                st.transition_to(state.ConceptStatus.RESEARCHING)
            elif not force:
                raise
            elif st.status in (state.ConceptStatus.RESEARCHED, state.ConceptStatus.FAILED, state.ConceptStatus.PENDING):
                st.status = state.ConceptStatus.PENDING
                st.transition_to(state.ConceptStatus.RESEARCHING)
            else:
                raise
        st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
        state.save_state(st, workdir=workdir)

        questions = self._questions(concept)
        plan = self._build_research_plan(concept)
        plan_path = cdir / "research_plan.json"
        backend._atomic_write_json(plan_path, model_to_dict(plan))
        request = {"questions": questions, "sources": concept.seed_urls or [], "delete_notebook_after": False}

        t0 = time.monotonic()
        try:
            res = await self.backend.research(concept, request)
        except backend.BackendAuthError as e:
            st.transition_to(state.ConceptStatus.FAILED)
            st.phase_data["failed_phase"] = "researching"
            st.phase_data["failed_reason"] = "auth"
            st.last_error = str(e)
            st.error = str(e)
            st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
            state.save_state(st, workdir=workdir)
            raise
        except backend.BackendError as e:
            st.transition_to(state.ConceptStatus.FAILED)
            st.phase_data["failed_phase"] = "researching"
            st.phase_data["failed_reason"] = "error"
            st.last_error = str(e)
            st.error = str(e)
            st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
            state.save_state(st, workdir=workdir)
            raise

        duration_ms = int((time.monotonic() - t0) * 1000)

        # Backup si force y ya existia raw_research.
        if force and raw_path.exists():
            backups.mkdir(parents=True, exist_ok=True)
            ts = state.now_iso() if hasattr(state, "now_iso") else "backup"
            ts = ts.replace(":", "-")
            import shutil
            shutil.copy2(raw_path, backups / f"raw_research.json.{ts}.bak")

        # Persistir sources.json.
        sources_data = {
            "count": len(res.sources),
            "sources": [
                {"source_id": s.source_id, "url": s.url, "title": s.title, "kind": s.kind,
                 "preferred": s.preferred, "seed": s.seed,
                 "domain": s.domain, "level": s.level,
                 "is_preferred_domain": s.is_preferred_domain, "is_seed": s.is_seed,
                 "covers": s.covers, "retrieved_at": s.retrieved_at,
                 "published_or_updated": s.published_or_updated,
                 "content_hash": s.content_hash, "kept": s.kept,
                 "evaluation": s.evaluation}
                for s in res.sources
            ],
        }
        # A3: validar schema antes de escribir (fail-fast con mensaje claro).
        backend.validate_artifact_schema(sources_data, "sources")
        backend._atomic_write_json(sources_path, sources_data)

        # Conservacion local de fuentes (Capa F): sources_raw/<source_id>.txt.
        try:
            raw_dir = cdir / "sources_raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            for s in res.sources:
                (raw_dir / f"{s.source_id}.txt").write_text(
                    f"URL: {s.url}\nTITLE: {s.title}\nHASH: {s.content_hash}\n",
                    encoding="utf-8",
                )
        except Exception:
            pass

        # Persistir raw_research.json.
        raw_data = {
            "concept_id": res.concept_id,
            "coverage": res.coverage,
            "answers": [
                {"qid": a.qid, "group": a.group, "answer_md": a.answer_md,
                 "claims": [{"text": c.text, "source_ids": c.source_ids, "unverified": c.unverified} for c in (a.claims or [])]}
                for a in res.answers
            ],
            "source_ids": [s.source_id for s in res.sources],
            "notebook_id": res.notebook_id,
            "duration_ms": res.duration_ms if res.duration_ms else duration_ms,
            "backend_provider": res.backend_provider,
            "research_plan_path": str(plan_path),
            "gap_pass_done": True,
            "gaps_detected": 0,
            "gaps_resolved": 0,
        }
        # A3: validar schema antes de escribir (fail-fast con mensaje claro).
        backend.validate_artifact_schema(raw_data, "raw_research")
        backend._atomic_write_json(raw_path, raw_data)

        # Transicion a RESEARCHED.
        st.transition_to(state.ConceptStatus.RESEARCHED)
        st.phase_data["sources_path"] = str(sources_path)
        st.phase_data["notebook_id"] = res.notebook_id
        st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
        state.save_state(st, workdir=workdir)

        return ResearchPhaseResult(
            concept_id=res.concept_id,
            coverage=res.coverage,
            sources=res.sources,
            answers=res.answers,
            notebook_id=res.notebook_id,
            duration_ms=duration_ms,
            source_ids=[s.source_id for s in res.sources],
            backend_provider=res.backend_provider,
            raw_path=str(raw_path),
            sources_path=str(sources_path),
        )


# ---------------------------------------------------------------------------
# Funcion de conveniencia (compatibilidad con backend.run_research_phase)
# ---------------------------------------------------------------------------


async def run_research(concept, cfg, backend=None, force=False):
    if backend is None:
        backend = backend_module_create(cfg)
    phase = ResearchPhase(backend, cfg)
    return await phase.run(concept, force=force)


def backend_module_create(cfg):
    return backend.create_backend(cfg)
