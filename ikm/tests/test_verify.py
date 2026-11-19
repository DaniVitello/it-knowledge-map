# -*- coding: utf-8 -*-
"""Tests de verificacion (L3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.api.verify.verifier import ResponseVerifier, verificar


def test_verifier_v2_fuentes_invalidas():
    rv = ResponseVerifier(release=None, retrieved_chunks=[])
    resp = {"blocks": [{"text": "test", "basis": "documented", "sources": ["chunk_invalido"]}], "ui_actions": [], "suggestions": []}
    result = rv.verificar(resp)
    # La fuente invalida se elimina
    assert result["blocks"][0]["sources"] == []


def test_verifier_v3_documented_sin_fuentes():
    rv = ResponseVerifier(release=None, retrieved_chunks=[])
    resp = {"blocks": [{"text": "sin entidades", "basis": "documented", "sources": []}], "ui_actions": [], "suggestions": []}
    result = rv.verificar(resp)
    # Pasa a general
    assert result["blocks"][0]["basis"] == "general"


def test_verifier_v8_elimina_urls():
    rv = ResponseVerifier(release=None, retrieved_chunks=[])
    resp = {"blocks": [{"text": "ver https://example.com mas", "basis": "general", "sources": []}], "ui_actions": [], "suggestions": []}
    result = rv.verificar(resp)
    assert "https://example.com" not in result["blocks"][0]["text"]


def test_verifier_v9_recorta():
    rv = ResponseVerifier(release=None, retrieved_chunks=[])
    long_text = "a" * 3000
    resp = {"blocks": [{"text": long_text, "basis": "general", "sources": []}], "ui_actions": [], "suggestions": []}
    result = rv.verificar(resp)
    assert len(result["blocks"][0]["text"]) <= 2000


def test_verifier_v7_acciones_invalidas():
    rv = ResponseVerifier(release=None, retrieved_chunks=[])
    resp = {"blocks": [], "ui_actions": [{"type": "invalid_action", "payload": {"uids": []}}], "suggestions": []}
    result = rv.verificar(resp)
    assert len(result["ui_actions"]) == 0


def test_verificar_funcion():
    result = verificar({"blocks": [], "ui_actions": [], "suggestions": []}, [], None)
    assert isinstance(result, dict)
