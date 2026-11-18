# IT Knowledge Map v2 — `ikm/`

Implementacion por capas (L0–L11) del diseño técnico v2. El vault (`IT-Mind-Map/`)
es la fuente de contenido y **solo lectura**; v1 (`it-concept-map/`) queda legacy.

## Estructura

```
ikm/
  contracts/    L0 — esquemas Pydantic -> JSON Schema -> tipos TypeScript
  content/      L1–L4 — pipeline de contenido (CLI `ikm`)
  api/          L5–L9 — backend FastAPI
  web/          L10 — frontend
  eval/         L11 — evaluacion
  fixtures/     vault sintetico
  releases/     salida del pipeline (gitignored, solo contenido aprobado)
  tests/        tests de las capas
  docs/decisions/  registros de decision
```

## Estado

- **L0 (contratos):** implementado y verificado.
  - Modelos Pydantic del release (`release.py`) y del servicio (`service.py`).
  - Identificadores estables (`ids.py`), feature flags y limites (`config.py`),
    taxonomia de errores (`errors.py`), utilidades (`utils.py`).
  - Generacion JSON Schema -> TypeScript (`generate.py`) y validacion (`validate.py`).
  - 22 tests en `tests/test_l0_contracts.py` (round-trip, ids, config, schemas).
- **L1+:** pendiente. Ver `PROJECT_STATE_v2.md`.

## Comandos

```bash
py -m pytest ikm/tests -q          # tests
py -c "from ikm.contracts import generate; print(generate.regenerar('ikm/contracts/generated'))"
```

## Regla de oro

El modelo no decide sobre estructuras del sistema; lo documentado, lo derivado,
lo general y lo inferido se distinguen **por codigo**. Degradar antes que inventar.
