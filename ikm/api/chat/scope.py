# -*- coding: utf-8 -*-
"""Clasificacion de alcance tematico (L3, capa 19)."""
from __future__ import annotations

import re
from typing import Any, Literal

# Terminos de ingenieria de software para clasificacion determinista
SE_TERMS = {
    "software", "codigo", "programacion", "algoritmo", "estructura de datos",
    "patron", "arquitectura", "api", "http", "tcp", "udp", "dns", "ip",
    "base de datos", "sql", "nosql", "frontend", "backend", "react", "vue",
    "angular", "node", "python", "javascript", "typescript", "java", "go",
    "rust", "docker", "kubernetes", "linux", "git", "ci", "cd", "testing",
    "deploy", "infraestructura", "red", "protocolo", "seguridad", "auth",
    "oauth", "jwt", "rest", "graphql", "microservicio", "monolito",
    "cache", "redis", "postgres", "mongo", "orm", "mvc", "solid", "dry",
    "kiss", "clean code", "refactoring", "debug", "profiling",
}

SMALLTALK_TERMS = {
    "hola", "hello", "hi", "buenos dias", "buenas", "gracias", "thanks",
    "adios", "chau", "bye", "como estas", "que tal",
}


def _normalizar(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def clasificar_alcance(pregunta: str, recuperacion: Any) -> Literal[
        "in_project", "in_general_se", "meta", "smalltalk", "out"]:
    """Primero determinista; en zona ambigua el modelo declara scope_verdict.

    Reglas:
    - smalltalk: saludos y cortesias.
    - out: sin coincidencias ni terminos tecnicos.
    - in_project: contiene terminos del proyecto o entidades enlazadas.
    - in_general_se: ingenieria de software sin nota especifica.
    - meta: sobre la plataforma o los recorridos.
    """
    pregunta_n = _normalizar(pregunta)

    # Smalltalk
    for term in SMALLTALK_TERMS:
        if term in pregunta_n:
            # Solo si la pregunta es corta (saludo)
            if len(pregunta_n.split()) <= 4:
                return "smalltalk"

    # Meta
    meta_terms = {"plataforma", "recorrido", "tour", "como funciona el sitio", "que es it knowledge map"}
    for term in meta_terms:
        if term in pregunta_n:
            return "meta"

    # Buscar terminos SE
    tiene_se = False
    for term in SE_TERMS:
        if term in pregunta_n:
            tiene_se = True
            break

    # Si hay recuperacion con entidades enlazadas -> in_project
    if recuperacion is not None:
        entidades = getattr(recuperacion, "entidades", None) or []
        if entidades:
            return "in_project"

    if tiene_se:
        # Si la pregunta menciona un concepto especifico del proyecto
        # (se detectaria por enlace de entidades), es in_project
        return "in_general_se"

    # Sin terminos tecnicos ni SE -> out
    return "out"
