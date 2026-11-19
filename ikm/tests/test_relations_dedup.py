# -*- coding: utf-8 -*-
"""Tests de colapsar_reciprocas (C4): conexiones unicas sin duplicados."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ikm.contracts.release import Explanation, ExplanationStatus, Relation, RelationType, TypeBasis
from ikm.contracts.ids import uid_relacion
from ikm.content.relations import colapsar_reciprocas

A = "c_AAAAAAAAAA"
B = "c_BBBBBBBBBB"
C = "c_CCCCCCCCCC"


def _rel(s, t, tipo=RelationType.untyped, texto=None):
    return Relation(
        uid=uid_relacion(s, t), source_uid=s, target_uid=t, type=tipo,
        type_basis=TypeBasis.none if tipo == RelationType.untyped else TypeBasis.explicit,
        explanation=Explanation(text=texto, status=ExplanationStatus.quoted) if texto else None,
        cross_area=False,
    )


def test_par_reciproco_colapsa_a_uno():
    out = colapsar_reciprocas([_rel(A, B, texto="A lista B"), _rel(B, A, texto="B lista A")])
    assert len(out) == 1


def test_direccion_canonica_min_a_max():
    out = colapsar_reciprocas([_rel(B, A), _rel(A, B)])
    assert out[0].source_uid == A and out[0].target_uid == B
    assert out[0].uid == uid_relacion(A, B)


def test_no_reciproca_se_conserva():
    out = colapsar_reciprocas([_rel(A, B), _rel(A, C)])
    assert len(out) == 2


def test_tipo_tipado_prefiere_sobre_untyped():
    out = colapsar_reciprocas([_rel(A, B, RelationType.untyped), _rel(B, A, RelationType.uses)])
    assert out[0].type == RelationType.uses


def test_explicacion_con_texto_se_conserva():
    out = colapsar_reciprocas([_rel(A, B, texto=None), _rel(B, A, texto="explicacion")])
    assert out[0].explanation is not None
    assert out[0].explanation.text == "explicacion"


def test_determinismo():
    rels = [_rel(B, A), _rel(A, B), _rel(A, C), _rel(C, A)]
    r1 = colapsar_reciprocas(list(rels))
    r2 = colapsar_reciprocas(list(reversed(rels)))
    assert [(r.source_uid, r.target_uid, r.uid) for r in r1] == [(r.source_uid, r.target_uid, r.uid) for r in r2]


def test_self_loop_se_descarta():
    out = colapsar_reciprocas([_rel(A, A), _rel(A, B)])
    assert len(out) == 1
    assert out[0].target_uid == B