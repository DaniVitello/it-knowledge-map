# -*- coding: utf-8 -*-
"""CLI del plano de contenido: `ikm inventory` y `ikm parse`.

En L4 se suma `ikm release build|diff|publish|resume`. Aca solo C0 y C1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ikm.contracts.config import Config
from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import escribir_json_atomico, sha256_text

from .inventory import C0_inventario
from .parse import C1_parseo
from .pipeline import ContentRunner, ejecutar_etapa
from .publish_config import PublishConfig
from .schemas import Inventory, ParsedConcept

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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="ikm", description="IT Knowledge Map v2 - plano de contenido")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inventory", help="C0: inventario y clasificacion")
    sub.add_parser("parse", help="C1: parseo de la Knowledge Base")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "inventory":
            return cmd_inventory(args)
        if args.cmd == "parse":
            return cmd_parse(args)
    except AbortStage as e:
        print(f"ABORT[{e.causa}] etapa={e.etapa} detalle={e.detalle}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
