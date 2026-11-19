# -*- coding: utf-8 -*-
"""Test de integracion end-to-end del pipeline."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.content.release_build import release_build


def test_release_build_end_to_end():
    """Verifica que release_build produce un manifest valido."""
    # Usar el vault real (ya existe)
    manifest = release_build()
    assert manifest is not None
    assert "release_id" in manifest
    assert manifest["counts"]["concepts"] > 0
    assert manifest["counts"]["relations"] > 0
    assert manifest["counts"]["chunks"] > 0
    assert len(manifest["files"]) > 0
