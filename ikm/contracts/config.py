# -*- coding: utf-8 -*-
"""Configuracion de feature flags, limites y plan del modelo (L0.4).

Valores propuestos por el disenio ([DR-xx] / [propuesto]). Cambiar un valor NO
cambia la estructura de ninguna capa: todo se parametriza aqui.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class FeatureFlags(_Base):
    embeddings_habilitados: bool = False       # [DR-09] solo si la eval lo justifica
    grafo_3d_habilitado: bool = True           # [DR-14] sujeto a prototipo medible
    streaming_por_bloques: bool = False        # [DR-10] respuesta completa validada
    borradores_relaciones: bool = True         # C4 opcional, siempre como derived
    persistencia_estados_servidor: bool = False  # [propuesto 19.4] solo si cross-device


class LimitsConfig(_Base):
    """Valores iniciales propuestos (disenio 17.2); calibrables (L6)."""

    max_message_chars: int = 800
    max_output_tokens: int = 700            # INCLUYE tokens de razonamiento
    min_interval_seconds: int = 4
    user_concurrency: int = 1
    global_concurrency: int = 3
    user_requests_per_hour: int = 20
    user_tokens_per_day: int = 40000        # ~10 consultas
    global_tokens_per_day_ratio: float = 0.8  # 80% del tope del proveedor o gasto
    provider_tpm_margin: float = 0.20
    offtopic_per_day: int = 2
    new_account_factor: float = 0.5         # primeras 24 h
    ip_requests_per_hour: int = 120         # complementario, NUNCA unico
    retencion_mensajes_dias: int = 30       # [propuesto 25]
    max_tokens_contexto_recuperacion: int = 2200


class PlanModelo(_Base):
    """[DR-08] free=demo | developer=publico."""

    plan: Literal["free", "developer"] = "free"
    provider: str = "groq"
    modelo: str = "openai/gpt-oss-120b"
    tope_gasto_mensual_usd: float = 5.0     # [propuesto 25]
    reasoning_effort: Literal["low", "medium", "high"] = "low"
    temperatura: float = 0.2
    timeout_segundos: int = 20
    reintentos: int = 1


class Config(_Base):
    feature_flags: FeatureFlags = Field(default_factory=FeatureFlags)
    limites: LimitsConfig = Field(default_factory=LimitsConfig)
    plan_modelo: PlanModelo = Field(default_factory=PlanModelo)
    schema_version: str = "2.0.0"

    def hash_config(self) -> str:
        """Hash canonico de la configuracion (para la clave de cache)."""
        from .utils import sha256_text

        import json

        crudo = json.dumps(
            json.loads(self.model_dump_json(exclude_none=True)),
            ensure_ascii=False, sort_keys=True,
        )
        return sha256_text(crudo)
