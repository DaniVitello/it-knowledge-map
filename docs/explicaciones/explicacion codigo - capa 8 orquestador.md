# Explicacion codigo - Capa 8: Orquestador

## Que es la Capa de Orquestador
Orquesta el pipeline completo por concepto: registry -> research -> synthesis -> validation -> writer, con logging en events.jsonl, reanudacion desde checkpoint, manejo de errores, pacing entre conceptos, reporte final.

## Runner
Clase que orquesta el pipeline. Recibe cfg, llm, workdir. Metodo run_concept(concept, force=False, dry_run=False) ejecuta las fases en orden. Metodo run_batch(concepts, force, dry_run) procesa una lista de conceptos con pacing.

## Flujo por concepto
1. Cargar estado (load_state). Si completed y no force/dry_run → saltar (idempotente).
2. Fase research: si estado es pending/failed/researching → ejecutar ResearchPhase. Si falla → failed, retornar.
3. Fase synthesis: si estado es researched/failed/synthesized → ejecutar SynthesisPhase. Si falla → failed.
4. Fase validation: si estado es synthesized/failed/validated → ejecutar ValidationPhase. Si no valido → failed.
5. Fase writing: si estado es validated/failed/written → ejecutar writing_phase. Si falla → failed.
6. Determinar status final (completed/failed/other). Logear run_end.

## Logging
- events.jsonl por concepto: run_start, phase_done, phase_failed, run_skip, run_end.
- Cada evento: ts, concept_id, event, y kwargs adicionales.

## Reportes
- RunReport: concept_id, status, phases_completed, error, duration_ms.
- BatchReport: total, completed, failed, blocked, skipped, results, duration_ms.

## Funciones de conveniencia
- run_concept(concept, cfg, llm, force, dry_run, workdir)
- run_batch(concepts, cfg, llm, force, dry_run, workdir)

## Integracion con todas las capas
- state.py: load_state, save_state, transiciones.
- backend.py: create_backend.
- research.py: ResearchPhase.
- synthesis.py: SynthesisPhase.
- validation.py: ValidationPhase.
- writer.py: writing_phase, SafeWriter.

## Manejo de errores
- Cada fase captura excepciones, marca estado como failed con failed_phase/failed_reason/last_error, persiste, y retorna report con status failed.
- El lote continúa con el siguiente concepto si uno falla.

## Idempotencia
- Si state es completed y no force/dry_run → salta (run_skip).
- Si state es researched/synthesized/validated → salta las fases ya completadas.

## Pacing
- pause_between_concepts_s entre conceptos del lote.
- pause_between_asks_s entre preguntas (manejado por las fases).

## Tests
- tests/test_runner.py: 11 tests, todos pasando.
- Cubren: run completo, idempotencia, fallo en research, desde researched/synthesized/validated, run_batch, logging, funciones de conveniencia, protocolo.

## Archivos
- runner.py: Runner, RunReport, BatchReport, run_concept, run_batch.
- tests/test_runner.py: 11 tests.

## Resultado de tests
- 11/11 OK.
- py_compile OK.
