# Explicacion codigo - Capa 10: Piloto + calibracion

## Que es la Capa de Piloto
Ejecuta el pipeline sobre un subconjunto de conceptos del vault para validar end-to-end, genera reporte de piloto con metricas (tiempos por fase, tasa de exito, errores, calidad de sintesis, fuentes). Calibracion de parametros (timeouts, pacing, max_per_notebook, etc.).

## PilotRunner
Clase que orquesta el piloto. Recibe cfg, llm, workdir, concepts. Metodo run_pilot(force, dry_run) ejecuta el pipeline sobre cada concepto y genera PilotReport. Metodo generate_summary(report) genera un resumen en Markdown.

## PilotReport
Dataclass con metricas: total, completed, failed, skipped, success_rate, avg_duration_ms, total_duration_ms, metrics (lista de PilotMetrics), errors, calibration. Metodo to_dict() para serializacion.

## PilotMetrics
Metricas por concepto: concept_id, status, duration_ms, phases_completed, error, synthesis_chars, validation_score, source_count.

## Calibracion
Basada en resultados del piloto: suggested_pacing_s (20 si success_rate < 0.8, sino 10), suggested_timeout_s (900). Persistido en pilot_report.json.

## Funcion de conveniencia
run_pilot(concepts, cfg, llm, workdir, force, dry_run) crea el PilotRunner y ejecuta.

## Integracion
- runner.py: Runner, run_concept.
- state.py: load_state.
- Todos los modulos anteriores.

## Tests
- tests/test_pilot.py: 9 tests, todos pasando.
- Cubren: reporte persistido, success_rate, metrics, generate_summary, to_dict, calibration, empty concepts, run_pilot funcion, protocolo.

## Archivos
- pilot.py: PilotRunner, PilotReport, PilotMetrics, run_pilot.
- tests/test_pilot.py: 9 tests.

## Resultado de tests
- 9/9 OK.
- py_compile OK.

## Resumen final del proyecto
TODAS LAS CAPAS COMPLETADAS (1-10). Total tests: 82 (15+12+11+12+11+12+9).
Proyecto listo para piloto con cuenta real (smoke_notebooklm.py + pilot.py).
```