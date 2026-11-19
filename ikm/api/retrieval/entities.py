# -*- coding: utf-8 -*-
"""Enlace de entidades contra titulos y alias (L3, capa 16)."""
from __future__ import annotations

import unicodedata
from typing import Any, List

from ikm.contracts.release import Concept


def _normalizar(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def enlazar_entidades(pregunta: str, conceptos: List[Any]) -> List[str]:
    """Devuelve uids de entidades detectadas (exacto o a una edicion).

    Estrategia:
    1. Normalizar pregunta y titulos.
    2. Match exacto por titulo o alias.
    3. Match por substring (titulo contenido en pregunta).
    4. Match por edicion (Levenshtein <= 2) para nombres cortos.
    """
    pregunta_n = _normalizar(pregunta)
    resultado: List[str] = []
    vistos: set[str] = set()

    for c in conceptos:
        uid = getattr(c, "uid", None) or (c.get("uid") if isinstance(c, dict) else None)
        if not uid or uid in vistos:
            continue
        title = getattr(c, "title", None) or (c.get("title") if isinstance(c, dict) else "") or ""
        aliases = getattr(c, "aliases", None) or (c.get("aliases", []) if isinstance(c, dict) else []) or []

        title_n = _normalizar(title)
        # Match exacto
        if title_n and title_n in pregunta_n:
            resultado.append(uid)
            vistos.add(uid)
            continue
        # Alias exacto
        for alias in aliases:
            if _normalizar(alias) in pregunta_n:
                resultado.append(uid)
                vistos.add(uid)
                break
        if uid in vistos:
            continue
        # Substring: titulo contenido en pregunta (para titulos multi-palabra)
        if len(title_n) >= 4 and title_n in pregunta_n:
            resultado.append(uid)
            vistos.add(uid)

    return resultado


def _levenshtein(a: str, b: str) -> int:
    """Distancia de Levenshtein simple."""
    if len(a) < len(b):
        a, b = b, a
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        cur = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            cur.append(min(prev[j + 1] + 1, cur[j] + 1, prev[j] + cost))
        prev = cur
    return prev[-1]
