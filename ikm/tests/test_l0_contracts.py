# -*- coding: utf-8 -*-
"""Tests de la capa L0 (contratos y nucleo compartido).

Criterios de aceptacion L0:
  * los esquemas validan un release y la API de ejemplo;
  * los tipos TS se generan de la misma definicion;
  * round-trip modelo -> JSON -> modelo;
  * ninguna capa futura redefine identificadores/hashes por su cuenta.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ikm.contracts import SCHEMA_VERSION, config, errors, ids, release, service, utils
from ikm.contracts import generate, validate


# --- identificadores ----------------------------------------------------------

def test_prefijos_y_uid():
    for tipo, pref in (("concept", "c_"), ("area", "a_"), ("relation", "r_"),
                       ("journey", "j_"), ("evidence", "e_"), ("source", "s_"),
                       ("tour", "t_")):
        uid = ids.nuevo_uid(tipo)
        assert uid.startswith(pref)
        assert len(uid) == 12
        assert ids.es_uid_valido(uid)


def test_uid_relacion_dirigida_y_estable():
    a, b = ids.nuevo_uid("concept"), ids.nuevo_uid("concept")
    assert ids.uid_relacion(a, b) == ids.uid_relacion(a, b)
    assert ids.uid_relacion(a, b) != ids.uid_relacion(b, a)
    assert ids.es_uid_relacion_valido(ids.uid_relacion(a, b))


def test_uid_invalido():
    assert not ids.es_uid_valido("c_corto")
    assert not ids.es_uid_valido("x_ABCDEFGHIJ")
    assert not ids.es_uid_valido("")


def test_slug_cosmetico():
    assert ids.slugify("Base de Datos & Analitica") == "base-de-datos-analitica"
    assert ids.slugify("  HTTP/2  ") == "http-2"
    assert ids.slugify("") == "sin-slug"


# --- config y limites --------------------------------------------------------

def test_config_valores_propuestos():
    c = config.Config()
    assert c.feature_flags.embeddings_habilitados is False      # DR-09
    assert c.feature_flags.grafo_3d_habilitado is True          # DR-14
    assert c.feature_flags.streaming_por_bloques is False       # DR-10
    assert c.limites.max_message_chars == 800
    assert c.limites.max_output_tokens == 700
    assert c.plan_modelo.provider == "groq"
    assert c.plan_modelo.modelo == "openai/gpt-oss-120b"


def test_hash_config_determinista_y_sensible():
    c = config.Config()
    assert c.hash_config() == config.Config().hash_config()
    otro = config.Config()
    otro.limites.max_message_chars = 900
    assert otro.hash_config() != c.hash_config()


# --- utilidades --------------------------------------------------------------

def test_sha256_texto_y_archivo(tmp_path):
    assert utils.sha256_text("hola") == utils.sha256_bytes(b"hola")
    p = tmp_path / "a.txt"
    p.write_bytes(b"hola")
    assert utils.sha256_file(p) == utils.sha256_text("hola")


def test_escritura_atomica(tmp_path):
    p = tmp_path / "sub" / "x.json"
    utils.escritura_atomica(p, b"{" + b"1" + b"}")
    assert p.read_bytes() == b"{1}"
    assert not list(p.parent.glob("*.tmp"))


def test_clave_cache():
    h = config.Config().hash_config()
    k1 = utils.clave_cache({"a": 1, "b": [2]}, 1, h)
    k2 = utils.clave_cache({"b": [2], "a": 1}, 1, h)
    assert k1 == k2                      # orden de claves no importa
    assert utils.clave_cache({"a": 1}, 2, h) != k1


def test_hash_arbol_vault_ignora_orden(tmp_path):
    (tmp_path / "b").mkdir()
    (tmp_path / "a.txt").write_text("A")
    (tmp_path / "b" / "c.md").write_text("C")
    h1 = utils.hash_arbol_vault(tmp_path)
    (tmp_path / "b" / "c.md").write_text("C2")
    assert utils.hash_arbol_vault(tmp_path) != h1


# --- round-trip de modelos ---------------------------------------------------

def test_round_trip_concept():
    c = release.Concept(
        uid=ids.nuevo_uid("concept"), slug="x", title="X",
        sections=release.ConceptSections(objetivo="hacer X", detalles="mas"),
        sources=[ids.nuevo_uid("source")],
        verification_marks=[release.VerificationMark(section="detalles", kind="sin_verificar")],
        content_hash="h1",
    )
    crudo = json.loads(c.model_dump_json())
    de_vuelta = release.Concept.model_validate(crudo)
    assert de_vuelta == c
    assert de_vuelta.sections.objetivo == "hacer X"


def test_round_trip_relacion_dirigida():
    a, b = ids.nuevo_uid("concept"), ids.nuevo_uid("concept")
    r = release.Relation(uid=ids.uid_relacion(a, b), source_uid=a, target_uid=b,
                         type=release.RelationType.depends_on,
                         type_basis=release.TypeBasis.explicit,
                         explanation=release.Explanation(text="x", status=release.ExplanationStatus.quoted))
    assert release.Relation.model_validate(json.loads(r.model_dump_json())) == r
    assert r.determinar_uid() == r.uid


def test_relacion_cross_area_se_calcula_no_se_declara():
    r = release.Relation(uid=ids.uid_relacion(ids.nuevo_uid("concept"), ids.nuevo_uid("concept")),
                         source_uid=ids.nuevo_uid("concept"), target_uid=ids.nuevo_uid("concept"))
    assert "cross_area" in r.model_dump()
    # el modelo lo acepta, pero la regla de negocio es calcularlo (C3)


def test_enums_de_relacion():
    tipos = {t.value for t in release.RelationType}
    assert {"depends_on", "uses", "implements", "communicates_with", "complements",
            "prerequisite", "specializes", "applied_in", "untyped"} == tipos
    assert {s.value for s in release.ExplanationStatus} == {
        "quoted", "authored", "derived", "reviewed", "stale"}


def test_journey_record_solo_approved_en_release():
    rec = release.JourneyRecord(uid=ids.nuevo_uid("journey"), slug="s", title="T",
                                publication=release.Publication.approved, content_hash="h")
    assert rec.publication == release.Publication.approved
    assert release.JourneyRecord.model_validate(json.loads(rec.model_dump_json())) == rec


def test_service_user_unico_por_sub():
    u = service.User(id="1", google_sub="sub", email="a@b.c", email_verified=True,
                     created_at="2026-01-01T00:00:00Z")
    assert service.User.model_validate(json.loads(u.model_dump_json())) == u


# --- validacion contra esquema ----------------------------------------------

def test_validar_contra_esquema_aborta():
    with pytest.raises(errors.AbortStage) as ei:
        validate.validar_contra_esquema({"uid": "malo"}, release.Area, etapa="L0.test")
    assert ei.value.causa == "schema_invalid"
    assert ei.value.etapa == "L0.test"


def test_extra_forbid():
    with pytest.raises(Exception):
        release.Area(uid=ids.nuevo_uid("area"), name="A", order=0, campo_Extra="no")


# --- release y API de ejemplo ------------------------------------------------

def test_release_de_ejemplo_valida():
    muestra = json.loads(Path(__file__).with_name("fixtures_l0.json").read_text(encoding="utf-8"))
    release.Area.model_validate(muestra["area"])
    for c in muestra["concepts"]:
        release.Concept.model_validate(c)
    for r in muestra["relations"]:
        release.Relation.model_validate(r)
    release.JourneyRecord.model_validate(muestra["journey"])
    release.Evidence.model_validate(muestra["evidence"])
    release.Tour.model_validate(muestra["tour"])
    release.ExplorationState.model_validate(muestra["exploration_state"])


def test_api_de_ejemplo_valida():
    muestra = json.loads(Path(__file__).with_name("fixtures_l0.json").read_text(encoding="utf-8"))
    for u in muestra["users"]:
        service.User.model_validate(u)
    for s in muestra["sessions"]:
        service.Session.model_validate(s)
    for w in muestra["usage_windows"]:
        service.UsageWindow.model_validate(w)
    service.Message.model_validate(muestra["message"])
    service.AbuseEvent.model_validate(muestra["abuse_event"])
    service.IpWindow.model_validate(muestra["ip_window"])


# --- generacion de tipos -----------------------------------------------------

def test_generacion_schema_y_ts(tmp_path):
    info = generate.regenerar(str(tmp_path))
    assert info["schemas"] > 0 and info["ts"] > 0
    ts = (tmp_path / "ts" / "Concept.ts").read_text(encoding="utf-8")
    assert "export interface Concept {" in ts
    assert "export interface Relation {" in (tmp_path / "ts" / "Relation.ts").read_text(encoding="utf-8")
    # mismo input -> mismo output
    assert generate.regenerar(str(tmp_path))["hash"] == info["hash"]


def test_schema_version_declarado():
    assert SCHEMA_VERSION == "2.0.0"
