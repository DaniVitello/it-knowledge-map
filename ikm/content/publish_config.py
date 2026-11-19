# -*- coding: utf-8 -*-
"""Configuracion de publicacion (C0/C1).

`publish.config.yml` vive en el repositorio PRIVADO. Define la lista de
inclusion, la de exclusion y qué zonas de la nota se publican. Todo elemento
nace `private`; la publicacion se decide en C5/C7, no aca.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field

from ikm.contracts.errors import AbortStage

# Zonas que NUNCA se publican (decision de disenio, no configurable).
ZONAS_SIEMPRE_EXCLUIDAS = ("navegacion", "pie", "mis_notas", "frontmatter", "titulo")

# Secciones del contrato de v1 y sus variantes ortograficas reales.
SECCIONES_CONTRATO = {
    "objetivo": ("objetivo",),
    "ideas_clave": ("ideas clave", "esqueleto"),
    "como_funciona": ("como funciona", "como funciona (paso a paso)"),
    "detalles": ("detalles",),
    "ejemplo_minimo": ("ejemplo minimo", "ejemplo minimo practico"),
    "errores_comunes": ("errores comunes",),
    "estado_actual": ("estado actual",),
    "conexiones": ("conexiones",),
    "ruta_estudio": ("ruta de estudio",),
    "preguntas_repaso": ("preguntas de repaso",),
}

# Zonas publicables por defecto (configurable).
ZONAS_PUBLICABLES_DEFAULT = ("bloque_ai", "relacionados", "que_abarca")


class PublishConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vault_root: str = r"C:/Users/DGVit/Proyectos/IT Career/IT-Mind-Map"
    journey_raw_roots: List[str] = Field(default_factory=list)
    include: List[str] = Field(default_factory=lambda: ["**/*.md"])
    exclude: List[str] = Field(default_factory=lambda: [
        "**/00 - *ndice*.md", "**/.obsidian/**", "**/.trash/**",
    ])
    publishable_zones: List[str] = Field(default_factory=lambda: list(ZONAS_PUBLICABLES_DEFAULT))
    secciones_contrato: List[str] = Field(default_factory=lambda: list(SECCIONES_CONTRATO.keys()))
    marcadores: List[str] = Field(default_factory=lambda: ["sin verificar", "verificar"])
    scan_patterns: List[str] = Field(default_factory=lambda: [
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"AKIA[0-9A-Z]{16}",
        r"sk-[A-Za-z0-9]{20,}",
        r"ghp_[A-Za-z0-9]{36}",
        r"AIza[0-9A-Za-z_\-]{35}",
    ])

    def zona_es_publicable(self, zona: str) -> bool:
        if zona in ZONAS_SIEMPRE_EXCLUIDAS:
            return False
        return zona in self.publishable_zones

    @classmethod
    def cargar(cls, ruta: Optional[str] = None) -> "PublishConfig":
        if not ruta:
            return cls()
        p = Path(ruta)
        if not p.exists():
            raise AbortStage("invalid_config", etapa="C0", detalle={"motivo": f"no existe: {ruta}"})
        try:
            datos = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise AbortStage("invalid_config", etapa="C0", detalle={"motivo": str(exc)}) from exc
        try:
            return cls.model_validate(datos)
        except Exception as exc:
            from pydantic import ValidationError

            if isinstance(exc, ValidationError):
                raise AbortStage(
                    "invalid_config", etapa="C0",
                    detalle={"motivo": [e.get("loc") for e in exc.errors()]},
                ) from exc
            raise
