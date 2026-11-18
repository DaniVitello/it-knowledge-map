# Documentacion - indice y fuente de verdad

## Estado (canonico)
- `STATE.md` - generado desde `workdir/concepts/*/estado.json` con `utility/report_state.py`.
  Unica fuente de verdad del estado. NO editar a mano; regenerar:
  `py utility/report_state.py <workdir> docs/STATE.md`
- `DOCS/project_state.md`, `manifest.json`, `progress.json` son SNAPSHOTS historicos y
  pueden estar desactualizados (project_state.md decia "1/255" cuando el run real completo
  los 255). No usarlos como estado actual.

## Regla de drift
Ante conflicto doc vs codigo, manda el codigo. El estado se DERIVA de datos (estado.json),
no de documentacion mantenida a mano. Los READMEs y design docs son snapshots: la
implementacion puede estar ahead.

## Numeracion de capas
Conviven esquemas historicos (fases del diseno v1, letras A-L del plan de mejoras).
Para la implementacion v2 el esquema canonico es L0-L11 (ver diseno tecnico v2).
