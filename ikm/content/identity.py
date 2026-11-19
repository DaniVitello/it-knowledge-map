# -*- coding: utf-8 -*-
"""C2 â€” Identidad estable (L1, capa 4).

Asigna uid desde un registro externo al vault; detecta renombres.
No modifica el vault ni escribe uid en las notas.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from ikm.contracts.errors import AbortStage
from ikm.contracts.ids import nuevo_uid
from ikm.contracts.utils import sha256_text

from .schemas import IdentifiedConcept, ParsedConcept


REGISTRY_VERSION = 1


class IdentityConflictError(AbortStage):
    """Conflicto de identidad (rename ambiguo o uid duplicado)."""
    pass


def _cargar_registry(ruta: Path) -> Dict[str, Any]:
    if not ruta.exists():
        return {"version": REGISTRY_VERSION, "entries": []}
    try:
        datos = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise AbortStage("invalid_registry", etapa="C2",
                         detalle={"motivo": str(exc)}) from exc
    if not isinstance(datos, dict):
        raise AbortStage("invalid_registry", etapa="C2",
                         detalle={"motivo": "registry no es un mapa"})
    datos.setdefault("version", REGISTRY_VERSION)
    datos.setdefault("entries", [])
    return datos


def _guardar_registry(ruta: Path, datos: Dict[str, Any]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    import os as _os
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(yaml.safe_dump(datos, allow_unicode=True, sort_keys=True),
                   encoding="utf-8")
    _os.replace(tmp, ruta)


def detectar_renombre(old: Dict[str, Any], new: ParsedConcept) -> bool:
    """Misma ruta con igual hash o titulo -> mismo concepto (rename detectado)."""
    if old.get("ruta") and new.ruta and old["ruta"] == new.ruta:
        return True
    mismo_hash = old.get("content_hash") and old["content_hash"] == new.content_hash
    mismo_titulo = old.get("titulo") and old["titulo"] == new.titulo
    return bool(mismo_hash or mismo_titulo)


def asignar_uids(parsed: List[ParsedConcept], registry_path: Path) -> List[IdentifiedConcept]:
    """Lee identity-registry; asigna uid a cada concepto; detecta renombres.

    Aborta si: conflicto de renombre sin resolver; uid duplicado.
    """
    registry = _cargar_registry(registry_path)
    entries_originales = list(registry.get("entries", []))

    by_ruta: Dict[str, Dict[str, Any]] = {}
    for e in entries_originales:
        if e.get("ruta"):
            by_ruta[e["ruta"]] = e

    uids_usados: set[str] = {e.get("uid") for e in entries_originales if e.get("uid")}

    resultado: List[IdentifiedConcept] = []
    entries = list(entries_originales)
    consumidos: set[str] = set()
    nuevos_entries: List[Dict[str, Any]] = []

    for pc in parsed:
        ruta = getattr(pc, "ruta", None) or ""
        titulo = getattr(pc, "titulo", "") or ""
        content_hash = getattr(pc, "content_hash", "") or ""

        # 1. Misma ruta -> reusar uid
        if ruta and ruta in by_ruta:
            entry = by_ruta[ruta]
            uid = entry["uid"]
            # actualizar hash/titulo si cambiaron
            entry["content_hash"] = content_hash
            entry["titulo"] = titulo
            identified = IdentifiedConcept(uid=uid, parsed=pc, ruta=ruta)
            resultado.append(identified)
            continue

        # 2. Ruta nueva: buscar en entradas ORIGINALES por hash o titulo
        candidatos = []
        seen_uids = set()
        for e in entries_originales:
            if e.get("uid") in consumidos:
                continue
            match_hash = bool(content_hash and e.get("content_hash") == content_hash)
            match_titulo = bool(titulo and e.get("titulo") == titulo)
            if match_hash or match_titulo:
                if e["uid"] not in seen_uids:
                    candidatos.append(e)
                    seen_uids.add(e["uid"])

        if len(candidatos) == 1:
            entry = candidatos[0]
            uid = entry["uid"]
            # rename: actualizar ruta
            entry["ruta"] = ruta
            entry["content_hash"] = content_hash
            entry["titulo"] = titulo
            consumidos.add(uid)
            consumidos.add(uid)
            by_ruta[ruta] = entry
            identified = IdentifiedConcept(uid=uid, parsed=pc, ruta=ruta)
            resultado.append(identified)
            continue
        elif len(candidatos) > 1:
            raise IdentityConflictError(
                "rename_ambiguous", etapa="C2",
                detalle={
                    "ruta": ruta,
                    "titulo": titulo,
                    "candidatos": [c.get("uid") for c in candidatos],
                },
            )

        # 3. Sin match -> nuevo uid
        uid = nuevo_uid("concept")
        if uid in uids_usados:
            raise IdentityConflictError(
                "uid_duplicado", etapa="C2",
                detalle={"uid": uid, "ruta": ruta},
            )
        uids_usados.add(uid)
        new_entry = {
            "uid": uid,
            "ruta": ruta,
            "content_hash": content_hash,
            "titulo": titulo,
        }
        entries.append(new_entry)
        by_ruta[ruta] = new_entry
        # by_hash removed (no longer used)
        nuevos_entries.append(new_entry)
        identified = IdentifiedConcept(uid=uid, parsed=pc, ruta=ruta)
        resultado.append(identified)

    # Verificar uids duplicados en el resultado
    uids_resultado = [ic.uid for ic in resultado]
    if len(uids_resultado) != len(set(uids_resultado)):
        raise IdentityConflictError(
            "uid_duplicado", etapa="C2",
            detalle={"uids": [u for u in uids_resultado if uids_resultado.count(u) > 1]},
        )

    # Guardar registry actualizado
    registry["entries"] = entries
    _guardar_registry(registry_path, registry)

    return resultado


def asignar_uids_simple(parsed: List[ParsedConcept], registry_path: Path) -> List[IdentifiedConcept]:
    """Alias para compatibilidad con el stub original."""
    return asignar_uids(parsed, registry_path)

