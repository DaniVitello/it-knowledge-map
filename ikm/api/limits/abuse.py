# -*- coding: utf-8 -*-
"""Abuso: cupo fuera de tema, cuentas nuevas con cupo reducido, interruptor global (L2, capa 15)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from ikm.contracts.config import LimitsConfig
from ikm.contracts.errors import AbortStage


class AbuseEventKind:
    RATE_LIMIT = "rate_limit"
    OFFTOPIC = "offtopic"
    CSRF = "csrf"
    AUTH_FAILURE = "auth_failure"
    MANUAL = "manual"


class AbuseTracker:
    """Rastrea eventos de abuso por usuario e IP."""

    def __init__(self, config: LimitsConfig):
        self.config = config
        self._events: List[Dict[str, Any]] = []
        self._offtopic_counts: Dict[str, int] = {}  # user_id -> count today
        self._new_account_cutoff: Dict[str, datetime] = {}  # user_id -> created_at
        self._global_switch: bool = True  # interruptor global

    def registrar_evento(self, user_id: Optional[str], ip_hash: str, kind: str) -> None:
        """Registra un evento de abuso."""
        self._events.append({
            "user_id": user_id,
            "ip_hash": ip_hash,
            "kind": kind,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

    def registrar_cuenta_nueva(self, user_id: str) -> None:
        """Registra que una cuenta es nueva (primeras 24h con cupo reducido)."""
        self._new_account_cutoff[user_id] = datetime.now(timezone.utc)

    def es_cuenta_nueva(self, user_id: str) -> bool:
        """Verifica si la cuenta tiene menos de 24h."""
        created = self._new_account_cutoff.get(user_id)
        if not created:
            return False
        return datetime.now(timezone.utc) - created < timedelta(hours=24)

    def factor_cuenta_nueva(self, user_id: str) -> float:
        """Devuelve el factor de reduccion para cuentas nuevas (0.5)."""
        if self.es_cuenta_nueva(user_id):
            return self.config.new_account_factor
        return 1.0

    def registrar_offtopic(self, user_id: str) -> int:
        """Registra una consulta fuera de tema. Devuelve el conteo actual."""
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{user_id}:{day}"
        self._offtopic_counts[key] = self._offtopic_counts.get(key, 0) + 1
        return self._offtopic_counts[key]

    def offtopic_excedido(self, user_id: str) -> bool:
        """Verifica si el usuario excedio el cupo de offtopic (2 por dia)."""
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{user_id}:{day}"
        return self._offtopic_counts.get(key, 0) >= self.config.offtopic_per_day

    def interruptor_global_activo(self) -> bool:
        """Verifica si el interruptor global esta activo."""
        return self._global_switch

    def desactivar_interruptor(self) -> None:
        """Desactiva el interruptor global (chatbot desactivado)."""
        self._global_switch = False

    def activar_interruptor(self) -> None:
        """Activa el interruptor global."""
        self._global_switch = True

    def eventos_por_usuario(self, user_id: str) -> List[Dict[str, Any]]:
        """Devuelve los eventos de abuso de un usuario."""
        return [e for e in self._events if e["user_id"] == user_id]

    def eventos_por_ip(self, ip_hash: str) -> List[Dict[str, Any]]:
        """Devuelve los eventos de abuso de una IP."""
        return [e for e in self._events if e["ip_hash"] == ip_hash]
