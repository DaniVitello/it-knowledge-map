"""Tests de Capa D (contexto por area, areas.py) sin red.

Cobertura obligatoria: las 10 areas de EXPECTED_AREAS tienen yaml y cargan.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import areas as A
import registry as R
from models import Volatility

TMP = Path(__file__).parent / ".tmp-workdir-areas"


def _reset():
    if TMP.exists():
        shutil.rmtree(TMP)


# ---------------------------------------------------------------------------
# Cobertura: las 10 areas de EXPECTED_AREAS
# ---------------------------------------------------------------------------


def test_expected_areas_son_10():
    assert len(A.EXPECTED_AREAS) == 10


def test_expected_areas_ordenadas_y_unicas():
    assert A.EXPECTED_AREAS == sorted(set(A.EXPECTED_AREAS))


def test_cada_area_esperada_tiene_yaml_en_disco():
    # cobertura de las 10 areas: si falta un yaml, falla
    slugs = {p.stem for p in A.AREAS_DIR.glob("*.yaml")}
    for area in A.EXPECTED_AREAS:
        assert A.slugify_area(area) in slugs, f"sin yaml: {area}"


def test_load_areas_devuelve_las_10_areas():
    areas = A.load_areas()
    nombres = {areas[k].name for k in areas if isinstance(areas[k].name, str)}
    nombres_cargados = {ctx.name for ctx in areas.values()}
    # indexado por nombre (ci) y por slug: los valores cubren exactamente 10 areas
    areas_unicas = {}
    for ctx in areas.values():
        areas_unicas[ctx.name] = ctx
    assert len(areas_unicas) == 10, f"cargadas {len(areas_unicas)} areas, se esperaban 10"
    for expected in A.EXPECTED_AREAS:
        # match del nombre case-insensitive
        assert any(u.lower() == expected.lower() for u in areas_unicas), \
            f"area no cargada: {expected}"
    assert nombres == nombres_cargados  # sanity: coleccion consistente


def test_cada_area_cargada_es_areacontext_completa():
    for ctx in {c.name: c for c in A.load_areas().values()}.values():
        assert ctx.name
        assert isinstance(ctx, A.AreaContext)
        assert ctx.path is not None
        assert isinstance(ctx.context_framing, str)
        assert isinstance(ctx.context_questions, list)
        assert isinstance(ctx.professional_roles, list)
        assert ctx.default_volatility in (Volatility.STABLE, Volatility.SEMI_STABLE, Volatility.DYNAMIC)
        assert isinstance(ctx.volatility_overrides, dict)


def test_cada_area_resuelve_por_nombre_y_slug():
    for area in A.EXPECTED_AREAS:
        por_nombre = A.load_area(area)
        por_slug = A.load_area(A.slugify_area(area))
        assert por_nombre is not None, f"load_area no resuelve: {area}"
        assert por_slug is not None, f"load_area no resuelve slug: {area}"
        assert por_nombre.name == por_slug.name


# ---------------------------------------------------------------------------
# slugify_area
# ---------------------------------------------------------------------------


def test_slugify_variantes_colapsan_al_mismo_slug():
    assert A.slugify_area("Database / Data Analytics") == "database-data-analytics"
    assert A.slugify_area("Database & Data Analytics") == "database-data-analytics"
    assert A.slugify_area("Networking / Internet") == "networking-internet"
    assert A.slugify_area("UX / UI") == "ux-ui"


def test_slugify_normaliza_acentos_y_espacios():
    assert A.slugify_area("Café  Con Leche") == "cafe-con-leche"
    assert A.slugify_area("  --x--  ") == "x"


# ---------------------------------------------------------------------------
# Carga y validacion de yaml
# ---------------------------------------------------------------------------


def _write_yaml(tmp: Path, name: str, data: str) -> Path:
    tmp.mkdir(parents=True, exist_ok=True)
    p = tmp / f"{name}.yaml"
    p.write_text(data, encoding="utf-8")
    return p


def test_load_area_yaml_ok():
    p = _write_yaml(TMP, "demo", (
        "area: Demo / Area\n"
        "context_framing: Framing\n"
        "context_questions:\n  - Que carpeta?\n"
        "professional_roles:\n  - demo-dev\n"
        "style_example: Estilo\n"
        "response_mode: FAQ\n"
        "preferred_domains:\n  - example.com\n"
        "seed_urls:\n  - https://example.com/doc\n"
        "default_volatility: dynamic\n"
        "volatility_overrides:\n  x: stable\n"
    ))
    ctx = A.load_area_yaml(p)
    assert ctx.name == "Demo / Area"
    assert ctx.context_framing == "Framing"
    assert ctx.context_questions == ["Que carpeta?"]
    assert ctx.professional_roles == ["demo-dev"]
    assert ctx.response_mode == "faq"
    assert ctx.preferred_domains == ["example.com"]
    assert ctx.seed_urls == ["https://example.com/doc"]
    assert ctx.default_volatility is Volatility.DYNAMIC
    assert ctx.volatility_overrides == {"x": "stable"}
    _reset()


def test_load_area_yaml_sin_area_lanza():
    p = _write_yaml(TMP, "roto", "style_example: hola\n")
    try:
        A.load_area_yaml(p)
        raise AssertionError("debia lanzar AreaConfigError")
    except A.AreaConfigError:
        pass
    finally:
        _reset()


def test_load_area_yaml_mapping_invalido_lanza():
    p = _write_yaml(TMP, "lista", "- a\n- b\n")
    try:
        A.load_area_yaml(p)
        raise AssertionError("debia lanzar AreaConfigError")
    except A.AreaConfigError:
        pass
    finally:
        _reset()


def test_load_area_yaml_tipo_invalido_lanza():
    p = _write_yaml(TMP, "malroles", "area: X\nprofessional_roles: no-soy-lista\n")
    try:
        A.load_area_yaml(p)
        raise AssertionError("debia lanzar AreaConfigError")
    except A.AreaConfigError:
        pass
    finally:
        _reset()


def test_load_area_yaml_volatility_invalida_lanza():
    p = _write_yaml(TMP, "malvol", "area: X\ndefault_volatility: ultra\n")
    try:
        A.load_area_yaml(p)
        raise AssertionError("debia lanzar AreaConfigError")
    except A.AreaConfigError:
        pass
    finally:
        _reset()


def test_load_area_yaml_yaml_invalido_lanza():
    p = _write_yaml(TMP, "malyaml", "area: [unbalanced\n")
    try:
        A.load_area_yaml(p)
        raise AssertionError("debia lanzar AreaConfigError")
    except A.AreaConfigError:
        pass
    finally:
        _reset()


def test_load_area_inexistente_devuelve_none():
    assert A.load_area("AreaQueNoExiste") is None
    assert A.load_area("") is None
    assert A.load_area(None) is None


# ---------------------------------------------------------------------------
# resolve_for_concept: merge de prioridad
# ---------------------------------------------------------------------------


def test_resolve_sin_nada_usa_defaults():
    res = A.resolve_for_concept("c1", "AreaInexistente")
    assert res["area_yaml"] is None
    assert res["volatility"] is Volatility.SEMI_STABLE
    assert res["professional_roles"] == []
    assert res["context_framing"] == ""


def test_resolve_frontend_yaml_real():
    res = A.resolve_for_concept("concepto-x", "Frontend")
    assert res["area_yaml"].name == "Frontend"
    # roles y dominios salen del yaml real del area
    assert res["professional_roles"] == ["profesional senior de Frontend"]
    assert "developer.mozilla.org" in res["preferred_domains"]
    # la volatilidad default del yaml
    assert res["volatility"] is Volatility.SEMI_STABLE


def test_resolve_prioridad_override_concepto_sobre_yaml(tmp_path=None):
    TMP.mkdir(parents=True, exist_ok=True)
    p = _write_yaml(TMP, "frontend", (
        "area: Frontend\n"
        "professional_roles:\n  - yaml-role\n"
        "preferred_domains:\n  - yaml.com\n"
        "seed_urls:\n  - https://yaml.com/s\n"
        "context_framing: yaml-framing\n"
        "default_volatility: semi_stable\n"
    ))
    config = {"concepts": {"concepto-1": {
        "professional_roles": ["override-role"],
        "preferred_domains": ["override.com"],
        "volatility": "dynamic",
        "context_framing": "override-framing",
    }}}
    res = A.resolve_for_concept("concepto-1", "Frontend", config=config, areas_dir=TMP)
    assert res["professional_roles"] == ["override-role"]
    assert res["preferred_domains"] == ["override.com"]
    assert res["volatility"] is Volatility.DYNAMIC
    assert res["context_framing"] == "override-framing"
    _reset()


def test_resolve_volatility_override_del_area_por_concepto():
    TMP.mkdir(parents=True, exist_ok=True)
    _write_yaml(TMP, "frontend", (
        "area: Frontend\nprofessional_roles:\n  - r\n"
        "default_volatility: semi_stable\n"
        "volatility_overrides:\n  http: dynamic\n"
    ))
    res = A.resolve_for_concept("http", "Frontend", areas_dir=TMP)
    assert res["volatility"] is Volatility.DYNAMIC
    # otro concepto sin override: default del yaml
    res2 = A.resolve_for_concept("css", "Frontend", areas_dir=TMP)
    assert res2["volatility"] is Volatility.SEMI_STABLE
    _reset()


def test_resolve_fallback_tags_frontmatter_sin_yaml():
    res = A.resolve_for_concept("c", "AreaYamlQueNoExiste",
                                frontmatter={"tags": ["dynamic"]})
    assert res["volatility"] is Volatility.DYNAMIC
    res2 = A.resolve_for_concept("c", "AreaYamlQueNoExiste",
                                 frontmatter={"tags": ["#stable"]})
    assert res2["volatility"] is Volatility.STABLE


def test_resolve_defaults_de_strategy_se_agregan_sin_duplicar():
    TMP.mkdir(parents=True, exist_ok=True)
    _write_yaml(TMP, "frontend", (
        "area: Frontend\nprofessional_roles:\n  - r\n"
        "preferred_domains:\n  - yaml.com\n"
        "seed_urls:\n  - https://yaml.com/s\n"
    ))
    config = {"strategy": {"preferred_domains": ["yaml.com", "global.com"],
                           "seed_urls": ["https://global.com/g"]}}
    res = A.resolve_for_concept("c", "Frontend", config=config, areas_dir=TMP)
    assert res["preferred_domains"] == ["yaml.com", "global.com"]
    assert res["seed_urls"] == ["https://yaml.com/s", "https://global.com/g"]
    _reset()


def test_resolve_frontmatter_llena_huecos():
    res = A.resolve_for_concept(
        "c", "AreaYamlQueNoExiste",
        frontmatter={"professional_roles": ["fm-role"],
                     "preferred_domains": ["fm.com"],
                     "seed_urls": ["https://fm.com/s"],
                     "context_framing": "fm-framing",
                     "style_example": "fm-style",
                     "response_mode": "FAQ"})
    assert res["professional_roles"] == ["fm-role"]
    assert res["preferred_domains"] == ["fm.com"]
    assert res["seed_urls"] == ["https://fm.com/s"]
    assert res["context_framing"] == "fm-framing"
    assert res["style_example"] == "fm-style"
    assert res["response_mode"] == "faq"


# ---------------------------------------------------------------------------
# Integracion con registry (Capa D usa areas/<area>.yaml como fuente de verdad)
# ---------------------------------------------------------------------------

VAULT_NOTE = """---
title: HTTP
area: Frontend
tags: [dynamic]
---

# HTTP

## Que abarca
- Protocolo de transferencia

## Relacionados
- [[Cliente-Servidor]]

<!-- ai:start -->
<!-- ai:end -->
"""


def test_registry_read_concept_usa_area_yaml():
    _reset()
    vault = TMP / "vault"
    (vault / "Frontend").mkdir(parents=True, exist_ok=True)
    note = vault / "Frontend" / "HTTP.md"
    note.write_text(VAULT_NOTE, encoding="utf-8")
    meta = R.read_concept(note, vault)
    assert meta.area == "Frontend"
    # el yaml del area provee roles y dominios (fuente de verdad de Capa D)
    ctx = A.load_area("Frontend")
    assert ctx.professional_roles == meta.professional_roles
    assert meta.preferred_domains == ctx.preferred_domains
    assert meta.seed_urls == ctx.seed_urls
    # tags dynamic NO gana si hay yaml (prioridad yaml > frontmatter)
    assert meta.volatility == ctx.default_volatility
    _reset()


def test_registry_read_concept_area_sin_yaml_rol_fallback():
    _reset()
    vault = TMP / "vault"
    (vault / "AreaRara").mkdir(parents=True, exist_ok=True)
    note = vault / "AreaRara" / "X.md"
    note.write_text(VAULT_NOTE.replace("Frontend", "AreaRara"), encoding="utf-8")
    meta = R.read_concept(note, vault)
    assert meta.volatility == Volatility.DYNAMIC  # sin yaml: gana tag
    assert meta.professional_roles == ["arearara-dev"]  # fallback legado
    _reset()


def test_areacontext_defaults_y_schema_version():
    ctx = A.AreaContext(name="X")
    assert ctx.schema_version == A.SCHEMA_VERSION == "1.0.0"
    assert ctx.default_volatility is Volatility.SEMI_STABLE
    assert ctx.professional_roles == []
    assert ctx.volatility_overrides == {}


# ---------------------------------------------------------------------------
# Integracion con sintesis: build_prompt inyecta el contexto del area
# ---------------------------------------------------------------------------

from models import ConceptMeta  # noqa: E402
from synthesis import build_prompt  # noqa: E402

SYN_CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("x/Internet.md"),
)


def test_prompt_inyecta_rol_y_contexto_del_area():
    p = build_prompt(SYN_CONCEPT, {"answers": []}, {"sources": []})
    # rol real del yaml, no roles inventados
    assert "profesional senior de Frontend" in p
    # context_framing del yaml
    assert "desarrollo frontend" in p.lower()
    assert "CONTEXTO PROFESIONAL" in p
    # estilo y modo del yaml
    assert "fragmento de codigo corto" in p
    assert "En formato de listas" in p or "en formato de listas" in p.lower()


def test_prompt_ya_no_usa_experto_generico():
    p = build_prompt(SYN_CONCEPT, {"answers": []}, {"sources": []})
    assert "Sos un experto en Frontend" not in p


def test_prompt_incluye_preguntas_de_contexto():
    p = build_prompt(SYN_CONCEPT, {"answers": []}, {"sources": []})
    assert "dia a dia del desarrollo frontend" in p


def test_prompt_con_contexto_explicito_pisa_el_yaml():
    ctx = {"professional_roles": ["ingeniero de producto senior"],
           "context_framing": "framing custom",
           "context_questions": ["pregunta custom?"],
           "style_example": "ejemplo custom",
           "response_mode": "libre"}
    p = build_prompt(SYN_CONCEPT, {"answers": []}, {"sources": []}, area_context=ctx)
    assert "ingeniero de producto senior" in p
    assert "framing custom" in p
    assert "pregunta custom?" in p


if __name__ == "__main__":
    _reset()
    fallos = 0
    for name, fn in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        try:
            fn()
            print(f"OK   {name}")
        except AssertionError as exc:
            fallos += 1
            print(f"FAIL {name}: {exc}")
        except Exception as exc:
            fallos += 1
            print(f"ERR  {name}: {type(exc).__name__}: {exc}")
    _reset()
    print("TODOS OK" if fallos == 0 else f"{fallos} fallos")
    raise SystemExit(1 if fallos else 0)
