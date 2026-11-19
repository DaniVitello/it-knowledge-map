# -*- coding: utf-8 -*-
"""C4 — Relaciones: tipo y explicacion (L1, capa 6).

Asigna tipo (8 + untyped) y explicacion (quoted/authored/derived/reviewed/stale).
El tipo nunca se infiere sin revision.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ikm.contracts.errors import AbortStage
from ikm.contracts.release import Explanation, ExplanationStatus, Relation, RelationType, TypeBasis

# Tipos validos (seccion 6.3 de la spec)
TIPOS_VALIDOS = {
    "depends_on", "uses", "implements", "communicates_with",
    "complements", "prerequisite", "specializes", "applied_in", "untyped",
}

# Marcas explicitas en el vault que indican tipo de relacion
MARCAS_TIPO = {
    "depends_on": ["depende de", "depends on", "depende"],
    "uses": ["usa", "uses", "utiliza"],
    "implements": ["implementa", "implements"],
    "communicates_with": ["se comunica con", "communicates with", "comunica"],
    "complements": ["complementa", "complements"],
    "prerequisite": ["prerequisito", "prerequisite", "requiere"],
    "specializes": ["especializa", "specializes", "es un tipo de"],
    "applied_in": ["se aplica en", "applied in", "aplicado en"],
}


def _normalizar(s: str) -> str:
    return (s or "").lower().strip()


def _detectar_tipo_explicito(oracion: str) -> Optional[str]:
    """Detecta tipo de relacion desde marca explicita en la oracion del link.

    Nunca infiere sin revision: solo asigna tipo si hay marca explicita.
    """
    oracion_n = _normalizar(oracion)
    for tipo, marcas in MARCAS_TIPO.items():
        for marca in marcas:
            if marca in oracion_n:
                return tipo
    return None


def _extraer_quoted(oracion: str, seccion: str) -> str:
    """Captura la oracion y seccion donde aparece el link como explicacion quoted."""
    texto = (oracion or "").strip()
    if seccion:
        return f"[{seccion}] {texto}"
    return texto


def asignar_tipo(rel: Relation, oracion: str) -> Relation:
    """Asigna tipo desde marca explicita o 'untyped'. Nunca infiere sin revision."""
    tipo = _detectar_tipo_explicito(oracion)
    if tipo:
        rel.type = RelationType(tipo)
        rel.type_basis = TypeBasis.explicit
    else:
        rel.type = RelationType.untyped
        rel.type_basis = TypeBasis.none
    return rel


def extraer_quoted(rel: Relation, oracion: str, seccion: str) -> Relation:
    """Asigna explicacion quoted desde la oracion del link."""
    texto = _extraer_quoted(oracion, seccion)
    if texto:
        rel.explanation = Explanation(
            text=texto,
            status=ExplanationStatus.quoted,
            evidence_chunk_ids=[],
        )
    return rel


def generar_borrador(rel: Relation, conceptos: dict) -> Relation:
    """Diferido/priorizado: borrador con modelo (P2). Stub por ahora."""
    # Se implementara cuando haya presupuesto de revision humana.
    return rel


def enriquecer_relaciones(relaciones: List[Relation],
                          wikilinks_info: List[dict]) -> List[Relation]:
    """Enriquece cada relacion con tipo y explicacion quoted.

    wikilinks_info: lista de dicts con keys: source_uid, target_uid, oracion, seccion.
    """
    # Indexar info de wikilinks por par (source, target)
    info_index: Dict[Tuple[str, str], dict] = {}
    for info in wikilinks_info:
        clave = (info.get("source_uid", ""), info.get("target_uid", ""))
        if clave not in info_index:
            info_index[clave] = info

    for rel in relaciones:
        clave = (rel.source_uid, rel.target_uid)
        info = info_index.get(clave, {})
        oracion = info.get("oracion", "")
        seccion = info.get("seccion", "")
        asignar_tipo(rel, oracion)
        extraer_quoted(rel, oracion, seccion)

    return relaciones


# Excepciones
class RelationError(AbortStage):
    pass


class ReviewNotFoundError(RelationError):
    pass
