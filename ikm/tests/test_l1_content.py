# -*- coding: utf-8 -*-
"""Tests de la capa L1 (C0 inventario + C1 parseo).

Criterios de aceptacion (disenio 22.2 KB):
  * cada concepto del release proviene de una nota del inventario;
  * el vault no cambia (hashes);
  * marcas de verificacion registradas por seccion;
  * WikiLinks con posicion y oracion.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ikm.content.inventory import C0_inventario
from ikm.content.parse import C1_parseo, _canon_seccion, _zonas_de
from ikm.content.publish_config import PublishConfig, ZONAS_SIEMPRE_EXCLUIDAS
from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import hash_arbol_vault

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "vault"


@pytest.fixture()
def cfg():
    return PublishConfig(vault_root=str(FIX), include=["**/*.md"],
                         exclude=["**/00 - *ndice*.md", "**/00 - *Index*.md"])


# --- C0 ----------------------------------------------------------------------

def test_c0_inventaria_y_clasifica_private(cfg):
    inv = C0_inventario(cfg)
    assert inv.summary.total == 6
    assert inv.summary.por_tipo == {"markdown": 6}
    assert inv.summary.por_clasificacion == {"private": 6}
    assert all(i.clasificacion == "private" for i in inv.items)


def test_c0_no_modifica_el_vault(cfg):
    antes = hash_arbol_vault(cfg.vault_root)
    C0_inventario(cfg)
    assert hash_arbol_vault(cfg.vault_root) == antes


def test_c0_detecta_senales(cfg):
    inv = C0_inventario(cfg)
    gamma = next(i for i in inv.items if "Gamma" in i.hash_de_ruta or i.id_temporal)
    por_archivo = {i.sha256: i for i in inv.items}
    # localizar Gamma por su contenido
    kinds = set()
    for i in inv.items:
        kinds |= {s.kind for s in i.signals}
    assert "secret_pattern" in kinds      # AKIA...
    assert "email" in kinds
    assert "absolute_path" in kinds
    assert "private_url" in kinds


def test_c0_excluye_indices(cfg):
    inv = C0_inventario(cfg)
    assert inv.summary.total == 6     # 7 notas - 2 indices


def test_c0_config_invalida():
    with pytest.raises(AbortStage):
        PublishConfig.cargar("/ruta/que/no/existe.yml")


# --- C1 ----------------------------------------------------------------------

def test_c1_parsea_nota_completa(cfg):
    nota = FIX / "01 - Area A" / "01 - Alpha.md"
    parsed = C1_parseo([(nota, "t1")], cfg)[0]
    assert parsed.titulo == "Alpha"
    assert parsed.sections.objetivo.startswith("Entender Alpha")
    assert parsed.sections.ejemplo_minimo is not None
    assert parsed.sections_missing == []


def test_c1_reporta_secciones_ausentes(cfg):
    nota = FIX / "01 - Area A" / "02 - Beta.md"
    parsed = C1_parseo([(nota, "t2")], cfg)[0]
    assert parsed.sections_missing == list(PublishConfig().secciones_contrato)
    assert parsed.sections.objetivo is None


def test_c1_variantes_de_titulo(cfg):
    assert _canon_seccion("Ideas clave") == "ideas_clave"
    assert _canon_seccion("Como funciona") == "como_funciona"
    assert _canon_seccion("Ejemplo minimo") == "ejemplo_minimo"
    assert _canon_seccion("Preguntas de repaso") == "preguntas_repaso"
    assert _canon_seccion("Esto no es una seccion") is None


def test_c1_wikilinks_con_oracion_y_exclusiones(cfg):
    nota = FIX / "01 - Area A" / "01 - Alpha.md"
    parsed = C1_parseo([(nota, "t3")], cfg)[0]
    destinos = {w.destino_textual for w in parsed.wikilinks}
    # incluye los de Relacionados y los del bloque AI
    assert any("02 - Beta" in d for d in destinos)
    assert any("CANARY" in d for d in destinos)
    # excluye navegacion (blockquote, pie) y Mis notas
    for w in parsed.wikilinks:
        assert "Indice" not in w.destino_textual
        assert w.zona != "mis_notas"
        assert w.zona != "navegacion"
        assert w.zona != "pie"
    # el wikilink dentro del bloque de codigo NO cuenta
    assert not any("Oculto" in d for d in destinos)
    # cada wikilink tiene oracion
    assert all(w.oracion for w in parsed.wikilinks)


def test_c1_marcas_por_seccion(cfg):
    alpha = C1_parseo([(FIX / "01 - Area A" / "01 - Alpha.md", "t4")], cfg)[0]
    assert any(m.kind == "sin_verificar" for m in alpha.marks)
    gamma = C1_parseo([(FIX / "01 - Area A" / "03 - Gamma.md", "t5")], cfg)[0]
    assert any(m.kind == "verificar" for m in gamma.marks)


def test_c1_fuentes(cfg):
    gamma = C1_parseo([(FIX / "01 - Area A" / "03 - Gamma.md", "t6")], cfg)[0]
    assert any("localhost" in s.url for s in gamma.sources)


def test_c1_zonas_publicables_y_excluidas(cfg):
    nota = FIX / "01 - Area A" / "01 - Alpha.md"
    texto = nota.read_text(encoding="utf-8")
    _, cuerpo, _ = __import__("ikm.content.parse", fromlist=["_extraer_frontmatter"])._extraer_frontmatter(texto)
    zonas = _zonas_de(cuerpo, cfg)
    por_kind = {z.kind.value: z for z in zonas}
    assert por_kind["bloque_ai"].publicable is True
    assert por_kind["relacionados"].publicable is True
    assert por_kind["mis_notas"].publicable is False
    assert por_kind["navegacion"].publicable is False
    assert "mis_notas" in ZONAS_SIEMPRE_EXCLUIDAS


def test_c1_frontmatter_invalido_revienta(tmp_path, cfg):
    mala = tmp_path / "mala.md"
    mala.write_text("---\ntitle: [sin cerrar\n---\n# Hola\n", encoding="utf-8")
    with pytest.raises(AbortStage) as ei:
        C1_parseo([(mala, "t7")], cfg)
    assert ei.value.causa == "invalid_frontmatter"


def test_c1_titulo_no_resoluble_revienta(tmp_path, cfg):
    rara = tmp_path / "rara.md"
    rara.write_text("---\narea: X\n---\n## Que abarca\n- nada\n", encoding="utf-8")
    with pytest.raises(AbortStage) as ei:
        C1_parseo([(rara, "t8")], cfg)
    assert ei.value.causa == "unresolvable_title"


def test_c1_round_trip(cfg):
    nota = FIX / "01 - Area A" / "01 - Alpha.md"
    parsed = C1_parseo([(nota, "t9")], cfg)[0]
    de_vuelta = type(parsed).model_validate(json.loads(parsed.model_dump_json()))
    assert de_vuelta == parsed


def test_c1_ideas_clave_es_seccion_canonica(cfg):
    nota = FIX / "01 - Area A" / "04 - Ideas.md"
    parsed = C1_parseo([(nota, "t10")], cfg)[0]
    assert parsed.sections.ideas_clave is not None
    assert "Punto" in parsed.sections.ideas_clave
    assert parsed.sections_missing == []


def test_c1_subtitulos_no_truncan_secciones(cfg):
    nota = FIX / "01 - Area A" / "04 - Ideas.md"
    parsed = C1_parseo([(nota, "t11")], cfg)[0]
    # los subtitulos ## Uso / ## Metricas quedan dentro de Detalles
    assert "Subtitulo interno" in parsed.sections.detalles
    assert "Otro subtitulo" in parsed.sections.detalles
    # el codigo con # comentario no abre seccion
    assert "Variables y tipos" in parsed.sections.ejemplo_minimo
    assert parsed.sections.errores_comunes is not None


def test_c1_canon_ideas_clave():
    assert _canon_seccion("Ideas clave") == "ideas_clave"
    assert _canon_seccion("Ideas Clave") == "ideas_clave"
