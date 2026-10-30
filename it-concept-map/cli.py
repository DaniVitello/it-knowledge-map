"""Capa 9 - CLI del pipeline (interfaz para humanos y agentes).

Comandos: run, status, list, reset, dry-run.
Integracion con runner.py y todas las capas.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import state
import runner as RN
from models import ConceptMeta


def _load_cfg(args):
    import yaml
    cfg_path = getattr(args, "config", None) or "config.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if getattr(args, "workdir", None):
        cfg["workdir"] = args.workdir
    if getattr(args, "vault", None):
        cfg["vault_path"] = args.vault
    return cfg


def _load_concepts(cfg):
    import registry
    try:
        return registry.load_concepts(cfg["vault_path"], cfg)
    except Exception:
        return []


def cmd_run(args):
    cfg = _load_cfg(args)
    concepts = _load_concepts(cfg)
    if args.concept:
        concepts = [c for c in concepts if c.id == args.concept or args.concept in c.id]
        if not concepts:
            print(f"Concepto no encontrado: {args.concept}")
            return 1
    elif args.area:
        concepts = [c for c in concepts if c.area == args.area]
    # limit
    if args.limit:
        concepts = concepts[:args.limit]
    llm = None
    if getattr(args, "llm", None):
        # placeholder: llm provided externally
        pass
    if getattr(args, "force_phase", None):
        args.force = True
    runner = RN.Runner(cfg=cfg, llm=llm, workdir=cfg.get("workdir", "workdir"))
    if len(concepts) == 1:
        rep = asyncio.run(runner.run_concept(concepts[0], force=args.force, dry_run=args.dry_run))
        print(f"{rep.concept_id}: {rep.status} ({rep.duration_ms}ms) phases={rep.phases_completed}")
        if rep.error:
            print(f"  error: {rep.error}")
        return 0 if rep.status == "completed" else 1
    else:
        batch = asyncio.run(runner.run_batch(concepts, force=args.force, dry_run=args.dry_run))
        print(f"Total: {batch.total} | completed: {batch.completed} | failed: {batch.failed} | skipped: {batch.skipped}")
        for r in batch.results:
            print(f"  {r.concept_id}: {r.status}")
        return 0 if batch.failed == 0 else 1


def cmd_status(args):
    cfg = _load_cfg(args)
    workdir = cfg.get("workdir", "workdir")
    st = state.load_state(args.concept, workdir=workdir)
    if st is None:
        print(f"Sin estado para: {args.concept}")
        return 1
    print(f"concept_id: {st.concept_id}")
    print(f"status: {st.status.value}")
    print(f"checkpoint: {st.checkpoint}")
    print(f"retries: {st.retries}")
    if st.error:
        print(f"last_error: {st.error}")
    if st.phase_data:
        print(f"phase_data: {json.dumps(st.phase_data, ensure_ascii=False)}")
    return 0


def cmd_list(args):
    cfg = _load_cfg(args)
    concepts = _load_concepts(cfg)
    workdir = cfg.get("workdir", "workdir")
    status_filter = args.status
    for c in concepts:
        st = state.load_state(c.id, workdir=workdir)
        st_status = st.status.value if st else "pending"
        if status_filter and st_status != status_filter:
            continue
        print(f"{c.id} | {c.title} | {c.area} | {st_status}")
    return 0


def cmd_reset(args):
    cfg = _load_cfg(args)
    workdir = cfg.get("workdir", "workdir")
    cdir = Path(workdir) / "concepts" / args.concept
    state_file = cdir / "estado.json"
    if state_file.exists():
        state_file.unlink()
        print(f"Estado reiniciado: {args.concept}")
    else:
        print(f"Sin estado para: {args.concept}")
    return 0


def cmd_dry_run(args):
    args.dry_run = True
    return cmd_run(args)




def cmd_validate(args):
    cfg = _load_cfg(args)
    concepts = _load_concepts(cfg)
    if args.concept:
        concepts = [c for c in concepts if c.id == args.concept or args.concept in c.id]
    elif args.area:
        concepts = [c for c in concepts if c.area == args.area]
    if args.limit:
        concepts = concepts[:args.limit]
    import validation as V
    for c in concepts:
        cdir = None
        try:
            import json
            from pathlib import Path
            wd = cfg.get("workdir", "workdir")
            sd = Path(wd) / "concepts" / c.id / "synthesis.json"
            src = Path(wd) / ".pipeline" / c.id / "sources.json"
            synth_data = json.loads(sd.read_text(encoding="utf-8")) if sd.exists() else {}
            sources = json.loads(src.read_text(encoding="utf-8")) if src.exists() else {}
            is_valid, issues, warnings = V.validate(c, synth_data, sources)
            print(f"{c.id}: valid={is_valid} issues={len(issues)} warnings={len(warnings)}")
            for it in issues:
                print(f"   issue: {it}")
        except Exception as e:
            print(f"{c.id}: error {e}")
    return 0


def cmd_report(args):
    cfg = _load_cfg(args)
    workdir = cfg.get("workdir", "workdir")
    from pathlib import Path
    import json
    rp = Path(workdir) / "run.jsonl"
    if not rp.exists():
        print("Sin run.jsonl")
        return 1
    lines = rp.read_text(encoding="utf-8").strip().splitlines()
    for ln in lines[-20:]:
        print(ln)
    return 0


def cmd_pilot(args):
    cfg = _load_cfg(args)
    concepts = _load_concepts(cfg)
    if args.area:
        concepts = [c for c in concepts if c.area == args.area]
    if args.limit:
        concepts = concepts[:args.limit]
    # Capa L: seleccionar 8 conceptos variados si no se especifica
    if not args.concept and not args.limit and len(concepts) > 8:
        concepts = select_pilot_concepts(concepts, n=8)
    llm = None
    runner_mod = None
    import pilot as PL
    import asyncio
    rep = asyncio.run(PL.run_pilot(concepts, cfg=cfg, llm=llm, workdir=cfg.get("workdir", "workdir"), force=args.force, dry_run=args.dry_run))
    print(f"Total: {rep.total} | completed: {rep.completed} | failed: {rep.failed} | skipped: {rep.skipped} | success_rate: {rep.success_rate:.1%}")
    return 0 if rep.failed == 0 else 1


def select_pilot_concepts(concepts, n=8):
    """Capa L: selecciona n conceptos variados (diversos por area)."""
    by_area = {}
    for c in concepts:
        by_area.setdefault(c.area, []).append(c)
    selected = []
    # round-robin across areas
    areas = sorted(by_area.keys())
    i = 0
    while len(selected) < n and areas:
        progressed = False
        for a in areas:
            if by_area[a] and len(selected) < n:
                selected.append(by_area[a].pop(0))
                progressed = True
        if not progressed:
            break
    return selected

def main(argv=None):
    parser = argparse.ArgumentParser(prog="kpipe", description="Pipeline de enriquecimiento de conceptos IT")
    parser.add_argument("--config", default="config.yaml", help="Ruta al config.yaml")
    parser.add_argument("--workdir", default=None, help="Override workdir")
    parser.add_argument("--vault", default=None, help="Override vault_path")
    sub = parser.add_subparsers(dest="command", required=True)

    # run
    p_run = sub.add_parser("run", help="Ejecutar pipeline por concepto o batch")
    p_run.add_argument("concept", nargs="?", default=None, help="concept_id (opcional)")
    p_run.add_argument("--area", default=None, help="Filtrar por area")
    p_run.add_argument("--limit", type=int, default=None, help="Limitar cantidad")
    p_run.add_argument("--force", action="store_true", help="Forzar re-ejecucion")
    p_run.add_argument("--force-phase", default=None, help="Forzar desde una fase (research/synthesis/validation/writing)")
    p_run.add_argument("--dry-run", dest="dry_run", action="store_true", help="Simular sin escribir")
    p_run.set_defaults(func=cmd_run)

    # status
    p_status = sub.add_parser("status", help="Ver estado de un concepto")
    p_status.add_argument("concept", help="concept_id")
    p_status.set_defaults(func=cmd_status)

    # list
    p_list = sub.add_parser("list", help="Listar conceptos por estado")
    p_list.add_argument("--status", default=None, help="Filtrar por estado (pending, completed, failed, ...)")
    p_list.set_defaults(func=cmd_list)

    # reset
    p_reset = sub.add_parser("reset", help="Reiniciar estado de un concepto")
    p_reset.add_argument("concept", help="concept_id")
    p_reset.set_defaults(func=cmd_reset)

    # dry-run
    p_dry = sub.add_parser("dry-run", help="Simular pipeline sin escribir")
    p_dry.add_argument("concept", nargs="?", default=None, help="concept_id (opcional)")
    p_dry.add_argument("--area", default=None, help="Filtrar por area")
    p_dry.add_argument("--limit", type=int, default=None, help="Limitar cantidad")
    p_dry.set_defaults(func=cmd_dry_run, dry_run=True, force=False)

    # validate
    p_val = sub.add_parser("validate", help="Validar sintesis de conceptos")
    p_val.add_argument("concept", nargs="?", default=None, help="concept_id (opcional)")
    p_val.add_argument("--area", default=None, help="Filtrar por area")
    p_val.add_argument("--limit", type=int, default=None, help="Limitar cantidad")
    p_val.set_defaults(func=cmd_validate, dry_run=False, force=False)

    # report
    p_rep = sub.add_parser("report", help="Mostrar run.jsonl reciente")
    p_rep.set_defaults(func=cmd_report)

    # pilot
    p_pilot = sub.add_parser("pilot", help="Ejecutar piloto con conceptos variados")
    p_pilot.add_argument("concept", nargs="?", default=None, help="concept_id (opcional)")
    p_pilot.add_argument("--area", default=None, help="Filtrar por area")
    p_pilot.add_argument("--limit", type=int, default=None, help="Limitar cantidad")
    p_pilot.add_argument("--force", action="store_true", help="Forzar re-ejecucion")
    p_pilot.add_argument("--dry-run", dest="dry_run", action="store_true", help="Simular sin escribir")
    p_pilot.set_defaults(func=cmd_pilot, dry_run=False, force=False)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    # asegurar dry_run attribute
    if not hasattr(args, "dry_run"):
        args.dry_run = False
    if not hasattr(args, "force"):
        args.force = False
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
