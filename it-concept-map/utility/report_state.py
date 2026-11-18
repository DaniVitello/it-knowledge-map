"""Genera el estado del pipeline desde la fuente canonica (workdir/concepts/*/estado.json).

Single-source of truth: el estado se DERIVA de los datos, no se mantiene a mano.
Uso: py utility/report_state.py [workdir] [out.md]
"""
from __future__ import annotations
import json, sys, collections
from pathlib import Path


def summarize(workdir: Path) -> dict:
    cdir = workdir / "concepts"
    statuses = collections.Counter()
    failed_phase = collections.Counter()
    total = 0
    with_events = 0
    runs = 0
    for d in sorted(cdir.iterdir()) if cdir.exists() else []:
        ej = d / "estado.json"
        if not ej.is_file():
            continue
        total += 1
        try:
            st = json.loads(ej.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            statuses["<ilegible>"] += 1
            continue
        statuses[st.get("status", "<sin status>")] += 1
        fp = (st.get("phase_data") or {}).get("failed_phase")
        if fp:
            failed_phase[fp] += 1
        ev = d / "events.jsonl"
        if ev.is_file():
            with_events += 1
            try:
                runs += sum(1 for l in ev.read_text(encoding="utf-8").splitlines() if '"run_start"' in l)
            except OSError:
                pass
    return {"total": total, "statuses": dict(statuses), "failed_phase": dict(failed_phase),
            "with_events": with_events, "runs": runs}


def render(s: dict) -> str:
    lines = ["# Estado del pipeline (generado desde estado.json)", "",
             "> Fuente canonica: `workdir/concepts/*/estado.json`. NO editar a mano.",
             "> Regenerar: `py utility/report_state.py <workdir> docs/STATE.md`", "",
             f"- Conceptos con estado: **{s['total']}**",
             f"- Con events.jsonl: {s['with_events']} | run_start totales: {s['runs']}", "",
             "## Status counts", ""]
    for k, v in sorted(s["statuses"].items(), key=lambda x: -x[1]):
        lines.append(f"- `{k}`: {v}")
    if s["failed_phase"]:
        lines += ["", "## failed_phase (recuperados o pendientes)", ""]
        for k, v in sorted(s["failed_phase"].items(), key=lambda x: -x[1]):
            lines.append(f"- `{k}`: {v}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    wd = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workdir")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    md = render(summarize(wd))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"Escrito {out}")
    else:
        print(md)
