"""State machine + persistencia del pipeline (Capa 2 de implementacion).

Responsabilidades:
- Enum de estados del ciclo de vida de un concepto.
- Dataclass ``ConceptState`` serializable (estado.json / state.sqlite).
- Transiciones validas y validacion de transicion.
- Persistencia por concepto en ``workdir/concepts/<id>/estado.json`` (o SQLite).
- Reanudacion desde checkpoint y reconciliacion de notebooks huerfanos.
- Reintentos con backoff exponencial y tope configurable.

No toca el vault ni la red. Las fases (investigacion, sintesis, ...) viven en
otras capas; esta solo define el estado y como persistirlo.
"""

from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Estados
# ---------------------------------------------------------------------------


class ConceptStatus(str, Enum):
    """Estados del ciclo de vida de un concepto en el pipeline."""

    PENDING = "pending"
    RESEARCHING = "researching"
    RESEARCHED = "researched"
    SYNTHESIZED = "synthesized"
    VALIDATED = "validated"
    WRITTEN = "written"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


# Aliases para compatibilidad con distintos nombres usados por callers/tests.
StateStatus = ConceptStatus
PipelineStatus = ConceptStatus
ConceptStateStatus = ConceptStatus
Status = ConceptStatus

TERMINAL_STATES: set[ConceptStatus] = {
    ConceptStatus.COMPLETED,
    ConceptStatus.FAILED,
    ConceptStatus.NEEDS_REVIEW,
}

VALID_TRANSITIONS: dict[ConceptStatus, list[ConceptStatus]] = {
    ConceptStatus.PENDING: [ConceptStatus.RESEARCHING],
    ConceptStatus.RESEARCHING: [ConceptStatus.RESEARCHED, ConceptStatus.FAILED],
    ConceptStatus.RESEARCHED: [ConceptStatus.SYNTHESIZED, ConceptStatus.FAILED],
    ConceptStatus.SYNTHESIZED: [
        ConceptStatus.VALIDATED,
        ConceptStatus.FAILED,
        ConceptStatus.NEEDS_REVIEW,
    ],
    ConceptStatus.VALIDATED: [
        ConceptStatus.WRITTEN,
        ConceptStatus.FAILED,
        ConceptStatus.NEEDS_REVIEW,
    ],
    ConceptStatus.WRITTEN: [ConceptStatus.COMPLETED, ConceptStatus.FAILED],
    ConceptStatus.COMPLETED: [],
    ConceptStatus.FAILED: [
        ConceptStatus.RESEARCHING,
        ConceptStatus.RESEARCHED,
        ConceptStatus.SYNTHESIZED,
        ConceptStatus.VALIDATED,
        ConceptStatus.WRITTEN,
    ],
    ConceptStatus.NEEDS_REVIEW: [
        ConceptStatus.RESEARCHING,
        ConceptStatus.SYNTHESIZED,
        ConceptStatus.VALIDATED,
        ConceptStatus.WRITTEN,
        ConceptStatus.COMPLETED,
    ],
}


class InvalidTransitionError(ValueError):
    """Se intento una transicion no permitida entre estados."""


def _to_status(value: Any) -> ConceptStatus | None:
    if value is None:
        return None
    if isinstance(value, ConceptStatus):
        return value
    if isinstance(value, Enum):
        try:
            return ConceptStatus(str(value.value).lower())
        except ValueError:
            pass
    text = str(value).strip().lower()
    if not text:
        return None
    try:
        return ConceptStatus(text)
    except ValueError:
        # Permitir variantes con guiones/espacios.
        normalized = text.replace("-", "_").replace(" ", "_")
        try:
            return ConceptStatus(normalized)
        except ValueError:
            return None


def can_transition(src: Any, dst: Any) -> bool:
    """Indica si la transicion src -> dst esta permitida."""
    s = _to_status(src)
    d = _to_status(dst)
    if s is None or d is None:
        return False
    return d in VALID_TRANSITIONS.get(s, [])


def validate_transition(src: Any, dst: Any) -> None:
    """Valida la transicion; lanza InvalidTransitionError si no es valida."""
    s = _to_status(src)
    d = _to_status(dst)
    if s is None or d is None:
        raise InvalidTransitionError(f"Estado desconocido: {src!r} -> {dst!r}")
    if not can_transition(s, d):
        raise InvalidTransitionError(f"Transicion invalida: {s.value} -> {d.value}")


def is_terminal(status: Any) -> bool:
    return _to_status(status) in TERMINAL_STATES


# ---------------------------------------------------------------------------
# Helpers generales
# ---------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cfg(config: Any, *keys: str, default: Any = None) -> Any:
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


def to_dict(obj: Any) -> dict[str, Any]:
    """Serializa un dataclass (o estructura) a dict serializable."""

    def _convert(value: Any) -> Any:
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, list):
            return [_convert(v) for v in value]
        if isinstance(value, tuple):
            return [_convert(v) for v in value]
        if isinstance(value, dict):
            return {str(k): _convert(v) for k, v in value.items()}
        return value

    if hasattr(obj, "__dataclass_fields__"):
        raw = asdict(obj)
        return {k: _convert(v) for k, v in raw.items()}
    if isinstance(obj, Mapping):
        return {str(k): _convert(v) for k, v in obj.items()}
    return _convert(obj)


# ---------------------------------------------------------------------------
# ConceptState
# ---------------------------------------------------------------------------


@dataclass
class ConceptState:
    """Estado persistido de un concepto (estado.json)."""

    concept_id: str
    status: ConceptStatus = ConceptStatus.PENDING
    last_good_state: ConceptStatus | None = None
    checkpoint: str | None = None
    phase_data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    retries: int = 0
    failure: dict[str, Any] = field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None
    timestamps: dict[str, str] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        self.status = _to_status(self.status) or ConceptStatus.PENDING
        if self.last_good_state is not None:
            self.last_good_state = _to_status(self.last_good_state)

        # Sincronizar created_at / updated_at con timestamps (ambas direcciones).
        if not self.created_at and isinstance(self.timestamps, Mapping):
            self.created_at = self.timestamps.get("created_at")
        if not self.updated_at and isinstance(self.timestamps, Mapping):
            self.updated_at = self.timestamps.get("updated_at")
        if not isinstance(self.timestamps, dict):
            self.timestamps = dict(self.timestamps) if isinstance(self.timestamps, Mapping) else {}
        if self.created_at and "created_at" not in self.timestamps:
            self.timestamps["created_at"] = self.created_at
        if self.updated_at and "updated_at" not in self.timestamps:
            self.timestamps["updated_at"] = self.updated_at

    def transition_to(
        self,
        new_status: Any,
        *,
        checkpoint: str | None = None,
        phase_data: Mapping[str, Any] | None = None,
        error: str | None = None,
        clear_error: bool = True,
        force: bool = False,
    ) -> "ConceptState":
        """Aplica una transicion validada y actualiza last_good_state."""
        new = _to_status(new_status)
        if new is None:
            raise InvalidTransitionError(f"Estado desconocido: {new_status!r}")
        if not force:
            validate_transition(self.status, new)

        # Conservar el ultimo estado "bueno" antes de fallar.
        if self.status not in (ConceptStatus.FAILED, ConceptStatus.NEEDS_REVIEW):
            self.last_good_state = self.status

        self.status = new
        if checkpoint is not None:
            self.checkpoint = checkpoint
        if phase_data is not None:
            self.phase_data = dict(phase_data)
        if error is not None:
            self.error = error
        elif clear_error and new not in (ConceptStatus.FAILED, ConceptStatus.NEEDS_REVIEW):
            self.error = None

        now = now_iso()
        self.updated_at = now
        self.timestamps = self.timestamps or {}
        self.timestamps["updated_at"] = now
        if self.created_at is None:
            self.created_at = now
            self.timestamps["created_at"] = now
        return self


# ---------------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------------


def resolve_workdir(workdir: Any = None, config: Any = None) -> Path:
    if workdir is not None:
        return Path(workdir)
    if config is not None:
        w = _cfg(config, "workdir", default=None)
        if w is None:
            w = _cfg(config, "workdir_path", default=None)
        if w is not None:
            return Path(w)
    return Path.cwd() / "workdir"


def resolve_backend(backend: Any = None, config: Any = None) -> str:
    if backend is not None:
        return str(backend).strip().lower()
    if config is not None:
        b = _cfg(config, "state_backend", default=None)
        if b is None:
            b = _cfg(config, "state", "backend", default=None)
        if b is None:
            b = _cfg(config, "backend", "state", default=None)
        if b is not None:
            return str(b).strip().lower()
    return "json"


def concept_dir(workdir: Any, concept_id: str) -> Path:
    return resolve_workdir(workdir) / "concepts" / concept_id


def _from_dict(data: Mapping[str, Any]) -> ConceptState | None:
    if not isinstance(data, Mapping):
        return None
    cid = data.get("concept_id")
    if not cid:
        return None
    status = _to_status(data.get("status", "pending")) or ConceptStatus.PENDING
    last_good = _to_status(data.get("last_good_state"))
    return ConceptState(
        concept_id=str(cid),
        status=status,
        last_good_state=last_good,
        checkpoint=data.get("checkpoint"),
        phase_data=dict(data.get("phase_data") or {}),
        error=data.get("error"),
        retries=int(data.get("retries", 0) or 0),
        failure=dict(data.get("failure") or {}),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
        timestamps=dict(data.get("timestamps") or {}),
        schema_version=str(data.get("schema_version", SCHEMA_VERSION)),
    )


def _normalize_save_args(args, kwargs):
    state = None
    concept_id = None
    workdir = kwargs.pop("workdir", None)
    if workdir is None:
        workdir = kwargs.pop("workdir_path", None)
    config = kwargs.pop("config", None)
    backend = kwargs.pop("backend", None)

    positional = list(args)
    if positional and isinstance(positional[0], ConceptState):
        state = positional.pop(0)
    elif positional and isinstance(positional[0], Mapping) and "concept_id" in positional[0]:
        state = _from_dict(positional.pop(0))
    if state is None and len(positional) >= 2:
        first, second = positional[0], positional[1]
        if isinstance(second, ConceptState):
            concept_id = first
            state = second
            positional = positional[2:]
        elif isinstance(second, Mapping) and "concept_id" in second:
            concept_id = first
            state = _from_dict(second)
            positional = positional[2:]
    if state is None and positional:
        cand = positional.pop(0)
        if isinstance(cand, ConceptState):
            state = cand
        elif isinstance(cand, Mapping) and "concept_id" in cand:
            state = _from_dict(cand)
    if workdir is None and positional:
        workdir = positional.pop(0)
    if concept_id is not None and state is not None and getattr(state, "concept_id", None) in (None, ""):
        state.concept_id = str(concept_id)
    if state is None:
        raise TypeError("save_state requiere un ConceptState (o dict con concept_id)")
    return state, workdir, config, backend


def save_state(*args, **kwargs) -> Path:
    """Persiste el estado. Devuelve la ruta del artefacto (json) o db."""
    state, workdir, config, backend = _normalize_save_args(args, kwargs)
    wd = resolve_workdir(workdir, config)
    be = resolve_backend(backend, config)

    if state.created_at is None:
        state.created_at = now_iso()
    if state.updated_at is None:
        state.updated_at = now_iso()
    state.timestamps = state.timestamps or {}
    state.timestamps.setdefault("created_at", state.created_at)
    state.timestamps.setdefault("updated_at", state.updated_at)

    if be in ("sqlite", "db", "state.sqlite"):
        wd.mkdir(parents=True, exist_ok=True)
        db_path = wd / "state.sqlite"
        conn = sqlite3.connect(str(db_path))
        try:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS concept_state (
                    concept_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    updated_at TEXT
                )"""
            )
            conn.execute(
                """INSERT INTO concept_state (concept_id, data, updated_at)
                   VALUES (?, ?, ?)
                   ON CONFLICT(concept_id) DO UPDATE SET
                     data = excluded.data,
                     updated_at = excluded.updated_at""",
                (
                    state.concept_id,
                    json.dumps(to_dict(state), ensure_ascii=False),
                    state.updated_at,
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return db_path

    # JSON por concepto.
    cdir = wd / "concepts" / state.concept_id
    cdir.mkdir(parents=True, exist_ok=True)
    target = cdir / "estado.json"
    tmp = cdir / ".estado.json.tmp"
    tmp.write_text(
        json.dumps(to_dict(state), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp.replace(target)
    return target


def _normalize_load_args(args, kwargs):
    concept_id = kwargs.pop("concept_id", None)
    if concept_id is None:
        concept_id = kwargs.pop("id", None)
    workdir = kwargs.pop("workdir", None)
    if workdir is None:
        workdir = kwargs.pop("workdir_path", None)
    if workdir is None:
        workdir = kwargs.pop("path", None)
    config = kwargs.pop("config", None)
    backend = kwargs.pop("backend", None)

    positional = list(args)
    if len(positional) == 2:
        a, b = positional
        a_dir = isinstance(a, (str, Path)) and Path(a).exists() and Path(a).is_dir()
        b_dir = isinstance(b, (str, Path)) and Path(b).exists() and Path(b).is_dir()
        if a_dir and not b_dir:
            workdir = a if workdir is None else workdir
            concept_id = b if concept_id is None else concept_id
        elif b_dir and not a_dir:
            workdir = b if workdir is None else workdir
            concept_id = a if concept_id is None else concept_id
        else:
            if concept_id is None:
                concept_id = a
            if workdir is None:
                workdir = b
    elif len(positional) == 1:
        if concept_id is None:
            concept_id = positional.pop(0)
    elif len(positional) > 2:
        # intentar: workdir, concept_id, ...
        if workdir is None:
            workdir = positional.pop(0)
        if concept_id is None:
            concept_id = positional.pop(0)
    if concept_id is None:
        raise TypeError("load_state requiere concept_id")
    return str(concept_id), workdir, config, backend


def load_state(*args, **kwargs) -> ConceptState | None:
    """Carga el estado de un concepto; None si no existe."""
    concept_id, workdir, config, backend = _normalize_load_args(args, kwargs)
    wd = resolve_workdir(workdir, config)
    be = resolve_backend(backend, config)

    if be in ("sqlite", "db", "state.sqlite"):
        db_path = wd / "state.sqlite"
        if not db_path.exists():
            return None
        conn = sqlite3.connect(str(db_path))
        try:
            cur = conn.execute(
                "SELECT data FROM concept_state WHERE concept_id = ?",
                (concept_id,),
            )
            row = cur.fetchone()
        finally:
            conn.close()
        if not row:
            return None
        try:
            return _from_dict(json.loads(row[0]))
        except (json.JSONDecodeError, TypeError):
            return None

    target = wd / "concepts" / concept_id / "estado.json"
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    # A3: validar artefacto de estado leido (skip si no existe / vacio / sin contenido).
    if data:
        from backend import validate_artifact_schema

        validate_artifact_schema(data, "state")
    return _from_dict(data)


def load_all_states(
    workdir: Any = None,
    config: Any = None,
    backend: Any = None,
) -> dict[str, ConceptState]:
    """Carga todos los estados persistidos."""
    wd = resolve_workdir(workdir, config)
    be = resolve_backend(backend, config)
    out: dict[str, ConceptState] = {}

    if be in ("sqlite", "db", "state.sqlite"):
        db_path = wd / "state.sqlite"
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            try:
                for (raw,) in conn.execute("SELECT data FROM concept_state"):
                    st = _from_dict(json.loads(raw))
                    if st is not None:
                        out[st.concept_id] = st
            finally:
                conn.close()
        return out

    concepts_root = wd / "concepts"
    if concepts_root.exists():
        for path in concepts_root.glob("*/estado.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            st = _from_dict(data)
            if st is not None:
                out[st.concept_id] = st
    return out


def resume_from_checkpoint(
    state_or_id: "ConceptState | str",
    workdir: Any = None,
    config: Any = None,
    backend: Any = None,
    phase: str | None = None,
) -> ConceptState:
    """Reanuda (o inicializa) el checkpoint de un concepto y persiste.

    - Si se pasa un id (str), carga el estado o crea uno nuevo (pending).
    - Si el estado es terminal (completed), se devuelve sin cambios.
    - Si se indica ``phase``, se usa como checkpoint.
    - Si no hay checkpoint, se deriva del status actual.
    """
    if isinstance(state_or_id, str):
        loaded = load_state(state_or_id, workdir=workdir, config=config, backend=backend)
        state = loaded if loaded is not None else ConceptState(concept_id=state_or_id)
    else:
        state = state_or_id

    if state.status == ConceptStatus.COMPLETED:
        return state

    if phase is not None:
        state.checkpoint = str(phase)
    if state.checkpoint is None:
        state.checkpoint = state.status.value

    state.updated_at = now_iso()
    state.timestamps = state.timestamps or {}
    state.timestamps["updated_at"] = state.updated_at
    if state.created_at is None:
        state.created_at = state.updated_at
        state.timestamps["created_at"] = state.created_at

    save_state(state, workdir=workdir, config=config, backend=backend)
    return state


def reconcile_orphan_notebooks(
    workdir: Any = None,
    config: Any = None,
    backend: Any = None,
    delete: bool = False,
    registry_name: str = "notebooks.json",
) -> list[str]:
    """Detecta notebooks registrados que ya no estan referenciados por ningun estado.

    Mantiene un registro simple ``workdir/notebooks.json``:
    ``{notebook_id: concept_id}``. Un notebook es huerfano si:
    - no aparece en ``phase_data`` de ningun estado, o
    - su concepto esta ausente o en estado terminal (failed/needs_review).

    Si ``delete=True``, los huerfanos se quitan del registro.
    Devuelve la lista de ids huerfanos.
    """
    wd = resolve_workdir(workdir, config)
    states = load_all_states(workdir=wd, config=config, backend=backend)

    referenced: set[str] = set()
    for st in states.values():
        pd = st.phase_data or {}
        for key in ("notebook_id", "notebook"):
            val = pd.get(key)
            if val:
                referenced.add(str(val))
        ids = pd.get("notebook_ids")
        if isinstance(ids, (list, tuple, set)):
            for nid in ids:
                if nid:
                    referenced.add(str(nid))

    registry_path = wd / registry_name
    recorded: dict[str, Any] = {}
    if registry_path.exists():
        try:
            raw = json.loads(registry_path.read_text(encoding="utf-8"))
            if isinstance(raw, Mapping):
                recorded = dict(raw)
        except (json.JSONDecodeError, OSError):
            recorded = {}

    orphans: list[str] = []
    for nid, cid in recorded.items():
        nid = str(nid)
        cid = str(cid) if cid is not None else None
        st = states.get(cid) if cid else None
        if nid not in referenced:
            orphans.append(nid)
            continue
        if st is None or st.status in (ConceptStatus.FAILED, ConceptStatus.NEEDS_REVIEW):
            if nid not in orphans:
                orphans.append(nid)

    # Dedup preservando orden.
    seen: set[str] = set()
    unique: list[str] = []
    for nid in orphans:
        if nid in seen:
            continue
        seen.add(nid)
        unique.append(nid)

    if delete:
        for nid in unique:
            recorded.pop(nid, None)
        wd.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(
            json.dumps(recorded, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return unique


def register_notebook(
    notebook_id: str,
    concept_id: str,
    workdir: Any = None,
    config: Any = None,
    registry_name: str = "notebooks.json",
) -> Path:
    """Registra un notebook en el indice (util para reconcile)."""
    wd = resolve_workdir(workdir, config)
    wd.mkdir(parents=True, exist_ok=True)
    registry_path = wd / registry_name
    recorded: dict[str, Any] = {}
    if registry_path.exists():
        try:
            raw = json.loads(registry_path.read_text(encoding="utf-8"))
            if isinstance(raw, Mapping):
                recorded = dict(raw)
        except (json.JSONDecodeError, OSError):
            recorded = {}
    recorded[str(notebook_id)] = str(concept_id)
    registry_path.write_text(
        json.dumps(recorded, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return registry_path


# ---------------------------------------------------------------------------
# Reintentos con backoff exponencial
# ---------------------------------------------------------------------------


def exponential_backoff_seconds(
    max_retries: int = 3,
    base: float = 2.0,
    factor: float = 2.0,
    cap: float | None = None,
) -> list[float]:
    """Genera la lista de delays (backoff exponencial) para ``max_retries`` intentos."""
    delays: list[float] = []
    for i in range(max_retries):
        delay = base * (factor ** i)
        if cap is not None:
            delay = min(delay, cap)
        delays.append(delay)
    return delays


def retry_with_backoff(
    func: Callable[..., Any],
    *args: Any,
    max_retries: int = 3,
    backoff_seconds: Sequence[float] = (2, 4, 8),
    on_retry: Callable[[int, BaseException, float], None] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    **kwargs: Any,
) -> Any:
    """Ejecuta ``func`` con reintentos y backoff exponencial.

    - ``max_retries``: tope de intentos.
    - ``backoff_seconds``: delays por intento (se reutiliza el ultimo si se agota).
    - Lanza la ultima excepcion si se agotan los intentos.
    """
    if max_retries < 1:
        raise ValueError("max_retries debe ser >= 1")

    last_exc: BaseException | None = None
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 - reintentamos errores de fase
            last_exc = exc
            if attempt >= max_retries:
                break
            idx = min(attempt - 1, len(backoff_seconds) - 1) if backoff_seconds else 0
            delay = float(backoff_seconds[idx]) if backoff_seconds else 0.0
            if on_retry is not None:
                try:
                    on_retry(attempt, exc, delay)
                except Exception:  # noqa: BLE001
                    pass
            sleep(delay)

    if last_exc is not None:
        raise last_exc
    raise RuntimeError("retry_with_backoff: no se ejecuto ningun intento")


def execute_phase_with_retry(
    phase_fn: Callable[[str], Any],
    concept_id: str,
    *,
    max_retries: int = 3,
    backoff_seconds: Sequence[float] = (2, 4, 8),
    sleep: Callable[[float], None] = time.sleep,
    on_retry: Callable[[int, BaseException, float], None] | None = None,
) -> Any:
    """Wrapper conveniente para reintentar una fase del pipeline."""
    return retry_with_backoff(
        phase_fn,
        concept_id,
        max_retries=max_retries,
        backoff_seconds=backoff_seconds,
        on_retry=on_retry,
        sleep=sleep,
    )


def with_retry(
    max_retries: int = 3,
    backoff_seconds: Sequence[float] = (2, 4, 8),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorador de reintentos con backoff."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return retry_with_backoff(
                func,
                *args,
                max_retries=max_retries,
                backoff_seconds=backoff_seconds,
                **kwargs,
            )

        return wrapper

    return decorator


__all__ = [
    "SCHEMA_VERSION",
    "ConceptStatus",
    "StateStatus",
    "PipelineStatus",
    "ConceptStateStatus",
    "Status",
    "TERMINAL_STATES",
    "VALID_TRANSITIONS",
    "InvalidTransitionError",
    "can_transition",
    "validate_transition",
    "is_terminal",
    "now_iso",
    "to_dict",
    "ConceptState",
    "resolve_workdir",
    "resolve_backend",
    "concept_dir",
    "save_state",
    "load_state",
    "load_all_states",
    "resume_from_checkpoint",
    "reconcile_orphan_notebooks",
    "register_notebook",
    "exponential_backoff_seconds",
    "retry_with_backoff",
    "execute_phase_with_retry",
    "with_retry",
]
