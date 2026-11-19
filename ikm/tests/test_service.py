# -*- coding: utf-8 -*-
"""Tests de modulos de servicio (L2-L3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.contracts.config import LimitsConfig
from ikm.api.limits.quotas import QuotaManager
from ikm.api.limits.budget import BudgetManager
from ikm.api.limits.abuse import AbuseTracker
from ikm.api.auth.sessions import SessionManager
from ikm.api.auth.csrf import CSRFValidator
from ikm.api.retrieval.bm25 import BM25Index, buscar_bm25


def test_quota_check_length():
    cfg = LimitsConfig(max_message_chars=10)
    qm = QuotaManager(cfg)
    try:
        qm.check_length("a" * 20)
        assert False, "should raise"
    except Exception:
        pass
    qm.check_length("short")
    assert True


def test_budget_estimar_tokens():
    cfg = LimitsConfig()
    bm = BudgetManager(cfg)
    est = bm.estimar_tokens("hello world", contexto_tokens=100)
    assert est > 0
    assert est > 100


def test_budget_reservar_y_contabilizar():
    cfg = LimitsConfig(user_tokens_per_day=1000)
    bm = BudgetManager(cfg)
    res = bm.reservar_presupuesto("u1", 100)
    assert res is not None
    bm.contabilizar_uso_real(res, 50)
    restante = bm.obtener_presupuesto_restante("u1")
    assert restante["used_tokens"] == 50


def test_abuse_offtopic():
    cfg = LimitsConfig(offtopic_per_day=2)
    at = AbuseTracker(cfg)
    at.registrar_cuenta_nueva("u1")
    assert at.es_cuenta_nueva("u1") is True
    assert at.factor_cuenta_nueva("u1") == 0.5
    c1 = at.registrar_offtopic("u1")
    c2 = at.registrar_offtopic("u1")
    assert c1 == 1
    assert c2 == 2
    assert at.offtopic_excedido("u1") is True


def test_session_crear_validar():
    sm = SessionManager(secret_key="test-secret")
    result = sm.crear_sesion("u1")
    assert "session_id" in result
    sid = result["session_id"]
    session = sm.validar_sesion(sid)
    assert session["user_id"] == "u1"


def test_session_revocar():
    sm = SessionManager(secret_key="test-secret")
    result = sm.crear_sesion("u1")
    sid = result["session_id"]
    sm.revocar_sesion(sid)
    assert sm.obtener_usuario(sid) is None


def test_csrf_validar():
    csrf = CSRFValidator(allowed_origins={"http://localhost:3000"})
    token = csrf.generar_token("session_hash_1")
    assert csrf.validar_token("session_hash_1", token) is True
    assert csrf.validar_token("session_hash_1", "wrong") is False


def test_csrf_origin():
    csrf = CSRFValidator(allowed_origins={"http://localhost:3000"})
    assert csrf.validar_origin("http://localhost:3000") is True
    assert csrf.validar_origin("http://evil.com") is False


def test_bm25_buscar():
    chunks = [
        {"chunk_id": "c1#obj#0", "text": "HTTP es un protocolo de transferencia de hipertexto", "entity_uid": "c1"},
        {"chunk_id": "c2#obj#0", "text": "TCP es un protocolo de transporte confiable", "entity_uid": "c2"},
        {"chunk_id": "c3#obj#0", "text": "DNS resuelve nombres de dominio a direcciones IP", "entity_uid": "c3"},
    ]
    results = buscar_bm25("protocolo HTTP", chunks, top_k=2)
    assert len(results) >= 1
    assert results[0]["chunk"]["chunk_id"] == "c1#obj#0"


def test_bm25_index():
    chunks = [
        {"chunk_id": "c1#obj#0", "text": "HTTP protocolo", "entity_uid": "c1"},
    ]
    idx = BM25Index(chunks)
    assert len(idx.doc_tokens) == 1
    assert idx.avg_dl > 0

