"""Backend de investigacion — Capa 4 de implementacion.

Interfaz + fake + notebooklm. Abstrae el acceso a NotebookLM detras de un
contrato unico (`ResearchBackend`) para que investigacion (Capa 5), sintesis
(Capa 7) y validacion (Capa 8) no dependan de un proveedor concreto.

Componentes:
- ``ResearchBackend``: Protocol con ``research(concept, context)`` y
  ``cleanup()``. El pipeline solo habla con esta interfaz.
- ``ResearchRequest`` / ``ResearchResult`` (+ ``Source`` re-exportada de
  models.py): dataclasses del contrato.
- ``FakeBackend``: implementacion en memoria, determinista, sin red
  (tests, dry-run, CI).
- ``NotebookLMBackend``: adaptador async de ``notebooklm-py`` v0.8.4
  (API directa, sin subprocess: evita el bug de encoding del CLI en
  Windows; ver DOCS/learnings.md).
- ``run_research_phase``: integracion con state.py (transiciones
  researching -> researched / failed) y persistencia de fuentes y
  respuestas en ``workdir/.pipeline/<concept_id>/`` (sources.json,
  raw_research.json).
- ``create_backend``: factory con precedencia parametro > env (BACKEND_PROVIDER)
  > config.yaml.

Segun "explicacion del proyecto por capas v1.md" (Capa 4) y su pseudo-codigo:
- El pipeline nunca importa notebooklm-py directamente; solo la interfaz.
- Timeouts obligatorios en toda llamada de red (sin timeout = bug), con
  ``asyncio.wait_for``.
- ``delete`` idempotente: no falla si el notebook ya no existe.
- Reintentos con backoff exponencial solo para errores transitorios
  (timeout / red / rate limit). Errores de auth/config no se reinician.
- Trazabilidad: cada respuesta mapea afirmaciones (claims) a source_id;
  claim sin fuente se marca ``unverified`` (la validacion lo penaliza).
- Limpieza best-effort de notebooks huerfanos: ante fallo post-create se
  intenta borrar el notebook, y ``cleanup()`` retoma los pendientes.
- Circuit breaker simple: N fallos de red consecutivos abortan rapido.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence, runtime_checkable

import state
from models import (
    SCHEMA_VERSION,
    Claim,
    ConceptMeta,
    RawResearch,
    ResearchAnswer,
    ResearchPlan,
    ResearchQuestion,
    Source,
    Volatility,
    now_iso,
    to_dict,
)

__all__ = [
    # Contrato
    "ResearchBackend",
    "ResearchRequest",
    "ResearchResult",
    "Source",
    # Implementaciones
    "FakeBackend",
    "NotebookLMBackend",
    # Factory
    "create_backend",
    # Persistencia (.pipeline)
    "pipeline_dir",
    "persist_research",
    "load_cached_research",
    "load_cached_sources",
    "research_result_from_dict",
    # Integracion con state.py
    "run_research_phase",
    # Excepciones
    "BackendError",
    "BackendTimeout",
    "BackendAuthError",
    "BackendNetworkError",
    "BackendRateLimitError",
    "BackendNotFoundError",
    "BackendConfigError",
    "BackendCircuitOpenError",
    "ResearchPersistError",
    # Helpers
    "estimate_coverage",
]


# ---------------------------------------------------------------------------
# Dataclasses del contrato
# ---------------------------------------------------------------------------


@dataclass
class ResearchRequest:
    """Contexto (y entradas) de la investigacion de un concepto.

    Lo arma la fase de investigacion (Capa 5): fuentes preseleccionadas,
    plan de preguntas (grupos a/b/c) y parametros de estrategia.
    ``ResearchBackend.research(concept)`` sin request infiere uno minimo
    desde el ``ConceptMeta``.
    """

    concept_id: str
    title: str
    area: str = ""
    volatility: Volatility = Volatility.SEMI_STABLE
    # Plan de preguntas: a = fundamento estable, b = practica moderna,
    # c = relaciones / casos de uso.
    questions: list[ResearchQuestion] = field(default_factory=list)
    # Fuentes a subir al notebook (url / text / file).
    sources: list[Source] = field(default_factory=list)
    # Contexto adicional del autor (manual_notes / hints), se anexa a cada
    # pregunta como orientacion. Nunca reemplaza fuentes.
    manual_notes: str = ""
    # Parametros de estrategia (defaults de la spec; config los ajusta).
    freshness_window_days: int = 30
    min_sources: int = 4
    coverage_threshold: float = 0.7
    # Titulo custom del notebook y limpieza post-research.
    notebook_title: str | None = None
    delete_notebook_after: bool = True

    schema_version: str = SCHEMA_VERSION

    @classmethod
    def from_concept(cls, concept: ConceptMeta) -> "ResearchRequest":
        """Request minimo derivado del ConceptMeta (sin plan ni fuentes)."""
        manual = "\n".join(concept.key_ideas)
        if concept.connections:
            manual += "\nRelacionados: " + ", ".join(concept.connections)
        return cls(
            concept_id=concept.id,
            title=concept.title,
            area=concept.area,
            volatility=concept.volatility,
            manual_notes=manual,
        )


@dataclass
class ResearchResult:
    """Resultado bruto de una investigacion ejecutada por un backend.

    ``notebook_id`` queda en ``None`` si el notebook ya fue eliminado
    (delete_notebook_after=True), para no dejar referencias a recursos
    que ya no existen.
    """

    concept_id: str
    notebook_id: str | None
    answers: list[ResearchAnswer] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    # Fuentes del request que no pudieron subirse (best-effort, no bloquean).
    failed_sources: list[dict[str, Any]] = field(default_factory=list)
    coverage: float = 0.0
    low_coverage: bool = False
    low_sources: bool = False
    duration_ms: int = 0
    backend_provider: str = "fake"
    researched_at: str = field(default_factory=now_iso)

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Excepciones (jerarquia de la spec)
# ---------------------------------------------------------------------------


class BackendError(Exception):
    """Error base de la capa backend."""


class BackendTimeout(BackendError):
    """Una operacion excedio su timeout."""

    def __init__(self, op: str, target: str, detail: str = "") -> None:
        msg = f"timeout en '{op}' (target={target})"
        if detail:
            msg += f": {detail}"
        super().__init__(msg)
        self.op = op
        self.target = target


class BackendAuthError(BackendError):
    """Credenciales invalidas o ausentes (requiere accion humana)."""


class BackendNetworkError(BackendError):
    """Red caida, 5xx u otro error transitorio de transporte."""


class BackendRateLimitError(BackendNetworkError):
    """Cuota / 429: rate limit del servicio."""


class BackendNotFoundError(BackendError):
    """El notebook o fuente pedida no existe (inconsistencia de estado)."""


class BackendConfigError(BackendError):
    """Configuracion invalida o proveedor desconocido."""


class BackendCircuitOpenError(BackendNetworkError):
    """Circuit breaker abierto: N errores de red transitorios consecutivos."""

    def __init__(self, failures: int, threshold: int) -> None:
        super().__init__(
            f"circuit breaker abierto tras {failures} fallos de red consecutivos "
            f"(umbral={threshold}); pausar el lote antes de reintentar"
        )
        self.failures = failures
        self.threshold = threshold


class ResearchPersistError(BackendError):
    """Fallo de IO persistiendo sources.json / raw_research.json."""


# Errores transitorios: se reintentan con backoff (operaciones idempotentes
# o sin side effects; un notebook creado se puede limpiar como best effort).
_TRANSIENT: tuple[type[BaseException], ...] = (
    BackendTimeout,
    BackendNetworkError,
    BackendRateLimitError,
    BackendCircuitOpenError,
)


# ---------------------------------------------------------------------------
# Helpers generales
# ---------------------------------------------------------------------------


def _cfg(config: Any, *keys: str, default: Any = None) -> Any:
    """Lee config.yaml anidado con fallbacks (mismo criterio que state.py)."""
    cur = config
    if cur is None:
        return default
    for key in keys:
        if isinstance(cur, Mapping):
            if key in cur:
                cur = cur[key]
            else:
                return default
        elif hasattr(cur, key):
            cur = getattr(cur, key)
        else:
            return default
    return cur if cur is not None else default


def _to_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "si", "yes", "y")


def _coerce_request(
    concept: ConceptMeta, context: Mapping[str, Any] | ResearchRequest | None
) -> ResearchRequest:
    """Normaliza ``context`` a ResearchRequest (acepta un Mapping crudo)."""
    if isinstance(context, ResearchRequest):
        if not context.title:
            return replace(context, title=concept.title)
        if not context.concept_id:
            return replace(context, concept_id=concept.id)
        return context

    req = ResearchRequest.from_concept(concept)
    if isinstance(context, Mapping):
        req.concept_id = str(context.get("concept_id") or req.concept_id)
        req.title = str(context.get("title") or req.title)
        req.area = str(context.get("area") or req.area)
        vol = context.get("volatility")
        if isinstance(vol, Volatility):
            req.volatility = vol
        elif isinstance(vol, str):
            try:
                req.volatility = Volatility(vol.strip().lower())
            except ValueError:
                pass  # volatilidad desconocida: queda el default del concepto
        questions = context.get("questions")
        if questions:
            normalized: list[ResearchQuestion] = []
            for i, q in enumerate(questions):
                if isinstance(q, ResearchQuestion):
                    normalized.append(q)
                elif isinstance(q, Mapping) and str(q.get("text") or "").strip():
                    normalized.append(
                        ResearchQuestion(
                            qid=str(q.get("qid", f"q{i + 1}")),
                            group=str(q.get("group", "a"))[:1] or "a",
                            text=str(q.get("text", "")),
                        )
                    )
            req.questions = normalized
        sources = context.get("sources")
        if sources:
            req.sources = [
                s for s in (
                    src if isinstance(src, Source) else _source_from_dict(src)
                    for src in sources
                ) if s is not None
            ]
        req.manual_notes = str(context.get("manual_notes") or req.manual_notes)
        req.freshness_window_days = int(
            context.get("freshness_window_days", req.freshness_window_days) or 30
        )
        req.min_sources = int(context.get("min_sources", req.min_sources) or 4)
        req.coverage_threshold = _to_float(context.get("coverage_threshold"), 0.7)
        if context.get("notebook_title"):
            req.notebook_title = str(context["notebook_title"])
        req.delete_notebook_after = _to_bool(context.get("delete_notebook_after"), True)
    return req


def _source_from_dict(raw: Mapping[str, Any]) -> Source | None:
    """Construye un Source desde un dict (tolerante, schema de models.py)."""
    if not isinstance(raw, Mapping):
        return None
    sid = str(raw.get("source_id") or raw.get("id") or "").strip()
    if not sid:
        url = raw.get("url")
        sid = str(url).strip() if url else ""
    if not sid:
        return None
    kind = str(raw.get("kind") or "url").strip().lower()
    if kind not in ("url", "text", "file"):
        kind = "url"
    url_val = (str(raw["url"]) if raw.get("url") else None)
    domain = str(raw.get("domain") or "")
    if not domain and url_val:
        try:
            from urllib.parse import urlparse
            domain = urlparse(url_val).netloc
        except Exception:
            domain = ""
    return Source(
        source_id=sid,
        url=url_val,
        title=str(raw.get("title") or ""),
        snippet=(str(raw["snippet"]) if raw.get("snippet") else None),
        kind=kind,  # type: ignore[arg-type]
        preferred=bool(raw.get("preferred", False)),
        seed=bool(raw.get("seed", False)),
        # --- Capa F: campos del diseno ---
        domain=domain,
        level=raw.get("level"),
        is_preferred_domain=bool(raw.get("is_preferred_domain", raw.get("preferred", False))),
        is_seed=bool(raw.get("is_seed", raw.get("seed", False))),
        covers=list(raw.get("covers") or []),
        retrieved_at=raw.get("retrieved_at"),
        published_or_updated=raw.get("published_or_updated"),
        content_hash=raw.get("content_hash"),
        kept=bool(raw.get("kept", True)),
        evaluation=dict(raw.get("evaluation") or {}),
    )


def _user_text(question: ResearchQuestion, request: ResearchRequest) -> str:
    """Texto final enviado al notebook: pregunta + hint manual del autor.

    La pregunta es autocontenida; el hint manual es orientacion para el
    modelo, no una fuente.
    """
    parts = [question.text.strip()]
    notes = request.manual_notes.strip()
    if notes:
        parts.append(f"Contexto del autor (solo como orientacion): {notes}")
    return "\n\n".join(parts)


def _claim(text: str, source_ids: Sequence[str]) -> Claim:
    """Claim trazable; sin fuentes queda marcado ``unverified``."""
    ids = [s for s in source_ids if s]
    return Claim(text=text, source_ids=ids, unverified=not ids)


def estimate_coverage(
    answers: Sequence[ResearchAnswer], num_questions: int
) -> float:
    """Cobertura = preguntas respondidas con contenido / total de preguntas.

    Si no hay preguntas se considera cobertura completa (1.0): no hay nada
    pendiente, no hay brechas.
    """
    if num_questions <= 0:
        return 1.0
    answered = sum(1 for a in answers if a.answer_md.strip())
    return min(1.0, answered / num_questions)


def _compact_ts() -> str:
    """Timestamp compacto para backups, ej: 20261023T101500Z."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# ---------------------------------------------------------------------------
# Interfaz (Protocol)
# ---------------------------------------------------------------------------


@runtime_checkable
class ResearchBackend(Protocol):
    """Contrato comun de los backends de investigacion.

    El pipeline nunca importa notebooklm-py directamente: solo habla con
    esta interfaz. ``research`` ejecuta el ciclo completo del notebook
    (crear -> subir fuentes -> preguntar -> respuestas -> limpiar).

    Reglas del contrato (spec Capa 4):
    - Todos los metodos son ``async`` (misma firma para fake y real).
    - ``notebook_id`` es un string opaco, no se interpreta afuera.
    - Errores tipados: subclases de ``BackendError``.
    - ``cleanup`` es best-effort e idempotente.
    """

    async def research(
        self,
        concept: ConceptMeta,
        context: Mapping[str, Any] | ResearchRequest | None = None,
    ) -> ResearchResult:
        """Ejecuta la investigacion de un concepto y devuelve el resultado."""
        ...

    async def cleanup(self) -> None:
        """Limpia artefactos pendientes (notebooks sin borrar). Best-effort."""
        ...


# ---------------------------------------------------------------------------
# FakeBackend (determinista, sin red — tests / dry-run / CI)
# ---------------------------------------------------------------------------


@dataclass
class FakeNotebook:
    """Estado interno de un notebook simulado."""

    notebook_id: str
    concept_id: str
    title: str
    sources: dict[str, Source] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    deleted_at: str | None = None


class FakeBackend:
    """Backend en memoria, determinista: mismas entradas -> mismas salidas.

    - Sin credenciales ni red. Respuesta canned por grupo (a/b/c) o fixture
      opcional ``<fixtures_dir>/<concept_id>.json`` (qid -> answer_md).
    - Registra cada llamada en ``calls`` para assertions de tests
      (``backend.was_called("research")``).
    - ``latency_ms`` simula red para probar timeouts/backoff.
    - Counter secuencial: ids predecibles (fake-nb-1, src-1, ...).
    """

    provider = "fake"

    def __init__(
        self,
        fixtures_dir: str | Path | None = None,
        latency_ms: int = 0,
    ) -> None:
        self.latency_ms = int(latency_ms or 0)
        self.notebooks: dict[str, FakeNotebook] = {}
        self.calls: list[dict[str, Any]] = []
        self.last_cleanup: list[str] = []
        self._counter = 0
        self._fixtures: dict[str, dict[str, str]] = {}
        if fixtures_dir:
            self._fixtures = self._load_fixtures(Path(fixtures_dir))

    # -- API ResearchBackend -------------------------------------------------

    async def research(
        self,
        concept: ConceptMeta,
        context: Mapping[str, Any] | ResearchRequest | None = None,
    ) -> ResearchResult:
        req = _coerce_request(concept, context)
        started = time.perf_counter()
        await self._delay()
        self._counter += 1
        nb_id = f"fake-nb-{self._counter}"
        self.notebooks[nb_id] = FakeNotebook(
            notebook_id=nb_id,
            concept_id=req.concept_id,
            title=req.notebook_title or req.title,
        )
        self._record("create_notebook", concept.id, nb_id)

        # Subida de fuentes determinista: ids por orden de arrival.
        uploaded: list[Source] = []
        for i, src in enumerate(req.sources, start=1):
            stored = replace(src, source_id=f"src-{i}")
            self.notebooks[nb_id].sources[stored.source_id] = stored
            uploaded.append(stored)
        self._record("add_sources", nb_id, [s.source_id for s in uploaded])

        # Respuestas deterministas: fixture > canned.
        answers: list[ResearchAnswer] = []
        for q in req.questions:
            raw = self._fixtures.get(req.concept_id, {}).get(q.qid) or self._canned_answer(req, q)
            answers.append(
                ResearchAnswer(
                    qid=q.qid,
                    group=q.group,
                    answer_md=raw,
                    claims=self._canned_claims(raw, uploaded),
                )
            )
        self._record("research", nb_id, [a.qid for a in answers])

        if req.delete_notebook_after:
            await self.delete(nb_id)

        coverage = estimate_coverage(answers, len(req.questions))
        return ResearchResult(
            concept_id=req.concept_id,
            notebook_id=None if req.delete_notebook_after else nb_id,
            answers=answers,
            sources=uploaded,
            failed_sources=[],
            coverage=coverage,
            low_coverage=bool(req.questions) and coverage < req.coverage_threshold,
            low_sources=len(uploaded) < req.min_sources,
            duration_ms=int((time.perf_counter() - started) * 1000),
            backend_provider=self.provider,
            researched_at=now_iso(),
        )

    async def delete(self, notebook_id: str) -> None:
        """Elimina un notebook simulado. Idempotente (no falla si no existe)."""
        await self._delay()
        nb = self.notebooks.get(notebook_id)
        if nb is not None:
            nb.deleted_at = now_iso()
        self._record("delete", notebook_id, nb is not None)

    async def cleanup(self) -> None:
        """Marca todos los notebooks activos como eliminados. Idempotente."""
        await self._delay()
        self.last_cleanup = [
            nid for nid, nb in self.notebooks.items() if nb.deleted_at is None
        ]
        for nb in self.notebooks.values():
            if nb.deleted_at is None:
                nb.deleted_at = now_iso()
        self._record("cleanup", len(self.last_cleanup))

    # -- Helpers para tests ---------------------------------------------------

    def was_called(self, method: str) -> bool:
        """True si se registro al menos una llamada al metodo."""
        return any(c.get("method") == method for c in self.calls)

    def calls_of(self, method: str) -> list[dict[str, Any]]:
        """Todas las llamadas registradas a un metodo, en orden."""
        return [c for c in self.calls if c.get("method") == method]

    # -- Internos ---------------------------------------------------------------

    async def _delay(self) -> None:
        if self.latency_ms > 0:
            await asyncio.sleep(self.latency_ms / 1000.0)

    def _record(self, method: str, *args: Any) -> None:
        self.calls.append({"method": method, "args": args, "ts": now_iso()})

    @staticmethod
    def _load_fixtures(fixtures_dir: Path) -> dict[str, dict[str, str]]:
        """Carga ``<concept_id>.json`` -> {qid: answer_md}; tolerante a errores."""
        if not fixtures_dir.is_dir():
            return {}
        out: dict[str, dict[str, str]] = {}
        for path in sorted(fixtures_dir.glob("*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(raw, Mapping):
                continue
            out[path.stem] = {
                str(qid): str(text)
                for qid, text in raw.items()
                if isinstance(text, str)
            }
        return out

    @staticmethod
    def _group_label(group: str) -> str:
        return {
            "a": "Fundamento estable",
            "b": "Practica moderna",
            "c": "Relaciones y casos de uso",
        }.get(group, "General")

    def _canned_answer(self, req: ResearchRequest, q: ResearchQuestion) -> str:
        """Respuesta generica determinista (no depende de red ni wall-clock)."""
        label = self._group_label(q.group)
        names = ", ".join(
            (s.title or s.source_id) for s in req.sources[:3]
        ) or "fuentes locales"
        return (
            f"**{q.qid} ({q.group}) — {label}.**\n\n"
            f"Respuesta determinista del FakeBackend para '{req.title}' "
            f"(area {req.area or 'n/a'}). Pregunta: {q.text}\n\n"
            f"Fuentes simuladas consultadas: {names}."
        )

    @staticmethod
    def _canned_claims(raw: str, sources: Sequence[Source]) -> list[Claim]:
        """Claims deterministas: hasta 2, trazados a las primeras fuentes.

        Sin fuentes => claim ``unverified`` (la sintesis/validacion lo ve).
        """
        lines = [ln for ln in raw.splitlines() if ln.strip()]
        first = lines[0][:200] if lines else ""
        if not sources:
            return [_claim(first, [])]
        ids = [s.source_id for s in sources[:2]]
        return [
            _claim(first, ids),
            _claim(lines[-1][:200] if len(lines) > 1 else first, ids),
        ]


# ---------------------------------------------------------------------------
# NotebookLMBackend (adaptador async de notebooklm-py)
# ---------------------------------------------------------------------------


def _notebooklm_module() -> Any:
    """Import perezoso de notebooklm; None si el paquete no esta instalado.

    Perezoso para que FakeBackend y los tests no dependan del paquete real.
    """
    try:
        import notebooklm  # type: ignore[import-not-found]
    except ImportError:
        return None
    return notebooklm


def _map_library_error(exc: BaseException, op: str, target: str) -> BackendError:
    """Mapea excepciones de notebooklm-py a la jerarquia del backend.

    El orden importa: se chequea de la subclase mas especifica a la
    generica (RateLimitError y RPCTimeoutError TAMBIEN son RPCError).
    La causa original se encadena en el call site (raise ... from exc).
    """
    nlm = _notebooklm_module()
    if isinstance(exc, asyncio.TimeoutError):
        return BackendTimeout(op, target)
    if nlm is not None:
        if isinstance(exc, (nlm.AuthError, nlm.AuthExtractionError)):
            return BackendAuthError(f"{op}: {exc}")
        if isinstance(exc, nlm.RateLimitError):
            return BackendRateLimitError(f"{op} ({target}): {exc}")
        if isinstance(exc, nlm.RPCTimeoutError):
            return BackendTimeout(op, target, str(exc))
        if isinstance(exc, (nlm.OperationTimeoutError, nlm.WaitTimeoutError)):
            return BackendTimeout(op, target, str(exc))
        if isinstance(exc, nlm.NotFoundError):
            return BackendNotFoundError(f"{op} ({target}): {exc}")
        if isinstance(exc, nlm.ConfigurationError):
            return BackendConfigError(f"{op}: {exc}")
        if isinstance(exc, (nlm.ServerError, nlm.RPCError, nlm.NetworkError)):
            return BackendNetworkError(f"{op} ({target}): {exc}")
        if isinstance(exc, nlm.NotebookLMError):
            return BackendError(f"{op} ({target}): {exc}")
    return BackendError(f"{op} ({target}): {exc}")


class NotebookLMBackend:
    """Adaptador real sobre ``NotebookLMClient`` (notebooklm-py, async).

    - Cliente por corrida de ``research`` via ``from_storage()``: usa el
      storage de la libreria o ``auth_file`` (env var NOTEBOOKLM_AUTH_JSON).
    - Timeouts por operacion con ``asyncio.wait_for``.
    - Retry con backoff exponencial solo ante errores transitorios.
    - Circuit breaker: N fallos de red consecutivos => salto rapido.
    - Limpieza del notebook al terminar; ``cleanup()`` retoma pendientes.
    - ``register_notebook`` (state.py) pone el id en workdir/notebooks.json
      para que Capa 3 reconcilie huerfanos.
    """

    provider = "notebooklm"

    DEFAULT_TIMEOUTS: dict[str, float] = {
        "create_notebook": 30.0,
        "add_source": 60.0,
        "research": 120.0,
        "delete": 30.0,
    }

    def __init__(
        self,
        config: Any = None,
        *,
        workdir: str | Path | None = None,
        auth_file: str | Path | None = None,
        max_retries: int | None = None,
        backoff_seconds: Sequence[float] | None = None,
        circuit_breaker_threshold: int = 3,
        sleep: Callable[[float], Any] | None = None,
        on_attempt: Callable[[str, int, BaseException | None], None] | None = None,
    ) -> None:
        nlm = _notebooklm_module()
        if nlm is None:
            raise BackendConfigError(
                "notebooklm-py no esta instalado; use provider='fake' o "
                "instale el paquete (py -m pip install notebooklm-py)"
            )
        self._nlm = nlm

        self.timeouts: dict[str, float] = {**self.DEFAULT_TIMEOUTS}
        configured = _cfg(config, "backend", "notebooklm", "timeouts", default=None)
        if isinstance(configured, Mapping):
            for key, value in configured.items():
                if key in self.DEFAULT_TIMEOUTS:
                    self.timeouts[key] = _to_float(value, self.DEFAULT_TIMEOUTS[key])
        self.max_concurrent_notebooks = int(
            _cfg(config, "backend", "notebooklm", "max_concurrent_notebooks", default=2) or 2
        )
        self.workdir = state.resolve_workdir(workdir, config)

        # Credenciales: auth_file configurado -> env var que lee from_storage().
        configured_auth = auth_file or _cfg(config, "backend", "notebooklm", "auth_file")
        if configured_auth:
            self.auth_file = Path(os.path.expanduser(str(configured_auth))).resolve()
            # La libreria soporta storage custom via NOTEBOOKLM_AUTH_JSON.
            os.environ.setdefault("NOTEBOOKLM_AUTH_JSON", str(self.auth_file))
        else:
            self.auth_file = None

        backoff_cfg = _cfg(config, "pacing", "backoff_seconds", default=None)
        retries_cfg = _cfg(config, "pacing", "max_retries", default=None)
        self.max_retries = max(1, int(
            max_retries if max_retries is not None else (retries_cfg or 3)
        ))
        if backoff_seconds is not None:
            self.backoff_seconds = tuple(float(b) for b in backoff_seconds)
        elif backoff_cfg:
            self.backoff_seconds = tuple(float(b) for b in backoff_cfg)
        else:
            self.backoff_seconds = (2.0, 4.0, 8.0)
        self.circuit_breaker_threshold = max(1, int(circuit_breaker_threshold))
        self._sleep = sleep or asyncio.sleep
        self.on_attempt = on_attempt
        self._semaphore: asyncio.Semaphore | None = None
        self._pending: dict[str, str] = {}  # notebook_id -> concept_id
        self.last_cleanup: list[str] = []
        self.consecutive_failures = 0

    # -- Validacion fail-fast ---------------------------------------------------

    def validate(self) -> None:
        """Valida credenciales/config al arrancar (spec: fail-fast).

        Con ``auth_file`` configurado e inexistente falla ANTES de procesar
        conceptos. Con storage default se confia en la libreria: si faltan
        cookies, la primera llamada real dara BackendAuthError.
        """
        if self.auth_file is not None and not self.auth_file.is_file():
            raise BackendAuthError(
                f"auth_file de NotebookLM no encontrado: {self.auth_file}. "
                "Renovar credenciales (export de cookies) antes de correr."
            )

    # -- API ResearchBackend --------------------------------------------------------

    async def research(
        self,
        concept: ConceptMeta,
        context: Mapping[str, Any] | ResearchRequest | None = None,
    ) -> ResearchResult:
        """Ciclo completo: crear notebook -> fuentes -> preguntas -> limpiar."""
        req = _coerce_request(concept, context)
        if self.consecutive_failures >= self.circuit_breaker_threshold:
            raise BackendCircuitOpenError(
                self.consecutive_failures, self.circuit_breaker_threshold
            )

        sem = self._semaphore
        if sem is None:
            sem = self._semaphore = asyncio.Semaphore(self.max_concurrent_notebooks)

        started = time.perf_counter()
        async with sem:
            try:
                result = await self._research_locked(req, started)
            except _TRANSIENT as exc:
                # Fallos de red consecutivos abren el circuit breaker.
                self.consecutive_failures += 1
                raise
            except Exception:
                raise
        self.consecutive_failures = 0
        return result

    async def _research_locked(
        self, req: ResearchRequest, started: float
    ) -> ResearchResult:
        """Cuerpo de research con el semaforo ya tomado.

        Ante fallo con notebook ya creado: best-effort delete para no dejar
        huerfanos (spec: "limpieza en fallo"); si la limpieza falla, queda
        en ``_pending`` para que ``cleanup()`` lo retome.
        """
        target = req.concept_id
        uploaded: list[Source] = []
        failed: list[dict[str, Any]] = []
        answers: list[ResearchAnswer] = []
        notebook_deleted = False

        async with self._client_context() as client:
            notebook_id = await self._retry_op(
                "create_notebook",
                target,
                lambda: self._create_notebook(client, req),
            )
            self._track(notebook_id, req.concept_id)
            try:
                uploaded, failed = await self._upload_sources(
                    client, notebook_id, req
                )

                for question in req.questions:
                    answers.append(
                        await self._retry_op(
                            f"research:{question.qid}",
                            target,
                            lambda q=question: self._ask(
                                client, notebook_id, q, req
                            ),
                        )
                    )

                if req.delete_notebook_after:
                    notebook_deleted = await self._delete_best_effort(
                        client, notebook_id
                    )
            except BackendError:
                # Fallo post-create: limpieza best-effort, sin propagar ese
                # error nuevo (el original tiene prioridad y el notebook,
                # si sigue vivo, queda en _pending para cleanup()).
                try:
                    await self._delete_notebook(client, notebook_id)
                    self._untrack(notebook_id)
                except BackendError:
                    pass
                raise

        coverage = estimate_coverage(answers, len(req.questions))
        return ResearchResult(
            concept_id=req.concept_id,
            notebook_id=None if notebook_deleted else notebook_id,
            answers=answers,
            sources=uploaded,
            failed_sources=failed,
            coverage=coverage,
            low_coverage=bool(req.questions) and coverage < req.coverage_threshold,
            low_sources=len(uploaded) < req.min_sources,
            duration_ms=int((time.perf_counter() - started) * 1000),
            backend_provider=self.provider,
            researched_at=now_iso(),
        )

    def _client_context(self) -> Any:
        """Context manager del cliente notebooklm (con auth configurada)."""
        return self._nlm.NotebookLMClient.from_storage()

    async def _create_notebook(self, client: Any, req: ResearchRequest) -> str:
        title = req.notebook_title or req.title
        try:
            nb = await asyncio.wait_for(
                client.notebooks.create(title),
                timeout=self.timeouts["create_notebook"],
            )
        except asyncio.TimeoutError:
            raise BackendTimeout("create_notebook", req.concept_id) from None
        except BaseException as exc:
            raise _map_library_error(exc, "create_notebook", req.concept_id) from exc
        notebook_id = str(nb.id)
        self._register(notebook_id, req.concept_id)
        return notebook_id

    async def _upload_sources(
        self, client: Any, notebook_id: str, req: ResearchRequest
    ) -> tuple[list[Source], list[dict[str, Any]]]:
        """Sube fuentes (best-effort por fuente, segun spec).

        Una fuente que falla (ej. seed con timeout) se registra en
        ``failed`` y no detiene el resto. Los source_ids finales son los
        que asigna NotebookLM: asi coinciden con los de las referencias
        del chat (trazabilidad directa claim -> source_id).
        """
        uploaded: list[Source] = []
        failed: list[dict[str, Any]] = []
        for src in req.sources:
            try:
                lm_source = await self._retry_op(
                    f"add_source:{src.source_id}",
                    notebook_id,
                    lambda s=src: self._add_one_source(client, notebook_id, s),
                )
            except BackendError as exc:
                failed.append(
                    {"source_id": src.source_id, "url": src.url, "error": str(exc)}
                )
                continue
            uploaded.append(lm_source)
        return uploaded, failed

    async def _add_one_source(
        self, client: Any, notebook_id: str, src: Source
    ) -> Source:
        """Sube una fuente; para kind='file', el path vive en Source.url."""
        timeout = self.timeouts["add_source"]
        payload_key = src.source_id
        try:
            if src.kind == "url":
                if not src.url:
                    raise BackendNotFoundError(
                        f"fuente url sin URL: {src.source_id}"
                    )
                res = await asyncio.wait_for(
                    client.sources.add_url(notebook_id, src.url, title=src.title),
                    timeout=timeout,
                )
            elif src.kind == "text":
                text = src.snippet if src.snippet else (src.title or src.source_id)
                res = await asyncio.wait_for(
                    client.sources.add_text(
                        notebook_id, src.title or "fuente", text
                    ),
                    timeout=timeout,
                )
            else:  # file
                path = src.url or src.source_id
                res = await asyncio.wait_for(
                    client.sources.add_file(notebook_id, Path(path)),
                    timeout=timeout,
                )
        except asyncio.TimeoutError:
            raise BackendTimeout("add_source", payload_key) from None
        except BackendError:
            raise
        except BaseException as exc:
            raise _map_library_error(exc, "add_source", payload_key) from exc

        if res is None:
            raise BackendNotFoundError(
                f"add_source no devolvio fuente para {payload_key}"
            )
        return Source(
            source_id=str(res.id),
            url=src.url if src.kind == "url" else getattr(res, "url", None),
            title=str(res.title) if getattr(res, "title", None) else src.title,
            snippet=src.snippet,
            kind=src.kind,
            preferred=src.preferred,
            seed=src.seed,
        )

    async def _ask(
        self,
        client: Any,
        notebook_id: str,
        question: ResearchQuestion,
        req: ResearchRequest,
    ) -> ResearchAnswer:
        try:
            res = await asyncio.wait_for(
                client.chat.ask(notebook_id, _user_text(question, req)),
                timeout=self.timeouts["research"],
            )
        except asyncio.TimeoutError:
            raise BackendTimeout("research", notebook_id) from None
        except BackendError:
            raise
        except BaseException as exc:
            raise _map_library_error(exc, "research", notebook_id) from exc

        answer_md = str(getattr(res, "answer", "") or "")
        return ResearchAnswer(
            qid=question.qid,
            group=question.group,
            answer_md=answer_md,
            claims=self._claims_from_references(res, answer_md),
        )

    @staticmethod
    def _claims_from_references(ask_result: Any, answer_md: str) -> list[Claim]:
        """Trazabilidad afirmacion -> source_id a partir de ChatReference.

        Sin referencias => un claim ``unverified`` con el inicio de la
        respuesta (se advierte, no se inventa una fuente).
        """
        refs = getattr(ask_result, "references", None) or []
        claims: list[Claim] = []
        for ref in refs:
            cited = str(getattr(ref, "cited_text", "") or "")
            sid = str(getattr(ref, "source_id", "") or "")
            if not cited and not sid:
                continue
            text = cited or (answer_md[:200] if answer_md else "")
            claims.append(_claim(text, [sid] if sid else []))
        if not claims and answer_md.strip():
            claims.append(_claim(answer_md.strip().splitlines()[0][:200], []))
        return claims

    async def _delete_notebook(self, client: Any, notebook_id: str) -> None:
        """Elimina el notebook. Idempotente: NotFound se tolera (spec)."""
        try:
            await asyncio.wait_for(
                client.notebooks.delete(notebook_id),
                timeout=self.timeouts["delete"],
            )
        except asyncio.TimeoutError:
            raise BackendTimeout("delete", notebook_id) from None
        except BaseException as exc:
            if isinstance(exc, BackendError):
                raise
            mapped = _map_library_error(exc, "delete", notebook_id)
            if isinstance(mapped, BackendNotFoundError):
                return  # ya no existe: delete es idempotente
            raise mapped from exc

    async def _delete_best_effort(self, client: Any, notebook_id: str) -> bool:
        """Delete sin propagar errores; False si queda pendiente para cleanup()."""
        try:
            await self._delete_notebook(client, notebook_id)
            self._untrack(notebook_id)
            return True
        except BackendError:
            return False  # queda en _pending; cleanup() lo reintentara

    async def cleanup(self) -> None:
        """Elimina notebooks pendientes de borrar (best-effort, idempotente).

        Si alguno queda pendiente (timeout/red), se reintenta en un proximo
        ``cleanup()``; un notebook ya borrado no falla (idempotente).
        """
        self.last_cleanup = []
        if not self._pending:
            return
        try:
            async with self._client_context() as client:
                for notebook_id in list(self._pending):
                    try:
                        await self._delete_notebook(client, notebook_id)
                    except BackendError:
                        continue  # best-effort: sigue con el resto
                    self.last_cleanup.append(notebook_id)
                    self._untrack(notebook_id)
        except BackendError:
            return  # sin auth/sesion: queda pendiente para un proximo cleanup

    # -- Retry con backoff exponencial (solo errores transitorios) -----------

    async def _retry_op(
        self,
        op: str,
        target: str,
        fn: Callable[[], Any],
        *,
        retryable: tuple[type[BaseException], ...] = _TRANSIENT,
    ) -> Any:
        """Ejecuta ``fn`` reintentando solo errores retryable.

        Backoff exponencial [2, 4, 8] (config pacing.backoff_seconds).
        Errores permanentes (auth / not found / config) se propagan al
        primer intento: reintentarlos es hammering inutil.
        """
        last_exc: BaseException | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return await fn()
            except BaseException as exc:  # noqa: BLE001 - se filtra aca abajo
                # Ctrl-C y otros BaseException salen sin tocar.
                if not isinstance(exc, Exception):
                    raise
                if not isinstance(exc, retryable):
                    raise
                last_exc = exc
                if attempt >= self.max_retries:
                    break
                idx = min(attempt - 1, len(self.backoff_seconds) - 1)
                delay = self.backoff_seconds[idx]
                if self.on_attempt is not None:
                    self.on_attempt(op, attempt, exc)
                await self._sleep(delay)
        assert last_exc is not None
        raise last_exc

    # -- Bookkeeping -------------------------------------------------------------

    def _track(self, notebook_id: str, concept_id: str) -> None:
        self._pending[notebook_id] = concept_id

    def _untrack(self, notebook_id: str) -> None:
        self._pending.pop(notebook_id, None)

    def _register(self, notebook_id: str, concept_id: str) -> None:
        """Registra el notebook en workdir/notebooks.json (reconcile Capa 3)."""
        try:
            state.register_notebook(notebook_id, concept_id, workdir=self.workdir)
        except OSError:
            pass  # best-effort: el registro es para reconciliar huerfanos


# ---------------------------------------------------------------------------
# Persistencia en .pipeline/ (sources.json, raw_research.json)
# ---------------------------------------------------------------------------


def pipeline_dir(
    concept_id: str,
    workdir: str | Path | None = None,
    config: Any = None,
) -> Path:
    """Directorio de artefactos de investigacion: ``workdir/.pipeline/<id>/``.

    Sobre la misma disciplina del workdir que estado.json (state.py); los
    artefactos JAMAS se escriben en el vault.
    """
    wd = state.resolve_workdir(workdir, config)
    return wd / ".pipeline" / concept_id


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    """Escritura atomica: temp en el mismo filesystem + ``os.replace``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def _backup_if_exists(path: Path, concept_id: str, workdir: Any) -> None:
    """Backup del artefacto previo antes de sobrescribir (pseudo-codigo).

    En ``workdir/backups/<concept_id>/<name>.<ts>.bak``.
    """
    if not path.is_file():
        return
    backup_dir = Path(state.resolve_workdir(workdir)) / "backups" / concept_id
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / f"{path.name}.{_compact_ts()}.bak"
    try:
        shutil.copy2(path, dest)
    except OSError:
        pass  # best-effort: no bloquear la corrida por un backup fallido


def build_sources_payload(
    result: ResearchResult,
    request: ResearchRequest | None = None,
) -> dict[str, Any]:
    """Payload de sources.json: fuentes finales usadas + counts/flags."""
    return {
        "schema_version": SCHEMA_VERSION,
        "concept_id": result.concept_id,
        "generated_at": result.researched_at,
        "backend_provider": result.backend_provider,
        "count": len(result.sources),
        "failed_count": len(result.failed_sources),
        "low_sources": result.low_sources,
        "min_sources": (request.min_sources if request else 4),
        "sources": [to_dict(s) for s in result.sources],
        "failed_sources": list(result.failed_sources),
    }


def build_raw_research(
    result: ResearchResult,
    request: ResearchRequest | None = None,
) -> dict[str, Any]:
    """Payload de raw_research.json conforme al contrato models.RawResearch."""
    req = request or ResearchRequest(
        concept_id=result.concept_id, title=result.concept_id
    )
    plan = ResearchPlan(questions=req.questions, concept_id=req.concept_id)
    raw = RawResearch(
        concept_id=result.concept_id,
        researched_at=result.researched_at,
        volatility=req.volatility.value,
        freshness_window_days=req.freshness_window_days,
        plan=plan,
        answers=list(result.answers),
        coverage=result.coverage,
        low_coverage=result.low_coverage,
        low_sources=result.low_sources,
        notebook_id=result.notebook_id,
        source_ids=[s.source_id for s in result.sources],
        duration_ms=result.duration_ms,
        backend_provider=result.backend_provider,
    )
    return to_dict(raw)


def persist_research(
    result: ResearchResult,
    request: ResearchRequest | None = None,
    *,
    workdir: str | Path | None = None,
    config: Any = None,
) -> tuple[Path, Path]:
    """Persiste sources.json + raw_research.json (atomicos, con backup previo).

    Devuelve (sources_path, raw_research_path). Nunca escribe en el vault.
    """
    wd = state.resolve_workdir(workdir, config)
    cdir = pipeline_dir(result.concept_id, wd)
    try:
        sources_path = cdir / "sources.json"
        raw_path = cdir / "raw_research.json"
        for target in (sources_path, raw_path):
            _backup_if_exists(target, result.concept_id, wd)
        _atomic_write_json(sources_path, build_sources_payload(result, request))
        _atomic_write_json(raw_path, build_raw_research(result, request))
    except OSError as exc:
        raise ResearchPersistError(
            f"no se pudo persistir la investigacion de {result.concept_id}: {exc}"
        ) from exc
    return sources_path, raw_path


def load_cached_research(
    concept_id: str,
    workdir: str | Path | None = None,
    config: Any = None,
) -> dict[str, Any] | None:
    """raw_research.json persistido de una corrida previa (None si no hay)."""
    raw_path = pipeline_dir(concept_id, workdir, config) / "raw_research.json"
    if not raw_path.is_file():
        return None
    try:
        data = json.loads(raw_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, Mapping) else None


def load_cached_sources(
    concept_id: str,
    workdir: str | Path | None = None,
    config: Any = None,
) -> list[Source]:
    """Fuentes persistidas de una corrida previa (lista vacia si no hay)."""
    sources_path = pipeline_dir(concept_id, workdir, config) / "sources.json"
    if not sources_path.is_file():
        return []
    try:
        data = json.loads(sources_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    raw_list = data.get("sources") if isinstance(data, Mapping) else None
    if not isinstance(raw_list, list):
        return []
    return [s for s in (_source_from_dict(item) for item in raw_list) if s is not None]


def research_result_from_dict(data: Mapping[str, Any]) -> ResearchResult | None:
    """Reconstruye un ResearchResult desde raw_research.json (cache)."""
    if not isinstance(data, Mapping):
        return None
    concept_id = data.get("concept_id")
    if not concept_id:
        return None
    answers: list[ResearchAnswer] = []
    for raw in data.get("answers") or []:
        if not isinstance(raw, Mapping):
            continue
        claims: list[Claim] = []
        for c in raw.get("claims") or []:
            if not isinstance(c, Mapping):
                continue
            claims.append(
                Claim(
                    text=str(c.get("text", "")),
                    source_ids=[str(s) for s in (c.get("source_ids") or [])],
                    unverified=bool(c.get("unverified", False)),
                )
            )
        answers.append(
            ResearchAnswer(
                qid=str(raw.get("qid", "")),
                group=str(raw.get("group", "a")),
                answer_md=str(raw.get("answer_md", "")),
                claims=claims,
            )
        )
    return ResearchResult(
        concept_id=str(concept_id),
        notebook_id=data.get("notebook_id"),
        answers=answers,
        sources=load_cached_sources(str(concept_id)),
        coverage=float(data.get("coverage", 0.0) or 0.0),
        low_coverage=bool(data.get("low_coverage", False)),
        low_sources=bool(data.get("low_sources", False)),
        duration_ms=int(data.get("duration_ms", 0) or 0),
        backend_provider=str(data.get("backend_provider", "fake")),
        researched_at=str(data.get("researched_at") or ""),
    )


# ---------------------------------------------------------------------------
# Integracion con state.py (transiciones a researched / failed)
# ---------------------------------------------------------------------------


async def run_research_phase(
    backend: ResearchBackend,
    concept: ConceptMeta,
    config: Any = None,
    *,
    workdir: str | Path | None = None,
    request: ResearchRequest | Mapping[str, Any] | None = None,
    force: bool = False,
) -> ResearchResult:
    """Fase de investigacion integrada con la maquina de estados.

    Flujo (spec capas 3/4):
    1. Carga estado (o crea pending). Cache: si ya esta ``researched`` (o
       mas alla en el pipeline) y existe raw_research.json, se reusa
       (idempotencia) salvo ``force``.
    2. Transicion valida a ``researching`` (desde pending / failed /
       researching-suspendido). persistencia del checkpoint. Con ``force``
       desde ``researched`` / ``synthesized``: la maquina no permite
       researched -> researching, asi que primero se invalida el resultado
       anterior via researched -> failed (razon "forced") y el estado
       queda re-entrable por la via failed -> researching.
    3. ``backend.research(concept, request)`` + persistencia de artefactos
       en ``.pipeline/<id>/``.
    4. Exito: ``researched`` con phase_data (coverage, paths, notebook_id).
       Fallo: ``failed`` (reintentable) con error y ``failed_phase``
       ("researching"). Errores de auth o circuit breaker se persisten con
       ``failed_reason`` explicito para accion humana; el reintento vuelve
       desde ``failed`` (permitido por la maquina: failed -> researching).

    Re-lanza el error tras persistir el estado failed.

    Nota de estado: la maquina no permite researching -> needs_review, asi
    que TODO error transita a ``failed``; el motivo del bloqueo humano vive
    en ``failed_reason`` dentro de phase_data (auth / circuit_breaker).
    """
    Status = state.ConceptStatus
    wd = state.resolve_workdir(workdir, config)
    st = state.load_state(concept.id, workdir=wd) or state.ConceptState(
        concept_id=concept.id
    )

    # 1. Cache / idempotencia: skip si ya hay investigacion y no fue forzada.
    if not force and st.status in (
        Status.RESEARCHED,
        Status.SYNTHESIZED,
        Status.VALIDATED,
        Status.WRITTEN,
        Status.COMPLETED,
    ):
        cached = load_cached_research(concept.id, workdir=wd)
        rebuilt = research_result_from_dict(cached) if cached else None
        if rebuilt is not None:
            return rebuilt

    # 2. Transicion de entrada a researching (permitidas por la maquina).
    #    - pending / failed / needs_review -> researching (transicion valida).
    #    - researching: reanudacion de corrida interrumpida (mismo estado).
    #    - researched: re-corrida (force=True o cache ausente): la maquina no
    #      permite researched -> researching, asi que se re-ejecuta sin
    #      transicionar (paso 4 solo actualiza phase_data).
    if st.status in (Status.PENDING, Status.FAILED, Status.NEEDS_REVIEW):
        st.transition_to(Status.RESEARCHING, checkpoint="researching")
    elif st.status not in (Status.RESEARCHING, Status.RESEARCHED):
        raise state.InvalidTransitionError(
            f"no se puede investigar {concept.id} desde estado {st.status.value}"
        )
    state.save_state(st, workdir=wd)

    # 3. Ejecucion del backend.
    req = request if isinstance(request, ResearchRequest) else _coerce_request(
        concept, request if isinstance(request, Mapping) else None
    )

    try:
        result = await backend.research(concept, req)
        sources_path, raw_path = persist_research(
            result, req, workdir=wd, config=config
        )
    except Exception as exc:  # noqa: BLE001 - se persiste failed y se re-lanza
        reason = "error"
        if isinstance(exc, BackendAuthError):
            reason = "auth"
        elif isinstance(exc, BackendCircuitOpenError):
            reason = "circuit_breaker"
        elif isinstance(exc, BackendTimeout):
            reason = "timeout"
        elif isinstance(exc, BackendRateLimitError):
            reason = "rate_limit"
        elif isinstance(exc, BackendNetworkError):
            reason = "network"
        elif isinstance(exc, ResearchPersistError):
            reason = "persist"
        st.transition_to(
            Status.FAILED,
            checkpoint="researching",
            phase_data={
                "failed_phase": "researching",
                "failed_reason": reason,
                "research_done": False,
            },
            error=str(exc),
        )
        state.save_state(st, workdir=wd)
        raise

    # 4. Exito: transicion a researched + pointers de artefactos.
    phase_data = {
        "research_done": True,
        "coverage": result.coverage,
        "low_coverage": result.low_coverage,
        "low_sources": result.low_sources,
        "notebook_id": result.notebook_id,
        "sources_path": str(sources_path),
        "raw_research_path": str(raw_path),
        "backend_provider": result.backend_provider,
    }
    if st.status != Status.RESEARCHED:
        st.transition_to(Status.RESEARCHED, checkpoint="researching", phase_data=phase_data)
    else:
        # Re-corrida desde researched (force=True / sin cache): la maquina
        # no permite researched -> researched, se refresca sin transicionar.
        st.phase_data = phase_data
        st.checkpoint = "researching"
    state.save_state(st, workdir=wd)
    return result


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def create_backend(
    config: Any = None,
    provider: str | None = None,
) -> ResearchBackend:
    """Instancia el backend una vez por corrida (spec: no crear por concepto).

    Precedencia: ``provider`` (CLI) > env ``BACKEND_PROVIDER`` >
    ``config.backend.provider`` > "fake".
    """
    p = (
        provider
        or os.environ.get("BACKEND_PROVIDER")
        or _cfg(config, "backend", "provider")
        or "fake"
    )
    p = str(p).strip().lower()

    if p == "fake":
        return FakeBackend(
            fixtures_dir=_cfg(config, "backend", "fake", "fixtures_dir"),
            latency_ms=int(_cfg(config, "backend", "fake", "latency_ms", default=0) or 0),
        )

    if p == "notebooklm":
        backend = NotebookLMBackend(config)
        backend.validate()  # fail-fast antes de procesar conceptos
        return backend

    raise BackendConfigError(
        f"backend desconocido: {p!r} (opciones: 'fake' | 'notebooklm')"
    )
