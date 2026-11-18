# Explicación del código — Capa 2: state + persistencia

> Documento educativo. Explica, con palabras, qué se implementó en la **Capa 2 de implementación** del proyecto `it-concept-map`, cómo se tradujo el pseudo-código de la Capa 3 del diseño técnico (pipeline de estados) a código real, y por qué se tomó cada decisión. No copia bloques de código: solo referencia módulos y líneas clave.

Proyecto: `C:\Users\DGVit\Proyectos\IT Career\it-concept-map\`
Vault de origen: `C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map\` (notas `.md` con bloque `<!-- ai:start --> ... <!-- ai:end -->`)

---

## 1. Qué es la Capa 2 y por qué va después del registry

La Capa 2 de implementación es la **máquina de estados + persistencia** del pipeline. En el pseudo-código esto corresponde a la **Capa 3 (Pipeline de estados)**, porque la Capa 1 de implementación ya fusionó las Capas 1 y 2 del diseño (modelo de datos + lectura del vault). Es decir: el pseudo-código dice "Capa 3", pero en este repo se llama "Capa 2" porque el numbering se reacomodó al fusionar las dos primeras.

La idea central: una vez que sabemos leer conceptos del vault (Capa 1, `registry.py`), necesitamos saber **en qué punto del pipeline está cada concepto** y poder **reanudar** si el proceso se corta a mitad. Sin estado no hay recuperación ni idempotencia: cada corrida empezaría de cero y no sabría si un concepto ya se investigó, sintetizó o escribió.

`state.py` es el único archivo nuevo de esta capa. No toca el vault ni la red: solo lee/escribe en el `workdir`. Eso mantiene la separación de responsabilidades: el registry lee el vault, el state persiste el progreso, y las capas futuras (backend, investigación, síntesis, validación, writer) harán el trabajo pesado.

---

## 2. Archivos creados y afectados

Todos viven en `it-concept-map\`:

| Archivo | Rol |
|---|---|
| `state.py` | Máquina de estados (`ConceptStatus`, `VALID_TRANSITIONS`), dataclass `ConceptState`, persistencia (JSON por concepto o SQLite), reanudación, reconciliación de notebooks huérfanos y reintentos con backoff. Nuevo (812 líneas). |
| `README.md` | Actualizado: ya lista `state.py` en la estructura y dice "Capa 2 (state + persistencia) implementada". |
| `workdir\` | No se crea todavía; se materializa en runtime al primer `save_state` (hoy no existe en disco). |

Nota práctica: `pyproject.toml` todavía declara solo `models` y `registry` en `py-modules`. `state.py` se importa como módulo suelto; no es bloqueante para usarlo, pero conviene tenerlo en cuenta si se arma un paquete instalable.

---

## 3. `state.py` — la máquina y la persistencia

Archivo: `it-concept-map\state.py` (812 líneas). Es el corazón de esta capa.

### 3.1 Versión de esquema

Línea 27: `SCHEMA_VERSION = "1.0.0"`. `ConceptState.schema_version` (línea 213) lo lleva por defecto. La idea es la misma que en `models.py`: los artefactos persistidos (`estado.json`, filas de SQLite) quedan versionados, y si mañana cambia la estructura se pueden invalidar caches viejos comparando la versión.

### 3.2 Estados del ciclo de vida

Líneas 34-46: `ConceptStatus` (un `str, Enum`) con 9 valores:

- `pending`: en cola, sin procesar.
- `researching`: buscando/evaluando fuentes.
- `researched`: investigación terminada.
- `synthesized`: síntesis generada.
- `validated`: síntesis validada.
- `written`: escrito en el vault.
- `completed`: terminal exitoso.
- `failed`: terminal por error (reintentable).
- `needs_review`: terminal que requiere acción humana.

La granularidad es deliberada: en lugar de un solo estado "synthesizing", hay un estado "synthesized" que marca que esa fase ya terminó. Así el runner sabe exactamente desde qué fase reanudar sin repetir trabajo. Es una diferencia con el pseudo-código, que lista 8 estados (`pending, researching, synthesizing, validating, writing, done, failed, blocked`). Acá se renombran `done → completed` y `blocked → needs_review`, y se agregan los estados "terminado por fase" (`researched, synthesized, validated, written`).

`models.py` conserva el enum del pseudo-código (`PENDING…BLOCKED/DONE`) como contrato adelantado; `state.py` es la versión operativa que usará el runner. La intención es unificarlos cuando se implemente el runner; por ahora `state.py` es la fuente operativa.

### 3.3 Aliases de compatibilidad

Líneas 49-52: `StateStatus`, `PipelineStatus`, `ConceptStateStatus` y `Status` son alias de `ConceptStatus`. Esto permite que callers o tests que usen distintos nombres no se rompan, sin duplicar la definición.

### 3.4 Estados terminales

Líneas 54-58: `TERMINAL_STATES = {completed, failed, needs_review}`. `is_terminal()` (líneas 140-141) consulta este set. Un estado terminal no se reejecuta automáticamente (salvo `--force` o reintento explícito). Esto implementa "done es terminal: nunca se reejecuta".

### 3.5 Transiciones válidas

Líneas 60-90: `VALID_TRANSITIONS` es un diccionario que define, para cada estado, a cuáles se puede pasar. La idea es linealidad con salidas de error/bloqueo:

- `pending → researching`
- `researching → researched | failed`
- `researched → synthesized | failed`
- `synthesized → validated | failed | needs_review`
- `validated → written | failed | needs_review`
- `written → completed | failed`
- `completed →` (sin salidas)
- `failed →` cualquiera de las fases (para reintentar)
- `needs_review →` researching | synthesized | validated | written | completed

Esto implementa la regla del pseudo-código: "un reintento vuelve al estado que falló (no reinicia desde pending), conservando el checkpoint previo". `failed` y `needs_review` son terminales operativos que permiten volver a una fase concreta.

### 3.6 Normalización y validación de transiciones

- `_to_status()` (líneas 97-118): acepta un `ConceptStatus`, un `Enum`, un string, o variantes con guiones/espacios y mayúsculas mezcladas. Devuelve `None` si no reconoce el valor. Por qué: el estado llega desde JSON/config con formatos distintos; normalizar evita fallos por formato.
- `can_transition()` (líneas 121-127): dice si una transición está permitida.
- `validate_transition()` (líneas 130-137): lanza `InvalidTransitionError` si no lo está.
- `InvalidTransitionError` (líneas 93-94): subclase de `ValueError`.

El pseudo-código exige "no se salta ninguna fase"; estas funciones son el guardián: cualquier intento de salto se rechaza explícitamente en lugar de corromper el progreso.

### 3.7 `ConceptState` — el registro persistido

Líneas 199-214: dataclass con los campos:

- `concept_id`: identidad del concepto.
- `status`: estado actual.
- `last_good_state`: último estado válido antes de fallar (para reanudar bien).
- `checkpoint`: nombre de la fase donde quedó (ej. `"researching"`).
- `phase_data`: datos de la fase (coverage, paths de artefactos, etc.) para no repetir trabajo.
- `error`: mensaje de error si falló.
- `retries`: contador de reintentos.
- `created_at` / `updated_at` / `timestamps`: auditoría.
- `schema_version`.

`__post_init__` (líneas 215-231) sincroniza `created_at`/`updated_at` con el diccionario `timestamps` en ambas direcciones y normaliza tipos. Por qué: permite crear un `ConceptState` con cualquiera de las dos formas (campos sueltos o dentro de `timestamps`) sin que queden inconsistentes. Es la misma idea de "una sola fuente de verdad" pero tolerando formatos de entrada distintos.

`transition_to()` (líneas 232-268) es el método que aplica una transición validada: valida, actualiza `last_good_state` (salvo que ya estuviera en `failed`/`needs_review`), setea `status`, `checkpoint`, `phase_data`, `error` (o lo limpia), y refresca timestamps. Devuelve `self` para encadenar. Implementa "persistir checkpoint y status antes de avanzar".

### 3.8 Resolución de workdir y backend

- `_cfg()` (líneas 153-167): acceso seguro a config, acepta dict u objeto, con fallback. Igual que en `registry.py`.
- `resolve_workdir()` (líneas 276-285): prioridad arg → config (`workdir` o `workdir_path`) → `cwd/workdir`.
- `resolve_backend()` (líneas 288-299): prioridad arg → config (`state_backend`, `state.backend`, `backend.state`) → `"json"`.
- `concept_dir()` (líneas 302-303): `workdir/concepts/<id>`.

Por qué: permite usar JSON o SQLite sin cambiar las llamadas, y aceptar config con distintas formas de anidar las claves. El backend por defecto es JSON porque es el más simple y debuggeable.

### 3.9 Serialización

`to_dict()` (líneas 170-192): convierte `Path`, `Enum`, listas, tuplas, dicts y dataclasses a valores serializables. Se usa en `save_state` para JSON y SQLite. Por qué centralizar: evita que cada capa escriba su propia serialización y reduce el riesgo de olvidar convertir un `Path` o un `Enum`.

### 3.10 Persistencia JSON

- `_normalize_save_args()` (líneas 329-365): acepta múltiples firmas: `save_state(state, ...)`, `save_state(concept_id, state, ...)`, `save_state(state, workdir, ...)`, más kwargs (`workdir`, `workdir_path`, `config`, `backend`). Por qué tanta flexibilidad: los callers (runner, tests, scripts) pueden tener convenciones distintas; normalizar en un solo lugar evita errores de orden de argumentos.
- `save_state()` (líneas 368-421): asegura timestamps, y si el backend es JSON escribe `workdir/concepts/<id>/estado.json` con escritura atómica: primero un archivo temporal `.estado.json.tmp`, luego `replace` sobre el destino. Por qué atómica: si el proceso muere a mitad de escritura, el `estado.json` anterior sigue intacto; no queda un JSON corrupto.
- `load_state()` (líneas 466-499): devuelve `ConceptState` o `None` si no existe o está corrupto/ilegible. No lanza: el runner decide qué hacer (marcar como bloqueado, por ejemplo).
- `load_all_states()` (líneas 502-535): escanea `concepts/*/estado.json` (o la tabla SQLite) y devuelve un dict `{concept_id: ConceptState}`.
- `_normalize_load_args()` (líneas 424-463): detecta si un argumento posicional es un directorio existente para ordenar correctamente `workdir` y `concept_id`. Misma filosofía de flexibilidad.

### 3.11 Persistencia SQLite (alternativa)

Dentro de `save_state`, `load_state` y `load_all_states`, si el backend es `sqlite`/`db`/`state.sqlite`:

- Se crea la tabla `concept_state (concept_id TEXT PRIMARY KEY, data TEXT NOT NULL, updated_at TEXT)`.
- `save_state` hace un upsert (`INSERT ... ON CONFLICT DO UPDATE`).
- `load_state` lee la fila y la deserializa.
- `load_all_states` recorre todas las filas.

Por qué ofrecer SQLite: una sola DB para consultar el estado global del lote es más cómodo que abrir N archivos JSON. Como el contenido de cada fila es el mismo JSON, se puede migrar de uno a otro sin pérdida. El pseudo-código menciona `estado.json` como fuente de verdad; acá se mantiene JSON como default y SQLite como opción.

### 3.12 Reanudación desde checkpoint

`resume_from_checkpoint()` (líneas 538-575):

- Si recibe un `str`, carga el estado o crea uno nuevo en `pending`.
- Si el estado es `completed`, lo devuelve sin cambios (no reejecuta).
- Si se indica `phase`, la usa como checkpoint; si no hay checkpoint, lo deriva del status actual.
- Persiste y devuelve el estado.

Implementa la idempotencia del pseudo-código: "si status es terminal → no se reejecuta; si no → reanudar desde el último checkpoint persistido, no desde cero".

### 3.13 Reconciliación de notebooks huérfanos

- `reconcile_orphan_notebooks()` (líneas 577-650): mantiene un registro simple `workdir/notebooks.json` con la forma `{notebook_id: concept_id}`. Un notebook es huérfano si:
  - no aparece en `phase_data` de ningún estado, o
  - su concepto está ausente o en estado `failed`/`needs_review`.
  Si `delete=True`, los huérfanos se quitan del registro. Devuelve la lista de ids huérfanos.
- `register_notebook()` (líneas 653-677): registra un notebook en el índice.

Por qué: el backend (Capa 4, pendiente) creará notebooks en NotebookLM. Si una fase falla a mitad, pueden quedar notebooks sin dueño. Esta utilidad permite detectarlos y limpiarlos. El pseudo-código lo menciona como "limpieza best-effort ante fallo" y "notebooks huérfanos se reportan al final del lote".

### 3.14 Reintentos con backoff exponencial

- `exponential_backoff_seconds()` (líneas 685-698): genera la lista de delays `base * factor^i`, con tope opcional (`cap`).
- `retry_with_backoff()` (líneas 701-738): ejecuta `func` hasta `max_retries` intentos; ante cualquier `Exception`, llama `on_retry`, duerme el delay correspondiente (reutilizando el último si se agotan), y al final lanza la última excepción. Si `max_retries < 1` lanza `ValueError`.
- `execute_phase_with_retry()` (líneas 741-758): wrapper conveniente que llama `phase_fn(concept_id)`.
- `with_retry()` (líneas 761-780): decorador equivalente.

Esto implementa "max 3 intentos, backoff 2/4/8s". La clasificación de qué errores son reintentables (red/backend) vs no reintentables (auth, markers, validación) la hará el runner cuando se implemente; `state.py` solo provee la mecánica genérica, que es lo correcto para no mezclar responsabilidades.

---

## 4. Cómo se conecta con el pseudo-código

El pseudo-código define 11 capas; la Capa 2 de implementación cubre la **Capa 3 (Pipeline de estados)** del diseño:

| Pseudo-código (Capa 3) | Implementación |
|---|---|
| Estados del pipeline (8) | `ConceptStatus` (state.py, líneas 34-46) con 9 granulares. |
| Transiciones lineales | `VALID_TRANSITIONS` (60-90) + `validate_transition()` (130-137). |
| Estados terminales (done/failed/blocked) | `TERMINAL_STATES` (54-58) + `is_terminal()` (140-141). |
| Idempotencia y resume desde checkpoint | `resume_from_checkpoint()` (538-575) + `load_state()` (466-499). |
| estado.json atómico por concepto | `save_state()` JSON (368-421) con tmp + `replace`. |
| Reintentos max 3 con backoff | `retry_with_backoff()` (701-738) + `exponential_backoff_seconds()` (685-698). |
| Persistir failed → error, fase_fallida, timestamp | `ConceptState.error` + `transition_to()` (232-268) + `timestamps`. |
| blocked → blocker, detalle, responsable | Hoy se modela como `needs_review` + `error`; el pseudo-código lo detalla más (pendiente de enriquecer cuando se implemente el runner). |
| Cola FIFO serial con backoff | No implementado aún (será Capa 9, runner); `state.py` provee las primitivas. |
| estado.json como única fuente de verdad del progreso | `load_state`/`save_state`/`load_all_states` (466-535). |

Lo que **no** se implementó todavía (y está pendiente) son las Capas 4-11 del pseudo-código: backend, writer, investigación, síntesis, validación, orquestador, CLI, piloto. El README lo deja explícito.

---

## 5. Decisiones de diseño y por qué

1. **Granularidad de estados por fase.** En lugar de un solo estado "synthesizing", hay `synthesized` (y análogos) que marcan que la fase terminó. Costo: más valores en el enum. Beneficio: el runner sabe exactamente desde dónde reanudar sin repetir trabajo ni adivinar.

2. **Dos enums conviviendo (models.py vs state.py).** `models.py` conserva el enum del pseudo-código como contrato adelantado; `state.py` define el enum operativo. Costo: posible drift. Beneficio: los contratos de las capas futuras ya existen, y la capa operativa puede evolucionar sin romperlos. Se unificarán al implementar el runner.

3. **JSON por concepto por defecto, SQLite opcional.** Costo: dos caminos de código. Beneficio: JSON es simple, debuggeable con cualquier editor y coincide con "estado.json" del pseudo-código; SQLite queda para consultar el lote completo cuando haga falta.

4. **Escritura atómica (tmp + replace).** Costo: un archivo temporal extra. Beneficio: nunca queda un `estado.json` a medias si el proceso muere; la recuperación siempre parte de un estado válido.

5. **API flexible con normalizadores.** `_normalize_save_args` y `_normalize_load_args` aceptan varias firmas. Costo: más código de plumbing. Beneficio: los callers no se acoplan a un orden rígido de argumentos, y se evitan bugs silenciosos por orden invertido (especialmente `workdir` vs `concept_id`).

6. **`last_good_state`.** Se guarda el último estado válido antes de fallar. Costo: un campo más. Beneficio: al reintentar se puede volver al punto justo anterior al fallo en lugar de reiniciar.

7. **Reconciliación de notebooks como registro simple.** `notebooks.json` es un dict plano. Costo: no es una DB robusta. Beneficio: suficiente para detectar huérfanos en esta etapa; se puede reemplazar por una tabla cuando exista el backend real.

8. **Reintentos genéricos, sin clasificar errores.** `state.py` no decide qué es reintentable; solo ejecuta y reintenta. Costo: la clasificación queda para el runner. Beneficio: separación de responsabilidades; `state.py` no conoce backend ni writer.

9. **Aliases de nombres (`StateStatus`, etc.).** Costo: exports extra. Beneficio: compatibilidad con callers/tests que usen distintas convenciones sin duplicar lógica.

10. **No tocar vault ni red.** `state.py` solo escribe en `workdir`. Costo: ninguno. Beneficio: una capa de progreso no puede corromper el vault por accidente; respeta el principio de mínimo privilegio del pseudo-código.

---

## 6. Referencias rápidas de líneas clave

`state.py`:

- `SCHEMA_VERSION` → línea 27.
- `ConceptStatus` → líneas 34-46.
- Aliases → líneas 49-52.
- `TERMINAL_STATES` → líneas 54-58.
- `VALID_TRANSITIONS` → líneas 60-90.
- `InvalidTransitionError` → líneas 93-94.
- `_to_status` → líneas 97-118.
- `can_transition` → líneas 121-127.
- `validate_transition` → líneas 130-137.
- `is_terminal` → líneas 140-141.
- `now_iso` → líneas 149-150.
- `_cfg` → líneas 153-167.
- `to_dict` → líneas 170-192.
- `ConceptState` → líneas 199-214.
- `__post_init__` → líneas 215-231.
- `transition_to` → líneas 232-268.
- `resolve_workdir` → líneas 276-285.
- `resolve_backend` → líneas 288-299.
- `concept_dir` → líneas 302-303.
- `_from_dict` → líneas 306-326.
- `_normalize_save_args` → líneas 329-365.
- `save_state` → líneas 368-421.
- `_normalize_load_args` → líneas 424-463.
- `load_state` → líneas 466-499.
- `load_all_states` → líneas 502-535.
- `resume_from_checkpoint` → líneas 538-575.
- `reconcile_orphan_notebooks` → líneas 577-650.
- `register_notebook` → líneas 653-677.
- `exponential_backoff_seconds` → líneas 685-698.
- `retry_with_backoff` → líneas 701-738.
- `execute_phase_with_retry` → líneas 741-758.
- `with_retry` → líneas 761-780.

`models.py` (contrato adelantado):

- `ConceptStatus` (enum del pseudo-código) → líneas 36-47.
- `ConceptState` (contrato mínimo) → líneas 326-340.

`config.yaml`:

- `workdir` → línea 5.
- `pacing.backoff_seconds` / `pacing.max_retries` → líneas 38-39.

---

## 7. Qué sigue (para ubicar esta capa en el roadmap)

Esta capa deja listas las primitivas de progreso y recuperación. Las siguientes capas del pseudo-código (4-11) se apoyan en ella:

- Capa 4 (backend) usará `ConceptState.phase_data` para guardar `notebook_id` y disparará `reconcile_orphan_notebooks` ante fallos.
- Capa 6 (investigación) marcará `researching → researched` y persistirá `sources_path`/`raw_research_path`.
- Capa 7 (síntesis) marcará `researched → synthesized` y persistirá `synthesis_path`.
- Capa 8 (validación) marcará `synthesized → validated` (o `needs_review`/`failed`).
- Capa 5 (writer) marcará `validated → written → completed`.
- Capa 9 (runner) orquestará las transiciones, usará `resume_from_checkpoint`, `retry_with_backoff` y `load_all_states`.
- Capa 10 (CLI) expondrá `status`/`review` leyendo el estado persistido.

Mientras esas capas no existan, `state.py` ya permite crear, transicionar, persistir y recargar el estado de un concepto, y reintentar funciones con backoff: base suficiente para empezar a construir el resto del pipeline.