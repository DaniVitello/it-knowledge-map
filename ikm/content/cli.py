# -*- coding: utf-8 -*-
"""CLI del plano de contenido: ikm <cmd>.

Comandos: inventory (C0), parse (C1), identity (C2), graph (C3),
relations (C4), journey (C5+C6), gate (C7), derivados (C8), package (C9),
release (build|diff|publish|resume).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ikm.contracts.config import Config
from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import escribir_json_atomico, sha256_text

from .identity import asignar_uids
from .inventory import C0_inventario
from .parse import C1_parseo
from .pipeline import ContentRunner, ejecutar_etapa
from .release_build import release_build
from .publish_config import PublishConfig
from .schemas import IdentifiedConcept, Inventory, ParsedConcept

WORKDIR = Path(r"C:/Users/DGVit/Proyectos/IT Career/ikm/workdir")


def _configurar() -> tuple[Config, PublishConfig, ContentRunner]:
    pc = PublishConfig.cargar()
    cfg = Config()
    runner = ContentRunner(WORKDIR, cfg, pc.vault_root)
    return cfg, pc, runner


def cmd_inventory(args: argparse.Namespace) -> int:
    cfg, pc, runner = _configurar()

    def ejecutar():
        return C0_inventario(pc)

    def validar(x):
        return Inventory.model_validate(x.model_dump() if hasattr(x, "model_dump") else x)

    etapa = ejecutar_etapa("C0", {"vault": pc.vault_root, "config": cfg.hash_config()},
                           cfg, WORKDIR, ejecutar, validar, runner.cache)
    runner.guardar_salida("inventory", etapa.salida)
    runner.registrar(etapa)
    s = etapa.salida.summary
    print(f"inventory: {s.total} elementos | por_tipo={s.por_tipo} | con_senales={s.con_senales}")
    for k, v in s.por_origen.items():
        print(f"  {k}: {v}")
    return 0


def cmd_parse(args: argparse.Namespace) -> int:
    from .inventory import _iter_archivos

    cfg, pc, runner = _configurar()
    rutas = _iter_archivos([pc.vault_root], pc)
    notas = [(r, sha256_text(r.as_posix())[:16]) for r in rutas]

    def ejecutar():
        return C1_parseo(notas, pc)

    def validar(x):
        return [ParsedConcept.model_validate(c.model_dump()) for c in x]

    etapa = ejecutar_etapa("C1", {"notas": len(notas), "config": cfg.hash_config()},
                           cfg, WORKDIR, ejecutar, validar, runner.cache)
    out = WORKDIR / "parsed"
    out.mkdir(parents=True, exist_ok=True)
    for c in etapa.salida:
        escribir_json_atomico(out / f"{c.note_id}.json", c.model_dump())
    runner.registrar(etapa)
    total_wl = sum(len(c.wikilinks) for c in etapa.salida)
    total_marks = sum(len(c.marks) for c in etapa.salida)
    con_secciones = sum(1 for c in etapa.salida if not c.sections_missing)
    print(f"parse: {len(etapa.salida)} notas | wikilinks={total_wl} | marcas={total_marks} | "
          f"con_secciones={con_secciones} | sin_secciones={len(etapa.salida)-con_secciones}")
    return 0


def cmd_identity(args: argparse.Namespace) -> int:
    from .inventory import _iter_archivos

    cfg, pc, runner = _configurar()
    rutas = _iter_archivos([pc.vault_root], pc)
    notas = [(r, sha256_text(r.as_posix())[:16]) for r in rutas]

    def ejecutar_parse():
        return C1_parseo(notas, pc)

    def validar_parse(x):
        return [ParsedConcept.model_validate(c.model_dump()) for c in x]

    etapa_parse = ejecutar_etapa("C1", {"notas": len(notas), "config": cfg.hash_config()},
                                 cfg, WORKDIR, ejecutar_parse, validar_parse, runner.cache)
    parsed = etapa_parse.salida
    out = WORKDIR / "parsed"
    out.mkdir(parents=True, exist_ok=True)
    for c in parsed:
        escribir_json_atomico(out / f"{c.note_id}.json", c.model_dump())
    runner.registrar(etapa_parse)

    registry_path = WORKDIR / "identity-registry.yml"

    def ejecutar():
        return asignar_uids(parsed, registry_path)

    def validar(x):
        out = []
        for c in x:
            if isinstance(c, IdentifiedConcept):
                out.append(c)
            elif hasattr(c, "model_dump"):
                out.append(IdentifiedConcept.model_validate(c.model_dump()))
            else:
                out.append(IdentifiedConcept.model_validate(c))
        return out

    etapa = ejecutar_etapa("C2", {"notas": len(parsed), "config": cfg.hash_config()},
                           cfg, WORKDIR, ejecutar, validar, None)
    runner.guardar_salida("identity", etapa.salida)
    runner.registrar(etapa)
    total = len(etapa.salida)
    uids = [c.uid for c in etapa.salida]
    print(f"identity: {total} conceptos | uids_unicos={len(set(uids))} | registry={registry_path}")
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    from .inventory import _iter_archivos
    from .graph import resolver_links

    cfg, pc, runner = _configurar()
    rutas = _iter_archivos([pc.vault_root], pc)
    notas = [(r, sha256_text(r.as_posix())[:16]) for r in rutas]

    def ejecutar_parse():
        return C1_parseo(notas, pc)

    def validar_parse(x):
        return [ParsedConcept.model_validate(c.model_dump()) for c in x]

    etapa_parse = ejecutar_etapa("C1", {"notas": len(notas), "config": cfg.hash_config()},
                                 cfg, WORKDIR, ejecutar_parse, validar_parse, runner.cache)
    parsed = etapa_parse.salida
    runner.registrar(etapa_parse)

    registry_path = WORKDIR / "identity-registry.yml"
    import yaml
    reg_data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {"entries": []}
    uid_to_ruta = {e["uid"]: e["ruta"] for e in reg_data.get("entries", [])}

    def ejecutar_identity():
        return asignar_uids(parsed, registry_path)

    def validar_identity(x):
        out = []
        for c in x:
            if isinstance(c, IdentifiedConcept):
                out.append(c)
            elif hasattr(c, "model_dump"):
                out.append(IdentifiedConcept.model_validate(c.model_dump()))
            else:
                out.append(IdentifiedConcept.model_validate(c))
        return out

    etapa_id = ejecutar_etapa("C2", {"notas": len(parsed), "config": cfg.hash_config()},
                              cfg, WORKDIR, ejecutar_identity, validar_identity, None)
    conceptos = etapa_id.salida
    runner.registrar(etapa_id)

    def ejecutar():
        rels, rotos = resolver_links(parsed, conceptos, uid_to_ruta)
        return rels, rotos

    def validar(x):
        return x

    etapa = ejecutar_etapa("C3", {"notas": len(parsed), "config": cfg.hash_config()},
                           cfg, WORKDIR, ejecutar, validar, None)
    rels, rotos = etapa.salida
    runner.guardar_salida("graph", {
        "relations": [r.model_dump() if hasattr(r, "model_dump") else r for r in rels],
        "broken_links": rotos,
    })
    runner.registrar(etapa)
    print(f"graph: {len(rels)} relaciones | {len(rotos)} links rotos | {len(set(r.source_uid for r in rels))} nodos con salida")
    return 0


def cmd_package(args: argparse.Namespace) -> int:
    from .package import empaquetar, guardar_manifest
    import yaml

    cfg, pc, runner = _configurar()
    registry_path = WORKDIR / "identity-registry.yml"
    reg_data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {"entries": []}

    # Leer graph si existe
    graph_path = WORKDIR / "graph.json"
    graph_data = {}
    if graph_path.exists():
        graph_data = __import__("json").loads(graph_path.read_text(encoding="utf-8"))

    rels = graph_data.get("relations", []) if isinstance(graph_data, dict) else []
    archivos = [{"path": "graph.json", "sha256": __import__("hashlib").sha256(graph_path.read_bytes()).hexdigest()}] if graph_path.exists() else []

    manifest = empaquetar(
        workdir=WORKDIR,
        conceptos=len(reg_data.get("entries", [])),
        areas=10,
        relaciones=len(rels),
        journey_records=0,
        evidencias=0,
        chunks=0,
        archivos=archivos,
    )
    dest = guardar_manifest(WORKDIR, manifest)
    print(f"package: release_id={manifest['release_id']} | manifest={dest}")
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    sub = args.release_cmd
    if sub == "build":
        return cmd_release_build(args)
    if sub == "diff":
        print("release diff: comparar contra release anterior (pendiente)")
        return 0
    if sub == "publish":
        print("release publish: subir sitio estatico + evidencias + mover puntero (pendiente)")
        return 0
    if sub == "resume":
        print("release resume: reanudar desde etapa fallida (pendiente)")
        return 0
    return 1


def cmd_release_build(args: argparse.Namespace) -> int:
    manifest = release_build()
    print(f"release build completado: {manifest['release_id']}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="ikm", description="IT Knowledge Map v2 - plano de contenido")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inventory", help="C0: inventario y clasificacion")
    sub.add_parser("parse", help="C1: parseo de la Knowledge Base")
    sub.add_parser("identity", help="C2: identidad estable (uid + renombres)")
    sub.add_parser("graph", help="C3: grafo (resolucion de links)")
    sub.add_parser("package", help="C9: empaquetado (manifest + release_id)")
    # release subcommands
    rel_parser = sub.add_parser("release", help="Release: build|diff|publish|resume")
    rel_sub = rel_parser.add_subparsers(dest="release_cmd", required=True)
    rel_sub.add_parser("build", help="Build release")
    rel_sub.add_parser("diff", help="Diff against previous release")
    rel_sub.add_parser("publish", help="Publish release")
    rel_sub.add_parser("resume", help="Resume failed release")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "inventory":
            return cmd_inventory(args)
        if args.cmd == "parse":
            return cmd_parse(args)
        if args.cmd == "identity":
            return cmd_identity(args)
        if args.cmd == "graph":
            return cmd_graph(args)
        if args.cmd == "package":
            return cmd_package(args)
        if args.cmd == "release":
            return cmd_release(args)
    except AbortStage as e:
        print(f"ABORT[{e.causa}] etapa={e.etapa} detalle={e.detalle}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
PYEOF