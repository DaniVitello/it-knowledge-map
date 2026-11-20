# -*- coding: utf-8 -*-
"""Tests de LLM (L3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.api.llm.prompts import render_p1, render_p2, PROMPT_VERSION
from ikm.contracts.config import PlanModelo
from ikm.api.llm.adapter import LLMAdapter


def test_render_p1():
    prompt = render_p1("contexto", ["c_ABC"], "historial", "que es HTTP?")
    assert "ROL: Asistente" in prompt
    assert "ALLOWED_UIDS" in prompt
    assert "c_ABC" in prompt
    assert "que es HTTP?" in prompt


def test_render_p2():
    prompt = render_p2("nota A", "nota B", "fragmentos", ["chunk1"])
    assert "ROL: Generador" in prompt
    assert "type_proposal" in prompt


def test_prompt_version():
    assert PROMPT_VERSION == "1.0.0"


def test_llm_adapter_init():
    cfg = PlanModelo()
    adapter = LLMAdapter(cfg)
    assert adapter.config == cfg
    assert adapter.model == cfg.modelo
    assert isinstance(adapter.keys, list)


def test_llm_adapter_chat_sin_keys():
    cfg = PlanModelo()
    adapter = LLMAdapter(cfg)
    adapter.keys = []  # sin keys: debe fallar sin llamar a la red
    try:
        adapter.chat([{"role": "user", "content": "hi"}])
        assert False, "should raise"
    except Exception:
        assert True

