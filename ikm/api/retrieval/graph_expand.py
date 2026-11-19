# -*- coding: utf-8 -*-
"""Expansion por grafo (L3, capa 16)."""
from __future__ import annotations

from typing import Any, List


def expandir_por_grafo(entidades: List[str], relaciones: List[Any],
                      chunks: List[Any]) -> List[Dict[str, Any]]:
    """Para dos entidades: caminos de hasta 3 saltos + explicaciones de relaciones.
    Para una entidad: chunk objetivo de sus vecinos de mayor grado.

    Devuelve lista de chunks/explicaciones relevantes.
    """
    resultado: List[Dict[str, Any]] = []

    # Construir adjacency
    adjacency: dict[str, set[str]] = {}
    rel_map: dict[tuple[str, str], Any] = {}
    for r in relaciones:
        su = getattr(r, "source_uid", None) or (r.get("source_uid") if isinstance(r, dict) else None)
        tu = getattr(r, "target_uid", None) or (r.get("target_uid") if isinstance(r, dict) else None)
        if not su or not tu:
            continue
        adjacency.setdefault(su, set()).add(tu)
        adjacency.setdefault(tu, set()).add(su)
        rel_map[(su, tu)] = r
        rel_map[(tu, su)] = r

    if len(entidades) >= 2:
        # Caminos de hasta 3 saltos entre entidades
        from collections import deque
        src, dst = entidades[0], entidades[1]
        # BFS para encontrar caminos cortos
        queue = deque([(src, [src])])
        visited = {src}
        paths_found = []
        while queue and len(paths_found) < 5:
            node, path = queue.popleft()
            if node == dst and len(path) > 1:
                paths_found.append(path)
                continue
            if len(path) >= 4:  # max 3 saltos
                continue
            for neighbor in adjacency.get(node, set()):
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))
        # Recoger explicaciones de las relaciones en los caminos
        for path in paths_found:
            for i in range(len(path) - 1):
                rel = rel_map.get((path[i], path[i + 1]))
                if rel:
                    exp = getattr(rel, "explanation", None)
                    texto = ""
                    if exp:
                        texto = getattr(exp, "text", None) or (exp.get("text") if isinstance(exp, dict) else "")
                    resultado.append({
                        "type": "relation",
                        "source_uid": path[i],
                        "target_uid": path[i + 1],
                        "explanation": texto,
                        "hop": i + 1,
                    })
    elif len(entidades) == 1:
        # Vecinos de mayor grado
        uid = entidades[0]
        neighbors = sorted(adjacency.get(uid, set()), key=lambda n: len(adjacency.get(n, set())), reverse=True)
        for nb in neighbors[:5]:
            rel = rel_map.get((uid, nb))
            if rel:
                exp = getattr(rel, "explanation", None)
                texto = ""
                if exp:
                    texto = getattr(exp, "text", None) or (exp.get("text") if isinstance(exp, dict) else "")
                resultado.append({
                    "type": "relation",
                    "source_uid": uid,
                    "target_uid": nb,
                    "explanation": texto,
                })

    # Agregar chunks de los conceptos involucrados
    involved_uids = set(entidades)
    for r in relaciones:
        su = getattr(r, "source_uid", None) or (r.get("source_uid") if isinstance(r, dict) else None)
        tu = getattr(r, "target_uid", None) or (r.get("target_uid") if isinstance(r, dict) else None)
        if su in involved_uids or tu in involved_uids:
            involved_uids.add(su)
            involved_uids.add(tu)

    for ch in chunks:
        uid = getattr(ch, "entity_uid", None) or (ch.get("entity_uid") if isinstance(ch, dict) else None)
        if uid in involved_uids:
            resultado.append({
                "type": "chunk",
                "chunk": ch,
            })

    return resultado
