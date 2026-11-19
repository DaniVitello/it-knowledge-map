# -*- coding: utf-8 -*-
"""Esquemas Pydantic de las salidas de C0 y C1 (contratos de etapa)."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ZoneKind(str, Enum):
    frontmatter = "frontmatter"
    titulo = "titulo"
    navegacion = "navegacion"
    que_abarca = "que_abarca"
    mis_notas = "mis_notas"
    bloque_ai = "bloque_ai"
    relacionados = "relacionados"
    pie = "pie"
    otro = "otro"


class Zone(_Base):
    kind: ZoneKind
    name: str = ""
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    publicable: bool = False
    text: str = ""


class ScanSignal(_Base):
    kind: str
    zone: Optional[str] = None
    excerpt: Optional[str] = None


class InventoryItem(_Base):
    id_temporal: str
    hash_de_ruta: str = Field(min_length=1)
    tipo: str  # "markdown" | "image" | "journey_raw" | "otro"
    sha256: str = Field(min_length=1)
    clasificacion: str = "private"
    signals: List[ScanSignal] = Field(default_factory=list)


class InventorySummary(_Base):
    total: int = 0
    por_tipo: Dict[str, int] = Field(default_factory=dict)
    por_clasificacion: Dict[str, int] = Field(default_factory=dict)
    con_senales: int = 0
    por_origen: Dict[str, int] = Field(default_factory=dict)


class Inventory(_Base):
    items: List[InventoryItem] = Field(default_factory=list)
    summary: InventorySummary = Field(default_factory=InventorySummary)
    vault_hash: str = Field(min_length=1)


class WikiLink(_Base):
    destino_textual: str
    alias: Optional[str] = None
    heading: Optional[str] = None
    seccion: str
    oracion: str
    offset: int = Field(ge=0)
    zona: str


class VerificationMark(_Base):
    section: str
    kind: str  # "sin_verificar" | "verificar"


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


class SourceRef(_Base):
    url: str
    title: Optional[str] = None


class ParsedConcept(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note_id: str
    titulo: str
    frontmatter: Dict[str, Any] = Field(default_factory=dict)
    zones: List[Zone] = Field(default_factory=list)
    sections: ConceptSections = Field(default_factory=ConceptSections)
    sections_missing: List[str] = Field(default_factory=list)
    wikilinks: List[WikiLink] = Field(default_factory=list)
    marks: List[VerificationMark] = Field(default_factory=list)
    sources: List[SourceRef] = Field(default_factory=list)
    content_hash: str = Field(min_length=1)


class RunRecord(_Base):
    etapa: str
    version: int = Field(ge=1)
    hash_entrada: str = Field(min_length=1)
    hash_salida: str = Field(min_length=1)
    duracion_s: float = Field(ge=0)
    cache_hit: bool = False
    warnings: List[str] = Field(default_factory=list)
    errores: List[str] = Field(default_factory=list)


class RunLog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    etapas: List[RunRecord] = Field(default_factory=list)
    ok: bool = True
