# -*- coding: utf-8 -*-
"""Runner de la evaluacion del chatbot (L5, capa 21)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ikm.eval.retrieval import medir_recall_at_8, evaluar_reglas_duras


class EvalError(Exception):
    pass


def cargar_casos(ruta: str) -> List[Dict[str, Any]]:
    """Carga casos de evaluacion desde un archivo YAML o JSON."""
    p = Path(ruta)
    if not p.exists():
        raise EvalError(f"archivo de casos no encontrado: {ruta}")
    texto = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        try:
            import yaml
            data = yaml.safe_load(texto)
        except Exception as exc:
            raise EvalError(f"error parseando YAML: {exc}") from exc
    else:
        data = json.loads(texto)
    if isinstance(data, dict):
        return data.get("casos", data.get("cases", []))
    if isinstance(data, list):
        return data
    return []


def ejecutar_evaluacion(casos_path: str, evaluar_fn: Optional[Callable] = None,
                        recuperacion_fn: Optional[Callable] = None,
                        modelo_real: bool = False) -> Dict[str, Any]:
    """Ejecuta los casos de eval/chat.yml; reglas duras al 100%.

    Args:
        casos_path: ruta al archivo de casos (YAML/JSON).
        evaluar_fn: funcion que evalua un caso y devuelve {passed, motivo}.
        recuperacion_fn: funcion de recuperacion para recall@8.
        modelo_real: si True, usa el modelo real (bajo demanda, con presupuesto).

    Returns:
        Dict con resultados de reglas duras y recall@8.
    """
    casos = cargar_casos(casos_path)
    if not casos:
        raise EvalError("sin casos de evaluacion")

    resultado: Dict[str, Any] = {
        "total_casos": len(casos),
        "modelo_real": modelo_real,
    }

    # Reglas duras
    if evaluar_fn:
        rd = evaluar_reglas_duras(casos, evaluar_fn)
        resultado["reglas_duras"] = rd
    else:
        resultado["reglas_duras"] = {"total": len(casos), "passed": 0, "failed": 0,
                                     "cumple_100": False, "nota": "evaluar_fn no proporcionado"}

    # Recall@8
    if recuperacion_fn:
        # Filtrar casos que tengan chunks_esperados
        casos_con_esperados = [c for c in casos if c.get("chunks_esperados")]
        if casos_con_esperados:
            recall = medir_recall_at_8(casos_con_esperados, recuperacion_fn)
            resultado["recall"] = recall
        else:
            resultado["recall"] = {"nota": "sin casos con chunks_esperados"}
    else:
        resultado["recall"] = {"nota": "recuperacion_fn no proporcionado"}

    # Resumen
    resultado["resumen"] = {
        "reglas_duras_100": resultado.get("reglas_duras", {}).get("cumple_100", False),
        "recall_at_8": resultado.get("recall", {}).get("recall_at_8", "N/A"),
    }

    return resultado


def generar_reporte_markdown(resultado: Dict[str, Any]) -> str:
    """Genera un reporte en Markdown de los resultados."""
    lines = ["# Reporte de Evaluacion\n"]
    lines.append(f"- Total de casos: {resultado.get('total_casos', 0)}")
    lines.append(f"- Modelo real: {resultado.get('modelo_real', False)}")
    rd = resultado.get("reglas_duras", {})
    lines.append(f"- Reglas duras: {rd.get('passed', 0)}/{rd.get('total', 0)} (cumple 100%: {rd.get('cumple_100', False)})")
    recall = resultado.get("recall", {})
    lines.append(f"- Recall@8: {recall.get('recall_at_8', 'N/A')}")
    if recall.get("por_tipo"):
        lines.append("\n## Recall por tipo\n")
        for tipo, val in recall["por_tipo"].items():
            lines.append(f"- {tipo}: {val:.3f}")
    if rd.get("detalles"):
        lines.append("\n## Fallos en reglas duras\n")
        for d in rd["detalles"]:
            lines.append(f"- {d.get('caso', '?')}: {d.get('motivo', '?')}")
    return "\n".join(lines)
