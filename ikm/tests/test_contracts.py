# -*- coding: utf-8 -*-
"""Tests de contratos (L0)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.contracts.ids import nuevo_uid, es_uid_valido, uid_relacion, slugify
from ikm.contracts.utils import sha256_text, clave_cache
from ikm.contracts.config import Config


def test_nuevo_uid_formato():
    uid = nuevo_uid("concept")
    assert uid.startswith("c_")
    assert len(uid) == 12  # c_ + 10 chars
    assert es_uid_valido(uid)


def test_uid_relacion_determinista():
    a = "c_AAAAAAAAAA"
    b = "c_BBBBBBBBBB"
    r1 = uid_relacion(a, b)
    r2 = uid_relacion(a, b)
    assert r1 == r2
    assert r1.startswith("r_")
    # Dirigida: (A,B) != (B,A)
    assert uid_relacion(a, b) != uid_relacion(b, a)


def test_slugify():
    assert slugify("HTTP Protocol") == "http-protocol"
    assert slugify("") == "sin-slug"


def test_sha256_text():
    h = sha256_text("hello")
    assert len(h) == 64
    assert sha256_text("hello") == sha256_text("hello")


def test_clave_cache():
    clave = clave_cache({"a": 1}, 1, "hashcfg")
    assert ":" in clave
    assert clave_cache({"a": 1}, 1, "hashcfg") == clave


def test_config_hash():
    cfg = Config()
    h1 = cfg.hash_config()
    h2 = cfg.hash_config()
    assert h1 == h2
    assert len(h1) == 64
