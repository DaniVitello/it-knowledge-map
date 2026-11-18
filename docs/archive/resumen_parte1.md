# Resumen Parte 1 — IT Career (raíz + DOCS)

> Generado: 2026-10-28 · Alcance: archivos `.txt`, `.py`, `.json` de la raíz y todos los archivos de `DOCS\`

---

## Parte A — Raíz

### `add_ai_markers.py`

**Propósito:** Script que agrega los marcadores `<!-- ai:start -->` / `<!-- ai:end -->` alrededor de la sección "Mis notas" de todas las notas `.md` del vault IT-Mind-Map.

- Prepara el vault para el pipeline: define dónde se autoriza escribir contenido generado (el bloque AI).
- Procesa recursivamente (`rglob`) todo el vault; si la nota ya tiene marcadores, la salta (idempotente).
- Si no encuentra la sección `## Mis notas`, también la salta sin error.
- Reescribe siempre con `utf-8` y newlines LF (normalización).
- Imprime un resumen final con contadores ok / skip / err.

### `automate_frontend_concepts.py`

**Propósito:** Automatiza, vía la CLI `notebooklm-py`, el flujo completo de crear notebook → deep research → study guide → descargar → integrar en la nota del vault (conceptos Frontend).

- Flujo por concepto: crea notebook, agrega fuentes de research (`--mode deep --import-all`), genera reporte tipo study-guide, lo descarga y lo inserta en "## Mis notas" de la nota del vault.
- Lee de cada nota el título y los bullets de "## Qué abarca" para armar la query de investigación.
- Acepta números de concepto por CLI (default: 2..6); busca las notas por prefijo numérico en `IT-Mind-Map\02 - Frontend`.
- Persistencia intermedia en la carpeta temp aprobada de OpenCode (`Temp\opencode`).
- Documenta el bug de encoding del subprocess de Windows (`UnicodeDecodeError` con `cp1252`) registrado en `DOCS\learnings.md`.

### `generar_vault_it.py`

**Propósito:** Generador del vault de Obsidian IT-Mind-Map: lee los `.txt` de conceptos por área y produce ~260 notas con índices, navegación y enlaces cruzados.

- Define las 10 áreas IT (Software Engineering, Frontend, Backend, DB/Data, Networking, OS/Linux, AI, UX/UI, Product, Project) con carpeta, id y tag por área.
- Incluye un bloque curado de grupos de relaciones (`GROUPS`): conceptos que se enlazan entre sí, además de auto-relaciones por título repetido en áreas distintas.
- Renderiza 3 tipos de nota: nota de concepto (frontmatter YAML + "Qué abarca" + "Mis notas" + "Relacionados" + navegación prev/next), índice por área, e Índice Maestro IT.
- Solo librería estándar (Python 3.8+); sanea nombres de archivo para Windows/Obsidian y valida numeración consecutiva de conceptos.
- No pisa notas de concepto existentes (protege "Mis notas") salvo con `--force`; los índices sí se regeneran siempre.

### `skills-lock.json`

**Propósito:** Lock de skills instaladas para OpenCode en este proyecto, con fuente y hash de verificación.

- Registra 3 skills del repo `addyosmani/agent-skills`: `interview-me`, `planning-and-task-breakdown`, `spec-driven-development`.
- Cada entrada guarda `sourceType: github`, la ruta del `SKILL.md` y un `computedHash` (SHA-256) para detectar modificaciones.
- Versión del formato de lock: 1.

### `AI Engineering — 25 conceptos funda.txt`

**Propósito:** Sopa tipográfica del vault: listado de los 25 conceptos fundamentales de AI Engineering que alimenta la generación del vault.

- Distinción clave del intro: AI Engineering moderna se centra en construir productos/sistemas sobre modelos existentes (LLMs), a diferencia de ML Engineering clásico.
- Cobertura: fundamentos (AI/ML, álgebra y probabilidad, redes neuronales, Transformers, LLMs, tokenization, embeddings).
- Cobertura aplicada: prompt engineering, structured outputs, LLM APIs, tool calling, RAG, vector DBs, agents, workflows, context engineering, memoria, evaluation.
- Cobertura de sistema: safety/security, observabilidad, infraestructura (GPUs, inference servers), fine-tuning (LoRA, distillation) y arquitectura de sistemas AI en producción.
- Formato: tabla `# / Concepto / Qué abarca` que `generar_vault_it.py` parsea por el prefijo de título del área.

### `Backend moderno — 25 conceptos fund.txt`

**Propósito:** Listado de los 25 conceptos fundamentales de Backend moderno para el vault.

- Intro contrasta: el Frontend abstrae interfaz/UX; el Backend concentra datos, lógica, seguridad, concurrencia y sistemas distribuidos.
- Base web: cliente-servidor, HTTP, servidor, lenguaje/runtime, routing, APIs (REST/RPC/GraphQL), middleware, validación.
- Datos: bases de datos, SQL, modelado, ORM, transacciones ACID.
- Seguridad y rendimiento: auth (sessions/JWT/OAuth), autorización (RBAC/ABAC), CORS/CSRF/XSS/injection, caching (Redis).
- Escala: asincronía/concurrencia, mensajería (queues/pub-sub), observabilidad, testing, deploy (Docker/CI-CD) y sistemas distribuidos.

### `Database / Data Analytics — 25 conce.txt`

**Propósito:** Listado de los 25 conceptos fundamentales de Bases de Datos y Data Analytics para el vault.

- Fundamentos y modelado: datos, modelado de entidades, bases relacionales.
- SQL práctico: queries, filtrado y agregación, JOINs, keys y constraints, normalización, índices.
- Integridad y motor: transacciones, ACID/isolation, arquitectura del motor, NoSQL (documento, key-value, graphs).
- Analítica: warehouses, OLTP vs OLAP, ETL/ELT, pipelines, calidad y limpieza de datos, estadística, KPIs, visualización y BI.
- Cierre avanzado: lakehouse, streaming y governance.

### `Frontend moderno — 25 conceptos fun.txt`

**Propósito:** Listado de los 25 conceptos fundamentales de Frontend moderno para el vault (es el área piloto de automatización).

- Fundamentos web: Internet/HTTP, HTML, CSS, layout (Flexbox/Grid), DOM.
- JavaScript: sintaxis base, avanzado (closures/prototypes/modules), eventos, asincronía (Promises/async), Web APIs, JSON/APIs, TypeScript.
- Aplicación: componentización, frameworks UI (React/Vue/Angular/Svelte), estado, routing SPA, formularios, data fetching, auth in-frontend.
- Calidad y escala: accesibilidad, tooling (Vite/bundlers/ESLint), testing, performance (Web Vitals), rendering moderno (CSR/SSR/SSG/hydration) y arquitectura frontend.
- Es el área que automatiza `automate_frontend_concepts.py` (conceptos 02–06: HTML, CSS, Layout, DOM, JavaScript).

### `Networking / Internet — 25 conceptos.txt`

**Propósito:** Listado de los 25 conceptos base de Networking e Internet para el vault.

- Base de red: Internet, IP, IPv4/IPv6, TCP vs UDP, puertos, DNS, DHCP, MAC/Ethernet, ARP.
- Encaminamiento: routing, routers, NAT, subnetting/CIDR, modelo OSI/TCP-IP.
- Web: HTTP, HTTPS/TLS, request/response, métodos, status codes, headers/cookies.
- En tiempo real e infra: WebSockets, proxies/reverse proxies, firewalls, CDN y load balancing.
- El título usa "Qué entendés" (no "Qué abarca") como segunda columna; el parser del generador soporta ambos.

### `Operating Systems / Linux — 25 conce.txt`

**Propósito:** Listado de los 25 conceptos fundamentales de Operating Systems y Linux para el vault.

- Núcleo del sistema: qué hace un SO, kernel, procesos, threads, CPU scheduling, memoria (RAM, virtual, stack/heap).
- Recursos: file systems, permisos, users/groups, system calls, I/O, IPC, sockets, variables de entorno.
- Linux práctico: shell, CLI (pipes/redirecciones), scripting Bash, señales, daemons/servicios, package management.
- Red y operación en Linux: interfaces/puertos/rutas, logs y monitoreo del sistema.
- Ciclo de vida: namespaces, Docker, containers, virtualización, VMs y cloud.

### `Product Management — 25 conceptos.txt`

**Propósito:** Listado de los 25 conceptos de Product Management para el vault.

- Thinking y discovery: product thinking, problem discovery, user/market research, personas, value proposition.
- Estrategia: product vision, strategy, goals/outcomes, roadmap, priorización, requirements, user stories.
- Construcción y validación: product discovery, MVP, experimentación/A-B, product metrics, funnels, retention, product analytics, product-market fit.
- Ciclo y organización: product lifecycle, stakeholder management, go-to-market (pricing/distribución).
- Escala final: portfolio, plataformas y decisiones de largo plazo (Product Strategy at Scale).

### `Project Management — 25 conceptos.txt`

**Propósito:** Listado de los 25 conceptos de Project Management para el vault (centrado en coordinar el trabajo, no en decidir qué producto construir).

- Fundamentos: proyecto/alcance/restricciones, scope, requirements, deliverables, WBS, task management, dependencies.
- Planificación: estimation, planning, scheduling (milestones), priorización, resource management, budget.
- Riesgo y control: risk management, issue management, change management de alcance.
- Metodologías: Agile, Scrum (sprints/backlog/ceremonies), Kanban (flow/WIP), releases y status reporting.
- Cierre humano: stakeholder management, coordinación de equipo, project metrics (velocity, cycle time) y retrospectives.

### `Software Engineering — 30 conceptos.txt`

**Propósito:** Listado de los 30 conceptos fundamentales de Software Engineering, el área más extensa del vault.

- Fundamentos: programación, estructuras de datos, algoritmos, complejidad (Big O), OOP, programación funcional, abstracción.
- Diseño: modularidad, API design, error handling, concurrencia, patrones de diseño, SOLID.
- Práctica: Git/version control, code quality, clean code, code review, refactoring, documentation (ADRs), testing, debugging.
- Operación: arquitectura, design trade-offs, security engineering, CI/CD, observabilidad, confiabilidad, sistemas distribuidos.
- Madurez del rol: technical leadership (dirección técnica) y procesos de ingeniería (estimación, incident management).

### `UX / UI — 25 conceptos fundamentales.txt`

**Propósito:** Listado de los 25 conceptos fundamentales de UX/UI para el vault.

- Intro clave: UX es cómo funciona y se experimenta el producto; UI es cómo esa experiencia se materializa visual e interactivamente.
- Research UX: human-centered design, entrevistas/observación, needs & problems, personas, user journeys.
- Estructura e interacción: information architecture, navigation, interaction design, user flows, wireframing, prototyping.
- Diseño visual: jerarquía visual, tipografía, color, spacing/layout, design systems, UI components, states/feedback, responsive.
- Validación: accesibilidad (WCAG), usabilidad testing, UX metrics, psicología/carga cognitiva e integración de producto.

---

## Parte B — Carpeta `DOCS\`

### `auditoria_spec_vs_impl.md`

**Propósito:** Informe de auditoría (2026-10-28) que compara, punto por punto, la implementación del pipeline `it-concept-map` contra la especificación maestra y el diseño técnico, y halla deriva contractual importante.

- Veredicto: lo mecánico (writer seguro, state machine, runner con fases, validación parcial, piloto) existe y funciona, pero los contratos de datos y gran parte de validación/logging/reportes no matchean el diseño (diferencias D1–D23).
- Hallazgos de severidad alta: contratos de datos con vocabulario propio de la impl (y tests que refuerzan esa deriva) y validación mucho menos exigente de lo diseñado (faltan checks de contexto, relaciones, fuentes, actualidad; sin veredicto `approved|needs_fix|rejected`).
- Hallazgos medios: logging sin `run_id` ni eventos de fuente/validación, 4 fases en vez de las 11 del diseño, rutas de artefactos y backups distintas, reportes sin `needs_review` ni causa de fallo.
- Lo que SÍ está alineado: nombres de estados y transiciones, backup + escritura atómica + dry-run, marcadores ai:start/end, gestión de gaps/unverified, protección del bloque AI.
- Cierra con prioridades: alinear contratos y completar validación (alta), logging y fases (media), rutas de backup/meta.json (baja).

### `explicacion del proyecto por capas v1 - pseudo codigo.md`

**Propósito:** Documento hermano de la explicación por capas: versión en pseudo-código puro de las 11 capas del pipeline, sin código real ni snippets.

- Explica primero el orden de las capas con su justificación, siguiendo el Apéndice A del diseño y la prioridad de decisiones (integridad > correctitud > fuentes > contexto > coherencia > actualidad > pedagogía > robustez > automatización > velocidad).
- Capa 1 (ConceptMeta) cubre: qué es un concepto del vault, campos identidad/metadatos/integridad, reglas de derivación con precedencia, y todos los usos del content hash (integridad, ediciones manuales, concurrencia, idempotencia, auditoría).
- Capas 2–5: lectura/escritura del vault sin romper nada, máquina de estados con checkpoints y backoff, backend intercambiable (fake para tests + NotebookLM real) y escritura atómica con backup/restore byte a byte.
- Capas 6–8: investigación con plan por dimensiones y estrategia de fuentes, síntesis pedagógica con trazabilidad claim → fuente, y validación de 17 chequeos en dos capas (determinista + semántica) con falla cerrada.
- Capas 9–11: orquestador serial sobre ~255 conceptos con logging JSONL, CLI sin prompts interactivos (scan/inspect/run/status/reset, --dry-run, --force) y piloto de calibración previo al escalado.

### `explicacion del proyecto por capas v1.md`

**Propósito:** Documento de diseño principal del proyecto: explicación detallada por capas del pipeline de enriquecimiento de conceptos (~4.800 líneas), con justificaciones, contratos y reglas de negocio de la spec.

- Estructura: las mismas 11 capas que el pseudo-código (modelo de datos → vault → estados → backend → writer → research → síntesis → validación → runner → CLI → piloto), cada una con objetivo, comportamiento y reglas de negocio.
- Define el contrato central `ConceptMeta` (el "átomo") y el modelo de dos vidas de la nota: metadatos manuales fuera del bloque AI (fuente de verdad, nunca modificados) vs. contenido generado dentro del bloque.
- Detalla la seguridad de escritura: marcadores ai:start/ai:end, hashes SHA-256 antes/después, backups, escritura atómica temp+rename, detección de edición concurrente y modo dry-run.
- Especifica tácticas de investigación y síntesis: preguntas por dimensión (accuracy/currentness/context), estrategia de volatilidad, seeds y dominios preferidos, ciclo de cobertura para gaps, prompts versionados y separación fundamento estable / práctica moderna.
- Sirve como fuente de diseño referenciada por la auditoría, el plan de mejoras y `project_state.md`; la auditoría detectó mojibake/encoding al leerlo vía shell.

### `learnings.md`

**Propósito:** Bitácora de aprendizajes e ideas de mejora del proyecto (entradas por fecha).

- Entrada 2026-10-22: `UnicodeDecodeError: 'charmap' codec` en `subprocess.run(..., text=True)` al automatizar NotebookLM en Windows.
- Causa analizada: Windows usa `cp1252` por defecto en subprocess, pero la CLI imprime UTF-8 (tildes, emojis); la responsabilidad es del wrapper, no del servicio.
- Fix documentado: pasar explícitamente `encoding="utf-8"` y `errors="replace"` al subprocess.
- Mejora propuesta: centralizar la invocación de la CLI en un helper único y considerar usar la API Python de `notebooklm` directo en vez de parsear stdout.
- Contexto registrado: script `automate_frontend_concepts.py`, `notebooklm-py` v0.8.4, conceptos Frontend 02–06.

### `plan de mejoras v1.md`

**Propósito:** Plan v1 (2026-10-28, no ejecutado) para cerrar las brechas de la auditoría, organizado en 12 capas de mejora (A–L) basadas en las 8 críticas, 10 mayores y 11 bugs detectados.

- Diagnóstico en una frase: lo mecánico del pipeline está sólido; lo cognitivo (investigar de verdad, evaluar fuentes, no inventar) está casi vacío, con bugs puntuales y deriva contractual.
- Proceso: una capa = una sesión nueva de OpenCode agente `build` para evitar context rot (degradación de atención de LLM con contexto largo); el plan vive en disco, no en el chat; cierre por capa = tests ok + `project_state.md` actualizado + capa marcada ✅.
- Capas principales: A contratos alineados al diseño; B integridad de ejecución (4 bugs que corrompen escritura o desactivan defensas); C higiene de config/tests (`asyncio` sin importar, config muerta, test sin asserts); D–G contexto real por área, investigación con fuentes reales (seeds que nunca llegan), evaluación/conservación de fuentes y ciclo de vida del notebook.
- Capas finales: H validación determinista completa (la brecha más grave: hoy URLs inventadas y copy-paste pasan), I validación semántica + bucle needs_fix/rejected + DoD, J orquestador robusto, K trazabilidad claim→fuente + run_id/run.jsonl, L idempotencia con hash + piloto real + limpieza.
- Incluye orden de ejecución, los 11 bugs con su corrección y criterios globales de cierre.

### `project_state.md`

**Propósito:** Archivo de estado compartido del proyecto: el documento que toda sesión debe leer al inicio antes de tocar código, y actualizar al completar una capa.

- Identifica el proyecto: IT Career Concept Map, código en `it-concept-map\` (Python 3.11+, venv), vault `IT-Mind-Map\` como fuente de verdad read-only.
- Estado: las 10 capas de implementación están completadas (registry, state, writer, backend, research, synthesis, validation, runner, CLI, piloto); nota: la implementación numera 10 capas, el pseudo-código 11.
- Lista archivos clave y reglas de qué no tocar: vault (edición manual prohibida), `.venv`/`workdir`/`__pycache__`, marcadores manuales del vault, `config.yaml` salvo necesidad explícita, identidad de OpenCode.
- Registra la conexión a OpenCode de la sesión que lo escribió (server local, session/project IDs, password del service.json — con advertencia de no exponerla).
- Historial por capa con archivos, resumen técnico y tests: 15+12+11+12+12+11+9 tests verdes; el archivo contiene algunos artefactos de formato (tabulaciones y diagonales perdidas) en los bloques de las capas 5–10.

---

*Conteo: 14 archivos de la raíz (3 `.py`, 1 `.json`, 10 `.txt`) + 6 de `DOCS\` = 20 archivos procesados.*
