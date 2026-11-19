# -*- coding: utf-8 -*-
"""Generacion de contratos: Pydantic -> JSON Schema -> tipos TypeScript (L0.4).

Una sola definicion (los modelos) produce los tres artefactos. CI verifica que
los tipos TS generados esten actualizados (disenio 20.2 paso 3).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Type

from pydantic import BaseModel

from . import SCHEMA_GENERATION_VERSION, SCHEMA_VERSION
from .utils import escritura_atomica, escribir_json_atomico

# --- registro de modelos ------------------------------------------------------

_RELEASE = (
    "Area", "Source", "Concept", "ConceptSections", "VerificationMark", "Relation",
    "RelationType", "TypeBasis", "ExplanationStatus", "Explanation", "JourneyRecord",
    "JourneyKind", "PeriodBasis", "Period", "Publication", "Evidence", "EvidenceKind",
    "EvidenceVariant", "EvidenceReview", "Tour", "TourTargetType", "TourStep",
    "ExplorationState", "ViewType", "Origin", "Camera",
)
_SERVICE = (
    "User", "UserStatus", "Session", "UsageWindow", "WindowKind", "GlobalUsage",
    "Conversation", "Message", "MessageRole", "AbuseEvent", "AbuseKind", "IpWindow",
)


def _importar() -> Dict[str, Any]:
    from . import release as rel
    from . import service as svc

    mod: Dict[str, Any] = {}
    for n in _RELEASE:
        mod[n] = getattr(rel, n)
    for n in _SERVICE:
        mod[n] = getattr(svc, n)
    return mod


def _es_enum(nombre: str, mod: Dict[str, Any]) -> bool:
    import enum

    obj = mod.get(nombre)
    return isinstance(obj, type) and issubclass(obj, enum.Enum)


def _es_modelo(nombre: str, mod: Dict[str, Any]) -> bool:
    obj = mod.get(nombre)
    return isinstance(obj, type) and issubclass(obj, BaseModel)


def _modelos_por_nombre() -> Dict[str, Type[BaseModel]]:
    mod = _importar()
    return {n: mod[n] for n in _RELEASE + _SERVICE if _es_modelo(n, mod)}


def _schema_con_nombre(modelo: Type[BaseModel], modelos: Dict[str, Type[BaseModel]]) -> Dict[str, Any]:
    """JSON Schema con definitions locales y $ref por nombre."""
    bruto = modelo.model_json_schema(ref_template="#/$defs/{model}")
    defs = bruto.pop("$defs", {})
    texto = json.dumps(bruto, ensure_ascii=False).replace("#/$defs/", "#/definitions/")
    bruto = json.loads(texto)
    for nombre in sorted(defs):
        defs[nombre] = json.loads(
            json.dumps(defs[nombre], ensure_ascii=False).replace("#/$defs/", "#/definitions/")
        )
    if defs:
        bruto["definitions"] = defs
    return bruto


def generar_json_schemas(dest_dir: str) -> List[str]:
    """Escribe schemas/<modelo>.json para cada modelo. Devuelve rutas."""
    from .utils import sha256_text

    modelos = _modelos_por_nombre()
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    escritos: List[str] = []
    for kind, nombres in (("release", _RELEASE), ("service", _SERVICE)):
        por_nombre = {n: modelos[n] for n in nombres if n in modelos}
        for n in nombres:
            if n not in modelos:
                continue
            schema = _schema_con_nombre(modelos[n], por_nombre)
            schema["title"] = n
            schema["x-entity-kind"] = kind
            ruta = dest / f"{n}.json"
            escribir_json_atomico(ruta, schema)
            escritos.append(str(ruta))
    manifiesto = {
        "schema_version": SCHEMA_VERSION,
        "generation_version": SCHEMA_GENERATION_VERSION,
        "hash": sha256_text(
            "\n".join(sha256_text(Path(p).read_text(encoding="utf-8")) for p in escritos)
        ),
        "archivos": [Path(p).name for p in escritos],
    }
    escribir_json_atomico(dest / "_manifest.json", manifiesto)
    return escritos


# --- TypeScript ---------------------------------------------------------------

_TS_SCALARS = {
    "string": "string",
    "integer": "number",
    "number": "number",
    "boolean": "boolean",
    "object": "Record<string, unknown>",
    "array": "unknown[]",
    "null": "null",
}


def _ident(nombre: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", nombre) or "Anonymous"


def _ts_type(nodo: Dict[str, Any], mod: Dict[str, Any], modelos: Dict[str, Type[BaseModel]]) -> str:
    if "$ref" in nodo:
        nombre = nodo["$ref"].rsplit("/", 1)[-1]
        if _es_enum(nombre, mod):
            return _ident(nombre)
        if _es_modelo(nombre, mod):
            return _ident(nombre)
        return "unknown"
    if "anyOf" in nodo:
        ramas = [_ts_type(p, mod, modelos) for p in nodo["anyOf"]]
        no_nulas = [t for t in ramas if t != "null"]
        base = " | ".join(dict.fromkeys(no_nulas)) or "unknown"
        if "null" in ramas:
            return f"({base}) | null"
        return base
    if nodo.get("type") == "array":
        return f"Array<{_ts_type(nodo.get('items', {}), mod, modelos)}>"
    if nodo.get("type") == "object":
        props = nodo.get("properties")
        if props:
            requeridos = set(nodo.get("required", []))
            campos = ", ".join(
                f"{k}{'?' if k not in requeridos else ''}: {_ts_type(v, mod, modelos)}"
                for k, v in props.items()
            )
            return "{ " + campos + " }"
        return "Record<string, unknown>"
    if "enum" in nodo:
        return " | ".join(json.dumps(v, ensure_ascii=False) for v in nodo["enum"])
    return _TS_SCALARS.get(nodo.get("type"), "unknown")


def _ts_enum(nombre: str, mod: Dict[str, Any]) -> str:
    import enum

    obj = mod[nombre]
    valores = [json.dumps(e.value, ensure_ascii=False) for e in obj]
    return f"export type {nombre} = " + " | ".join(valores) + ";"


def _ts_interface(nombre: str, schema: Dict[str, Any], mod: Dict[str, Any],
                  modelos: Dict[str, Type[BaseModel]]) -> str:
    props = schema.get("properties", {})
    requeridos = set(schema.get("required", []))
    lineas = [f"export interface {nombre} {{"]
    for campo, spec in props.items():
        opcional = "" if campo in requeridos else "?"
        lineas.append(f"  {campo}{opcional}: {_ts_type(spec, mod, modelos)};")
    lineas.append("}")
    cuerpo = "\n".join(lineas)
    # Cada archivo es un modulo: importar los tipos referenciados (DR-L10-04).
    conocidos = [
        n for n in _RELEASE + _SERVICE
        if n != nombre and (_es_enum(n, mod) or _es_modelo(n, mod))
    ]
    refs = sorted({n for n in conocidos if re.search(r"\b" + re.escape(n) + r"\b", cuerpo)})
    imports = "".join(f"import type {{ {n} }} from './{n}';\n" for n in refs)
    return imports + cuerpo


def _escribir_ts(dest_dir: str, schema_dir: str, mod: Dict[str, Any],
                 modelos: Dict[str, Type[BaseModel]]) -> List[str]:
    dest = Path(dest_dir)
    (dest / "ts").mkdir(parents=True, exist_ok=True)
    esc: List[str] = []
    cabecera = "// Generado desde contracts. No editar a mano.\n"
    for nombre in _RELEASE + _SERVICE:
        if not _es_enum(nombre, mod):
            continue
        ruta = dest / "ts" / f"{nombre}.ts"
        escritura_atomica(ruta, (cabecera + _ts_enum(nombre, mod) + "\n").encode("utf-8"))
        esc.append(str(ruta))
    for nombre in _RELEASE + _SERVICE:
        if not _es_modelo(nombre, mod):
            continue
        schema = json.loads((Path(schema_dir) / f"{nombre}.json").read_text(encoding="utf-8"))
        ruta = dest / "ts" / f"{nombre}.ts"
        escritura_atomica(ruta, (cabecera + _ts_interface(nombre, schema, mod, modelos) + "\n").encode("utf-8"))
        esc.append(str(ruta))
    indice = "\n".join(
        f"export * from './{n}';"
        for n in _RELEASE + _SERVICE
        if _es_enum(n, mod) or _es_modelo(n, mod)
    )
    escritura_atomica(dest / "ts" / "index.ts", (indice + "\n").encode("utf-8"))
    return esc


def generar_tipos_ts(dest_dir: str) -> List[str]:
    """Regenera schemas/ y los tipos TS. Idempotente: mismo input -> mismo output."""
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    mod = _importar()
    modelos = _modelos_por_nombre()
    generar_json_schemas(str(dest / "schemas"))
    return _escribir_ts(dest_dir, str(dest / "schemas"), mod, modelos)


def regenerar(dest_dir: str) -> Dict[str, Any]:
    from .utils import sha256_text

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    mod = _importar()
    modelos = _modelos_por_nombre()
    schemas = generar_json_schemas(str(dest / "schemas"))
    ts = _escribir_ts(dest_dir, str(dest / "schemas"), mod, modelos)
    return {
        "schemas": len(schemas),
        "ts": len(ts),
        "hash": sha256_text(
            "\n".join(sha256_text(Path(p).read_text(encoding="utf-8")) for p in schemas + ts)
        ),
    }
