# IT Knowledge Map — Agent Guidelines

## Objetivo del proyecto

Vault de Obsidian con ~255 conceptos de carrera IT. Cada concepto es un `.md`
con información verificada, estructurada y conectada con vecinos del vault.

El pipeline automatiza la investigación, síntesis, validación y escritura de
cada concepto, usando NotebookLM como backend de investigación.

## Entorno

- OS: Windows 11
- Python: usar siempre el launcher `py` (nunca `python` ni `python3`)
- Terminales: PowerShell, CMD, GitBash
- Editor: VS Code
- Proyecto real: `C:\Users\DGVit\Proyectos\IT Career\`

## Estructura

```
IT Career/
├── it-concept-map/     # Pipeline (NO tocar sin orden)
├── docs/               # Documentación
├── explicaciones/      # Explicaciones por capa
├── *.txt               # Fuentes por área (NO borrar)
└── *.md                # Conceptos del vault
```

## Comandos

### Pipeline

- `py run_pipeline.py --area "AREA" --limit N` — procesar N conceptos de un área
- `py run_pipeline.py --status` — estado por fase (pending/ok/failed)
- `py run_pipeline.py --retry --failed` — reintentar conceptos fallidos
- `py eval_concept.py --all` — evaluar calidad de todos los conceptos
- `py diagnose.py --concept ID` — diagnosticar fallo de un concepto
- `pytest` — ejecutar tests

### Áreas válidas

Software Engineering, Frontend, Backend, Database / Data Analytics,
Networking / Internet, Operating Systems / Linux, AI Engineering,
UX / UI, Product Management, Project Management.

## Reglas de operación

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
- `ideas-ausentes` — ideas clave del `.txt` no aparecen en la nota
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

## Notas de arquitectura

- El adaptador de NotebookLM está aislado detrás de la interfaz `ResearchBackend`.
- Cada fase lee artefactos de la anterior y persiste los suyos en `workdir/.pipeline/<id>/`.
- Escrituras atómicas: temp + `os.replace`.
- Reintentos con backoff exponencial solo para errores transitorios.
- Circuit breaker: N fallos de red consecutivos abortan rápido.
- Limpieza de notebooks: best-effort, idempotente.

## Restricciones de NotebookLM

- Límite: 100 notebooks por cuenta (plan gratuito).
- El notebook es temporal: se borra solo después de éxito completo.
- Reconciliación de huérfanos al arrancar (ver `state.reconcile_orphan_notebooks`).
- Guardia de límite: pausar si la cuenta se acerca a 100.
