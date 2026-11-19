# -*- coding: utf-8 -*-
"""Tests de C3 â€” Grafo."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.content.graph import resolver_links, _normalizar_nombre
from ikm.content.schemas import ParsedConcept, WikiLink
from ikm.content.identity import asignar_uids


def _make_parsed(note_id, ruta, titulo, wikilinks=None):
    pc = ParsedConcept(
        note_id=note_id,
        ruta=ruta,
        titulo=titulo,
        content_hash="hash_" + note_id,
        wikilinks=wikilinks or [],
    )
    return pc


def test_normalizar_nombre():
    assert _normalizar_nombre("01 - Programming Fundamentals.md") == "programming fundamentals"
    assert _normalizar_nombre("HTTP") == "http"
    assert _normalizar_nombre("03 - IPv4 - IPv6.md") == "ipv4 - ipv6"


def test_resolver_links_basico():
    with tempfile.TemporaryDirectory() as tmp:
        reg = Path(tmp) / "reg.yml"
        parsed = [
            _make_parsed("n1", "/vault/a.md", "Alpha", [
                WikiLink(destino_textual="Beta", seccion="Relacionados", oracion="usa Beta", offset=0, zona="relacionados"),
            ]),
            _make_parsed("n2", "/vault/b.md", "Beta", []),
        ]
        conceptos = asignar_uids(parsed, reg)
        rels, rotos = resolver_links(parsed, conceptos, {})
        assert len(rels) == 1
        assert rels[0].source_uid != rels[0].target_uid
        assert len(rotos) == 0


def test_resolver_links_roto():
    with tempfile.TemporaryDirectory() as tmp:
        reg = Path(tmp) / "reg.yml"
        parsed = [
            _make_parsed("n1", "/vault/a.md", "Alpha", [
                WikiLink(destino_textual="NoExiste", seccion="Relacionados", oracion="link roto", offset=0, zona="relacionados"),
            ]),
        ]
        conceptos = asignar_uids(parsed, reg)
        rels, rotos = resolver_links(parsed, conceptos, {})
        assert len(rels) == 0
        assert len(rotos) == 1
        assert rotos[0] == "NoExiste"


def test_resolver_links_self_link_ignorado():
    with tempfile.TemporaryDirectory() as tmp:
        reg = Path(tmp) / "reg.yml"
        parsed = [
            _make_parsed("n1", "/vault/a.md", "Alpha", [
                WikiLink(destino_textual="Alpha", seccion="Relacionados", oracion="self", offset=0, zona="relacionados"),
            ]),
        ]
        conceptos = asignar_uids(parsed, reg)
        rels, rotos = resolver_links(parsed, conceptos, {})
        assert len(rels) == 0


def test_cross_area():
    with tempfile.TemporaryDirectory() as tmp:
        reg = Path(tmp) / "reg.yml"
        parsed = [
            _make_parsed("n1", "/vault/a.md", "Alpha", [
                WikiLink(destino_textual="Beta", seccion="Relacionados", oracion="usa Beta", offset=0, zona="relacionados"),
            ]),
            _make_parsed("n2", "/vault/b.md", "Beta", []),
        ]
        # Set area in frontmatter
        parsed[0].frontmatter = {"area": "Frontend"}
        parsed[1].frontmatter = {"area": "Backend"}
        conceptos = asignar_uids(parsed, reg)
        rels, rotos = resolver_links(parsed, conceptos, {})
        assert len(rels) == 1
        assert rels[0].cross_area is True
