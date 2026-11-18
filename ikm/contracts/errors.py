# -*- coding: utf-8 -*-
"""Taxonomia de errores (L0.4).

Cada clase es un resultado definido: aborta, reporta, limita, degrada o falla
cerrado. Ninguna capa improvisa un comportamiento ante el fallo.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional


class ErrorTaxonomy:
    AbortStage = "AbortStage"
    Warning = "Warning"
    RateLimited = "RateLimited"
    DegradeResponse = "DegradeResponse"
    FailClosed = "FailClosed"


class RateLimitReason(str, Enum):
    interval = "interval"
    concurrency = "concurrency"
    rate = "rate"
    user_budget = "user_budget"
    global_budget = "global_budget"
    offtopic = "offtopic"


class IkmError(Exception):
    """Base de todos los errores del sistema."""

    taxon = "IkmError"

    def __init__(self, message: str, detalle: Optional[dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.detalle = detalle or {}


class AbortStage(IkmError):
    """Etapa de contenido fallida. Detiene la etapa; conserva salidas previas."""

    taxon = "AbortStage"

    def __init__(self, causa: str, etapa: str = "", detalle: Optional[dict] = None) -> None:
        super().__init__(f"abort[{causa}] en etapa {etapa}", detalle)
        self.causa = causa
        self.etapa = etapa


class Warning(IkmError):
    """Senal registrada; NO detiene la etapa."""

    taxon = "Warning"

    def __init__(self, senal: str, detalle: Optional[dict] = None) -> None:
        super().__init__(f"warn[{senal}]", detalle)
        self.senal = senal


class RateLimited(IkmError):
    """Rechazo por limite. Mapea a 429 con reason + retry_after."""

    taxon = "RateLimited"

    def __init__(self, reason: RateLimitReason, retry_after: Optional[float] = None,
                 detalle: Optional[dict] = None) -> None:
        super().__init__(f"rate_limited[{reason.value}]", detalle)
        self.reason = reason
        self.retry_after = retry_after


class DegradeResponse(IkmError):
    """Recuperacion sin modelo: reduce funcionalidad, no confiabilidad."""

    taxon = "DegradeResponse"

    def __init__(self, motivo: str, detalle: Optional[dict] = None) -> None:
        super().__init__(f"degrade[{motivo}]", detalle)
        self.motivo = motivo


class FailClosed(IkmError):
    """Servicio indispensable caido -> 503; el sitio estatico sigue."""

    taxon = "FailClosed"

    def __init__(self, servicio: str, detalle: Optional[dict] = None) -> None:
        super().__init__(f"fail_closed[{servicio}]", detalle)
        self.servicio = servicio
