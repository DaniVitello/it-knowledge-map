# -*- coding: utf-8 -*-
"""Tests de release loader (L2)."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.api.release.loader import cargar_release, validar_compatibilidad, listar_releases


def _crear_release(tmp: Path, release_id: str) -> Path:
    rdir = tmp / release_id
    rdir.mkdir()
    manifest = {
        "schema_version": 1,
        "release_id": release_id,
        "counts": {"concepts": 1},
        "files": [],
    }
    (rdir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return rdir


def test_cargar_release_ok():
    with tempfile.TemporaryDirectory() as tmp:
        rdir = _crear_release(Path(tmp), "rel-001")
        release = cargar_release("rel-001", rdir)
        assert release.release_id == "rel-001"


def test_cargar_release_no_existe():
    with tempfile.TemporaryDirectory() as tmp:
        try:
            cargar_release("no-existe", Path(tmp) / "no-existe")
            assert False, "should raise"
        except Exception:
            pass


def test_validar_compatibilidad():
    assert validar_compatibilidad("r1", "r1") is True
    assert validar_compatibilidad("r1", "r2") is False


def test_listar_releases():
    with tempfile.TemporaryDirectory() as tmp:
        _crear_release(Path(tmp), "rel-001")
        _crear_release(Path(tmp), "rel-002")
        releases = listar_releases(Path(tmp))
        assert "rel-001" in releases
        assert "rel-002" in releases
