# -*- coding: utf-8 -*-
"""FastAPI del plano de servicio (L5-L9): chat real sobre el release.

Chat ABIERTO con rate-limit por IP (QuotaManager). Google auth OIDC disponible
como base (flag IKM_REQUIRE_AUTH=0 por ahora: no se exige login). El LLM es Groq
(openai/gpt-oss-120b) con las keys de la sintesis. Portable a HF Spaces.
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from ikm.contracts.config import Config
from ikm.api.release.loader import cargar_release, listar_releases
from ikm.api.chat.orchestrator import ChatOrchestrator
from ikm.api.limits.quotas import QuotaManager
from ikm.api.limits.budget import BudgetManager
from ikm.api.limits.abuse import AbuseTracker
from ikm.api.llm.adapter import LLMAdapter
from ikm.api.auth.sessions import SessionManager
from ikm.api.auth import oidc

app = FastAPI(title="IT Knowledge Map API", version="2.0.0")

# --- Configuracion por entorno ---------------------------------------------
_DEFAULT_ORIGINS = (
    "https://it-knowledge-map-v2.netlify.app,"
    "http://localhost:5173,http://localhost:3000,"
    "http://192.168.0.107:5173"
)
CORS_ORIGINS = [o.strip() for o in os.environ.get("IKM_CORS_ORIGINS", _DEFAULT_ORIGINS).split(",") if o.strip()]
REQUIRE_AUTH = os.environ.get("IKM_REQUIRE_AUTH", "0") == "1"
RELEASES_DIR = Path(os.environ.get("IKM_RELEASE_DIR", r"C:/Users/DGVit/Proyectos/IT Career/ikm/workdir/releases"))
FRONTEND_URL = os.environ.get("IKM_FRONTEND_URL", "https://it-knowledge-map-v2.netlify.app")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
SESSION_SECRET = os.environ.get("IKM_SESSION_SECRET", secrets.token_urlsafe(32))

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Estado global ----------------------------------------------------------
_config: Optional[Config] = None
_release: Any = None
_orchestrator: Optional[ChatOrchestrator] = None
_sessions = SessionManager(SESSION_SECRET)
_pending_oidc: Dict[str, Dict[str, str]] = {}


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config


def get_release() -> Any:
    global _release
    if _release is None:
        releases = listar_releases(RELEASES_DIR)
        if releases:
            latest = releases[-1]
            _release = cargar_release(latest, RELEASES_DIR / latest)
    return _release


def get_orchestrator() -> ChatOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        cfg = get_config()
        release = get_release()
        adapter = LLMAdapter(cfg.plan_modelo)
        orch = ChatOrchestrator(
            cfg, release,
            QuotaManager(cfg.limites),
            BudgetManager(cfg.limites),
            AbuseTracker(cfg.limites),
            llm_adapter=adapter if adapter.disponible else None,
        )
        if release is not None:
            try:
                chunks = release.load_json("chunks.json")
                if isinstance(chunks, dict):
                    chunks = chunks.get("chunks", [])
                orch.set_chunks(chunks or [])
            except Exception:
                orch.set_chunks([])
        _orchestrator = orch
    return _orchestrator


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def session_user(request: Request) -> Optional[str]:
    sid = request.cookies.get("ikm_session")
    if not sid:
        return None
    return _sessions.obtener_usuario(sid)


# --- Health / release -------------------------------------------------------
@app.get("/health")
def health() -> Dict[str, Any]:
    rel = get_release()
    orch = get_orchestrator()
    return {
        "status": "ok",
        "version": "2.0.0",
        "release_id": rel.release_id if rel else None,
        "llm_disponible": bool(orch.llm and orch.llm.disponible),
        "auth_configured": bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET),
        "require_auth": REQUIRE_AUTH,
    }


@app.get("/api/release")
def get_release_info() -> Dict[str, Any]:
    release = get_release()
    if release is None:
        raise HTTPException(status_code=404, detail="no release available")
    return {"release_id": release.release_id, "manifest": release.manifest}


@app.get("/api/concepts/{uid}")
def get_concept(uid: str) -> Dict[str, Any]:
    release = get_release()
    if release is None:
        raise HTTPException(status_code=404, detail="no release")
    try:
        return release.load_json(f"concepts/{uid}.json")
    except Exception:
        raise HTTPException(status_code=404, detail=f"concept not found: {uid}")


@app.get("/api/graph")
def get_graph() -> Dict[str, Any]:
    release = get_release()
    if release is None:
        raise HTTPException(status_code=404, detail="no release")
    try:
        return release.load_json("graph.json")
    except Exception:
        raise HTTPException(status_code=404, detail="graph not found")


# --- Chat (abierto, rate-limit por IP) --------------------------------------
@app.post("/api/chat")
def chat_endpoint(payload: Dict[str, Any], request: Request) -> Any:
    message = (payload.get("message") or "").strip()
    if not message:
        raise HTTPException(status_code=422, detail="message required")

    ip = client_ip(request)
    user = session_user(request)
    if REQUIRE_AUTH and not user:
        raise HTTPException(status_code=401, detail="auth_required")
    user_id = user or f"anon:{ip}"

    orch = get_orchestrator()
    release = get_release()
    release_id = release.release_id if release else "unknown"
    result = orch.procesar_consulta(user_id, ip, message, release_id)

    if isinstance(result, dict) and result.get("error"):
        status = result.get("status", 429)
        resp = JSONResponse(status_code=status, content=result)
        if result.get("retry_after") is not None:
            resp.headers["Retry-After"] = str(result["retry_after"])
        return resp
    return result


# --- Google auth OIDC (base, no exigido por ahora) --------------------------
def _redirect_uri(request: Request) -> str:
    explicit = os.environ.get("GOOGLE_REDIRECT_URI")
    if explicit:
        return explicit
    return str(request.base_url).rstrip("/") + "/api/auth/google/callback"


@app.get("/api/auth/google/login")
def google_login(request: Request) -> Any:
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET):
        raise HTTPException(status_code=503, detail="google_auth_not_configured")
    state = oidc.generar_state()
    nonce = oidc.generar_nonce()
    verifier = oidc.generar_pkce_verifier()
    challenge = oidc.generar_pkce_challenge(verifier)
    _pending_oidc[state] = {"nonce": nonce, "verifier": verifier}
    url = oidc.construir_url_autorizacion(
        GOOGLE_CLIENT_ID, _redirect_uri(request), state, nonce, challenge
    )
    return RedirectResponse(url)


@app.get("/api/auth/google/callback")
def google_callback(request: Request, code: str = "", state: str = "") -> Any:
    pending = _pending_oidc.pop(state, None)
    if not pending:
        raise HTTPException(status_code=400, detail="invalid_state")
    try:
        tokens = oidc.intercambiar_code(
            code, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
            _redirect_uri(request), pending["verifier"],
        )
        claims = oidc.verificar_id_token_real(tokens["id_token"], GOOGLE_CLIENT_ID, pending["nonce"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"auth_failed: {exc}")
    user_id = claims.get("sub") or claims.get("email")
    sess = _sessions.crear_sesion(user_id, ip_hash=client_ip(request))
    resp = RedirectResponse(FRONTEND_URL + "/chat")
    resp.set_cookie(
        "ikm_session", sess["session_id"],
        httponly=True, secure=True, samesite="none", max_age=14 * 24 * 3600,
    )
    return resp


@app.get("/api/auth/me")
def auth_me(request: Request) -> Dict[str, Any]:
    user = session_user(request)
    return {"authenticated": bool(user), "user_id": user}


@app.post("/api/auth/logout")
def auth_logout(request: Request, response: Response) -> Dict[str, Any]:
    sid = request.cookies.get("ikm_session")
    if sid:
        _sessions.revocar_sesion(sid)
    response.delete_cookie("ikm_session")
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)