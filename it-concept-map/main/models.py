"""Modelos y contratos de datos del proyecto IT Career Concept Map.

Capa 1 de implementacion: contratos compartidos por todo el pipeline.
Cada dataclass lleva ``schema_version`` para versionado de los artefactos
persistidos (sources.json, raw_research.json, synthesis.json, validation.json,
estado.json).

Referencia: "explicacion del proyecto por capas v1.md" (Capas 1, 6, 7, 8, 5, 3).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Literal

SCHEMA_VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Volatility(str, Enum):
    """Volatilidad del concepto: determina la ventana de frescura de la investigacion."""

    STABLE = "stable"
    SEMI_STABLE = "semi_stable"
    DYNAMIC = "dynamic"


# ConceptStatus vive en state.py (fuente unica). Alias para compatibilidad.
# (Capa A: se elimina el enum duplicado de models.py.)
try:
    from .state import ConceptStatus as ConceptStatus
except Exception:  # pragma: no cover
    ConceptStatus = None  # type: ignore


class Severity(str, Enum):
    """Severidad de un chequeo de validacion."""

    ERROR = "error"
    WARN = "warn"


class PromptContext(str, Enum):
    """Contexto de prompt para la sintesis."""

    FRONTEND = "frontend"
    BACKEND = "backend"
    DATA = "data"
    INFRA = "infra"
    GENERAL = "general"


# ---------------------------------------------------------------------------
# ConceptMeta (Capa 1)
# ---------------------------------------------------------------------------


@dataclass
class ConceptMeta:
    """Ficha de un concepto del vault. Unica representacion compartida por el pipeline."""

    # --- Identidad y ubicacion ---
    id: str
    title: str
    area: str
    note_path: Path

    # --- Aliases / metadatos crudos ---
    slug: str = ""
    numero: int | None = None
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    # --- Contenido manual del autor (fuente de verdad del vault) ---
    key_ideas: list[str] = field(default_factory=list)
    connections: list[str] = field(default_factory=list)

    # --- Frontmatter crudo ---
    frontmatter: dict[str, Any] | None = None

    # --- Clasificacion y estrategia de investigacion ---
    volatility: Volatility = Volatility.SEMI_STABLE
    professional_roles: list[str] = field(default_factory=list)
    preferred_domains: list[str] = field(default_factory=list)
    seed_urls: list[str] = field(default_factory=list)

    # --- Trazabilidad de lectura (integridad) ---
    has_ai_block: bool = False
    content_hash_outside: str | None = None
    # --- Capa A: campos del diseno ---
    concept_id: str | None = None
    path: str | None = None
    content_hash_outside_ai: str | None = None
    content_hash_inside: str | None = None
    outside_hash_at_read: str | None = None
    mtime_at_read: float | None = None
    newline: str | None = None
    has_frontmatter: bool = False
    has_bom: bool = False
    concept_dir: Path | None = None

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Investigacion (Capa 6)
# ---------------------------------------------------------------------------


@dataclass
class Source:
    """Fuente de investigacion (URL, texto pegado o archivo)."""

    source_id: str
    url: str | None = None
    title: str = ""
    snippet: str | None = None
    kind: Literal["url", "text", "file"] = "url"
    preferred: bool = False
    seed: bool = False
    # --- Capa A: campos del diseno (punto 2) ---
    domain: str = ""
    level: int | None = None
    is_preferred_domain: bool = False
    is_seed: bool = False
    covers: list[str] = field(default_factory=list)
    retrieved_at: str | None = None
    published_or_updated: str | None = None
    content_hash: str | None = None
    kept: bool = True
    evaluation: dict[str, Any] = field(default_factory=dict)

    schema_version: str = SCHEMA_VERSION


@dataclass
class ResearchQuestion:
    """Pregunta de investigacion agrupada por dimension (a/b/c)."""

    qid: str
    group: Literal["a", "b", "c"]
    text: str

    schema_version: str = SCHEMA_VERSION


@dataclass
class ResearchPlan:
    """Plan de investigacion para un concepto."""

    questions: list[ResearchQuestion] = field(default_factory=list)
    concept_id: str | None = None
    # --- Capa A: campos del diseno ---
    questions_by_dim: dict[str, list[str]] = field(default_factory=dict)
    relation_questions: list[dict[str, str]] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)
    source_requirements: dict[str, Any] = field(default_factory=dict)

    schema_version: str = SCHEMA_VERSION


@dataclass
class Claim:
    """Afirmacion trazable a fuentes."""

    text: str
    source_ids: list[str] = field(default_factory=list)
    unverified: bool = False
    # --- Capa A: campos del diseno ---
    claim_id: str = ""
    status: str = ""

    schema_version: str = SCHEMA_VERSION


@dataclass
class ResearchAnswer:
    """Respuesta cruda de investigacion (con claims trazables)."""

    qid: str
    group: str
    answer_md: str = ""
    claims: list[Claim] = field(default_factory=list)

    schema_version: str = SCHEMA_VERSION


@dataclass
class RawResearch:
    """Resultado crudo persistido como raw_research.json."""

    concept_id: str
    researched_at: str
    volatility: str
    freshness_window_days: int
    plan: ResearchPlan
    answers: list[ResearchAnswer] = field(default_factory=list)
    coverage: float = 0.0
    low_coverage: bool = False
    low_sources: bool = False
    gap_pass_done: bool = False
    gaps_detected: int = 0
    gaps_resolved: int = 0
    notebook_id: str | None = None
    source_ids: list[str] = field(default_factory=list)
    duration_ms: int = 0
    backend_provider: str = "fake"

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Sintesis (Capa 7)
# ---------------------------------------------------------------------------


@dataclass
class CrossLink:
    """Cross-link a un concepto vecino."""

    target_concept_id: str | None
    target_title: str
    wikilink: str
    reason: str = ""
    exists: bool = False
    direction: Literal["out", "in", "both"] = "both"

    schema_version: str = SCHEMA_VERSION


@dataclass
class ClaimRef:
    """Referencia de trazabilidad afirmacion -> source_id."""

    claim_text: str
    source_ids: list[str] = field(default_factory=list)
    section: str = ""
    unverified: bool = False

    schema_version: str = SCHEMA_VERSION


@dataclass
class Synthesis:
    """Resultado de la sintesis (study guide) persistido como synthesis.json."""

    concept_id: str
    title: str
    markdown: str
    sections: dict[str, str] = field(default_factory=dict)
    stable_foundation: str = ""
    modern_practice: str = ""
    cross_links: list[CrossLink] = field(default_factory=list)
    claims_index: list[ClaimRef] = field(default_factory=list)
    prompt_template_hash: str = ""
    prompt_version: str = ""
    prompt_context: str = "general"
    generated_at: str = ""
    coverage: float = 0.0
    low_coverage: bool = False
    # --- Capa A: campos del diseno ---
    claims: list[Claim] = field(default_factory=list)
    unverified_items: list[str] = field(default_factory=list)

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Validacion (Capa 8)
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    """Resultado de un chequeo individual de validacion."""

    check_id: str
    name: str
    layer: Literal["deterministic", "semantic"]
    severity: Severity
    passed: bool
    message: str = ""
    evidence: dict[str, Any] | None = None
    duration_ms: int = 0

    schema_version: str = SCHEMA_VERSION


# Alias historico/usado por la spec.
Check = CheckResult


@dataclass
class ValidationReport:
    """Resultado de la validacion de una sintesis."""

    concept_id: str
    synthesis_path: str = ""
    checked_at: str = ""
    prompt_template_hash: str = ""
    checks: list[CheckResult] = field(default_factory=list)
    errors: list[CheckResult] = field(default_factory=list)
    warnings: list[CheckResult] = field(default_factory=list)
    is_valid: bool = False
    blocked_reason: str | None = None
    score: float = 0.0
    # --- Capa A: campos del diseno ---
    blocking_failures: list[str] = field(default_factory=list)
    verdict: str = "approved"

    schema_version: str = SCHEMA_VERSION


# Alias para compatibilidad con la spec (ValidationResult).
ValidationResult = ValidationReport


# ---------------------------------------------------------------------------
# Escritura (Capa 5)
# ---------------------------------------------------------------------------


@dataclass
class WriteResult:
    """Resultado de la escritura segura en el vault."""

    path: Path
    backup_path: Path | None = None
    outside_hash: str | None = None
    inside_hash: str | None = None
    written_at: str | None = None
    success: bool = True
    # --- Capa A: campos del diseno ---
    concept_id: str | None = None
    ai_block_hash: str | None = None
    outside_block_hash_before: str | None = None
    outside_block_hash_after: str | None = None
    verified: bool = False

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Estado (Capa 3)
# ---------------------------------------------------------------------------


@dataclass
class ConceptState:
    """Estado persistido de un concepto (estado.json)."""

    concept_id: str
    status: ConceptStatus = ConceptStatus.PENDING
    checkpoint: str | None = None
    phase_data: dict[str, Any] = field(default_factory=dict)
    retries: int = 0
    last_error: str | None = None
    blocked_reason: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    # --- Capa A: campos del diseno ---
    last_good_state: str | None = None
    failure: dict[str, Any] = field(default_factory=dict)

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def to_dict(obj: Any) -> dict[str, Any]:
    """Serializa un dataclass a dict (con conversion de Path/Enum)."""

    def _convert(value: Any) -> Any:
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, list):
            return [_convert(v) for v in value]
        if isinstance(value, dict):
            return {k: _convert(v) for k, v in value.items()}
        return value

    raw = asdict(obj)
    return {k: _convert(v) for k, v in raw.items()}


# ---------------------------------------------------------------------------
# Excepciones de la capa (Capa 1)
# ---------------------------------------------------------------------------


class ConceptModelError(Exception):
    """Error base del modelo de concepto."""


class MissingRequiredFieldError(ConceptModelError):
    """Falta un campo obligatorio no derivable (title/area)."""


class InvalidFrontmatterError(ConceptModelError):
    """Frontmatter YAML invalido."""


class UnknownAreaError(ConceptModelError):
    """Area no reconocida (solo si config lo exige)."""


class InvalidVolatilityError(ConceptModelError):
    """Volatilidad fuera del enum."""
