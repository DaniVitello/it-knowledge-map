# -*- coding: utf-8 -*-
"""Reglas comunes a TODO el pipeline de contenido (L1.0).

1. Solo lectura sobre el vault: hash del arbol antes y despues; si cambia, aborta.
2. Idempotencia: clave_cache(entrada, version_etapa, hash_config); si no cambio, se omite.
3. Ejecucion: salida validada contra el esquema de la etapa.
4. Solo lectura verificada: compara el hash del vault.
5. Determinismo: ordenamiento estable, semillas fijas, sin marcas de tiempo.
6. Guardado atomico + registro en run.json.
Una etapa que falla conserva las salidas de las anteriores.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ikm.contracts.config import Config
from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import clave_cache, escribir_json_atomico, hash_arbol_vault, sha256_text

from .schemas import RunLog, RunRecord

ETAPA_VERSION = {"C0": 1, "C1": 1}


class Etapa:
    """Resultado de una etapa de contenido: salida validada + registro."""

    def __init__(self, nombre: str, salida: Any, hash_entrada: str, duracion_s: float,
                 cache_hit: bool = False, warnings: Optional[List[str]] = None,
                 errores: Optional[List[str]] = None) -> None:
        self.nombre = nombre
        self.salida = salida
        self.hash_entrada = hash_entrada
        self.duracion_s = duracion_s
        self.cache_hit = cache_hit
        self.warnings = warnings or []
        self.errores = errores or []

    def a_registro(self) -> RunRecord:
        return RunRecord(
            etapa=self.nombre,
            version=ETAPA_VERSION.get(self.nombre, 1),
            hash_entrada=self.hash_entrada,
            hash_salida=sha256_text(str(self.salida)),
            duracion_s=round(self.duracion_s, 3),
            cache_hit=self.cache_hit,
            warnings=self.warnings,
            errores=self.errores,
        )


def ejecutar_etapa(nombre: str, entrada: Any, config: Config, workdir: Path,
                   ejecutar: Callable[[], Any], validador: Callable[[Any], Any],
                   cache: Optional[Dict[str, Any]] = None) -> Etapa:
    """Ejecuta una etapa con las reglas comunes. Conserva salidas previas si falla."""
    vault_root = getattr(config, "_vault_root", None)
    hash_vault_antes = hash_arbol_vault(vault_root) if vault_root else None

    cfg_hash = config.hash_config()
    clave = clave_cache(entrada, ETAPA_VERSION.get(nombre, 1), cfg_hash)
    if cache is not None and clave in cache:
        return Etapa(nombre, cache[clave], clave, 0.0, cache_hit=True)

    t0 = time.perf_counter()
    salida = ejecutar()
    salida = validador(salida)
    duracion = time.perf_counter() - t0

    if vault_root is not None:
        if hash_arbol_vault(vault_root) != hash_vault_antes:
            raise AbortStage("vault_modified", etapa=nombre,
                             detalle={"hash_antes": hash_vault_antes})

    if cache is not None:
        cache[clave] = salida
    return Etapa(nombre, salida, clave, duracion)


class ContentRunner:
    """Orquesta etapas de contenido con workdir, run.json y reanudacion."""

    def __init__(self, workdir: Path, config: Config, vault_root: str) -> None:
        self.workdir = Path(workdir)
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.config = config
        self.config._vault_root = vault_root
        self.cache: Dict[str, Any] = {}
        self.runlog = RunLog()
        self._cargar_runlog()

    def _runlog_path(self) -> Path:
        return self.workdir / "run.json"

    def _cargar_runlog(self) -> None:
        p = self._runlog_path()
        if p.exists():
            try:
                self.runlog = RunLog.model_validate_json(p.read_text(encoding="utf-8"))
            except Exception:
                self.runlog = RunLog()

    def guardar_runlog(self) -> None:
        escribir_json_atomico(self._runlog_path(), self.runlog.model_dump())

    def guardar_salida(self, nombre: str, salida: Any) -> Path:
        """Guarda la salida de una etapa de forma atomica (determinista)."""
        if hasattr(salida, "model_dump"):
            datos = salida.model_dump()
        elif isinstance(salida, list):
            datos = [x.model_dump() if hasattr(x, "model_dump") else x for x in salida]
        else:
            datos = salida
        ruta = self.workdir / f"{nombre}.json"
        escribir_json_atomico(ruta, datos)
        return ruta

    def registrar(self, etapa: Etapa) -> None:
        self.runlog.etapas.append(etapa.a_registro())
        self.guardar_runlog()

    def etapas_completadas(self) -> List[str]:
        return [e.etapa for e in self.runlog.etapas if not e.errores]
