# Plan de Sesiones - IT Career Concept Map (v1)

> Generado: 2026-10-30
> Objetivo: completar los 255 conceptos del vault con NotebookLM
> Principio: una capa = una sesión nueva. Sin context rot.

---

## Fase 0: Verificación de estado real (Sesión 0)

**Duración:** 1 sesión
**Objetivo:** Saber exactamente qué está hecho y qué no.

### Tareas
1. Leer `project_state.md` (sección progreso)
2. Para cada capa A-L, verificar si el código refleja lo que el plan pide
3. Ejecutar `py -m pytest` y anotar tests pasando/fallando
4. Verificar que `run_pipeline.py` funciona para 1 concepto
5. Documentar resultados en `project_state.md` sección "Verificación real"

### Criterio de salida
- Tabla actualizada: capa | estado real | tests | notas
- Saber qué capas necesitan re-ejecución

---

## Fase 1: Corrección de capas A-L (Sesiones 1-12)

**Duración:** 1 sesión por capa (12 sesiones)
**Principio:** una capa, una sesión nueva. Sin arrastrar historial.

### Orden de ejecución (según dependencias del plan)

| Sesión | Capa | Depende de | Archivos que toca | Tests esperados |
|--------|------|------------|-------------------|-----------------|
| S1 | A - Contratos | - | models.py, state.py, tests | Round-trip JSON |
| S2 | B - Integridad | A | runner.py, synthesis.py, validation.py | 4 bugs en rojo→verde |
| S3 | C - Higiene config | Independiente | config.yaml, runner.py, pilot.py, runner.py (asyncio) | Pacing medible |
| S4 | D - areas.json | A | areas/, registry.py, config | Dominios reales |
| S5 | E - Investigación | A, C, D | research.py, prompts | Seeds subidas, research_plan.json |
| S6 | F - Evaluación fuentes | A, E | synthesis.py, backend.py | Source con evaluation |
| S7 | G - Notebook lifecycle | A | runner.py, state.py | Delete tras verified |
| S8 | H - Validación determinista | A, E, F, C | validation.py | 4 checks bloqueantes |
| S9 | I - Semántica + bucle + DoD | H, G | validation.py, runner.py | needs_fix/rejected |
| S10 | J - Orquestador | B, I | runner.py, cli.py | Kill-and-resume |
| S11 | K - Trazabilidad | Pipeline estable | log.py, writer.py, runner.py | run.jsonl, pie de traza |
| S12 | L - Idempotencia + piloto + limpieza | Todo | runner.py, cli.py, README | GO/NO-GO |

### Reglas por sesión
1. Abrir sesión nueva de Hermes
2. Leer `project_state.md` + skill `opencode`
3. Leer SOLO la sección de la capa en `plan de mejoras v1.md`
4. Leer SOLO los archivos que toca la capa
5. Implementar cambios
6. Ejecutar tests de la capa
7. Actualizar `project_state.md` sección progreso
8. Commit + push a GitHub
9. Cerrar sesión

### Qué NO hacer en cada sesión
- No leer archivos de otras capas
- No acumular contexto de capas anteriores
- No modificar archivos que no toca la capa
- No ejecutar el pipeline completo (solo tests de la capa)

---

## Fase 2: Preparación MVP (Sesión 13)

**Duración:** 1 sesión
**Objetivo:** Verificar que todas las capas están aplicadas y el pipeline funciona end-to-end.

### Tareas
1. Ejecutar suite completa de tests (`py -m pytest`)
2. Verificar NotebookLM auth (cookies válidas)
3. Ejecutar `run_pipeline.py` para 1 concepto (Programming Fundamentals ya hecho, elegir otro)
4. Verificar que el concepto se escribió correctamente en el vault
5. Verificar que el notebook se eliminó post-write
6. Documentar resultado

### Criterio de salida
- Suite completa verde
- 1 concepto procesado end-to-end con NotebookLM real
- Sin errores de auth o conexión

---

## Fase 3: Piloto (Sesión 14)

**Duración:** 1 sesión
**Objetivo:** Procesar ~8 conceptos variados y validar GO/NO-GO.

### Selección de conceptos (deliberadamente variados)
- 2 estables (conceptos bien definidos, con fuentes claras)
- 2 dinámicos (conceptos que cambian rápido, versiones, etc.)
- 1 con poca info (concepto nicho, pocas fuentes)
- 1 de otra área (no Software Engineering)
- 1 con contenido manual existente (para probar idempotencia)
- 1 con seed_urls (para probar subida de fuentes)

### Criterio de salida (binario)
- [ ] Vault intacto (no se destruyó contenido manual)
- [ ] Idempotencia: matar y reanudar funciona
- [ ] Sin URLs fuera de fuentes
- [ ] Revisión humana configurable
- [ ] Reporte de grafo del mapa (conceptos aislados/conexiones asimétricas)

### Si GO → Fase 4
### Si NO-GO → corregir la capa que falló, re-pilot

---

## Fase 4: Batch por área (Sesiones 15-24)

**Duración:** 1 sesión por área (10 áreas, pero 1 ya tiene 1 concepto)
**Objetivo:** Procesar todos los conceptos de cada área.

### Orden sugerido (por tamaño estimado)
1. Software Engineering (30 conceptos) - ya tiene 1
2. Frontend (25)
3. Backend / Data / etc. (resto)

### Por sesión
1. Ejecutar `cli.py run --area <area>`
2. Monitorear progreso (events.jsonl)
3. Manejar fallos (needs_review, rejected)
4. Revisar conceptos procesados (muestra)
5. Actualizar project_state.md
6. Commit + push

### Criterio de salida por área
- Todos los conceptos del área procesados (completed o needs_review documentado)
- Sin errores silenciosos
- Reporte batch con causas de fallo

---

## Fase 5: Auditoría final (Sesión 25)

**Duración:** 1 sesión
**Objetivo:** Verificar que los 255 conceptos están completos y correctos.

### Tareas
1. Ejecutar `cli.py status` (todos completed o needs_review)
2. Verificar grafo del mapa (sin conceptos aislados)
3. Verificar trazabilidad (cada concepto tiene run_id + prompt_version + fuentes)
4. Revisar 5 conceptos aleatorios por área (calidad)
5. Documentar resultado final
6. Actualizar README con métricas reales

### Criterio de salida
- 255 conceptos procesados
- 0 errores silenciosos
- README actualizado con métricas reales

---

## Resumen de sesiones

| Fase | Sesiones | Duración estimada | Objetivo |
|------|----------|-------------------|----------|
| Fase 0 | 1 | 1 sesión | Verificación real |
| Fase 1 | 12 | 12 sesiones | Corrección A-L |
| Fase 2 | 1 | 1 sesión | MVP end-to-end |
| Fase 3 | 1 | 1 sesión | Piloto GO/NO-GO |
| Fase 4 | 10 | 10 sesiones | Batch por área |
| Fase 5 | 1 | 1 sesión | Auditoría final |
| **Total** | **26** | **26 sesiones** | **255 conceptos completos** |

---

## Reglas generales (todas las sesiones)

1. **Una sesión = una tarea.** No mezclar capas ni áreas.
2. **Leer project_state.md al inicio.** Siempre.
3. **Cargar skill opencode al inicio.** Siempre.
4. **Verificar conexión antes de operar.** Quick verification del skill.
5. **Commit + push al final de cada sesión.** Sin excepciones.
6. **Actualizar project_state.md al final.** Secciones 2 y 6.
7. **Cerrar la sesión al terminar la tarea.** No acumular contexto.
8. **Si algo falla, documentar y cerrar.** No intentar arreglar en la misma sesión si requiere otra capa.

## Riesgos conocidos

| Riesgo | Mitigación |
|--------|------------|
| Context rot | Sesiones cortas, una tarea por sesión |
| Free tier agotado | Usar Groq como provider (configurado) |
| NotebookLM auth expira | Verificar antes de cada batch |
| Edición concurrente del vault | Hash de protección en writer |
| Tests falsos positivos | Verificar con código real, no solo tests |
| Password/port cambian | Quick verification en cada sesión |

## Lo que NO hacer

- No ejecutar múltiples capas en una sesión
- No acumular contexto de sesiones anteriores
- No modificar archivos que no toca la capa/área actual
- No pushear sin commit message descriptivo
- No ignorar fallos (documentar y cerrar)
