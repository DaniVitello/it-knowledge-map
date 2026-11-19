# -*- coding: utf-8 -*-
"""Orquestador del plano de contenido (L1, capa 9).

Encadena etapas C0-C9, reanuda desde checkpoint, reintenta con backoff.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ikm.contracts.config import Config
from ikm.contracts.errors import AbortStage
from ikm.content.pipeline import ContentRunner, ejecutar_etapa

MAX_REINTENTOS = 3
BACKOFF_SECONDS = [2, 4, 8]


class RunnerError(Exception):
    pass


class ConceptRunner:
    """Orquesta las etapas de contenido para un vault completo."""

    def __init__(self, workdir: Path, config: Config, vault_root: str):
        self.workdir = Path(workdir)
        self.config = config
        self.vault_root = vault_root
        self.runner = ContentRunner(workdir, config, vault_root)

    def ejecutar_etapa_con_reintento(self, nombre: str, entrada: Any,
                                     ejecutar: Callable, validador: Callable,
                                     cache: Optional[dict] = None) -> Any:
        """Ejecuta una etapa con reintentos y backoff."""
        last_error = None
        for intento in range(1, MAX_REINTENTOS + 1):
            try:
                return ejecutar_etapa(nombre, entrada, self.config, self.workdir,
                                      ejecutar, validador, cache or self.runner.cache)
            except AbortStage as e:
                last_error = e
                if intento < MAX_REINTENTOS:
                    time.sleep(BACKOFF_SECONDS[intento - 1])
                else:
                    raise
        raise last_error

    def estado(self) -> Dict[str, Any]:
        """Devuelve el estado actual del runner (etapas completadas)."""
        return {
            "etapas_completadas": self.runner.etapas_completadas(),
            "workdir": str(self.workdir),
        }

    def reanudar(self) -> List[str]:
        """Devuelve las etapas que faltan por ejecutar."""
        completadas = set(self.runner.etapas_completadas())
        todas = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
        return [e for e in todas if e not in completadas]
