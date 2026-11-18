# -*- coding: utf-8 -*-
"""Identificadores estables (L0.1).

Un uid se asigna UNA sola vez y no cambia. El registro externo (C2) es quien
lo mantiene; este modulo solo define el formato y las funciones derivadas.
"""
from __future__ import annotations

import base64
import hashlib
import re
import secrets
import unicodedata

from . import ENTITY_PREFIXES

_UID_RE = re.compile(
    r"^(" + "|".join(re.escape(p) for p in ENTITY_PREFIXES.values()) + r")[0-9A-Z]{10}$"
)
_REL_RE = re.compile(r"^r_[0-9a-f]{64}$")


def nuevo_uid(tipo: str) -> str:
    """Prefijo por tipo + 10 chars base32 (RFC4648, sin relleno)."""
    prefijo = ENTITY_PREFIXES.get(tipo)
    if prefijo is None:
        raise ValueError(f"tipo de entidad desconocido: {tipo!r}")
    raw = secrets.token_bytes(8)
    cuerpo = base64.b32encode(raw).decode("ascii").rstrip("=")[:10]
    return prefijo + cuerpo


def es_uid_valido(uid: str) -> bool:
    return bool(_UID_RE.match(uid or ""))


def uid_relacion(source_uid: str, target_uid: str) -> str:
    """uid de relacion = hash(source|target). Dirigida: (A,B) != (B,A)."""
    clave = f"{source_uid}|{target_uid}".encode("utf-8")
    return "r_" + hashlib.sha256(clave).hexdigest()


def es_uid_relacion_valido(uid: str) -> bool:
    return bool(_REL_RE.match(uid or ""))


def slugify(titulo: str) -> str:
    """Slug cosmetico para URLs (no identidad)."""
    t = unicodedata.normalize("NFKD", titulo or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "sin-slug"
