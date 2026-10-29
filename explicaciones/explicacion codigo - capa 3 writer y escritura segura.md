# Explicación del código — Capa 3: writer y escritura segura

> Documento educativo. Explica, con palabras, qué se implementó en la **Capa 3 de implementación** del proyecto `it-concept-map`, cómo se tradujo el pseudo-código de la Capa 5 del diseño técnico (escritura segura) a código real, y por qué se tomó cada decisión. No copia bloques de código: solo referencia módulos y líneas clave. Incluye el hallazgo de diseño **read_bytes vs read_text** (sección 5).

Proyecto: `C:\Users\DGVit\Proyectos\IT Career\it-concept-map\`
Vault de origen: `C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map\` (notas `.md` con bloque `<!-- ai:start --> ... <!-- ai:end -->`)

---

## 1. Qué es la Capa 3 y por qué va acá

La Capa 3 de implementación es el **writer**, es decir, la única pieza del sistema que se permite modificar los archivos del vault. En el pseudo-código esto corresponde a la **Capa 5 (Escritura segura, `writer.py`)**. El desfase de numeración es el mismo que ya se documentó en las capas anteriores: la Capa 1 de implementación fusionó las Capas 1 y 2 del diseño (modelo de datos + lectura del vault) y la Capa 2 de implementación tradujo la Capa 3 del diseño (estados). Además, esta capa **adelanta la Capa 5 salteando la Capa 4 del diseño (backend)**: se puede hacer porque el writer trabaja sobre un objeto `Synthesis` que llega *ya validado*; no necesita que exista el backend real para diseñar la escritura. El docstring de `writer.py` (líneas 1-2) lo declara explícito: "Capa 3 de implementacion / Capa 5 del diseno".

¿Por qué el writer merece una capa entera y tanta ceremonia? Porque es el punto donde el sistema toca algo que **no puede volver a generar**: tus notas escritas a mano. Todo lo demás es reconstruible (se puede re-investigar, re-sintetizar, re-validar); si el writer rompe una nota, se destruye trabajo humano. Por eso el pseudo-código le exige: tocar *solamente* el interior del bloque autorizado, hacer backup antes de escribir, escribir atómicamente, verificar releyendo desde disco, y restaurar ante cualquier duda. La filosofía es **falla cerrada** ("fail-safe"): si algo no se puede probar que salió bien, se considera que falló.

La idea central del diseño es el **principio de mínimo privilegio**: el vault tiene una zona editable (el interior del bloque `ai:start`/`ai:end`, donde vive el contenido generado por el pipeline) y una zona sagrada (el resto de la nota: frontmatter, título, headings, la sección "Que abarca", la sección "Relacionados" con sus wikilinks). El writer no "trata de no romper" la zona sagrada: la zona sagrada ni siquiera entra por el camino de escritura — se *reemplaza alrededor* de ella y luego se **verifica byte a byte** que quedó idéntica.

También hay una regla de arquitectura que hasta ahora era solo declarativa y con esta capa se vuelve real: "el registry solo lee, solo el writer escribe". Con `writer.py` existe el primer módulo con permiso de escritura sobre el vault, y queda claro que ningún otro módulo deberá hacerlo.

---

## 2. Archivos creados y afectados

Todos viven en `it-concept-map\`:

| Archivo | Rol |
|---|---|
| `writer.py` | Escritura segura: `SafeWriter`, reemplazo del interior del bloque, integridad del afuera, verificación de frontmatter/headings/wikilinks, escritura atómica con backup/restore, detección de edición concurrente, dry-run con diff, excepciones tipadas e integración con `state.py`. **Nuevo (946 líneas).** |
| `README.md` | Actualizado: lista `writer.py` en la estructura, documenta sus funciones y reglas, y declara "Capa 3 (writer, escritura segura) implementada". |
| `pyproject.toml` | Actualizado: `[tool.setuptools] py-modules` ahora incluye los cuatro módulos (`models`, `registry`, `state`, `writer`). Nota: cuando la Capa 2 se documentó, este archivo todavía sólo anunciaba `models` y `registry`; fue actualizado en esta capa para ponerse al día con `state` y `writer`. |

Sin cambios: `models.py`, `registry.py`, `state.py`, `config.yaml` (el writer los consume tal como están). Lo que sí conviene ver de `config.yaml` son las claves `markers.start`/`markers.end` (líneas 14-16) y `workdir` (línea 5), que el writer lee con su helper `_cfg`.

---

## 3. La idea en una frase

> El writer no escribe una nota nueva: toma la nota original, cambia *únicamente* lo que está entre los dos marcadores, escribe ese resultado de forma atómica, y después relee desde disco y demuestra — con hash y byte a byte — que todo lo demás quedó idéntico. Si no puede demostrarlo, restaura el backup y declara el fracaso.

---

## 4. `writer.py` por partes

Archivo: `it-concept-map\writer.py` (946 líneas). El docstring inicial (líneas 1-28) es la "constitución" de la capa: enuncia responsabilidades y reglas de negocio antes de cualquier código. Prioridad de lectura si querés entender la capa: docstring → `write_concept` → resto.

### 4.1 Contrato, versión y constantes

- `WRITER_VERSION = "1.0.0"` (línea 58). Cumple el mismo rol que `SCHEMA_VERSION` en `models.py` (línea 20) y `state.py` (línea 27): identifica el *formato* de escritura. Se persiste en el estado (`record_write_result`, línea 799) para trazabilidad: si mañana cambia cómo se escribe, se puede auditar qué nota fue escrita con qué versión.
- `MARKER_START_DEFAULT` / `MARKER_END_DEFAULT` (líneas 60-61): los marcadores canónicos del pseudo-código, como defaults; los valores reales salen de `config.yaml`.
- `REQUIRED_HEADINGS` (línea 64): los headings de la "voz del autor" (`Que abarca`, `Relacionados`) que deben seguir presentes después de escribir. Es la base de la defensa en profundidad (4.7).

### 4.2 Excepciones tipadas (líneas 96-165)

El pseudo-código pide errores con precisión diagnóstica ("si faltan marcadores, falla — no se inventan"). La capa lo implementa como una familia de clases: `WriterError` (base, 96-97), la familia de verificaciones `VerificationError` (100-101), y una clase específica por cada modo de falla: `MissingMarkersError`, `DuplicateMarkersError`, `MarkerOrderError`, `ConcurrentEditError`, `OutsideIntegrityError` (que además guarda `expected` vs `actual`), `OutsideByteMismatchError`, `FrontmatterChangedError`, `FrontmatterSemanticMismatchError`, `InsideMismatchError`, `MarkerCountError`, `HeadingsChangedError`, `WikilinksChangedError` y `WriteFailedError`.

Por qué tipadas y no mensajes sueltos: cada excepción comunica *qué falló y qué hacer* sin parsear strings. El orchestrador (capa 9) va a clasificar reintentables vs no reintentables mirando el tipo, igual que ya hace `state.py` con `InvalidTransitionError` y como hará la Capa 4 con `BackendAuthError` vs `BackendNetworkError`. Heredar de `VerificationError` las fallas de verificación posterior permite tratarlas como familia ("algo escribió mal") sin acoplarse a los nombres individuales.

### 4.3 Newlines: detectar y normalizar (líneas 173-185)

`detect_newline()` cuenta cuántas terminaciones `CRLF` y `LF` predominan en el texto y devuelve la dominante. `normalize_newlines()` unifica todo a `LF` y después re-expande al estilo objetivo. ¿Por qué importa? Porque una nota de Obsidian en Windows suele estar en CRLF, y si al insertar el contenido nuevo se mezclara con LF adentro del bloque, el archivo tendría terminaciones de línea inconsistentes (feo de ver, y sobre todo *modificaría bytes que no se debían tocar* si se "arreglara" a fondo). La regla de la capa: el afuera conserva sus newlines originales porque nunca se reescribe; el interior nuevo se normaliza al estilo del archivo destino.

Detalle técnico que vale la pena conocer: `detect_newline` del writer (que *cuenta* y elige la dominante, líneas 173-177) es más precisa que su gemela del `registry.py` (líneas 124-127, que solo mira si existe *algún* CRLF). Es una de las dos implementaciones que conviven (ver decisiones, ítem 9).

### 4.4 Marcadores y el bloque: el reemplazo quirúrgico (líneas 193-258)

- `MarkerSpan` (193-202): un dataclass congelado que describe *dónde* está el bloque: línea del marcador start, línea del end, rango del interior y el texto actual del interior. Es el "mapa quirúrgico" de la nota: una sola vez se localiza el bloque, y todos los demás operadores trabajan sobre ese mapa en vez de re-escanear.
- `find_markers()` (204-224): busca exactamente un start y un end, en ese orden, trabajando por líneas (`splitlines(keepends=True)`, que conserva los terminadores de línea originales). Devuelve `None` si algo no calza (0, 2+, orden invertido). No lanza: convertir el `None` en el error preciso lo hace otro método (ver 4.8, `_raise_marker_error`). Por qué separar "detectar" de "clasificar": permite usar `find_markers` como predicado silencioso (hashes, dry-run) y solo clasificar el diagnóstico cuando se va a fracasar.
- `count_markers()` (227-233): conteo crudo de apariciones por subcadena. Es la base del diagnóstico: distingue "no hay nada", "hay duplicados" y "hay dos pero en orden incorrecto".
- `replace_inside()` (236-258): el corazón del reemplazo. Reconstruye el texto como `antes + interior_nuevo + después`, donde "antes" incluye la línea del marcador start y "después" empieza en la línea del marcador end. Consecuencia: los marcadores quedan **verbatim** (mismos bytes, mismo newline) y las líneas adentro se reemplazan. El interior nuevo se normaliza al newline del archivo y, si queda vacío, se deja una línea vacía entre los marcadores (nunca se colapsan — regla del pseudo-código). Nota honesta: la firma acepta los marcadores como parámetro pero no los usa (`del marker_start, marker_end` en línea 249) — se respeta la firma del diseño para que las capas futuras no tengan que cambiar contratos.

### 4.5 Integridad del afuera: hash + byte a byte (líneas 266-337)

- `sha256()` (266-268): el hash del pseudo-código. SHA-256 es determinista: el mismo texto siempre da el mismo hash, y cualquier cambio de un solo bit cambia el hash por completo. Es el mecanismo de "sello" del afuera.
- `extract_outside()` (271-288): devuelve **todo el texto excepto el interior** del bloque (los marcadores se incluyen, tal como dicta la regla del pseudo-código: "los marcadores se incluyen en el afuera"). Si no hay bloque válido, lanza `MissingMarkersError` (aquí sí se clasifica, porque este operador exige bloque).
- `content_hash_outside()` / `content_hash_inside()` (291-312): versiones amables para consultas — devuelven `None` si no hay bloque en vez de lanzar. Son las que usa la detección de concurrencia (4.8) y las que hablan con los campos `content_hash_outside`/`outside_hash_at_read` del `ConceptMeta` (registra `registry.py` al escanear, líneas 643-647).
- `verify_outside_integrity()` (315-337): la verificación de integridad con **dos niveles**. Primero compara el hash del afuera después contra el hash calculado antes; si difieren, `OutsideIntegrityError`. Luego, además, compara el afuera **byte a byte** (texto completo, no hash) entre original y escrito: `OutsideByteMismatchError`. ¿Por qué duplicar si el hash ya cubre todo? Por la filosofía de "ni un byte más": el hash es el sello, la comparación byte a byte es la prueba fehaciente. En la práctica, la comparación byte a byte también atrapa *bugs del propio código de hashing o normalización* — no solo colisiones teóricas de SHA-256, que son imposibles en la práctica, sino errores de programación que hashen textos distintos por accidente. El pseudo-código lo pide explícito: "verificación adicional byte a byte del afuera (no solo hash)".

Concepto pedagógico: **hash vs comparación directa**. El hash te da un "resumen" compacto que podés persistir y comparar después (útil en `estado.json` para auditar post-mortem); la comparación directa te da la verdad absoluta pero exige todo el contenido. El writer usa ambos porque tiene ambos en mano en el momento de verificar.

### 4.6 Frontmatter: solo verificar, nunca escribir (líneas 344-409)

Tres piezas:

- `parse_frontmatter()` (347-371): detecta el bloque `---...---` (tolerando BOM inicial) y parsea el YAML. Si la nota no tiene frontmatter devuelve `(None, texto)` sin dramas — la capa es tolerante con notas sin frontmatter porque solo se van a *verificar*, no exigir.
- `extract_frontmatter_block()` (374-383): el texto del bloque YAML inclusive delimitadores. Es el insumo de la comparación byte a byte.
- `verify_frontmatter_preserved()` (386-409): verificación de dos fases. Principal: el bloque de frontmatter debe ser **idéntico byte a byte** entre original y escrito. Red de seguridad: además de esa comparación, se parsean ambos como YAML y se comparan los dicts; si difieren semánticamente (mismo texto pero se llegó a dict distinto — teóricamente imposible si el byte-a-byte pasó, por eso es red de seguridad), lanza `FrontmatterSemanticMismatchError`.

¿Por qué verificación en dos niveles y no solo byte a byte? El pseudo-código ordena: "la verificación principal es byte a byte del bloque, la comparación semántica es red de seguridad". La lógica pedagógica: si ya se comprobó que los bytes son idénticos, el YAML no puede ser semánticamente distinto, así que el segundo chequeo nunca debería dispararse. Pero si un bug lo hace disparar, tenés un diagnóstico distinto (semántica) al mismo precio. Nota de diseño: el writer define su propio `parse_frontmatter` y no reutiliza el de `registry.py` (línea 134) porque las firmas difieren (el del registry devuelve una 3-tupla con `has_frontmatter`, pensada para el scan; el del writer es una 2-tupla para verificación) y porque la verificación necesita además el bloque byte a byte, algo que el registry no expone.

### 4.7 Defensa en profundidad: headings y wikilinks (líneas 417-474)

Esta subsección es una **agregación de esta capa** respecto del pseudo-código, que pedía verificar "frontmatter/titulo/navegacion/wikilinks siguen presentes" sin detallar tanto. Acá se concreta:

- `verify_headings_preserved()` (438-453): verifica que los headings obligatorios del original (`REQUIRED_HEADINGS`) sigan presentes después de escribir. ¿Por qué "obligatorios" y no todos los headings? Porque los otros pueden cambiar por la propia escritura (los headings del estudio generado son nuevos), pero los de la voz del autor son la señal de "la parte manual sobrevivió".
- Normalización por acentos: `_accent_less()` (417-422) y `_norm_heading()` (425-426) quitan acentos y signos de apertura/cierre y pasan a minúsculas antes de comparar. ¿Por qué? Porque el vault escribe los headings con acento ("¿Qué abarca?") mientras que la spec los nombra sin acento ("Que abarca"). Comparar crudo daría falso negativo. Esa normalización intermedia es un detalle pequeño que evita un bug silencioso.
- `verify_wikilinks_preserved()` (469-474): extrae el *set* de wikilinks (con regex, línea 456, manejando alias `[[x|alias]]` y anclas `[[x#sección]]`, líneas 459-466) y exige que el set sea idéntico antes y después. ¿Set y no lista? Porque la escritura puede reordenar líneas adentro del bloque sin alterar la semántica de enlaces: lo que importa a la nota es *qué* enlaces existen, no en qué línea están.

Por qué "defensa en profundidad": el afuera ya está protegido por hash + byte a byte, que atrapan *cualquier* cambio fuera del bloque. Estos chequeos adicionales no aportan protección nueva contra el writer; aportan **diagnóstico granular** ("el heading Que abarca desapareció" es más accionable que "el afuera difiere") y un seguro ante fallos del propio mecanismo de verificación. Es el patrón de defensa en capas: cada capa de chequeo tiene un propósito distinto (detección, diagnóstico, redundancia).

### 4.8 `SafeWriter`: el único objeto que toca el vault (líneas 497-783)

#### Constructor (525-546)

Lee la config con el helper local `_cfg()` (67-82, mismo patrón de `_cfg` en `state.py`), y resuelve tres rutas: `workdir` (arg → config → `cwd/workdir`), `backup_root = workdir/backups` y `tmp_root = workdir/tmp`. Los marcadores vienen de config con los defaults canónicos como plan B.

Sobre los directorios temporales: el docstring (líneas 25-26) y el constructor (línea 540) explican por qué el tmp vive ahí y no en `C:\Temp`: la escritura atómica de Python (`os.replace`) solo es atómica garantizada dentro del **mismo volumen/filesystem** (lo implementa el SO como un rename). Si el tmp estuviera en otro disco, `os.replace` tendría que copiar+borrar, y ahí lo atómico se rompe. Vault y workdir viven en el mismo árbol (`C:\Users\DGVit\Proyectos\IT Career\`), así que el rename es rename de verdad.

#### `write_concept()` (550-646): el flujo principal

Es la implementación directa del flujo de 11 pasos del pseudo-código (Capa 5, sección 1). En orden:

1. **Leer en bytes y decodificar UTF-8** (565-567): ver sección 5 — este punto pequeño trae el hallazgo de diseño más importante de la capa.
2. **Validar marcadores** (570-573): `find_markers` → si es `None`, `_raise_marker_error()` clasifica el diagnóstico (faltan / duplicados / orden incorrecto). Falla cerrado: no se *insertan* marcadores faltantes.
3. **Hash del afuera antes** (575-578): el sello contra el que se va a comparar después.
4. **Detección de edición concurrente** (580-590): ver 4.8.d. Si el archivo cambió entre el scan (registry) y ahora, `ConcurrentEditError` — no se escribe encima del trabajo del otro.
5. **Construir texto nuevo** (592-602): `render_inside()` (482-489, normaliza el Markdown de la síntesis al newline del archivo) y `replace_inside()`. Y aquí un paso clave: **pre-check en memoria** antes de tocar disco (598-602) — la misma `verify_outside_integrity` se corre sobre el texto que se *piensa* escribir. Si la lógica de reemplazo tiene un bug, se descubre antes de escribir, no después.
6. **Dry-run** (604-614): si es dry-run, se devuelve un `DiffResult` (497-519) con el diff unificado (`unified_diff`, 509-519, usando `difflib`) sin tocar disco ni estado. Implementa el `--dry-run` del pseudo-código.
7. **Backup antes de escribir** (616-617): `backup()` (650-656) copia byte a byte a `workdir/backups/<concept_id>/<nombre>.<timestamp>.<uuid>.bak` con `shutil.copy2` (preserva mtime). ¿Por qué backup *antes* y no "confiar en os.replace"? Porque el backup es la única versión que garantiza el estado previo a la escritura: si la verificación posterior falla (o si el orchestrador escribe mal el tmp), lo único que da certeza absoluta de "cómo estaba antes" es esa copia. El timestamp compacto con sufijo uuid (85-88) hace acumulativos los backups por concepto sin colisiones de nombre.
8. **Escritura atómica** (619-625): `_atomic_write()` (668-678): escribe el texto en `workdir/tmp/<nombre>.<uuid>.tmp` con **write_bytes** (a nivel de bytes: control exacto sobre lo que queda en disco) y luego `os.replace(tmp, path)`. El `os.replace` es atómico desde el punto de vista del observador: o la nota vieja sigue ahí, o la nueva está *completa*; nunca hay una nota "a medias" visible, aunque el proceso muera a mitad.
9. **Verificación releyendo desde disco** (627-637): `_verify()` (4.8.f). Si falla, `restore()` (658-664) copia el backup de vuelta con `copy2` (preserva mtime, clave para no disparar falsos positivos de concurrencia después), se limpia el tmp (`unlink(missing_ok=True)`) y se lanza `WriteFailedError`. Si el propio `_atomic_write` lanza `OSError`, se falla sin restaurar: el `os.replace` falló *antes* de tocar el destino, la nota original nunca se tocó (comentario en 622-625).
10. **Éxito** (639-646): `WriteResult` (contrato adelantado en `models.py`, líneas 307-318) con path, backup, hashes afuera/interior, `written_at` y `success=True`.

#### Detección de edición concurrente (682-709)

`concurrent_edit_detected()`: si hay hash del afuera `at_read` (persistido por el registry en `ConceptMeta.outside_hash_at_read`), ese hash es la referencia autoritativa — se recalcula el hash actual del afuera y si difiere (o el bloque de marcadores se perdió), alguien modificó la nota entre el scan y ahora. Si no hay hash, cae al **mtime con epsilon** (0.001 seg, línea 687): Obsidian a veces "toca" archivos sin cambiar contenido, y el epsilon absorbe esas fluctuaciones. El docstring (691-695) lo documenta: `copy2` en backups preserva mtime para no disparar falsos positivos con las restauraciones.

¿Por qué hash primero y mtime como fallback? Porque el hash no miente (dice *qué* cambió); el mtime solo dice que algo pasó pero no garantiza contenido (y garantiza poco: se puede tocar sin cambiar). Hash es exacto pero más costoso (leer y hashear todo el afuera); mtime es barato pero ambiguo. La jerarquía "hash si hay, mtime si no" refleja eso.

Por qué importa: sin esta verificación, una corrida del pipeline podría pisar una edición manual que el autor acabara de hacer en Obsidian entre el scan y la escritura. Es la protección del "no sobrescribir silenciosamente" del pseudo-código.

#### `_verify()` (725-766): qué se verifica y de dónde vienen los datos

La lista de verificaciones después de escribir, **releyendo desde disco** con `_read_text()` (713-721), no confiando en el texto en memoria:

1. Hash + byte a byte del afuera (739-742).
2. Marcadores: siguen siendo exactamente uno de cada, en orden (745-751) — `MarkerCountError` si no.
3. Interior escrito == interior esperado (753-759). Comparación normalizada a `\n`: queda a salvo de las diferencias de estilo de newline (que son *sabidas*, no un bug). Si difiere, `InsideMismatchError`: esto despeja la pregunta "¿se escribió realmente la síntesis validada?".
4. Frontmatter byte a byte + semántica (761-762).
5. Headings y wikilinks de la voz del autor (764-766).

Detalle técnico honesto: la firma acepta `new_text` y `concept` pero no los usa (`del` en línea 735) — están reservados para la firma del diseño, igual que en `replace_inside`. No es descuido; son contratos adelantados para las capas que vienen.

#### `_read_text()` (713-721): la pieza del hallazgo

La responsabilidad es simple a la vista: "leer el archivo como bytes y decodificar UTF-8", y con eso reemplaza el uso de `read_text()` nativo. Por qué (docstring 717-720): `read_text()` usa newlines universales y traduce `CRLF → LF`; eso invalidaría los hashes del afuera en notas CRLF. Esto se desarrolla a fondo en la sección 5.

#### `_raise_marker_error()` (770-783)

Convierte el `find_markers → None` en el error específico: cuenta marcadores y decide entre `DuplicateMarkersError`, `MarkerOrderError` o `MissingMarkersError`. Es el ejemplo pedagógico de "diagnostico progresivo": primero preguntá *cuántos hay*, después *en qué orden*, y recién después decí *lo que falta*.

### 4.9 Dry-run: `DiffResult` (497-519)

Dataclass con path, texto original, texto propuesto, interior antes/después y newline detectado, más el método `unified_diff()` que genera la salida estilo `git diff` con `difflib` (del stdlib, sin dependencias nuevas). La rama dry-run en `write_concept` (604-614) devuelve este objeto *antes* del backup y de la escritura atómica. Semánticamente: "mostrame lo que harías, no hagas nada" — ni estado ni disco cambian, lo que lo hace perfecto para revisar un concepto antes de commitear.

Detalle elegante: el dry-run también pasa por el pre-check de integridad (paso 5) antes de devolver el diff. Vale decir: un diff que se muestra ya *está garantizado* como safe (no mostraría un diff que rompería la nota). El dry-run no es solo una vista previa: es una escritura "falsa" con todas las garantías menos la de escribir.

### 4.10 Integración con `state.py`: transiciones y fase completa (790-899)

El pseudo-código pide: "si OK, marcar estado DONE con checkpoint writing y persistir write_result; si falla, marcar failed en fase writing y propagar". La implementación:

- `record_write_result()` (791-799): guarda el resultado en `state.phase_data["write_result"]` (backup_path, outside_hash, inside_hash, written_at, `WRITER_VERSION`). Por qué en `phase_data`: es el lugar del estado reservado para los datos de la fase actual, así todos los Journal de auditoría quedan en un solo lugar para el runner futuro.
- `mark_written()` (802-816): transición `validated → written`, **idempotente** (si ya está en `written` o `completed`, no falla: es idempotencia deliberada). Usa `state.transition_to()` de `state.py` (líneas 232-268) con `checkpoint="writing"`, y persiste con `save_state()` (líneas 368-421, escritura ya atómica por la capa 2).
- `mark_completed()` (819-829): transición `written → completed`, también idempotente.
- `mark_writing_failed()` (832-853): marca `failed` en fase writing. Si ya estaba en `failed`, solo actualiza `error` y `checkpoint` (no re-transiciona: `failed` no tiene salida hacia sí mismo en `VALID_TRANSITIONS`, `state.py` línea 76). Si `transition_to` lanza `InvalidTransitionError` (ej. desde `needs_review`, que a `failed` no llega según el diseño), **no se silencia: se propaga** (849-851). Discusión pedagógica: fallar con ruido es mejor que fallar en silencio — el diseño explícito de que ciertas rutas no son válidas es información.
- `writing_phase()` (856-899): el punto de entrada que la Capa 9 (orchestrador) va a llamar. Lo que hace:
  1. Carga el estado si no te lo pasaron (`load_state`, o un `ConceptState` nuevo como punto de partida).
  2. **Idempotencia**: si el concepto ya está `completed` y no es dry-run, lo devuelve tal cual (880-881). Implementa "done es terminal: nunca se reejecuta".
  3. Crea un `SafeWriter` si no te lo inyectaron (inyección de dependencias: el orchestrador futuro va a poder pasarle su propio writer con una config distinta; el default se comporta igual).
  4. Llama `write_concept`; si tira cualquier excepción, marca `failed` (salvo en dry-run, donde no toca estado) y **re-propaga** (886-891).
  5. Si volvió un `WriteResult` real, encadena `mark_written` + `mark_completed` (897-898).

Nota de estilo: no atrapa la excepción y no la traduce — el orchestrador decide qué hacer con el tipo (reintentable vs no). Es exactamente el patrón de separación de responsabilidades que `state.py` ya adoptó para los reintentos: *la mecánica en una capa, la política en otra*.

---

## 5. El hallazgo del diseño: `read_bytes` vs `read_text`

Este es el hallazgo técnico más importante de la capa y conviene contarlo como historia, porque es un bug silencioso clásico de trabajar con archivos en Python.

### El problema

Python ofrece dos formas de leer un archivo de texto:

- **`path.read_text()`** — abre en modo texto con la opción `universal newlines` activa: cada `\r\n` (estilo Windows) y `\r` (estilo Mac clásico) se **traduce a `\n`** en el string que recibís.
- **`path.read_bytes()` + `.decode("utf-8")`** — lee los bytes crudos del disco y los decodifica. El `\r\n` llega a memoria tal como está en disco, como dos caracteres consecutivos.

La primera parece la opción natural para leer texto. El problema: **el string que te devuelve no es lo mismo que hay en disco**.

### Por qué le rompe este proyecto en particular

Todo el esquema de integridad de la capa se basa en poder comparar hashes y texto byte a byte *entre dos momentos distintos en el tiempo*:

1. El **registry** (Capa 1) escanea la nota cuando el pipeline arranca y la lee *con `read_bytes`* (`registry.py`, líneas 514-519). De ahí calcula `content_hash_outside` y lo persiste en `ConceptMeta.outside_hash_at_read` (líneas 643-647).
2. El **writer**, mucho después, re-lee la nota para (a) detectar edición concurrente y (b) verificar después de escribir.

Si el paso 2 usara `read_text()`, en una nota con terminaciones CRLF (normal en Windows / Obsidian) el string en memoria ya no tiene los `\r`, el texto del afuera es *distinto al texto que se hasheó en el scan*, y el hash no coincide → **la detección de edición concurrente daría falso positivo en TODAS las notas CRLF** (`ConcurrentEditError` en una nota que nadie tocó). Igual con la verificación byte a byte: se estarían comparando dos versiones *normalizadas distinto* del mismo archivo, y el resultado sería "el afuera cambió" cuando en realidad "el lector tradujo los bytes de manera distinta". Ese bug no explota en Linux (donde todo es LF), es 100% específico de archivos con CRLF — justamente el tipo de archivo dominante en este vault.

### La regla que se extrae

> **Hashear lo que hay en disco, no lo que el runtime te tradujo.**

La decisión que se tomó: `SafeWriter._read_text()` (writer.py, líneas 713-721) hace explícito el patrón — `read_bytes()` primero, `decode("utf-8")` después — y se usa en **todos** los puntos donde el hash o la comparación byte a byte tienen valor (detección de concurrencia, verificación post-escritura). Lo mismo vale en el otro extremo del ciclo: la escritura se hace con `tmp.write_bytes(text.encode("utf-8"))` (línea 676) y **no** con escribir en modo texto, porque en Windows el modo texto *también* traduce (`\n` → `\r\n` al escribir, si no desactivás la traducción) y volvería a corromper la correspondencia con los bytes esperados.

El ciclo completo queda en el dominio de los bytes:

```
disco (bytes con CRLF) → read_bytes → decode UTF-8 (CRLF intacto en memoria)
                       → manipular solo el interior
                       → encode UTF-8 → write_bytes → os.replace
                       → read_bytes → decode → verificar byte a byte
```

### Corolarios que el mismo hallazgo habilita

- **`detect_newline` es necesario**: si uno leyera *siempre* con `read_text`, aplicar newlines sería irrelevante porque ya las normalizaría el lector. Es justamente porque se lee fiel que hace falta detectar el estilo del archivo destino y normalizar el interior nuevo a ese estilo (4.3) — si no, el bloque insertado mezclaría estilos con el resto del archivo.
- **El BOM también se juega en el dominio de bytes**: `decode("utf-8")` mantiene el BOM como carácter `\ufeff` al principio del string; como el writer solo reemplaza el interior del bloque, el BOM sobrevive porque vive "afuera". El `lstrip("\ufeff")` en `parse_frontmatter`/`extract_frontmatter_block` (353, 376) es el detalle que permite que el frontmatter se detecte igual en notas con BOM.
- **La consistencia registry↔writer**: la detección de concurrencia solo funciona si el hash del scan y el hash del writer se calculan sobre *la misma representación*. Por eso `registry.py` también lee bytes (líneas 514, 689) — el hallazgo fue sistémico, no solo del writer.

Moral pedagógica: cuando el "dato de verdad" es el archivo en disco, y tus invariantes (hashes, comparación byte a byte) viven sobre ese disco, **toda lectura tiene que ser fiel**. La comodidad de un helper (`read_text`) puede invalidar silenciosamente un sistema de verificación entero si introduce una traducción invisible.

---

## 6. Cómo se conecta con el pseudo-código

La Capa 3 de implementación cubre la **Capa 5 (Escritura segura)** del diseño:

| Pseudo-código (Capa 5) | Implementación (`writer.py`) |
|---|---|
| Flujo de escritura de 11 pasos | `write_concept()` (550-646), pasos numerados 1-9 en los comentarios. |
| Leer en bytes + decodificar UTF-8 | Paso 1 (565-567), `_read_text()` (713-721) — hallazgo read_bytes vs read_text (sección 5). |
| Validar marcadores: exactamente 1/1 en orden | `find_markers` (204-224) + `count_markers` (227-233) + `_raise_marker_error` (770-783). |
| Si faltan marcadores → fallar (no insertar) | Excepciones tipadas; ninguna ruta inserta marcadores. |
| Hash del afuera antes/después | Hash del antes (575-578) + `verify_outside_integrity` (315-337) con `extract_outside` (271-288) + `sha256` (266-268). |
| Byte a byte del afuera (no solo hash) | Segunda fase de `verify_outside_integrity` (332-337). |
| Reemplazo solo del interior; marcadores verbatim | `replace_inside` (236-258) sobre el `MarkerSpan` (193-202). |
| Newlines: detectar y respetar, interior normalizado | `detect_newline` (173-177) + `normalize_newlines` (180-185) + `render_inside` (482-489). |
| Escritura atómica: temp + renombre atómico (mismo FS) | `_atomic_write` (668-678), tmp en `workdir/tmp` (constructor, línea 540). |
| Backup ANTES en `workdir/backups/<id>/` con copy2 | `backup` (650-656), timestamp compacto `now_iso_compact` (85-88). |
| Verificación RELEYENDO desde disco | `_verify` (725-766) sobre `_read_text` (713-721). |
| Falla → restaurar backup byte a byte + failed | `restore` (658-664) + `mark_writing_failed` (832-853); rama de error en 627-637. |
| Frontmatter byte a byte + semántica como red de seguridad | `verify_frontmatter_preserved` (386-409) con `parse_frontmatter` (347-371) y `extract_frontmatter_block` (374-383). |
| Detección de edición concurrente (mtime/hash) | `concurrent_edit_detected` (682-709) + `ConcurrentEditError` (116-117). |
| Dry-run: diff sin escribir ni cambiar estado | `DiffResult` (497-519) + rama dry-run (604-614). |
| Integración con Capa 3: validated → written → completed / failed | `mark_written` (802-816) + `mark_completed` (819-829) + `writing_phase` (856-899); `write_result` en `phase_data` vía `record_write_result` (791-799). |
| Excepciones del writer (familia) | Bloque completo de excepciones (96-165), con `HeadingsChangedError`/`WikilinksChangedError` como agregados. |
| "Que se escribe y que no" / mínimo privilegio | Docstring (1-28) + `replace_inside` + todas las `verify_*`: la implementación le da estructura operativa al enunciado. |

**Agregados de la implementación** que el pseudo-código no detallaba tanto:

- `verify_headings_preserved` (438-453) y `verify_wikilinks_preserved` (469-474), con normalización por acentos: concreta la verificación de "titulo/navegacion/wikilinks siguen presentes" de forma granular y testeable.
- **Pre-check en memoria** del texto nuevo antes de escribir (598-602): el pseudo-código solo pedía verificar después de escribir; agregar el chequeo antes es redundancia barata que descarta bugs antes de tocar disco.
- **Sufijo uuid en el nombre del backup** (línea 85-88): pseudo-código pedía "timestamp compacto"; el uuid evita colisión si se hace backup más de una vez en el mismo segundo.
- **Distinción entre `OSError` de `_atomic_write` y verificación fallida** (619-625 vs 627-637): el primero no restaura (la nota original nunca se tocó), el segundo sí. El pseudo-código no distinguía estos dos modos de falla.
- **Idempotencia en `writing_phase`** (880-881): completado no se re-escribe. El pseudo-código lo dice a nivel del pipeline general; acá se lo reforzó dentro de la fase misma.

Lo que **no** se implementó todavía y va en capas futuras: backend real (Capa 4 del diseño), investigación (6), síntesis (7), validación semántica (8), orchestrador (9), CLI (10). En particular, hoy `writing_phase` espera un objeto `Synthesis` que todavía no se produce en ningún lado — la firma ya está como contrato adelantado para que las capas 6-8 completen el camino.

---

## 7. Decisiones de diseño y por qué

1. **El writer como clase con estado propio (`SafeWriter`), no funciones sueltas.** Costo: una clase más cuando casi todo podría ser funcional. Beneficio: la config (rutas, marcadores) se resuelve una vez en el constructor y los mismos invariantes aplican a todas las llamadas; el orchestrador futuro inyecta un único writer con config conocida, en vez de re-resolver config por cada nota. Mirá cómo `_verify` usa `self.marker_start`/`self.marker_end` en todos los operadores: nadie puede "olvidar" pasarle los marcadores, porque el objeto los lleva consigo.

2. **Leer bytes, escribir bytes (hallazgo central).** Discutido en la sección 5. Costo: un poco más de código y una función `_read_text` que parece trivial. Beneficio: el modelo de integridad (hashes, comparación byte a byte, detección de concurrencia) queda a prueba de la traducción invisible de newlines del runtime.

3. **Doble verificación de integridad: hash + byte a byte.** Costo: verificación redundante. Beneficio: si un bug hashara algo distinto de lo que se comparó byte a byte, la otra capa lo atraparía; y hay un error tipado distinto para cada caso (`OutsideIntegrityError` vs `OutsideByteMismatchError`), lo que da diagnóstico granular. Es el patrón de "dos pruebas que acuerdan" en lugar de una sola que puede fallar sola.

4. **La verificación relee desde disco, no usa el buffer en memoria.** Costo: una lectura más del archivo. Beneficio: la verificación testea el resultado real, no la abstracción. Si el FS devolvió algo distinto de lo que creíste escribir (disco lleno, otro proceso tocó, encoding raro), es *exactamente el caso* donde no querés confiar en tu propia convicción. Disciplina del "quien verifica no puede usar el mismo dato que se está verificando".

5. **Excepciones tipadas con jerarquía.** Costo: 15 clases en vez de `raise ValueError("algo")`. Beneficio: errores accionables sin tratar strings, polimorfismo por tipo (el orchestrador atrapa `VerificationError` como grupo, igual que en Capa 4 se va a atrapar `BackendAuthError` como grupo), y documentación viva de todos los modos de falla en la firma publicada (`__all__`).

6. **`find_markers` devuelve `None` y la clasificación del error es after-the-fact (`_raise_marker_error`).** Costo: un método extra y un patrón de "dos pasos". Beneficio: `find_markers` sirve tanto como función de lectura silenciosa (hashes, dry-run, `_verify` para contar) como para validación explícita; y la clasificación se hace solo ante un fallo real, no en el path feliz.

7. **Pre-check de integridad en memoria antes de escribir.** Costo: doble cómputo de la verificación (porque se repite post-escritura). Beneficio: un bug de reemplazo se descubre sin haber tocado disco, el dry-run hereda la garantía de seguridad, y los backups no se generan al cuete por errores que el pre-check ya habría atrapado.

8. **Backup con `shutil.copy2` que preserva mtime.** Costo: la copia es un poco más lenta que un rename. Beneficio: dos por el precio de uno. (a) El backup es una foto byte a byte del estado previo (no se pierde por el `os.replace`). (b) Que el mtime sobreviva evita que una restauración *parezca* edición concurrente después del hecho (ver nota del docstring del `concurrent_edit_detected`, 691-695).

9. **Duplicación deliberada de `detect_newline`/`content_hash_outside`/`parse_frontmatter` respecto de `registry.py`.** Costo: dos implementaciones que podrían divergir (y de hecho divergen sutilmente, ver 4.3 y 4.6). Beneficio: la capa es **autónoma** (se puede usar y testear sin importar el registry); además, las firmas de API difieren — el writer tiene versiones pensadas para verificación con errores tipados, el registry para scan con valores `None`. Punto de mejora honesto si se nota drift: unificar en un módulo de primitivas de vault cuando madure la capa 6.

10. **`writing_phase` encapsula todo el asunto estado+writer.** Costo: una capa más de indirección (el orchestrador podría llamar ambas piezas directamente). Beneficio: un único punto que encapsula la secuencia completa de la fase (dry-run, fallos, transiciones, persistencia en el momento correcto), lo cual deja al orchestrador futuro una API de alto nivel ("escribime este concepto y manejá el estado") en vez de una secuencia de pasos que podría ejecutar en mal orden.

11. **Contratos adelantados con parámetros sin usar.** (`replace_inside` acepta markers y los marca `del`; `_verify` acepta `new_text`/`concept` y los marca `del`.) Costo: parámetros "muertos" hoy. Beneficio: la firma que se publica hoy es la que va a valer mañana; las capas que llenen esos parámetros no van a necesitar romper el API ni migrar callers.

---

## 8. Referencias rápidas de líneas clave

`writer.py`:

- Docstring del contrato de la capa → líneas 1-28.
- `WRITER_VERSION` → 58. Marcadores default → 60-61. `REQUIRED_HEADINGS` → 64.
- `_cfg` → 67-82. `now_iso_compact` → 85-88.
- Excepciones: `WriterError` 96-97, `VerificationError` 100-101, `MissingMarkersError` 104-105, `DuplicateMarkersError` 108-109, `MarkerOrderError` 112-113, `ConcurrentEditError` 116-117, `OutsideIntegrityError` 120-128, `OutsideByteMismatchError` 131-134, `FrontmatterChangedError` 135-136, `FrontmatterSemanticMismatchError` 139-141, `InsideMismatchError` 143-145, `MarkerCountError` 147-149, `HeadingsChangedError` 151-153, `WikilinksChangedError` 155-157, `WriteFailedError` 159-165.
- `detect_newline` → 173-177. `normalize_newlines` → 180-185.
- `MarkerSpan` → 193-202. `find_markers` → 204-224. `count_markers` → 227-233. `replace_inside` → 236-258.
- `sha256` → 266-268. `extract_outside` → 271-288. `content_hash_outside` → 291-300. `content_hash_inside` → 303-312. `verify_outside_integrity` → 315-337.
- Frontmatter: `_FM_DELIM` → 344, `parse_frontmatter` → 347-371, `extract_frontmatter_block` → 374-383, `verify_frontmatter_preserved` → 386-409.
- Headings: `_accent_less` → 417-422, `_norm_heading` → 425-426, `_heading_texts` → 429-435, `verify_headings_preserved` → 438-453.
- Wikilinks: `_WIKILINK_RE` → 456, `_wikilink_set` → 459-466, `verify_wikilinks_preserved` → 469-474.
- `render_inside` → 482-489.
- `DiffResult` (dry-run) → 497-519.
- `SafeWriter` → 522 (decl.), constructor 525-546.
- `write_concept` → 550-646 (pasos: leer bytes 565-567, marcadores 570-573, hash 575-578, concurrencia 580-590, construir + pre-check 592-602, dry-run 604-614, backup 616-617, escritura atómica 619-625, verificación/restore 627-637, resultado 639-646).
- `backup` → 650-656. `restore` (+ aliases `_backup`/`_restore` conforme al diseño) → 658-664.
- `_atomic_write` → 668-678.
- `concurrent_edit_detected` → 682-709.
- `_read_text` (hallazgo read_bytes vs read_text) → 713-721.
- `_verify` → 725-766.
- `_raise_marker_error` → 770-783.
- Integración estado: `record_write_result` → 791-799, `mark_written` → 802-816, `mark_completed` → 819-829, `mark_writing_failed` → 832-853, `writing_phase` → 856-899.
- `__all__` → 902-946.

`state.py` (lo que el writer consume):

- `ConceptStatus` → líneas 34-46 (usa `VALIDATED`, `WRITTEN`, `COMPLETED`, `FAILED`).
- `VALID_TRANSITIONS` → 60-90 (las rutas `validated → written`, `written → completed`, y `failed`/`needs_review` como terminales operativos que el writer respeta).
- `InvalidTransitionError` → 93-94 (se propaga en `mark_writing_failed`).
- `validate_transition` → 130-137, `transition_to` → 232-268.
- `resolve_workdir` → 276-285.
- `save_state` → 368-421 (persistencia atómica tmp + replace, ya garantizada por la capa 2). `load_state` → 466-499.

`registry.py` (lo que alimenta al writer):

- Lectura de la nota en bytes al scan → 514-519.
- `content_hash_outside` / hash del afuera (consistencia con el writer) → 201-206.
- Persistencia de campos de integridad en `ConceptMeta` → 643-647 (`outside_hash_at_read`, `mtime_at_read`, `newline`, etc.), clave para `concurrent_edit_detected`.

`models.py` (contratos pertinentes):

- `ConceptMeta` (integridad: `outside_hash_at_read`, `mtime_at_read`, `content_hash_outside`, `newline`) → líneas 71-112.
- `Synthesis` (lo que el writer inserta) → 233-252.
- `WriteResult` (contrato adelantado del resultado) → 307-318.
- `now_iso` → 348-349.

Config y estructura del proyecto:

- `config.yaml`: `workdir` → línea 5; `markers.start`/`markers.end` → 14-16.
- `README.md`: módulos y reglas actualizados a Capa 3 → líneas 5-6 (introducción), 14-16 (estructura), 32-43 (módulo writer), 70-74 (reglas del writer), 78-80 (estado de la implementación).
- Referencia conceptual del diseño: `explicacion del proyecto por capas v1.md` → Capa 5 (línea 843 en adelante); pseudo-código de la capa: `explicacion del proyecto por capas v1 - pseudo codigo.md` → Capa 5 (línea 264 en adelante).

---

## 9. Qué sigue (para ubicar esta capa en el roadmap)

Esta capa cierra el ciclo "leer → luego escribir" con integridad garantizada. Las capas que vienen se van a conectar así:

- **Capa 4 (backend)** producirá las fuentes crudas; el writer le es ajeno (no la conoce).
- **Capa 6 (investigación)** y **Capa 7 (síntesis)** irán llenando el camino restante: producirán el `Synthesis` que `writing_phase()` ya espera (firma adelantada).
- **Capa 8 (validación)** será el filtro antes del writer: es quien decide si el `Synthesis` está "validado" o no; el writer asume "ya validado" por contrato.
- **Capa 9 (orchestrador)** llamará `writing_phase()` por concepto; usará el `WriteResult` que se persiste en `phase_data` y las excepciones tipadas para decidir reintentos.
- **Capa 10 (CLI)** expondrá `--dry-run` a nivel humano, que el writer ya soporta vía `dry_run=True` y `DiffResult.unified_diff()`.

Mientras esas capas no existan, `writer.py` ya permite: escribir de forma atómica con backup y verificación, diagnosticar todas las fallas de la escritura con precisión, detectar concurrencia, y ensayar el flujo completo con dry-runs — base suficiente para que las capas de generación de contenido se conecten y produzcan una escritura ya probada.
