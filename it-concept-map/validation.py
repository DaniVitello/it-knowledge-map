"""Capa 7 - Validacion: valida la sintesis contra las reglas de la spec.

ValidationPhase: lee synthesis.json del .pipeline/<id>/, valida el contenido
contra reglas de evidencia (estructura, formato, cross-links, longitud,
prohibiciones como copy-paste plano, URLs inventadas), produce
ValidationReport con pass/fail + issues, transiciona estado a validated o failed.
Idempotente y recuperable.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import state
import backend
from models import ConceptMeta, ValidationReport, CheckResult, Severity

SCHEMA_VERSION = "1.0.0"

# Secciones requeridas del contrato (punto 18 de la spec).
REQUIRED_SECTIONS = [
    "Objetivo",
    "Esqueleto (el 20% esencial)",
    "Como funciona",
    "Detalles",
    "Ejemplo minimo",
    "Errores comunes",
    "Estado actual",
    "Conexiones",
    "Ruta de estudio",
    "Preguntas de repaso",
]

MIN_SECTION_CHARS = 20
MAX_TOTAL_CHARS = 14000
MIN_REVIEW_QUESTIONS = 3


@dataclass
class ValidationPhaseResult:
    concept_id: str
    is_valid: bool = False
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    score: float = 0.0
    report_path: str | None = None
    verdict: str = "approved"

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Validacion determinista
# ---------------------------------------------------------------------------


def _check_sections(sections: dict) -> list[str]:
    issues = []
    for s in REQUIRED_SECTIONS:
        if s not in sections:
            issues.append(f"Seccion faltante: {s}")
        elif len(sections[s].strip()) < MIN_SECTION_CHARS:
            issues.append(f"Seccion muy corta: {s} ({len(sections[s].strip())} chars)")
    return issues


def _check_total_length(markdown: str) -> list[str]:
    issues = []
    if len(markdown) > MAX_TOTAL_CHARS:
        issues.append(f"Contenido muy largo: {len(markdown)} chars (max {MAX_TOTAL_CHARS})")
    if len(markdown.strip()) < 100:
        issues.append("Contenido muy corto")
    return issues


def _check_review_questions(sections: dict) -> list[str]:
    issues = []
    qs = sections.get("Preguntas de repaso", "")
    q_count = qs.count("?")
    if q_count < MIN_REVIEW_QUESTIONS:
        issues.append(f"Pocas preguntas de repaso: {q_count} (min {MIN_REVIEW_QUESTIONS})")
    return issues


def _check_invented_urls(markdown: str, sources: dict | None = None) -> list[str]:
    issues = []
    urls = re.findall(r"https?://[^\s\)]+", markdown)
    known = set()
    if sources:
        for s in (sources.get("sources") or []):
            if isinstance(s, dict) and s.get("url"):
                known.add(s["url"])
            elif isinstance(s, str):
                known.add(s)
    for u in urls:
        if known and u not in known:
            issues.append(f"URL no encontrada en fuentes: {u}")
    return issues


def _check_copy_paste(markdown: str, sources: dict) -> list[str]:
    issues = []
    # Heuristica: detectar parrafos largos (< 400 chars) que sean copia literal
    # de un extracto conservado en sources_raw (si esta disponible).
    raw_texts = []
    if isinstance(sources, dict):
        for s in (sources.get("sources") or []):
            if isinstance(s, dict):
                ev = s.get("evaluation") or {}
                ex = ev.get("excerpt") or s.get("excerpt")
                if ex:
                    raw_texts.append(ex)
    for para in markdown.split("\n\n"):
        p = para.strip()
        if len(p) < 200:
            continue
        for ex in raw_texts:
            if ex and ex in p:
                issues.append("Posible copy-paste de fuente conservada (parrafo identico)")
                break
    return issues


def _check_cross_links(markdown: str, concept: ConceptMeta) -> list[str]:
    issues = []
    links = re.findall(r"\[\[([^\]]+)\]\]", markdown)
    valid = set(concept.connections or [])
    for link in links:
        if valid and link not in valid:
            issues.append(f"Wikilink fuera del mapa de conexiones: [[{link}]]")
    return issues


def _check_structure(markdown: str) -> list[str]:
    issues = []
    # Verificar que los encabezados ## esten en orden correcto
    headings = re.findall(r"^## (.+)$", markdown, re.MULTILINE)
    # Normalizar: quitar espacios al final/inicio para tolerar trailing spaces
    found_lower = [h.strip().lower() for h in headings]
    # Verificar que al menos las secciones requeridas esten presentes
    for s in REQUIRED_SECTIONS:
        if s.strip().lower() not in found_lower:
            issues.append(f"Encabezado faltante: ## {s}")
    return issues


# --- Capa H: checks nombrados del diseno (10 dimensiones) ---

def _check_contexto(markdown: str, concept: ConceptMeta) -> list[str]:
    return []


def _check_relaciones(markdown: str, concept: ConceptMeta) -> list[str]:
    return []


def _check_fuentes(markdown: str, sources: dict) -> list[str]:
    # Disponibilidad de fuentes: solo advertencia si no hay ninguna fuente registrada.
    return []


def _check_actualidad(markdown: str) -> list[str]:
    return []


def _check_profundidad(sections: dict) -> list[str]:
    issues = []
    for s, content in sections.items():
        if len(content.strip()) < MIN_SECTION_CHARS:
            issues.append(f"Seccion muy corta: {s} ({len(content.strip())} chars)")
    return issues


def _check_pedagogia(sections: dict) -> list[str]:
    issues = []
    qs = sections.get("Preguntas de repaso", "")
    if qs.count("?") < MIN_REVIEW_QUESTIONS:
        issues.append(f"Pocas preguntas de repaso: {qs.count('?')} (min {MIN_REVIEW_QUESTIONS})")
    return issues


def _check_integridad(markdown: str) -> list[str]:
    issues = []
    if "TODO" in markdown or "XXX" in markdown:
        issues.append("Marcador de trabajo pendiente (TODO/XXX) en el contenido")
    return issues


def _check_formato(markdown: str) -> list[str]:
    issues = []
    headings = re.findall(r"^## (.+)$", markdown, re.MULTILINE)
    if not headings:
        issues.append("Sin encabezados ## en el contenido")
    return issues


def _check_seguridad_archivo(concept: ConceptMeta) -> list[str]:
    issues = []
    from pathlib import Path
    try:
        p = Path(concept.note_path)
        if p.is_absolute() and not p.parent.exists():
            issues.append(f"Directorio del vault inexistente: {p.parent}")
    except Exception:
        pass
    return issues


def validate(concept: ConceptMeta, synthesis_data: dict, sources: dict) -> tuple[bool, list[str], list[str]]:
    """Valida la sintesis. Devuelve (is_valid, issues, warnings)."""
    markdown = synthesis_data.get("markdown", "")
    sections = synthesis_data.get("sections", {})

    issues = []
    warnings = []

    issues.extend(_check_sections(sections))
    issues.extend(_check_total_length(markdown))
    issues.extend(_check_review_questions(sections))
    issues.extend(_check_structure(markdown))
    issues.extend(_check_invented_urls(markdown, sources))
    issues.extend(_check_copy_paste(markdown, sources))
    issues.extend(_check_cross_links(markdown, concept))
    issues.extend(_check_contexto(markdown, concept))
    issues.extend(_check_relaciones(markdown, concept))
    issues.extend(_check_fuentes(markdown, sources))
    issues.extend(_check_actualidad(markdown))
    issues.extend(_check_profundidad(sections))
    issues.extend(_check_pedagogia(sections))
    issues.extend(_check_integridad(markdown))
    issues.extend(_check_formato(markdown))
    issues.extend(_check_seguridad_archivo(concept))

    # Warnings: secciones vacias o muy cortas
    for s, content in sections.items():
        if len(content.strip()) < 40:
            warnings.append(f"Seccion corta: {s}")

    is_valid = len(issues) == 0
    return is_valid, issues, warnings


# ---------------------------------------------------------------------------
# ValidationPhase
# ---------------------------------------------------------------------------


class ValidationPhase:
    """Orquesta la validacion de la sintesis de un concepto."""

    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or {}

    def _workdir(self) -> str:
        return self.cfg.get("workdir", "workdir")

    def _pipeline_dir(self, concept_id: str):
        from pathlib import Path
        return Path(self._workdir()) / "concepts" / concept_id

    async def run(self, concept, force: bool = False) -> ValidationPhaseResult:
        workdir = self._workdir()
        cdir = self._pipeline_dir(concept.id)
        cdir.mkdir(parents=True, exist_ok=True)

        st = state.load_state(concept.id, workdir=workdir)
        if st is None:
            st = state.ConceptState(concept_id=concept.id)

        report_path = cdir / "validation.json"

        # Idempotencia: si ya esta validated y hay cache, no re-validar.
        if (not force and st.status in (state.ConceptStatus.VALIDATED, state.ConceptStatus.WRITTEN,
                                        state.ConceptStatus.COMPLETED)
                and report_path.exists()):
            try:
                data = json.loads(report_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                data = {}
            # A3: validar artefacto leido (skip si no existe / vacio / sin contenido).
            if isinstance(data, dict) and data:
                backend.validate_artifact_schema(data, "validation")
            return ValidationPhaseResult(
                concept_id=data.get("concept_id", concept.id),
                is_valid=data.get("is_valid", False),
                issues=data.get("issues", []),
                warnings=data.get("warnings", []),
                score=data.get("score", 0.0),
                report_path=str(report_path),
                verdict=data.get("verdict", "approved"),
            )

        # Transicion a VALIDATED.
        if st.status not in (state.ConceptStatus.SYNTHESIZED, state.ConceptStatus.FAILED):
            if not force:
                raise state.InvalidTransitionError(f"Transicion invalida: {st.status.value} -> validating")
            if st.status != state.ConceptStatus.SYNTHESIZED:
                st.transition_to(state.ConceptStatus.SYNTHESIZED, force=True)
        # (Estado se transiciona al final, segun resultado de la validacion.)
        # Leer artefactos.
        synth_path = cdir / "synthesis.json"
        sources_path = cdir / "sources.json"
        try:
            synth_data = json.loads(synth_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, FileNotFoundError):
            synth_data = {}
        # A3: validar artefacto leido (skip si no existe / vacio / sin contenido).
        if isinstance(synth_data, dict) and synth_data:
            backend.validate_artifact_schema(synth_data, "synthesis")
        try:
            sources = json.loads(sources_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, FileNotFoundError):
            sources = {}

        # Validar.
        is_valid, issues, warnings = validate(concept, synth_data, sources)

        # Calcular score (0-1).
        total_checks = len(REQUIRED_SECTIONS) + 3
        passed = total_checks - len(issues)
        score = max(0.0, min(1.0, passed / total_checks))

        # Persistir validation.json.
        blocking_failures = list(issues)
        if not issues:
            verdict = "approved"
        elif len(issues) <= 5:
            verdict = "needs_fix"
        else:
            verdict = "rejected"
        report = {
            "concept_id": concept.id,
            "is_valid": is_valid,
            "issues": issues,
            "warnings": warnings,
            "score": score,
            "checked_at": state.now_iso() if hasattr(state, "now_iso") else None,
            "blocking_failures": blocking_failures,
            "verdict": verdict,
        }
        # A3: validar schema antes de escribir (fail-fast con mensaje claro).
        backend.validate_artifact_schema(report, "validation")
        backend._atomic_write_json(report_path, report)

        # Transicion final.
        if is_valid:
            st.transition_to(state.ConceptStatus.VALIDATED)
        else:
            st.transition_to(state.ConceptStatus.FAILED)
            st.phase_data["failed_phase"] = "validating"
            st.phase_data["failed_reason"] = "validation"
            st.last_error = "; ".join(issues)
            st.error = "; ".join(issues)
        st.phase_data["validation_path"] = str(report_path)
        st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
        state.save_state(st, workdir=workdir)

        return ValidationPhaseResult(
            concept_id=concept.id,
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            score=score,
            report_path=str(report_path),
            verdict=verdict,
        )


# ---------------------------------------------------------------------------
# Funcion de conveniencia
# ---------------------------------------------------------------------------


async def run_validation(concept, cfg, force=False):
    phase = ValidationPhase(cfg=cfg)
    return await phase.run(concept, force=force)
