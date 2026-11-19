# -*- coding: utf-8 -*-
"""Entidades del release: contenido publico (L0.2).

Son los esquemas que validan `releases/<release_id>/` y la API.
"""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .ids import uid_relacion


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)


class Area(_Base):
    uid: str = Field(pattern=r"^a_[0-9A-Z]{10}$")
    name: str = Field(min_length=1)
    order: int = Field(ge=0)
    color_token: Optional[str] = None


class Source(_Base):
    uid: str = Field(pattern=r"^s_[0-9A-Z]{10}$")
    url: str = Field(min_length=1)
    title: str = Field(min_length=1)
    tier: int = Field(ge=1, le=4)
    concept_uids: List[str] = Field(default_factory=list)


class ConceptSections(_Base):
    objetivo: Optional[str] = None
    ideas_clave: Optional[str] = None
    como_funciona: Optional[str] = None
    detalles: Optional[str] = None
    ejemplo_minimo: Optional[str] = None
    errores_comunes: Optional[str] = None
    estado_actual: Optional[str] = None
    conexiones: Optional[str] = None
    ruta_estudio: Optional[str] = None
    preguntas_repaso: Optional[str] = None


class VerificationMark(_Base):
    section: str
    kind: str  # "sin_verificar" | "verificar"


class Concept(_Base):
    uid: str = Field(pattern=r"^c_[0-9A-Z]{10}$")
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    aliases: List[str] = Field(default_factory=list)
    area_uid: Optional[str] = None
    sections: ConceptSections = Field(default_factory=ConceptSections)
    sources: List[str] = Field(default_factory=list)
    verification_marks: List[VerificationMark] = Field(default_factory=list)
    content_hash: str = Field(min_length=1)


class RelationType(str, Enum):
    depends_on = "depends_on"
    uses = "uses"
    implements = "implements"
    communicates_with = "communicates_with"
    complements = "complements"
    prerequisite = "prerequisite"
    specializes = "specializes"
    applied_in = "applied_in"
    untyped = "untyped"


class TypeBasis(str, Enum):
    explicit = "explicit"
    reviewed = "reviewed"
    none = "none"


class ExplanationStatus(str, Enum):
    quoted = "quoted"
    authored = "authored"
    derived = "derived"
    reviewed = "reviewed"
    stale = "stale"


class Explanation(_Base):
    text: str
    status: ExplanationStatus
    evidence_chunk_ids: List[str] = Field(default_factory=list)


class Relation(_Base):
    """Dirigida: A->B y B->A son dos relaciones."""

    uid: str = Field(pattern=r"^r_[0-9a-f]{64}$")
    source_uid: str = Field(pattern=r"^c_[0-9A-Z]{10}$")
    target_uid: str = Field(pattern=r"^c_[0-9A-Z]{10}$")
    type: RelationType = RelationType.untyped
    type_basis: TypeBasis = TypeBasis.none
    explanation: Optional[Explanation] = None
    cross_area: bool = False

    def determinar_uid(self) -> str:
        return uid_relacion(self.source_uid, self.target_uid)


class JourneyKind(str, Enum):
    project = "project"
    role = "role"
    course = "course"
    certification = "certification"
    self_study = "self_study"
    job_change = "job_change"
    other = "other"


class PeriodBasis(str, Enum):
    documented = "documented"
    confirmed_from_metadata = "confirmed_from_metadata"


class Period(_Base):
    start: date
    end: Optional[date] = None
    precision: str  # "day" | "month" | "year"
    basis: PeriodBasis


class Publication(str, Enum):
    private = "private"
    candidate = "candidate"
    approved = "approved"


class JourneyRecord(_Base):
    uid: str = Field(pattern=r"^j_[0-9A-Z]{10}$")
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    kind: List[JourneyKind] = Field(default_factory=list)
    period: Optional[Period] = None
    context: Optional[str] = None
    objective: Optional[str] = None
    description: Optional[str] = None
    decisions: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    problems: List[str] = Field(default_factory=list)
    solutions: List[str] = Field(default_factory=list)
    results: List[str] = Field(default_factory=list)
    evidence_uids: List[str] = Field(default_factory=list)
    concept_uids: List[str] = Field(default_factory=list)
    stage: Optional[str] = None
    topics: List[str] = Field(default_factory=list)
    publication: Publication = Publication.approved
    content_hash: str = Field(min_length=1)


class EvidenceKind(str, Enum):
    image = "image"
    video = "video"
    document = "document"
    link = "link"
    code = "code"


class EvidenceVariant(_Base):
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    storage_key: str
    mime: str
    size: int = Field(ge=0)


class EvidenceReview(str, Enum):
    manually_reviewed = "manually_reviewed"


class Evidence(_Base):
    uid: str = Field(pattern=r"^e_[0-9A-Z]{10}$")
    record_uid: str = Field(pattern=r"^j_[0-9A-Z]{10}$")
    kind: EvidenceKind
    storage_key: str = Field(min_length=1)
    sha256: str = Field(min_length=1)
    mime: str = Field(min_length=1)
    size: int = Field(ge=0)
    variants: List[EvidenceVariant] = Field(default_factory=list)
    alt_text: Optional[str] = None
    review: EvidenceReview = EvidenceReview.manually_reviewed


class TourTargetType(str, Enum):
    concept = "concept"
    relation = "relation"
    record = "record"
    view = "view"


class TourStep(_Base):
    target: TourTargetType
    uid: Optional[str] = None
    text: str = Field(min_length=1)


class Tour(_Base):
    uid: str = Field(pattern=r"^t_[0-9A-Z]{10}$")
    title: str = Field(min_length=1)
    steps: List[TourStep] = Field(default_factory=list)


class ViewType(str, Enum):
    overview = "overview"
    contextual = "contextual"


class Origin(str, Enum):
    manual = "manual"
    chat = "chat"


class Camera(_Base):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    zoom: float = 1.0


class ExplorationState(_Base):
    """Vive en el cliente; versionado junto al release."""

    version: int = Field(ge=1)
    release_id: str = Field(min_length=1)
    view_type: ViewType
    focus_uids: List[str] = Field(default_factory=list)
    relation_uids: List[str] = Field(default_factory=list)
    filters: Dict[str, str] = Field(default_factory=dict)
    camera: Optional[Camera] = None
    origin: Origin = Origin.manual
    created_at: Optional[str] = None
    label: Optional[str] = None
