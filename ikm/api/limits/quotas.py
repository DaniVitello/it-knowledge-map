# -*- coding: utf-8 -*-
"""Limites baratos: longitud, intervalo, concurrencia, tasa (L2, capa 15)."""
from __future__ import annotations

import time
from typing import Any, Dict, Optional

from ikm.contracts.config import LimitsConfig
from ikm.contracts.errors import AbortStage


class LimitExceededError(AbortStage):
    pass


class RateLimitError(LimitExceededError):
    pass


class ConcurrencyError(LimitExceededError):
    pass


class QuotaManager:
    """Gestiona limites baratos por usuario e IP."""

    def __init__(self, config: LimitsConfig):
        self.config = config
        self._user_last_request: Dict[str, float] = {}
        self._user_concurrency: Dict[str, int] = {}
        self._ip_requests: Dict[str, List[float]] = {}
        self._user_requests_hour: Dict[str, List[float]] = {}

    def check_length(self, message: str) -> None:
        if len(message) > self.config.max_message_chars:
            raise LimitExceededError(
                "message_too_long", etapa="limits",
                detalle={"max": self.config.max_message_chars, "actual": len(message)},
            )

    def check_interval(self, user_id: str) -> None:
        now = time.monotonic()
        last = self._user_last_request.get(user_id)
        if last is not None and (now - last) < self.config.min_interval_seconds:
            raise RateLimitError(
                "min_interval", etapa="limits",
                detalle={"retry_after": self.config.min_interval_seconds - (now - last)},
            )
        self._user_last_request[user_id] = now

    def check_concurrency(self, user_id: str) -> None:
        current = self._user_concurrency.get(user_id, 0)
        if current >= self.config.user_concurrency:
            raise ConcurrencyError("user_concurrency", etapa="limits",
                                   detalle={"current": current, "max": self.config.user_concurrency})
        self._user_concurrency[user_id] = current + 1

    def release_concurrency(self, user_id: str) -> None:
        current = self._user_concurrency.get(user_id, 0)
        if current > 0:
            self._user_concurrency[user_id] = current - 1

    def check_hourly(self, user_id: str) -> None:
        now = time.monotonic()
        window = self._user_requests_hour.setdefault(user_id, [])
        # Limpiar requests fuera de la ventana de 1 hora
        cutoff = now - 3600
        window[:] = [t for t in window if t > cutoff]
        if len(window) >= self.config.user_requests_per_hour:
            raise RateLimitError("user_requests_per_hour", etapa="limits",
                                 detalle={"retry_after": 3600 - (now - window[0])})
        window.append(now)

    def check_ip(self, ip: str) -> None:
        now = time.monotonic()
        window = self._ip_requests.setdefault(ip, [])
        cutoff = now - 3600
        window[:] = [t for t in window if t > cutoff]
        if len(window) >= self.config.ip_requests_per_hour:
            raise RateLimitError("ip_requests_per_hour", etapa="limits",
                                 detalle={"retry_after": 3600 - (now - window[0])})
        window.append(now)

    def verificar_limites_baratos(self, user_id: str, ip: str, message: str) -> None:
        """Verifica todos los limites baratos. Lanza excepcion si alguno se excede."""
        self.check_length(message)
        self.check_interval(user_id)
        self.check_concurrency(user_id)
        self.check_hourly(user_id)
        self.check_ip(ip)
