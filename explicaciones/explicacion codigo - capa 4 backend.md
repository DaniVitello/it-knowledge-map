# Explicacion codigo - Capa 4: Backend

## Que es la Capa de Backend
Interfaz de abstraccion (ResearchBackend) que separa al pipeline de la implementacion concreta de NotebookLM. Metodos: create_workspace/create_notebook, discover, import_discovered, add_urls, list_sources, wait_sources_ready, ask, delete_workspace/delete_notebook, workspace_exists, cleanup, research. Ningun otro modulo habla directamente con NotebookLM.

## FakeBackend
Backend sin red para tests y calibracion. Simula notebooks, fuentes y consultas. Determinista, idempotente, con fixtures opcionales y latencia configurable. Los 15 tests corren sobre el. Permite probar estados, persistencia, validacion y escritura sin gastar cuota ni romper la cuenta real.

## NotebookLMBackend
Adaptador real contra notebooklm-py v0.8.4 (API async). Usa NotebookLMClient.from_storage. Crea notebooks, investiga (research.start + wait_for_completion), importa fuentes, consulta (chat.ask), borra. Mapea errores de la libreria a excepciones tipadas (BackendAuthError, BackendRateLimitError, BackendTimeout, BackendNotFoundError, BackendNetworkError). Intercambiable: si falla, se puede usar modo de respaldo (sintesis solo desde fuentes locales).

## Conexion con state.py y writer.py
- state.py: guarda notebook_id al crear; verifica workspace_exists al reanudar; transiciones researching->researched; reintentos con backoff; al completar, notebook_id=None.
- writer.py: no habla con el backend. Escribe solo tras validacion aprobada. El notebook se borra solo despues de verificar la escritura (run_finalize).

## Que falta
1. Smoke test con cuenta real (scripts/smoke_notebooklm.py) para validar el adaptador y calibrar timeouts/pacing.
2. Modo de respaldo sin NotebookLM (sintesis solo desde fuentes locales).
3. Reconciliacion de notebooks huerfanos al arrancar.
4. Decision sobre persistencia de texto de fuentes (URL+hash+extracto vs texto completo).
5. Calibracion de max_per_notebook, max_per_domain, wait_timeout_s, source_ready_timeout_s.

## Archivos
- backend.py: interfaz, excepciones, FakeBackend, NotebookLMBackend, run_research_phase, create_backend, pipeline_dir, _map_library_error, _notebooklm_module.
- notebooklm_backend.py: re-export del adaptador real.
- scripts/smoke_notebooklm.py: smoke test con cuenta real.
- tests/test_backend.py: 15 tests (FakeBackend + integracion de estado), todos pasando.

## Resultado de tests
- 15/15 OK.
- py_compile OK.
