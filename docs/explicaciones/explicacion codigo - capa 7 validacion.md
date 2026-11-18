# Explicacion codigo - Capa 7: Validacion

## Que es la Capa de Validacion
Valida la sintesis contra las reglas de la spec: evidencia, estructura, formato, cross-links, longitud, prohibiciones (copy-paste plano, URLs inventadas). Produce ValidationReport con pass/fail + issues + warnings + score. Transiciona estado a validated o failed. Idempotente y recuperable.

## ValidationPhase
Clase que orquesta la validacion. Recibe config. Metodo run(concept, force=False). Incluye:
- _check_sections: verifica que todas las secciones requeridas esten presentes y con contenido suficiente.
- _check_total_length: verifica longitud minima y maxima.
- _check_review_questions: verifica al menos 3 preguntas de repaso (con "?").
- _check_structure: verifica encabezados ## en orden.
- _check_invented_urls: heuristica de URLs (advertencia, no bloqueante).
- _check_copy_paste: heuristica de copy-paste (advertencia).
- _check_cross_links: verifica wikilinks contra connections del concepto.
- validate(): funcion pura que devuelve (is_valid, issues, warnings).
- Idempotencia: si ya esta validated y hay cache, no re-valida.
- Transicion a VALIDATED (directa) o FAILED con failed_reason "validation".
- Persistencia de validation.json (concept_id, is_valid, issues, warnings, score, checked_at).

## Funcion de conveniencia
run_validation(concept, cfg, force=False) crea la fase y ejecuta.

## Integracion con state.py y synthesis.py
- state.py: load_state/save_state, transicion a VALIDATED o FAILED.
- synthesis.py: lee synthesis.json del .pipeline/<id>/.

## Manejo de errores
- Si la sintesis esta corrupta o faltan secciones -> issues bloqueantes -> is_valid=False -> estado FAILED.
- Si la transicion es invalida (ej: desde pending sin force) -> InvalidTransitionError.

## Idempotencia
- Si state es VALIDATED/WRITTEN/COMPLETED y validation.json existe y no force → retorna resultado cacheado.
- force=True: re-ejecuta y sobrescribe validation.json.

## Tests
- tests/test_validation.py: 12 tests, todos pasando.
- Cubren: pass con contenido completo, fail seccion faltante, fail seccion corta, fail muy corto, fail pocas preguntas, persistencia de artefactos, idempotencia, force, fallo marca failed, transicion invalida, run_validation, protocolo de estados.

## Archivos
- validation.py: ValidationPhase, ValidationPhaseResult, validate(), run_validation, REQUIRED_SECTIONS, helpers de chequeo.
- tests/test_validation.py: 12 tests.

## Resultado de tests
- 12/12 OK.
- py_compile OK.
