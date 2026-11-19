# -*- coding: utf-8 -*-
"""Tests de C2 â€” Identidad estable."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.content.identity import asignar_uids, detectar_renombre
from ikm.content.schemas import ParsedConcept, IdentifiedConcept
from ikm.contracts.ids import nuevo_uid


def _make_parsed(note_id, ruta, titulo, content_hash="abc123"):
    return ParsedConcept(
        note_id=note_id,
        ruta=ruta,
        titulo=titulo,
        content_hash=content_hash,
    )


def test_asignar_uids_nuevos():
    with tempfile.TemporaryDirectory() as tmp:
        registry = Path(tmp) / "registry.yml"
        parsed = [
            _make_parsed("n1", "/vault/a.md", "Alpha", "hash1"),
            _make_parsed("n2", "/vault/b.md", "Beta", "hash2"),
        ]
        result = asignar_uids(parsed, registry)
        assert len(result) == 2
        assert len(set(r.uid for r in result)) == 2
        assert all(r.uid.startswith("c_") for r in result)
        assert registry.exists()


def test_asignar_uids_reutiliza_por_ruta():
    with tempfile.TemporaryDirectory() as tmp:
        registry = Path(tmp) / "registry.yml"
        # Primera corrida
        parsed1 = [_make_parsed("n1", "/vault/a.md", "Alpha", "hash1")]
        r1 = asignar_uids(parsed1, registry)
        uid1 = r1[0].uid
        # Segunda corrida (misma ruta)
        parsed2 = [_make_parsed("n1", "/vault/a.md", "Alpha", "hash1")]
        r2 = asignar_uids(parsed2, registry)
        assert r2[0].uid == uid1


def test_asignar_uids_detecta_rename():
    with tempfile.TemporaryDirectory() as tmp:
        registry = Path(tmp) / "registry.yml"
        parsed1 = [_make_parsed("n1", "/vault/a.md", "Alpha", "hash1")]
        r1 = asignar_uids(parsed1, registry)
        uid1 = r1[0].uid
        # Rename: nueva ruta, mismo hash
        parsed2 = [_make_parsed("n2", "/vault/renamed.md", "Alpha", "hash1")]
        r2 = asignar_uids(parsed2, registry)
        assert r2[0].uid == uid1


def test_detectar_renombre():
    old = {"ruta": "/vault/a.md", "content_hash": "h1", "titulo": "Alpha"}
    new = _make_parsed("n1", "/vault/a.md", "Alpha", "h1")
    assert detectar_renombre(old, new) is True

    old2 = {"ruta": "/vault/a.md", "content_hash": "h1", "titulo": "Alpha"}
    new2 = _make_parsed("n2", "/vault/b.md", "Beta", "h2")
    assert detectar_renombre(old2, new2) is False
