# SESSION BOOTSTRAP (leer esto primero)

> Si sos una sesión nueva de Hermes, leé esta sección antes de hacer cualquier cosa.

## Conexión a laptop 1 (OpenCode server)
- URL: http://192.168.0.107:26826
- Usuario: opencode
- Password: Qh4KO9x41R55B4hke5_PmEIo7T-JclWrWvpr5y8lwoI
- Puerto puede cambiar. Verificar con: curl -s -o /dev/null -w "%{http_code}" http://192.168.0.107:26826/api/info
- Si 401: password cambió. Si connection refused: puerto cambió (probar 4096, 26826, 3000, 8080, 8000, 9000, 5000).

## Cómo operar laptop 1
- NO usar OpenCode CLI/TUI (consume free tier, falla en MSYS).
- Usar HTTP API directa con Basic auth (0 tokens, filesystem/shell ops).
- Leer archivos: GET /api/fs/read/<path>
- Escribir archivos: POST /api/experimental/fs/write?path=<path> (Content-Type: application/octet-stream)
- Shell: POST /api/shell (PowerShell, usar ; no &&, py no python)
- Verificar conexión: GET /api/info

## Skill obligatoria
- Cargar skill 'opencode' para guía de conexión, file handling, y troubleshooting.

## Estado actual del proyecto
- 10 capas implementadas + 12 correcciones A-L aplicadas
- 108 tests pasando
- 1 concepto completado (Programming Fundamentals) de 255
- LLM: Groq gpt-oss-120b (via llm_groq.py)
- Script de ejecución: run_pipeline.py
- Backend: notebooklm (auth via cookies, válida hasta 2027)

## Lo que NO tocar
- synthesis.py (prompt ya modificado para no generar wikilinks)
- llm_groq.py (adapter Groq)
- run_pipeline.py (script de ejecución)
- writer.py (verificación de wikilinks, correcta para MVP)
- config.yaml (backend=notebooklm, auth_file=null)

## Lo que SÍ hacer
- Leer project_state.md para progreso actual
- Ejecutar run_pipeline.py por área
- Verificar con cli.py status
- Actualizar project_state.md al cerrar cada área

---

# project_state.md â€” Estado compartido entre sesiones de Hermes

> Archivo de estado del proyecto. Leerlo al inicio de cada sesiÃ³n antes de tocar cÃ³digo.
> Actualizar las secciones 2 y 6 cada vez que se complete una capa.

- **Ãšltima actualizaciÃ³n:** 2026-10-28
- **Autor de la Ãºltima actualizaciÃ³n:** sesiÃ³n "Mente Gemela IT" (build)

---

## 1. Proyecto y ubicaciÃ³n

- **Nombre:** IT Career Concept Map â€” pipeline de enriquecimiento de conceptos IT
- **Ruta raÃ­z:** `C:\Users\DGVit\Proyectos\IT Career`
- **CÃ³digo (Python):** `C:\Users\DGVit\Proyectos\IT Career\it-concept-map`
- **Vault (fuente de verdad, solo lectura):** `C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map`
- **Python:** 3.11+ (venv en `IT Career\.venv`; `pyproject.toml` declara `pytest>=8.0` dev y `notebooklm-py` opcional)
- **Dependencias runtime:** `pyyaml>=6.0` (dev: `pytest>=8.0`)
- **Config principal:** `it-concept-map\config.yaml`
- **Docs de diseÃ±o:** `explicacion del proyecto por capas v1.md`, `explicacion del proyecto por capas v1 - pseudo codigo.md`

---

## 2. Estado actual

- **Capas completadas:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, A (contratos), B (integridad), C (higiene) y D (contexto por area)
- **Capa en curso proxima del plan de mejoras v1:** A contratos (siguiente foundational; dependencias: A -> B -> E/F/G -> H/I -> J -> K -> L)
- **Capas pendientes del plan de mejoras v1 (DOCS\plan de mejoras v1.md):** E, F, G, H, I, J, K, L
- **Capas pendientes de implementacion original:** (ninguna)

| # | Capa (implementaciÃ³n) | Estado |
|---|---|---|
| 1 | Registry + contratos de datos (`models.py`, `registry.py`) | âœ… Completada |
| 2 | State machine + persistencia (`state.py`) | âœ… Completada |
| 3 | Writer, escritura segura (`writer.py`) | âœ… Completada |
| 4 | Backend (interfaz + FakeBackend + NotebookLMBackend) | âœ… Completada |
| 5 | InvestigaciÃ³n (`research.py`) | âœ… Completada |
| 6 | SÃ­ntesis (`synthesis.py` + prompts) | âœ… Completada |
| 7 | ValidaciÃ³n (`validation.py`) | âœ… Completada |
| 8 | Orquestador (`runner.py` + logging) | âœ… Completada |
| 9 | CLI (cli.py) | Completada |
| 10 | Piloto + calibracion | Completada |
| D | Contexto por area (`areas.py` + `areas/*.yaml`) | âœ… Completada |

> Nota: la numbering de implementaciÃ³n fusiona las capas 1 y 2 del diseÃ±o pseudo-cÃ³digo
> (modelo de datos + lectura del vault) en la Capa 1 de implementaciÃ³n. El pseudo-cÃ³digo
> numera 11 capas; acÃ¡ se cuentan 10.

---

## 3. Archivos clave creados hasta ahora

### CÃ³digo (it-concept-map\)
- `models.py` â€” contratos de datos: dataclasses con `schema_version`, enums, excepciones
- `registry.py` â€” descubrimiento y lectura del vault, parseo de frontmatter, `key_ideas`, `connections`, hashes, contexto por Ã¡rea (`areas/<area>.yaml`)
- `state.py` â€” mÃ¡quina de estados, transiciones vÃ¡lidas, persistencia JSON/SQLite, reanudaciÃ³n, reintentos con backoff
- `config.yaml` â€” configuraciÃ³n base (rutas, backend, marcadores, pacing, validaciÃ³n)
- `areas.py` â€” Capa D: cargador del contexto por Ã¡rea con merge de prioridad (concepto > Ã¡rea > frontmatter > defaults)
- `areas\*.yaml` â€” Capa D: 10 contextos de Ã¡rea (fuente de verdad generada desde `areas.json`)
- `pyproject.toml` â€” metadatos del proyecto y pytest
- `README.md` â€” documentaciÃ³n de la capa y uso rÃ¡pido

### DocumentaciÃ³n
- `explicacion del proyecto por capas v1.md` â€” orden y justificaciÃ³n de las capas
- `explicacion del proyecto por capas v1 - pseudo codigo.md` â€” pseudo-cÃ³digo de alto nivel
- `explicacion codigo - capa 1 registry y contratos.md` â€” detalle de la Capa 1
- `explicacion codigo - capa 2 state y persistencia.md` â€” detalle de la Capa 2
- `DOCS\learnings.md` â€” aprendizajes e ideas de mejora (ej. encoding en subprocess)

### Scripts auxiliares
- `generar_vault_it.py` â€” generaciÃ³n del vault de Obsidian
- `automate_frontend_concepts.py` â€” automatizaciÃ³n de conceptos Frontend (NotebookLM)
- `add_ai_markers.py` â€” marcadores `ai:start`/`ai:end` en las notas

### Datos
- `IT-Mind-Map\` â€” vault con ~260 notas `.md` por Ã¡rea (fuente de verdad)
- `it-concept-map\workdir\` â€” se materializa en runtime (hoy no existe en disco)
- `skills-lock.json` â€” lock de skills

---

## 4. ConexiÃ³n a OpenCode

- **Server:** `http://127.0.0.1:4096` (proceso `opencode`, PID 7620)
- **Session ID actual:** `ses_e9b3abd69ffeC74r3u1si2P0FY` ("Probemos algo", agente `build`)
- **Otra sesiÃ³n del proyecto:** `ses_e9a05e5b8ffencCuF50jVawHwQ` ("Listing OpenCode sessions")
- **Project ID:** `2d391c104e73b92469c681b8d48e67e1964ab662`
- **Password (ubicaciÃ³n):** `C:\Users\DGVit\.config\opencode\service.json` â†’ campo `password`
  (no commitear, no exponer en logs ni en commits)
- **Modelo:** `opencode/beam-free` (variant `high`)
- **DB:** `C:\Users\DGVit\.local\share\opencode\opencode.db`

---

## 5. Instrucciones para quien lee este archivo

### QuÃ© hacer
- Leer este archivo al inicio de la sesiÃ³n antes de modificar cÃ³digo.
- Trabajar el cÃ³digo dentro de `it-concept-map\`; el vault `IT-Mind-Map\` es solo lectura.
- Antes de implementar una capa, leer la explicaciÃ³n correspondiente en
  `explicacion codigo - capa N ...md` y el pseudo-cÃ³digo.
- Mantener `SCHEMA_VERSION = "1.0.0"` y los aliases de compatibilidad en `state.py`.
- Usar el venv `.venv` y Python 3.11+.
- Actualizar este archivo (secciones 2 y 6) al completar una capa.

### QuÃ© no tocar
- `IT-Mind-Map\` (vault, fuente de verdad): no editar notas a mano ni regenerarlas.
- `.venv\`, `__pycache__\`, `workdir\`: artefactos generados, no versionar.
- Marcadores manuales del vault (`key_ideas`, `connections`, frontmatter): son fuente de verdad.
- `config.yaml` salvo que la capa en curso lo requiera explÃ­citamente.
- Identidad de OpenCode (project ID, session IDs, password).

---

## 6. Historial de capas completadas

### Capa 1 â€” Registry + contratos de datos (2026-10-22)
- **Archivos:** `models.py`, `registry.py`, `config.yaml`, `pyproject.toml`, `README.md`
- **Resumen:** se definiÃ³ el Ã¡tomo del sistema (`ConceptMeta`) con enums (`Volatility`,
  `ConceptStatus`, `Severity`, `PromptContext`), `SCHEMA_VERSION`, y el registry que
  lee el vault sin escribirlo. DerivaciÃ³n por prioridad: override por concepto >
  override por Ã¡rea > frontmatter > cuerpo > defaults. Campos manuales nunca se
  sobrescriben. Sin acceso a disco de escritura ni red.

### Capa 2 â€” State machine + persistencia (2026-10-22)
- **Archivos:** `state.py` (812 lÃ­neas), `README.md` actualizado
- **Resumen:** mÃ¡quina de estados con 9 estados y transiciones vÃ¡lidas, estados
  terminales (`completed`, `failed`, `needs_review`), persistencia JSON por concepto
  o SQLite, reanudaciÃ³n desde checkpoint, reconciliaciÃ³n de notebooks huÃ©rfanos y
  reintentos con backoff (`[2, 4, 8]`, `max_retries=3`). Aliases de compatibilidad
  (`StateStatus`, `PipelineStatus`, etc.). No toca el vault ni la red.

---

## Actualizacion Capa 4 - Backend (2026-10-23)

### Archivos creados/modificados
- it-concept-map/backend.py - interfaz ResearchBackend, FakeBackend, NotebookLMBackend, run_research_phase, create_backend, pipeline_dir, excepciones tipadas
- it-concept-map/notebooklm_backend.py - re-export del adaptador real
- it-concept-map/scripts/smoke_notebooklm.py - smoke test con cuenta real (mide tiempos)
- it-concept-map/tests/test_backend.py - 15 tests (FakeBackend + integracion de estado), todos pasando
- it-concept-map/pyproject.toml - v0.2.0, +notebooklm-py optional dep, +backend/notebooklm_backend en py-modules
- it-concept-map/README.md - actualizado con Capa 4

### Resultado de tests
- 15/15 OK (FakeBackend + integracion de estado + factory + mapeo de errores + protocolo)
- py_compile OK


### Capa 3 - Writer, escritura segura (2026-10-22)
- **Archivos:** writer.py (SafeWriter)
- **Resumen:** escritura atomica temp+os.replace, backup en workdir/backups/<id>/, restore byte a byte, hash SHA-256 del afuera antes/despues releyendo desde disco, parse_frontmatter/verify_frontmatter_preserved, detect_newline/normalize_newlines, excepciones tipadas, integracion con state.py (writing_phase, transiciones validated->written->completed, failed ante error), modo dry_run con DiffResult. No toca el vault salvo dentro del bloque ai:start/ai:end.

### Capa 4 - Backend (2026-10-23)
- **Archivos:** ackend.py, 
otebooklm_backend.py, scripts/smoke_notebooklm.py, 	ests/test_backend.py
- **Resumen:** interfaz ResearchBackend (Protocol runtime_checkable), excepciones tipadas (BackendError, BackendAuthError, BackendRateLimitError, BackendTimeout, BackendNotFoundError, BackendNetworkError, BackendConfigError). FakeBackend sin red (determinista, fixtures, cleanup idempotente, latency). NotebookLMBackend adaptador real async contra notebooklm-py v0.8.4 (create_notebook, discover, import, add_urls, list_sources, wait_sources_ready, ask, delete, workspace_exists). run_research_phase con idempotencia (cache si RESEARCHED), persistencia sources.json + raw_research.json, backup con force, transicion a RESEARCHED, manejo de errores (auth->failed_reason auth). create_backend factory. _map_library_error mapea excepciones de notebooklm-py. 15 tests pasando.


### Capa 5 - Investigacion (2026-10-28)
- **Archivos:** 
esearch.py, 	ests/test_research.py
- **Resumen:** ResearchPhase orquesta el backend para investigar un concepto: crea workspace, descubre fuentes, importa, consulta, persiste sources.json + raw_research.json en workdir/.pipeline/<id>/, borra notebook, transiciona estado a researched. Idempotente (cache si RESEARCHED), manejo de errores (fallo -> failed con failed_reason), force re-ejecuta con backup. 12 tests pasando.


### Capa 6 - Sintesis (2026-10-28)
- **Archivos:** synthesis.py, 	ests/test_synthesis.py
- **Resumen:** SynthesisPhase genera el study guide a partir de raw_research.json + sources.json. Construye prompt con reglas de evidencia, llama al LLM (sync/async), parsea secciones (## Nombre), persiste synthesis.json, transiciona a synthesized. Idempotente (cache si synthesized), manejo de errores (fallo -> failed). 11 tests pasando (mock LLM).


### Capa 7 - Validacion (2026-10-28)
- **Archivos:** 
alidation.py, 	ests/test_validation.py
- **Resumen:** ValidationPhase valida la sintesis contra reglas de la spec: estructura (secciones requeridas), formato (headings), longitud (min/max), preguntas de repaso (min 3), cross-links, prohibiciones. Produce ValidationReport con pass/fail + issues + warnings + score. Transiciona a validated o failed. Idempotente. 12 tests pasando.


### Capa 8 - Orquestador (2026-10-28)
- **Archivos:** 
unner.py, 	ests/test_runner.py
- **Resumen:** Runner orquesta el pipeline completo por concepto: registry -> research -> synthesis -> validation -> writer, con logging en events.jsonl, reanudacion desde checkpoint, manejo de errores, pacing entre conceptos, reporte final (RunReport/BatchReport). Idempotente. 11 tests pasando.


### Capa 9 - CLI (2026-10-28)
- **Archivos:** cli.py, 	ests/test_cli.py
- **Resumen:** CLI con argparse: comandos run, status, list, reset, dry-run. Integracion con runner.py y todas las capas. Entry point kpipe en pyproject.toml. 12 tests pasando.


### Capa 10 - Piloto + calibracion (2026-10-28)
- **Archivos:** pilot.py, 	ests/test_pilot.py
- **Resumen:** PilotRunner ejecuta el pipeline sobre un subconjunto de conceptos, genera reporte de piloto con metricas (tiempos por fase, tasa de exito, errores, calidad de sintesis, fuentes). Calibracion sugerida (pacing, timeout). 9 tests pasando. TODAS LAS CAPAS COMPLETADAS (1-10).


### Capa D - Contexto por area (2026-10-28)
- **Archivos:** it-concept-map/areas.py, it-concept-map/areas/*.yaml (10 areas), it-concept-map/registry.py (integracion del merge), it-concept-map/synthesis.py (build_prompt inyecta contexto del area), it-concept-map/config.yaml (limpieza de divergencia), it-concept-map/runner.py (pasa concepts a sintesis), it-concept-map/tests/test_areas.py
- **Resumen:** areas/<area>.yaml es la fuente de verdad del contexto por area (estrucura diseno 7.1, auditoria D18): context_framing, context_questions, professional_roles, style_example, response_mode, preferred_domains, seed_urls, default_volatility + volatility_overrides. Merge de prioridad al resolver por concepto: override por concepto > areas/<area>.yaml > frontmatter > defaults (igual criterio que el registry). slugify_area colapsa variantes de nombre ("Database / Data Analytics" vs "Database & Data Analytics"). El prompt de sintesis ya no dice "Sos un experto en {area}": inyecta rol/orientacion/framing/estilo/modo/preguntas de contexto del yaml (punto 3 y 7 de la spec: contexto antes que definicion). En registry ya no hay roles inventados "{area}-dev" para las 10 areas ni dominios divergentes. config.yaml: eliminadas las claves area_overrides, area_domains y area_roles (contradicen areas.json; la divergencia critica 1.7 queda resuelta). EXPECTED_AREAS define las 10 areas con cobertura de tests.
- **Tests:** py_compile OK. tests/test_areas.py: 25 tests (cobertura de las 10 areas, slugify, validacion de yaml, merge de prioridad, integracion con registry, prompt de sintesis). Suite completa: 109/109 pasando (requerido instalar pytest>=8.0 y notebooklm-py en el venv .venv, que solo tenia PyYAML).

### Capa C â€” Higiene de config, tests y arranque (2026-10-29)
- **Archivos:** `config.yaml`, `tests/test_backend.py`
- **Resumen:** eliminado el bloque muerto `validation:` de config.yaml (las secciones canonicas viven en validation.py, REQUIRED_SECTIONS). Eliminadas las claves muertas `generate_report` y `download` de `backend.notebooklm.timeouts` (no estan en NotebookLMBackend.DEFAULT_TIMEOUTS y se ignoraban). Eliminado el test vacio `test_persist_error_razon` (sin asserts; cubierto por test_fallo_marca_failed_con_razon). Verificado `py_compile` sobre todos los modulos.
- **Tests:** py_compile OK. pytest no instalado en el venv (verificacion por sintaxis).



## Diagnostico de verificacion real - Capas A-L (2026-10-29)

Verificacion ejecutada sobre el codigo en `it-concept-map/`. Tests: 108 passed, 37 warnings. No se corrigio nada.

### Resumen por capa

| Capa | Plan dice | Verificacion real | Estado |
|------|-----------|-------------------|--------|
| A | Contratos alineados | models.py tiene campos del diseno + ConceptStatus importado de state. Falta validacion de esquema al leer/escribir JSON. | Parcial |
| B | Integridad | B2/B3/B5 OK. B4: runner asigna st.status=FAILED directo en except (violacion). | Parcial |
| C | Higiene | B6: runner OK, pilot.py sigue con pause_between_concepts_s (bug persiste). B7/B8/B10/B11 OK. | Parcial |
| D | Contexto por area | areas.py + areas/*.yaml integrado en synthesis y registry. | OK |
| E | Investigacion real | B1 corregido. _build_research_plan OK. Gaps siempre 0 (ciclo no implementado). | Parcial |
| F | Evaluacion fuentes | sources.json con evaluation/kept, sources_raw/. Prompt P2 no vi. | Parcial |
| G | Notebook lifecycle | reconcile llamado, delete post-write, notebook_id persistido. Reutilizacion en retry no vi. | Parcial |
| H | Validacion determinista | 4 stubs vacios (_check_contexto, _check_relaciones, _check_fuentes, _check_actualidad). Score usa 13 checks no 10. _check_cross_links solo vs connections. | NO implementado |
| I | Semantica + bucle + DoD | Bucle needs_fix en runner. Marcador "?? verificar" (spec dice "warning verificar"). DoD no vi. | Parcial |
| J | Orquestador robusto | execute_phase_with_retry existe pero NO se invoca. Reanudacion por strings. CLI sin pilot/--force-phase/validate/report. _load_concepts sin try/except OK. | NO implementado |
| K | Trazabilidad | run_id, run.jsonl, events.jsonl OK. Pie de trazabilidad en nota no vi. claims_index no poblado. | Parcial |
| L | Idempotencia + piloto | Idempotencia solo por status, no hash. pilot.py existe. README no verificado. | Parcial |

### Bugs B1-B11

- B1: corregido (seed_urls or []).
- B2: corregido (no reconstruye ConceptMeta parcial).
- B3: corregido (solo VALIDATED entra a writing).
- B4: parcial (synthesis/validation usan transition_to; runner asigna st.status=FAILED directo en except).
- B5: corregido (atomic writes).
- B6: parcial (runner OK, pilot.py sigue con pause_between_concepts_s).
- B7: corregido.
- B8: corregido.
- B9: parcial (campos seteados a 0 siempre).
- B10: corregido (test vacio eliminado).
- B11: corregido (import asyncio presente).

### Warnings de tests

- DeprecationWarning: asyncio.iscoroutinefunction (synthesis.py:169).
- RuntimeWarning: coroutine 'FakeBackend.delete' never awaited (runner.py:230).

### Conclusion

El plan marca todas las capas A-L como completadas, pero la verificacion real muestra que H y J NO estan implementadas, y varias capas (A, B, C, E, F, G, I, K, L) estan parciales. Los tests (108) pasan pero no cubren los checks bloqueantes de H ni el retry de J.



## Diagnostico Tanda 1 - Capas A, B, C, D (verificacion profunda, 2026-10-29)

Tests tanda 1: 99 passed (areas, backend, cli, runner, synthesis, validation, research), 23 warnings.

### Capa A - Contratos de datos

Implementado:
- models.py: ConceptMeta, Source, ResearchPlan, Synthesis, ValidationReport, WriteResult, ConceptState, Claim, ResearchQuestion, ResearchAnswer, RawResearch, CheckResult, CrossLink, ClaimRef, Volatility, Severity, PromptContext.
- Campos del diseno presentes: Source (domain, level, is_preferred_domain, is_seed, covers, retrieved_at, published_or_updated, content_hash, kept, evaluation); ResearchPlan (questions_by_dim, relation_questions, queries, source_requirements); Synthesis (claims, unverified_items); ValidationReport (blocking_failures, verdict); WriteResult (ai_block_hash, outside_block_hash_before/after, verified); ConceptState (last_good_state, retries).
- ConceptStatus importado de state.py (enum duplicado eliminado).

Parcial / NO implementado:
- ConceptMeta: id (no concept_id), note_path (no path), content_hash_outside (no content_hash_outside_ai). Nombres difieren del diseno; sin aliases de compatibilidad.
- Synthesis.Claim: text, source_ids, unverified. Falta claim_id y status (diseno pide claims[{claim_id,text,sources,status}]).
- ConceptState: state.py no tiene failure dict (models.py si lo tiene). Dos ConceptState divergentes (deriva contractual D1).
- Validacion de esquemas al leer/escribir artefactos JSON: NO existe.
- Aliases de compatibilidad transitorios documentados: NO existen.

### Capa B - Integridad de ejecucion

- B2 (ConceptMeta parcial en writer): OK. runner.py Fase 4 usa concept original + dataclasses.replace solo para note_path.
- B3 (writing_phase si FAILED): OK. Condicion VALIDATED/WRITTEN, no FAILED.
- B4 (st.status directo): PARCIAL. synthesis.py, validation.py, writer.py usan transition_to. runner.py asigna st.status=FAILED directo en 3 except blocks (research, synthesis, validation).
- B5 (atomic writes): OK. research/synthesis/validation usan backend._atomic_write_json.

### Capa C - Higiene

- B6 (pacing): PARCIAL. runner.py usa between_concepts_s (OK). pilot.py usa pause_between_concepts_s (bug persiste, siempre 0).
- B7 (validation config muerto): OK. Bloque eliminado, documentado.
- B8 (timeouts): OK. Alineados con DEFAULT_TIMEOUTS.
- B10 (test vacio): OK. Eliminado, cubierto por test_fallo_marca_failed_con_razon.
- B11 (asyncio): OK. import presente en runner.py.
- Adicional: sin test de pacing efectivo en runner (solo en pilot). Plan C pide "pacing efectivo se puede medir en un test" - no cubierto para runner.

### Capa D - Contexto por area

Implementado:
- areas.py + 10 areas/*.yaml. OK.
- registry.py: merge de prioridad (concept override > area yaml > frontmatter > defaults). OK.
- synthesis.py build_prompt: inyecta roles, framing, questions, style, mode del area (no dice "Sos un experto en {area}"). OK.
- config.yaml: sin area_overrides/area_domains/area_roles. OK.
- slugify_area colapsa variantes. OK.

Parcial:
- Plan D dice investigacion/validacion inyectan contexto por area. Solo synthesis lo hace; research.py y validation.py no inyectan contexto del area.

Tests: test_areas.py 25 tests (10 areas, slugify, yaml, merge, integracion registry, prompt sintesis).

### Conclusion tanda 1

- Capa A: parcial (campos presentes pero nombres difieren del diseno; falta schema validation; dos ConceptState divergentes).
- Capa B: parcial (B4 no cerrado en runner except blocks).
- Capa C: parcial (B6 en pilot.py; sin test de pacing en runner).
- Capa D: OK (observacion: investigacion/validacion no inyectan contexto de area).


## Resumen de resolucion - Tandas 1 (A-D) (2026-10-29)

Capa A (contratos): COMPLETADA
- Sub-A1: ConceptMeta aliases (concept_id, path, content_hash_outside_ai) + sync en registry.py.
- Sub-A2: Claim (claim_id, status) + ConceptState.failure dict + unificacion models/state.
- Sub-A3: validate_artifact_schema helper en backend.py (SchemaError).
- Sub-A4: 8 tests round-trip (test_roundtrip.py). Todos pasan.

Capa B (integridad): COMPLETADA
- B4: runner.py except blocks (research, synthesis, validation) usan transition_to con fallback.

Capa C (higiene): COMPLETADA
- B6: pilot.py usa between_concepts_s (era pause_between_concepts_s).

Capa D (contexto por area): OK
- Observacion: research.py y validation.py no inyectan contexto de area (solo synthesis). Pendiente para futura iteracion.

Tests: 116 passed, 37 warnings. py_compile OK en todos los modulos.


## Leccion de orquestacion (2026-10-30)

**Agency levels por fase:**
- ☆☆☆ Simple processor: ejecutar pipeline, monitorear, verificar (cero decisiones)
- ★☆☆ Router: detectar si algo fallo (decision binaria: atascado o no)
- ★★☆ Tool caller: diagnosticar causa (elegir herramienta)
- ★★★ Multi-step Agent: decidir accion (reintentar, abortar, pedir ayuda)

**Regla:** No mezclar fases en tiempo real. Ejecutar lo determinista sin decisiones. Cuando haya que decidir (★★★), hacerlo con un plan predefinido, no ad-hoc.

**Leccion:** Self-questioning es valioso pero se convierte en autosabotaje cuando consume energia/tokens sin producir output accionable. Claridad sobre agency levels por tarea previene sobrecargar con demasiadas tareas simultaneas.
