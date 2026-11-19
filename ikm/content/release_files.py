# -*- coding: utf-8 -*-
"""Armado de los archivos del release (C9, capa 11).

Funciones puras que construyen los payloads JSON del release estatico:
release.json (bootstrap), areas.json, graph.json y la ficha de cada
concepto. El release es autocontenido: el frontend y el backend consumen
exactamente estos archivos (diseno v3, seccion 15.2).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from ikm.contracts.ids import slugify, uid_relacion
from ikm.content.areas_catalog import area_uid_por_ruta

SECCIONES_CONTRATO = [
    "objetivo", "ideas_clave", "como_funciona", "detalles",
    "ejemplo_minimo", "errores_comunes", "estado_actual",
    "conexiones", "ruta_estudio", "preguntas_repaso",
]


def serializar_json(obj: Any) -> bytes:
    """Serializacion canonica del release (misma forma que escribir_json_atomico)."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")


def _areas_yaml(areas_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Lee el framing de cada area desde ikm/areas/<slug>.yaml (best-effort)."""
    out: Dict[str, Dict[str, Any]] = {}
    if not areas_dir.exists():
        return out
    for p in sorted(areas_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            continue
        out[p.stem] = data
    return out


def construir_areas_json(catalogo: List[Dict[str, Any]],
                         conceptos_release: List[Dict[str, Any]],
                         areas_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """areas.json: contrato Area + conteo + framing profesional."""
    conteo: Dict[str, int] = {}
    for c in conceptos_release:
        a = c.get("area_uid")
        if a:
            conteo[a] = conteo.get(a, 0) + 1
    framing = _areas_yaml(areas_dir) if areas_dir is not None else {}
    out = []
    for a in catalogo:
        yaml_area = framing.get(a["uid"], {})
        out.append({
            "uid": a["uid"],
            "name": a["name"],
            "order": a["order"],
            "color_token": a["color_token"],
            "count": conteo.get(a["uid"], 0),
            "context_framing": yaml_area.get("context_framing"),
            "professional_roles": yaml_area.get("professional_roles") or [],
        })
    return out


def construir_ficha(ic: Any, catalogo: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Ficha publicable de un concepto (concepts/<uid>.json).

    Campos del contrato Concept + meta de navegacion (numero, tags,
    sections_missing, related_uids). Las marcas de verificacion se
    conservan SIEMPRE: son senales de integridad, no ruido.
    """
    parsed = ic.parsed
    fm = parsed.frontmatter if isinstance(parsed.frontmatter, dict) else {}
    area_uid = area_uid_por_ruta(ic.ruta or parsed.ruta, catalogo)
    secciones = parsed.sections.model_dump() if hasattr(parsed.sections, "model_dump") else dict(parsed.sections or {})
    marcas = [
        {"section": m.section, "kind": m.kind}
        for m in (parsed.marks or [])
    ]
    fuentes = parsed.sources or []
    return {
        "uid": ic.uid,
        "title": parsed.titulo,
        "slug": slugify(parsed.titulo),
        "area_uid": area_uid,
        "aliases": fm.get("aliases") or [],
        "tags": fm.get("tags") or [],
        "numero": fm.get("numero"),
        "sections": {s: secciones.get(s) for s in SECCIONES_CONTRATO},
        "sections_missing": list(parsed.sections_missing or []),
        "verification_marks": marcas,
        "sources": [f.url if hasattr(f, "url") else str(f) for f in fuentes],
        "sources_detail": [
            {"url": f.url, "title": getattr(f, "title", None)}
            for f in fuentes if hasattr(f, "url")
        ],
        "content_hash": parsed.content_hash,
    }


def agregar_vecinos(fichas: Dict[str, Dict[str, Any]],
                    relaciones: List[Any]) -> None:
    """Agrega related_uids a cada ficha (ambas direcciones, orden estable)."""
    vecinos: Dict[str, set] = {uid: set() for uid in fichas}
    for r in relaciones:
        su = r.source_uid if hasattr(r, "source_uid") else r.get("source_uid")
        tu = r.target_uid if hasattr(r, "target_uid") else r.get("target_uid")
        if su in vecinos and tu in vecinos and su != tu:
            vecinos[su].add(tu)
            vecinos[tu].add(su)
    for uid, ficha in fichas.items():
        ficha["related_uids"] = sorted(vecinos.get(uid, set()))


def construir_graph_json(posiciones: Dict[str, Any],
                         relaciones: List[Any]) -> Dict[str, Any]:
    """graph.json: nodos con posicion + aristas con uid de relacion.

    Las aristas carry el uid para abrir la explicacion quoted en <300 ms
    sin recomputar identidad (criterio 15.3).
    """
    por_par: Dict[tuple, Any] = {}
    for r in relaciones:
        su = r.source_uid if hasattr(r, "source_uid") else r.get("source_uid")
        tu = r.target_uid if hasattr(r, "target_uid") else r.get("target_uid")
        por_par[(su, tu)] = r
    aristas = []
    for e in posiciones.get("edges", []):
        su, tu = e["source"], e["target"]
        r = por_par.get((su, tu))
        if r is not None:
            uid = r.uid if hasattr(r, "uid") else r.get("uid")
            tipo = r.type.value if hasattr(r.type, "value") else (r.get("type") or "untyped")
            cross = bool(r.cross_area if hasattr(r, "cross_area") else r.get("cross_area"))
            expl = r.explanation if hasattr(r, "explanation") else r.get("explanation")
            tiene = bool(expl and (expl.text if hasattr(expl, "text") else expl.get("text")))
        else:
            uid = uid_relacion(su, tu)
            tipo, cross, tiene = "untyped", False, False
        aristas.append({
            "uid": uid, "source": su, "target": tu,
            "type": tipo, "cross_area": cross, "has_explanation": tiene,
        })
    aristas.sort(key=lambda a: a["uid"])
    nodos = sorted(posiciones.get("nodes", []), key=lambda n: n["uid"])
    return {"nodes": nodos, "edges": aristas}


def construir_release_json(conceptos_release: List[Dict[str, Any]],
                           areas_json: List[Dict[str, Any]],
                           conteos: Dict[str, int]) -> Dict[str, Any]:
    """release.json: bootstrap del frontend (indice liviano de conceptos).

    No incluye release_id: vive en manifest.json y en el nombre del
    directorio (evita referencia circular con el hash de contenido).
    """
    indice = []
    for c in sorted(conceptos_release, key=lambda x: (x.get("area_uid") or "", x.get("numero") or 0, x["uid"])):
        indice.append({
            "uid": c["uid"],
            "title": c["title"],
            "slug": c["slug"],
            "area_uid": c.get("area_uid"),
            "numero": c.get("numero"),
            "marks_count": c.get("marks_count", 0),
            "sections_missing": c.get("sections_missing") or [],
        })
    return {
        "schema_version": 1,
        "counts": conteos,
        "areas": [
            {"uid": a["uid"], "name": a["name"], "order": a["order"], "count": a["count"]}
            for a in areas_json
        ],
        "concepts": indice,
    }