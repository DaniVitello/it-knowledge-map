# -*- coding: utf-8 -*-
"""C8 — Derivados (L1, capa 10).

Chunks, indice BM25, indice de busqueda del cliente, posiciones del grafo.
No llama a modelos. Todo determinista (orden estable, sin fechas).
"""
from __future__ import annotations

import hashlib
import math
import re
from typing import Any, Dict, List

from ikm.contracts.errors import AbortStage
from ikm.contracts.ids import uid_relacion

SECCIONES_CONTRATO = [
    "objetivo", "ideas_clave", "como_funciona", "detalles",
    "ejemplo_minimo", "errores_comunes", "estado_actual",
    "conexiones", "ruta_estudio", "preguntas_repaso",
]

TOKENS_POR_CHUNK = 400
SOLAPAMIENTO = 50

# Layout del grafo (DR-L10-02): phyllotaxis por area, centros en circulo.
RADIO_CENTROS = 560.0
PASO_PHYLLOTAXIS = 26.0
ANGULO_AUREO = math.pi * (3.0 - math.sqrt(5.0))


def _tokenizar(texto: str) -> List[str]:
    return re.findall(r"\w+", (texto or "").lower())


def _dividir_en_chunks(texto: str, max_tokens: int = TOKENS_POR_CHUNK,
                       solapamiento: int = SOLAPAMIENTO) -> List[str]:
    """Divide texto en chunks de ~max_tokens tokens con solapamiento."""
    tokens = _tokenizar(texto)
    if not tokens:
        return []
    chunks = []
    paso = max(1, max_tokens - solapamiento)
    i = 0
    while i < len(tokens):
        bloque = tokens[i:i + max_tokens]
        chunks.append(" ".join(bloque))
        i += paso
        if i >= len(tokens):
            break
    return chunks


def generar_chunks(conceptos: List[Any]) -> List[Dict[str, Any]]:
    """Un chunk por seccion del contrato; secciones largas se dividen.

    Formato chunk_id: {uid}#{seccion}#{n}. preguntas_repaso queda fuera
    del corpus (pregunta, no explica).
    """
    chunks: List[Dict[str, Any]] = []
    for c in conceptos:
        uid = getattr(c, "uid", None) or (c.get("uid") if isinstance(c, dict) else None)
        if not uid:
            continue
        titulo = getattr(c, "title", None) or (c.get("title") if isinstance(c, dict) else "")
        area_uid = getattr(c, "area_uid", None) or (c.get("area_uid") if isinstance(c, dict) else None)
        sections = getattr(c, "sections", None) or (c.get("sections") if isinstance(c, dict) else {}) or {}
        if not isinstance(sections, dict):
            sections = {}

        for seccion in SECCIONES_CONTRATO:
            texto = sections.get(seccion)
            if not texto:
                continue
            if seccion == "preguntas_repaso":
                continue
            texto = str(texto).strip()
            if not texto:
                continue
            sub_chunks = _dividir_en_chunks(texto)
            if not sub_chunks:
                sub_chunks = [texto]
            for idx, sub in enumerate(sub_chunks):
                chunk_id = f"{uid}#{seccion}#{idx}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "entity_uid": uid,
                    "entity_type": "concept",
                    "source_class": "A",
                    "area_uid": area_uid,
                    "section": seccion,
                    "text": f"Concepto: {titulo} | Area: {area_uid or ''} | Seccion: {seccion}\n{sub}",
                    "flags": [],
                    "content_hash": hashlib.sha256(sub.encode("utf-8")).hexdigest(),
                })
    return chunks


def generar_indice_bm25(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Indice lexical BM25 sobre los chunks: doc_count, avg_dl, idf, postings."""
    doc_tokens: List[List[str]] = []
    for ch in chunks:
        doc_tokens.append(_tokenizar(ch.get("text", "")))

    n = len(doc_tokens)
    if n == 0:
        return {"doc_count": 0, "avg_dl": 0, "idf": {}, "postings": {}}

    df: Dict[str, int] = {}
    for toks in doc_tokens:
        for t in set(toks):
            df[t] = df.get(t, 0) + 1

    idf: Dict[str, float] = {}
    for t, d in df.items():
        idf[t] = math.log((n - d + 0.5) / (d + 0.5) + 1)

    postings: Dict[str, List[List[int]]] = {}
    for i, toks in enumerate(doc_tokens):
        tf_map: Dict[str, int] = {}
        for t in toks:
            tf_map[t] = tf_map.get(t, 0) + 1
        for t, tf in tf_map.items():
            postings.setdefault(t, []).append([i, tf])

    avg_dl = sum(len(t) for t in doc_tokens) / n if n else 0
    chunk_ids = [ch["chunk_id"] for ch in chunks]
    return {
        "doc_count": n,
        "avg_dl": avg_dl,
        "idf": idf,
        "postings": postings,
        "chunk_ids": chunk_ids,
    }


def generar_indice_cliente(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Indice de busqueda del cliente: {chunk_id, entity_uid, text truncado}."""
    out = []
    for ch in chunks:
        out.append({
            "chunk_id": ch["chunk_id"],
            "entity_uid": ch["entity_uid"],
            "area_uid": ch.get("area_uid"),
            "section": ch.get("section"),
            "text": ch.get("text", "")[:200],
        })
    return {"chunks": out, "total": len(out)}


def calcular_posiciones_grafo(relaciones: List[Any], conceptos: List[Any]) -> Dict[str, Any]:
    """Posiciones precalculadas del grafo (layout determinista, legible).

    Cada area es un cluster phyllotaxis (angulo aureo, radio ~ sqrt(i))
    centrado en un circulo mayor. Sin semillas ni timestamps: el mismo
    input produce exactamente las mismas coordenadas.
    """
    def _campo(obj: Any, nombre: str, default: Any = None) -> Any:
        return getattr(obj, nombre, None) or (obj.get(nombre) if isinstance(obj, dict) else None) or default

    por_area: Dict[str, List[Dict[str, Any]]] = {}
    for c in conceptos:
        uid = _campo(c, "uid")
        if not uid:
            continue
        area = _campo(c, "area_uid") or "sin-area"
        por_area.setdefault(area, []).append(c)

    areas_orden = sorted(por_area.keys())
    num_areas = max(len(areas_orden), 1)
    positions: Dict[str, Dict[str, float]] = {}
    for ai, area in enumerate(areas_orden):
        angulo_area = (2 * math.pi * ai) / num_areas
        cx = RADIO_CENTROS * math.cos(angulo_area)
        cy = RADIO_CENTROS * math.sin(angulo_area)
        uids = sorted((_campo(c, "uid") for c in por_area[area]))
        for i, uid in enumerate(uids):
            r = PASO_PHYLLOTAXIS * math.sqrt(i + 0.5)
            theta = i * ANGULO_AUREO
            positions[uid] = {
                "x": round(cx + r * math.cos(theta), 2),
                "y": round(cy + r * math.sin(theta), 2),
            }

    grado: Dict[str, int] = {}
    for r in relaciones:
        su = _campo(r, "source_uid")
        tu = _campo(r, "target_uid")
        if su:
            grado[su] = grado.get(su, 0) + 1
        if tu:
            grado[tu] = grado.get(tu, 0) + 1

    nodos = []
    for c in conceptos:
        uid = _campo(c, "uid")
        if not uid:
            continue
        pos = positions.get(uid, {"x": 0.0, "y": 0.0})
        nodos.append({
            "uid": uid,
            "title": _campo(c, "title", ""),
            "slug": _campo(c, "slug", ""),
            "area_uid": _campo(c, "area_uid"),
            "grado": grado.get(uid, 0),
            "x": pos["x"],
            "y": pos["y"],
        })

    pares = []
    for r in relaciones:
        su = _campo(r, "source_uid")
        tu = _campo(r, "target_uid")
        if su and tu:
            pares.append({
                "uid": _campo(r, "uid") or uid_relacion(su, tu),
                "source": su,
                "target": tu,
            })
    return {"nodes": nodos, "edges": pares}


class DerivadosError(AbortStage):
    pass