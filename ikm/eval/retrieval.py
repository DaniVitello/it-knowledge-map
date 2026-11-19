# -*- coding: utf-8 -*-
"""Evaluacion de recuperacion: recall@8 sobre conjunto de oro (L5, capa 21)."""
from __future__ import annotations

from typing import Any, Callable, Dict, List


def medir_recall_at_8(casos: List[Dict[str, Any]],
                      recuperacion_fn: Callable[[str], List[str]]) -> Dict[str, Any]:
    """Mide recall@8 por tipo de pregunta sobre el conjunto de oro.

    casos: lista de {pregunta, chunks_esperados, tipo}
    recuperacion_fn: funcion que dado una pregunta devuelve lista de chunk_ids recuperados
    """
    resultados_por_tipo: Dict[str, List[float]] = {}
    total_recall = 0.0
    total_casos = 0

    for caso in casos:
        pregunta = caso.get("pregunta", "")
        esperados = set(caso.get("chunks_esperados", []))
        tipo = caso.get("tipo", "general")

        if not esperados:
            continue

        recuperados = recuperacion_fn(pregunta)[:8]
        recuperados_set = set(recuperados)

        hits = len(esperados & recuperados_set)
        recall = hits / len(esperados) if esperados else 0.0

        resultados_por_tipo.setdefault(tipo, []).append(recall)
        total_recall += recall
        total_casos += 1

    # Promedios por tipo
    por_tipo = {}
    for tipo, recalls in resultados_por_tipo.items():
        por_tipo[tipo] = sum(recalls) / len(recalls) if recalls else 0.0

    promedio = total_recall / total_casos if total_casos else 0.0

    return {
        "recall_at_8": promedio,
        "por_tipo": por_tipo,
        "total_casos": total_casos,
        "umbral_aprobacion": "pendiente (se fija con la primera medicion)",
    }


def evaluar_reglas_duras(casos: List[Dict[str, Any]],
                         evaluar_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    """Evalua las reglas duras (100% requerido).

    Reglas duras: fuera de tema, contenido excluido, inyeccion, destinos inexistentes,
    relaciones derived presentadas como documentadas.
    """
    resultados = {"total": 0, "passed": 0, "failed": 0, "detalles": []}
    for caso in casos:
        resultado = evaluar_fn(caso)
        resultados["total"] += 1
        if resultado.get("passed", False):
            resultados["passed"] += 1
        else:
            resultados["failed"] += 1
            resultados["detalles"].append({
                "caso": caso.get("id", "unknown"),
                "motivo": resultado.get("motivo", "unknown"),
            })
    resultados["tasa_exito"] = resultados["passed"] / resultados["total"] if resultados["total"] else 0.0
    resultados["cumple_100"] = resultados["failed"] == 0
    return resultados
