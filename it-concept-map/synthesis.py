"""Capa 6 - Sintesis: genera el study guide a partir de la investigacion.

SynthesisPhase: lee raw_research.json + sources.json del .pipeline/<id>/,
construye el prompt de sintesis siguiendo las reglas de evidencia de la spec,
llama al LLM para generar el contenido del .md, persiste synthesis.json,
transiciona estado a synthesized. Idempotente y recuperable.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Awaitable

import state
import backend
import areas as areas_mod
from models import ConceptMeta, Synthesis

SCHEMA_VERSION = "1.0.0"

# Secciones del contrato (punto 18 de la spec).
CONTRACT_SECTIONS = [
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


@dataclass
class SynthesisPhaseResult:
    concept_id: str
    markdown: str = ""
    sections: dict = field(default_factory=dict)
    prompt: str = ""
    duration_ms: int = 0
    synthesis_path: str | None = None

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Construccion del prompt
# ---------------------------------------------------------------------------


def build_prompt(concept: ConceptMeta, raw: dict, sources: dict,
                 area_context: dict | None = None) -> str:
    if area_context is None:
        area_context = areas_mod.resolve_for_concept(concept.id, concept.area,
                                                     frontmatter=concept.frontmatter)
    ctx = area_context or {}
    roles = ctx.get("professional_roles") or [f"experto en {concept.area}"]
    roles_str = " y ".join(roles)
    main_role = roles[0]
    framing = ctx.get("context_framing") or ""
    questions = ctx.get("context_questions") or []
    style_example = ctx.get("style_example") or ""
    response_mode = ctx.get("response_mode") or ""
    mode_text = {
        "lista": "en formato de listas ordenadas, con prosa breve entre ellas",
        "libre": "en prosa libre, con ejemplos concretos",
    }.get(response_mode, "en prosa clara, con ejemplos concretos")
    questions_text = ""
    for q in questions:
        questions_text += f"- {q}\n"
    if not questions_text:
        questions_text = "(no definidas)\n"

    title = concept.title
    area = concept.area
    key_ideas = ", ".join(concept.key_ideas) if concept.key_ideas else "(no definidas)"
    connections = ", ".join(concept.connections) if concept.connections else "(ninguno)"
    volatility = getattr(concept, "volatility", "semi_stable")
    if hasattr(volatility, "value"):
        volatility = volatility.value

    sources_list = ""
    for s in sources.get("sources", []):
        sources_list += f"- {s.get('source_id')}: {s.get('title', '')} ({s.get('url', '')})\n"

    answers_text = ""
    for a in raw.get("answers", []):
        answers_text += f"\n### Grupo {a.get('group', '')} ({a.get('qid', '')})\n{a.get('answer_md', '')}\n"

    context_block = f"""CONTEXTO PROFESIONAL (area: {area})
- Rol: Sos {roles_str} y un excelente docente.
- Contexto profesional: {framing}
- Estilo de ejemplo esperado: {style_example}
- Modo de respuesta: respondé {mode_text}
- Preguntas de contexto que la nota debe responder:
{questions_text}
"""

    prompt = f"""Estas ayudando a una persona autodidacta a construir un mapa conceptual interconectado de ingenieria de software.

{context_block}
CONCEPTO: {title}
AREA: {area}
IDEAS PRINCIPALES (definidas por el autor): {key_ideas}
CONCEPTOS CONECTADOS: {connections}
ESTABILIDAD: {volatility}

REGLAS INNEGOCIABLES
1. Usa SOLO las fuentes del notebook. Si las fuentes no permiten afirmar algo, NO lo incluyas en el texto. No escribas "sin verificar" ni "??" en el texto visible.
1b. PROHIBIDO escribir "(sin verificar)", "??", "sin verificar" o cualquier marcador de incertidumbre en el texto. Si no tienes fuente, omiti la afirmacion. Este marcador es metadata interna y NUNCA aparece en el output.
2. No inventes URLs, versiones, fechas, estadisticas, estandares, funcionalidades ni relaciones.
3. Contexto antes que definicion: explica que significa y para que sirve DENTRO del area {area}.
4. Principio 20/80: primero las 3 a 5 ideas que dan el modelo mental.
5. Nada de historia innecesaria, listas interminables, definiciones circulares ni copiar documentacion.
6. Menciona conceptos conectados por nombre (sin usar [[...]]). Explica la naturaleza de la relacion.
7. Espanol claro y directo; terminos tecnicos en ingles cuando son el estandar.
8. Respondé SOLO con las secciones pedidas, cada una con su encabezado de nivel 2 EXACTO (## Nombre). Sin introduccion ni cierre.
9. Usa acentos correctos en español (á, é, í, ó, ú, ñ, ü). No generes caracteres corruptos.
10. Máximo 6000 caracteres en total para todas las secciones combinadas.

FUENTES DISPONIBLES:
{sources_list}

RESULTADOS DE INVESTIGACION:
{answers_text}

TAREA: escribi unicamente estas secciones, con estos encabezados exactos y en este orden:
{chr(10).join('## ' + s for s in CONTRACT_SECTIONS)}

GUA POR SECCION
- Objetivo: Redacta un parrafo corrido (no bullets, no preguntas) que responda en prosa natural: para que lo uso, que problema resuelve, donde aparece en el trabajo de un {main_role}, que puedo hacer despues de entenderlo, cuando no necesito preocuparme. Primera persona ("Utilizo...", "Resuelvo..."). Maximo 200 palabras. La definicion formal va despues.
- Esqueleto (el 20% esencial): entre 3 y 5 ideas fundamentales, como lista numerada, cada una con una o dos frases. Las IDEAS PRINCIPALES del autor (listadas en el contexto) son la base: el esqueleto debe cubrir al menos esas ideas, aunque puede expandirlas o reorganizarlas.
- Como funciona: que ocurre cuando se usa, paso a paso, conectado a las ideas del esqueleto.
- Detalles: progresion de lo basico a lo intermedio y lo avanzado, colgando de las ideas del esqueleto.
- Ejemplo minimo: el ejemplo mas chico que muestre el concepto funcionando. Siempre incluir un bloque de codigo. Si no hay ejemplo respaldado por las fuentes, escribilo igual de simple.
- Errores comunes: los errores y malentendidos reales, con una linea sobre como evitarlos.
- Estado actual: separa fundamentos estables de practica moderna. Cada afirmacion sensible al tiempo debe salir de una fuente. Si no puedes respaldar una afirmacion, omitila por completo. NUNCA escribas "(sin verificar)" ni "??" ni parentesis similares en el texto. Es metadata interna, no contenido visible.
- Conexiones: exactamente 3 conceptos conectados por nombre (sin [[...]]), priorizando conceptos de OTRAS areas. Para cada uno, una frase que explique la naturaleza de la relacion.
- Ruta de estudio: que conviene saber antes (prerrequisitos) y como avanzar despues, de fundamentos a avanzado. Debe ser especifico del tema, no generico.
- Preguntas de repaso: exactamente 5 preguntas, mezclando comprension y aplicacion. Cada pregunta termina con "?".
"""
    return prompt


# ---------------------------------------------------------------------------
# SynthesisPhase
# ---------------------------------------------------------------------------


class SynthesisPhase:
    """Orquesta la sintesis de un concepto usando un LLM."""

    def __init__(self, llm: Callable[[str], Awaitable[str]] | Callable[[str], str] | None = None, cfg: dict | None = None):
        self.llm = llm
        self.cfg = cfg or {}

    def _workdir(self) -> str:
        return self.cfg.get("workdir", "workdir")

    def _pipeline_dir(self, concept_id: str):
        from pathlib import Path
        return Path(self._workdir()) / "concepts" / concept_id

    async def _call_llm(self, prompt: str) -> str:
        if self.llm is None:
            raise RuntimeError("No se proporciono LLM para la sintesis")
        import asyncio
        if asyncio.iscoroutinefunction(self.llm):
            return await self.llm(prompt)
        # sync callable
        return self.llm(prompt)

    async def run(self, concept, force: bool = False) -> SynthesisPhaseResult:
        workdir = self._workdir()
        cdir = self._pipeline_dir(concept.id)
        cdir.mkdir(parents=True, exist_ok=True)

        st = state.load_state(concept.id, workdir=workdir)
        if st is None:
            st = state.ConceptState(concept_id=concept.id)

        synthesis_path = cdir / "synthesis.json"

        # Idempotencia: si ya esta synthesized y hay cache, no re-sintetizar.
        if (not force and st.status in (state.ConceptStatus.SYNTHESIZED, state.ConceptStatus.VALIDATED,
                                        state.ConceptStatus.WRITTEN, state.ConceptStatus.COMPLETED)
                and synthesis_path.exists()):
            try:
                data = json.loads(synthesis_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                data = {}
            # A3: validar artefacto leido (skip si no existe / vacio / sin contenido).
            if isinstance(data, dict) and data:
                backend.validate_artifact_schema(data, "synthesis")
            return SynthesisPhaseResult(
                concept_id=data.get("concept_id", concept.id),
                markdown=data.get("markdown", ""),
                sections=data.get("sections", {}),
                prompt=data.get("prompt", ""),
                synthesis_path=str(synthesis_path),
            )

        # Transicion a SYNTHESIZED.
        if st.status not in (state.ConceptStatus.RESEARCHED, state.ConceptStatus.FAILED):
            if not force:
                raise state.InvalidTransitionError(f"Transicion invalida: {st.status.value} -> synthesized")
            if st.status != state.ConceptStatus.RESEARCHED:
                st.transition_to(state.ConceptStatus.RESEARCHED, force=True)
        st.transition_to(state.ConceptStatus.SYNTHESIZED)
        st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
        state.save_state(st, workdir=workdir)

        # Leer artefactos de investigacion.
        raw_path = cdir / "raw_research.json"
        sources_path = cdir / "sources.json"
        try:
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, FileNotFoundError):
            raw = {}
        try:
            sources = json.loads(sources_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, FileNotFoundError):
            sources = {}

        # Construir prompt con contexto por area (Capa D).
        area_ctx = areas_mod.resolve_for_concept(
            concept.id, concept.area, config=self.cfg, frontmatter=concept.frontmatter
        )
        prompt = build_prompt(concept, raw, sources, area_context=area_ctx)

        # Llamar al LLM.
        import time
        t0 = time.monotonic()
        try:
            markdown = await self._call_llm(prompt)
            # Post-procesamiento: eliminar marcadores de incertidumbre del texto visible.
            import re as _re
            markdown = _re.sub(r'\s*\(sin verificar\)', '', markdown)
            markdown = _re.sub(r'\s*\?\?', '', markdown)
        except Exception as e:
            st.transition_to(state.ConceptStatus.FAILED)
            st.phase_data["failed_phase"] = "synthesizing"
            st.phase_data["failed_reason"] = "error"
            st.last_error = str(e)
            st.error = str(e)
            st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
            state.save_state(st, workdir=workdir)
            raise
        duration_ms = int((time.monotonic() - t0) * 1000)

        # Parsear secciones (## Nombre).
        sections = {}
        current = None
        for line in markdown.splitlines():
            if line.startswith("## "):
                current = line[3:].strip()
                sections[current] = ""
            elif current is not None:
                sections[current] += line + "\n"
        sections = {k: v.strip() for k, v in sections.items()}

        # Backup si force y ya existia synthesis.json.
        if force and synthesis_path.exists():
            backups = Path(workdir) / "backups" / concept.id
            backups.mkdir(parents=True, exist_ok=True)
            ts = (state.now_iso() if hasattr(state, "now_iso") else "backup").replace(":", "-")
            import shutil
            shutil.copy2(synthesis_path, backups / f"synthesis.json.{ts}.bak")

        # Persistir synthesis.json.
        import datetime
        synth_data = {
            "concept_id": concept.id,
            "title": concept.title,
            "markdown": markdown,
            "sections": sections,
            "prompt": prompt,
            "generated_at": state.now_iso() if hasattr(state, "now_iso") else datetime.datetime.now().isoformat(),
            "duration_ms": duration_ms,
        }
        # A3: validar schema antes de escribir (fail-fast con mensaje claro).
        backend.validate_artifact_schema(synth_data, "synthesis")
        backend._atomic_write_json(synthesis_path, synth_data)

        # (Ya transicionado a SYNTHESIZED al inicio de la fase.)
        st.phase_data["synthesis_path"] = str(synthesis_path)
        st.updated_at = state.now_iso() if hasattr(state, "now_iso") else None
        state.save_state(st, workdir=workdir)

        return SynthesisPhaseResult(
            concept_id=concept.id,
            markdown=markdown,
            sections=sections,
            prompt=prompt,
            duration_ms=duration_ms,
            synthesis_path=str(synthesis_path),
        )


# ---------------------------------------------------------------------------
# Funcion de conveniencia
# ---------------------------------------------------------------------------


async def run_synthesis(concept, cfg, llm=None, force=False):
    phase = SynthesisPhase(llm=llm, cfg=cfg)
    return await phase.run(concept, force=force)
