# Explicacion codigo - Capa 5: Investigacion

## Que es la Capa de Investigacion
Orquesta el backend para investigar un concepto: crea workspace, descubre fuentes, importa, consulta, persiste sources.json + raw_research.json en workdir/.pipeline/<id>/, borra notebook, transiciona estado a researched. Idempotente y recuperable.

## ResearchPhase
Clase que orquesta la investigacion. Recibe un backend y config. Metodo run(concept, force=False) ejecuta el flujo completo. Incluye:
- _questions(concept): genera 3 preguntas (a/b/c) a partir del concepto.
- Idempotencia: si ya esta researched y hay cache, no re-investiga.
- Transicion a RESEARCHING, manejo de errores (BackendAuthError -> failed_reason "auth"; BackendError -> failed_reason "error").
- Persistencia de sources.json (count + lista de fuentes) y raw_research.json (concept_id, coverage, answers, source_ids, notebook_id, duration_ms, backend_provider).
- Backup con force si ya existia raw_research.json.
- Transicion a RESEARCHED y guardado de state.

## Funcion de conveniencia
run_research(concept, cfg, backend=None, force=False) crea el backend si no se pasa y ejecuta la fase.

## Integracion con state.py y backend.py
- state.py: load_state/save_state, transition_to (PENDING->RESEARCHING->RESEARCHED), manejo de FAILED con failed_phase/failed_reason.
- backend.py: ResearchBackend (FakeBackend/NotebookLMBackend), ResearchResult, create_backend, pipeline_dir.

## Manejo de errores
- BackendAuthError -> estado FAILED, failed_phase="researching", failed_reason="auth", last_error/error guardados.
- BackendError (otros) -> estado FAILED, failed_phase="researching", failed_reason="error".
- InvalidTransitionError: si force, resetea a PENDING y reintenta; si no force, propaga.

## Idempotencia
- Si state es RESEARCHED/SYNTHESIZED/VALIDATED/WRITTEN/COMPLETED y raw_research.json existe y no force → retorna resultado cacheado sin llamar al backend.
- force=True: re-ejecuta y backupea raw_research.json anterior.

## Tests
- tests/test_research.py: 12 tests (FakeBackend), todos pasando.
- Cubren: persistencia de artefactos, idempotencia, force+backup, fallo marca failed, retry desde failed, transicion invalida, request minimo, fixtures, cleanup, latency, factory, protocolo.

## Archivos
- research.py: ResearchPhase, ResearchPhaseResult, run_research.
- tests/test_research.py: 12 tests.

## Resultado de tests
- 12/12 OK.
- py_compile OK.
