# Capa C — Higiene de config, tests y arranque

**Fecha:** 2026-10-29
**Estado:** ✅ Completada

## Cambios realizados

### config.yaml
- Eliminado bloque muerto `validation:` (las secciones canónicas viven en `validation.py` → `REQUIRED_SECTIONS`).
- Eliminadas claves muertas `generate_report` y `download` de `backend.notebooklm.timeouts` (no están en `NotebookLMBackend.DEFAULT_TIMEOUTS` y se ignoraban).

### tests/test_backend.py
- Eliminado test vacío `test_persist_error_razon` (sin asserts; cubierto por `test_fallo_marca_failed_con_razon`).

### Correcciones adicionales (transiciones de estado)
- `validation.py`: eliminada transición redundante `VALIDATED -> VALIDATED` (early); el estado se transiciona al final según resultado. En el branch `force`, se usa asignación directa `st.status = SYNTHESIZED` en vez de `transition_to` (que era inválida desde VALIDATED).
- `synthesis.py`: eliminada transición redundante `SYNTHESIZED -> SYNTHESIZED` final. En el branch `force`, se usa asignación directa `st.status = RESEARCHED`.
- `tests/test_research.py`: actualizados `test_retry_desde_failed` (notebook_id ahora persiste, `is not None`) y `test_latency_y_llamadas` (ya no se llama `delete` tras `delete_notebook_after=False`).

### Dependencias instaladas en .venv
- `pytest>=8.0` (9.2.0) y `notebooklm-py`.

## Verificación
- `py -m py_compile` sobre todos los módulos: OK.
- `pytest`: 108 passed, 37 warnings.

## Siguiente capa
- A (contratos de datos alineados al diseño) — foundational.
