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
├── it-concept-map/     # Pipeline
│   ├── main/           # Core (backend, cli, research, runner, state, synthesis, validation, writer, models, registry, areas, llm_groq, log)
│   ├── exe/            # Scripts de ejecución (run_pipeline, retry_failed, pilot, eval_concept, run_*)
│   ├── test/           # Tests
│   ├── utility/        # Scripts auxiliares (review_concepts, mark_issues_failed, diagnose, monitor, audit, etc.)
│   ├── areas/          # Config de áreas (YAML)
│   ├── workdir/        # Estado y artefactos (gitignored)
│   └── config.yaml     # Config (gitignored, con secrets)
├── IT-Mind-Map/        # Vault de Obsidian (conceptos generados)
├── data/archive/       # Fuentes .txt por área (obsoletas, ya generaron el vault)
├── docs/               # Documentación (archive/, explicaciones/, fix-capas/)
├── scripts/archive/    # Scripts one-off históricos
└── AGENTS.md           # Este archivo
```

## Comandos

### Pipeline

- `py exe\run_pipeline.py --area "AREA" --limit N` — procesar N conceptos de un área
- `py exe\run_pipeline.py --concept "ID" --force` — re-procesar un concepto específico
- `py exe\retry_failed.py` — reintentar conceptos en estado failed
- `py main\cli.py status` — estado en tiempo real de todos los conceptos
- `py main\cli.py status <id>` — detalle de un concepto
- `py utility\review_concepts.py --vault "IT-Mind-Map"` — revisar calidad de todos los conceptos
- `py utility\mark_issues_failed.py` — marcar conceptos con issues como failed
- `py utility\diagnose.py --concept ID` — diagnosticar fallo de un concepto
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

## Restricciones

- No tocar `.venv/`, `node_modules/`, `.git/`.
- No modificar `config.yaml` (contiene secrets). Usar `config.example.yaml` para compartir.
- No borrar archivos del vault (`IT-Mind-Map/`) sin orden explícita.
- No borrar fuentes (`data/archive/*.txt`) sin orden explícita.

## Convenciones de código

- Python: usar `py`, nunca `python` ni `python3`.
- Encoding: UTF-8 sin BOM.
- Imports: relativos dentro de `main/`, `sys.path` insert en `exe/`, `test/`, `utility/`.
- Commits: en español, formato `tipo: descripción` (feat, fix, refactor, docs).
- No modificar dependencias en `.venv/` ni `node_modules/`.

## Recovery

- Si un concepto falla: `py utility\diagnose.py --concept ID`
- Si hay conceptos failed: `py exe\retry_failed.py`
- Si el pipeline se corta: el estado se guarda en `workdir/concepts/<id>/estado.json`. Re-ejecutar con `--force`.
- Si la cuota de Groq se agota: el runner corta automáticamente y guarda estado. Reintentar después de 10-15 min.