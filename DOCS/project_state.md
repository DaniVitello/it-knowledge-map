# project_state.md — Estado compartido entre sesiones de Hermes

> Archivo de estado del proyecto. Leerlo al inicio de cada sesión antes de tocar código.
> Actualizar las secciones 2 y 6 cada vez que se complete una capa.

- **Última actualización:** 2026-10-28
- **Autor de la última actualización:** sesión "Mente Gemela IT" (build)

---

## 1. Proyecto y ubicación

- **Nombre:** IT Career Concept Map — pipeline de enriquecimiento de conceptos IT
- **Ruta raíz:** `C:\Users\DGVit\Proyectos\IT Career`
- **Código (Python):** `C:\Users\DGVit\Proyectos\IT Career\it-concept-map`
- **Vault (fuente de verdad, solo lectura):** `C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map`
- **Python:** 3.11+ (venv en `IT Career\.venv`; `pyproject.toml` declara `pytest>=8.0` dev y `notebooklm-py` opcional)
- **Dependencias runtime:** `pyyaml>=6.0` (dev: `pytest>=8.0`)
- **Config principal:** `it-concept-map\config.yaml`
- **Docs de diseño:** `explicacion del proyecto por capas v1.md`, `explicacion del proyecto por capas v1 - pseudo codigo.md`

---

## 2. Estado actual

- **Capas completadas:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, A (contratos), B (integridad), C (higiene) y D (contexto por area)
- **Capa en curso proxima del plan de mejoras v1:** A contratos (siguiente foundational; dependencias: A -> B -> E/F/G -> H/I -> J -> K -> L)
- **Capas pendientes del plan de mejoras v1 (DOCS\plan de mejoras v1.md):** E, F, G, H, I, J, K, L
- **Capas pendientes de implementacion original:** (ninguna)

| # | Capa (implementación) | Estado |
|---|---|---|
| 1 | Registry + contratos de datos (`models.py`, `registry.py`) | ✅ Completada |
| 2 | State machine + persistencia (`state.py`) | ✅ Completada |
| 3 | Writer, escritura segura (`writer.py`) | ✅ Completada |
| 4 | Backend (interfaz + FakeBackend + NotebookLMBackend) | ✅ Completada |
| 5 | Investigación (`research.py`) | ✅ Completada |
| 6 | Síntesis (`synthesis.py` + prompts) | ✅ Completada |
| 7 | Validación (`validation.py`) | ✅ Completada |
| 8 | Orquestador (`runner.py` + logging) | ✅ Completada |
| 9 | CLI (cli.py) | Completada |
| 10 | Piloto + calibracion | Completada |
| D | Contexto por area (`areas.py` + `areas/*.yaml`) | ✅ Completada |

> Nota: la numbering de implementación fusiona las capas 1 y 2 del diseño pseudo-código
> (modelo de datos + lectura del vault) en la Capa 1 de implementación. El pseudo-código
> numera 11 capas; acá se cuentan 10.

---

## 3. Archivos clave creados hasta ahora

### Código (it-concept-map\)
- `models.py` — contratos de datos: dataclasses con `schema_version`, enums, excepciones
- `registry.py` — descubrimiento y lectura del vault, parseo de frontmatter, `key_ideas`, `connections`, hashes, contexto por área (`areas/<area>.yaml`)
- `state.py` — máquina de estados, transiciones válidas, persistencia JSON/SQLite, reanudación, reintentos con backoff
- `config.yaml` — configuración base (rutas, backend, marcadores, pacing, validación)
- `areas.py` — Capa D: cargador del contexto por área con merge de prioridad (concepto > área > frontmatter > defaults)
- `areas\*.yaml` — Capa D: 10 contextos de área (fuente de verdad generada desde `areas.json`)
- `pyproject.toml` — metadatos del proyecto y pytest
- `README.md` — documentación de la capa y uso rápido

### Documentación
- `explicacion del proyecto por capas v1.md` — orden y justificación de las capas
- `explicacion del proyecto por capas v1 - pseudo codigo.md` — pseudo-código de alto nivel
- `explicacion codigo - capa 1 registry y contratos.md` — detalle de la Capa 1
- `explicacion codigo - capa 2 state y persistencia.md` — detalle de la Capa 2
- `DOCS\learnings.md` — aprendizajes e ideas de mejora (ej. encoding en subprocess)

### Scripts auxiliares
- `generar_vault_it.py` — generación del vault de Obsidian
- `automate_frontend_concepts.py` — automatización de conceptos Frontend (NotebookLM)
- `add_ai_markers.py` — marcadores `ai:start`/`ai:end` en las notas

### Datos
- `IT-Mind-Map\` — vault con ~260 notas `.md` por área (fuente de verdad)
- `it-concept-map\workdir\` — se materializa en runtime (hoy no existe en disco)
- `skills-lock.json` — lock de skills

---

## 4. Conexión a OpenCode

- **Server:** `http://127.0.0.1:4096` (proceso `opencode`, PID 7620)
- **Session ID actual:** `ses_e9b3abd69ffeC74r3u1si2P0FY` ("Probemos algo", agente `build`)
- **Otra sesión del proyecto:** `ses_e9a05e5b8ffencCuF50jVawHwQ` ("Listing OpenCode sessions")
- **Project ID:** `2d391c104e73b92469c681b8d48e67e1964ab662`
- **Password (ubicación):** `C:\Users\DGVit\.config\opencode\service.json` → campo `password`
  (no commitear, no exponer en logs ni en commits)
- **Modelo:** `opencode/beam-free` (variant `high`)
- **DB:** `C:\Users\DGVit\.local\share\opencode\opencode.db`

---

## 5. Instrucciones para quien lee este archivo

### Qué hacer
- Leer este archivo al inicio de la sesión antes de modificar código.
- Trabajar el código dentro de `it-concept-map\`; el vault `IT-Mind-Map\` es solo lectura.
- Antes de implementar una capa, leer la explicación correspondiente en
  `explicacion codigo - capa N ...md` y el pseudo-código.
- Mantener `SCHEMA_VERSION = "1.0.0"` y los aliases de compatibilidad en `state.py`.
- Usar el venv `.venv` y Python 3.11+.
- Actualizar este archivo (secciones 2 y 6) al completar una capa.

### Qué no tocar
- `IT-Mind-Map\` (vault, fuente de verdad): no editar notas a mano ni regenerarlas.
- `.venv\`, `__pycache__\`, `workdir\`: artefactos generados, no versionar.
- Marcadores manuales del vault (`key_ideas`, `connections`, frontmatter): son fuente de verdad.
- `config.yaml` salvo que la capa en curso lo requiera explícitamente.
- Identidad de OpenCode (project ID, session IDs, password).

---

## 6. Historial de capas completadas

### Capa 1 — Registry + contratos de datos (2026-10-22)
- **Archivos:** `models.py`, `registry.py`, `config.yaml`, `pyproject.toml`, `README.md`
- **Resumen:** se definió el átomo del sistema (`ConceptMeta`) con enums (`Volatility`,
  `ConceptStatus`, `Severity`, `PromptContext`), `SCHEMA_VERSION`, y el registry que
  lee el vault sin escribirlo. Derivación por prioridad: override por concepto >
  override por área > frontmatter > cuerpo > defaults. Campos manuales nunca se
  sobrescriben. Sin acceso a disco de escritura ni red.

### Capa 2 — State machine + persistencia (2026-10-22)
- **Archivos:** `state.py` (812 líneas), `README.md` actualizado
- **Resumen:** máquina de estados con 9 estados y transiciones válidas, estados
  terminales (`completed`, `failed`, `needs_review`), persistencia JSON por concepto
  o SQLite, reanudación desde checkpoint, reconciliación de notebooks huérfanos y
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

### Capa C — Higiene de config, tests y arranque (2026-10-29)
- **Archivos:** `config.yaml`, `tests/test_backend.py`
- **Resumen:** eliminado el bloque muerto `validation:` de config.yaml (las secciones canonicas viven en validation.py, REQUIRED_SECTIONS). Eliminadas las claves muertas `generate_report` y `download` de `backend.notebooklm.timeouts` (no estan en NotebookLMBackend.DEFAULT_TIMEOUTS y se ignoraban). Eliminado el test vacio `test_persist_error_razon` (sin asserts; cubierto por test_fallo_marca_failed_con_razon). Verificado `py_compile` sobre todos los modulos.
- **Tests:** py_compile OK. pytest no instalado en el venv (verificacion por sintaxis).
