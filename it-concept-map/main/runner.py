"""Capa 8 - Orquestador del pipeline por concepto.



Orquesta: registry -> research -> synthesis -> validation -> writer, con

logging en events.jsonl, reanudacion desde checkpoint, manejo de errores,

pacing entre conceptos, reporte final.

"""



from __future__ import annotations



import json

import time

import asyncio

from dataclasses import dataclass, field

from pathlib import Path

from typing import Any, Callable, Awaitable



from . import backend

from . import research as R

from . import state

from . import synthesis as S

from . import validation as V

from . import writer

try:
    import dod
except Exception:
    dod = None

try:
    from . import log as _logmod
except Exception:
    _logmod = None

from .models import ConceptMeta, Synthesis



async def execute_phase_with_retry(phase_obj, method_name, *args, max_retries=3, backoff=(2, 4, 8), **kwargs):
    """Capa J: ejecuta un metodo de fase con reintentos y tope."""
    import asyncio as _asyncio
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            meth = getattr(phase_obj, method_name)
            res = meth(*args, **kwargs)
            if hasattr(res, '__await__'):
                res = await res
            return res
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries:
                delay = backoff[min(attempt - 1, len(backoff) - 1)]
                try:
                    await _asyncio.sleep(delay)
                except Exception:
                    pass
    raise last_exc


SCHEMA_VERSION = "1.0.0"



def _mark_failed(st):

    """Transicion segura a FAILED (Capa B4): usa transition_to con fallback."""

    try:

        st.transition_to(state.ConceptStatus.FAILED)

    except Exception:

        st.status = state.ConceptStatus.FAILED





@dataclass

class RunReport:

    concept_id: str

    status: str = "pending"

    phases_completed: list[str] = field(default_factory=list)

    error: str | None = None

    cause: str | None = None

    duration_ms: int = 0



    schema_version: str = SCHEMA_VERSION





@dataclass

class BatchReport:

    total: int = 0

    completed: int = 0

    failed: int = 0

    blocked: int = 0

    skipped: int = 0

    needs_review: int = 0

    results: list[RunReport] = field(default_factory=list)

    duration_ms: int = 0



    schema_version: str = SCHEMA_VERSION





class Runner:

    """Orquesta el pipeline completo por concepto."""



    def __init__(self, cfg: dict | None = None, llm=None, workdir: str | None = None):

        import uuid, datetime

        self.cfg = cfg or {}

        self.workdir = workdir or self.cfg.get("workdir", "workdir")

        self.llm = llm

        self.run_id = "run-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]

        self.max_phase_retries = int(self.cfg.get("max_phase_retries", 3)) if isinstance(self.cfg, dict) else 3

        try:
            from . import log as _log
            self.logger = _log.RunLogger(self.workdir, self.run_id)
        except Exception:
            self.logger = None

        self.pacing_concept = self.cfg.get("pacing", {}).get("between_concepts_s", 0)

        self.pacing_ask = self.cfg.get("pacing", {}).get("pause_between_asks_s", 0)



    def _resume_phase(self, st):
        if st is None:
            return "research"
        status = getattr(st, "status", None)
        cp = getattr(st, "checkpoint", None)
        if status == state.ConceptStatus.COMPLETED:
            return None
        if status == state.ConceptStatus.WRITTEN or cp == "writing":
            return "writing"
        if status == state.ConceptStatus.VALIDATED:
            return "writing"
        if status == state.ConceptStatus.SYNTHESIZED or cp in ("synthesis", "synthesizing"):
            return "validation"
        if status == state.ConceptStatus.RESEARCHED or cp in ("research", "researching"):
            return "synthesis"
        return "research"

    def _log_event(self, concept_id: str, event: str, **kwargs):

        cdir = Path(self.workdir) / "concepts" / concept_id

        cdir.mkdir(parents=True, exist_ok=True)

        entry = {"ts": state.now_iso() if hasattr(state, "now_iso") else None, "run_id": getattr(self, "run_id", None), "concept_id": concept_id, "event": event}

        entry.update(kwargs)

        with open(cdir / "events.jsonl", "a", encoding="utf-8") as f:

            f.write(json.dumps(entry, ensure_ascii=False) + "\n")



    async def run_concept(self, concept: ConceptMeta, force: bool = False, dry_run: bool = False) -> RunReport:

        report = RunReport(concept_id=concept.id)

        t0 = __import__("time").monotonic()

        self._log_event(concept.id, "run_start", force=force, dry_run=dry_run)



        # Cargar estado.

        st = state.load_state(concept.id, workdir=self.workdir)

        if st is None:

            st = state.ConceptState(concept_id=concept.id)

        try:

            state.reconcile_orphan_notebooks(workdir=self.workdir, delete=False)

        except Exception:

            pass



        # Idempotencia: si ya esta completed, saltar (verificando hash del bloque AI).

        if st.status == state.ConceptStatus.COMPLETED and not force and not dry_run:

            # Capa L: verificar hash del bloque AI antes de saltar.
            _skip = True
            try:
                wr = (st.phase_data or {}).get("write_result", {}) if hasattr(st, "phase_data") else {}
                stored_hash = (wr or {}).get("inside_hash")
                if stored_hash and getattr(concept, "note_path", None):
                    from pathlib import Path as _P
                    import hashlib as _hl
                    _note = _P(concept.note_path)
                    if not _note.is_absolute():
                        _vp = self.cfg.get("vault_path") if isinstance(self.cfg, dict) else None
                        if _vp:
                            _note = _P(_vp) / _note
                    if _note.exists():
                        _txt = _note.read_text(encoding="utf-8")
                        # extraer bloque ai:start..ai:end
                        import re as _re
                        _m = _re.search(r"ai:start\](.*?)\[ai:end", _txt, _re.S)
                        _inside = _m.group(1).strip() if _m else ""
                        _h = _hl.sha256(_inside.encode("utf-8")).hexdigest()
                        if _h != stored_hash:
                            _skip = False
                            self._log_event(concept.id, "idempotency_hash_mismatch", stored=stored_hash, actual=_h)
            except Exception:
                _skip = True

            if _skip:
                report.status = "completed"
                report.phases_completed = ["research", "synthesis", "validation", "writing"]
                report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)
                self._log_event(concept.id, "run_skip", reason="already_completed")
                return report



        # Fase 1: Research.

        if st.status in (state.ConceptStatus.PENDING, state.ConceptStatus.FAILED, state.ConceptStatus.RESEARCHING):

            try:

                backend_inst = backend.create_backend(self.cfg)

                research_phase = R.ResearchPhase(backend_inst, {"workdir": self.workdir})

                res = await execute_phase_with_retry(research_phase, "run", concept, force=force, max_retries=self.max_phase_retries)

                st = state.load_state(concept.id, workdir=self.workdir)

                report.phases_completed.append("research")

                self._log_event(concept.id, "phase_done", phase="research")

            except Exception as e:

                st = state.load_state(concept.id, workdir=self.workdir) or st

                _mark_failed(st)

                st.phase_data["failed_phase"] = "researching"

                st.last_error = str(e)

                st.error = str(e)

                state.save_state(st, workdir=self.workdir)

                report.status = "failed"

                report.error = str(e)

                report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

                self._log_event(concept.id, "phase_failed", phase="research", error=str(e))

                return report



        # Fase 2: Synthesis.

        if st.status in (state.ConceptStatus.RESEARCHED, state.ConceptStatus.FAILED, state.ConceptStatus.SYNTHESIZED):

            if st.status == state.ConceptStatus.FAILED and st.phase_data.get("failed_phase") != "synthesizing":

                # Si fallo en research, no intentar synthesis.

                pass

            try:

                # solo si estamos en researched o force

                if st.status in (state.ConceptStatus.RESEARCHED, state.ConceptStatus.FAILED):

                    synth_phase = S.SynthesisPhase(

                        llm=self.llm,

                        cfg={"workdir": self.workdir, "concepts": self.cfg.get("concepts") or {}},

                    )

                    synth_res = await execute_phase_with_retry(synth_phase, "run", concept, force=force, max_retries=self.max_phase_retries)

                    st = state.load_state(concept.id, workdir=self.workdir)

                    report.phases_completed.append("synthesis")

                    self._log_event(concept.id, "phase_done", phase="synthesis")

            except Exception as e:

                st = state.load_state(concept.id, workdir=self.workdir) or st

                _mark_failed(st)

                st.phase_data["failed_phase"] = "synthesizing"

                st.last_error = str(e)

                st.error = str(e)

                state.save_state(st, workdir=self.workdir)

                report.status = "failed"

                report.error = str(e)

                report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

                self._log_event(concept.id, "phase_failed", phase="synthesis", error=str(e))

                return report



        # Fase 3: Validation.

        if st.status in (state.ConceptStatus.SYNTHESIZED, state.ConceptStatus.FAILED, state.ConceptStatus.VALIDATED):

            try:

                if st.status in (state.ConceptStatus.SYNTHESIZED, state.ConceptStatus.FAILED):

                    val_phase = V.ValidationPhase(cfg={"workdir": self.workdir})

                    val_res = await execute_phase_with_retry(val_phase, "run", concept, force=force, max_retries=self.max_phase_retries)

                    st = state.load_state(concept.id, workdir=self.workdir)

                    report.phases_completed.append("validation")

                    self._log_event(concept.id, "phase_done", phase="validation")

                    if not val_res.is_valid:

                        # Capa I: bucle needs_fix -> re-sintetizar una vez.

                        if getattr(val_res, "verdict", "") == "needs_fix":

                            try:

                                from .synthesis import SynthesisPhase

                                synth_phase = SynthesisPhase(llm=self.llm, cfg={"workdir": self.workdir, "concepts": self.cfg.get("concepts") or {}})

                                await execute_phase_with_retry(synth_phase, "run", concept, force=True, max_retries=self.max_phase_retries)

                                st = state.load_state(concept.id, workdir=self.workdir)

                                val_phase = V.ValidationPhase(cfg={"workdir": self.workdir})

                                val_res = await execute_phase_with_retry(val_phase, "run", concept, force=True, max_retries=self.max_phase_retries)

                                st = state.load_state(concept.id, workdir=self.workdir)

                            except Exception:

                                pass

                        if not val_res.is_valid:

                            report.status = "failed"

                            report.error = "validation failed"

                            report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

                            return report

            except Exception as e:

                st = state.load_state(concept.id, workdir=self.workdir) or st

                _mark_failed(st)

                st.phase_data["failed_phase"] = "validating"

                st.last_error = str(e)

                st.error = str(e)

                state.save_state(st, workdir=self.workdir)

                report.status = "failed"

                report.error = str(e)

                report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

                self._log_event(concept.id, "phase_failed", phase="validation", error=str(e))

                return report



        # Fase 4: Writing.

        if st.status in (state.ConceptStatus.VALIDATED, state.ConceptStatus.WRITTEN):

            try:

                if st.status in (state.ConceptStatus.VALIDATED,):

                    # Cargar synthesis para el writer.

                    cdir = Path(self.workdir) / "concepts" / concept.id

                    synth_data = json.loads((cdir / "synthesis.json").read_text(encoding="utf-8"))

                    from .models import Synthesis

                    synth = Synthesis(

                        concept_id=concept.id,

                        title=concept.title,

                        markdown=synth_data.get("markdown", ""),

                        sections=synth_data.get("sections", {}),

                    )

                    # Resolver note_path contra vault_path para que el writer encuentre el archivo.

                    vault_path = Path(self.cfg.get("vault_path", ""))

                    import dataclasses

                    concept_for_write = concept

                    if vault_path and not Path(concept.note_path).is_absolute():

                        concept_for_write = dataclasses.replace(concept, note_path=vault_path / concept.note_path)

                    writer_state = state.load_state(concept.id, workdir=self.workdir)

                    new_state = writer.writing_phase(

                        concept=concept_for_write,

                        synthesis=synth,

                        state=writer_state,

                        config={"vault_path": str(vault_path), "workdir": self.workdir},

                        workdir=self.workdir,

                        dry_run=dry_run,

                        run_id=self.run_id,

                    )

                    st = new_state

                    state.save_state(st, workdir=self.workdir)

                    report.phases_completed.append("writing")

                    self._log_event(concept.id, "phase_done", phase="writing")

                    # Capa I: DoD gate - solo marca completed si el DoD pasa.
                    _dod_ok = True
                    _dod_failed_items = []
                    if dod is not None and not dry_run:
                        try:
                            _dod_res = dod.verify_dod(concept, synth_data, None, st, workdir=self.workdir)
                            _dod_ok = getattr(_dod_res, "ok", True)
                            _dod_failed_items = getattr(_dod_res, "failed", []) or []
                        except Exception as _e:
                            self._log_event(concept.id, "dod_error", error=str(_e))
                            _dod_ok = True
                    if not dry_run:
                        if _dod_ok:
                            try:
                                from . import writer as _w
                                st = _w.mark_completed(st, workdir=self.workdir, config={"vault_path": str(vault_path), "workdir": self.workdir})
                                state.save_state(st, workdir=self.workdir)
                            except Exception as _e:
                                self._log_event(concept.id, "mark_completed_error", error=str(_e))
                        else:
                            try:
                                st.transition_to(state.ConceptStatus.FAILED)
                            except Exception:
                                _mark_failed(st)
                            st.phase_data = st.phase_data or {}
                            st.phase_data["failed_phase"] = "dod"
                            st.phase_data["failed_reason"] = "dod_failed"
                            st.last_error = "DoD failed: " + "; ".join(_dod_failed_items)
                            st.error = st.last_error
                            state.save_state(st, workdir=self.workdir)
                            self._log_event(concept.id, "dod_failed", items=_dod_failed_items)
                            report.status = "failed"
                            report.error = st.last_error
                            report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)
                            return report

                    # Delete notebook after verified write (Capa C).

                    nb_id = st.phase_data.get("notebook_id") if st.phase_data else None

                    if nb_id and not dry_run:

                        try:

                            backend_inst = backend.create_backend(self.cfg)

                            await backend_inst.delete(nb_id)

                            st.phase_data["notebook_id"] = None

                            st.phase_data["notebook_deleted_at"] = state.now_iso() if hasattr(state, "now_iso") else None

                            state.save_state(st, workdir=self.workdir)

                            self._log_event(concept.id, "notebook_deleted", notebook_id=nb_id)

                        except Exception as e:

                            self._log_event(concept.id, "notebook_delete_failed", notebook_id=nb_id, error=str(e))

            except Exception as e:

                st = state.load_state(concept.id, workdir=self.workdir) or st

                try:

                    st.transition_to(state.ConceptStatus.FAILED)

                except Exception:

                    _mark_failed(st)

                st.phase_data["failed_phase"] = "writing"

                st.last_error = str(e)

                st.error = str(e)

                state.save_state(st, workdir=self.workdir)

                report.status = "failed"

                report.error = str(e)

                report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

                self._log_event(concept.id, "phase_failed", phase="writing", error=str(e))

                return report



        # Determinar status final.

        st = state.load_state(concept.id, workdir=self.workdir) or st

        if st.status == state.ConceptStatus.COMPLETED:

            report.status = "completed"

        elif st.status == state.ConceptStatus.FAILED:

            report.status = "failed"

            report.error = st.last_error

            report.cause = st.phase_data.get("failed_reason") if isinstance(st.phase_data, dict) else None

        elif st.status == state.ConceptStatus.NEEDS_REVIEW:

            report.status = "needs_review"

            report.error = st.last_error

            report.cause = "needs_review"

        else:

            report.status = str(st.status.value)



        report.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

        self._log_event(concept.id, "run_end", status=report.status)

        return report



    async def run_batch(self, concepts: list, force: bool = False, dry_run: bool = False) -> BatchReport:

        batch = BatchReport(total=len(concepts))

        try:

            state.reconcile_orphan_notebooks(workdir=self.workdir, delete=False)

        except Exception:

            pass

        try:

            from pathlib import Path

            import json as _j

            Path(self.workdir).mkdir(parents=True, exist_ok=True)

            with open(Path(self.workdir) / "run.jsonl", "a", encoding="utf-8") as _f:

                _f.write(_j.dumps({"ts": state.now_iso() if hasattr(state, "now_iso") else None, "run_id": self.run_id, "event": "run_start", "total": len(concepts)}) + "\n")

        except Exception:

            pass

        t0 = __import__("time").monotonic()

        for i, concept in enumerate(concepts):

            rep = await self.run_concept(concept, force=force, dry_run=dry_run)

            batch.results.append(rep)

            if rep.status == "completed":

                batch.completed += 1

            elif rep.status == "failed":

                batch.failed += 1

            elif rep.status == "needs_review":

                batch.needs_review += 1

            elif rep.status == "blocked":

                batch.blocked += 1

            else:

                batch.skipped += 1

            # Pacing entre conceptos.

            if self.pacing_concept and i < len(concepts) - 1:

                await asyncio.sleep(self.pacing_concept)

        batch.duration_ms = int((__import__("time").monotonic() - t0) * 1000)

        try:

            from pathlib import Path

            import json as _j

            with open(Path(self.workdir) / "run.jsonl", "a", encoding="utf-8") as _f:

                _f.write(_j.dumps({"ts": state.now_iso() if hasattr(state, "now_iso") else None, "run_id": self.run_id, "event": "run_end", "completed": batch.completed, "failed": batch.failed, "duration_ms": batch.duration_ms}) + "\n")

        except Exception:

            pass

        return batch





# ---------------------------------------------------------------------------

# Funciones de conveniencia

# ---------------------------------------------------------------------------





async def run_concept(concept, cfg=None, llm=None, force=False, dry_run=False, workdir=None):

    runner = Runner(cfg=cfg, llm=llm, workdir=workdir)

    return await runner.run_concept(concept, force=force, dry_run=dry_run)





async def run_batch(concepts, cfg=None, llm=None, force=False, dry_run=False, workdir=None):

    runner = Runner(cfg=cfg, llm=llm, workdir=workdir)

    return await runner.run_batch(concepts, force=force, dry_run=dry_run)

