# -*- coding: utf-8 -*-
"""Proteccion CSRF (L2, capa 14)."""
from __future__ import annotations

from typing import Set

from ikm.contracts.errors import AbortStage


class CSRFDeniedError(AbortStage):
    pass


class CSRFValidator:
    """Valida tokens CSRF y Origins permitidos."""

    def __init__(self, allowed_origins: Set[str], token_length: int = 32):
        self.allowed_origins = allowed_origins
        self.token_length = token_length
        self._tokens: dict[str, str] = {}  # session_hash -> csrf_token

    def generar_token(self, session_hash: str) -> str:
        """Genera un token CSRF para la sesion."""
        import secrets
        token = secrets.token_urlsafe(self.token_length)
        self._tokens[session_hash] = token
        return token

    def obtener_token(self, session_hash: str) -> str:
        """Obtiene el token CSRF de la sesion o genera uno nuevo."""
        if session_hash not in self._tokens:
            return self.generar_token(session_hash)
        return self._tokens[session_hash]

    def validar_origin(self, origin: str) -> bool:
        """Valida que el Origin este en la lista permitida."""
        if not origin:
            return False
        return origin in self.allowed_origins

    def validar_token(self, session_hash: str, token: str) -> bool:
        """Valida el token CSRF contra el de la sesion."""
        expected = self._tokens.get(session_hash)
        if not expected:
            return False
        # Comparacion en tiempo constante
        import hmac
        return hmac.compare_digest(expected, token)

    def validar(self, origin: str, session_hash: str, token: str) -> bool:
        """Validacion completa: origin + token."""
        if not self.validar_origin(origin):
            raise CSRFDeniedError("origin_denied", etapa="auth",
                                  detalle={"origin": origin})
        if not self.validar_token(session_hash, token):
            raise CSRFDeniedError("token_invalid", etapa="auth")
        return True

    def invalidar(self, session_hash: str) -> None:
        """Invalida el token CSRF de la sesion."""
        self._tokens.pop(session_hash, None)
