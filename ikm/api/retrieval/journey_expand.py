# -*- coding: utf-8 -*-
"""Expansion al Journey (L3, capa 16)."""
from __future__ import annotations

from typing import Any, List


def expandir_al_journey(entidades: List[str], links: dict,
                        registros: List[Any]) -> List[Dict[str, Any]]:
    """Hasta 2 chunks de registros vinculados por journey/links.json.

    Devuelve lista de dicts con claim y record_uid.
    """
    resultado: List[Dict[str, Any]] = []
    registros_por_uid: dict[str, Any] = {}
    for r in registros:
        uid = getattr(r, "uid", None) or (r.get("uid") if isinstance(r, dict) else None)
        if uid:
            registros_por_uid[uid] = r

    for uid in entidades:
        record_uids = links.get(uid, [])
        for ruid in record_uids[:2]:
            reg = registros_por_uid.get(ruid)
            if not reg:
                continue
            # Extraer campos relevantes
            titulo = getattr(reg, "title", None) or (reg.get("title") if isinstance(reg, dict) else "")
            description = getattr(reg, "description", None) or (reg.get("description") if isinstance(reg, dict) else "")
            decisions = getattr(reg, "decisions", None) or (reg.get("decisions", []) if isinstance(reg, dict) else [])
            kind = getattr(reg, "kind", None) or (reg.get("kind") if isinstance(reg, dict) else [])
            chunk_text = f"Registro: {titulo}\n"
            if description:
                chunk_text += f"Descripcion: {description}\n"
            if decisions:
                chunk_text += f"Decisiones: {', '.join(decisions)}\n"
            if kind:
                chunk_text += f"Tipo: {kind}\n"
            resultado.append({
                "type": "journey",
                "record_uid": ruid,
                "text": chunk_text.strip(),
                "kind": kind,
            })
            if len(resultado) >= 2:
                break
        if len(resultado) >= 2:
            break

    return resultado
