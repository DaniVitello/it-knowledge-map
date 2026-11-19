# -*- coding: utf-8 -*-
"""Catalogo de areas: mapeo directorio del vault -> area del release.

El uid de area es el slug del catalogo (estable y legible). El orden sale
del prefijo numerico del directorio del vault. `color_token` es la clave
que el frontend usa para su paleta (DR-L10-01).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

# (nombre de directorio normalizado, slug/uid, nombre canonico) en orden 01-10.
_AREAS: List[tuple] = [
    ("software engineering", "software-engineering", "Software Engineering"),
    ("frontend", "frontend", "Frontend"),
    ("backend", "backend", "Backend"),
    ("database & data analytics", "database", "Database & Data Analytics"),
    ("networking & internet", "networking", "Networking & Internet"),
    ("operating systems & linux", "os-linux", "Operating Systems & Linux"),
    ("ai engineering", "ai-engineering", "AI Engineering"),
    ("ux & ui", "ux-ui", "UX & UI"),
    ("product management", "product-management", "Product Management"),
    ("project management", "project-management", "Project Management"),
]


def _normalizar_directorio(nombre: str) -> str:
    """Quit el prefijo numerico ('05 - ') y normaliza a minusculas."""
    return re.sub(r"^\d+\s*-\s*", "", nombre or "").strip().lower()


def catalogo_areas(vault_root: Any = None) -> List[Dict[str, Any]]:
    """Catalogo determinista de las 10 areas, en orden del vault.

    `vault_root` se acepta por compatibilidad de firma; el catalogo es
    fijo porque el vault tiene un directorio por area (relevamiento L1).
    """
    catalogo: List[Dict[str, Any]] = []
    for orden, (directorio, slug, nombre) in enumerate(_AREAS, start=1):
        catalogo.append({
            "uid": slug,
            "name": nombre,
            "order": orden,
            "color_token": slug,
            "directorio": directorio,
        })
    return catalogo


def area_uid_por_ruta(ruta: str, catalogo: List[Dict[str, Any]]) -> Optional[str]:
    """Devuelve el uid de area de una nota segun su directorio en el vault."""
    for parte in (ruta or "").replace("\\", "/").split("/"):
        normal = _normalizar_directorio(parte)
        for area in catalogo:
            if normal == area["directorio"]:
                return area["uid"]
    return None