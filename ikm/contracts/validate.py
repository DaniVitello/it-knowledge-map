# -*- coding: utf-8 -*-
"""Validacion contra esquema (L0.4): validar_contra_esquema aborta si no valida."""
from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel, ValidationError

from .errors import AbortStage


def validar_contra_esquema(obj: Any, esquema: Type[BaseModel], etapa: str = "") -> BaseModel:
    """Valida y devuelve el modelo tipado. Si no valida, ABORTA (schema_invalid)."""
    try:
        if isinstance(obj, esquema):
            return obj
        return esquema.model_validate(obj)
    except ValidationError as exc:
        errores = [
            {"loc": ".".join(str(x) for x in e.get("loc", ())), "msg": e.get("msg", "")}
            for e in exc.errors()
        ]
        raise AbortStage("schema_invalid", etapa=etapa, detalle={"errores": errores}) from exc


def validar_o_none(obj: Any, esquema: Type[BaseModel], etapa: str = "") -> BaseModel:
    return validar_contra_esquema(obj, esquema, etapa=etapa)
