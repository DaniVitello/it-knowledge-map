# -*- coding: utf-8 -*-
"""Sesiones por cookie (L2, capa 14)."""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from ikm.contracts.errors import AbortStage


class SessionError(AbortStage):
    pass


class SessionExpiredError(SessionError):
    pass


class SessionRevokedError(SessionError):
    pass


class SessionManager:
    """Gestiona sesiones de usuario por cookie."""

    def __init__(self, secret_key: str, sliding_days: int = 14, max_days: int = 30):
        self.secret_key = secret_key
        self.sliding_days = sliding_days
        self.max_days = max_days
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def _hash_session_id(self, session_id: str) -> str:
        return hashlib.sha256(
            (session_id + self.secret_key).encode("utf-8")
        ).hexdigest()

    def crear_sesion(self, user_id: str, ip_hash: Optional[str] = None,
                     ua_hash: Optional[str] = None) -> Dict[str, Any]:
        """Crea una sesion con vencimiento deslizante."""
        session_id = secrets.token_urlsafe(32)
        session_hash = self._hash_session_id(session_id)
        now = datetime.now(timezone.utc)
        session = {
            "id_hash": session_hash,
            "user_id": user_id,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(days=self.sliding_days)).isoformat(),
            "max_expires_at": (now + timedelta(days=self.max_days)).isoformat(),
            "last_seen_at": now.isoformat(),
            "ip_hash": ip_hash,
            "ua_hash": ua_hash,
            "revoked_at": None,
        }
        self._sessions[session_hash] = session
        return {"session_id": session_id, "session_hash": session_hash, "expires_at": session["expires_at"]}

    def validar_sesion(self, session_id: str) -> Dict[str, Any]:
        """Valida una sesion. Lanza excepcion si expiro o fue revocada."""
        session_hash = self._hash_session_id(session_id)
        session = self._sessions.get(session_hash)
        if not session:
            raise SessionError("session_not_found", etapa="auth")
        if session.get("revoked_at"):
            raise SessionRevokedError("session_revoked", etapa="auth")
        now = datetime.now(timezone.utc)
        expires = datetime.fromisoformat(session["expires_at"])
        max_expires = datetime.fromisoformat(session["max_expires_at"])
        if now > max_expires:
            raise SessionExpiredError("session_expired", etapa="auth",
                                     detalle={"motivo": "max lifetime exceeded"})
        if now > expires:
            raise SessionExpiredError("session_expired", etapa="auth",
                                     detalle={"motivo": "sliding expiry"})
        # Renovar vencimiento deslizante
        session["expires_at"] = (now + timedelta(days=self.sliding_days)).isoformat()
        session["last_seen_at"] = now.isoformat()
        return session

    def revocar_sesion(self, session_id: str) -> None:
        """Revoca la sesion."""
        session_hash = self._hash_session_id(session_id)
        session = self._sessions.get(session_hash)
        if session:
            session["revoked_at"] = datetime.now(timezone.utc).isoformat()

    def revocar_todas(self, user_id: str) -> int:
        """Revoca todas las sesiones de un usuario. Devuelve cantidad revocada."""
        count = 0
        for session in self._sessions.values():
            if session["user_id"] == user_id and not session.get("revoked_at"):
                session["revoked_at"] = datetime.now(timezone.utc).isoformat()
                count += 1
        return count

    def obtener_usuario(self, session_id: str) -> Optional[str]:
        """Devuelve el user_id de la sesion o None si invalida."""
        try:
            session = self.validar_sesion(session_id)
            return session["user_id"]
        except (SessionError, SessionExpiredError, SessionRevokedError):
            return None
