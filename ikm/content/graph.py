# -*- coding: utf-8 -*-
"""C3 — Grafo: resolucion de links (L1, capa 5).

Resuelve WikiLinks con las reglas de Obsidian, crea relaciones dirigidas
y calcula cross_area. No tipifica ni explica.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ikm.contracts.errors import AbortStage
from ikm.contracts.ids import uid_relacion
from ikm.contracts.release import Relation

# Mapeo de area (nombre de carpeta) a uid de area. Se asigna en tiempo de build.
AREA_NAME_TO_UID: Dict[str, str] = {}


def _normalizar_nombre(s: str) -> str:
    """Normaliza para matching case-insensitive, sin numero ni extension."""
    s = s.strip()
    # quitar numero inicial "01 - "
    s = re.sub(r"^\d+\s*-\s*", "", s)
    # quitar extension
    s = re.sub(r"\.[a-zA-Z0-9]+$", "", s)
    return s.lower().strip()


def _resolver_destino(destino_textual: str, conceptos_por_nombre: Dict[str, str],
                      conceptos_por_ruta: Dict[str, str]) -> Optional[str]:
    """Resuelve un destino textual de WikiLink a un uid de concepto.

    Reglas de Obsidian:
    - Por nombre de archivo sin numero ni extension, case-insensitive.
    - Alias con barra y headings apuntan al concepto base.
    - Links dentro de bloques de codigo se ignoran (ya filtrado en C1).
    - Link a nota excluida no crea relacion.
    - Link roto: retorna None (se lista, no se dibuja).
    """
    # heading: "Nota#heading" -> concepto base
    if "#" in destino_textual:
        destino_textual = destino_textual.split("#", 1)[0]
    # alias con barra: "carpeta/nota" -> usar el ultimo segmento
    destino_textual = destino_textual.strip()
    if "/" in destino_textual or "\\" in destino_textual:
        partes = re.split(r"[/\\]", destino_textual)
        destino_textual = partes[-1]

    clave = _normalizar_nombre(destino_textual)
    return conceptos_por_nombre.get(clave)


def resolver_links(parsed_list: List[Any], conceptos: List[Any],
                   registry: Dict[str, str]) -> Tuple[List[Relation], List[str]]:
    """Resuelve WikiLinks -> relaciones dirigidas.

    Args:
        parsed_list: lista de ParsedConcept (con wikilinks).
        conceptos: lista de IdentifiedConcept (con uid).
        registry: mapeo uid -> ruta (para area).

    Returns:
        (relaciones, links_rotos): lista de Relation y lista de destinos no resueltos.
    """
    # Construir indices
    conceptos_por_nombre: Dict[str, str] = {}  # nombre normalizado -> uid
    conceptos_por_ruta: Dict[str, str] = {}    # ruta -> uid
    uid_to_area: Dict[str, str] = {}

    for ic in conceptos:
        uid = ic.uid
        pc = ic.parsed
        titulo = getattr(pc, "titulo", "") or ""
        ruta = getattr(pc, "ruta", "") or ""
        frontmatter = getattr(pc, "frontmatter", {}) or {}
        area = frontmatter.get("area", "") if isinstance(frontmatter, dict) else ""
        uid_to_area[uid] = area

        # nombre normalizado del titulo
        conceptos_por_nombre[_normalizar_nombre(titulo)] = uid
        # nombre del archivo (sin numero/extension)
        if ruta:
            nombre_archivo = Path(ruta).stem
            conceptos_por_nombre.setdefault(_normalizar_nombre(nombre_archivo), uid)
            conceptos_por_ruta[ruta] = uid

    relaciones: List[Relation] = []
    pares_vistos: set[Tuple[str, str]] = set()
    links_rotos: List[str] = []

    for ic in conceptos:
        source_uid = ic.uid
        pc = ic.parsed
        wikilinks = getattr(pc, "wikilinks", []) or []
        for wl in wikilinks:
            destino = getattr(wl, "destino_textual", "") if hasattr(wl, "destino_textual") else (wl.get("destino_textual", "") if isinstance(wl, dict) else "")
            target_uid = _resolver_destino(destino, conceptos_por_nombre, conceptos_por_ruta)
            if target_uid is None:
                links_rotos.append(destino)
                continue
            if target_uid == source_uid:
                continue  # self-link, ignorar
            par = (source_uid, target_uid)
            if par in pares_vistos:
                continue
            pares_vistos.add(par)
            cross = uid_to_area.get(source_uid, "") != uid_to_area.get(target_uid, "")
            rel = Relation(
                uid=uid_relacion(source_uid, target_uid),
                source_uid=source_uid,
                target_uid=target_uid,
                type="untyped",
                type_basis="none",
                cross_area=cross,
            )
            relaciones.append(rel)

    return relaciones, links_rotos


def calcular_cross_area(rel: Relation, uid_to_area: Dict[str, str]) -> bool:
    """True si source y target pertenecen a areas distintas."""
    return uid_to_area.get(rel.source_uid, "") != uid_to_area.get(rel.target_uid, "")


# Excepciones
class GraphError(AbortStage):
    pass


class AmbiguousLinkError(GraphError):
    pass
