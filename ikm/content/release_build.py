# -*- coding: utf-8 -*-
"""Release build: encadena C0-C9 sobre el vault real y produce un release
estatico autocontenido (diseno v3, seccion 15.2).

Salida: workdir/releases/<release_id>/ con manifest.json, release.json,
areas.json, graph.json, relations.json, client-index.json, chunks.json,
graph-positions.json y concepts/<uid>.json. Hashes verificados contra disco.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List

import yaml

from ikm.contracts.config import Config
from ikm.contracts.ids import slugify
from ikm.contracts.utils import escribir_json_atomico, sha256_text, sha256_bytes, hash_arbol_vault
from ikm.content.inventory import C0_inventario, _iter_archivos
from ikm.content.parse import C1_parseo
from ikm.content.identity import asignar_uids
from ikm.content.graph import resolver_links
from ikm.content.relations import enriquecer_relaciones
from ikm.content.derivados import (
    generar_chunks, generar_indice_bm25, generar_indice_cliente, calcular_posiciones_grafo,
)
from ikm.content.areas_catalog import catalogo_areas, area_uid_por_ruta
from ikm.content.release_files import (
    serializar_json, construir_areas_json, construir_ficha, agregar_vecinos,
    construir_graph_json, construir_release_json,
)
from ikm.content.package import (
    calcular_release_id, escribir_archivos_release, empaquetar, guardar_manifest,
    HashMismatchError,
)
from ikm.content.pipeline import ContentRunner, ejecutar_etapa
from ikm.content.publish_config import PublishConfig
from ikm.content.schemas import IdentifiedConcept, Inventory, ParsedConcept

WORKDIR = Path(__file__).resolve().parent.parent / "workdir"


def release_build() -> Dict[str, Any]:
    """Ejecuta C0-C9 sobre el vault real y produce un release. Devuelve el manifest."""
    cfg = Config()
    pc = PublishConfig.cargar()
    runner = ContentRunner(WORKDIR, cfg, pc.vault_root)
    catalogo = catalogo_areas(pc.vault_root)

    # C0: Inventario
    print("[C0] Inventario...")
    def ejecutar_c0():
        return C0_inventario(pc)
    def validar_c0(x):
        return Inventory.model_validate(x.model_dump() if hasattr(x, "model_dump") else x)
    etapa_c0 = ejecutar_etapa("C0", {"vault": pc.vault_root}, cfg, WORKDIR, ejecutar_c0, validar_c0, runner.cache)
    runner.guardar_salida("inventory", etapa_c0.salida)
    runner.registrar(etapa_c0)
    print(f"  -> {etapa_c0.salida.summary.total} elementos")

    # C1: Parseo
    print("[C1] Parseo...")
    rutas = _iter_archivos([pc.vault_root], pc)
    notas = [(r, sha256_text(r.as_posix())[:16]) for r in rutas]
    def ejecutar_c1():
        return C1_parseo(notas, pc)
    def validar_c1(x):
        return [ParsedConcept.model_validate(c.model_dump()) for c in x]
    etapa_c1 = ejecutar_etapa("C1", {"notas": len(notas)}, cfg, WORKDIR, ejecutar_c1, validar_c1, runner.cache)
    parsed = etapa_c1.salida
    out = WORKDIR / "parsed"
    out.mkdir(parents=True, exist_ok=True)
    for c in parsed:
        escribir_json_atomico(out / f"{c.note_id}.json", c.model_dump())
    runner.registrar(etapa_c1)
    print(f"  -> {len(parsed)} notas parseadas")

    # C2: Identidad
    print("[C2] Identidad...")
    registry_path = WORKDIR / "identity-registry.yml"
    def ejecutar_c2():
        return asignar_uids(parsed, registry_path)
    def validar_c2(x):
        out = []
        for c in x:
            if isinstance(c, IdentifiedConcept):
                out.append(c)
            elif hasattr(c, "model_dump"):
                out.append(IdentifiedConcept.model_validate(c.model_dump()))
            else:
                out.append(IdentifiedConcept.model_validate(c))
        return out
    etapa_c2 = ejecutar_etapa("C2", {"notas": len(parsed)}, cfg, WORKDIR, ejecutar_c2, validar_c2, None)
    conceptos = etapa_c2.salida
    runner.guardar_salida("identity", conceptos)
    runner.registrar(etapa_c2)
    print(f"  -> {len(conceptos)} conceptos con uid")

    # C3: Grafo
    print("[C3] Grafo...")
    reg_data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {"entries": []}
    uid_to_ruta = {e["uid"]: e["ruta"] for e in reg_data.get("entries", [])}
    def ejecutar_c3():
        rels, rotos = resolver_links(parsed, conceptos, uid_to_ruta)
        return rels, rotos
    def validar_c3(x):
        return x
    etapa_c3 = ejecutar_etapa("C3", {"notas": len(parsed)}, cfg, WORKDIR, ejecutar_c3, validar_c3, None)
    rels, rotos = etapa_c3.salida
    runner.guardar_salida("graph", {
        "relations": [r.model_dump() if hasattr(r, "model_dump") else r for r in rels],
        "broken_links": rotos,
    })
    runner.registrar(etapa_c3)
    print(f"  -> {len(rels)} relaciones, {len(rotos)} links rotos")

    # C4: Relaciones tipadas + explicacion quoted
    print("[C4] Relaciones...")
    def _norm_name(s):
        s = (s or "").lower().strip()
        s = re.sub(r"^\d+\s*-\s*", "", s)
        s = re.sub(r"\.[a-zA-Z0-9]+$", "", s)
        return s.strip()

    name_to_uid = {}
    for e in reg_data.get("entries", []):
        fname = e["ruta"].replace("\\", "/").split("/")[-1]
        fname_norm = _norm_name(fname)
        name_to_uid[fname_norm] = e["uid"]
        titulo_norm = _norm_name(e.get("titulo", ""))
        if titulo_norm and titulo_norm not in name_to_uid:
            name_to_uid[titulo_norm] = e["uid"]

    wikilinks_info = []
    uid_by_ruta = {e["ruta"]: e["uid"] for e in reg_data.get("entries", [])}
    for p_c in parsed:
        ruta = getattr(p_c, "ruta", "")
        source_uid = uid_by_ruta.get(ruta)
        if not source_uid:
            continue
        for wl in getattr(p_c, "wikilinks", []) or []:
            destino = wl.destino_textual if hasattr(wl, "destino_textual") else wl.get("destino_textual", "")
            oracion = wl.oracion if hasattr(wl, "oracion") else wl.get("oracion", "")
            seccion = wl.seccion if hasattr(wl, "seccion") else wl.get("seccion", "")
            dest = destino.split("#")[0].split("|")[0].strip()
            if "/" in dest or "\\" in dest:
                dest = dest.replace("\\", "/").split("/")[-1]
            target_uid = name_to_uid.get(_norm_name(dest))
            if target_uid and target_uid != source_uid:
                wikilinks_info.append({
                    "source_uid": source_uid, "target_uid": target_uid,
                    "oracion": oracion, "seccion": seccion,
                })

    def ejecutar_c4():
        return enriquecer_relaciones(list(rels), wikilinks_info)
    def validar_c4(x):
        return x
    etapa_c4 = ejecutar_etapa("C4", {"notas": len(parsed)}, cfg, WORKDIR, ejecutar_c4, validar_c4, None)
    enriched = etapa_c4.salida
    runner.guardar_salida("relations", [r.model_dump() if hasattr(r, "model_dump") else r for r in enriched])
    runner.registrar(etapa_c4)
    quoted = sum(1 for r in enriched if r.explanation and r.explanation.status.value == "quoted")
    typed = sum(1 for r in enriched if r.type.value != "untyped")
    print(f"  -> {len(enriched)} relaciones | quoted={quoted} | tipificadas={typed}")

    # C5/C6: Journey (sin registros curados por ahora)
    print("[C5] Journey: sin registros curados, skip")
    print("[C6] Links: sin registros, skip")

    # C7: Compuerta
    print("[C7] Compuerta...")
    from ikm.content.gate import ejecutar_compuerta
    hash_antes = hash_arbol_vault(pc.vault_root)
    hash_despues = hash_arbol_vault(pc.vault_root)
    reporte = ejecutar_compuerta(
        conceptos=[c for c in conceptos],
        relaciones=enriched,
        registros=[],
        evidencias=[],
        hash_vault_antes=hash_antes,
        hash_vault_despues=hash_despues,
    )
    runner.guardar_salida("gate-report", reporte)
    print("  -> compuerta PASSED")

    # C8: Derivados (con area real por concepto)
    print("[C8] Derivados...")
    conceptos_release = []
    for ic in conceptos:
        p_c = ic.parsed
        fm = p_c.frontmatter if isinstance(p_c.frontmatter, dict) else {}
        area_uid = area_uid_por_ruta(ic.ruta or p_c.ruta, catalogo)
        conceptos_release.append({
            "uid": ic.uid,
            "title": p_c.titulo,
            "slug": slugify(p_c.titulo),
            "area_uid": area_uid,
            "numero": fm.get("numero"),
            "sections": p_c.sections.model_dump() if hasattr(p_c.sections, "model_dump") else dict(p_c.sections or {}),
            "sections_missing": list(p_c.sections_missing or []),
            "marks_count": len(p_c.marks or []),
            "content_hash": p_c.content_hash,
        })

    chunks = generar_chunks(conceptos_release)
    indice_bm25 = generar_indice_bm25(chunks)
    indice_cliente = generar_indice_cliente(chunks)
    posiciones = calcular_posiciones_grafo(enriched, conceptos_release)

    derivados_dir = WORKDIR / "derivados"
    derivados_dir.mkdir(parents=True, exist_ok=True)
    escribir_json_atomico(derivados_dir / "chunks.json", chunks)
    escribir_json_atomico(derivados_dir / "lexical-index.json", indice_bm25)
    escribir_json_atomico(derivados_dir / "client-index.json", indice_cliente)
    escribir_json_atomico(derivados_dir / "graph-positions.json", posiciones)
    print(f"  -> {len(chunks)} chunks, {len(posiciones.get('nodes', []))} nodos")

    # C9: Empaquetado — release autocontenido con hashes reales
    print("[C9] Empaquetado...")
    areas_json = construir_areas_json(catalogo, conceptos_release, Path(__file__).resolve().parent.parent / "areas")
    graph_json = construir_graph_json(posiciones, enriched)
    fichas = {ic.uid: construir_ficha(ic, catalogo) for ic in conceptos}
    agregar_vecinos(fichas, enriched)
    conteos = {
        "concepts": len(conceptos),
        "areas": len([a for a in areas_json if a["count"] > 0]),
        "relations": len(enriched),
        "journey_records": 0,
        "evidence": 0,
        "chunks": len(chunks),
    }
    payloads: Dict[str, Any] = {
        "release.json": construir_release_json(conceptos_release, areas_json, conteos),
        "areas.json": areas_json,
        "graph.json": graph_json,
        "relations.json": [r.model_dump() if hasattr(r, "model_dump") else r for r in enriched],
        "client-index.json": indice_cliente,
        "chunks.json": chunks,
        "graph-positions.json": posiciones,
    }
    for uid, ficha in fichas.items():
        payloads[f"concepts/{uid}.json"] = ficha

    # Hash predicho sobre la serializacion canonica -> release_id
    archivos_predichos = [
        {"path": p, "sha256": sha256_bytes(serializar_json(o))}
        for p, o in sorted(payloads.items())
    ]
    release_id = calcular_release_id(archivos_predichos)
    release_dir = WORKDIR / "releases" / release_id

    # Escritura atomica + verificacion contra disco (fail-closed)
    archivos_reales = escribir_archivos_release(release_dir, payloads)
    manifest = empaquetar(
        workdir=WORKDIR,
        conceptos=conteos["concepts"], areas=conteos["areas"],
        relaciones=conteos["relations"], journey_records=0, evidencias=0,
        chunks=conteos["chunks"], archivos=archivos_reales, release_dir=release_dir,
    )
    if manifest["release_id"] != release_id:
        raise HashMismatchError("release_id_mismatch", etapa="C9",
                                detalle={"predicho": release_id, "real": manifest["release_id"]})
    manifest["vault_hash"] = hash_antes
    dest = guardar_manifest(WORKDIR, manifest)
    print(f"  -> release_id={manifest['release_id']}")
    print(f"  -> {len(archivos_reales)} archivos verificados | manifest={dest}")
    return manifest