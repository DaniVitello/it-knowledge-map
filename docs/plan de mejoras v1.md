# Plan de mejoras v1 — pipeline `it-concept-map`

**Fecha:** 2026-10-28
**Estado:** v1 (plan escrito, sin ejecutar)
**Base material:** `auditoria_spec_vs_impl.md` (diferencias D1–D23, 8 críticas, 10 mayores, 11 bugs, prioridades sugeridas) + análisis de sesión de auditoría (8 críticas / 10 mayores / 11 bugs con causas y correcciones).

> **Nota de procedencia (importante):** la división en 12 capas A–L de este documento es una **reconstrucción de v1** elaborada a partir del material de auditoría disponible en los archivos de esta laptop. La conversación original donde se esbozó la escala A–L no quedó persistida en ningún archivo ni sesión guardada acá. Si la versión original (laptop 1) difiere, corregir este documento y **aumentar a v2** para no pisar la trazabilidad.

---

## 0. Cómo usar este plan

- **Una capa = una sesión nueva de OpenCode.** Ver §4 (context rot y sesiones nuevas).
- Cada sesión abre en `C:\Users\DGVit\Proyectos\IT Career\`, agente `build`, y recibe: este documento (solo su capa) + `project_state.md` + los archivos de la capa.
- Cada capa termina cuando: los tests corren (`py -m pytest`, dentro de `it-concept-map\.venv`), `py_compile` pasa, el vault `IT-Mind-Map\` queda intacto, y `project_state.md` (secciones 2 y 6) queda actualizado.
- Este documento es el registro de avance: al cerrar una capa, marcarla ✅ en la tabla del §3.

---

## 1. El problema en una frase

Lo mecánico del pipeline (escribir en el vault sin romper nada: writer, state machine, backend) está sólido y hasta mejorado; **lo cognitivo (investigar de verdad, evaluar fuentes y no inventar) está casi vacío**, y encima hay bugs concretos, config muerta y deriva contractual entre la implementación y el diseño/spec.

---

## 2. Diagnóstico resumido (por qué estas capas)

| Dimensión | Estado según auditoría | Capa que lo resuelve |
|---|---|---|
| Contratos de datos (D1: ConceptMeta, Source, ResearchPlan, Synthesis, ValidationReport, WriteResult, ConceptState) | Deriva contractual alta; tests refuerzan el vocabulario de la impl | **A** |
| Bugs que corrompen escritura o desactivan defensas (ConceptMeta parcial, FAILED→writing, transiciones directas, escritura no atómica) | 4 bugs de integridad | **B** |
| Config muerta / desincronizada, test vacío, `asyncio` sin importar | 5 bugs de higiene | **C** |
| Contexto por área (`areas.json` no integrado, dominios que no coinciden, roles inventados) | Crítica 🔴 1.7 | **D** |
| Investigación real (3 preguntas fijas, 0 fuentes subidas, seeds que nunca llegan) | Crítica 🔴 1.2 + bugs 1 y 9 | **E** |
| Evaluación/conservación de fuentes (jerarquía de 4 niveles, prompt P2, hashes: cero) | Crítica 🔴 1.3 | **F** |
| Ciclo de vida del notebook (se borra antes de tiempo; reconcile nunca invocado; sin reutilización) | Crítica 🔴 1.1 | **G** |
| Validación determinista (checks de integridad son stubs vacíos: URLs inventadas, copy-paste y wikilinks inválidos pasan) | Crítica 🔴 1.4 — **la brecha más grave** | **H** |
| Validación semántica P5 + bucle `needs_fix`/`rejected` + DoD del `completed` | Críticas 🔴 1.5, 1.6, 1.8 | **I** |
| Orquestador (retry con backoff nunca invocado, reanudación frágil por strings, CLI incompleta, `except` que silencia fallos) | Mayores 2.3/2.6 | **J** |
| Logging/trazabilidad/reportes (sin `run_id`, sin `run.jsonl`, sin trazabilidad claim→fuente, sin pie en la nota) | Mayor 2.6, D11/D12 | **K** |
| Idempotencia con hash, piloto real con criterios, doc y limpieza final | Mayores 2.7/2.9/2.10 | **L** |

---

## 3. Estado de ejecución

| Capa | Tema | Estado |
|---|---|---|
| A | Contratos de datos alineados al diseño | ✅ Completada (2026-10-29) |
| B | Integridad de ejecución (bugs 2–5) | ✅ Completada (2026-10-29) |
| C | Higiene de config, tests y arranque (bugs 6–8, 10, 11) | ✅ Completada (2026-10-29) |
| D | Contexto por área: `areas.json` integrado | ✅ Completada (2026-10-28) |
| E | Investigación con fuentes reales (bugs 1 y 9) | ✅ Completada (2026-10-29) |
| F | Evaluación y conservación de fuentes | ✅ Completada (2026-10-29) |
| G | Ciclo de vida del notebook | ✅ Completada (2026-10-29) |
| H | Validación determinista completa | ✅ Completada (2026-10-29) |
| I | Validación semántica P5 + bucle de corrección + DoD | ✅ Completada (2026-10-29) |
| J | Orquestador robusto | ✅ Completada (2026-10-29) |
| K | Trazabilidad, logging y reportes | ✅ Completada (2026-10-29) |
| L | Idempotencia con hash + piloto real + limpieza | ✅ Completada (2026-10-29) |

---

## 4. Nota sobre context rot y sesiones nuevas

**Qué es context rot.** La eficacia de un LLM degrada cuando el contexto crece y envejece: con 50+ mensajes de sesión (o millones de tokens de caché acumulados), el modelo olvida instrucciones tempranas, mezcla decisiones viejas con el código actual, "defiende" hipótesis que ya fueron descartadas y comete más errores de pequeña escala. No es un límite binario de ventana: es degradación progresiva de la *calidad de la atención* sobre un contexto largo.

**Aplicado a este proyecto.** Las capas de este plan tienen ~misma dificultad, pero una sesión que arranca "limpia" con solo la capa que le toca rinde mejor que una sesión que ya cargó toda la auditoría, el diseño técnico, la spec de 977 líneas y tres capas de código anteriormente corregido. Hoy las sesiones de auditoría del proyecto ya corren cerca del techo de contexto (~88M de tokens de caché de lectura acumulados): seguir ahí garantiza context rot durante la corrección.

**Regla de trabajo:**

1. **Una capa, una sesión nueva.** Abrir OpenCode parado en `C:\Users\DGVit\Proyectos\IT Career\`, agente `build`, sesión con título de la capa (ej. `Mejora capa H — validación determinista`).
2. **El plan vive en disco, no en la memoria del chat.** Este documento es el ancla: cada sesión solo necesita la sección de su capa + los archivos que toca. Nada de arrastrar el historial de la capa anterior.
3. **Cierre de sesión por capa:** tests ok → actualizar `project_state.md` → marcar la capa ✅ en §3 de este documento → cerrar la sesión. Si una capa sale mal, se descarta esa sesión (y si hizo daño, se revierte con git) sin perder las demás.
4. **Beneficio extra:** trazabilidad y rollback por capa. Cada capa es una unidad de revisión humana ("mostrame qué cambió la capa F") y una unidad de revert.

---

## 5. Las 12 capas (A–L)

### Capa A — Contratos de datos alineados al diseño

- **Qué:** llevar los dataclasses de `models.py` a los esquemas del diseño técnico (punto 2) / spec (puntos 2–25): `ConceptMeta` (con `concept_id`, `path`, `content_hash_outside_ai`…), `Source` (con `source_id` "s01", `level`, `is_preferred_domain`, `is_seed`, `covers`, `retrieved_at`, `published_or_updated`, `content_hash`, `kept`, `evaluation{…}`), `ResearchPlan` (con `questions{accuracy,currentness,context}`, `relation_questions`, `queries`, `source_requirements`), `Synthesis` (con `claims[{claim_id,text,sources,status}]`, `unverified_items`), `ValidationReport` (con los 10 checks nombrados, `blocking_failures`, `verdict{approved|needs_fix|rejected}`), `WriteResult` (con `ai_block_hash`, `outside_block_hash_before/after`, `verified`), `ConceptState` (con `failure{phase,error,attempts,retryable}`, `last_good_state`). Además: validar esquemas al leer **y** al escribir artefactos JSON, y eliminar el enum duplicado `ConceptStatus` de `models.py` (que compite con `state.ConceptStatus`). Nota: ajustar `SCHEMA_VERSION` + `schema_version` en artefactos.
- **Por qué:** es la diferencia más amplia (D1-1…D1-8) y la prioridad alta #1 de la auditoría. Todo lo demás (validación, investigación, trazabilidad) se apoya en estos objetos; hoy los nombres y campos propios de la impl **ocultan la deriva**, y hasta los tests la refuerzan (`test_backend.py` construye `Source(kind="url", …)`, `ConceptMeta(id=…, note_path=…, key_ideas=…)`, validación con `is_valid/issues/warnings/score`).
- **Cómo:** redefinir dataclasses con los campos del diseño (mantener aliases de compatibilidad transitorios documentados) → actualizar tests al contrato nuevo (no escribir aliases para "hacer pasar" los tests viejos) → agregar round-trip `dataclass → JSON → dataclass` por contrato como test → regenerar artefactos de `workdir/` con `--force` al probar. Dos definiciones del mismo enum es fuente segura de bugs: quedarse solo con `state.ConceptStatus`.
- **Listo cuando:** todos los tests pasan con el vocabulario del diseño; no queda ningún `ConceptStatus` en `models.py`; leer un artefacto viejo o malformado produce error claro de esquema.

### Capa B — Integridad de ejecución (bugs 2, 3, 4, 5)

- **Qué:** corregir los cuatro bugs que pueden corromper datos o desactivar defensas: (B2) el runner reconstruye un `ConceptMeta` parcial antes del writer — pasa `ConceptMeta` completo (el del registry, con `mtime_at_read`, `outside_hash_at_read`, `newline`, `content_hash_outside`) o re-leer del vault inmediatamente antes de escribir; (B3) la fase 4 del runner entra a `writing_phase` si el estado es `VALIDATED` **o `FAILED`** — escribir el .md tras una falla de validación es una transición inválida: solo `VALIDATED` entra al writer; (B4) `synthesis.py` y `validation.py` asignan `st.status = …` directo saltándose `validate_transition` — todas las transiciones pasan por `transition_to`; (B5) escritura de artefactos con `write_text` directo (no atómica) en research/synthesis/validation — usar el helper atómico ya existente (`_atomic_write_json` en backend) o un helper común de `temp + os.replace`.
- **Por qué:** estos bugs desactivan la defensa contra edición concurrente justo antes de la operación más peligrosa (escribir en el vault), permiten escribir .md de conceptos fallados, y dejan artefactos corruptos ante un corte a mitad de escritura. Son bugs "silenciosos": hoy no detonan, pero el día que detonan, rompen la fuente de verdad.
- **Cómo:** un test por bug que **falla primero** con el código actual (rojo), luego la corrección (verde) → no refactorizar de más: son 4 correcciones puntuales → verificar que el test de edición concurrente del writer efectivamente dispara cuando llega un meta completo.
- **Listo cuando:** los 4 tests nuevos pasan; ningún módulo escribe `st.status` fuera de `transition_to`; todos los JSON de artefactos se escriben atómicamente.

### Capa C — Higiene de config, tests y arranque (bugs 6, 7, 8, 10, 11)

- **Qué:** (B6) pacing: `config.yaml` define `pacing.between_concepts_s` pero el código lee `pause_between_concepts_s` y la pausa siempre es 0 — unificar la clave (elegir `between_concepts_s`) en runner y pilot, con test que valide la lectura de config; (B7) el bloque `validation` de `config.yaml` (`required_sections`, `min_words`, `strict_mode`) no lo lee nadie y además **difiere** del contrato hard-codeado en synthesis/validation — decidir una sola fuente de verdad (se recomienda: el código define las secciones canónicas y el config se limpia en la capa H, si H requiere parametrización); (B8) `timeouts.generate_report/download` de config sin efecto alinear con `NotebookLM.DEFAULT_TIMEOUTS` o quitar las claves; (B10) `test_persist_error_razon` no tiene asserts — escribir los asserts que su nombre promete (o eliminarlo si la razón la cubre otro test); (B11) `import asyncio` faltante a nivel módulo en `runner.py` (`run_batch` hace `await asyncio.sleep`) — `NameError` latente que va a explotar en cuanto el pacing (B6) se arregle.
- **Por qué:** config muerta y test vacío producen falsa confianza (creés que configurás algo que no tiene efecto); el `asyncio` es una bomba de tiempo acoplada al bug 6: arreglar la clave sin importar `asyncio` rompe `run_batch` en el primer batch con pausa > 0.
- **Cómo:** B11 primero (una línea), B6 con test de lectura de config, B7/B8 limpiando config y documentando la decisión, B10 con asserts reales. Correr la suite completa al terminar.
- **Listo cuando:** no queda ninguna clave de `config.yaml` que ningún código lea; el pacing efectivo se puede medir en un test; suite verde.

### Capa D — Contexto por área: `areas.json` integrado

- **Qué:** hacer que `areas.json` (10 áreas, la spec dice por área: rol senior, orientación, ejemplo/estilo, modo, fuentes preferidas) sea la fuente de verdad, según estructura `areas/<area>.yaml` del diseño §7.1: `context_framing`, `context_questions`, `professional_roles` reales (Software Engineer, PM…, no `frontend-dev` inventados), estilo/ejemplo, `preferred_domains` reales (los de `areas.json`, no los divergentes del `config.yaml` actual), `seed_urls`, `default_volatility` + `volatility_overrides`. Los prompts (síntesis, y en adelante investigación/validación) inyectan el contexto por área, no "Sos un experto en {area}".
- **Por qué:** es la crítica 🔴 1.7 y una regla de negocio de la spec ("contexto antes que definición", puntos 3 y 7): el material profesional que le da sentido de destino a cada nota. Hoy queda reducido a un titular de área; peor, los dominios del config **no coinciden** con los de `areas.json`.
- **Cómo:** leer `areas.json` (Desktop, junto a la spec) → generar `it-concept-map/areas/<area>.yaml` → módulo pequeño de carga con merge prioridad: override por concepto > override por área > frontmatter > defaults → integrar la carga en registry/config → test por área (que dominios y roles pasen).
- **Listo cuando:** el prompt de síntesis recibe rol/orientación/contexto real del área; los dominios preferidos que ve el backend son los de `areas.json`; la divergencia del config viejo desaparece.

### Capa E — Investigación con fuentes reales (bugs 1 y 9)

- **Qué:** la investigación de verdad según el diseño §4: construir `ResearchPlan` (persistir `research_plan.json`) con prompt **P1**; preguntas por las 3 dimensiones (accuracy/currentness/context) **y por cada conexión** (`relation_questions[{with, ask}]`); `queries` y `source_requirements{min_level1_or_2, min_context_sources}`; **subir fuentes al notebook**: seeds (`seed_urls`) y dominios preferidos primero — hoy `concept.seed_urls and [] or []` evalúa **siempre** `[]` (bug B1) y las semillas jamás llegan —; búsquedas dirigidas a brechas con ciclos de cobertura (diseño §4.1.5, manejo `gap` §4.2); al cerrar, setear `gaps_detected`/`gaps_resolved`/`gap_pass_done` de `RawResearch` (bug B9, hoy nunca se setean). Si NotebookLM no automatiza búsqueda de dominios preferidos, **declarar explícitamente el modo "fuentes del autor"** en la spec del pipeline (decisión del Apéndice C), en vez del falso modo "investiga solo".
- **Por qué:** crítica 🔴 1.2: la regla de negocio central ("investigar antes de sintetizar", punto 13) queda reducida a 3 preguntas fijas y cero fuentes reales; el prompt de síntesis hoy recibe "FUENTES DISPONIBLES: (vacío)" con backend real. Es la superficie sin la cual la validación (H) no tiene qué validar.
- **Cómo:** arreglar el bug de seeds (expresión real: `sources=list(concept.seed_urls or [])`) → prompt P1 → ciclo de cobertura con `gap` → persistir `research_plan.json` (diseño §10, artefacto faltante) → integrar dominios/seeds de la capa D → tests con FakeBackend garantizando que seeds y plan llegan.
- **Listo cuando:** un concepto con `seed_urls` las recibe el notebook; `research_plan.json` existe y cumple el esquema de A; los campos de gaps se setean; pregunta por conexión existe en el plan.

### Capa F — Evaluación y conservación de fuentes

- **Qué:** implementar la fase de evaluación/conservación (diseño §5, fase [D] del pipeline): `Source` completa (con la base que dejó la capa A), prompt **P2** de evaluación de fuente (authority/currentness/context_fit/covers), reglas de conservación y descarte (duplicados, SEO descartable con razón registrada — evento de log para la capa K): `kept: true/false` + `evaluation.reason`; conservación por copyright: `sources_raw/<source_id>.txt` con extracto breve + URL + `content_hash` (hoy no se conserva **nada** del contenido de las fuentes); métricas de diagnóstico §5.4 para el reporte de la capa K.
- **Por qué:** crítica 🔴 1.3: sin evaluación, el pipeline no distingue fuente de jerarquía 1 de SEO; sin conservación local, no existe "modo de respaldo sin NotebookLM" (decisión 5 del Apéndice C no resuelta) y la trazabilidad claim→fuente (capa K) no tiene material.
- **Cómo:** prompt P2 versionado (schema de la capa K) → pipeline de fuentes: hallar → evaluar → conservar/descartar (con evento y razón) → persistir `sources.json` completo + `sources_raw/` → tests con FakeBackend (que empiece a devolver fuentes con campos completos).
- **Listo cuando:** fuentes con evaluación y conservación persistidas; un concepto en modo sin red puede sintetizar desde el local; duplicados descartados con razón registrada.

### Capa G — Ciclo de vida del notebook

- **Qué:** vida del notebook según spec punto 14 / diseño §1.1 fase [K]: **no borrar el notebook al terminar la investigación** — borrar recién después de validación y **verificación de escritura** (limpieza después del `verified` del writer); reutilización: guardar `notebook_id` en `phase_data`, si existe y es válido reutilizarlo en reintentos (reformulación de preguntas / revalidación del bucle I); reconciliación de notebooks huérfanos **invocada** al arrancar (`reconcile_orphan_notebooks` ya está implementada, nadie la llama); eventos de limpieza en log (capa K).
- **Por qué:** crítica 🔴 1.1: hoy si un campo se omitió de las respuestas, no hay notebook para reformular (el bucle de corrección I lo necesita). Además el notebook muerto consume cuota silenciosamente.
- **Cómo:** mover `delete` a la fase de limpieza del runner → persistir `notebook_id` → invocar reconcile en `run_batch`/CLI start → test: reformulación de pregunta posible después de fase de respuesta; `kill` a mitad del pipeline y la reanudación encuentra el notebook vivo.
- **Listo cuando:** delete ocurre solo tras verificación; reconcile corre al arranque y limpia huérfanos; reutilización probada.

### Capa H — Validación determinista completa

- **Qué:** activar los checks bloqueantes de integridad que hoy son **stubs vacíos** (crítica 🔴 1.4): toda URL de la nota existe en `sources.json` (bloqueante); similitud/copy-paste contra las fuentes conservadas (usa `sources_raw/` de la capa F); todo WikiLink apunta a concepto existente en el registry (hoy el loop calcula los inválidos y **no agrega el issue**); claims respaldados: toda cifra/versión/fecha relevantes verificable contra un claim con source. Además: veredicto con `blocking_failures` y score con semántica correcta: `passed/total_checks` donde `total_checks` son los 10 checks del checklist §9.2, no `len(REQUIRED_SECTIONS)+3` como hoy.
- **Por qué:** crítico: hoy un contenido inventado (URLs falsas, versiones, relaciones fuera del mapa) pasa como `is_valid=True` **y se escribe en el vault**. Es la brecha más grave frente al objetivo del proyecto: "no inventar" (punto 27). La validación es la barrera entre investigación y escritura: si es de juguete, todo lo demás se desperdicia.
- **Cómo:** cada check bloqueante con test que falla primero (fixture con URL inventada / wikilink roto / texto copiado) → conectar con la fuente de verdad de secciones decidida en C → marcar severidad por check (bloqueante o advertencia) según el diseño §9.2 → integración con el config de validación (si se decidió parametrizar).
- **Listo cuando:** los 4 checks bloqueantes disparan con fixtures reales de cada caso; score refleja los 10 checks; ningún stub devuelve `[]` "por ahora".

### Capa I — Validación semántica P5 + bucle de corrección + DoD

- **Qué:** (1) prompt **P5** "validación asistida" **que devuelve hallazgos, no veredicto final** (diseño §9.1/§6-P5): checks semánticos de contenido, contexto (uso dentro del área), relaciones (integración al mapa), profundidad y pedagogía (severidad advertencia); arreglar el marcador `"?? verificar"` del prompt por el `⚠️ verificar` de la spec. (2) Bucle de corrección (crítica 🔴 1.6): veredicto completo `approved → needs_fix → rejected`: `needs_fix` re-valida **solo lo señalado** con tope configurable; `rejected` vuelve a síntesis o investigación (por eso esta capa depende de G: sin notebook vivo no hay "volver a investigar"); hoy fallar va directo a `failed` y corta. (3) DoD del `completed` (crítica 🔴 1.8): checklist verificable del diseño §14.1 (12 ítems) antes de marcar `completed` — hoy con `low_coverage=True` el pipeline escribe el .md igual.
- **Por qué:** son las críticas 1.5, 1.6 y 1.8: la validación del diseño es de **dos capas** (determinista + semántica) — sin la semántica, un contenido "correcto en forma pero pobre en concepto" se aprueba igual; sin bucle, cada falla mata el concepto sin recuperación; sin DoD, `completed` se marca sobre promesas no verificadas.
- **Cómo:** prompt P5 versionado + parser de hallazgos → estados y transiciones del bucle (usa `needs_review`, que ya existe en la máquina de estados) → checklist DoD como función que controla `mark_completed` → tope de correcciones configurable (config) → tests: needs_fix re-valida solo lo señalado; rejected retorna; DoD frena con brecha bloqueante.
- **Listo cuando:** el pipeline completo corre: investiga → sintetiza → valida (2 capas) → corrige → escribe; `completed` solo con DoD completo; marcador `⚠️ verificar` sale a la nota tal cual.

### Capa J — Orquestador robusto

- **Qué:** el runner de verdad según diseño §11/§15: (1) reintentos por fase invocando `execute_phase_with_retry` (existe, testeado, **nunca llamado** — hoy un fallo de fase corta el concepto); contador de intentos **por fase con tope** y `retryable: false` (hoy `ConceptState.retries` existe y nada lo incrementa); (2) reanudación real desde `last_good_state` (hoy es ad-hoc por strings con checks `st.status in (…)` frágil en el runner); (3) reconciliación al arranque (ya cubierta en G, ganchear acá); (4) sub-estados de notebook del diseño §3; (5) CLI: subcomandos `pilot`, `--force-phase research|synthesis`, `validate`/`report`; (6) quitar `cli._load_concepts` con `except Exception: return []` — hoy si el vault falla, `run` "termina OK" con 0 conceptos; fallar con diagnóstico.
- **Por qué:** mayor 2.3/2.6: el pipeline no es confiable a escala (255 conceptos) si los reintentos y la reanudación son decorativos. El `except` silencioso es el peor anti-patrón del CLI: error real aparenta éxito.
- **Cómo:** mover la lógica de flujo al state machine (`resume_from_checkpoint` como transición de verdad) → retry por fase con contador persistido → CLI con los comandos y **fallo ruidoso** → tests de kill-and-resume por fase (el criterio que el piloto de la capa L va a verificar).
- **Listo cuando:** matar al proceso en cualquier fase y reanudar funciona; retry por fase con tope dispara y persiste intentos; `run` no engaña con 0 conceptos; `kpipe pilot` corre.

### Capa K — Trazabilidad, logging y reportes

- **Qué:** módulo `log` (diseño §15) con: formato JSONL (`{"ts","run_id","concept_id","phase","event","source_id","level","attempt"}`); `run_id` generado al arrancar (`run-YYYYMMDD-HHMMSS-<shortuuid>`) y pegado en `estado.json` y en todos los eventos; **`run.jsonl` global** + `events.jsonl` por concepto; flush por línea; eventos mínimos: fuente hallada/descartada/conservada con razón, consulta enviada/respuesta recibida, validación por check, escritura con hashes, reintento con causa, transición de estado, limpieza de notebook; niveles debug/info/warn/error con `--verbose` (mandar `backend_call` a debug); rotación por corrida, retención (config, default 30 días), y **nunca** secretos ni contenido de notas. Trazabilidad de afirmaciones: `claim_id → source_id → URL + content_hash` (diseño §15.2) — el `claims_index` que hoy queda vacío y la capa A define el campo; **pie de trazabilidad dentro del bloque escrito**: fecha, `prompt_version`, `run_id`, fuentes. Reportes (diseño §15.3 / piloto §14): resumen batch con `completed / failed / needs_review / omitidos` + **causa de cada fallo** (hoy `BatchReport` no tiene ni `needs_review` ni causa por concepto); diagnóstico de calidad informativo (§26: cobertura, distribución de niveles, brechas, % dominios preferidos) — como usa las métricas de F.
- **Por qué:** mayor 2.6 + D11/D12: sin `run_id` ni eventos por fuente/check, una corrida larga es inauditable (¿qué fuente se descartó y por qué? ¿qué check bloqueó?). Reproducibilidad (punto 26 de la spec) requiere `prompt_version` + `run_id` en la nota producida.
- **Cómo:** módulo `log.py` + inyección en las fases → instrumentar los eventos → pie de trazabilidad en el writer (dentro del bloque, nunca fuera) → reportes batch/pilot con causas y diagnóstico.
- **Listo cuando:** un run real produce `run.jsonl` filtrable por cualquier evento; la nota escrita incluye su pie (run_id + prompt_version + fuentes); el reporte batch distingue needs_review/omitidos con causa.

### Capa L — Idempotencia con hash + piloto real + limpieza final

- **Qué:** (1) idempotencia real (diseño §12): el skip del runner solo si `completed` **verificando** hash del bloque AI == `write_result.ai_block_hash` y afuera intacto (hoy se basa solo en el estado) + edición manual dentro del bloque → `needs_review` sin sobreescribir (diseño §12.2); reutilización de notebook si existe y válido (de G); (2) piloto real (diseño §14): ~8 conceptos deliberadamente variados (2 estables, 2 dinámicos, 1 con poca info, 1 con otra área, 1 con contenido manual…), criterios de aceptación verificables (vault intacto, idempotencia matar-y-reanudar, sin URLs fuera de fuentes, revisión humana configurable), reporte del grafo del mapa (§14.3: conceptos aislados/conexiones asimétricas — hoy nada audita el grafo); (3) limpieza final: `smoke_notebooklm.py` reescrito (usa la API de una sesión anterior que ya no existe — está roto contra la clase actual); README/pyproject actualizados (README anuncia 82 tests, la real es 80; `pyproject.description` dice "Capas 1–4"); documentar la desviación de secciones sin acentos (spec exige `## Cómo funciona` con acento; decisión razonable del vault sin acentos, pero **no documentada**); limpiar `workdir/backups/capa4-otra-sesion/` (3 versiones huérfanas de backend) y restos de config muerta.
- **Por qué:** sin idempotencia con hash, editar una nota post-`completed` y correr de nuevo la sobreescribe silenciosamente (rompe la regla "no destruir contenido manual"); el piloto es la puerta de salida al lote real y hoy sólo mide tiempos sobre la lista que se le pase; los números inflados del README son exactamente el tipo de deriva que el proyecto quiere evitar.
- **Cómo:** idempotencia con test de "edición manual → needs_review, no sobrescribir" → piloto con selección de conceptos + criterios binarios GO/NO-GO (diseño §14 / pseudo-código) → renovar README/pyproject con números reales → smoke test contra cuenta real (con la autenticación de NotebookLM ya validada en `smoke_notebooklm.py`) → eliminar/limpiar backups huérfanos.
- **Listo cuando:** la edición manual dentro del bloque se detecta; la re-corrida no toca notas editadas; el piloto produce GO/NO-GO documentado; README con números reales y conteo de tests correcto.

---

## 6. Orden de ejecución

| # | Capa | Depende de | Notas |
|---|---|---|---|
| 1 | **A** Contratos | — | Todo lo demás cambia de forma en A |
| 2 | **B** Integridad | A (B4 toca estados; A puede mover el enum) | Los 4 tests del bug en rojo→verde |
| 3 | **C** Higiene config | Independiente (B11 puede ir con B) | B6 y B11 se arreglan juntos |
| 4 | **D** areas.json | A (estructura de areas yaml) | Antes de E: E consume dominios/seeds/roles |
| 5 | **E** Investigación | A (ResearchPlan), C/D | Bug B1 se arregla acá, antes del prompt P1 |
| 6 | **F** Evaluación fuentes | A (Source completa), E (fuentes que evaluar) | Prompt P2; las fuentes brutas ya existen de E |
| 7 | **G** Notebook | A (phase_data→notebook_id); puede paralelizarse con E/F | Reusa `reconcile_orphan_notebooks`, ya implementada |
| 8 | **H** Validación determinista | A (ValidationReport), E/F (sources, claims), C (config secciones) | Los checks necesitan el material generado en E/F |
| 9 | **I** Semántica + bucle + DoD | H (veredicto/bloqueos), G (no hay "volver a investigar" sin notebook) | Depende del veredicto de H |
| 10 | **J** Orquestador | B (estados sólidos), I (bucle) | Último antes de trazabilidad para congelar el flujo |
| 11 | **K** Trazabilidad | Pipeline estable | Los eventos requieren fases trazables (surgen en E–I) |
| 12 | **L** Idempotencia + piloto + limpieza | — (casi todo) | Piloto final: la puerta de salida al lote |

**En líneas generales:** A (cimentación) → B+C (estabilizar lo existente) → D+E+F+G (reconstruir la dimensión de investigación: ahí está el grueso cognitivo faltante) → H+I (la barrera de calidad) → J (control de flujo confiable) → K (auditabilidad) → L (idempotencia + validación final). Que A vaya primero no es intuitivo pero es lo barato: invertir temprano en los contratos hace rápido todo lo demás; dejarlos para el final obligaría a rehacer trabajo doble.

**Nota sobre el orden sugerido por la auditoría.** La auditoría (§8) pone la validación como prioridad #1. Esa sugerencia es correcta en intención pero asume material que validar: validación sin `sources.json` lleno y sin claims (E/F) no valida nada real. La dependencia dura es: investigar/evaluar **primero**, validar **después**. La capa H sigue siendo crítica apenas exista material: se puede adelantar corriendo H con fixtures/stubs de fuentes y retocando después de E/F. Si preferís respetar el orden estricto de la auditoría §8, alternativa válida: A, B, E, F, H, I, D, C, G, K, J, L. Documentar en §3 cuál orden se corrió.

---

## 7. Los 11 bugs con sus correcciones

| # | Bug | Ubicación | Corrección | Capa |
|---|---|---|---|---|
| B1 | `concept.seed_urls and [] or []` evalúa **siempre** `[]` — las seed URLs jamás se suben al notebook (anula el punto 9 de la spec en la práctica; el prompt de síntesis recibe "FUENTES DISPONIBLES: (vacío)") | `research.py` (~línea 136) | Expresión real: `"sources": list(concept.seed_urls or [])` + (capa E) subir además dominios preferidos | E |
| B2 | El runner reconstruye un `ConceptMeta` parcial antes del writer (id/title/area/note_path/key_ideas/connections/frontmatter) → pierde `mtime_at_read`, `outside_hash_at_read`, `newline`, `content_hash_outside` → **desactiva la defensa de edición concurrente** justo antes de escribir | `runner.py` (fase 4) | Pasar el `ConceptMeta` completo del registry (o re-leer el archivo inmediatamente antes de escribir); nunca reconstruir a mano | B |
| B3 | El runner entra a `writing_phase` si el estado es `VALIDATED` **o `FAILED`** → permite escribir el .md de un concepto fallado + transición inválida después de que ya se escribió | `runner.py` (fase 4) | Solo `VALIDATED` entra a writing; `FAILED` va por reanudación/retry | B |
| B4 | `synthesis.py` y `validation.py` asignan `st.status = …` directo (ej. `st.status = state.ConceptStatus.SYNTHESIZED`), saltándose `validate_transition`; solo `transition_to` la impone | `synthesis.py`, `validation.py` (varias transiciones) | Todas las transiciones por `transition_to` | B |
| B5 | Escritura de artefactos con `write_text` directo (no atómica) en research/synthesis/validation; si se corta a mitad, JSON corrupto (duplica además lógica que ya existe correcta en `backend._atomic_write_json`) | `research.py`, `synthesis.py`, `validation.py` | Helper atómico común (`temp + os.replace`); un solo camino de persistencia | B |
| B6 | Pacing desincronizada: config define `pacing.between_concepts_s: 1.0`, el código lee `pause_between_concepts_s` (runner y pilot) → clave nunca matchea, pausa siempre 0 | `config.yaml` ↔ `runner.py`, `pilot.py` | Unificar clave (`between_concepts_s`) + test de lectura de config | C |
| B7 | Bloque `validation` de `config.yaml` muerto: `required_sections`/`min_words`/`strict_mode` no mapean a ningún código; el contrato real de secciones está hard-codeado y **difiere** del config (drift garantizado) | `config.yaml` ↔ `synthesis.py`/`validation.py` | Elegir una única fuente de verdad (secciones canónicas en código; config solo si H la parametriza) y borrar/leer lo demás | C (conecta con H) |
| B8 | `backend.notebooklm.timeouts.generate_report/download` definidos en config sin efecto: `NotebookLM.DEFAULT_TIMEOUTS` solo acepta `create_notebook/add_source/research/delete` | `config.yaml` ↔ `backend.py` | Alinear los timeouts del config con `DEFAULT_TIMEOUTS` (o quitar claves) | C |
| B9 | Campos de brechas de `RawResearch` (`gap_pass_done`, `gaps_detected`, `gaps_resolved`) nunca seteados (la fase de brechas del diseño §4.2 no existe) | `research.py` / `models.RawResearch` | Implementar ciclo de cobertura con gaps (capa E) y setearlos al cerrar | E |
| B10 | Test vacío: `tests/test_backend.py::test_persist_error_razon` no tiene asserts (no prueba nada, pese al nombre) | `tests/test_backend.py` | Escribir asserts de la razón de fallo de persistencia (o eliminar + reemplazar) | C |
| B11 | `asyncio` sin importar a nivel módulo en `runner.py`, pero `run_batch` hace `await asyncio.sleep(...)` → `NameError` en cuanto el pacing > 0 (hoy no explota solo porque el bug B6 tiene la pausa en 0): arreglo de un bug despierta el otro | `runner.py` | `import asyncio` a nivel módulo + test de `run_batch` con pacing > 0 | C (junto con B6) |

**Los dos bugs más peligrosos:** B1 (anula el punto 9 de la spec en silencio) y B2 (desactiva la protección más crítica justo antes de la operación más peligrosa). B6+B11 forman una "bomba de dos mangas": arreglar uno sin el otro rompe `run_batch`. Todos los tests de corrección van en rojo→verde: el test falla con el bug presente y pasa tras la corrección.

---

## 8. Criterios globales de cierre del plan

1. Los 11 bugs (§7) corregidos con test rojo→verde cada uno.
2. Las 8 críticas 🔴 resueltas: notebook hasta verificación (G), estrategia de investigación (E), evaluación/conservación de fuentes (F), validación determinista + semántica (H+I), bucle de corrección (I), contexto por áreas (D), DoD del `completed` (I).
3. Suite de tests verde y números reales en README; los tests reflejan el contrato del diseño (no el de la impl), y las desviaciones acordadas quedan documentadas.
4. Piloto GO/NO-GO de la capa L sin criterios de integridad fallando.
5. `project_state.md` actualizado capa por capa (secciones 2 y 6) — es el checkpoint compartido entre sesiones.

---

*Fin del plan de mejoras v1. Creado: 2026-10-28. Las capas A–L de esta v1 se elaboraron sobre el material de la auditoría (ver nota de procedencia); el detalle por capa es orientativo: ajustarlo en disco y subir el número de versión cuando la ejecución lo corrija.*
