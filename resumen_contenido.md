# Resumen de contenido — IT Career

_Generado: 2026-10-28 · Ámbito: `C:\Users\DGVit\Proyectos\IT Career` · Secciones: raíz, DOCS, explicaciones, it-concept-map, IT-Mind-Map · Excluye: `.venv`, `__pycache__`, `.pyc`_

**Total de archivos procesados: 323** (283 `.md` · 26 `.py` · 10 `.txt` · 2 `.yaml` · 1 `.json` · 1 `.toml`)

| # | Sección | Archivos | Contenido |
|---|---------|----------|-----------|
| 1 | Raíz | 14 | 10 packs de conceptos (.txt), 3 scripts Python generadores/automatizadores, 1 lockfile de skills |
| 2 | DOCS | 6 | Documentación del pipeline `it-concept-map`: estado, auditoría, plan de mejoras y diseño |
| 3 | explicaciones | 10 | Explicación por capas (1–10) del código del pipeline |
| 4 | it-concept-map | 27 | Código fuente del pipeline (12 módulos + config + docs), tests y backups descartados |
| 5 | IT-Mind-Map | 266 | Vault de Obsidian: índice maestro + 10 áreas temáticas (255 conceptos) |

En conjunto, el repositorio contiene **dos cosas conectadas**: (1) un vault de aprendizaje de conceptos de TI en Obsidian (`IT-Mind-Map`, con 10 áreas de 25–30 conceptos cada una) generado a partir de los packs de conceptos en la raíz, y (2) un pipeline Python (`it-concept-map`) que enriquece esas notas de forma automatizada con investigación (NotebookLM/LLM) y escritura segura.

---


## 1. Raíz (14 archivos)

### AI Engineering — 25 conceptos funda.txt
- **Título:** AI Engineering (25 conceptos)
- **Propósito:** Archivo fuente en formato tabla (número, concepto, qué abarca) con los conceptos fundamentales de AI Engineering, distinguiéndolo del ML Engineering clásico por su foco en construir productos alrededor de modelos existentes, especialmente LLMs.
- **Puntos clave:**
  - Fundamentos base: ML fundamentals, redes neuronales, Transformers, álgebra lineal y probabilidad.
  - Temas centrales de LLMs: LLM APIs, prompt engineering, structured outputs, tool calling, RAG, embeddings y vector databases.
  - Temas de sistemas: agents, AI workflows, context engineering, memory, evaluation y AI system architecture.
  - Temas de producción: AI safety & security, observability, infraestructura (GPUs, inference servers) y fine-tuning (LoRA, distillation).

### Backend moderno — 25 conceptos fund.txt
- **Título:** Backend moderno (25 conceptos)
- **Propósito:** Archivo fuente con los conceptos fundamentales del desarrollo Backend, enfocado en datos, lógica, seguridad, concurrencia y sistemas distribuidos.
- **Puntos clave:**
  - Bases web y servidor: cliente-servidor, HTTP, runtime, routing, middleware y APIs (REST, RPC, GraphQL).
  - Datos: bases de datos, SQL, modelado, ORM, transacciones (ACID).
  - Seguridad y acceso: autenticación (JWT, OAuth), autorización (RBAC/ABAC) y seguridad web (CORS, CSRF, injection).
  - Escala: caching, mensajería (queues, pub/sub), observabilidad, deploy con Docker/CI-CD y sistemas distribuidos.

### Database  Data Analytics — 25 conce.txt
- **Título:** Database / Data Analytics (25 conceptos)
- **Propósito:** Archivo fuente que cubre desde bases de datos relacionales hasta la cadena completa de análisis de datos, modelado y business intelligence.
- **Puntos clave:**
  - SQL y modelado: queries, filtering/aggregation, JOINs, keys & constraints, normalización e índices.
  - Transacciones y motor interno: ACID, isolation, storage/query engine.
  - Más allá de lo relacional: NoSQL, data warehouses, OLTP vs OLAP, ETL/ELT y data pipelines.
  - Analítica: data quality y cleaning, estadística, analytics metrics (KPIs), visualización, BI y lakehouse/streaming.

### Frontend moderno — 25 conceptos fun.txt
- **Título:** Frontend moderno (25 conceptos)
- **Propósito:** Archivo fuente con el roadmap completo de Frontend, desde HTTP/HTML/CSS hasta arquitectura de aplicaciones.
- **Puntos clave:**
  - Fundamentos: Internet/Web, HTML semántico, CSS (cascade, box model), layout (Flexbox/Grid) y DOM.
  - JavaScript: desde sintaxis básica hasta closures, eventos, asincronía (event loop) y Web APIs.
  - Aplicaciones: TypeScript, componentización, frameworks UI (React, Vue, Angular), estado, routing, formularios y data fetching.
  - Producción: autenticación en frontend, accesibilidad, testing, performance (Web Vitals), rendering (SSR/SSG/hydration) y arquitectura.

### Networking  Internet — 25 conceptos.txt
- **Título:** Networking / Internet (25 conceptos base)
- **Propósito:** Archivo fuente que explica cómo funciona Internet desde adentro: protocolos, direccionamiento, transporte y aplicación.
- **Puntos clave:**
  - Capa de red y transporte: IP (IPv4/IPv6), TCP vs UDP, puertos, DNS, DHCP, MAC/ARP, routing, routers y NAT.
  - Organización: subnetting/CIDR y modelo OSI/TCP-IP.
  - Capa web: HTTP, HTTPS/TLS, request/response, métodos, status codes, headers y cookies.
  - Comunicación y tráfico: WebSockets, proxies/reverse proxies, firewalls y CDN/load balancing.

### Operating Systems  Linux — 25 conce.txt
- **Título:** Operating Systems / Linux (25 conceptos)
- **Propósito:** Archivo fuente sobre cómo funciona un sistema operativo (kernel, procesos, memoria) y el uso práctico de Linux y su CLI.
- **Puntos clave:**
  - Núcleo del SO: kernel, processes, threads, CPU scheduling, memory management (RAM, virtual, stack/heap).
  - Archivos y permisos: file systems, users & groups, permissions (read/write/execute).
  - Interfaz e interacción: system calls, I/O, IPC, sockets, environment variables, shell, Linux CLI y Bash scripting.
  - Operación: signals, daemons, package management, logs/monitoring, containers (Docker) y virtualización.

### Product Management — 25 conceptos.txt
- **Título:** Product Management (25 conceptos)
- **Propósito:** Archivo fuente centrado en pensar el producto: qué construir, para quién, con qué valor y cómo se mide.
- **Puntos clave:**
  - Descubrimiento: product thinking, problem discovery, user research, market research, personas y value proposition.
  - Estrategia: product vision, strategy, goals, roadmap, priorización y requirements/user stories.
  - Validación: discovery, MVP, experimentación (A/B testing) y metrics (funnels, retention, analytics).
  - Negocio y escala: product-market fit, lifecycle, stakeholder management, go-to-market y estrategia de portfolio.

### Project Management — 25 conceptos.txt
- **Título:** Project Management (25 conceptos)
- **Propósito:** Archivo fuente centrado en cómo coordinar el trabajo para producir el proyecto (no qué construir), con una nota introductoria sobre ese cambio de foco.
- **Puntos clave:**
  - Definición del trabajo: scope, requirements, deliverables y Work Breakdown Structure.
  - Ejecución: task management, dependencies, estimation, planning, scheduling y resource management.
  - Control: risk/issue/change management, status & reporting, budget y project metrics (velocity, cycle time).
  - Marcos y equipo: Agile, Scrum y Kanban, más stakeholders, retrospectivas y mejora continua.

### Software Engineering — 30 conceptos.txt
- **Título:** Software Engineering (30 conceptos)
- **Propósito:** Archivo fuente generalista que cubre fundamentos de programación, diseño, calidad e ingeniería de sistemas, con 30 ítems en lugar de 25.
- **Puntos clave:**
  - Fundamentos: programming basics, data structures, algorithms, complexity (Big O), OOP y programación funcional.
  - Diseño: abstracción, modularidad, API design, design patterns, SOLID y architecture.
  - Calidad: error handling, testing, debugging, code review, refactoring, clean code y documentación.
  - Operación: Git, CI/CD, security, observability, reliability, distributed systems y leadership técnico.

### UX  UI — 25 conceptos fundamentales.txt
- **Título:** UX / UI (25 conceptos)
- **Propósito:** Archivo fuente que distingue UX (cómo funciona y se experimenta el producto) de UI (cómo se materializa visualmente), con nota introductoria al respecto.
- **Puntos clave:**
  - Investigación: human-centered design, user research, needs/pain points, personas, user journeys e information architecture.
  - Diseño: interaction design, user flows, wireframing, prototyping y navegación.
  - UI visual: visual hierarchy, tipografía, color, spacing/layout, design systems y componentes con estados/feedback.
  - Evaluación: responsive design, accesibilidad (WCAG), usabilidad, usability testing, UX metrics y psicología del comportamiento.

### add_ai_markers.py
- **Título:** Marcador de contenido AI en notas del vault
- **Propósito:** Recorre todas las notas .md del vault `IT-Mind-Map` y envuelve el contenido de la sección "## Mis notas" entre los comentarios HTML `<!-- ai:start -->` y `<!-- ai:end -->`.
- **Puntos clave:**
  - Idempotente: si la nota ya tiene ambos marcadores, la salta.
  - Usa una regex con modo DOTALL para localizar el bloque de "Mis notas" (delimitado por el próximo `## `, `---` o fin de archivo).
  - Reescribe todo el archivo solo cuando aplica el marcador, con encoding UTF-8 y saltos `\n`.
  - Imprime un resumen con contadores ok/skip/err.

### automate_frontend_concepts.py
- **Título:** Automatización de study guides de Frontend vía NotebookLM
- **Propósito:** Orquesta el ciclo completo para conceptos del área Frontend (por defecto 2..6): crea un notebook en NotebookLM, corre research profundo, genera un study guide, lo descarga y lo integra en la nota correspondiente del vault.
- **Puntos clave:**
  - No usa librería externa: invoca el módulo `notebooklm` por CLI con `subprocess.run` y timeouts por paso.
  - Parsea cada nota md con regex para extraer el título (del frontmatter `title:`) y los ítems de "Qué abarca", que arma la query de research.
  - El merge reemplaza el placeholder `## Mis notas` por la guía descargada, con `time.sleep(2)` entre conceptos.
  - Reporta un resumen final OK/FAIL por concepto y sigue ante fallos parciales (ej. research fallido no aborta).

### generar_vault_it.py
- **Título:** Generador del vault de Obsidian del mind map IT
- **Propósito:** Script principal del proyecto: lee los .txt de conceptos (uno por área) y genera la estructura completa del vault `IT-Mind-Map` en Obsidian con notas de concepto, índices por área y un índice maestro.
- **Puntos clave:**
  - Tabla de 10 áreas predefinidas (prefijo → carpeta/ID/etiquetas) y bloque `GROUPS` que define relaciones curadas entre conceptos vía tokens tipo `be12`, `se28`.
  - `parse_txt` es tolerante: acepta filas separadas por tabs o espacios múltiples, lee títulos tal cual (sin reescritura) y advierte numeración irregular.
  - Agrega relaciones automáticamente por títulos normalizados iguales entre áreas distintas; render usa frontmatter con tags `it/<slug>`, sección "Qué abarca", "Mis notas", "Relacionados" y navegación prev/next.
  - Protección de contenido: las notas de concepto NO se pisan si ya existen (solo con `--force`); los índices y el maestro se regeneran siempre. Solo librería estándar (Python 3.8+).

### skills-lock.json
- **Título:** Lockfile de skills instaladas
- **Propósito:** Registro de las 3 skills de agente instaladas y su contenido, estructura tipo lockfile con versión y repositorio de origen.
- **Puntos clave:**
  - Las 3 skills (`interview-me`, `planning-and-task-breakdown`, `spec-driven-development`) provienen del mismo repo GitHub: `addyosmani/agent-skills`.
  - Cada entrada apunta a su ruta relativa (`skills/<nombre>/SKILL.md`) y guarda un hash SHA-256 (`computedHash`) de verificación.
  - `version: 1` indica el formato del lockfile.

---


## 2. DOCS (6 archivos)

### project_state.md
- **Título:** Estado compartido del proyecto entre sesiones
- **Propósito:** Archivo de checkpoint que se lee al inicio de cada sesión de OpenCode antes de tocar código del pipeline `it-concept-map`. Registra el progreso por capas, archivos clave e instrucciones de trabajo.
- **Puntos clave:**
  - **Proyecto:** IT Career Concept Map — pipeline de enriquecimiento de conceptos IT sobre un vault de Obsidian (`IT-Mind-Map\`, ~260 notas, solo lectura como fuente de verdad); código en `it-concept-map\` (Python 3.11+, venv, `config.yaml`).
  - **Estado:** las 10 capas de implementación están completadas (registry/modelos, state machine, writer, backend, investigación, síntesis, validación, orquestador, CLI y piloto+calibración), con nota de que el pseudo-código numera 11 capas y la implementación fusiona dos en la Capa 1.
  - **Historial:** máquina de estados con 9 estados y transiciones validadas, writer con escritura atómica + backup + verificación byte a byte, backend NotebookLM async con FakeBackend, suites de tests verdes por capa (9–15 tests cada una).
  - **Reglas de trabajo:** actualizar las secciones 2 y 6 al completar una capa, mantener `SCHEMA_VERSION = "1.0.0"`, no tocar el vault, `.venv`, marcadores manuales ni los datos de sesión/secretos del backend.
  - **Contexto técnico:** conexión a servidor OpenCode local (puerto 4096), trabajo con agente `build`, lectura del vault sin escribirlo salvo dentro del bloque `ai:start/ai:end`.

### plan de mejoras v1.md
- **Título:** Plan de 12 mejoras (capas A–L) post-auditoría
- **Propósito:** Plan de corrección del pipeline basado en la auditoría spec vs implementación (23 diferencias, 8 críticas, 11 bugs). Organiza el trabajo en 12 capas (A–L), cada una ejecutada en una sesión nueva de OpenCode para evitar context rot.
- **Puntos clave:**
  - **Diagnóstico central:** lo mecánico (writer, state machine, backend) está sólido; lo cognitivo (investigar de verdad, evaluar fuentes, no inventar) está casi vacío, con bugs concretos, config muerta y deriva contractual entre impl y spec.
  - **Regla de trabajo:** una capa = una sesión nueva y limpia; el plan vive en disco (no en memoria del chat); cierre por capa con tests verdes + `project_state.md` actualizado; trazabilidad y rollback por capa.
  - **Capas A–L:** A contratos de datos alineados al diseño; B integridad (4 bugs que corrompen escritura o desactivan defensas); C higiene de config/tests (`asyncio` sin importar, pacing roto); D contexto por área (`areas.json`); E investigación real (bug de seeds que impide subir fuentes, prompt P1); F evaluación/conservación de fuentes (prompt P2, `sources_raw/`); G ciclo de vida del notebook (borrar solo tras verificación); H validación determinista (checks bloqueantes que hoy son stubs); I validación semántica P5 + bucle `needs_fix`/`rejected` + DoD; J orquestador robusto (retry/reanudación reales); K trazabilidad (`run_id`, `run.jsonl`, pie de trazabilidad); L idempotencia con hash + piloto GO/NO-GO + limpieza.
  - **Los 11 bugs:** los más peligrosos son B1 (`seed_urls` jamás se suben al notebook) y B2 (runner reconstruye `ConceptMeta` parcial y desactiva la defensa de edición concurrente justo antes de escribir); B6+B11 forman una "bomba de dos mangas" (arreglar el pacing sin importar `asyncio` rompe `run_batch`).
  - **Orden de ejecución:** A primero (cimentación de contratos) → B+C (estabilizar) → D+E+F+G (reconstruir lo cognitivo) → H+I (barrera de calidad) → J → K → L; notas sobre por qué no seguir el orden estricto de la auditoría (validar sin fuentes no valida nada).

### learnings.md
- **Título:** Aprendizajes e ideas de mejora
- **Propósito:** Bitácora de errores y soluciones técnicas encontrados durante el desarrollo, para no repetirlos. Registra problemas puntuales con causa y fix.
- **Puntos clave:**
  - **Error registrado (2026-10-22):** `UnicodeDecodeError: 'charmap' codec can't decode byte 0x90` al automatizar notebook con `notebooklm-py` vía CLI en `automate_frontend_concepts.py`.
  - **Causa:** `subprocess.run(..., text=True)` usa el encoding por defecto del sistema; en Windows es `cp1252`, pero la CLI de NotebookLM imprime UTF-8 (tildes, emojis). Responsabilidad del wrapper, no del servicio.
  - **Fix:** pasar explícitamente `encoding="utf-8"` y `errors="replace"` al subprocess.
  - **Idea de mejora:** centralizar la invocación del CLI del backend en un helper único para no repetir el bug, y considerar usar la API Python directa de `notebooklm` (en vez de la CLI/subprocess) — decisión que se reflejó después en el diseño del backend async.
  - **Contexto:** notebooklm-py v0.8.4, conceptos Frontend 02–06 (HTML, CSS, Layout, DOM, JavaScript).

### auditoria_spec_vs_impl.md
- **Título:** Auditoría spec/diseño técnico vs implementación
- **Propósito:** Comparación punto por punto entre la especificación maestra (977 líneas), el diseño técnico del pipeline (654 líneas) y el código de `it-concept-map`. Documenta diferencias con evidencia (archivo:línea) y prioridades de corrección.
- **Puntos clave:**
  - **Veredicto:** la implementación existe y es funcional, pero hay **deriva contractual** importante: los dataclasses, artefactos JSON y hasta los tests usan vocabulario propio de la impl (`id/note_path`, `Source(kind=...)`, `is_valid/issues`, `WriteResult{outside_hash/inside_hash}`) que no coincide con los esquemas del diseño/spec — y los tests refuerzan esa deriva ocultándola.
  - **Diferencias críticas:** validación mucho menos exigente que el diseño (checks de contexto, actualidad, integridad y seguridad de archivo ausentes; sin veredicto `approved|needs_fix|rejected`); logging sin `run_id` ni eventos de fuentes/validación (solo inicio/fin de fase); 4 fases ejecutables vs 11 fases [A]–[K] del diseño; backups y artefactos en rutas distintas a las del diseño; reportes sin `needs_review` ni causa por fallo.
  - **Lo que SÍ está alineado:** nombres de estados y transiciones, backup + escritura atómica + restore byte a byte + dry-run, marcadores `ai:start/end`, gestión de gaps/`unverified`, `prompt_version`/hash, no escribir fuera del bloque.
  - **Prioridades sugeridas:** 1) alinear contratos de datos; 2) completar checks de validación + veredicto con `blocking_failures`; 3) completar logging (`run_id`, `run.jsonl`); 4) reorganizar fases o documentar el agrupamiento; 5) mover backups a `.pipeline/`, persistir `meta.json` y `research_plan.json`.
  - **Extras detectados:** tres ordenamientos de capas conviviendo (D16), CLI sin comandos `pilot`/`validate`, config único vs `areas/<area>.yaml` del diseño (D18), piloto con métricas propias sin diagnóstico de calidad, y principio rector del diseño (integridad > correctitud > fuentes...) no detectado en código/config.

### explicacion del proyecto por capas v1.md
- **Título:** Diseño técnico completo del pipeline por capas (con pseudo-código comentado)
- **Propósito:** Documento de diseño madre (~4840 líneas según la auditoría) que explica las 11 capas del pipeline: qué se hace, por qué, cómo, con dataclasses, pseudo-código real en Python y reglas de negocio de la spec en cada capa. Es la referencia que la implementación debe seguir.
- **Puntos clave:**
  - **Estructura (11 capas):** 1) modelo de datos `ConceptMeta` (átomo: identidad, metadatos manuales, volatilidad, hashes `outside/inside`, reglas de derivación por precedencia); 2) vault como fuente de verdad (lectura segura, scan, marcadores); 3) state machine (estados, transiciones validadas, checkpoint/reanudación, backoff `[2,4,8]`); 4) backend (`ResearchBackend` Protocol, FakeBackend determinista, NotebookLMBackend async con timeouts, circuit breaker, factory `create_backend`); 5) writer seguro (backup, escritura atómica `os.replace`, verificación byte a byte, 11 excepciones tipadas); 6) investigación (`ResearchContext`, grupos a/b/c, estrategia de fuentes con seeds/preferred/blocked, ciclo de cobertura con gaps, dedup y cap); 7) síntesis (prompts versionados por contexto, 7 secciones requeridas, separación fundamento estable vs práctica moderna, cross-links `[[concept_id|Título]]`, `claims_index`); 8) validación (17 chequeos deterministas + semánticos con severidad error/warn, gate "falla cerrado", score informativo); 9) orquestador + logging JSONL (`run_id`, reintentos por fase, circuit breaker, reporte final `FinalReport`); 10) CLI (`scan/inspect/run/run-batch/status/review/reset/report`, exit codes 0/1/2/130, `--dry-run/--force/--stop-after`); 11) piloto + calibración (concepto `frontend-01-internet-web`, dry-run primero, checklist manual, gate binario GO/NO-GO, escalamiento por fases A–E: frontend → backend → data → infra → lote de 255).
  - **Invariantes transversales:** nunca escribir fuera del bloque `ai:start/end`; validación determinista + semántica antes de escribir; idempotencia por hash/frescura; reanudación desde checkpoint; no invención (citas `[src-N]`, `[UNVERIFIED]` obligatorio para lo sin fuente); prompts y config versionados en git; calibración nunca aplicada automáticamente sin revisión humana.
  - **Mapeo de errores:** cada capa define sus excepciones y su traducción a `failed` (reintentable) o `blocked` (intervención humana), p. ej. `BackendAuthError → blocked`, `ValidationError` por errores → `failed`, por warnings → `blocked`.
  - **Relevancia:** la auditoría (`auditoria_spec_vs_impl.md`) usa este documento como referencia para determinar la deriva contractual; el plan de mejoras A–L rearma la implementación sobre estos contratos.

### explicacion del proyecto por capas v1 - pseudo codigo.md
- **Título:** Pseudo-código de alto nivel de las 11 capas
- **Propósito:** Documento hermano del diseño por capas: solo pseudo-código conceptual (qué, por qué, cómo, cuándo, dónde) estructurado por las mismas 11 capas, sin código real ni comandos. Versión condensada y navegable del diseño.
- **Puntos clave:**
  - **Orden y justificación:** cada capa se apoya en las anteriores (no se puede validar sin síntesis, ni sintetizar sin fuentes, ni buscar sin backend, ni persistir sin estados, ni definir estados sin modelo de datos), siguiendo el Apéndice A del diseño y la prioridad de decisiones de la spec.
  - **Reglas destacadas por capa:** ConceptMeta como único contrato con derivación por precedencia y 6 usos del content hash (integridad, concurrencia, edición manual, idempotencia, trazabilidad, verificación byte a byte); backend con interfaz async única y jerarquía de excepciones; validación con los 17 chequeos y gate "falla cerrado" (excepción interna = error fallido; score no entra al gate); runner con cola FIFO serial, reintentos por fase, limpieza best-effort de notebooks huérfanos y manejo de señales (Ctrl+C → reporte parcial, exit 130); CLI sin prompts interactivos con salida humana o `--json`.
  - **Piloto (capa 11):** concepto `frontend-01-internet-web` elegido por ser estable, con conexiones ricas y fuentes canónicas; siempre dry-run primero, `--strict`, revisión humana obligatoria, calibración por hallazgos (iterar máx. 3 veces), gate de escalamiento binario con criterios de integridad bloqueantes absolutos.
  - **Escalamiento:** plan de fases con mini-gates por área y cronograma de ~9 semanas (implementación → piloto → calibración → frontend → backend → data → infra → lote completo de 255 conceptos); hallazgos sistemáticos (mismo check fallando en muchos) indican problema de prompt/config, no de contenido.
  - **Diferencia con la implementación:** el pseudo-código numera 11 capas (modelo de datos y vault separados), mientras que `project_state.md` cuenta 10 implementadas (fusionadas en la Capa 1) — discrepancia ya documentada en el estado del proyecto y en la auditoría.

---


## 3. explicaciones (10 archivos)

Explicación didáctica del código del pipeline `it-concept-map`, capa por capa tal como quedó implementado (10 capas, tras fusionar las capas 1 y 2 del diseño).

### explicacion codigo - capa 1 registry y contratos.md
- **Título:** Capa 1: Registry y contratos de datos
- **Propósito:** Define la base del pipeline: el modelo de datos (`ConceptMeta`) y la lectura del vault de notas Obsidian. Fusiona las Capas 1 y 2 del diseño técnico porque el modelo y su materialización son inseparables.
- **Puntos clave:**
  - `models.py` (396 líneas) define los contratos de todo el pipeline: `SCHEMA_VERSION = "1.0.0"`, enums compartidos (`Volatility`, `ConceptStatus`, `Severity`, `PromptContext`), la dataclass central `ConceptMeta`, y los DTOs adelantados de las capas 3–8 (`Source`, `RawResearch`, `Synthesis`, `CheckResult`, `WriteResult`, `ConceptState`) más helpers de serialización y una jerarquía de excepciones.
  - `registry.py` (722 líneas) materializa conceptos: lee notas UTF-8 en bytes, detecta BOM/newlines, parsea frontmatter YAML, localiza el bloque `<!-- ai:start/end -->` (exactamente uno de cada, en orden), calcula hashes SHA-256 del interior y del "afuera", extrae key_ideas y connections (wikilinks con fallback), deriva título/área vía cadena de prioridad (override concepto > área > tags > default), y descubre el vault con `scan_vault()` (colisión de `concept_id` = error fatal).
  - Decisiones de diseño: el registry **solo lee** (mínimo privilegio, solo el writer escribe), hashes sobre bytes crudos sin normalizar, BOM preservado, fallbacks explícitos y nunca silenciosos, y `config.yaml` (122 líneas) que adelanta toda la configuración en un solo archivo.
  - El `concept_id` es el slug del path relativo al vault, estable mientras no se renombre. Python ≥3.11 con `pyyaml` como única dependencia.
  - Estado de avance al escribirse: capas 4–11 del diseño pendientes; la capa solo permite leer e inspeccionar el vault, pero fija todos los contratos futuros.

### explicacion codigo - capa 2 state y persistencia.md
- **Título:** Capa 2: State y persistencia (máquina de estados)
- **Propósito:** Implementa la máquina de estados y la persistencia del pipeline (corresponde a la Capa 3 del diseño, renumerada al fusionar 1+2). Permite saber en qué fase está cada concepto y reanudar si el proceso se corta.
- **Puntos clave:**
  - `state.py` (812 líneas) define `ConceptStatus` con 9 estados granulares (`pending`, `researched`, `synthesized`, `validated`, `written`, `completed`, `failed`, `needs_review`...): estados "terminado por fase" que permiten reanudar exactamente donde quedó. Difiere del pseudo-código (8 estados): `done → completed`, `blocked → needs_review`.
  - `VALID_TRANSITIONS` impone flujo lineal sin saltos de fase; `failed` puede volver a cualquier fase (reintento desde el punto de falla), conservando `last_good_state` y `checkpoint` en `ConceptState`. `TERMINAL_STATES` no se re-ejecutan salvo `--force`.
  - Persistencia dual: JSON por defecto (`workdir/concepts/<id>/estado.json` con escritura **atómica** tmp+`replace`) o SQLite opcional (upsert, migrable sin pérdida). Normalizadores de argumentos aceptan múltiples firmas para evitar bugs por orden de parámetros.
  - Primitivas de recuperación: `resume_from_checkpoint()` (idempotente), `reconcile_orphan_notebooks()` (registro `notebooks.json` para detectar notebooks sin dueño), y reintentos genéricos con backoff exponencial (`retry_with_backoff`, decorador `with_retry`).
  - Decisión clave: `state.py` no toca el vault ni la red, solo el workdir; no clasifica qué errores son reintentables (eso queda para el runner). Dos enums conviven (`models.py` contrato vs `state.py` operativo) con unificación pendiente al implementar el runner.

### explicacion codigo - capa 3 writer y escritura segura.md
- **Título:** Capa 3: Writer y escritura segura
- **Propósito:** Implementa la única pieza autorizada a modificar el vault (Capa 5 del diseño, adelantada). Protege las notas manuales (trabajo humano no reconstruible) con filosofía *fail-safe*: si no se puede probar que la escritura salió bien, se restaura el backup.
- **Puntos clave:**
  - `writer.py` (946 líneas) con `SafeWriter` como clase con estado (config resuelta una vez). Reemplazo quirúrgico vía `MarkerSpan` + `replace_inside()`: solo cambia el interior del bloque `ai:start/ai:end`. La "zona sagrada" (frontmatter, headings, wikilinks) ni siquiera entra por el camino de escritura.
  - Ciclo completo: hash del afuera antes → detección de edición concurrente (hash `at_read` primero, mtime con epsilon como fallback) → **pre-check en memoria** antes de tocar disco → dry-run con `DiffResult` → backup con `shutil.copy2` (preserva mtime) → escritura atómica (`os.replace`) → verificación **releyendo desde disco** → si falla, restore + `WriteFailedError`.
  - Defensa en profundidad: doble verificación hash + byte a byte del afuera, frontmatter byte a byte (con semántica YAML como red de seguridad), headings y wikilinks verificados con normalización de acentos (agregados sobre el pseudo-código).
  - Hallazgo central: **`read_text()` traduce CRLF→LF silenciosamente**, invalidando hashes en notas Windows/Obsidian → regla: "hashear lo que hay en disco, no lo que el runtime traduce". Todo el ciclo es en dominio de bytes (`read_bytes` → decode → manipular → encode → `write_bytes` → verificar).
  - 15 excepciones tipadas por modo de falla; integración con `state.py` (`writing_phase()` como API de alto nivel: idempotente, marca `validated→written→completed` o `failed`, persiste `write_result` con `WRITER_VERSION`).

### explicacion codigo - capa 4 backend.md
- **Título:** Capa 4: Backend (abstracción NotebookLM)
- **Propósito:** Interfaz de abstracción `ResearchBackend` que aísla al pipeline de la implementación concreta de NotebookLM. Ningún otro módulo habla directamente con la librería `notebooklm-py`.
- **Puntos clave:**
  - `backend.py` define la interfaz completa: `create_notebook`, `discover`, `import_discovered`, `add_urls`, `list_sources`, `wait_sources_ready`, `ask`, `delete_notebook`, `workspace_exists`, `cleanup`, `research`; más `ResearchResult`, `create_backend` (factory), `pipeline_dir` y `_map_library_error`.
  - **FakeBackend:** backend sin red, determinista e idempotente, con fixtures opcionales y latencia configurable. Permite correr todos los tests y calibrar sin gastar cuota ni tocar la cuenta real.
  - **NotebookLMBackend:** adaptador real contra `notebooklm-py` v0.8.4 (API async, `NotebookLMClient.from_storage`). Errores mapeados a excepciones tipadas (`BackendAuthError`, `BackendRateLimitError`, `BackendTimeout`, `BackendNotFoundError`, `BackendNetworkError`) para que el runner clasifique reintentos por tipo.
  - Integración: `state.py` guarda `notebook_id` al crear y verifica `workspace_exists` al reanudar; `writer.py` es ajeno al backend; el notebook se borra solo después de verificar la escritura.
  - Pendiente: smoke test con cuenta real (`scripts/smoke_notebooklm.py`), modo de respaldo sin NotebookLM, reconciliación de notebooks huérfanos, y calibración de timeouts/límites.

### explicacion codigo - capa 5 investigacion.md
- **Título:** Capa 5: Investigación (ResearchPhase)
- **Propósito:** Orquesta el backend para investigar un concepto de punta a punta: crea workspace, descubre/importa fuentes, consulta, persiste artefactos y transiciona el estado. Idempotente y recuperable.
- **Puntos clave:**
  - `ResearchPhase.run(concept, force)` ejecuta el flujo: genera 3 preguntas (a/b/c) a partir del concepto, transiciona a `RESEARCHING`, llama al backend y persiste `sources.json` y `raw_research.json` (concept_id, coverage, answers, source_ids, notebook_id, duration_ms, backend_provider) en `workdir/.pipeline/<id>/`, para luego terminar en `RESEARCHED`.
  - **Idempotencia:** si el estado está en `RESEARCHED` o posterior y existe `raw_research.json` sin `force`, retorna el resultado cacheado sin llamar al backend (no gastar cuota). Con `force=True` re-ejecuta y hace backup del artefacto anterior.
  - Manejo de errores granular: `BackendAuthError` → `failed_reason="auth"`, otros `BackendError` → `"error"`; siempre marca `FAILED` con `failed_phase="researching"` y persiste el estado antes de propagar.
  - Manejo de `InvalidTransitionError`: con `force` resetea a `PENDING` y reintenta; sin `force`, propaga.
  - Función de conveniencia `run_research()` crea el backend si no se pasa. Tests: `tests/test_research.py`, 12/12 OK sobre FakeBackend.

### explicacion codigo - capa 6 sintesis.md
- **Título:** Capa 6: Síntesis (SynthesisPhase)
- **Propósito:** Genera el study guide a partir de la investigación (`raw_research.json` + `sources.json`), construyendo el prompt según las reglas de evidencia de la spec, llamando al LLM y persistiendo el resultado. Idempotente y recuperable.
- **Puntos clave:**
  - `build_prompt(concept, raw, sources)` implementa las reglas de la spec: contexto antes que definición, principio 20/80, no inventar, trazabilidad por afirmación, separación entre fundamento estable y práctica moderna, y las secciones del contrato (`CONTRACT_SECTIONS`).
  - `SynthesisPhase.run()` transiciona a `SYNTHESIZED`, llama al LLM (acepta implementación sync o async), parsea las secciones `## Nombre` del markdown generado, y persiste `synthesis.json` con trazado completo (concept_id, title, markdown, sections, prompt, generated_at, duration_ms).
  - **Idempotencia** igual que la capa anterior: cache si ya está `SYNTHESIZED`/posterior; `force=True` re-ejecuta con backup del artefacto previo.
  - Manejo de errores: fallo del LLM → `FAILED` con `failed_phase="synthesizing"`, `last_error`/`error` guardados; no proveer LLM lanza `RuntimeError`.
  - Función de conveniencia `run_synthesis()`. Tests: `tests/test_synthesis.py`, 11/11 OK con mock de LLM.

### explicacion codigo - capa 7 validacion.md
- **Título:** Capa 7: Validación (ValidationPhase)
- **Propósito:** Valida la síntesis contra las reglas de la spec antes de permitir la escritura: produce un `ValidationReport` con pass/fail, issues, warnings y score. Es el filtro que decide si un `Synthesis` está apto para el writer. Idempotente y recuperable.
- **Puntos clave:**
  - Chequeos como métodos especializados: `_check_sections` (secciones requeridas presentes y con contenido suficiente), `_check_total_length` (longitud mínima y máxima), `_check_review_questions` (al menos 3 preguntas de repaso con "?"), `_check_structure` (encabezados `##` en orden), `_check_cross_links` (wikilinks contra connections del concepto), y heurísticas no bloqueantes: `_check_invented_urls` y `_check_copy_paste`.
  - `validate()` es una función pura que devuelve `(is_valid, issues, warnings)`; `ValidationPhase.run()` la envuelve, transiciona a `VALIDATED` o `FAILED` con `failed_reason="validation"`, y persiste `validation.json` (concept_id, is_valid, issues, warnings, score, checked_at) en `.pipeline/<id>/`.
  - Fallos de estructura: síntesis corrupta o secciones faltantes/cortas → issues bloqueantes → `is_valid=False` → estado `FAILED`. Transición inválida sin force → `InvalidTransitionError`.
  - **Idempotencia** estándar de la serie: cache en estados `VALIDATED`/posterior, `force=True` re-ejecuta y sobrescribe.
  - Función de conveniencia `run_validation()`. Tests: `tests/test_validation.py`, 12/12 OK.

### explicacion codigo - capa 8 orquestador.md
- **Título:** Capa 8: Orquestador (Runner)
- **Propósito:** Orquesta el pipeline completo por concepto y por lote: registry → research → synthesis → validation → writer, con logging, reanudación desde checkpoint, manejo de errores y pacing. Es la capa que unifica todas las anteriores.
- **Puntos clave:**
  - `Runner.run_concept(concept, force, dry_run)` aplica el flujo fase por fase, cada una condicionada al estado actual; si `completed` y no force/dry-run → salta (idempotente). Un lote que se corta a mitad se reanuda sin repetir trabajo.
  - `run_batch(concepts, force, dry_run)` procesa listas con **pacing** (`pause_between_concepts_s`) y no corta el lote ante un fallo: marca `failed`, persiste, y continúa con el siguiente concepto.
  - Logging estructurado en `events.jsonl` por concepto con eventos tipados: `run_start`, `phase_done`, `phase_failed`, `run_skip`, `run_end`. Reportes finales `RunReport` (status, phases_completed, error, duration_ms) y `BatchReport` (total, completed, failed, blocked, skipped, results, duration_ms).
  - Manejo de errores consistente: cada fase captura excepciones, marca el estado `failed` con `failed_phase`/`failed_reason`/`last_error`, persiste y devuelve reporte — el runner nunca deja estado sin persistir tras un error.
  - Funciones de conveniencia `run_concept()` y `run_batch()`. Tests: `tests/test_runner.py`, 11/11 OK.

### explicacion codigo - capa 9 cli.md
- **Título:** Capa 9: CLI (interfaz de comandos)
- **Propósito:** Interfaz de línea de comandos para humanos y agentes, expuesta como entry point `kpipe` en `pyproject.toml`. Conecta al runner y a las capas anteriores sin agregar lógica de negocio propia.
- **Puntos clave:**
  - Cinco comandos: `run [concepto] [--area] [--limit] [--force] [--dry-run]`, `status <concepto>`, `list [--status]`, `reset <concepto>` y `dry-run`.
  - Opciones globales para operar en distintos entornos: `--config`, `--workdir` y `--vault`.
  - Integración de solo-consumo: `runner.py` (ejecución), `state.py` (leer/escribir estado para `status`/`reset`), y `registry.load_concepts` para poblar `list` y filtros.
  - Cubre el caso de error básico: concepto no encontrado; `main` sin comando muestra ayuda.
  - Tests: `tests/test_cli.py`, 12/12 OK.

### explicacion codigo - capa 10 piloto.md
- **Título:** Capa 10: Piloto y calibración
- **Propósito:** Ejecuta el pipeline completo sobre un subconjunto de conceptos del vault para validar el sistema end-to-end, generando un reporte con métricas y parámetros de calibración sugeridos (timeouts, pacing).
- **Puntos clave:**
  - `PilotRunner.run_pilot(force, dry_run)` ejecuta el pipeline sobre cada concepto (vía `Runner` de la capa 8) y produce un `PilotReport`; `generate_summary(report)` genera un resumen en Markdown.
  - Dos niveles de datos: `PilotReport` con métricas agregadas (total, completed, failed, skipped, **success_rate**, avg/total duration_ms, errores, calibración) y `PilotMetrics` por concepto (status, duration_ms, phases_completed, error, `synthesis_chars`, `validation_score`, `source_count`).
  - **Calibración automática** a partir de los resultados: `suggested_pacing_s` (20 si success_rate < 0.8, si no 10) y `suggested_timeout_s` (900), persistidos en `pilot_report.json`.
  - Integra todos los módulos anteriores: es la validación real del pipeline completo.
  - Tests: `tests/test_pilot.py`, 9/9 OK. **Resumen final: TODAS LAS CAPAS 1–10 COMPLETADAS, ~82 tests en total, proyecto listo para piloto con cuenta real (`smoke_notebooklm.py` + `pilot.py`).**

---


## 4. it-concept-map (27 archivos)

Pipeline Python (capas 1–10) que enriquece conceptos IT de un vault Obsidian (`IT-Mind-Map`) investigando con NotebookLM (o un backend fake), sintetizando un study guide con un LLM, validándolo y escribiéndolo de forma segura dentro de un bloque `<!-- ai:start -->...<!-- ai:end -->` de cada nota. Estado persistido en `workdir/`; nunca escribe fuera del bloque en el vault.

### registry.py
- **Título:** Carga de conceptos desde el vault (Capa 2)
- **Propósito:** Descubre notas `.md` del vault y las convierte en `ConceptMeta`, la ficha única que consume todo el pipeline.
- **Puntos clave:**
  - `scan_vault()` / `read_concept()` / `load_concepts()`: glob con exclude_globs, parseo de frontmatter YAML, derivación de `title`/`area`/`tags`/`aliases` (frontmatter > H1 > nombre de archivo).
  - Extrae `key_ideas` (bullets de "Qué abarca" y alias configurables) y `connections` (wikilinks de "Relacionados"), filtrando índices y auto-referencias.
  - Calcula `slugify_path` (id estable), hashes SHA-256 del "afuera" y del "interior" del bloque AI, detección de BOM y newlines, `mtime_at_read` para detectar ediciones concurrentes.
  - Resolución de overrides (volatilidad, roles, dominios, seeds) con prioridad concepto > área > global, tolerante a config como dict u objeto.
  - Es de solo lectura: nunca escribe en el vault.

### models.py
- **Título:** Contratos de datos del pipeline (Capa 1)
- **Propósito:** Define los dataclasses compartidos por todas las capas, cada uno con `schema_version` para versionar los artefactos persistidos.
- **Puntos clave:**
  - Enums: `Volatility` (stable/semi_stable/dynamic), `ConceptStatus`, `Severity`, `PromptContext`.
  - Dataclasses principales: `ConceptMeta`, `Source`, `ResearchPlan`/`ResearchAnswer`/`Claim`, `RawResearch`, `Synthesis` (+ `CrossLink`, `ClaimRef`), `ValidationReport`/`CheckResult`, `WriteResult`, `ConceptState`.
  - Helpers: `to_dict()` serializa dataclasses convirtiendo `Path` y `Enum`; `now_iso()`, `sha256_text()`.
  - Jerarquía de excepciones de la capa: `ConceptModelError` con subtipos (`InvalidFrontmatterError`, `MissingRequiredFieldError`, etc.).
  - Aliases de compatibilidad con la spec (`Check = CheckResult`, `ValidationResult = ValidationReport`).

### state.py
- **Título:** Máquina de estados + persistencia (Capa 3)
- **Propósito:** Define el ciclo de vida de un concepto, valida transiciones y persiste el estado en JSON o SQLite.
- **Puntos clave:**
  - `ConceptStatus` con tabla `VALID_TRANSITIONS` explícita (pending → researching → researched → synthesized → validated → written → completed, más failed/needs_review reentrables); `TERMINAL_STATES`, `can_transition`, `validate_transition`.
  - `ConceptState` con `checkpoint`, `phase_data`, `last_good_state` y sincronización automática de timestamps en `__post_init__`.
  - `save_state`/`load_state`/`load_all_states`: JSON atómico por concepto (`workdir/concepts/<id>/estado.json`) o SQLite (`workdir/state.sqlite`); normalización flexible de args.
  - `resume_from_checkpoint()` y reconciliación de notebooks huérfanos vía `notebooks.json` (`reconcile_orphan_notebooks`, `register_notebook`).
  - Reintentos con backoff exponencial: `retry_with_backoff`, `execute_phase_with_retry` y decorador `@with_retry`.

### writer.py
- **Título:** Escritura segura del vault (Capa 5)
- **Propósito:** `SafeWriter` es la única pieza que modifica el vault, reemplazando solo el interior del bloque AI con verificaciones y rollback.
- **Puntos clave:**
  - Flujo de `write_concept()`: leer bytes → validar marcadores (errores tipados por duplicados/orden/ausencia) → hash del "afuera" antes → detectar edición concurrente (hash > mtime con epsilon) → pre-check en memoria → dry-run (diff) → backup (`copy2`) → escritura atómica (tmp + `os.replace`) → verificación releyendo de disco; si falla, restaura backup.
  - Verificaciones post-escritura: hash + byte a byte del afuera, marcadores 1/1, interior coincide con la síntesis, frontmatter intacto, y defensa en profundidad (headings "Qué abarca"/"Relacionados" y wikilinks preservados).
  - `replace_inside`/`render_inside`: normalización de newlines al estilo del archivo original; lectura fiel con `read_bytes` (evita la traducción universal de newlines).
  - Integra con state.py: `writing_phase()` hace `validated → written → completed` o `failed`, persistiendo `phase_data["write_result"]`.
  - ~15 excepciones tipadas (`OutsideIntegrityError`, `FrontmatterChangedError`, `ConcurrentEditError`, ...).

### backend.py
- **Título:** Backend de investigación (Capa 4)
- **Propósito:** Interfaz `ResearchBackend` + implementaciones Fake y NotebookLM real, con integración de estado y persistencia de artefactos.
- **Puntos clave:**
  - Contrato: Protocol `research()/cleanup()` con dataclasses `ResearchRequest`/`ResearchResult`; el pipeline nunca importa `notebooklm-py` directo.
  - `FakeBackend`: determinista, sin red, con fixtures opcionales `<concept_id>.json`, latencia simulada y registro de llamadas para tests.
  - `NotebookLMBackend`: cliente async via `from_storage()`, timeouts `asyncio.wait_for` por operación, retry con backoff solo para errores transitorios, circuit breaker (N fallos de red consecutivos), delete idempotente y limpieza best-effort de notebooks huérfanos. Claims mapeados a `source_id`; sin fuente ⇒ `unverified`.
  - Persistencia atómica con backup previo en `workdir/.pipeline/<id>/` (`sources.json`, `raw_research.json`), más funciones de cache (`load_cached_research`, `research_result_from_dict`).
  - `run_research_phase()`: carga estado, usa cache si ya researched (salvo `force`); error ⇒ `failed` con `failed_reason` tipado. `create_backend()`: factory con precedencia CLI > env `BACKEND_PROVIDER` > config.

### notebooklm_backend.py
- **Título:** Adaptador real de NotebookLM (re-export)
- **Propósito:** Módulo de 10 líneas que re-exporta `NotebookLMBackend` y helpers desde `backend.py`.
- **Puntos clave:**
  - Mantiene un único punto de verdad: la implementación vive en `backend.py`; este archivo existe para conservar la interfaz/nombre históricos.

### research.py
- **Título:** Fase de investigación (Capa 6)
- **Propósito:** `ResearchPhase` orquesta el backend por concepto: genera preguntas, ejecuta la investigación y persiste artefactos con transiciones de estado.
- **Puntos clave:**
  - `_questions()`: plan mínimo con 3 preguntas (a: fundamento estable, b: práctica moderna, c: relaciones), enriquecido con `key_ideas` del concepto.
  - Idempotencia: si el estado ya está researched+ y hay `raw_research.json`, reconstruye el resultado del cache sin re-ejecutar; `force=True` re-ejecuta con backup previo.
  - Persistencia de `sources.json` y `raw_research.json` y transiciones `→ RESEARCHING` / `→ RESEARCHED`, con manejo de errores (`failed_phase`="researching").
  - `run_research()` de conveniencia crea el backend via factory.

### synthesis.py
- **Título:** Fase de síntesis (Capa 7)
- **Propósito:** `SynthesisPhase` lee los artefactos de investigación, construye el prompt del study guide, llama al LLM y persiste `synthesis.json`.
- **Puntos clave:**
  - `build_prompt()`: prompt extenso en español con reglas innegociables (solo fuentes del notebook, no inventar URLs/versiones, 20/80, wikilinks solo a conceptos conectados, marcado "sin verificar"), encabezados `##` EXACTOS de las 10 secciones del contrato (`CONTRACT_SECTIONS`).
  - El LLM es un callable inyectado (sync o async, detectado con `iscoroutinefunction`); sin LLM lanza `RuntimeError`.
  - Parseo del markdown en diccionario de secciones por `## Nombre`.
  - Idempotencia (cache de synthesis.json salvo force + backup previo), transiciones de estado, persistencia del prompt en el artefacto.

### validation.py
- **Título:** Fase de validación (Capa 8)
- **Propósito:** `ValidationPhase` valida la síntesis contra reglas deterministas (estructura, longitud, preguntas) y persiste `validation.json`.
- **Puntos clave:**
  - Chequeos: secciones requeridas presentes y con mínimo de caracteres (20), longitud total (máx 14000, mín 100), ≥3 preguntas de repaso ("?"), estructura de encabezados `##`.
  - Chequeos declarados pero aún no bloqueantes: URLs inventadas, copy-paste de fuentes y cross-links fuera de `connections` (retornan solo warnings).
  - `validate()` devuelve `(is_valid, issues, warnings)`; score 0–1 = checks pasados / total.
  - `ValidationPhase.run()`: cache por idempotencia, si falla ⇒ estado `failed` con `failed_phase`="validating" y `failed_reason`="validation".
  - Nota de alineación: los nombres de `required_sections` de `config.yaml` difieren del contrato en español — algo a sincronizar (ver auditoría).

### runner.py
- **Título:** Orquestador del pipeline (Capa 9)
- **Propósito:** `Runner` ejecuta el pipeline completo por concepto con logging y reportes.
- **Puntos clave:**
  - `run_concept()`: skip si ya completed (salvo force/dry-run); por fase decide si ejecutar según el estado actual, tolerando reanudación desde researched/synthesized/validated.
  - Log de eventos en `concepts/<id>/events.jsonl` (run_start, phase_done, phase_failed, run_end).
  - En writing: re-resuelve el `note_path` contra `vault_path` si es relativo, reconstruye `Synthesis` desde synthesis.json y llama `writer.writing_phase()` con soporte dry-run.
  - Cada fase atrapa excepciones ⇒ estado `failed` + `failed_phase` + reporte `RunReport`.
  - `run_batch()`: itera conceptos con pacing configurable; produce `BatchReport` (completed/failed/blocked/skipped).

### cli.py
- **Título:** CLI `kpipe` (Capa 10)
- **Propósito:** Interfaz de línea de comandos para humanos y agentes: `run`, `status`, `list`, `reset`, `dry-run`.
- **Puntos clave:**
  - `--config/--workdir/--vault` globales con overrides sobre config.yaml; carga conceptos desde registry.
  - `run` filtra por concepto exacto/parcial, área o `--limit`; ejecuta corrida individual o batch (asyncio.run) e imprime resumen; exit-code según éxito.
  - `dry-run` es un wrapper de `run` con `dry_run=True` (no escribe).
  - `reset` borra directamente `workdir/concepts/<id>/estado.json`.

### pilot.py
- **Título:** Piloto + calibración
- **Propósito:** `PilotRunner` ejecuta el pipeline sobre un subconjunto de conceptos y produce métricas para validar end-to-end y calibrar parámetros.
- **Puntos clave:**
  - Métricas por concepto: duración, fases completadas, `synthesis_chars`, `validation_score`, `source_count` (leídos de los artefactos del workdir).
  - `PilotReport`: tasas de éxito, duración media/total, lista de errores; se persiste como `workdir/pilot_report.json`.
  - Calibración sugerida automática: pacing 20s si success rate < 0.8 (si no 10s) y timeout sugerido 900s.
  - `generate_summary()` renderiza un reporte Markdown legible; usa `Runner` internamente.

### config.yaml
- **Título:** Configuración base del pipeline
- **Propósito:** Parámetros operativos del proyecto: rutas, backend, pacing, estrategia de fuentes y reglas de validación.
- **Puntos clave:**
  - `vault_path` apunta a `IT-Mind-Map` y `workdir` a la carpeta del proyecto; glob `**/*.md` con excludes (`00 - *`, `_`, README).
  - Marcadores del bloque AI (`<!-- ai:start -->` / `<!-- ai:end -->`).
  - Backend: provider `fake` (fixtures + latency) o `notebooklm` (auth_file de cookies, timeouts por operación, max 2 notebooks concurrentes).
  - Pacing/backoff `[2,4,8]` max_retries 3; overrides de volatilidad por área, dominios y roles preferidos por área.
  - Estrategia de fuentes (seed_urls, dominios bloqueados, min/max fuentes, ventanas de frescura por volatilidad: stable 90d, semi 30d, dynamic 7d) y validación con secciones/min_words requeridos.

### README.md
- **Título:** Documentación del proyecto
- **Propósito:** Describe la estructura por capas y el estado de avance.
- **Puntos clave:**
  - Mapa archivo → capa (models, registry, state, writer, backend, research, synthesis, validation, runner, cli, pilot).
  - Declara TODAS LAS CAPAS COMPLETADAS (1–10) y listo para piloto con cuenta real.
  - Conteo de tests: 82 (15+12+11+12+11+12+9) — nota: los contadores del README no coinciden exactamente con los archivos actuales de tests.

### pyproject.toml
- **Título:** Metadatos y empaquetado
- **Propósito:** Define el proyecto como paquete Python y el script de entrada de la CLI.
- **Puntos clave:**
  - Nombre `it-concept-map` v0.2.0; requiere Python ≥3.11; dependencia base `pyyaml`.
  - Extras: `dev` (pytest) y `nlm` (`notebooklm-py>=0.8.4`).
  - Módulos planos (no package): los módulos raíz listados en `py-modules`.
  - Console script: `kpipe = cli:main`.

### scripts\smoke_notebooklm.py
- **Título:** Smoke test del backend real
- **Propósito:** Prueba cada operación del NotebookLMBackend contra una cuenta real midiendo tiempos y guarda un reporte JSON.
- **Puntos clave:**
  - Secuencia: create_notebook → add_urls (seed MDN) → discover → list_sources → wait_sources_ready → ask → delete_notebook, cada paso con `timed()` que imprime OK/FAIL + ms.
  - Escribe `workdir/smoke_report.json`.
  - OJO: usa una API del backend (`create_notebook`, `add_urls`, `discover`, `ask`, etc.) que NO coincide con la de `backend.py` actual y trata `NotebookLMBackend` como context manager con `async with` — parecería desactualizado respecto del código vivo.

### tests\config_cli.yaml
- **Título:** Config mínima para tests de CLI
- **Propósito:** Fixture YAML apuntando vault y workdir a carpetas temporales de tests con backend fake.
- **Puntos clave:**
  - 4 líneas; usado por `test_cli.py` para no tocar el config real del proyecto.

### tests\test_backend.py
- **Título:** Tests de Capa 4 (backend)
- **Propósito:** 15+ tests del FakeBackend, persistencia `.pipeline`, transiciones de estado y factory.
- **Puntos clave:**
  - Valida determinismo del fake, fixtures por concepto, claims `unverified` sin fuentes, cleanup idempotente.
  - `run_research_phase`: artefactos creados, cache de segunda corrida, force → backup, fallo auth ⇒ failed con reason, reintento desde failed ⇒ researched, transición inválida desde validated.
  - Factory: fake ok, proveedor desconocido ⇒ `BackendConfigError`; protocolo runtime_checkable cumplido.

### tests\test_research.py
- **Título:** Tests de Capa 5 (ResearchPhase)
- **Propósito:** 12 tests de la fase de investigación sobre FakeBackend, sin red.
- **Puntos clave:**
  - Persistencia de sources/raw, idempotencia (segunda corrida no llama `research`), force con backups.
  - Fallo auth ⇒ failed con razón, retry desde failed, transición inválida desde validated.
  - Cleanup idempotente, latencia simulada, factory y protocolo.

### tests\test_synthesis.py
- **Título:** Tests de Capa 6 (SynthesisPhase)
- **Propósito:** 11 tests con mock LLM (sync y async).
- **Puntos clave:**
  - `build_prompt` incluye concepto/área/ideas/reglas y secciones; `_seed_research()` arma los artefactos y estado researched.
  - Persistencia de synthesis.json, idempotencia con LLM contador (0 llamadas la 2ª vez), force + backup.
  - Fallo del LLM ⇒ failed; transición inválida desde pending; parseo correcto de secciones `##`.

### tests\test_validation.py
- **Título:** Tests de Capa 7 (ValidationPhase)
- **Propósito:** 12 tests de la validación determinista y su integración de estado.
- **Puntos clave:**
  - Casos de pass/fail: sección faltante, sección muy corta, contenido muy corto, pocas preguntas de repaso.
  - `ValidationPhase.run()`: persiste validation.json, idempotencia, force, fallo (síntesis corrupta) ⇒ estado failed.
  - Transición inválida desde pending; funciones de conveniencia y protocolo de fases.

### tests\test_runner.py
- **Título:** Tests de Capa 8 (Runner)
- **Propósito:** 11 tests end-to-end del orquestador con FakeBackend + mock LLM sobre un vault temporal.
- **Puntos clave:**
  - `_seed_vault()` crea la nota con frontmatter y bloque `ai:start/end`; helpers permiten iniciar en cualquier estado.
  - `run_concept` completo llega a "completed" con las 4 fases; corrida desde researched/synthesized/validated salta fases ya hechas.
  - Fallo en research (backend monkeypatcheado) ⇒ report failed; idempotencia (2ª corrida completed); `run_batch`; log events.jsonl.

### tests\test_cli.py
- **Título:** Tests de Capa 9 (CLI)
- **Propósito:** 12 tests de los comandos CLI usando config temporal y mocks (monkeypatch de Runner).
- **Puntos clave:**
  - `status`/`reset`/`list` sin estado o con estado; filtro por status; concepto inexistente ⇒ rc 1.
  - `cmd_run` con dry_run + LLM inyectado con monkeypatch.
  - `main` sin comando ⇒ rc != 0; `--help` ⇒ 0.

### tests\test_pilot.py
- **Título:** Tests de Capa 10 (PilotRunner)
- **Propósito:** 9 tests del piloto sobre un vault temporal con mock LLM y backend fake.
- **Puntos clave:**
  - Valida persistencia de `pilot_report.json`, success rate, métricas (synthesis_chars > 0), `generate_summary`, `to_dict`, calibración.
  - Caso de lista de conceptos vacía (total 0, success rate 0.0); función de conveniencia `run_pilot`.

### workdir\backups\capa4-otra-sesion\backend.discarded*.py (3 archivos)
- **Título:** Versiones descartadas del backend (Capa 4)
- **Propósito:** Histórico de trabajo de una sesión anterior en la capa backend (`backend.discarded.py` ~20 KB, `backend.discarded.v2.py` ~23 KB, `backend.discarded.v3.resumed.py` ~55 KB).
- **Puntos clave:**
  - Son iteraciones abandonadas/resumidas antes de consolidar el backend actual en `backend.py`; se conservan solo como respaldo (no participan del pipeline).
  - El archivo final `v3.resumed` coincide en tamaño con el `backend.py` vigente, lo que sugiere que la v3 es la base del código vivo.

---


## 5. IT-Mind-Map (266 archivos)

Vault de Obsidian generado por `generar_vault_it.py`: 255 conceptos de TI en 10 áreas + índice maestro. Estructura por nota: frontmatter (title, tags, área), sección "Qué abarca", sección "Mis notas" (marcada con `<!-- ai:start/end -->` para el pipeline), sección "Relacionados" (wikilinks) y navegación prev/next. Varios conceptos ya tienen guías de estudio extensas (generadas via NotebookLM/LLM); el resto son esqueletos pendientes de contenido.

### 00 · Archivo raíz del vault

#### 00 - Indice Maestro IT.md
- **Título:** Índice maestro del mind map de IT
- **Propósito:** Servir como hub raíz del vault: enlaza las 10 áreas temáticas (255 conceptos en total) y lista los conceptos hijos de cada área con enlaces wiki.
- **Puntos clave:**
  - Organiza 255 conceptos en 10 áreas: Software Engineering (30), Frontend (25), Backend (25), Database/Data Analytics (25), Networking/Internet (25), Operating Systems/Linux (25), AI Engineering (25), UX/UI (25), Product Management (25), Project Management (25).
  - Cada concepto aparece como lista plana de enlaces `[[ruta|alias]]`.
  - Recomendación de uso: abrir la Graph view para navegar el mapa completo; los índices de área (`00 - Índice X.md`) son la puerta de entrada.

### 01 · Software Engineering (31 archivos)

#### 00 - Índice Software Engineering.md
- **Título:** Índice del área Software Engineering
- **Propósito:** Listar los 30 conceptos del área con sus enlaces internos y las áreas conectadas del mind map.
- **Puntos clave:**
  - Estructura secuencial de conceptos: de fundamentos de programación hasta arquitectura, fiabilidad y liderazgo técnico.
  - Fuertes conexiones hacia Backend (16 enlaces), Project Management y AI Engineering.

#### 01 - Programming Fundamentals.md
- **Título:** Fundamentos de programación
- **Propósito:** Reunir los bloques básicos de todo código: variables, funciones y control de flujo.
- **Puntos clave:**
  - Cubre variables, funciones, tipos, control flow y abstracción.
  - Se enlaza con Lenguaje Backend y Runtime del área Backend.

#### 02 - Data Structures.md
- **Título:** Estructuras de datos
- **Propósito:** Catalogar las formas de organizar y almacenar datos en memoria.
- **Puntos clave:**
  - Cubre arrays, listas, árboles, hash tables y grafos.
  - Enlazado directamente con Algorithms y Complexity Analysis.

#### 03 - Algorithms.md
- **Título:** Algoritmos
- **Propósito:** Documentar los algoritmos fundamentales de procesamiento de datos.
- **Puntos clave:**
  - Cubre búsqueda, ordenamiento, recursión y complejidad.
  - Conceptuado como pareja inseparable de Data Structures.

#### 04 - Complexity Analysis.md
- **Título:** Análisis de complejidad
- **Propósito:** Marco para medir y comparar el costo de los algoritmos.
- **Puntos clave:**
  - Cubre Big O, complejidad temporal/espacial y trade-offs.
  - Complementa a Data Structures y Algorithms para elegir soluciones.

#### 05 - Object-Oriented Programming.md
- **Título:** Programación orientada a objetos
- **Propósito:** Agrupar el paradigma de objetos con sus cuatro pilares.
- **Puntos clave:**
  - Cubre encapsulación, herencia, polimorfismo y composición.
  - Se conecta con Functional Programming y Abstraction como paradigmas/prácticas alternativas.

#### 06 - Functional Programming.md
- **Título:** Programación funcional
- **Propósito:** Documentar el paradigma funcional y sus principios centrales.
- **Puntos clave:**
  - Cubre inmutabilidad, funciones puras y higher-order functions.
  - Se vincula con OOP y Abstraction para mezclar paradigmas.

#### 07 - Abstraction.md
- **Título:** Abstracción
- **Propósito:** Concepto transversal de ocultar detalles tras interfaces y contratos.
- **Puntos clave:**
  - Cubre interfaces, contratos y separation of concerns.
  - Conecta con Modularity, Architecture y Design Trade-offs: base de casi todo el diseño.

#### 08 - Modularity.md
- **Título:** Modularidad
- **Propósito:** Marco para dividir sistemas en piezas independientes con límites claros.
- **Puntos clave:**
  - Cubre módulos, dependencias y boundaries.
  - Puente directo hacia Architecture y Design Trade-offs.

#### 09 - API Design.md
- **Título:** Diseño de APIs
- **Propósito:** Reflejar el diseño de interfaces entre componentes y sistemas.
- **Puntos clave:**
  - Enfoque conceptual (a diferencia del área Backend, que es implementación).
  - Enlaza con Web APIs de Frontend, APIs de Backend y LLM APIs de AI Engineering.

#### 10 - Error Handling.md
- **Título:** Manejo de errores
- **Propósito:** Estrategias para tratar fallos y excepciones en el código.
- **Puntos clave:**
  - Cubre excepciones, tipos de error, recuperación y failure modes.
  - Se conecta con Middleware y Validación en Backend.

#### 11 - Concurrency.md
- **Título:** Concurrencia
- **Propósito:** Marco general para ejecución simultánea y sus riesgos.
- **Puntos clave:**
  - Cubre threads, async, locks y race conditions.
  - Conectado con asincronía de Frontend, Backend y procesos/threads del sistema operativo.

#### 12 - Git - Version Control.md
- **Título:** Git / control de versiones
- **Propósito:** Documentar el versionado de código y flujo de cambios.
- **Puntos clave:**
  - Cubre commits, branches, merge, rebase e historial.
  - Enlazado con CI/CD como parte del pipeline de entrega.

#### 13 - Code Quality.md
- **Título:** Calidad de código
- **Propósito:** Núcleo del grupo de prácticas para mantener código sano.
- **Puntos clave:**
  - Cubre legibilidad, mantenibilidad y consistencia.
  - Hub de Clean Code, Design Patterns, SOLID, Code Review y Refactoring.

#### 14 - Clean Code.md
- **Título:** Código limpio
- **Propósito:** Detallar cómo escribir código legible y coherente a nivel de línea y función.
- **Puntos clave:**
  - Cubre naming, funciones, cohesión y acoplamiento.
  - Complementario a Code Quality y a las prácticas de revisión/refactor.

#### 15 - Design Patterns.md
- **Título:** Patrones de diseño
- **Propósito:** Catalogar soluciones recurrentes a problemas de diseño comunes.
- **Puntos clave:**
  - Concepto amplio: patrones recurrentes de diseño.
  - Se apoya en Code Quality, Clean Code y SOLID.

#### 16 - SOLID & Design Principles.md
- **Título:** SOLID y principios de diseño
- **Propósito:** Agrupar los principios que guían la estructura y dependencias del código.
- **Puntos clave:**
  - Cubre principios de diseño y manejo de dependencias.
  - Pertenece al mismo "clúster" de calidad que Patterns, Clean Code y Refactoring.

#### 17 - Testing.md
- **Título:** Testing
- **Propósito:** Marco general de pruebas de software y su estrategia.
- **Puntos clave:**
  - Cubre unit, integration, E2E y test strategy.
  - Versión transversal; Frontend y Backend tienen sus notas específicas.

#### 18 - Debugging.md
- **Título:** Depuración
- **Propósito:** Proceso metódico para encontrar y corregir bugs.
- **Puntos clave:**
  - Cubre reproducción, diagnosis, profiling y root cause.
  - Único concepto de este rango sin "Relacionados" explícitos (aún sin enlaces).

#### 19 - Code Review.md
- **Título:** Code review
- **Propósito:** Práctica de validación del código entre pares antes de integrar.
- **Puntos clave:**
  - Cubre feedback, corrección y mantenibilidad.
  - Parte del clúster de calidad junto a Refactoring y Clean Code.

#### 20 - Refactoring.md
- **Título:** Refactorización
- **Propósito:** Definir el proceso de mejorar la estructura de código sin cambiar su comportamiento.
- **Puntos clave:**
  - Único apartado: mejorar estructura sin cambiar comportamiento.
  - Íntimamente ligado a Code Review y al clúster de calidad.

#### 21 - Documentation.md
- **Título:** Documentación
- **Propósito:** Reunir las formas de documentar código y decisiones.
- **Puntos clave:**
  - Cubre code docs, READMEs, ADRs (Architecture Decision Records) y docs técnicas.
  - Sin enlaces externos aún; se ubica entre Refactoring y Architecture.

#### 22 - Architecture.md
- **Título:** Arquitectura de software
- **Propósito:** Marco de alto nivel para organizar sistemas completos.
- **Puntos clave:**
  - Cubre capas, módulos, servicios y boundaries.
  - Se conecta con Arquitectura Frontend, arquitectura de aplicaciones Backend y AI System Architecture.

#### 23 - Design Trade-offs.md
- **Título:** Trade-offs de diseño
- **Propósito:** Recordar que toda decisión de diseño sacrifica algo.
- **Puntos clave:**
  - Cubre performance, simplicidad, costo y escalabilidad.
  - Dimensión "económica" que condiciona Abstraction, Modularity y Architecture.

#### 24 - Security Engineering.md
- **Título:** Ingeniería de seguridad
- **Propósito:** Marco transversal para desarrollar software de forma segura.
- **Puntos clave:**
  - Cubre amenazas, vulnerabilidades y desarrollo seguro.
  - Conectado con auth/seguridad de Backend, HTTPS/TLS y firewalls de Networking.

#### 25 - CI-CD.md
- **Título:** CI/CD
- **Propósito:** Documentar la automatización de build, test y deploy.
- **Puntos clave:**
  - Cubre build, test y deploy automation.
  - Se apoya en Git y conecta con contenedores/virtualización e infraestructura AI.

#### 26 - Observability.md
- **Título:** Observabilidad
- **Propósito:** Marco para conocer el estado interno de los sistemas en producción.
- **Puntos clave:**
  - Cubre logs, métricas, traces y monitoring.
  - Réplica transversal de las versiones Backend, OS y AI Engineering.

#### 27 - Reliability.md
- **Título:** Fiabilidad
- **Propósito:** Marco para que el sistema siga funcionando ante fallos.
- **Puntos clave:**
  - Cubre fault tolerance, availability y recovery.
  - Conecta con Distributed Systems y CDN/Load Balancing.

#### 28 - Distributed Systems.md
- **Título:** Sistemas distribuidos (SE)
- **Propósito:** Marco conceptual de sistemas compuestos por múltiples servicios.
- **Puntos clave:**
  - Cubre services, replication, consistency y messaging.
  - Núcleo común para Mensajería y Sistemas distribuidos de Backend y Advanced Data Architecture.

#### 29 - Technical Leadership.md
- **Título:** Liderazgo técnico
- **Propósito:** Definir responsabilidades de dirección técnica sin necesariamente gestionar personas.
- **Puntos clave:**
  - Cubre decisiones, standards y dirección técnica.
  - Enlaza con Stakeholder Management y Team Coordination de PM.

#### 30 - Engineering Processes.md
- **Título:** Procesos de ingeniería
- **Propósito:** Agrupar los procesos organizativos del trabajo de ingeniería.
- **Puntos clave:**
  - Cubre planning, estimación, delivery e incident management.
  - Puente fuerte hacia Project Management (Agile, Scrum, Kanban, retros).


### 02 · Frontend (26 archivos)

#### 00 - Índice Frontend.md
- **Título:** Índice del área Frontend
- **Propósito:** Listar los 25 conceptos del área Frontend y sus conexiones con otras áreas del vault.
- **Puntos clave:**
  - 25 conceptos ordenados de fundamentos (Internet & Web → DOM → JavaScript) hacia aplicación (Frameworks, Performance, Arquitectura).
  - Define con una frase la extensión de cada concepto (la columna "Qué abarca").
  - Áreas conectadas: Backend (12 enlaces), Networking/Internet (10), UX/UI (7), Software Engineering (5), OS/Linux y AI Engineering (1 cada una).
  - Estructura común de navegación: enlace `↑` hacia el índice maestro y pager `← · →` entre conceptos.

#### 01 - Internet & Web.md (guía extensa)
- **Título:** HTTP, HTTPS/TLS y URIs (arquitectura del web)
- **Propósito:** Guía técnica profunda sobre URIs, evolución de los protocolos HTTP y seguridad de transporte con TLS.
- **Puntos clave:**
  - **URIs (RFC 3986):** estructura `scheme://authority/path?query#fragment`; el fragmento nunca se transmite al servidor; percent-encoding para caracteres reservados; RFC 8820 reserva la gobernanza de paths al servidor de origen.
  - **STD 97 (2022):** separa la semántica HTTP (RFC 9110/9111: métodos, status codes, caching) de los formatos de transporte — HTTP/1.1 texto sobre TCP, HTTP/2 binario con multiplexación y HPACK, HTTP/3 binario sobre QUIC/UDP con QPACK (elimina head-of-line blocking de transporte).
  - **TLS 1.3 (RFC 8446) vs 1.2:** handshake 1-RTT (0-RTT en resumisión), solo intercambio efímero Diffie-Hellman (forward secrecy obligatoria), únicamente 5 cifras AEAD, transcript completo firmado (anti-downgrade); eliminó ataques como Bleichenbacher, POODLE, LogJam/FREAK. Riesgo del 0-RTT: replay attacks → solo métodos seguros (GET/HEAD).
  - **PKI:** cadena Root CA → Intermediate CA → certificado final; OCSP Stapling evita la latencia y la fuga de privacidad de consultas OCSP en tiempo real.
  - **GET con body:** RFC 9110 prohíbe que un payload cambie el significado del request; riesgos de cache poisoning, rechazo por proxies y request smuggling.
  - Incluye preguntas de práctica, prompts de ensayo y glosario (AEAD, ALPN, HPACK/QPACK, QUIC, SNI, etc.).

#### 02 - HTML.md (guía extensa)
- **Título:** Estructura del documento, carga de scripts y accesibilidad (A11Y)
- **Propósito:** Guía técnica sobre modos de renderizado, parsing y carga de scripts, HTML semántico y el pipeline de accesibilidad (ARIA + WCAG 2.2).
- **Puntos clave:**
  - **DOCTYPE y modos de renderizado:** `<!DOCTYPE html>` activa No-Quirks Mode (`compatMode: "CSS1Compat"`); sin doctype el browser entra en Quirks Mode. El `<head>` debe abrir con `meta charset` y viewport.
  - **Estrategias de carga de scripts:** síncrono (parser-blocking), `async` (orden no determinista), `defer` (orden de documento, antes de DOMContentLoaded), `type="module"` (defer por defecto, scope aislado, strict mode); `fetchpriority` ajusta la prioridad de red.
  - **Modelos de contenido:** elementos contenedor vs void elements (`img`, `input`, `br`...) sin cierre; landmarks semánticos (`header`→banner, `nav`, `main` única, `footer`→contentinfo, `aside`, `article`, `section` solo es landmark con nombre accesible).
  - **Accessibility Tree y ARIA:** cada nodo tiene Role/Name/State/Value; primera regla de ARIA (usar HTML nativo si existe); precedencia del nombre accesible: `aria-labelledby` > `aria-label` > contenido > `title`; live regions (`polite`/`assertive`).
  - **WCAG 2.2 (POUR, niveles A/AA/AAA):** contraste 4.5:1 texto normal, 3:1 texto grande y no-texto; zoom 200%, reflow a 320px; targets ≥24×24 px; teclado sin traps, tabindex prohibido positivo, skip links, focus trap en modales con `<dialog>`; placeholders NO son labels.
  - **Testing de accesibilidad:** automatizado (Lighthouse/axe) solo detecta 30–50% de los bugs; requiere inspección de la Accessibility Tree, testing de teclado manual y screen readers (NVDA/VoiceOver/Narrator).

#### 03 - CSS.md (guía extensa)
- **Título:** Cascade, especificidad, box model y pipeline de valores
- **Propósito:** Mecánica interna de cómo el motor CSS resuelve y materializa valores de estilo, desde la hoja de estilos hasta el píxel físico.
- **Puntos clave:**
  - **Pipeline de 6 etapas por propiedad:** Declared → Cascaded → Specified → Computed (unidades absolutas, pre-layout, es lo que heredan los hijos) → Used (dependiente de layout) → Actual (redondeo a hardware).
  - **Cascade (jerarquía de 8 niveles):** UA normal < User normal < Author normal < Keyframe animations < Author !important < User !important < UA !important < Transitions activas; `!important` invierte el orden de orígenes. `@layer`: reglas sin capa > capas (normal), pero capas > sin capa y capas anteriores ganan con `!important`.
  - **Especificidad como vector (a,b,c):** IDs, clases/atributos/pseudo-clases, tipos/pseudo-elementos; comparación lexicográfica. `:is()/:not()/:has()` heredan la especificidad máxima de sus argumentos, `:where()` fuerza (0,0,0).
  - **Inheritance:** propiedades heredadas (tipografía) vs no heredadas (layout/bordes) con fallback a `initial`; keywords universales `inherit`, `initial`, `unset`, `revert`, `revert-layer`.
  - **Box model:** `content-box` (width = contenido) vs `border-box` (width incluye padding+border); matemática del margin collapsing vertical y condiciones que lo suprimen (Flex, Grid, BFC vía `flow-root`/`overflow hidden`).

#### 04 - Layout.md (guía extensa)
- **Título:** Flexbox, Grid, posicionamiento y responsive por componente
- **Propósito:** Algoritmos de distribución de espacio en CSS moderno, stacking contexts y el paradigma de Container Queries.
- **Puntos clave:**
  - **Flexbox (1D):** ejes main/cross dependientes de `flex-direction` y writing mode; sizing por free space: `flex-grow` reparte espacio positivo proporcionalmente, `flex-shrink` pondera factor × base size en espacio negativo; trampa de `flex-basis: 0%` sin altura definida en columnas (cae a `content`); shorthands `initial/auto/none/<number>`.
  - **Grid (2D):** grid explícito vs implícito (`grid-auto-*`), `fr`, `minmax()`, `fit-content()`, y `auto-fill` (conserva tracks vacíos) vs `auto-fit` (los colapsa a 0px); algoritmo de auto-placement con `dense packing` que reordena visualmente (trade-off con teclado/AT); `subgrid` para alinear cards anidadas.
  - **Containing block y posicionamiento:** static/relative/sticky usan content box del ancestro; `absolute` usa padding box del ancestro posicionado; `fixed` usa viewport; `transform`/`filter`/`contain`/`container-type` en un ancestro lo convierten en containing block de hijos fixed/absolute.
  - **BFC y stacking contexts:** `display: flow-root` aísla floats y margin collapse; stacking contexts son atómicos — un `z-index: 9999` hijo no escapa del nivel de su padre; triggers: position+z-index, fixed/sticky, opacity<1, transform, filter, isolation, contain.
  - **Container Queries:** `container-type: inline-size` evita loops de layout infinitos; unidades `cqw/cqh/cqi/cqb/cqmin/cqmax` relativas al contenedor, no al viewport — base del responsive modular y design systems.

#### 05 - DOM.md (guía extensa)
- **Título:** Arquitectura del DOM, Observer APIs y mecánica de eventos
- **Propósito:** Guía técnica sobre la jerarquía de interfaces del DOM, manipulación eficiente, performance de rendering y observación asíncrona del navegador.
- **Puntos clave:**
  - **Jerarquía WHATWG:** `EventTarget` → `Node` → `Document`/`Element`/`CharacterData`/`DocumentFragment`; DOM4 deprecó tipos de nodos (ATTRIBUTE, ENTITY, NOTATION...) para reducir overhead; `isSameNode` = identidad por referencia, `isEqualNode` = igualdad estructural profunda.
  - **Manipulación:** live collections (`childNodes`, actualizan en tiempo real, cuidado con loops infinitos) vs static snapshots (`querySelectorAll`); métodos modernos (`append/prepend/before/after/replaceWith/remove`); `insertAdjacentHTML` evita el costo de re-parsear todo con `innerHTML`.
  - **Critical Rendering Path:** render tree (DOM+CSSOM, excluyendo `display:none`) → Layout/Reflow → Paint → Compositing GPU. Layout Thrashing: intercalar lecturas geométricas con escrituras al DOM fuerza synchronous layouts — mitigar batcheando lecturas y diferir escrituras con `requestAnimationFrame`.
  - **Observer APIs:** `MutationObserver` (cambios estructurales, microtask queue), `IntersectionObserver` (visibilidad/lazy loading, con `root`/`rootMargin`/`threshold`), `ResizeObserver` (geometría de box, con protección anti-loop); patrones con `takeRecords()` antes de `disconnect()`.
  - **Eventos y abort:** fases capturing → at_target → bubbling; `stopPropagation` vs `stopImmediatePropagation` vs `preventDefault`; opciones de listeners (`once`, `passive: true`, `signal` con AbortSignal); Shadow DOM retargeting y `composedPath()`; utilidades `AbortSignal.timeout()/any()/abort()`.

#### 06 - JavaScript.md (guía extensa)
- **Título:** Fundamentos del lenguaje: contextos, tipos y estructuras de datos
- **Propósito:** Síntesis de mecanismos core de JS según la especificación ECMAScript: alcance, closures, tipos primitivos, objetos y arrays/mutabilidad.
- **Puntos clave:**
  - **Contextos de ejecución y scopes:** Variable Environment + Lexical Environment + binding de `this`; scope chain por resolución lineal hacia arriba; closures retienen su entorno léxico (el GC no puede liberar variables externas mientras exista la referencia).
  - **Variables y globals:** `var` (function scope, hoisted a `undefined`) vs `let`/`const` (block scope, en TDZ → ReferenceError si se accede antes); `globalThis` unifica `window`/`self`/`global`.
  - **Tipos y precisión:** 7 primitivos vs reference types en heap; `Number` IEEE 754 con límite `(2^53−1)` en safe integers; `BigInt` sin mezcla implícita con Number, incompatible con `Math` y con `JSON.stringify`; igualdades: `==` (coerción) vs `===` vs `Object.is()` (distingue ±0 y NaN).
  - **Objetos:** delegación por prototype chain; campos privados `#` con encapsulación dura (invisibles a reflection e inmunes a freeze); `Object.groupBy` vs `Map.groupBy`; `structuredClone` para copias profundas (falla con funciones/DOM nodes).
  - **Arrays y Sets:** sparse arrays (métodos legacy saltan empty slots, modernos los tratan como `undefined`); métodos no destructivos ES2023 (`toSorted`, `toReversed`, `toSpliced`, `with`); operaciones de conjuntos nativas ES2024 (`intersection`, `union`, `difference`, `symmetricDifference`).

#### 07 - JavaScript avanzado.md
- **Título:** Scope, closures, prototypes, modules, this
- **Propósito:** Placeholder de nota para el nivel avanzado de JavaScript (aún sin contenido desarrollado).
- **Puntos clave:**
  - Define el alcance conceptual vía la sección "Qué abarca" y enlaces de navegación.
  - La sección "Mis notas" está vacía (pendiente de llenado).

#### 08 - Eventos.md
- **Título:** Event listeners, bubbling, capturing, delegation
- **Propósito:** Placeholder de nota sobre el sistema de eventos del navegador (sin contenido desarrollado).
- **Puntos clave:**
  - Define el alcance: listeners, burbujeo, captura y delegación.
  - Enlaza con 06 JavaScript, 07 JS avanzado y 09 Asincronía.

#### 09 - Asincronía.md
- **Título:** Callbacks, Promises, async/await, event loop
- **Propósito:** Placeholder de nota sobre asincronía en JavaScript (sin contenido desarrollado).
- **Puntos clave:**
  - Define el alcance: callbacks, Promises, async/await y event loop.
  - Enlaza cruzado con Concurrency (Software Engineering), Asincronía & Concurrencia (Backend) y Threads (OS) — concepto transversal.

#### 10 - Web APIs.md
- **Título:** APIs del navegador (Fetch, Storage, History, URL)
- **Propósito:** Placeholder de nota sobre las Web APIs del navegador (sin contenido desarrollado).
- **Puntos clave:**
  - Define el alcance: Fetch, Storage, History, URL y demás Web APIs.
  - Conecta con API Design (Software Engineering) y APIs (Backend).

#### 11 - JSON & APIs.md
- **Título:** Consumo y serialización de JSON, errores y contratos
- **Propósito:** Placeholder de nota sobre consumo de APIs y JSON desde el frontend.
- **Puntos clave:**
  - Define el alcance: consumo, serialización, manejo de errores y contratos de API.
  - Enlaza con Web APIs, Estado y Data fetching — núcleo del flujo de datos frontend.

#### 12 - TypeScript.md
- **Título:** Tipado, interfaces, generics, narrowing
- **Propósito:** Placeholder de nota sobre TypeScript.
- **Puntos clave:**
  - Define el alcance: tipado, interfaces, generics y narrowing.
  - Es el concepto más corto del área (sin sección de relacionados).

#### 13 - Componentización.md
- **Título:** Componentes, composición, reutilización
- **Propósito:** Placeholder de nota sobre la arquitectura por componentes.
- **Puntos clave:**
  - Define el alcance: componentes, composición y reutilización.
  - Enlaza con Design Systems y UI Components del área UX/UI.

#### 14 - Frameworks UI.md
- **Título:** React, Vue, Angular, Svelte y similares
- **Propósito:** Placeholder de nota sobre frameworks de interfaces.
- **Puntos clave:**
  - Define el alcance: React, Vue, Angular, Svelte, etc.
  - Se sitúa entre Componentización y Estado en el roadmap del área.

#### 15 - Estado.md
- **Título:** Gestión de estado (local, global, derivado, server)
- **Propósito:** Placeholder de nota sobre manejo de estado en frontend.
- **Puntos clave:**
  - Define el alcance: estado local, global, derivado y server state.
  - Enlaza directamente con Data fetching y con Frameworks UI.

#### 16 - Routing.md
- **Título:** Rutas en frontend (SPA, parámetros, guards)
- **Propósito:** Placeholder de nota sobre routing en SPAs.
- **Puntos clave:**
  - Define el alcance: SPA, rutas, parámetros, navegación y guards.
  - Diferencia el routing de frontend del Routing de Backend y de Networking (nombres homónimos, dominios distintos).

#### 17 - Formularios.md
- **Título:** Formularios en frontend (validación y errores)
- **Propósito:** Placeholder de nota sobre formularios.
- **Puntos clave:**
  - Define el alcance: validación, errores y controlled state.
  - Enlaza con Autenticación en Frontend y Accesibilidad (formularios como superficie crítica).

#### 18 - Data fetching.md
- **Título:** Captura de datos: cache, mutations, estados de carga
- **Propósito:**_placeholder de nota sobre data fetching client-side.
- **Puntos clave:**
  - Define el alcance: cache, mutations, loading/error states y sincronización.
  - Conecta con Estado, Performance, Caching (Backend) y CDN/Load Balancing (Networking).

#### 19 - Autenticación en Frontend.md
- **Título:** Sesiones, tokens, cookies, permisos
- **Propósito:** Placeholder de nota sobre autenticación vista desde el cliente.
- **Puntos clave:**
  - Define el alcance: sesiones, tokens, cookies y permisos.
  - Empareja con Autenticación y Autorización del Backend (concepto espejo).

#### 20 - Accesibilidad.md
- **Título:** Accesibilidad web: Semantic HTML, ARIA, teclado
- **Propósito:** Placeholder de nota sobre accesibilidad (el detalle técnico está en el archivo 02 - HTML).
- **Puntos clave:**
  - Define el alcance: Semantic HTML, ARIA y navegación por teclado.
  - Enlaza con Accessibility (UX/UI) y con Formularios.

#### 21 - Tooling.md
- **Título:** Node, gestores de paquetes, Vite, bundlers, ESLint
- **Propósito:** Placeholder de nota sobre el ecosistema de herramientas frontend.
- **Puntos clave:**
  - Define el alcance: Node, npm/pnpm, Vite, bundlers y ESLint.
  - Comparte con 12 y 16 el rasgo de carecer de sección de relacionados.

#### 22 - Testing.md
- **Título:** Testing en frontend (unit → E2E)
- **Propósito:** Placeholder de nota sobre la pirámide de testing frontend.
- **Puntos clave:**
  - Define el alcance: unit, integration, component y E2E.
  - Espejo conceptual de Testing (Software Engineering) y Testing Backend.

#### 23 - Performance.md
- **Título:** Performance web: rendering, bundles, Web Vitals
- **Propósito:** Placeholder de nota sobre optimización de performance frontend.
- **Puntos clave:**
  - Define el alcance: rendering, bundles, lazy loading, caching y Web Vitals.
  - Enlaza con Data fetching, Rendering moderno, Caching y CDN.

#### 24 - Rendering moderno.md
- **Título:** Estrategias de renderizado: CSR, SSR, SSG, hydration
- **Propósito:** Placeholder de nota sobre patrones modernos de rendering.
- **Puntos clave:**
  - Define el alcance: CSR, SSR, SSG, hydration y streaming.
  - Enlaza con Performance (el rendering es la mitad "servidor" de la ecuación).

#### 25 - Arquitectura Frontend.md
- **Título:** Arquitectura de aplicaciones frontend
- **Propósito:** Placeholder de nota sobre arquitectura a escala (design systems, módulos, patrones), cierre del área.
- **Puntos clave:**
  - Define el alcance: design systems, módulos, patrones y escalabilidad.
  - Es el concepto con más enlaces cruzados del área: Architecture (SE), Backend, Design Systems y UI Components (UX/UI), AI System Architecture.

### 03 · Backend (26 archivos)

#### 00 - Índice Backend.md
- **Título:** Índice del área Backend
- **Propósito:** Listar los 25 conceptos del área con su descripción y áreas conectadas.
- **Puntos clave:**
  - Contraste clave: el Backend se centra en datos, lógica, seguridad, concurrencia y sistemas distribuidos (vs. interfaz del Frontend).
  - Muy conectado con Software Engineering y Database (16 enlaces cada uno).

#### 01 - Cliente-Servidor.md
- **Título:** Modelo cliente-servidor
- **Propósito:** Fundamento de la arquitectura web: quién pide y quién responde.
- **Puntos clave:**
  - Cubre request/response, reparto de responsabilidades y comunicación.
  - Base conceptual compartida con Internet & Web (Frontend) e Internet (Networking).

#### 02 - HTTP.md
- **Título:** Protocolo HTTP
- **Propósito:** Detallar el protocolo que transporta toda la comunicación web.
- **Puntos clave:**
  - Cubre métodos, headers, status codes y cookies.
  - Se apoya en seis notas de Networking dedicadas a HTTP.

#### 03 - Servidor.md
- **Título:** Servidor
- **Propósito:** Describir el proceso que escucha y atiende peticiones.
- **Puntos clave:**
  - Cubre procesos, puertos, conexiones y lifecycle.
  - Conecta con processes y daemons/servicios del sistema operativo.

#### 04 - Lenguaje Backend.md
- **Título:** Lenguajes de backend
- **Propósito:** Paisaje de lenguajes típicos del lado servidor.
- **Puntos clave:**
  - Cubre Java, Go, Python, C# y JavaScript/TypeScript, entre otros.
  - Se vincula a Programming Fundamentals y al Runtime correspondiente.

#### 05 - Runtime.md
- **Título:** Runtimes
- **Propósito:** Entorno de ejecución que da vida a los lenguajes backend.
- **Puntos clave:**
  - Cubre JVM, Node.js, .NET y el runtime de Python, entre otros.
  - Pareja inseparable del concepto de Lenguaje Backend.

#### 06 - Routing.md
- **Título:** Routing (backend)
- **Propósito:** Mecanismo de dirigir peticiones al handler correcto.
- **Puntos clave:**
  - Cubre endpoints, parámetros y middleware.
  - Mismo concepto que el routing de Frontend y de red, pero aplicado al servidor.

#### 07 - APIs.md
- **Título:** APIs (backend)
- **Propósito:** Estilos de exposición de lógica y datos al exterior.
- **Puntos clave:**
  - Cubre REST, RPC, GraphQL y contratos.
  - Implementación práctica del API Design de Software Engineering.

#### 08 - Middleware.md
- **Título:** Middleware
- **Propósito:** Patrón de pipeline de procesamiento de peticiones.
- **Puntos clave:**
  - Cubre pipeline, logging, auth, validación y manejo de errores.
  - Conecta con Error Handling (SE) y Validación como siguiente eslabón.

#### 09 - Validación.md
- **Título:** Validación de entrada
- **Propósito:** Garantizar que los datos que entran al sistema son válidos y seguros.
- **Puntos clave:**
  - Cubre input validation, schemas y sanitización.
  - Línea de defensa temprana ligada a Error Handling y Middleware.

#### 10 - Arquitectura de aplicaciones.md
- **Título:** Arquitectura de aplicaciones
- **Propósito:** Organización interna de una aplicación backend en capas.
- **Puntos clave:**
  - Cubre capas, módulos, services y repositories.
  - Versión backend de la Architecture general y de la Arquitectura Frontend.

#### 11 - Bases de datos.md
- **Título:** Bases de datos (perspectiva backend)
- **Propósito:** Vista del desarrollador backend sobre la persistencia de datos.
- **Puntos clave:**
  - Cubre persistencia, tablas, documentos y relaciones.
  - Puente hacia el área Database: relaciones, índices, arquitectura y NoSQL.

#### 12 - SQL.md
- **Título:** SQL (uso backend)
- **Propósito:** Uso del lenguaje SQL desde la aplicación.
- **Puntos clave:**
  - Cubre SELECT, JOIN, índices y transacciones.
  - Espejo del concepto SQL del área Database (sabor más aplicado).

#### 13 - Modelado de datos.md
- **Título:** Modelado de datos (backend)
- **Propósito:** Diseñar la estructura de datos que usará la aplicación.
- **Puntos clave:**
  - Cubre relaciones, normalización y constraints.
  - Conecta con Data Modeling, Keys & Constraints y Normalization del área Database.

#### 14 - ORM - Data Access.md
- **Título:** ORM / capa de acceso a datos
- **Propósito:** Herramientas que traducen objetos del lenguaje a tablas de BD.
- **Puntos clave:**
  - Cubre Prisma, Hibernate, SQLAlchemy, Entity Framework, etc.
  - Capa intermedia entre Modelado de datos y la BD relacional.

#### 15 - Transacciones.md
- **Título:** Transacciones (backend)
- **Propósito:** Garantizar operaciones multi-paso consistentes en la BD.
- **Puntos clave:**
  - Cubre ACID, isolation, locks y consistency.
  - Enlaza con Transactions y ACID & Isolation del área Database.

#### 16 - Autenticación.md
- **Título:** Autenticación
- **Propósito:** Verificar la identidad de quien hace la petición.
- **Puntos clave:**
  - Cubre sessions, cookies, JWT y OAuth.
  - Primer eslabón del bloque de seguridad, antes de Autorización y Seguridad.

#### 17 - Autorización.md
- **Título:** Autorización
- **Propósito:** Controlar qué puede hacer cada identidad autenticada.
- **Puntos clave:**
  - Cubre roles, permissions, RBAC y ABAC.
  - Segundo nivel del bloque de seguridad, complementario a Autenticación.

#### 18 - Seguridad.md
- **Título:** Seguridad (backend)
- **Propósito:** Catálogo de amenazas web y defensas del backend.
- **Puntos clave:**
  - Cubre CORS, CSRF, XSS, injection y manejo de secrets.
  - Engloba auth/autorización y se apoya en HTTPS/TLS y firewalls.

#### 19 - Caching.md
- **Título:** Caching
- **Propósito:** Estrategias de caché para reducir carga y latencia.
- **Puntos clave:**
  - Cubre Redis, HTTP cache e invalidación.
  - Conecta con Data fetching y Performance de Frontend y CDN/Load Balancing.

#### 20 - Asincronía & Concurrencia.md
- **Título:** Asincronía y concurrencia (backend)
- **Propósito:** Manejo de muchas peticiones simultáneas en el servidor.
- **Puntos clave:**
  - Cubre threads, async, queues y workers.
  - Aplicación backend del concepto general de Concurrency (SE) y threads del OS.

#### 21 - Mensajería.md
- **Título:** Mensajería
- **Propósito:** Desacoplar componentes mediante comunicación indirecta.
- **Puntos clave:**
  - Cubre queues, events, brokers y pub/sub.
  - Pieza clave para Sistemas distribuidos y Advanced Data Architecture.

#### 22 - Observabilidad.md
- **Título:** Observabilidad (backend)
- **Propósito:** Instrumentar el backend para ver qué pasa en producción.
- **Puntos clave:**
  - Cubre logs, métricas, traces y monitoring.
  - Versión backend del concepto general de Observability.

#### 23 - Testing Backend.md
- **Título:** Testing en backend
- **Propósito:** Niveles de prueba específicos del lado servidor.
- **Puntos clave:**
  - Cubre unit, integration, API y E2E.
  - Especialización del Testing general de SE para servicios backend.

#### 24 - Deploy & Infraestructura.md
- **Título:** Despliegue e infraestructura
- **Propósito:** Poner el backend en producción y su plataforma.
- **Puntos clave:**
  - Cubre Linux, Docker, CI/CD y cloud.
  - Enlaza con contenedores y virtualización del OS e infraestructura de AI.

#### 25 - Sistemas distribuidos.md
- **Título:** Sistemas distribuidos (backend)
- **Propósito:** Escalar el backend a múltiples máquinas/instancias.
- **Puntos clave:**
  - Cubre load balancing, scaling, replication y consistency.
  - Corresponde a Reliability/Distributed Systems de SE más Mensajería local.

### 04 · Database & Data Analytics (26 archivos)

#### 00 - Índice Database - Data Analytics.md
- **Título:** Índice del área Database / Data Analytics
- **Propósito:** Listar los 25 conceptos del área desde fundamentos de datos hasta arquitectura avanzada.
- **Puntos clave:**
  - Arco completo: datos → SQL → motor de BD → almacenes analíticos → análisis/BI → lakehouse/streaming.
  - Su mayor conexión es con Backend (16 enlaces).

#### 01 - Data Fundamentals.md
- **Título:** Fundamentos de datos
- **Propósito:** Vocabulario y taxonomía básica de lo que es un dato.
- **Puntos clave:**
  - Cubre datos, registros, atributos, entidades y relaciones.
  - Sin enlaces "Relacionados" externos (grano último del área).

#### 02 - Data Modeling.md
- **Título:** Modelado de datos (BD)
- **Propósito:** Diseñar entidades y relaciones antes de crear la base de datos.
- **Puntos clave:**
  - Cubre modelado de entidades, relaciones y estructuras.
  - Enlaza con Modelado de datos de Backend y con Keys/Normalization propios.

#### 03 - Relational Databases.md
- **Título:** Bases de datos relacionales
- **Propósito:** Modelo dominante de BD basado en tablas y relaciones.
- **Puntos clave:**
  - Cubre tablas, filas, columnas y relaciones.
  - Hub del área: conecta con Backend (BD, modelado, ORM) y con Architecture/NoSQL propios.

#### 04 - SQL.md
- **Título:** SQL (BD)
- **Propósito:** Lenguaje estándar para consultar y modificar datos relacionales.
- **Puntos clave:**
  - Cubre SELECT, INSERT, UPDATE, DELETE y queries.
  - Se apoya en Filtering & Aggregation y JOINs como dos pilares de consulta.

#### 05 - Filtering & Aggregation.md
- **Título:** Filtrado y agregación
- **Propósito:** Técnicas SQL para resumir y seleccionar subconjuntos de datos.
- **Puntos clave:**
  - Cubre WHERE, GROUP BY, HAVING y funciones agregadas.
  - Continuación natural del SQL básico hacia análisis de datos.

#### 06 - JOINs.md
- **Título:** JOINs
- **Propósito:** Combinar datos de múltiples tablas relacionadas.
- **Puntos clave:**
  - Cubre INNER, LEFT, RIGHT y relaciones entre tablas.
  - Tercera pieza del trío SQL (con SELECT y agregación).

#### 07 - Keys & Constraints.md
- **Título:** Claves y restricciones
- **Propósito:** Mecanismos de integridad e identidad de los datos.
- **Puntos clave:**
  - Cubre primary keys, foreign keys, unique y constraints.
  - Base del Data Modeling y de la Normalización.

#### 08 - Normalization.md
- **Título:** Normalización
- **Propósito:** Diseñar esquemas que minimicen redundancia y anomalías.
- **Puntos clave:**
  - Cubre reducción de redundancia y anomalías (formas normales).
  - Íntimamente ligada a Data Modeling y Keys & Constraints.

#### 09 - Indexes.md
- **Título:** Índices
- **Propósito:** Estructuras internas para acelerar las búsquedas.
- **Puntos clave:**
  - Cubre búsqueda eficiente, B-trees e índices compuestos.
  - Conecta con la arquitectura interna de la BD (Database Architecture).

#### 10 - Transactions.md
- **Título:** Transacciones (BD)
- **Propósito:** Mecanismo para agrupar operaciones atómicas en la BD.
- **Puntos clave:**
  - Cubre commit, rollback y atomicidad.
  - Versión más profunda de las Transacciones desde el backend.

#### 11 - ACID & Isolation.md
- **Título:** ACID y niveles de aislamiento
- **Propósito:** Garantías formales de las transacciones concurrentes.
- **Puntos clave:**
  - Cubre consistencia, concurrencia y niveles de aislamiento.
  - Complemento teórico del concepto de Transactions.

#### 12 - Database Architecture.md
- **Título:** Arquitectura interna de BD
- **Propósito:** Cómo funciona una BD por dentro para ejecutar queries.
- **Puntos clave:**
  - Cubre storage engine, query engine y connections.
  - Integra NoSQL, indexes y BD relacionales como piezas del sistema.

#### 13 - NoSQL.md
- **Título:** NoSQL
- **Propósito:** Alternativas no relacionales al modelo de tablas.
- **Puntos clave:**
  - Cubre document, key-value, wide-column y graph databases.
  - Enlaza con Embeddings y Vector Databases de AI Engineering (datos no tradicionales).

#### 14 - Data Warehouses.md
- **Título:** Data warehouses
- **Propósito:** Sistemas de almacenamiento optimizados para análisis, no para transacciones.
- **Puntos clave:**
  - Cubre sistemas optimizados para análisis.
  - Se apoya en OLTP vs OLAP, ETL/ELT y Data Pipelines.

#### 15 - OLTP vs OLAP.md
- **Título:** OLTP vs OLAP
- **Propósito:** Distinguir cargas transaccionales (operación) de analíticas (análisis).
- **Puntos clave:**
  - Cubre operaciones transaccionales vs analíticas.
  - Justifica por qué existen los warehouses y los pipelines.

#### 16 - ETL - ELT.md
- **Título:** ETL / ELT
- **Propósito:** Patrones clásicos de mover y transformar datos hacia almacenes.
- **Puntos clave:**
  - Cubre Extract, Transform y Load.
  - Conecta con AI Workflows; la "T" en ELT se hace en el destino, no en tránsito.

#### 17 - Data Pipelines.md
- **Título:** Data pipelines
- **Propósito:** Generalización de ETL a flujos continuos de datos.
- **Puntos clave:**
  - Cubre ingesta, transformación y movimiento de datos.
  - Base para Data Quality y AI Workflows.

#### 18 - Data Quality.md
- **Título:** Calidad de datos
- **Propósito:** Detectar y medir los problemas de los datos.
- **Puntos clave:**
  - Cubre datos faltantes, duplicados, inconsistencias y validación.
  - Prerrequisito de un análisis fiable (Data Cleaning y Data Analysis).

#### 19 - Data Cleaning.md
- **Título:** Limpieza de datos
- **Propósito:** Proceso de corregir los problemas detectados de calidad.
- **Puntos clave:**
  - Cubre normalización, transformación y deduplicación.
  - La acción práctica sobre los problemas de Data Quality.

#### 20 - Data Analysis.md
- **Título:** Análisis de datos
- **Propósito:** Extraer significado accionable de los datos limpios.
- **Puntos clave:**
  - Cubre exploración, patrones, tendencias y correlaciones.
  - Núcleo del bloque analítico; se alimenta de Statistics y alimenta Visualización/BI.

#### 21 - Statistics.md
- **Título:** Estadística
- **Propósito:** Base matemática para el análisis y el ML.
- **Puntos clave:**
  - Cubre media, mediana, distribución, varianza y probabilidad.
  - Enlaza con AI/ML Fundamentals de AI Engineering (base de los modelos).

#### 22 - Analytics Metrics.md
- **Título:** Métricas analíticas
- **Propósito:** Definir y medir los números que importan al negocio.
- **Puntos clave:**
  - Cubre KPIs, métricas, dimensiones y ratios.
  - Conecta con métricas de UX, Producto y Project Management (medición transversal).

#### 23 - Data Visualization.md
- **Título:** Visualización de datos
- **Propósito:** Representar gráficamente los datos para comunicar hallazgos.
- **Puntos clave:**
  - Cubre charts, dashboards y visual encoding.
  - Aplica principios de jerarquía visual de UX/UI.

#### 24 - BI & Reporting.md
- **Título:** BI y reporting
- **Propósito:** Capacidades de reporting y autoservicio analítico de una organización.
- **Puntos clave:**
  - Cubre dashboards, reports y self-service analytics.
  - Capa de consumo situada sobre métricas y visualización.

#### 25 - Advanced Data Architecture.md
- **Título:** Arquitectura de datos avanzada
- **Propósito:** Arquitecturas modernas de datos a gran escala.
- **Puntos clave:**
  - Cubre lakehouse, streaming, distributed systems y governance.
  - Punto de fusión con Distributed Systems (SE), Mensajería y Sistemas distribuidos (Backend).


### 05 · Networking & Internet (26 archivos)

#### 00 - Índice Networking - Internet.md
- **Título:** Índice de Networking / Internet
- **Propósito:** Listar y enlazar los 25 conceptos del área con sus resúmenes en una línea.
- **Puntos clave:**
  - Va de fundamentos (Internet, IP, TCP/UDP) a capa web (HTTP, WebSockets) e infraestructura (CDN, Load Balancing).
  - Conecta con 5 áreas externas: Backend (11), Frontend (10), OS/Linux (5), Software Engineering (4), AI Engineering (2).

#### 01 - Internet.md
- **Título:** Internet
- **Propósito:** Definir Internet como red de redes bajo el modelo cliente-servidor.
- **Puntos clave:**
  - Es el concepto raíz del área; aún sin notas propias.
  - Se relaciona con Frontend (Internet & Web), Backend (Cliente-Servidor), IP y DNS.

#### 02 - IP.md
- **Título:** IP (Internet Protocol)
- **Propósito:** Explicar el direccionamiento de dispositivos en red.
- **Puntos clave:**
  - Concepto pivotal: se conecta con 9 temas (IPv4/IPv6, TCP, DNS, DHCP, ARP, Subnetting, OSI, HTTP).
  - Es la base de todo direccionamiento de paquetes en el área.

#### 03 - IPv4 - IPv6.md
- **Título:** IPv4 / IPv6
- **Propósito:** Cubrir las dos versiones del protocolo IP.
- **Puntos clave:**
  - Concepto enfocado: solo se enlaza con IP, DHCP, ARP y Subnetting.
  - Representa la evolución del esquema de direcciones.

#### 04 - TCP.md
- **Título:** TCP
- **Propósito:** Describir el protocolo de comunicación confiable orientado a conexión.
- **Puntos clave:**
  - Garantiza entrega, orden y control de flujo (contraste implícito con UDP).
  - Enlaza con OS/Linux vía Sockets y Networking en Linux.

#### 05 - UDP.md
- **Título:** UDP
- **Propósito:** Explicar la comunicación rápida sin conexión.
- **Puntos clave:**
  - Complemento ligero de TCP: sin handshake ni garantías.
  - Concepto con pocos enlaces: solo TCP y Puertos.

#### 06 - Puertos.md
- **Título:** Puertos
- **Propósito:** Explicar cómo los servicios reciben conexiones dentro de una máquina.
- **Puntos clave:**
  - Identifican la aplicación destino sobre TCP/UDP.
  - Conecta con Sockets y Networking en Linux en OS/Linux.

#### 07 - DNS.md
- **Título:** DNS
- **Propósito:** Explicar la traducción de nombres de dominio a direcciones IP.
- **Puntos clave:**
  - Concepto mínimo: solo se relaciona con Internet e IP.
  - Es el "phonebook" de Internet según la estructura de enlaces.

#### 08 - DHCP.md
- **Título:** DHCP
- **Propósito:** Explicar la asignación automática de configuración de red (IP, máscara, gateway, DNS).
- **Puntos clave:**
  - Elimina el setup manual de red en clientes.
  - Se relaciona con IP, IPv4/IPv6, ARP y Subnetting/CIDR.

#### 09 - MAC - Ethernet.md
- **Título:** MAC / Ethernet
- **Propósito:** Explicar la comunicación física dentro de una red local.
- **Puntos clave:**
  - Dirección MAC identifica la tarjeta de red (capa 2).
  - Único concepto del bloque sin sección "Relacionados" explícita.

#### 10 - ARP.md
- **Título:** ARP
- **Propósito:** Explicar la resolución de direcciones IP a direcciones MAC en IPv4.
- **Puntos clave:**
  - Puente entre el mundo IP (capa 3) y el mundo Ethernet (capa 2).
  - Se enlaza con IP, IPv4/IPv6, DHCP y Subnetting.

#### 11 - Routing.md
- **Título:** Routing
- **Propósito:** Explicar cómo los paquetes encuentran su destino a través de redes.
- **Puntos clave:**
  - Distingue rutas en red física vs. routing en apps (Frontend/Backend tienen su propio "Routing").
  - Conecta con Routers, NAT y Subnetting.

#### 12 - Routers.md
- **Título:** Routers
- **Propósito:** Describir los dispositivos que interconectan redes distintas.
- **Puntos clave:**
  - Implementación física/hardware del concepto Routing.
  - Enlaza con Routing, NAT y Subnetting/CIDR.

#### 13 - NAT.md
- **Título:** NAT
- **Propósito:** Explicar la traducción entre direcciones privadas y públicas.
- **Puntos clave:**
  - Permite que múltiples dispositivos internos compartan una IP pública.
  - Concepto compacto: solo se enlaza con Routing, Routers y Subnetting.

#### 14 - Subnetting - CIDR.md
- **Título:** Subnetting / CIDR
- **Propósito:** Explicar la división de redes y la notación de prefijos CIDR.
- **Puntos clave:**
  - Relacionado con 7 conceptos: IP, IPv4/IPv6, DHCP, ARP, Routing, Routers y NAT.
  - Es la estructura matemática/lógica del direccionamiento IP en el área.

#### 15 - OSI - TCP-IP Model.md
- **Título:** OSI / TCP-IP Model
- **Propósito:** Explicar las capas y responsabilidades del modelo de networking.
- **Puntos clave:**
  - Marco conceptual que ordena todos los otros conceptos del área.
  - Enlaza específicamente con IP, TCP y HTTP.

#### 16 - HTTP.md
- **Título:** HTTP
- **Propósito:** Explicar el protocolo fundamental de la Web.
- **Puntos clave:**
  - Concepto hub: se conecta con 11 temas, más que ningún otro del área.
  - Enlaza Frontend (Internet & Web) y Backend (HTTP), y sirve de base para HTTPS, Request/Response, Methods, Status Codes, Headers, WebSockets.

#### 17 - HTTPS - TLS.md
- **Título:** HTTPS / TLS
- **Propósito:** Explicar la comunicación HTTP cifrada con TLS.
- **Puntos clave:**
  - Bloque de seguridad dentro de Networking: enlaza con Security Engineering, Backend (Seguridad) y AI (AI Safety).
  - Añade criptografía/certificados sobre HTTP plano.

#### 18 - Request - Response.md
- **Título:** Request / Response
- **Propósito:** Explicar el modelo de comunicación web entre cliente y servidor.
- **Puntos clave:**
  - Patrón estructural de toda interacción HTTP.
  - Enlaza con HTTP, Methods, Status Codes y Headers/Cookies.

#### 19 - HTTP Methods.md
- **Título:** HTTP Methods
- **Propósito:** Enumerar los verbos HTTP: GET, POST, PUT, PATCH, DELETE.
- **Puntos clave:**
  - Define la semántica de las operaciones sobre recursos.
  - Enlaza con el bloque HTTP (HTTP, Request/Response, Status Codes, Headers).

#### 20 - HTTP Status Codes.md
- **Título:** HTTP Status Codes
- **Propósito:** Explicar los códigos de respuesta HTTP: 2xx, 3xx, 4xx, 5xx.
- **Puntos clave:**
  - Comunican el resultado de cada request: éxito, redirección, error del cliente, error del servidor.
  - Enlaza al mismo bloque HTTP central que los demás conceptos web.

#### 21 - Headers - Cookies.md
- **Título:** Headers / Cookies
- **Propósito:** Explicar la metadata y el manejo de estado en la comunicación HTTP.
- **Puntos clave:**
  - Headers transportan info contextual; cookies persisten estado en el cliente.
  - Enlaza con el bloque HTTP + HTTPS y WebSockets.

#### 22 - WebSockets.md
- **Título:** WebSockets
- **Propósito:** Explicar la comunicación bidireccional persistente entre cliente y servidor.
- **Puntos clave:**
  - Escapa del modelo Request/Response para tiempo real.
  - Enlaza con Sockets en OS/Linux y con HTTP/HTTPS.

#### 23 - Proxies - Reverse Proxies.md
- **Título:** Proxies / Reverse Proxies
- **Propósito:** Explicar los intermediarios entre clientes y servidores.
- **Puntos clave:**
  - Proxy actúa del lado del cliente; reverse proxy del lado del servidor.
  - Enlaza con Firewalls y CDN/Load Balancing.

#### 24 - Firewalls.md
- **Título:** Firewalls
- **Propósito:** Explicar el control del tráfico de red según reglas.
- **Puntos clave:**
  - Filtra qué conexiones se permiten, bloquean o inspeccionan.
  - Bloque de seguridad junto a HTTPS/TLS y Proxies, con enlaces a Software Engineering y AI Engineering.

#### 25 - CDN - Load Balancing.md
- **Título:** CDN / Load Balancing
- **Propósito:** Explicar la distribución y escalamiento del tráfico.
- **Puntos clave:**
  - CDN aproxima contenido al usuario; Load Balancing reparte carga entre servidores.
  - Concepto más conectado a "áreas externas": enlaza con 8 temas fuera del área (Reliability, Distributed Systems, Caching, Performance, etc.).

### 06 · Operating Systems & Linux (26 archivos)

#### 00 - Índice Operating Systems - Linux.md
- **Título:** Índice de Operating Systems / Linux
- **Propósito:** Listar y enlazar los 25 conceptos del área con sus resúmenes en una línea.
- **Puntos clave:**
  - Se organiza en un arco lógico: SO → kernel → procesos/threads → memoria → archivos/permisos → I/O, IPC, sockets → shell/CLI → servicios, redes, contenedores.
  - Conecta con 5 áreas externas: Backend (6), Software Engineering (6), Networking (5), AI Engineering (3), Frontend (1).

#### 01 - Operating System.md
- **Título:** Operating System
- **Propósito:** Definir qué hace un SO y cómo administra el hardware.
- **Puntos clave:**
  - Es el concepto raíz del área; aún sin notas propias.
  - Se relaciona únicamente con Kernel y System Calls.

#### 02 - Kernel.md
- **Título:** Kernel
- **Propósito:** Explicar el núcleo que conecta software y hardware.
- **Puntos clave:**
  - Es el componente central que gestiona recursos en nombre del SO.
  - Enlaza con Operating System, System Calls y Processes.

#### 03 - Processes.md
- **Título:** Processes
- **Propósito:** Explicar los programas en ejecución y su ciclo de vida.
- **Puntos clave:**
  - Concepto pivote: enlaza con 7 temas (Threads, CPU, Memoria, Stack/Heap, Daemons) más Concurrency y Servidor.
  - Es la unidad básica de ejecución que el sistema gestiona.

#### 04 - Threads.md
- **Título:** Threads
- **Propósito:** Explicar la ejecución concurrente dentro de un proceso.
- **Puntos clave:**
  - Comparten memoria del proceso que los contiene.
  - Enlaza externamente con Concurrency (Software Engineering), Asincronía (Frontend) y Asincronía & Concurrencia (Backend).

#### 05 - CPU & Scheduling.md
- **Título:** CPU & Scheduling
- **Propósito:** Explicar cómo el SO distribuye el tiempo de CPU entre procesos/threads.
- **Puntos clave:**
  - Introduce el concepto de time-sharing / schedulers.
  - Enlaza con Processes y Threads, más Concurrency externo.

#### 06 - Memory Management.md
- **Título:** Memory Management
- **Propósito:** Explicar la RAM, la memoria virtual y las páginas.
- **Puntos clave:**
  - Gestiona asignación y traducción de memoria (virtual → física).
  - Enlaza con Processes y Stack & Heap.

#### 07 - Stack & Heap.md
- **Título:** Stack & Heap
- **Propósito:** Explicar la organización de memoria dentro de los procesos.
- **Puntos clave:**
  - Distingue memoria automática (pila) vs. memoria dinámica (heap).
  - Enlaza con Processes y Memory Management.

#### 08 - File Systems.md
- **Título:** File Systems
- **Propósito:** Explicar archivos, directorios, bloques y metadata del almacenamiento.
- **Puntos clave:**
  - Organiza la persistencia en disco.
  - Enlaza con File Permissions y Users & Groups.

#### 09 - File Permissions.md
- **Título:** File Permissions
- **Propósito:** Explicar los permisos de lectura/escritura/ejecución por usuario y grupo.
- **Puntos clave:**
  - Modelo de permisos octal + usuarios/grupos (rwx).
  - Enlaza con File Systems y Users & Groups.

#### 10 - Users & Groups.md
- **Título:** Users & Groups
- **Propósito:** Explicar la identidad y separación de privilegios de usuarios.
- **Puntos clave:**
  - Define quién puede hacer qué en el sistema.
  - Enlaza con File Systems, File Permissions y System Calls.

#### 11 - System Calls.md
- **Título:** System Calls
- **Propósito:** Explicar la interfaz entre programas de usuario y el kernel.
- **Puntos clave:**
  - Es el único punto de entrada oficial al kernel.
  - Enlaza con Operating System y Kernel.

#### 12 - I-O.md
- **Título:** I/O
- **Propósito:** Explicar las operaciones de input/output, dispositivos y streams.
- **Puntos clave:**
  - La comunicación con dispositivos de hardware paso a paso.
  - Concepto sin "Relacionados" explícitos (solo enlaces de navegación prev/next).

#### 13 - Processes IPC.md
- **Título:** Processes IPC
- **Propósito:** Explicar la comunicación entre procesos (pipes, shm, mensajes).
- **Puntos clave:**
  - Mecanismos para que procesos independientes se comuniquen.
  - Enlaza con Sockets y Signals.

#### 14 - Sockets.md
- **Título:** Sockets
- **Propósito:** Explicar la comunicación entre procesos y/o por red.
- **Puntos clave:**
  - Puente entre el mundo local (IPC) y el mundo de red.
  - Conecta externamente con TCP, Puertos y WebSockets del área Networking.

#### 15 - Environment Variables.md
- **Título:** Environment Variables
- **Propósito:** Explicar cómo se configura el entorno de ejecución de los procesos.
- **Puntos clave:**
  - Variables que definen comportamiento y configuración sin hardcode.
  - Enlaza con Shell y Package Management.

#### 16 - Shell.md
- **Título:** Shell
- **Propósito:** Explicar la interfaz para interactuar con el sistema operativo.
- **Puntos clave:**
  - Traduce comandos del usuario al sistema.
  - Enlaza con Environment Variables, CLI, Bash Scripting, Signals y Package Management.

#### 17 - Linux CLI.md
- **Título:** Linux CLI
- **Propósito:** Explicar comandos, pipes y redirecciones en la línea de comandos de Linux.
- **Puntos clave:**
  - Herramienta compuesta por comandos combinables (unix pipelines).
  - Enlaza con Shell, Bash Scripting y Signals.

#### 18 - Bash - Shell Scripting.md
- **Título:** Bash / Shell Scripting
- **Propósito:** Explicar la automatización mediante scripts de shell.
- **Puntos clave:**
  - Lleva los comandos sueltos del CLI a lógica programática (condiciones, loops).
  - Enlaza con Shell, CLI y Signals.

#### 19 - Signals.md
- **Título:** Signals
- **Propósito:** Explicar la comunicación y control de procesos vía señales del SO.
- **Puntos clave:**
  - Notificaciones asíncronas que interrumpen procesos (SIGKILL, SIGTERM...).
  - Enlaza con IPC, Sockets, Shell, CLI y Bash.

#### 20 - Daemons - Services.md
- **Título:** Daemons / Services
- **Propósito:** Explicar los procesos que funcionan como servicios de fondo.
- **Puntos clave:**
  - Corren sin interacción directa del usuario (servidores, schedulers).
  - Enlaza con Servidor (Backend) y Processes.

#### 21 - Package Management.md
- **Título:** Package Management
- **Propósito:** Explicar la instalación y gestión de software en Linux.
- **Puntos clave:**
  - Herramientas tipo apt/yum que administran dependencias del sistema.
  - Enlaza con Environment Variables y Shell.

#### 22 - Networking en Linux.md
- **Título:** Networking en Linux
- **Propósito:** Explicar interfaces, puertos, rutas y sockets a nivel de sistema Linux.
- **Puntos clave:**
  - Dimensiona cómo Linux implementa internamente lo teorizado en Networking.
  - Enlaza externamente con TCP y Puertos, más Sockets local.

#### 23 - Logs & System Monitoring.md
- **Título:** Logs & System Monitoring
- **Propósito:** Explicar el monitoreo de procesos, CPU, RAM, disco y logs del sistema.
- **Puntos clave:**
  - Herramientas como top/htop, journalctl para diagnóstico.
  - Conecta externamente con Observability en Software Engineering, Backend y AI Engineering.

#### 24 - Containers.md
- **Título:** Containers
- **Propósito:** Explicar namespaces, isolation y Docker.
- **Puntos clave:**
  - Virtualización ligera a nivel de kernel del sistema host.
  - Enlaza con CI/CD, Deploy & Infraestructura, Virtualization y AI Infrastructure.

#### 25 - Virtualization & Infrastructure.md
- **Título:** Virtualization & Infrastructure
- **Propósito:** Explicar VMs, hypervisors y cloud infrastructure.
- **Puntos clave:**
  - Cierre del área: conecta lo local con lo cloud/distribuido.
  - Enlaza con Containers, CI/CD, Deploy & Infraestructura y AI Infrastructure.

### 07 · AI Engineering (26 archivos)

#### 00 - Índice AI Engineering.md
- **Título:** Índice de AI Engineering
- **Propósito:** Listar y enlazar los 25 conceptos del área con sus resúmenes en una línea.
- **Puntos clave:**
  - Incluye una nota del autor distinguiendo AI Engineering (construir productos alrededor de modelos existentes, sobre todo LLMs) de ML Engineering.
  - Se conecta con 6 áreas externas: Backend (7), Database/Data Analytics (6), Software Engineering (6), OS/Linux (3), Networking (2), Frontend (1).

#### 01 - AI - ML Fundamentals.md
- **Título:** AI / ML Fundamentals
- **Propósito:** Introducir los conceptos base: modelos, entrenamiento, inferencia y datos.
- **Puntos clave:**
  - Concepto raíz del área; aún sin notas propias.
  - Enlaza con Statistics (Database) y los siguientes bloques de la lista (Linear Algebra, ML Fundamentals, Neural Networks).

#### 02 - Python & Programming.md
- **Título:** Python & Programming
- **Propósito:** Cubrir el tooling de programación para AI: Python, estructuras, APIs, async.
- **Puntos clave:**
  - Concepto de habilidades transversales, no de conocimiento teórico de AI.
  - Enlaza con Programming Fundamentals, Lenguaje Backend y Runtime.

#### 03 - Linear Algebra & Probability.md
- **Título:** Linear Algebra & Probability
- **Propósito:** Cubrir vectores, matrices, distribuciones y probabilidad como base matemática.
- **Puntos clave:**
  - Sostiene los conceptos cuantitativos del área (embeddings, attention, distributions).
  - Enlaza con AI/ML Fundamentals, ML Fundamentals y Neural Networks.

#### 04 - Machine Learning Fundamentals.md
- **Título:** Machine Learning Fundamentals
- **Propósito:** Explicar features, labels, training, validation y generalization.
- **Puntos clave:**
  - Formaliza el ciclo de vida de un modelo clásico de ML.
  - Enlaza con Statistics (Database) y los conceptos previos (AI/ML Fundamentals, Linear Algebra).

#### 05 - Neural Networks.md
- **Título:** Neural Networks
- **Propósito:** Explicar layers, activations, backpropagation y optimization.
- **Puntos clave:**
  - Es el concepto más conectado de los fundamentos "hard": 7 enlaces.
  - Puente entre el ML clásico y las arquitecturas modernas (Transformers, LLMs).

#### 06 - Transformers.md
- **Título:** Transformers
- **Propósito:** Explicar attention, tokens, embeddings y la arquitectura transformer.
- **Puntos clave:**
  - Arquitectura base de los LLMs modernos.
  - Enlaza con Neural Networks, LLMs, Tokenization y Embeddings.

#### 07 - LLMs.md
- **Título:** LLMs
- **Propósito:** Explicar pretraining, inference, context windows y capabilities de los modelos de lenguaje.
- **Puntos clave:**
  - Concepto central de la AI Engineering "moderna" (según la nota del índice).
  - Enlaza con Transformers, Tokenization, Embeddings, AI Infrastructure y Fine-tuning.

#### 08 - Tokenization.md
- **Título:** Tokenization
- **Propósito:** Explicar tokens, token budgets y su relación con el contexto.
- **Puntos clave:**
  - Determina cuánto texto cabe en la ventana de contexto (y el costo).
  - Enlaza con Neural Networks, Transformers, LLMs y Embeddings.

#### 09 - Embeddings.md
- **Título:** Embeddings
- **Propósito:** Explicar representaciones vectoriales y semantic similarity.
- **Puntos clave:**
  - Base conceptual para búsqueda semántica y retrieval (RAG, vector DBs).
  - Enlaza con Neural Networks, Transformers, LLMs, Tokenization, RAG, Vector Databases y Context Engineering.

#### 10 - Prompt Engineering.md
- **Título:** Prompt Engineering
- **Propósito:** Explicar instructions, context, few-shot y structured prompts.
- **Puntos clave:**
  - Habilidad práctica para guiar el comportamiento de un LLM.
  - Enlaza con Structured Outputs, Tool Calling, Context Engineering y Memory.

#### 11 - Structured Outputs.md
- **Título:** Structured Outputs
- **Propósito:** Explicar JSON schemas, constrained generation y typed outputs.
- **Puntos clave:**
  - Permite integrar salidas que se pueden parsear de manera confiable.
  - Enlaza con Prompt Engineering, Tool Calling, Context Engineering y Memory.

#### 12 - LLM APIs & Model Serving.md
- **Título:** LLM APIs & Model Serving
- **Propósito:** Explicar APIs, SDKs, inference y streaming con modelos.
- **Puntos clave:**
  - Interfaz práctica para interactuar con modelos (local u online).
  - Enlaza externamente con API Design (Software Engineering) y APIs (Backend).

#### 13 - Tool Calling.md
- **Título:** Tool Calling
- **Propósito:** Explicar cómo el modelo utiliza funciones, APIs y herramientas externas.
- **Puntos clave:**
  - Es el mecanismo que extiende al LLM más allá de generación de texto.
  - Enlaza con Prompt Engineering, Structured Outputs, Agents, AI Workflows, Context Engineering y Memory.

#### 14 - RAG.md
- **Título:** RAG (Retrieval-Augmented Generation)
- **Propósito:** Explicar cómo augmentar la generación del modelo con información recuperada externamente.
- **Puntos clave:**
  - Complementa los límites del contexto/knowledge estático del modelo.
  - Enlaza con Embeddings, Vector Databases y Context Engineering.

#### 15 - Vector Databases.md
- **Título:** Vector Databases
- **Propósito:** Explicar indexación, similarity search y retrieval de vectores.
- **Puntos clave:**
  - Infraestructura de almacenamiento optimizada para búsqueda semántica.
  - Enlaza con NoSQL (Database), Embeddings, RAG y Context Engineering.

#### 16 - Agents.md
- **Título:** Agents
- **Propósito:** Explicar planning, tools, loops, state y autonomous workflows.
- **Puntos clave:**
  - Combina varios conceptos anteriores para crear comportamiento autónomo.
  - Enlaza con Tool Calling, AI Workflows y Memory.

#### 17 - AI Workflows.md
- **Título:** AI Workflows
- **Propósito:** Explicar pipelines, orchestration, routing y parallelization con AI.
- **Puntos clave:**
  - Combina varias llamadas/pasos de AI en sistemas más grandes.
  - Enlaza con ETL/ELT y Data Pipelines (Database), más Tool Calling, Agents y Memory.

#### 18 - Context Engineering.md
- **Título:** Context Engineering
- **Propósito:** Explicar qué información recibe el modelo y en qué momento.
- **Puntos clave:**
  - Generaliza prompt engineering al diseño sistemático del contexto completo.
  - Es el concepto más conectado del bloque application-layer: 7 enlaces.

#### 19 - Memory.md
- **Título:** Memory
- **Propósito:** Explicar conversation state, long-term memory y retrieval.
- **Puntos clave:**
  - Determina si el sistema "recuerda" entre llamadas y sesiones.
  - Enlaza con Prompt Engineering, Structured Outputs, Tool Calling, Agents, Workflows y Context Engineering.

#### 20 - Evaluation.md
- **Título:** Evaluation
- **Propósito:** Explicar accuracy, relevance, groundedness y evals task-specific.
- **Puntos clave:**
  - Permite medir/validar la calidad de las salidas del modelo.
  - Enlaza con AI Safety & Security y Observability.

#### 21 - AI Safety & Security.md
- **Título:** AI Safety & Security
- **Propósito:** Explicar prompt injection, data leakage, abuse y permissions.
- **Puntos clave:**
  - Bloque de seguridad específico para sistemas con AI.
  - Enlaza externamente con Security Engineering (Software), Seguridad (Backend), HTTPS/TLS y Firewalls (Networking), más Evaluation y Observability locales.

#### 22 - Observability.md
- **Título:** Observability (AI)
- **Propósito:** Explicar traces, latency, token usage, failures y monitoring.
- **Puntos clave:**
  - Observabilidad específica para sistemas con AI (costo, latencia, errores).
  - Enlaza externamente con Observability en Software Engineering, Backend y OS/Linux, más Evaluation y AI Safety.

#### 23 - AI Infrastructure.md
- **Título:** AI Infrastructure
- **Propósito:** Explicar GPUs, inference servers, queues, caching y scaling.
- **Puntos clave:**
  - Infraestructura computacional que sostiene el entrenamiento y la inferencia.
  - Enlaza con CI/CD, Deploy & Infraestructura, Containers y Virtualization (de OS/Linux), más LLMs y Fine-tuning.

#### 24 - Fine-tuning & Adaptation.md
- **Título:** Fine-tuning & Adaptation
- **Propósito:** Explicar fine-tuning, LoRA, distillation y model adaptation.
- **Puntos clave:**
  - Métodos para especializar modelos pre-entrenados.
  - Enlaza con LLMs y AI Infrastructure.

#### 25 - AI System Architecture.md
- **Título:** AI System Architecture
- **Propósito:** Explicar el diseño completo de sistemas AI en producción.
- **Puntos clave:**
  - Cierre del área: integra todas las piezas (modelos, contexto, evaluación, infra) en un sistema real.
  - Enlaza con Architecture (Software Engineering), Arquitectura Frontend y Arquitectura de aplicaciones (Backend).


### 08 · UX & UI (26 archivos)

#### 00 - Índice UX - UI.md
- **Título:** Índice general de UX/UI
- **Propósito:** Listar los 25 conceptos del área y sus conexiones con otras áreas del mind map.
- **Puntos clave:**
  - Distinción central: UX = cómo funciona y se experimenta; UI = cómo se materializa visualmente.
  - Conecta fuerte con Product Management (11 enlaces) y Frontend (7 enlaces).

#### 01 - Human-Centered Design.md
- **Título:** Diseño centrado en el humano
- **Propósito:** Definir el enfoque de diseñar alrededor de necesidades, capacidades y contexto humano.
- **Puntos clave:**
  - Punto de partida conceptual del área (concepto 1 de 25).
  - Es el fundamento del que derivan investigación, journeys y diseño visual.

#### 02 - User Research.md
- **Título:** Investigación de usuarios
- **Propósito:** Abarcar los métodos para entender a los usuarios: entrevistas, observación y encuestas.
- **Puntos clave:**
  - Incluye investigación tanto cualitativa como cuantitativa.
  - Enlaza directamente con sus equivalentes en Product Management (User Research, User Personas).

#### 03 - User Needs & Problems.md
- **Título:** Necesidades y problemas del usuario
- **Propósito:** Identificar necesidades, pain points, objetivos y motivaciones del usuario.
- **Puntos clave:**
  - Se alimenta de la User Research y sirve de base para personas y journeys.
  - Conexión bidireccional con Product Management.

#### 04 - Personas & User Models.md
- **Título:** Personas y modelos de usuario
- **Propósito:** Modelar a los usuarios mediante segmentación, arquetipos y modelos mentales.
- **Puntos clave:**
  - Convierte datos de investigación en perfiles accionables.
  - Concepto espejo de "05 - User Personas" en Product Management.

#### 05 - User Journeys.md
- **Título:** Viajes del usuario
- **Propósito:** Mapear la experiencia del usuario con journey maps, escenarios y puntos de contacto.
- **Puntos clave:**
  - Cierra el bloque de investigación/entendimiento del usuario (conceptos 2–5).
  - Puente hacia Information Architecture y Navigation.

#### 06 - Information Architecture.md
- **Título:** Arquitectura de información
- **Propósito:** Organizar y jerarquizar la información del producto.
- **Puntos clave:**
  - Traduce el entendimiento del usuario en estructura.
  - Dependencia directa de Navigation y User Flows.

#### 07 - Navigation.md
- **Título:** Navegación
- **Propósito:** Definir cómo el usuario se mueve por el producto: menús, breadcrumbs, navegación global/local.
- **Puntos clave:**
  - Concreta la Information Architecture en patrones de uso.
  - Relacionado con User Flows para tareas completas.

#### 08 - Interaction Design.md
- **Título:** Diseño de interacción
- **Propósito:** Definir cómo el usuario interactúa con el producto.
- **Puntos clave:**
  - Conecta la navegación/IA con el diseño concreto (wireframes, prototipos).
  - Antecede al bloque visual de la carpeta.

#### 09 - User Flows.md
- **Título:** Flujos de usuario
- **Propósito:** Definir los caminos necesarios para completar tareas.
- **Puntos clave:**
  - Complementa Navigation: no solo dónde está la info, sino cómo se llega.
  - Comparte bloques relacionados con IA (06) y Navigation (07).

#### 10 - Wireframing.md
- **Título:** Wireframing
- **Propósito:** Definir la estructura antes del diseño visual.
- **Puntos clave:**
  - Paso intermedio entre interacción y prototipo.
  - Separa lo estructural de lo estético.

#### 11 - Prototyping.md
- **Título:** Prototipado
- **Propósito:** Crear prototipos low/high fidelity para validar interacción.
- **Puntos clave:**
  - Cubre desde bocetos rápidos hasta prototipos interactivos.
  - Cierra el bloque de diseño estructural (08–11).

#### 12 - Visual Hierarchy.md
- **Título:** Jerarquía visual
- **Propósito:** Guiar la atención mediante tamaño, contraste, posición, agrupación y énfasis.
- **Puntos clave:**
  - Apertura del bloque visual del área (12–17).
  - Enlaza también con Data Visualization y BI / Reporting.

#### 13 - Typography.md
- **Título:** Tipografía
- **Propósito:** Definir tipografía, escala, legibilidad y jerarquía de texto.
- **Puntos clave:**
  - Variable clave de la jerarquía visual.
  - Trío visual con Color y Spacing & Layout.

#### 14 - Color.md
- **Título:** Color
- **Propósito:** Definir paletas, contraste, significado y estados con color.
- **Puntos clave:**
  - Es tanto estético como semántico (estados, significado).
  - Dependiente de Visual Hierarchy y Typography.

#### 15 - Spacing & Layout.md
- **Título:** Espaciado y layout
- **Propósito:** Definir grid, sistemas de espaciado y composición.
- **Puntos clave:**
  - Base estructural del diseño visual.
  - Cierra el trío visual junto a jerarquía, tipografía y color.

#### 16 - Design Systems.md
- **Título:** Design Systems
- **Propósito:** Abarcar tokens, componentes, patrones y reglas compartidas.
- **Puntos clave:**
  - Puente fuerte hacia Frontend (Componentización, Arquitectura Frontend).
  - Escala el diseño visual a nivel de producto/equipo.

#### 17 - UI Components.md
- **Título:** Componentes de UI
- **Propósito:** Catalogar los bloques de interfaz: buttons, inputs, modals, cards, tables, etc.
- **Puntos clave:**
  - Vía de aplicación concreta de un Design System.
  - Enlaza de nuevo con Frontend.

#### 18 - States & Feedback.md
- **Título:** Estados y feedback
- **Propósito:** Definir los estados de la interfaz: loading, empty, success, error, disabled, hover.
- **Puntos clave:**
  - Los estados casi siempre se olvidan: estados incompletos generan mala UX.
  - Conecta con Data fetching en Frontend.

#### 19 - Responsive Design.md
- **Título:** Diseño responsive
- **Propósito:** Adaptar la interfaz a desktop, tablet y mobile.
- **Puntos clave:**
  - Concreta los componentes/states en distintos tamaños.
  - Enlaza con Layout en Frontend.

#### 20 - Accessibility.md
- **Título:** Accesibilidad
- **Propósito:** Abarcar WCAG, teclado, contraste y screen readers.
- **Puntos clave:**
  - Estándares formales (WCAG) más que heurísticas.
  - Espejo directo de "Accesibilidad" en Frontend.

#### 21 - Usability.md
- **Título:** Usabilidad
- **Propósito:** Definir la calidad de uso: facilidad, eficiencia, errores y learnability.
- **Puntos clave:**
  - Pasa del diseño al comportamiento real del usuario.
  - Central para Usability Testing y UX Metrics.

#### 22 - Usability Testing.md
- **Título:** Testing de usabilidad
- **Propósito:** Validar con tests con usuarios, tareas, observación y hallazgos.
- **Puntos clave:**
  - Referente "técnico" de Usabilidad.
  - Alimenta a UX Metrics con datos reales.

#### 23 - UX Metrics.md
- **Título:** Métricas de UX
- **Propósito:** Medir la experiencia con completion rate, time-on-task, retention, conversion.
- **Puntos clave:**
  - Conecta UX con los otros bloques métricos (Analytics, Product, Project Metrics).
  - Base para hablar de UX con lenguaje de negocio.

#### 24 - Behavior & Psychology.md
- **Título:** Comportamiento y psicología
- **Propósito:** Abarcar atención, percepción, memoria y carga cognitiva.
- **Puntos clave:**
  - Fundamento psicológico detrás de la jerarquía visual y la usabilidad.
  - Penúltimo concepto, antes de integrar todo en Product Design.

#### 25 - Product Design.md
- **Título:** Product Design
- **Propósito:** Integrar UX, UI, negocio, tecnología y producto.
- **Puntos clave:**
  - Punto de cierre y síntesis de todo el área.
  - Enlaza con Product Thinking y Value Proposition en Product Management.

### 09 · Product Management (26 archivos)

#### 00 - Índice Product Management.md
- **Título:** Índice general de Product Management
- **Propósito:** Listar los 25 conceptos del área y sus conexiones con otras áreas del mind map.
- **Puntos clave:**
  - Cambia el foco respecto a UX: qué producto construir, no solo cómo.
  - Conecta con UX & UI (11 enlaces) y Project Management (8 enlaces).

#### 01 - Product Thinking.md
- **Título:** Product Thinking
- **Propósito:** Definir la forma de pensar en problemas, usuarios, valor y resultados.
- **Puntos clave:**
  - Concepto raíz del área (1 de 25).
  - Conecta con Product Design en UX & UI.

#### 02 - Problem Discovery.md
- **Título:** Discovery de problemas
- **Propósito:** Identificar problemas reales antes de pensar en soluciones.
- **Puntos clave:**
  - Primera etapa del ciclo product thinking.
  - Se apoya en User Research y Market Research.

#### 03 - User Research.md
- **Título:** Investigación de usuarios (PM)
- **Propósito:** Abarcar necesidades, comportamiento y entrevistas para decisiones de producto.
- **Puntos clave:**
  - Espejo de User Research en UX & UI (4 enlaces cruzados).
  - Alimenta personas y problem discovery.

#### 04 - Market Research.md
- **Título:** Investigación de mercado
- **Propósito:** Analizar mercado, competidores y alternativas.
- **Puntos clave:**
  - Complementa la vista interna (usuarios) con la externa (mercado).
  - Cierra el bloque de discovery/entendimiento (01–05).

#### 05 - User Personas.md
- **Título:** Personas de usuario (PM)
- **Propósito:** Segmentar usuarios en perfiles concretos.
- **Puntos clave:**
  - Traduce la investigación en segmentos accionables.
  - Conexión directa con Personas & User Models en UX & UI.

#### 06 - Value Proposition.md
- **Título:** Propuesta de valor
- **Propósito:** Definir qué valor ofrece el producto y para quién.
- **Puntos clave:**
  - Génesis de la línea estratégica del área (06–11).
  - Conecta estrategia de producto con negocio (Product Design, Strategy at Scale).

#### 07 - Product Vision.md
- **Título:** Visión de producto
- **Propósito:** Definir la dirección futura del producto.
- **Puntos clave:**
  - Norte de largo plazo del que derivan estrategia, goals y roadmap.
  - Punto de partida de la línea estratégica.

#### 08 - Product Strategy.md
- **Título:** Estrategia de producto
- **Propósito:** Definir cómo llegar desde la situación actual hacia la visión.
- **Puntos clave:**
  - Traduce visión en plan de acción.
  - Base para goals, roadmap y estrategia a escala.

#### 09 - Goals & Outcomes.md
- **Título:** Metas y resultados
- **Propósito:** Definir objetivos y resultados esperados del producto.
- **Puntos clave:**
  - Hace medible la estrategia del producto.
  - Enlaza con roadmap y estrategia at scale.

#### 10 - Product Roadmap.md
- **Título:** Roadmap de producto
- **Propósito:** Comunicar dirección y evolución prevista del producto.
- **Puntos clave:**
  - Cierra la línea estratégica concreta (06–10).
  - Puente hacia Project Management (Planning, Scheduling, Milestones & Releases).

#### 11 - Prioritization.md
- **Título:** Priorización (PM)
- **Propósito:** Decidir qué hacer y qué no hacer.
- **Puntos clave:**
  - Dueto directo con Prioritization en Project Management.
  - Antes de requirements/stories.

#### 12 - Requirements.md
- **Título:** Requisitos (PM)
- **Propósito:** Definir necesidades funcionales y no funcionales.
- **Puntos clave:**
  - Abre el bloque de definición de trabajo (12–14).
  - Espejo directo con Requirements en Project Management.

#### 13 - User Stories.md
- **Título:** User Stories
- **Propósito:** Expresar necesidades desde la óptica del usuario.
- **Puntos clave:**
  - Refinamiento de requirements en lenguaje de usuario.
  - Enlaza con Project Management para su ciclo de trabajo.

#### 14 - Product Discovery.md
- **Título:** Product Discovery
- **Propósito:** Explorar soluciones antes de construir.
- **Puntos clave:**
  - Inicio del ciclo de validación (14–16).
  - Conexión directa con MVP y Experimentation.

#### 15 - MVP.md
- **Título:** MVP (Minimum Viable Product)
- **Propósito:** Crear el producto mínimo para validar una hipótesis.
- **Puntos clave:**
  - Nodo central conectado con Product-Market Fit, Lifecycle y Go-to-Market.
  - Relación fuerte con Experimentation y Discovery.

#### 16 - Experimentation.md
- **Título:** Experimentación
- **Propósito:** Validar hipótesis mediante experimentos y A/B testing.
- **Puntos clave:**
  - Da rigor al discovery y al MVP.
  - Alimenta a Product Metrics con datos de causa/efecto.

#### 17 - Product Metrics.md
- **Título:** Métricas de producto
- **Propósito:** Abarcar métricas para evaluar el producto.
- **Puntos clave:**
  - Empieza el bloque de análisis (17–20).
  - Conecta con Analytics, UX y Project Metrics.

#### 18 - Funnels.md
- **Título:** Funnels
- **Propósito:** Modelar el recorrido Acquisition → Activation → Conversion → Retention.
- **Puntos clave:**
  - Modelo clásico del comportamiento del usuario.
  - Base para Retention y Product Analytics.

#### 19 - Retention.md
- **Título:** Retención
- **Propósito:** Medir el uso recurrente y comportamiento a lo largo del tiempo.
- **Puntos clave:**
  - Una de las señales más fuertes de la salud del producto.
  - Conexión directa con Funnels y Product Analytics.

#### 20 - Product Analytics.md
- **Título:** Analytics de producto
- **Propósito:** Analizar comportamiento dentro del producto.
- **Puntos clave:**
  - Cierra el bloque de métricas (17–20).
  - Depende de Product Metrics, Funnels y Retention.

#### 21 - Product-Market Fit.md
- **Título:** Product-Market Fit
- **Propósito:** Definir la relación entre problema, producto y mercado.
- **Puntos clave:**
  - Concepto clave de validación en ciclo de vida temprano.
  - Conecta MVP, Lifecycle y Go-to-Market.

#### 22 - Product Lifecycle.md
- **Título:** Ciclo de vida del producto
- **Propósito:** Modelar Discovery → Launch → Growth → Maturity.
- **Puntos clave:**
  - Marco temporal del producto.
  - Interconectado con MVP, PMF y Go-to-Market.

#### 23 - Stakeholder Management.md
- **Título:** Gestión de stakeholders (PM)
- **Propósito:** Manejar la relación con usuarios, negocio, ingeniería, diseño y dirección.
- **Puntos clave:**
  - Dueto directo con Stakeholder Management en Project Management.
  - Conecta también con Technical Leadership en Software Engineering.

#### 24 - Go-to-Market.md
- **Título:** Go-to-Market
- **Propósito:** Definir lanzamiento, distribución, pricing y adopción.
- **Puntos clave:**
  - Puente hacia el mercado real.
  - Integrado con MVP, PMF y Lifecycle.

#### 25 - Product Strategy at Scale.md
- **Título:** Estrategia de producto a escala
- **Propósito:** Abarcar portfolio, plataformas, crecimiento y decisiones de largo plazo.
- **Puntos clave:**
  - Punto de cierre del área con visión de largo plazo.
  - Depende de toda la línea estratégica (Value Prop, Vision, Strategy, Goals, Roadmap).

### 10 · Project Management (26 archivos)

#### 00 - Índice Project Management.md
- **Título:** Índice general de Project Management
- **Propósito:** Listar los 25 conceptos del área y sus conexiones con otras áreas del mind map.
- **Puntos clave:**
  - Cambia el foco: no qué producto construir, sino cómo coordinar el trabajo para producirlo.
  - Conecta fuerte con Software Engineering (9 enlaces) y Product Management (8 enlaces).

#### 01 - Project Fundamentals.md
- **Título:** Fundamentos de proyecto
- **Propósito:** Definir el concepto base de proyecto con objetivos, alcance y restricciones.
- **Puntos clave:**
  - Concepto raíz del área (1 de 25).
  - Origen natural de Scope, Requirements y Deliverables.

#### 02 - Scope.md
- **Título:** Alcance
- **Propósito:** Definir qué está y qué no está dentro del proyecto.
- **Puntos clave:**
  - Se deriva directamente de los fundamentos del proyecto.
  - Base para requirements y deliverables.

#### 03 - Requirements.md
- **Título:** Requisitos (Project Management)
- **Propósito:** Definir qué debe entregarse.
- **Puntos clave:**
  - Espejo directo de Requirements en Product Management (2 enlaces cruzados).
  - Vinculado a scope, deliverables y fundamentos.

#### 04 - Deliverables.md
- **Título:** Entregables
- **Propósito:** Definir los resultados concretos del proyecto.
- **Puntos clave:**
  - Concreta lo que el scope promete.
  - Puerta hacia la descomposición del trabajo (WBS).

#### 05 - Work Breakdown Structure.md
- **Título:** Work Breakdown Structure (WBS)
- **Propósito:** Dividir trabajo complejo en partes manejables.
- **Puntos clave:**
  - Apertura del bloque de ejecución del trabajo (05–10).
  - Alimenta task management, dependencies, estimation, planning y scheduling.

#### 06 - Task Management.md
- **Título:** Gestión de tareas
- **Propósito:** Abarcar tareas, estados y responsables.
- **Puntos clave:**
  - Es la unidad mínima de trabajo.
  - Base para dependencies, estimation, planning y scheduling.

#### 07 - Dependencies.md
- **Título:** Dependencias
- **Propósito:** Abarcar las relaciones entre tareas y equipos.
- **Puntos clave:**
  - Es la estructura que define orden de trabajo.
  - Fuente de bloqueos y riesgos de scheduling.

#### 08 - Estimation.md
- **Título:** Estimación
- **Propósito:** Abarcar la estimación de tiempo, esfuerzo y complejidad.
- **Puntos clave:**
  - Conexión con Engineering Processes en Software Engineering.
  - Base de planning, scheduling y project metrics.

#### 09 - Planning.md
- **Título:** Planificación
- **Propósito:** Abarcar la secuencia y organización del trabajo.
- **Puntos clave:**
  - Conexión directa con Product Roadmap en Product Management.
  - Integración de WBS, tasks, dependencies, estimation, scheduling y milestones.

#### 10 - Scheduling.md
- **Título:** Scheduling
- **Propósito:** Abarcar fechas, milestones y deadlines.
- **Puntos clave:**
  - Concreción temporal del planning.
  - Conecta con Product Roadmap y Milestones & Releases.

#### 11 - Prioritization.md
- **Título:** Priorización (proyectos)
- **Propósito:** Abarcar el orden de ejecución.
- **Puntos clave:**
  - Dueto directo con Prioritization en Product Management.
  - Aspecto operativo del planning.

#### 12 - Resource Management.md
- **Título:** Gestión de recursos
- **Propósito:** Abarcar personas, tiempo, presupuesto e infraestructura.
- **Puntos clave:**
  - Inicio del bloque de gestión de recursos/riesgos (12–15).
  - Enlaza directo con Budget & Cost.

#### 13 - Risk Management.md
- **Título:** Gestión de riesgos
- **Propósito:** Abarcar la identificación y mitigación de riesgos.
- **Puntos clave:**
  - Opuesto conceptual a Issue Management (riesgo = aún no ocurrió).
  - Compone el trío riesgos-problemas-cambios (13–15).

#### 14 - Issue Management.md
- **Título:** Gestión de problemas
- **Propósito:** Abarcar el manejo de problemas que ya ocurrieron.
- **Puntos clave:**
  - Complemento reactivo de Risk Management.
  - Relación estrecha con Change Management.

#### 15 - Change Management.md
- **Título:** Gestión de cambios
- **Propósito:** Controlar cambios de alcance/requisitos.
- **Puntos clave:**
  - Cierra el bloque de gestión de la incertidumbre (13–15).
  - Transición hacia el bloque Agile (16–18).

#### 16 - Agile.md
- **Título:** Agile
- **Propósito:** Abarcar iteración, adaptación y feedback.
- **Puntos clave:**
  - Filosofía general detrás de metodologías concretas.
  - Base de Scrum y Kanban; conexión con Engineering Processes.

#### 17 - Scrum.md
- **Título:** Scrum
- **Propósito:** Abarcar sprints, backlog, ceremonies y roles.
- **Puntos clave:**
  - Implementación concreta de Agile.
  - Dueto con Kanban; unión con Engineering Processes.

#### 18 - Kanban.md
- **Título:** Kanban
- **Propósito:** Abarcar flow, WIP y cycle time.
- **Puntos clave:**
  - Alternativa/complemento de Scrum enfocado en flujo.
  - Métricas propias conectan con Project Metrics.

#### 19 - Milestones & Releases.md
- **Título:** Milestones y releases
- **Propósito:** Definir puntos importantes y entregas del proyecto.
- **Puntos clave:**
  - Concreción de la línea temporal de entregas.
  - Conecta con Product Roadmap y el planning.

#### 20 - Status & Reporting.md
- **Título:** Estado y reporting
- **Propósito:** Comunicar estado, progreso y bloqueos.
- **Puntos clave:**
  - Comunicación con stakeholders y coordinación de equipo.
  - Base para transparencia en el proyecto.

#### 21 - Stakeholder Management.md
- **Título:** Gestión de stakeholders (proyectos)
- **Propósito:** Abarcar comunicación y alineamiento de stakeholders.
- **Puntos clave:**
  - Espejo directo con Stakeholder Management en Product Management.
  - Conecta con Technical Leadership en Software Engineering.

#### 22 - Team Coordination.md
- **Título:** Coordinación de equipo
- **Propósito:** Abarcar dependencias y colaboración de equipo.
- **Puntos clave:**
  - Aspecto humano del project management.
  - Conecta con stakeholder y reporting; puente hacia Software Engineering.

#### 23 - Budget & Cost.md
- **Título:** Presupuesto y costo
- **Propósito:** Abarcar recursos financieros y trade-offs.
- **Puntos clave:**
  - Dueto directo con Resource Management.
  - Definición de límites económicos del proyecto.

#### 24 - Project Metrics.md
- **Título:** Métricas de proyecto
- **Propósito:** Abarcar velocity, cycle time, throughput y predictability.
- **Puntos clave:**
  - Conecta con las otras tres áreas métricas (UX, Product, Analytics).
  - Base para retrospectivas y mejoras.

#### 25 - Retrospectives & Improvement.md
- **Título:** Retrospectivas y mejora
- **Propósito:** Abarcar el aprendizaje y la mejora del proceso.
- **Puntos clave:**
  - Concepto de cierre del área.
  - Alimenta Project Metrics y conecta con Engineering Processes.
