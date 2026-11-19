# -*- coding: utf-8 -*-
"""Flujo OIDC con PKCE gestionado por el backend (L2, capa 14)."""
from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional, Tuple

from ikm.contracts.errors import AbortStage


class AuthError(AbortStage):
    pass


class InvalidTokenError(AuthError):
    pass


class UserNotFoundError(AuthError):
    pass


def generar_state() -> str:
    """Genera un state aleatorio para CSRF protection."""
    return secrets.token_urlsafe(32)


def generar_nonce() -> str:
    """Genera un nonce para el ID token."""
    return secrets.token_urlsafe(32)


def generar_pkce_verifier() -> str:
    """Genera el code_verifier para PKCE (43-128 chars)."""
    return secrets.token_urlsafe(64)


def generar_pkce_challenge(verifier: str) -> str:
    """Genera el code_challenge (S256) a partir del verifier."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def construir_url_autorizacion(client_id: str, redirect_uri: str,
                                state: str, nonce: str,
                                code_challenge: str) -> str:
    """Construye la URL de autorizacion de Google."""
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"


def verificar_id_token(id_token: str, client_id: str, nonce: str) -> Dict[str, Any]:
    """Verifica el ID token: firma, iss, aud, exp, nonce, email_verified.

    En produccion, usar google-auth o PyJWT para verificar la firma.
    Este es un stub que valida la estructura.
    """
    # Stub: en produccion, verificar con google.oauth2.id_token
    # Aqui solo validamos que no este vacio
    if not id_token:
        raise InvalidTokenError("token_vacio", etapa="auth",
                                detalle={"motivo": "id_token vacio"})
    # Parsear JWT (sin verificar firma en stub)
    try:
        parts = id_token.split(".")
        if len(parts) != 3:
            raise InvalidTokenError("token_malformado", etapa="auth")
        import base64 as b64
        payload = b64.urlsafe_b64decode(parts[1] + "==")
        data = __import__("json").loads(payload)
    except Exception as exc:
        raise InvalidTokenError("token_invalido", etapa="auth",
                                detalle={"motivo": str(exc)}) from exc

    # Validar claims basicos
    if data.get("aud") != client_id:
        raise InvalidTokenError("aud_invalido", etapa="auth",
                                detalle={"aud": data.get("aud"), "expected": client_id})
    if data.get("nonce") != nonce:
        raise InvalidTokenError("nonce_invalido", etapa="auth")
    if not data.get("email_verified"):
        raise InvalidTokenError("email_no_verificado", etapa="auth")
    iss = data.get("iss")
    if iss not in ("https://accounts.google.com", "accounts.google.com"):
        raise InvalidTokenError("iss_invalido", etapa="auth", detalle={"iss": iss})

    return data


def buscar_o_crear_usuario(sub: str, email: str, email_verified: bool) -> str:
    """Busca o crea un usuario por sub (no por correo). Devuelve user_id."""
    # Stub: en produccion, consultar Postgres
    # Por ahora, generar un user_id determinista a partir del sub
    return f"u_{hashlib.sha256(sub.encode()).hexdigest()[:12]}"


def start() -> Dict[str, Any]:
    """GET /api/auth/google/start: genera state, nonce, verificador PKCE."""
    state = generar_state()
    nonce = generar_nonce()
    verifier = generar_pkce_verifier()
    challenge = generar_pkce_challenge(verifier)
    return {
        "state": state,
        "nonce": nonce,
        "code_verifier": verifier,
        "code_challenge": challenge,
    }


def callback(code: str, state: str, expected_state: str, nonce: str,
            client_id: str) -> Dict[str, Any]:
    """GET /api/auth/google/callback: verifica y crea sesion."""
    if state != expected_state:
        raise AuthError("state_mismatch", etapa="auth")
    # En produccion: intercambiar code por tokens con Google
    # id_token = intercambiar_code(code, client_id, code_verifier)
    # data = verificar_id_token(id_token, client_id, nonce)
    # user_id = buscar_o_crear_usuario(data["sub"], data["email"], data["email_verified"])
    return {"user_id": "stub", "session_token": secrets.token_urlsafe(32)}
