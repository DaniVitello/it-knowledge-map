# -*- coding: utf-8 -*-
"""Tests de chat (L3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.api.chat.scope import clasificar_alcance
from ikm.contracts.config import Config
from ikm.api.limits.quotas import QuotaManager
from ikm.api.limits.budget import BudgetManager
from ikm.api.limits.abuse import AbuseTracker
from ikm.api.chat.orchestrator import ChatOrchestrator


def test_scope_smalltalk():
    assert clasificar_alcance("hola", None) == "smalltalk"
    assert clasificar_alcance("gracias", None) == "smalltalk"


def test_scope_out():
    assert clasificar_alcance("receta de cocina", None) in ("out", "in_general_se")


def test_scope_se():
    assert clasificar_alcance("que es HTTP", None) == "in_general_se"


def test_scope_meta():
    assert clasificar_alcance("que es it knowledge map", None) == "meta"


def test_orchestrator_init():
    cfg = Config()
    qm = QuotaManager(cfg.limites)
    bm = BudgetManager(cfg.limites)
    at = AbuseTracker(cfg.limites)
    orch = ChatOrchestrator(cfg, None, qm, bm, at)
    assert orch.config == cfg


def test_orchestrator_smalltalk():
    cfg = Config()
    qm = QuotaManager(cfg.limites)
    bm = BudgetManager(cfg.limites)
    at = AbuseTracker(cfg.limites)
    orch = ChatOrchestrator(cfg, None, qm, bm, at)
    result = orch.procesar_consulta("u1", "127.0.0.1", "hola", "r1")
    assert result.get("scope", {}).get("class") == "smalltalk"


def test_orchestrator_out_of_scope():
    cfg = Config()
    qm = QuotaManager(cfg.limites)
    bm = BudgetManager(cfg.limites)
    at = AbuseTracker(cfg.limites)
    orch = ChatOrchestrator(cfg, None, qm, bm, at)
    result = orch.procesar_consulta("u1", "127.0.0.1", "receta de cocina", "r1")
    assert result.get("scope", {}).get("class") in ("out", "in_general_se", "in_project")


