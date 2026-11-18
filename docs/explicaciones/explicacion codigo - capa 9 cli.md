# Explicacion codigo - Capa 9: CLI

## Que es la Capa de CLI
Interfaz de linea de comandos para humanos y agentes. Comandos: run, status, list, reset, dry-run. Integracion con runner.py y todas las capas anteriores.

## Comandos
- `run [concepto] [--area] [--limit] [--force] [--dry-run]`: ejecuta el pipeline por concepto o batch.
- `status <concepto>`: muestra el estado de un concepto.
- `list [--status]`: lista conceptos filtrados por estado.
- `reset <concepto>`: reinicia el estado de un concepto.
- `dry-run [concepto] [--area] [--limit]`: simula el pipeline sin escribir.

## Opciones globales
- `--config`: ruta al config.yaml (default: config.yaml).
- `--workdir`: override del workdir.
- `--vault`: override del vault_path.

## Integracion
- runner.py: Runner, run_concept, run_batch.
- state.py: load_state, save_state.
- registry: load_concepts (para list y filtros).

## Entry point
- `kpipe = "cli:main"` en pyproject.toml [project.scripts].

## Tests
- tests/test_cli.py: 12 tests, todos pasando.
- Cubren: status sin/con estado, list vacio/filtrado, reset, run dry-run, run concepto no encontrado, main sin comando, main help, run status filter.

## Archivos
- cli.py: main, cmd_run, cmd_status, cmd_list, cmd_reset, cmd_dry_run.
- tests/test_cli.py: 12 tests.

## Resultado de tests
- 12/12 OK.
- py_compile OK.
