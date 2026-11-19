# -*- coding: utf-8 -*-
"""Tests de reglas comunes del pipeline (L1.0)."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.content.pipeline import ContentRunner, ejecutar_etapa, Etapa
from ikm.contracts.config import Config
from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import escribir_json_atomico, hash_arbol_vault


def test_ejecutar_etapa_cache_hit():
    cfg = Config()
    workdir = Path(tempfile.mkdtemp())
    runner = ContentRunner(workdir, cfg, str(workdir))
    calls = {"n": 0}

    def ejecutar():
        calls["n"] += 1
        return {"value": 42}

    def validar(x):
        return x

    e1 = ejecutar_etapa("C0", {"input": "test"}, cfg, workdir, ejecutar, validar, runner.cache)
    assert e1.cache_hit is False
    assert calls["n"] == 1

    e2 = ejecutar_etapa("C0", {"input": "test"}, cfg, workdir, ejecutar, validar, runner.cache)
    assert e2.cache_hit is True
    assert calls["n"] == 1  # no se re-ejecuto


def test_ejecutar_etapa_diferente_entrada():
    cfg = Config()
    workdir = Path(tempfile.mkdtemp())
    runner = ContentRunner(workdir, cfg, str(workdir))
    calls = {"n": 0}

    def ejecutar():
        calls["n"] += 1
        return {"value": calls["n"]}

    def validar(x):
        return x

    e1 = ejecutar_etapa("C0", {"input": "a"}, cfg, workdir, ejecutar, validar, runner.cache)
    e2 = ejecutar_etapa("C0", {"input": "b"}, cfg, workdir, ejecutar, validar, runner.cache)
    assert e1.cache_hit is False
    assert e2.cache_hit is False
    assert calls["n"] == 2


def test_content_runner_guardar_salida():
    cfg = Config()
    workdir = Path(tempfile.mkdtemp())
    runner = ContentRunner(workdir, cfg, str(workdir))
    runner.guardar_salida("test", {"hello": "world"})
    assert (workdir / "test.json").exists()
    import json
    data = json.loads((workdir / "test.json").read_text())
    assert data == {"hello": "world"}


def test_content_runner_registrar():
    cfg = Config()
    workdir = Path(tempfile.mkdtemp())
    runner = ContentRunner(workdir, cfg, str(workdir))

    def ejecutar():
        return {"value": 1}

    def validar(x):
        return x

    etapa = ejecutar_etapa("C0", {"input": "x"}, cfg, workdir, ejecutar, validar, runner.cache)
    runner.registrar(etapa)
    assert "C0" in runner.etapas_completadas()
    assert (workdir / "run.json").exists()


def test_etapa_a_registro():
    etapa = Etapa("C0", {"v": 1}, "hash123", 0.5, cache_hit=False, warnings=["w1"])
    reg = etapa.a_registro()
    assert reg.etapa == "C0"
    assert reg.version == 1
    assert reg.duracion_s == 0.5
    assert reg.warnings == ["w1"]
    assert reg.cache_hit is False
