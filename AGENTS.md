# IT Knowledge Map — Agent Guidelines

## Objetivo del proyecto

Vault de Obsidian con ~255 conceptos de carrera IT. Cada concepto es un .md
con información verificada, estructurada y conectada con vecinos del vault.

## Comandos

### Pipeline
- `python run_pipeline.py --area "AREA" --limit N` — procesar N conceptos de un área
- `python run_pipeline.py --status` — estado por fase (pending/ok/failed)
- `python run_pipeline.py --retry --failed` — reintentar conceptos fallidos
- `python eval_concept.py --all` — evaluar calidad de todos los conceptos
- `python diagnose.py --concept ID` — diagnosticar fallo de un concepto
- `pytest` — 116 tests

### Áreas válidas
Software Engineering, Frontend, Backend, Database / Data Analytics,
Networking / Internet, Operating Systems / Linux, AI Engineering,
UX / UI, Product Management, Project Management

## Estructura

```
IT Career/
├── it-concept-map/     # Pipeline (NO tocar sin orden)
├── docs/               # Documentación
├── explicaciones/      # Explicaciones por capa
├── *.txt               # Fuentes por área (NO borrar)
└── *.md                # Conceptos del vault
```

## Reglas

1. **No borrar ni modificar archivos sin orden explícita.**
2. **Git push:** dry-run primero o push manual. Nunca push directo sin confirmación.
3. **No matar procesos ni limpiar directorios** sin verificar estado primero. Usar `status` y `retry`.
4. **No modificar código del pipeline** sin orden. Solo ejecutar.
5. **Cada lote en una rama de git + commit local** como punto de retorno.
6. **Push manual** — nunca automático.

## Definición de "concepto terminado"

Un concepto está terminado cuando:
- [ ] Validación OK (score ≥ 70)
- [ ] Fuentes citadas (cada afirmación tiene id de fuente válido)
- [ ] Aprobación de muestra del lote (3 notas por lote revisadas a mano)
- [ ] Commit local del lote

## Taxonomía de fallas

Etiquetar conceptos malos con:
- `generico` — contenido genérico, no específico del concepto
- `alucinado` — afirma cosas no presentes en las fuentes
- `no-fuentes` — no usa las fuentes de research
- `ideas-ausentes` — ideas clave del .txt no aparecen en la nota
- `relaciones-vagas` — wikilinks o relaciones sin justificación
- `largo-inadecuado` — muy corto o muy largo

## Workflow del pipeline

```
concept_id + área
  ↓
[Research] → work/<id>/research.json (fuentes de NotebookLM)
  ↓
[Synthesis] → work/<id>/draft.json (contenido generado por LLM)
  ↓
[Validation] → work/<id>/validation.json (score + issues)
  ↓ (si falla → vuelve a Synthesis con issues)
[Writer] → vault/<concepto>.md (archivo final)
  ↓
Hermes verifica → siguiente concepto
```

## Reglas de orquestación

- Hermes NO opera el batch en vivo. Solo llama `status` y `run`.
- El runner es la única forma de ejecutar el pipeline.
- Si un concepto falla, usar `retry --failed`, no re-lanzar todo.
- Si la cuota de Groq se agota, el runner corta automáticamente y guarda estado.
- Al día siguiente, `run --resume` continúa desde donde se quedó.
- No improvisar: si no hay criterio claro, parar y preguntar.

## Calidad

- Golden set: 8-10 conceptos de áreas distintas (fáciles y difíciles)
- Iterar prompt sobre golden set antes de escalar
- 4 ejes de puntuación (1-5): fidelidad a fuentes, utilidad, conexiones, estructura
- No escalar hasta que el golden set pase el umbral (≥4 en todos los ejes)
- LLM judge solo sobre muestras (3 por lote), no sobre los 255
- Pasada final de enlaces entre conceptos (determinista, por alias)

## Estado

- Manifest: workdir/manifest.json (a crear)
- 61 conceptos legacy (prompt v1, calidad desconocida)
- 194 pendientes
- 116 tests pasando
