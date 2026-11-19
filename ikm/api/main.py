# -*- coding: utf-8 -*-
"""FastAPI app del plano de servicio (L2-L3)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ikm.contracts.config import Config
from ikm.api.release.loader import cargar_release, listar_releases

app = FastAPI(title="IT Knowledge Map API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado global
_config: Optional[Config] = None
_release: Any = None
_RELEASES_DIR = Path(r"C:/Users/DGVit/Proyectos/IT Career/ikm/workdir/releases")


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config


def get_release() -> Any:
    global _release
    if _release is None:
        # Cargar el release mas reciente
        releases = listar_releases(_RELEASES_DIR)
        if releases:
            latest = releases[-1]
            _release = cargar_release(latest, _RELEASES_DIR / latest)
    return _release


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "version": "2.0.0"}


@app.get("/api/release")
def get_release_info() -> Dict[str, Any]:
    release = get_release()
    if release is None:
        raise HTTPException(status_code=404, detail="no release available")
    return {
        "release_id": release.release_id,
        "manifest": release.manifest,
    }


@app.get("/api/release/{release_id}")
def get_release_by_id(release_id: str) -> Dict[str, Any]:
    release_path = _RELEASES_DIR / release_id
    if not release_path.exists():
        raise HTTPException(status_code=404, detail="release not found")
    release = cargar_release(release_id, release_path)
    return {
        "release_id": release.release_id,
        "manifest": release.manifest,
    }


@app.get("/api/concepts/{uid}")
def get_concept(uid: str) -> Dict[str, Any]:
    release = get_release()
    if release is None:
        raise HTTPException(status_code=404, detail="no release")
    try:
        data = release.load_json(f"concepts/{uid}.json")
        return data
    except Exception:
        # Try to find in parsed
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


@app.post("/api/chat")
def chat_endpoint(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: requiere auth, limits, retrieval, llm
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=422, detail="message required")
    return {
        "blocks": [{"text": f"Echo: {message}", "basis": "general", "sources": []}],
        "degraded": False,
        "scope": {"class": "in_general_se", "offtopic_today": 0},
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
