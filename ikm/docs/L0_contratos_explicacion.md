# Explicacion del codigo — v2 Capa L0: contratos y nucleo compartido

> Documento educativo. Explica, con palabras, qué es la **capa L0** de IT Knowledge Map v2, cómo se tradujo el pseudocódigo de la capa 0 del diseño técnico a código real, y por qué se tomó cada decisión. No copia bloques de código: solo referencia módulos y líneas clave.
>
> Proyecto: `C:\Users\DGVit\Proyectos\IT Career\ikm\` · Rama: `v2/L0-contratos` · Commit: `66d970d`
> Diseño de referencia: `IT_Knowledge_Map_v2_Technical_Pipeline_Design.md` §4, §6.1, §7.
> Pseudocódigo de referencia: `IT_Knowledge_Map_v2_Pseudocode_por_Capas.md` capa 0.

---

## 1. Que es L0 y por que va primero

L0 es la **base del contrato**: define una sola vez los esquemas de datos, los identificadores y las utilidades que consumen las 11 capas siguientes. El principio rector del diseño es "contratos primero" (§4.9): si los esquemas están mal, todo lo que viene después hereda el error.

En el pseudocódigo, la capa 0 se llama "Contratos y núcleo compartido" y su objetivo es explícito: *"definir una sola vez los esquemas de datos, identificadores y utilidades que consumen todas las capas"*. Su criterio de aceptación es el que gobierna la capa:

> los esquemas validan un release y la API de ejemplo; los tipos TS se generan de la misma definición; tests round-trip (modelo→JSON→modelo) pasan; ninguna capa futura redefine identificadores/hashes por su cuenta.

La decisión de fondo: **Pydantic como única fuente de verdad**. De los modelos salen tres artefactos (JSON Schema para validar el release en C7/CI, tipos TypeScript para el frontend, y los propios modelos Python). Si cada capa definiera sus propios identificadores o hashes, el sistema se fragmenta; por eso `ids.py` y `utils.py` son de importación obligatoria, no una convención.

L0 **no hace** lógica de dominio, acceso a red ni escritura en el vault. Es la capa más aburrida a propósito.

---

## 2. Archivos creados

Todo vive en `ikm/contracts/`:

| Archivo | Rol |
|---|---|
| `__init__.py` | `SCHEMA_VERSION`, `ENTITY_PREFIXES`, versión de generacion. Importa cero dependencias pesadas. |
| `ids.py` | Identificadores estables: prefijos, `nuevo_uid`, `uid_relacion`, `slugify`. |
| `release.py` | Entidades del release (contenido publico): `Area`, `Source`, `Concept`, `Relation`, `JourneyRecord`, `Evidence`, `Tour`, `ExplorationState` y sus enums. |
| `service.py` | Entidades del servicio (base de datos): `users`, `sessions`, `usage_windows`, `global_usage`, `conversations`, `messages`, `abuse_events`, `ip_windows`. |
| `config.py` | Feature flags, limites y plan del modelo, con los valores propuestos del diseño. |
| `errors.py` | Taxonomia de errores: `AbortStage`, `Warning`, `RateLimited`, `DegradeResponse`, `FailClosed`. |
| `utils.py` | `sha256_text/sha256_file`, `escritura_atomica`, `clave_cache`, `hash_arbol_vault`. |
| `validate.py` | `validar_contra_esquema` (aborta con `schema_invalid`). |
| `generate.py` | Pydantic → JSON Schema → tipos TypeScript. |
| `generated/schemas/*.json` | 23 esquemas generados (commiteados). |
| `generated/ts/*.ts` | 38 tipos TS generados, incluyendo aliases de enums. |
| `tests/test_l0_contracts.py` | 22 tests. |

Además: `ikm/pyproject.toml`, `ikm/README.md`, `ikm/.gitignore`, `ikm/releases/.gitkeep`.

---

## 3. `ids.py` — identidad que no depende del título

Archivo: `ikm/contracts/ids.py`.

El diseño §7.1 es tajante: *"Identidad estable. Los identificadores no dependen de títulos ni rutas"* (§4.5). En v1 el id era el slug de la ruta: si renombrabas la nota, se rompía. v2 separa identidad de presentación.

Tres funciones, tres reglas:

- `nuevo_uid(tipo)` → prefijo por tipo (`c_`, `a_`, `r_`, `j_`, `e_`, `s_`, `t_`) + 10 caracteres base32. Se asigna **una sola vez** y no cambia; el registro externo (C2) es quien lo mantiene.
- `uid_relacion(source, target)` → `r_` + `sha256(source + "|" + target)`. Es **dirigida**: `(A,B) ≠ (B,A)`. Es estable mientras ambos extremos existan. Por eso no se deriva de títulos ni de rutas.
- `slugify(titulo)` → solo cosmético, para URLs. Una ruta con el uid correcto y un slug desactualizado redirige; al revés (slug lindo con uid inventado) no resuelve.

El test `test_uid_relacion_dirigida_y_estable` verifica exactamente eso: mismo par → mismo uid; par invertido → uid distinto.

---

## 4. `release.py` — el contenido publico

Archivo: `ikm/contracts/release.py`. Mapea el §0.2 del pseudocódigo y el §7.2 del diseño.

### 4.1 Entidades

`Area` (uid, name, order, color_token), `Source` (uid, url, title, tier 1–4, concept_uids), `Concept` (uid, slug, title, aliases, area_uid, `sections`, sources, `verification_marks`, content_hash), `Relation`, `Explanation`, `JourneyRecord`, `Evidence`, `Tour`, `ExplorationState`.

Dos decisiones que vale la pena nombrar:

- **`Concept.sections`** replica las 10 secciones del contrato de v1 (`objetivo`, `esqueleto`, `como_funciona`, `detalles`, `ejemplo_minimo`, `errores_comunes`, `estado_actual`, `conexiones`, `ruta_estudio`, `preguntas_repaso`). Es un modelo propio (`ConceptSections`), no un `Dict[str, str]`: así el esquema obliga a que las claves sean las correctas y el TS generado las expone tipadas. El contenido es de v1 **sin reescritura** (§7.4); `content_hash` es el del texto original.
- **`verification_marks`** registra `sin verificar` / `⚠️ verificar` por sección. Son **señales de integridad de la spec**, no ruido: el diseño §C1 los parsea como flags y prohíbe stripearlos. El test `test_round_trip_concept` los incluye para que no se pierdan en la serialización.

### 4.2 `Relation` — dirigida, con explicación y estado

`Relation` tiene `type` (8 tipos + `untyped`), `type_basis` (`explicit`/`reviewed`/`none`) y una `Explanation` opcional con `status` (`quoted`/`authored`/`derived`/`reviewed`/`stale`). El `cross_area` está en el modelo, pero el pseudocódigo es explícito: **se calcula, nunca se declara** (lo hace C3). Por eso el test `test_relacion_cross_area_se_calcula_no_se_declara` solo verifica que el campo exista; la regla de negocio queda para L2.

### 4.3 `JourneyRecord` y `Evidence`

`JourneyRecord.publication` es un enum de tres niveles (`private`/`candidate`/`approved`) y **solo `approved` entra al release** (§0.2). `Evidence.review` es `manually_reviewed`: sin revisión humana no hay publicación. `period.basis` distingue `documented` de `confirmed_from_metadata`: una fecha tomada de metadatos sin confirmar del autor **no se publica**.

### 4.4 `ExplorationState`

Vive en el cliente (§19.4). Es un JSON serializable con `version` y `release_id`; `origin` distingue `manual` de `chat`. Es el contrato que L10 consume y que permite "recuperar exploraciones anteriores" (decisión 10 de la spec).

---

## 5. `service.py` — las tablas del servicio

Archivo: `ikm/contracts/service.py`. Es el §0.3 del pseudocódigo, casi literal: `User`, `Session`, `UsageWindow`, `GlobalUsage`, `Conversation`, `Message`, `AbuseEvent`, `IpWindow`.

Estas son contratos, no SQL. El acceso a datos y las migraciones son L5. Pero definirlos aquí fija dos reglas de seguridad antes de que exista código que las pueda violar:

- **`User.google_sub` es único**; la spec §16.1 dice buscar/crear por `sub`, nunca por correo. El email es dato, la identidad es el `sub`.
- **`Session.id_hash`**: en base de datos solo se guarda el hash de la cookie, nunca la cookie.
- **`IpWindow.ip_hash`**: la IP se almacena como hash con sal rotativa, nunca en claro.
- **`Message.expires_at`**: retención propuesta de 30 días (§25), con borrado por el usuario.

`Message` también deja el hueco para `blocks`, `ui_actions`, `retrieval_trace`, `scope_class`, `tokens_in/out`, `cached`, `degraded`: es la forma persistida de la respuesta del chatbot (L9/L10).

---

## 6. `config.py` — flags y limites como datos, no como if dispersos

Archivo: `ikm/contracts/config.py`. El pseudocódigo §0.4 lo dice: las limitaciones no bloqueantes se **parametrizan como config con valores propuestos**, marcados `[DR-xx]`. Cambiar el valor no cambia la estructión de ninguna capa.

- `FeatureFlags`: `embeddings_habilitados=False` [DR-09], `grafo_3d_habilitado=True` [DR-14], `streaming_por_bloques=False` [DR-10], `borradores_relaciones=True`, `persistencia_estados_servidor=False`.
- `LimitsConfig`: los valores de §17.2 — `max_message_chars=800`, `max_output_tokens=700` (incluye razonamiento), `min_interval_seconds=4`, `user_concurrency=1`, `global_concurrency=3`, `user_requests_per_hour=20`, `user_tokens_per_day=40000`, `offtopic_per_day=2`, `new_account_factor=0.5`, `retencion_mensajes_dias=30`.
- `PlanModelo` [DR-08]: `provider="groq"`, `modelo="openai/gpt-oss-120b"`, `tope_gasto_mensual_usd=5`.

`Config.hash_config()` produce el hash canónico de la configuración: es el tercer componente de la clave de caché (§6.1). El test `test_hash_config_determinista_y_sensible` verifica que es determinista y que **cambia** si cambia un límite (si no cambiara, la caché serviría resultados con configuración vieja).

---

## 7. `errors.py` — una taxonomía, no excepciones sueltas

Archivo: `ikm/contracts/errors.py`. El pseudocódigo §0.4 define cinco resultados posibles ante un fallo, y cada uno tiene un comportamiento distinto:

| Taxón | Significado | Resultado |
|---|---|---|
| `AbortStage(causa)` | etapa de contenido fallida | detiene la etapa, conserva salidas previas |
| `Warning(senal)` | reporte | NO detiene |
| `RateLimited(reason, retry_after)` | límite | 429 con reason (`interval`/`concurrency`/`rate`/`user_budget`/`global_budget`/`offtopic`) |
| `DegradeResponse(motivo)` | recuperación sin modelo | reduce funcionalidad, no confiabilidad |
| `FailClosed(servicio)` | servicio indispensable caído | 503; el sitio estático sigue |

Que esto viva en L0 evita que L6/L9 inventen códigos de error ad hoc. `RateLimitReason` es un enum cerrado: la interfaz muestra un mensaje por motivo y el `retry_after` se propaga del proveedor.

---

## 8. `utils.py` — hashes y escritura atómica

Archivo: `ikm/contracts/utils.py`. Cuatro utilidades que todo el sistema reutiliza:

- `sha256_text` / `sha256_file` / `sha256_bytes`: un solo algoritmo (sha256, como dice la convención del pseudocódigo).
- `escritura_atomica(path, bytes)`: escribe a un `.tmp` **del mismo directorio** y hace `os.replace`. El `os.replace` atómico de POSIX/Windows garantiza que nunca queda un archivo a medias tras un fallo. Por eso el `tmp` debe estar en el mismo filesystem que el destino.
- `escribir_json_atomico`: JSON con `sort_keys=True` y `indent=2`. El `sort_keys` es lo que hace determinista la salida: mismo contenido → mismo byte → mismo hash.
- `clave_cache(entrada, version_etapa, hash_config)`: `hash(entrada) + version_etapa + hash_config`. Es la idempotencia de §6.1: si la clave no cambió, la etapa se omite.
- `hash_arbol_vault(root)`: hash estable de un árbol (ruta relativa + sha256 por archivo). Es la comprobación de "solo lectura": si el vault cambió durante una corrida, el hash difiere y C0/L1 aborta con `vault_modified`.

`test_hash_arbol_vault_ignora_orden` verifica que el orden de los archivos no afecta el hash (crítico para que dos máquinas den el mismo resultado).

---

## 9. `generate.py` — una definición, tres artefactos

Archivo: `ikm/contracts/generate.py`. Es la parte más "de contrato" de L0: de los modelos Pydantic salen JSON Schema y tipos TypeScript.

Flujo:

1. `_importar()` carga los nombres de `release.py` y `service.py`.
2. `generar_json_schemas()` llama a `model_json_schema()` de Pydantic y **reescribe los `$ref` locales** de `#/$defs/X` a `#/definitions/X`, para que cada schema sea autónomo y legible. Cada schema lleva `title` y `x-entity-kind` (`release`/`service`).
3. `_escribir_ts()` lee los schemas recién escritos y emite una interfaz por modelo. Aquí está el detalle importante: **los enums de Python no son `BaseModel`**, así que Pydantic los emite como `$ref` a un `definitions/RelationType` que no existe como interfaz. El generador detecta `_es_enum(nombre)` y emite un `export type RelationType = "depends_on" | ...` en su propio `.ts`. Sin ese paso, `Relation.type` saldría como `unknown`.
4. `regenerar()` orquesta y devuelve un hash de todo lo generado.

El criterio de idempotencia está en `test_generacion_schema_y_ts`: regenerar dos veces sobre el mismo destino produce el **mismo hash**. Y el test `test_generacion_schema_y_ts` también comprueba que `Concept.ts` y `Relation.ts` existen con la interfaz esperada.

> Lección de implementación: la primera versión del generador producía `type?: unknown` en `Relation` porque los enums no estaban en el registro de modelos. El fix no fue "tocar el modelo", fue registrar los enums como ciudadanos de primera clase. Quedó cubierto por tests.

---

## 10. `validate.py` — validar aborta

Archivo: `ikm/contracts/validate.py`. Una sola función: `validar_contra_esquema(obj, esquema, etapa)`. Valida con Pydantic y, si falla, lanza `AbortStage("schema_invalid")` con la lista de errores por campo.

Es la materialización de la convención del pseudocódigo: *"SI no valida ENTONCES ABORTAR('schema_invalid')"*. No devuelve `False` ni registra y continúa: aborta. C7 (compuerta) y CI dependen de que esta función no perdone.

---

## 11. Criterios de aceptación y verificación

**Criterios del pseudocódigo (capa 0):**

- [x] los esquemas validan un release y la API de ejemplo → `tests/test_l0_contracts.py::test_release_de_ejemplo_valida`, `test_api_de_ejemplo_valida` con `tests/fixtures_l0.json`.
- [x] los tipos TS se generan de la misma definición → `test_generacion_schema_y_ts`; `Relation.ts` usa `RelationType`/`TypeBasis`, no `unknown`.
- [x] tests round-trip (modelo→JSON→modelo) → `test_round_trip_concept`, `test_round_trip_relacion_dirigida`, `test_service_user_unico_por_sub`.
- [x] ninguna capa futura redefine identificadores/hashes por su cuenta → `ids.py`/`utils.py` son el único lugar que los define; `config.hash_config()` y `clave_cache()` son las únicas fuentes de hash de config/caché.

**Verificación ejecutada en laptop 1** (venv `.venv/Scripts/python.exe`):

```
.venv/Scripts/python.exe -m pytest ikm/tests/test_l0_contracts.py -q
22 passed in 2.08s
```

`py_compile` no es necesario por separado: pytest importa todos los módulos. El generador se ejecutó y produjo 23 schemas + 38 TS, commiteados en `66d970d`.

---

## 12. Qué NO hace L0 (y qué deja para las siguientes capas)

- **No** lógica de dominio: no decide qué se publica, no tipifica relaciones, no asigna identidades (eso es C2/C3/C4 en L2–L3).
- **No** acceso a red ni escritura en el vault.
- **No** SQL ni migraciones (L5), ni recuperación (L7), ni verificación de respuestas (L8).
- **No** juzga la calidad del contenido de los 255 conceptos (fuera de alcance por decisión del autor): los toma como dados.

**Pendiente inmediato:** L1 (inventario y parseo C0–C1) sobre el vault real. Las precondiciones P1–P5 de v1 (importabilidad, packaging, hash canónico, compuerta DoD) se resuelven **al importar v1 en L1+**, no bloquean L0.

---

## 13. Mapa de referencia rápida

| Concepto del pseudocódigo | Código |
|---|---|
| `PREFIJOS`, `nuevo_uid`, `uid_relacion`, `slug` | `contracts/ids.py` |
| `ESQUEMA Area/Concept/Source/Relation/JourneyRecord/Evidence/Tour/ExplorationState` | `contracts/release.py` |
| `TABLA users…ip_windows` | `contracts/service.py` |
| `CONFIG feature_flags / limites / plan_modelo` | `contracts/config.py` |
| `TAXONOMIA_ERRORES` | `contracts/errors.py` |
| `sha256_*`, `escritura_atomica`, `clave_cache` | `contracts/utils.py` |
| `validar_contra_esquema` | `contracts/validate.py` |
| `generar_tipos` | `contracts/generate.py` |
| Aceptación L0 | `tests/test_l0_contracts.py`, `tests/fixtures_l0.json` |
