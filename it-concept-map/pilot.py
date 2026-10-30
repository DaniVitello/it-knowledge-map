"""Capa 10 - Piloto + calibracion del pipeline.

PilotRunner: ejecuta el pipeline sobre un subconjunto de conceptos del vault
para validar end-to-end, genera reporte de piloto con metricas (tiempos por
fase, tasa de exito, errores, calidad de sintesis). Calibracion de parametros.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import runner as RN
import state
from models import ConceptMeta

SCHEMA_VERSION = "1.0.0"


@dataclass
class PilotMetrics:
    concept_id: str
    status: str = "pending"
    duration_ms: int = 0
    phases_completed: list[str] = field(default_factory=list)
    error: str | None = None
    synthesis_chars: int = 0
    validation_score: float = 0.0
    source_count: int = 0

    schema_version: str = SCHEMA_VERSION


@dataclass
class PilotReport:
    total: int = 0
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    success_rate: float = 0.0
    avg_duration_ms: float = 0.0
    total_duration_ms: int = 0
    metrics: list[PilotMetrics] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    calibration: dict = field(default_factory=dict)

    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "completed": self.completed,
            "failed": self.failed,
            "skipped": self.skipped,
            "success_rate": self.success_rate,
            "avg_duration_ms": self.avg_duration_ms,
            "total_duration_ms": self.total_duration_ms,
            "metrics": [
                {
                    "concept_id": m.concept_id,
                    "status": m.status,
                    "duration_ms": m.duration_ms,
                    "phases_completed": m.phases_completed,
                    "error": m.error,
                    "synthesis_chars": m.synthesis_chars,
                    "validation_score": m.validation_score,
                    "source_count": m.source_count,
                }
                for m in self.metrics
            ],
            "errors": self.errors,
            "calibration": self.calibration,
        }


class PilotRunner:
    """Ejecuta el pipeline sobre un subconjunto de conceptos para validar end-to-end."""

    def __init__(self, cfg: dict | None = None, llm=None, workdir: str | None = None, concepts: list | None = None):
        self.cfg = cfg or {}
        self.workdir = workdir or self.cfg.get("workdir", "workdir")
        self.llm = llm
        self.concepts = concepts or []
        self.pacing = self.cfg.get("pacing", {}).get("between_concepts_s", 0)

    async def run_pilot(self, force: bool = False, dry_run: bool = False) -> PilotReport:
        report = PilotReport(total=len(self.concepts))
        t0 = __import__("time").monotonic()

        for i, concept in enumerate(self.concepts):
            m = PilotMetrics(concept_id=concept.id)
            ct0 = __import__("time").monotonic()
            try:
                runner = RN.Runner(cfg=self.cfg, llm=self.llm, workdir=self.workdir)
                rep = await runner.run_concept(concept, force=force, dry_run=dry_run)
                m.status = rep.status
                m.phases_completed = rep.phases_completed
                m.error = rep.error
                m.duration_ms = rep.duration_ms

                # Metricas de calidad.
                cdir = Path(self.workdir) / "concepts" / concept.id
                synth_path = cdir / "synthesis.json"
                val_path = cdir / "validation.json"
                src_path = cdir / "sources.json"
                if synth_path.exists():
                    try:
                        synth = json.loads(synth_path.read_text(encoding="utf-8"))
                        m.synthesis_chars = len(synth.get("markdown", ""))
                    except (json.JSONDecodeError, OSError):
                        pass
                if val_path.exists():
                    try:
                        val = json.loads(val_path.read_text(encoding="utf-8"))
                        m.validation_score = val.get("score", 0.0)
                    except (json.JSONDecodeError, OSError):
                        pass
                if src_path.exists():
                    try:
                        src = json.loads(src_path.read_text(encoding="utf-8"))
                        m.source_count = src.get("count", 0)
                    except (json.JSONDecodeError, OSError):
                        pass

                if rep.status == "completed":
                    report.completed += 1
                elif rep.status == "failed":
                    report.failed += 1
                    report.errors.append({"concept_id": concept.id, "error": rep.error})
                else:
                    report.skipped += 1
            except Exception as e:
                m.status = "failed"
                m.error = str(e)
                report.failed += 1
                report.errors.append({"concept_id": concept.id, "error": str(e)})
            m.duration_ms = m.duration_ms or int((__import__("time").monotonic() - ct0) * 1000)
            report.metrics.append(m)

            if self.pacing and i < len(self.concepts) - 1:
                await asyncio.sleep(self.pacing)

        report.total_duration_ms = int((__import__("time").monotonic() - t0) * 1000)
        if report.total > 0:
            report.success_rate = report.completed / report.total
        if report.metrics:
            report.avg_duration_ms = sum(m.duration_ms for m in report.metrics) / len(report.metrics)

        # Calibracion sugerida.
        report.calibration = {
            "avg_duration_ms": report.avg_duration_ms,
            "success_rate": report.success_rate,
            "suggested_pacing_s": 20 if report.success_rate < 0.8 else 10,
            "suggested_timeout_s": 900,
        }

        # Persistir reporte.
        out_dir = Path(self.workdir)
        out_dir.mkdir(parents=True, exist_ok=True)
        report_path = out_dir / "pilot_report.json"
        report_path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    def generate_summary(self, report: PilotReport) -> str:
        lines = []
        lines.append(f"# Reporte de piloto")
        lines.append(f"")
        lines.append(f"- Total: {report.total}")
        lines.append(f"- Completados: {report.completed}")
        lines.append(f"- Fallidos: {report.failed}")
        lines.append(f"- Tasa de exito: {report.success_rate:.1%}")
        lines.append(f"- Duracion promedio: {report.avg_duration_ms:.0f} ms")
        lines.append(f"- Duracion total: {report.total_duration_ms} ms")
        lines.append(f"")
        lines.append(f"## Conceptos")
        for m in report.metrics:
            lines.append(f"- {m.concept_id}: {m.status} ({m.duration_ms}ms, score={m.validation_score:.2f}, sources={m.source_count})")
        if report.errors:
            lines.append(f"")
            lines.append(f"## Errores")
            for e in report.errors:
                lines.append(f"- {e['concept_id']}: {e['error']}")
        lines.append(f"")
        lines.append(f"## Calibracion")
        lines.append(f"- Pacing sugerido: {report.calibration.get('suggested_pacing_s')}s")
        lines.append(f"- Timeout sugerido: {report.calibration.get('suggested_timeout_s')}s")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Funcion de conveniencia
# ---------------------------------------------------------------------------


async def run_pilot(concepts, cfg=None, llm=None, workdir=None, force=False, dry_run=False):
    runner = PilotRunner(cfg=cfg, llm=llm, workdir=workdir, concepts=concepts)
    report = await runner.run_pilot(force=force, dry_run=dry_run)
    return report
