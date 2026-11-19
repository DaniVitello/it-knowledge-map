# -*- coding: utf-8 -*-
"""Presupuestos de tokens: por usuario/dia, global/dia, por minuto del proveedor (L2, capa 15)."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ikm.contracts.config import LimitsConfig
from ikm.contracts.errors import AbortStage


class BudgetExceededError(AbortStage):
    pass


class BudgetReservation:
    """Representa una reserva de presupuesto."""

    def __init__(self, user_id: str, estimated_tokens: int, reservation_id: str):
        self.user_id = user_id
        self.estimated_tokens = estimated_tokens
        self.reservation_id = reservation_id
        self.actual_tokens: Optional[int] = None
        self.released = False


class BudgetManager:
    """Gestiona presupuestos de tokens por usuario y global."""

    def __init__(self, config: LimitsConfig):
        self.config = config
        self._user_tokens: Dict[str, Dict[str, int]] = {}  # user_id -> {day: tokens}
        self._global_tokens: Dict[str, int] = {}  # day -> tokens
        self._provider_tpm: List[float] = []  # timestamps de tokens del proveedor
        self._reservations: Dict[str, BudgetReservation] = {}

    def _today(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _user_tokens_today(self, user_id: str) -> int:
        day = self._today()
        return self._user_tokens.get(user_id, {}).get(day, 0)

    def _global_tokens_today(self) -> int:
        return self._global_tokens.get(self._today(), 0)

    def estimar_tokens(self, message: str, contexto_tokens: int = 2200) -> int:
        """Estima tokens para una consulta (entrada + salida estimada)."""
        # ~4 chars por token
        input_tokens = len(message) // 4 + contexto_tokens
        output_tokens = self.config.max_output_tokens
        return input_tokens + output_tokens

    def reservar_presupuesto(self, user_id: str, estimacion_tokens: int) -> BudgetReservation:
        """Reserva tokens. Lanza BudgetExceededError si no alcanza."""
        # Verificar presupuesto por usuario
        user_used = self._user_tokens_today(user_id)
        if user_used + estimacion_tokens > self.config.user_tokens_per_day:
            raise BudgetExceededError(
                "user_budget_exceeded", etapa="limits",
                detalle={
                    "used": user_used,
                    "requested": estimacion_tokens,
                    "limit": self.config.user_tokens_per_day,
                    "retry_after": "tomorrow",
                },
            )

        # Verificar presupuesto global
        global_used = self._global_tokens_today()
        global_limit = int(self.config.global_tokens_per_day_ratio * 100000)  # placeholder
        if global_used + estimacion_tokens > global_limit:
            raise BudgetExceededError(
                "global_budget_exceeded", etapa="limits",
                detalle={"retry_after": "tomorrow"},
            )

        # Verificar TPM del proveedor (margen del 20%)
        now = time.monotonic()
        window = [t for t in self._provider_tpm if t > now - 60]
        self._provider_tpm = window
        # Estimacion simple: si hay muchos requests recientes, rechazar
        if len(window) > 10:
            raise BudgetExceededError(
                "provider_tpm_exceeded", etapa="limits",
                detalle={"retry_after": 60},
            )

        reservation_id = f"res_{user_id}_{int(now)}"
        reservation = BudgetReservation(user_id, estimacion_tokens, reservation_id)
        self._reservations[reservation_id] = reservation
        return reservation

    def contabilizar_uso_real(self, reservation: BudgetReservation, tokens_reales: int) -> None:
        """Reemplaza la reserva por el uso real."""
        if reservation.released:
            return
        day = self._today()
        # Actualizar contador por usuario
        user_data = self._user_tokens.setdefault(reservation.user_id, {})
        user_data[day] = user_data.get(day, 0) + tokens_reales
        # Actualizar contador global
        self._global_tokens[day] = self._global_tokens.get(day, 0) + tokens_reales
        # Registrar TPM del proveedor
        self._provider_tpm.append(time.monotonic())
        reservation.actual_tokens = tokens_reales
        reservation.released = True
        self._reservations.pop(reservation.reservation_id, None)

    def liberar_reserva(self, reservation: BudgetReservation) -> None:
        """Libera una reserva sin contabilizar (en caso de error)."""
        if not reservation.released:
            reservation.released = True
            self._reservations.pop(reservation.reservation_id, None)

    def obtener_presupuesto_restante(self, user_id: str) -> Dict[str, int]:
        """Devuelve el presupuesto restante del usuario."""
        used = self._user_tokens_today(user_id)
        return {
            "remaining_tokens": max(0, self.config.user_tokens_per_day - used),
            "used_tokens": used,
            "limit_tokens": self.config.user_tokens_per_day,
        }
