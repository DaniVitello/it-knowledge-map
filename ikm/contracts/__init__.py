# -*- coding: utf-8 -*-
"""Contratos de IT Knowledge Map v2 (capa L0).

Fuente unica de verdad para los esquemas de datos del release y del servicio.
Los esquemas Pydantic generan JSON Schema y los tipos TypeScript (L0.4);
ninguna capa posterior redefine identificadores ni hashes.
"""

__all__ = [
    "SCHEMA_VERSION",
    "ENTITY_PREFIXES",
    "SCHEMA_GENERATION_VERSION",
]

SCHEMA_VERSION = "2.0.0"
ENTITY_PREFIXES = {
    "concept": "c_",
    "area": "a_",
    "relation": "r_",
    "journey": "j_",
    "evidence": "e_",
    "source": "s_",
    "tour": "t_",
}
SCHEMA_GENERATION_VERSION = 1
