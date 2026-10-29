# Explicacion codigo - Capa 6: Sintesis

## Que es la Capa de Sintesis
Genera el study guide a partir de la investigacion (raw_research.json + sources.json). Construye el prompt de sintesis siguiendo las reglas de evidencia de la spec, llama al LLM para generar el contenido del .md, persiste synthesis.json, transiciona estado a synthesized. Idempotente y recuperable.

## SynthesisPhase
Clase que orquesta la sintesis. Recibe un LLM (sync o async) y config. Metodo run(concept, force=False). Incluye:
- build_prompt(concept, raw, sources): construye el prompt con reglas de evidencia (contexto antes que definicion, 20/80, no inventar, trazabilidad por afirmacion, separacion fundamento estable/practica moderna, secciones del contrato).
- Idempotencia: si ya esta synthesized y hay cache, no re-sintetiza.
- Transicion a SYNTHESIZED (directa, sin validate_transition para evitar problemas de estado), manejo de errores (fallo -> failed con failed_reason "error").
- Parseo de secciones (## Nombre) del markdown generado.
- Backup con force si ya existia synthesis.json.
- Persistencia de synthesis.json (concept_id, title, markdown, sections, prompt, generated_at, duration_ms).

## Funcion de conveniencia
run_synthesis(concept, cfg, llm=None, force=False) crea la fase y ejecuta.

## Integracion con state.py y research.py
- state.py: load_state/save_state, transicion a SYNTHESIZED (directa), manejo de FAILED.
- research.py: lee raw_research.json y sources.json del .pipeline/<id>/.

## Manejo de errores
- Si el LLM falla -> estado FAILED, failed_phase="synthesizing", failed_reason="error", last_error/error guardados.
- Si no se proporciona LLM -> RuntimeError.

## Idempotencia
- Si state es SYNTHESIZED/VALIDATED/WRITTEN/COMPLETED y synthesis.json existe y no force → retorna resultado cacheado sin llamar al LLM.
- force=True: re-ejecuta y backupea synthesis.json anterior.

## Tests
- tests/test_synthesis.py: 11 tests (mock LLM), todos pasando.
- Cubren: build_prompt, persistencia de artefactos, idempotencia, force+backup, fallo marca failed, transicion invalida desde pending, async llm, sin llm lanza error, parseo de secciones, run_synthesis, protocolo de estados.

## Archivos
- synthesis.py: SynthesisPhase, SynthesisPhaseResult, build_prompt, run_synthesis, CONTRACT_SECTIONS.
- tests/test_synthesis.py: 11 tests.

## Resultado de tests
- 11/11 OK.
- py_compile OK.
