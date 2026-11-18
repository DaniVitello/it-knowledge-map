# Auditoría: Especificación / Diseño técnico vs Implementación

**Fecha:** 2026-10-28
**Proyecto bajo revisión:** `C:\Users\DGVit\Proyectos\IT Career\it-concept-map`
**Documento de salida:** `C:\Users\DGVit\Proyectos\IT Career\auditoria_spec_vs_impl.md`

---

## 1. Alcance y metodología

### 1.1 Fuentes leídas

**Especificación maestra** — `C:\Users\DGVit\Desktop\# Especificaciónes.txt` (977 líneas):
Se leyeron por rangos (líneas 1–150, 151–290, 291–400, 401–530, 531–650, 651–775, 776–885, 886–977).
Puntos auditados: contexto/objetivo (1–2), regla de negocio (2), contexto antes que definición (3),
qué significa "completo" (4), dos dimensiones de completitud (5), universidad vs actualidad (6),
fuentes / niveles 1–4 (7), preferred no exclusivo (8), preferred vs seeds (9), dimensión Context (10),
objetivo técnico inmediato (11), pipeline técnico requerido (12), investigar antes de sintetizar (13),
notebook temporal (14), no perder investigación (15), idempotencia (16), protección de notas (17),
contrato de contenido (18), principio 20/80 (19), objetivo práctico (20), relaciones (21), no Wikipedia (22),
estado actual (23), validación antes de escribir (24), Definition of Done (25), métricas (26), no invención (27),
separación investigación/escritura (28), artefactos persistentes (29), fallos y recuperación (30), objetivo final (31),
prioridad de decisiones (32), qué debe hacer Claude (33), principio final (34).

**Diseño técnico del pipeline** — `C:\Users\DGVit\Downloads\diseno-tecnico-pipeline.md` (654 líneas):
Leído por rangos (1–220, 221–360, 361–465, 466–570, 571–654). Puntos 1–15 + Apéndices A–C. Design doc =
"Punto 33 de la Especificación maestra"; define los **15 puntos** que el punto 33 exige antes de implementar.

**Design docs hermanos / contexto:**
- `C:\Users\DGVit\Proyectos\IT Career\explicacion del proyecto por capas v1.md` (4844 líneas) y su pseudo-código (847).
- `C:\Users\DGVit\Proyectos\IT Career\explicacion codigo - capa N.md` (9 archivos).
- `C:\Users\DGVit\Proyectos\IT Career\project_state.md` (186 líneas).
- `C:\Users\DGVit\Proyectos\IT Career\DOCS\learnings.md` (39 líneas).
- `C:\Users\DGVit\Proyectos\IT Career\add_ai_markers.py`, `generar_vault_it.py` (475), `automate_frontend_concepts.py` (168).

**Implementación** — `C:\Users\DGVit\Proyectos\IT Career\it-concept-map\`:
- `models.py` (396 líneas), `registry.py` (722), `state.py` (812), `writer.py` (946), `backend.py` (~1348),
  `research.py` (230), `synthesis.py` (263), `validation.py` (269), `runner.py` (259), `cli.py` (173),
  `pilot.py` (202), `notebooklm_backend.py` (13), `config.yaml` (122), `pyproject.toml` (27), `README.md` (43).
- `scripts\smoke_notebooklm.py` (93).
- Tests: `tests\test_backend.py`, `test_cli.py`, `test_pilot.py`, `test_research.py`, `test_runner.py`,
  `test_synthesis.py`, `test_validation.py` + `tests\config_cli.yaml`.

**Correspondencia:** design docs, spec, estado del proyecto y código se compararon punto por punto.

### 1.2 Supuestos y límites de la auditoría

- No se modificó ningún archivo del proyecto. El único archivo creado fuera del proyecto es este informe.
- Los PDFs/ZIPs de `Downloads` y `Desktop` se usaron solo como contexto (no auditados línea por línea).
- Los fragments de salida de herramientas con límite de caracteres se releyeron en rangos más chicos cuando
  la comparación lo requería.

---

## 2. Resumen ejecutivo

**Veredicto general:** la implementación existe y es funcional (FakeBackend, state machine, writer seguro,
runner con fases, validación, piloto), pero **la implementación no está alineada con el diseño técnico ni con la
especificación maestra en los contratos de datos y en gran parte de la estrategia de validación, logging y
reportes**. Hay una **deriva contractual** importante: los artefactos JSON y los tests de la implementación usan
un vocabulario propio (`id`, `note_path`, `key_ideas`, `kind`, `markdown`+`sections`, `is_valid`+`issues`,
`WriteResult{path, backup_path, outside_hash, inside_hash, written_at, success}`), que no coincide con los
esquemas exigidos en el diseño (punto 2) y la especificación (puntos 2–25).

### 2.1 Principales diferencias detectadas

1. **Contratos de datos distintos (D1–D8).** Conceptos, fuentes, planes, síntesis, validación y escritura usan
   campos propios de la implementación en vez de los del diseño/spec. Es la diferencia más amplia y afecta a tests,
   artefactos persistidos y reproducibilidad.

2. **Validación mucho menos exigente que el diseño (D5).** El diseño define 10 checks con semántica, capa
   (determinista/semántico), severidad y regla de bloqueo (punto 9). La implementación solo ejecuta una fracción
   (secciones, longitud, preguntas de repaso, estructura, URLs, copy-paste, cross-links) y con heurísticas
   simplificadas; faltan checks de contexto, relaciones, fuentes, actualidad, integridad, seguridad de archivo y
   pedagogía, y no hay veredicto `approved | needs_fix | rejected` ni `blocking_failures` en el reporte.

3. **Logging/trazabilidad incompleto (D11).** El diseño exige JSONL con `run_id`, `phase`, eventos de fuente
   (hallada/descartada/conservada), consulta, respuesta, validación por check, escritura con hashes, reintentos,
   transiciones, limpieza, y `run.jsonl` global. La implementación escribe `events.jsonl` por concepto con un
   subset (`run_start`, `run_skip`, `phase_done`, `phase_failed`, `run_end`) y sin `run_id`.

4. **Fases del pipeline agrupadas (D2).** Diseño: 11 fases numeradas [A]–[K] (carga, estrategia, búsqueda,
   evaluación/conservación, notebook+respuesta, síntesis, normalización, validación, escritura, verificación,
   limpieza). Implementación: 4 fases ejecutables (`research`, `synthesis`, `validation`, `writing`) con
   sub-fases absorbidas.

5. **Ubicación/nomenclatura de artefactos y backups (D7, D9).** Diseño: `.pipeline/<concept_id>/backup/<timestamp>.md`,
   `sources_raw/<source_id>.txt`, `synthesis.md`, `state.sqlite`. Implementación: `workdir/concepts/<id>/...`,
   backups en `workdir/backups/<concept_id>/`, `WriteResult` con `path/backup_path/outside_hash/inside_hash`.

6. **Reportes de corrida incompletos (D12).** Diseño: resumen con completed/failed/needs_review/omitidos +
   causa de fallo + diagnóstico de calidad informativo. Implementación: `BatchReport` sin `needs_review`, sin
   causa de fallo por concepto en el resumen batch, y `PilotReport` con métricas propias.

### 2.2 Gravedad resumida

| Dimensión | Severidad |
|---|---|
| Contratos de datos (esquemas) | Alta |
| Validación (checks/veredicto) | Alta |
| Logging/trazabilidad | Media-Alta |
| Fases del pipeline | Media |
| Artefactos/backups | Media |
| Reportes | Media |
| Nomenclatura/layers | Baja-Media |

---

## 3. Diferencias encontradas (detalladas)

### 3.1 D2 — Fases del pipeline y nombres de módulos

| # | Diseño / Spec | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D2-1 | Diseño lista **11 fases** `[A] Carga → [B] Estrategia → [C] Búsqueda → [D] Evaluación/conservación → [E] Notebook+respuesta → [F] Síntesis → [G] Normalización → [H] Validación → [I] Escritura → [J] Verificación → [K] Limpieza** | Runner ejecuta **4 fases**: `research`, `synthesis`, `validation`, `writing` (runner.py, docstring línea 3–5: "Orquesta: registry -> research -> synthesis -> validation -> writer") | runner.py:69–224 | **Diferencia** |
| D2-2 | Diseño nombra módulo de adaptador **NotebookLM** y orquestador **orchestrator** | Implementación: módulo **`backend.py`** (`ResearchBackend`, `FakeBackend`, `NotebookLMBackend`, `run_research_phase`) y módulo **`runner.py`** (`Runner`, `run_concept`, `run_batch`) | backend.py:4–17; runner.py:51–69 | **Diferencia** |
| D2-3 | Diseño mapea la fase `research` a "RESEARCH + EVIDENCE" (A–E) | Implementación agrupa evaluación/conservación dentro de research (`run_research_phase`, `FakeBackend.research` con sources/evaluation) | backend.py:17, 105–152; research.py:50–110 | **Aproximación** |
| D2-4 | Diseño separa fase de **normalización** (G) y **verificación de escritura** (J) como pasos propios | Implementación: normalización implícita en síntesis; verificación dentro de `writer.writing_phase`; limpieza vía `backend.cleanup` | writer.py:555–641; backend.py:430–440 | **Agrupación (aceptable?)** |

### 3.2 D1 — Contratos de datos (punto 2 del diseño / puntos 2–25 de la spec)

| # | Contrato del diseño/spec | Contrato de la implementación | Evidencia | Estado |
|---|---|---|---|---|
| D1-1 | `ConceptMeta`: `schema_version`, `concept_id`, `title`, `path`, `area`, `volatility`, `professional_roles`, `connections`, `preferred_domains`, `seed_urls`, `content_hash_outside_ai` | `ConceptMeta`: `id`, `title`, `area`, `note_path`, `slug`, `numero`, `aliases`, `tags`, `key_ideas`, `connections`, `frontmatter`, `volatility`, `professional_roles`, `preferred_domains`, `seed_urls`, `has_ai_block`, `content_hash_outside`, `content_hash_inside`, `outside_hash_at_read`, `mtime_at_read`, `newline`, `has_frontmatter`, `has_bom`, `concept_dir`, `schema_version` | models.py:72–109 | **Diferencia** |
| D1-2 | `Source`: `source_id` ("s01"), `url`, `title`, `domain`, `level`, `is_preferred_domain`, `is_seed`, `covers`, `retrieved_at`, `published_or_updated`, `content_hash`, `kept`, `evaluation{authority,relevance,currentness,context_fit,reason}` | `Source`: `source_id`, `url`, `title`, `snippet`, `kind` ("url"\|"text"\|"file"), `preferred`, `seed` | models.py:120–131; test_backend.py:37–42 | **Diferencia** |
| D1-3 | `ResearchPlan`: `concept_id`, `questions{accuracy, currentness, context}`, `relation_questions[{with, ask}]`, `queries`, `source_requirements{min_level1_or_2, min_context_sources}` | `ResearchPlan`: `questions: list[ResearchQuestion]`, `concept_id`; `ResearchQuestion{qid, group("a"\|"b"\|"c"), text}` | models.py:135–152; research.py:63–74 | **Diferencia** |
| D1-4 | `RawResearch`: respuesta bruta + preguntas formuladas + `source_id` usados (guardar sin modificar) | `RawResearch`: `concept_id`, `researched_at`, `volatility`, `freshness_window_days`, `plan`, `answers`, `coverage`, `low_coverage`, `low_sources`, `gap_pass_done`, `gaps_detected`, `gaps_resolved`, `notebook_id`, `source_ids`, `duration_ms`, `backend_provider` | models.py:179–197; backend.py persistencia | **Superficie ampliada** (coincide en objetivo) |
| D1-5 | `Synthesis`: `concept_id`, `sections{objetivo, esqueleto[], ...}`, `claims[{claim_id, text, sources, status}]`, `unverified_items[]` | `Synthesis`: `concept_id`, `title`, `markdown`, `sections: dict[str,str]`, `stable_foundation`, `modern_practice`, `cross_links`, `claims_index: list[ClaimRef]`, `prompt_version`, ... | models.py:234–252; test_runner.py:106–113 | **Diferencia** |
| D1-6 | `ValidationReport`: `concept_id`, `checks{contenido, contexto, relaciones, fuentes, actualidad, profundidad, pedagogia, integridad, formato, seguridad_archivo}`, `blocking_failures`, `warnings`, `verdict{approved\|needs_fix\|rejected}` | `ValidationReport`: `concept_id`, `synthesis_path`, `checked_at`, `prompt_template_hash`, `checks: list[CheckResult]`, `errors: list[CheckResult]`, `warnings: list[CheckResult]`, `is_valid`, `blocked_reason`, `score`; alias `ValidationResult` | models.py:281–299 | **Diferencia** |
| D1-7 | `WriteResult`: `concept_id`, `written_at`, `ai_block_hash`, `outside_block_hash_before`, `outside_block_hash_after`, `verified` | `WriteResult`: `path`, `backup_path`, `outside_hash`, `inside_hash`, `written_at`, `success` | models.py:307–318; writer.py:45, 639–641 | **Diferencia** |
| D1-8 | `ConceptState`: `status`, artefactos por fase, `last_good_state`, `failure{phase,error,attempts,retryable}` | `ConceptState`: `concept_id`, `status`, `checkpoint`, `phase_data`, `retries`, `last_error`, `blocked_reason`, `created_at`, `updated_at` | models.py:326–340; state.py:34–45, 205–253 | **Diferencia** |

### 3.3 D5 — Validación (diseño punto 9 / spec punto 24)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D5-1 | 10 checks con semántica declarada: Contenido, Contexto, Relaciones, Fuentes, Actualidad, Profundidad, Pedagogía, Integridad, Formato, Seguridad de archivo. Cada uno con capa (determinista/semántico) y regla de bloqueo. | `REQUIRED_SECTIONS` (10 secciones, con "Esqueleto (el 20% esencial)"), `MIN_SECTION_CHARS=20`, `MAX_TOTAL_CHARS=14000`, `MIN_REVIEW_QUESTIONS=3`; checks implementados: `_check_sections`, `_check_total_length`, `_check_review_questions`, `_check_invented_urls`, `_check_copy_paste`, `_check_cross_links`, `_check_structure` | validation.py:24–150 | **Diferencia** |
| D5-2 | Check **Fuentes**: afirmaciones importantes con respaldo suficiente (mixto). | `_check_invented_urls` solo registra URLs y **no bloquea** ("Por ahora no bloqueamos URLs, solo las registramos como warning") | validation.py:87–93 | **Diferencia** |
| D5-3 | Check **Contexto**: uso dentro del área (semántico, bloqueante). | No implementado explícitamente. | — | **Diferencia** |
| D5-4 | Check **Relaciones**: integración al mapa (mixto, bloqueante). | `_check_cross_links` solo emite warning si el link no está en `connections`; no valida prere/dependientes. | validation.py:103–112 | **Diferencia** |
| D5-5 | Check **Actualidad**: sensible al tiempo verificado o marcado (mixto, bloqueante). | No implementado (síntesis guarda `coverage`, `stable_foundation`, `modern_practice`). | — | **Diferencia** |
| D5-6 | Check **Seguridad de archivo**: solo se modifica el bloque permitido (determinista, bloqueante). | No aparece como check; se asume cubierto en writer (no en validación). | writer.py:556–641 | **Diferencia de capa** |
| D5-7 | Veredicto: `approved | needs_fix | rejected`; `blocking_failures`; `warnings`. | `ValidationPhaseResult{is_valid, issues, warnings, score}`; estado transiciona a `validated`/`failed`; `blocked_reason` en reporte. No hay veredicto `needs_fix`. | validation.py:42–50, 240–259; models.py:292 | **Diferencia** |
| D5-8 | Profundidad y Pedagogía: severidad **advertencia**. | Warnings genéricos de secciones <40 chars. | validation.py:144–147 | **Aproximación** |
| D5-9 | Score: heurística `passed/total_checks` con `total_checks = len(REQUIRED_SECTIONS)+3` — no corresponde a los 10 checks del diseño ni a ponderación de calidad. | Igual implementación. | validation.py:224–226 | **Diferencia de semántica** |

### 3.4 D7 — Política y protocolo de escritura (diseño punto 13)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D7-1 | Backup de la nota en `.pipeline/<concept_id>/backup/<timestamp>.md` | Backup en `workdir/backups/<concept_id>/` (ej. `raw_research.json.*.bak` según tests; copia byte a byte con mtime) | writer.py:23, 539, 650–658; test_backend.py:149–150 | **Diferencia** |
| D7-2 | Escritura atómica: temp + rename; backup antes; reemplazar interior; re-leer y verificar `outside_hash_after == before`, bloque == síntesis validada, frontmatter válido, título/navegación/"Mis notas"/WikiLinks fuera del bloque intactos. Si falla → restaurar backup y `failed`. | Implementado en `writer.writing_phase` (dry-run con `DiffResult`, atomic write tmp+os.replace, restore byte a byte) | writer.py:5–7, 23–25, 518–541, 555–641 | **Coincide** |
| D7-3 | Si faltan marcadores, no insertar automáticamente salvo config explícita; concepto `failed` con causa `missing_markers`. | Docstring writer valida ausencia de markers; no se verificó el camino de `missing_markers` en runner/state | writer.py:105; runner.py:88–107 | **Parcial** |
| D7-4 | `--dry-run` genera todo y muestra diff sin escribir. | Implementado (`dry_run` → `DiffResult`, writer.py:604–613). | writer.py:604 | **Coincide** |

### 3.5 D11 — Logging y trazabilidad (diseño punto 15)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D11-1 | Formato JSONL: `{"ts","run_id","concept_id","phase","event","source_id","level","attempt"}`; `events.jsonl` por concepto **y** `run.jsonl` global. | Eventos: `run_start`, `run_skip`, `phase_done`, `phase_failed`, `run_end`; JSON con `ts`, `concept_id`, `event` + kwargs (p. ej. `phase`) en `concepts/<id>/events.jsonl`. Sin `run_id`, sin `run.jsonl`. | runner.py:61–67, 72, 84, 95, 106, 223 | **Diferencia** |
| D11-2 | Eventos mínimos requeridos: inicio/fin de fase, fuente hallada/descartada/conservada (con razón), consulta enviada, respuesta recibida, validación (por check), escritura (hashes), reintento (causa), transición de estado, limpieza de notebook. | Solo inicio/fin de fase + failure/run_end/run_skip. No hay eventos de fuentes ni de validación. | runner.py:95, 106, 223 | **Diferencia** |
| D11-3 | Cada afirmación → `claim_id` → `source_id` → URL + hash del contenido consultado; nota escrita guarda pie de trazabilidad (fecha, `prompt_version`, `run_id`, fuentes). | Síntesis guarda `prompt_version`, `prompt_template_hash`; raw research guarda `source_ids`; writer guarda hashes. Falta `run_id` en nota/pie. | models.py:246, 245; writer.py:639–641 | **Parcial** |

### 3.6 D12 — Reportes (diseño punto 15.3, piloto punto 14)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D12-1 | Resumen por corrida: completed / failed / **needs_review** / omitidos por idempotencia, con **causa de cada fallo**. | `BatchReport{total, completed, failed, blocked, skipped, results, duration_ms}`; batch summary imprime total/completed/failed/skipped (cli.py:66). No hay `needs_review` ni causa por concepto. | runner.py:38–47, 226–244; cli.py:65–66 | **Diferencia** |
| D12-2 | Diagnóstico de calidad (punto 26): cobertura, distribución de niveles, brechas, % dominios preferidos — solo informativo. | Pilot: `success_rate`, `avg_duration_ms`, `calibration{suggested_pacing_s, suggested_timeout_s}`; sin diagnóstico de calidad. | pilot.py:147–159 | **Diferencia** |

### 3.7 D8/D10 — Idempotencia, reanudación, recuperación (diseños 12 y 11)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D8-1 | Idempotencia: completed + hash bloque + outside → omitir (sin notebook ni escribir). | Runner omite si `completed` y no force/dry-run; reporta `phases_completed` inventado como las 4 fases. | runner.py:79–85 | **Aproximación** |
| D8-2 | Más de un par de marcadores → `failed` (estructura corrupta). | Verificado parcialmente (writer valida markers; manejo duplicados no confirmado en las lecturas completas). | writer.py:60–61, 105 | **Pendiente de verificación** |
| D8-3 | Edición manual dentro del bloque (hash ≠ último escrito) → `needs_review` en vez de sobrescribir. | Writer detecta cambios entre lectura/escritura (`outside_hash_at_read`, `mtime_at_read`); no se confirmó la comparación contra `ai_block_hash` previo. | models.py:102–108; writer.py:580–585 | **Parcial** |
| D8-4 | Reanudación desde `last_good_state`; reintentos con backoff y tope por fase; errores no recuperables → `failed` con causa. | `state.last_good_state`, `retries`, `transition_to`; backend con backoff/circuit breaker (`BackendCircuitOpenError`), transitorios reintentables. | state.py:205–253; backend.py:217–238, 233–238 | **Coincide** (detalle: diseño pide "tope por fase con `retryable:false`"; impl usa contadores globales de retries por backend) |

### 3.8 D9 — Estados del proceso (diseño punto 3)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D9-1 | Diagrama: `pending → researching → researched → synthesized → validated → written → completed`; `failed` conserva último bueno. | Enum `ConceptStatus` con exactamente esos nombres + `NEEDS_REVIEW`; transiciones validadas con `can_transition`/`validate_transition` | state.py:34–45, 121–136, 232–253 | **Coincide** |
| D9-2 | `failed`: `{phase, error, attempts, retryable}`; al reintentar reanudar desde `last_good_state`. | `phase_data["failed_phase"]`, `failed_reason`, `last_error`, `retries`; reanuda por checkpoints | state.py:242–253; runner.py:88–107 | **Diferencia menor** (nombres/campos) |

### 3.9 D3/D4 — Investigación, fuentes, síntesis (diseños 4–8)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D3-1 | Política de actualidad por `volatility` (`stable/semi-stable/dynamic`) + overrides por área. | `Volatility` enum en models (`SEMI_STABLE` default); overrides por concepto en meta. | models.py:28–34 | **Aproximación** |
| D3-2 | Cierre de cobertura: preguntas sin fuente → `gap`; síntesis trata como `sin verificar`. | `RawResearch.coverage`, `low_coverage`, `gap_pass_done`, `gaps_detected/resolved`; síntesis marca claims `unverified` | backend.py:383–396; models.py:188–195, 160–161 | **Coincide** |
| D3-3 | Síntesis: 3–5 ideas fundamentales (20%), orden mental→propósito→función→aplicación→relaciones→profundidad, "Objetivo" no empieza con definición, conexión sin respaldo → `⚠️ verificar`. | `CONTRACT_SECTIONS` (10), `stable_foundation`/`modern_practice`, `cross_links`, `claims_index` con `unverified` | synthesis.py; models.py:241–244 | **Aproximación** |
| D3-4 | Sin invención: `⚠️ verificar` / `sin verificar` para lo no respaldado. | Markers en síntesis (`unverified`, `low_coverage`); validación `_check_invented_urls` no bloquea. | synthesis.py; validation.py:87–93 | **Parcial** |

### 3.10 D6 — Backend / NotebookLM / fuentes (diseño punto 1.3, 5, 11.2)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D6-1 | Adaptador NotebookLM intercambiable (`create_notebook`, `add_sources`, `query`, `delete`); fallback a síntesis desde fuentes locales. | `ResearchBackend` Protocol con `research`, `cleanup`; `NotebookLMBackend` adapta `notebooklm-py` v0.8.4 (async); fallback/fake en tests. | backend.py:8–17, 408–436; notebooklm_backend.py (13 líneas) | **Coincide** (nomenclatura de ops difiere) |
| D6-2 | Fallos: backoff exponencial + tope por fase; errores no recuperables → `failed`. | Backoff, circuit breaker (`BackendCircuitOpenError`), errores transitorios reintentables (`BackendTimeout`, `BackendNetworkError`, `BackendRateLimitError`). | backend.py:217–238; config.yaml pacing/backoff/max_retries | **Coincide** |
| D6-3 | No generar URLs a mano: solo de resultados de búsqueda o `seed_urls`. | No se verificó explícitamente el guard; `ResearchRequest`/`_source_from_dict` sugieren filtrado. | backend.py:105–152, 340–364 | **Pendiente** |

### 3.11 D13–D14 — Arquitectura, artefactos persistentes (diseño punto 10)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D13-1 | Estructura `.pipeline/state.sqlite` (o `state.json`), `concepts/<id>/{meta.json, research_plan.json, sources.json, sources_raw/<sid>.txt, raw_research.json, synthesis.json, synthesis.md, validation.json, write_result.json, state.json, events.jsonl, backup/<timestamp>.md}` | `workdir/concepts/<id>/` con `raw_research.json`, `sources.json`, `synthesis.json`, `validation.json`, `state.json`, `events.jsonl`; backups en `workdir/backups/<id>/`; `WriteResult{path, backup_path, ...}` | writer.py:23, 539; state.py:312; tests | **Diferencia** |
| D13-2 | Inmutabilidad por versión: artefactos con `attempt` incrementado, no pisar hasta validar. | Backups con sufijo `.bak`; `force` re-ejecuta; `retries` en state. | test_backend.py:145–150; state.py:334 | **Aproximación** |
| D13-3 | Mínimo del punto 29: identidad, área, estado, fuentes, resultado bruto, síntesis, validación, escritura. | `RawResearch.backend_provider`, `sources`, `synthesis`, `validation`, `WriteResult` — identidad/área en `ConceptMeta`; **ausente**: persistencia de `meta.json` por concepto y de `research_plan.json`. | state.phase_data / writer | **Diferencia** |

### 3.12 D15 — Principio rector y prioridades (diseño punto 1.3, spec 32/34)

| # | Diseño | Implementación | Evidencia | Estado |
|---|---|---|---|---|
| D15-1 | Principio rector: integridad > correctitud > fuentes > contexto profesional > coherencia del mapa > actualidad > pedagogía > robustez > automatización > velocidad/costo. | No se detectó en config/code; piloto con `suggested_pacing_s` sugiere priorización por velocidad. | config.yaml; pilot.py:154–159 | **No detectado / posible ausencia** |

---

## 4. Otras diferencias detectadas (código, docs y tests)

| # | Diferencia | Detalle | Evidencia |
|---|---|---|---|
| D16 | **Nomenclatura de capas vs. orden real de fases.** Los docs de capa numeran writer como Capa 3 y backend como Capa 4, investigación como Capa 5, etc. El diseño (Apéndice A) lista writer antes que research, pero su tabla de módulos lo pone después de validation. Hay tres ordenamientos conviviendo. | README.md, `explicacion codigo - capa N.md`, design Apéndice A vs tabla de módulos | README.md; design 1.2, Apéndice A |
| D17 | **CLI.** Diseño no detalla comandos CLI; la spec pide robustez. Implementación: argparse con `run`, `status`, `list`, `reset`, `dry-run` (cli.py:122–160). Faltan comandos de `pilot`, `validate`, `synthesis`, `research` individuales. | cli.py:3, 122–160 | **Diferencia de superficie** |
| D18 | **Config.** Diseño: `areas/<area>.yaml` con `context_framing`, `preferred_domains`, `seed_urls`, `default_volatility`, `volatility_overrides`, `context_questions`. Implementación: `config.yaml` único con pacing/backend/markers (122 líneas). | config.yaml | **Diferencia de arquitectura** |
| D19 | **Tests reflejan el contrato de la implementación, no el de la spec.** Ej.: `Source(kind="url", ...)`, `ConceptMeta(id=..., note_path=..., key_ideas=...)`, `Synthesis(concept_id, title, markdown, sections)`, validación con `is_valid/issues/warnings/score`, `WriteResult` con `outside_hash/inside_hash`. | test_backend.py:24–44, 106–124, 269–266 | **Diferencia** |
| D20 | **Errores de traducción/encoding:** el design/spec están en UTF-8 legible; los archivos leídos vía shell mostraron mojibake (codificación distinta), lo que puede indicar inconsistencia de codificación en los .md fuente. | `Get-Content` del design; `read` del spec | Observación |
| D21 | **`PilotRunner` usa `__import__("time")` y `Path(self.workdir)` para reporte** (paths relativos), y `PilotMetrics.validation_score` lee `validation.json` con `score`; diseño exige métricas de calidad por check. | pilot.py:92–96, 116–121, 147–159 | **Detalle** |
| D22 | **`runner.run_concept` reporta `phases_completed` con 4 nombres** (research/synthesis/validation/writing) en el path de idempotencia, mientras el diseño lista 11 fases. | runner.py:82 | **Diferencia** |
| D23 | **Spec vs. diseño: separación investigación/escritura.** Spec punto 28 separa Research / Evidence / Synthesis / Validation / Writing. Diseño agrupa Research+Evidence; implementación solo tiene 4 fases (research ya incluye fuentes/evidence). | backend.py:17; design 1.1 | **Agrupación** |

### 3.13 Coincidencias verificadas (lo que SÍ está alineado)

- Nombres de estados (`pending`, `researching`, `researched`, `synthesized`, `validated`, `written`, `completed`, `failed`, `needs_review`).
- Transiciones con validación (`can_transition`, `validate_transition`, `resume_from_checkpoint`).
- Backup + escritura atómica + restore byte a byte + `--dry-run`.
- Bloque de escritura delimitado por `<!-- ai:start -->` / `<!-- ai:end -->`.
- `RawResearch.coverage` y gestión de `gaps`/`unverified`.
- `prompt_version` / `prompt_template_hash` en síntesis.
- Principio de integridad: no escribir fuera del bloque.

---

## 5. Conclusión y prioridades sugeridas

1. **Prioridad alta:** alinear los contratos de datos (`ConceptMeta`, `Source`, `ResearchPlan`, `Synthesis`,
   `ValidationReport`, `WriteResult`) con el diseño (punto 2) y la spec (puntos 2–25). Actualmente los tests
   refuerzan el vocabulario de la implementación, lo que oculta la deriva.
2. **Prioridad alta:** completar la batería de checks de validación (contexto, relaciones, fuentes, actualidad,
   integridad, seguridad de archivo, pedagogía) y adoptar veredicto `approved | needs_fix | rejected` +
   `blocking_failures`.
3. **Prioridad media:** completar logging (eventos de fuentes/validación/escritura/reintentos, `run_id`, `run.jsonl`).
4. **Prioridad media:** renombrar/reorganizar fases al modelo de 11 fases del diseño o documentar explícitamente
   el agrupamiento aceptado.
5. **Prioridad baja:** mover backups a la ruta `.pipeline/<concept_id>/backup/`, persistir `meta.json` y
   `research_plan.json`, y añadir diagnóstico de calidad a los reportes.

---

## 6. Fuentes consultadas para la auditoría

- `C:\Users\DGVit\Desktop\# Especificaciónes.txt`
- `C:\Users\DGVit\Downloads\diseno-tecnico-pipeline.md`
- `C:\Users\DGVit\Proyectos\IT Career\explicacion del proyecto por capas v1.md`
- `C:\Users\DGVit\Proyectos\IT Career\explicacion del proyecto por capas v1 - pseudo codigo.md`
- `C:\Users\DGVit\Proyectos\IT Career\project_state.md`
- `C:\Users\DGVit\Proyectos\IT Career\DOCS\learnings.md`
- `C:\Users\DGVit\Proyectos\IT Career\it-concept-map\*.py`, `config.yaml`, `pyproject.toml`, `README.md`, `scripts\`
- `C:\Users\DGVit\Proyectos\IT Career\it-concept-map\tests\*.py`, `tests\config_cli.yaml`

---

*Fin del informe de auditoría. No se modificaron archivos del proyecto durante esta auditoría.*
