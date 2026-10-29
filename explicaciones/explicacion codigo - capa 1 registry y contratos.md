# Explicación del código — Capa 1: registry + contratos

> Documento educativo. Explica, con palabras, qué se implementó en la **Capa 1 de implementación** del proyecto `it-concept-map`, cómo se tradujo el pseudo-código de las Capas 1 y 2 del diseño técnico a código real, y por qué se tomó cada decisión. No copia bloques de código: solo referencia módulos y líneas clave.

Proyecto: `C:\Users\DGVit\Proyectos\IT Career\it-concept-map\`
Vault de origen: `C:\Users\DGVit\Proyectos\IT Career\IT-Mind-Map\` (notas `.md` con bloque `<!-- ai:start --> ... <!-- ai:end -->`)

---

## 1. Qué es la Capa 1 y por qué va primero

La Capa 1 es la **base del pipeline**: define qué es un "concepto" y cómo se lee del vault. Es el átomo sobre el que se construye todo lo demás (estados, backend, writer, investigación, síntesis, validación, orquestador, CLI). Si esta capa está mal, todo lo que viene después hereda el error.

En el pseudo-código, la Capa 1 se llama "Modelo de datos (ConceptMeta)" y la Capa 2 "Vault como fuente de verdad (vault.py)". En la implementación real se fusionaron en una sola entrega porque son inseparables: el modelo (`ConceptMeta`) solo tiene sentido si hay algo que lo materializa leyendo el vault (`registry.py`). Por eso el README del proyecto dice explícitamente: "Capa 1 de implementación: registry + contratos de datos".

Decisión clave: **el registry solo lee**. No escribe en el vault ni en el workdir. Eso mantiene el principio de mínimo privilegio: la única pieza que escribe en el vault será el writer (Capa 5, pendiente).

---

## 2. Archivos creados

Todos viven en `it-concept-map\`:

| Archivo | Rol |
|---|---|
| `models.py` | Los contratos de datos: dataclasses con `schema_version`, enums, excepciones de la capa y helpers de serialización. |
| `registry.py` | La materialización: descubre notas del vault, las parsea, deriva un `ConceptMeta` por nota, calcula hashes. |
| `config.yaml` | Configuración base: rutas, glob/exclude, marcadores, backend, volatilidad por área, estrategia de fuentes, validación. |
| `pyproject.toml` | Metadatos del proyecto Python (nombre, versión, dependencias, pytest). |
| `README.md` | Documentación de la capa y uso rápido. |

Además se generó `__pycache__\` (artefacto de Python, no fuente) y el `workdir\` se declara en config pero se crea recién cuando otras capas lo usen.

---

## 3. `models.py` — los contratos de datos

Archivo: `it-concept-map\models.py` (396 líneas).

### 3.1. Versión de esquema (`SCHEMA_VERSION`)

Línea 20: `SCHEMA_VERSION = "1.0.0"`. Toda dataclass de la capa lleva un campo `schema_version` con este valor (por ejemplo `ConceptMeta.schema_version`, línea 111). La idea: los artefactos persistidos (sources.json, raw_research.json, synthesis.json, validation.json, estado.json) quedan versionados. Si mañana cambia la estructura de un artefacto, se puede invalidar caches viejos comparando la versión. Es el mismo concepto que el pseudo-código llama "versionado de artefactos".

### 3.2. Enums

Líneas 27-64:

- `Volatility` (línea 28): `STABLE`, `SEMI_STABLE`, `DYNAMIC`. Determina la ventana de frescura de la investigación (90/30/7 días). Se deriva del área + tags con override en config.
- `ConceptStatus` (línea 36): los 8 estados del pipeline (`PENDING` … `BLOCKED`). Es el enum que la Capa 3 (estados) va a usar; ya se define acá para que todo el pipeline hable el mismo idioma.
- `Severity` (línea 49): `ERROR` / `WARN`, para los chequeos de validación (Capa 8).
- `PromptContext` (línea 56): `FRONTEND`, `BACKEND`, `DATA`, `INFRA`, `GENERAL`, para seleccionar prompts en la síntesis (Capa 7).

Definirlos en la Capa 1 evita que cada capa posterior invente su propio enum (drift entre módulos). Es la "única fuente de verdad del modelo" que exige el pseudo-código.

### 3.3. `ConceptMeta` — el átomo

Líneas 71-112. Es la dataclass central: la ficha de un concepto que circula por todo el pipeline. Agrupa:

- Identidad y ubicación: `id`, `title`, `area`, `note_path` (líneas 76-79).
- Aliases y metadatos crudos: `slug`, `numero`, `aliases`, `tags` (82-85).
- Contenido manual del autor: `key_ideas`, `connections` (88-89). Son la "voz del autor" y nunca se sobrescriben.
- Frontmatter crudo: `frontmatter` (92).
- Clasificación y estrategia: `volatility`, `professional_roles`, `preferred_domains`, `seed_urls` (95-98). Vienen de config/overrides, no de la nota.
- Trazabilidad de lectura: `has_ai_block`, `content_hash_outside`, `content_hash_inside`, `outside_hash_at_read`, `mtime_at_read`, `newline`, `has_frontmatter`, `has_bom`, `concept_dir` (101-109).

La docstring (línea 73) lo deja claro: "única representación compartida por el pipeline". Esto coincide con el pseudo-código: "Es la única estructura que el resto del pipeline consume".

Decisión de diseño: `ConceptMeta` es un dataclass normal (no `frozen`), pero se trata como inmutable en espíritu: se deriva en el scan y no se modifica después. Si la nota cambia, se re-deriva. No se hizo frozen porque las capas futuras (escritura) necesitan adjuntar resultados; pero la convención es no mutarlo.

### 3.4. Contratos de las capas futuras (definidos ya, para no redefinirlos después)

El mismo `models.py` declara los DTOs que las capas 5-8 van a usar, para que el contrato esté fijado desde ahora:

- Investigación (líneas 119-199): `Source`, `ResearchQuestion`, `ResearchPlan`, `Claim`, `ResearchAnswer`, `RawResearch`.
- Síntesis (líneas 207-252): `CrossLink`, `ClaimRef`, `Synthesis`.
- Validación (líneas 260-295): `CheckResult` (alias `Check`), `ValidationReport` (alias `ValidationResult`).
- Escritura (líneas 307-318): `WriteResult`.
- Estado (líneas 326-340): `ConceptState`.

Esto es deliberado: la regla de dependencia del pseudo-código dice "ninguna capa puede redefinir ConceptMeta; si se necesita un campo nuevo, se agrega acá y se propaga". Se extendió la misma regla a todos los DTOs del pipeline. Así, cuando se implementen las capas siguientes, ya tienen los contratos listos y no hay riesgo de drift.

### 3.5. Helpers (líneas 344-372)

- `now_iso()`: timestamp ISO-8601 en UTC.
- `sha256_text()`: hash de texto (primitiva reutilizable).
- `to_dict()`: serializa cualquier dataclass a dict, convirtiendo `Path` y `Enum` a valores serializables. Es lo que permite persistir `ConceptMeta`/`ConceptState` a JSON (estado.json, etc.) sin escribir código de serialización en cada capa.

### 3.6. Excepciones de la capa (líneas 375-396)

Jerarquía base para errores del modelo:

- `ConceptModelError` (base)
- `MissingRequiredFieldError` — title/area no derivables.
- `InvalidFrontmatterError` — YAML inválido en frontmatter.
- `UnknownAreaError` — área no reconocida (solo si config lo exige).
- `InvalidVolatilityError` — volatilidad fuera del enum.

Estas son las únicas excepciones que el registry puede lanzar por problemas de modelo. El pseudo-código las lista idénticas en la sección "Excepciones de la capa".

---

## 4. `registry.py` — materialización desde el vault

Archivo: `it-concept-map\registry.py` (722 líneas). Es el corazón de la Capa 1/2 implementada.

### 4.1. Constantes y helpers de config (líneas 32-88)

- Marcadores por defecto: `MARKER_START_DEFAULT = "<!-- ai:start -->"`, `MARKER_END_DEFAULT = "<!-- ai:end -->"` (líneas 32-33). Coinciden con el pseudo-código (Capa 5).
- Headings por defecto para key_ideas y connections (líneas 35-49): listas de alias en minúsculas ("que abarca", "que cubre", … / "relacionados", "conexiones", …). Se normalizan sin acentos para tolerar variaciones.
- `DEFAULT_EXCLUDE_GLOBS` (línea 51): excluye índices (`00 - *`), archivos que empiezan con `_` y READMEs.
- `_cfg()` (líneas 59-74): acceso seguro a config, acepta dict u objeto, con fallback. Permite que la misma función sirva para config YAML (dict) o para objetos de config futuros.
- `_markers()` (líneas 77-88): resuelve los marcadores desde config con varios nombres posibles (`markers.start`, `marker_start`), cayendo al default. Flexibilidad sin romper.

### 4.2. Normalización de texto (líneas 95-116)

- `_strip_accents()`: normalización NFKD para comparar headings ignorando tildes.
- `_norm_heading()`: strip + lower + sin acentos.
- `slugify_path()`: convierte el path relativo al vault en el `concept_id` (slug). Minúsculas, espacios→`-`, mantiene números, colapsa guiones. Es la regla "id = slug del path" del pseudo-código. Estable mientras el path no cambie.

### 4.3. Lectura de archivo (líneas 124-215)

- `detect_newline()` (124-127): detecta CRLF vs LF del archivo original. Se respeta en la escritura futura.
- `has_bom_bytes()` (130-131): detecta BOM UTF-8. Se preserva (no se elimina) para no romper el vault.
- `parse_frontmatter()` (134-166): extrae el bloque YAML entre `---`. Usa `yaml.safe_load`. Si es inválido lanza `InvalidFrontmatterError`. Si no hay cierre válido, trata como "sin frontmatter" (no falla).
- `find_markers()` (169-188): busca exactamente un `ai:start` y un `ai:end`, en ese orden. Devuelve `None` si no es válido (0, 2+, o orden invertido). Es la primitiva de integridad de la Capa 5.
- `extract_outside()` (191-198): todo el archivo excepto el interior del bloque (marcadores incluidos en el "afuera").
- `content_hash_outside()` / `content_hash_inside()` (201-214): SHA-256 del afuera / interior. `None` si no hay bloque. Implementan la primitiva de integridad que el pseudo-código define en la Capa 1 (sección "Content hash") y que la Capa 5 (writer) y Capa 8 (validación) van a usar.

### 4.4. Extracción de contenido estructurado (líneas 222-347)

- `_section_lines()` (222-249): devuelve las líneas que pertenecen a una sección cuyo heading normalizado está en la lista dada. La sección termina en el siguiente heading de nivel ≤ 2. Incluye sub-headings.
- `extract_key_ideas()` (252-275): bullets bajo "Que abarca" (o alias). Dedup preservando orden. Solo toma bullets; texto suelto no se toma como idea. Si no hay sección → `[]`.
- `_extract_wikilinks()` (278-299): regex `\[\[...\]\]`, normaliza target/display, quita `.md`, dedup.
- `extract_connections()` (302-347): si existe sección "Relacionados", extrae wikilinks de sus bullets; si no, fallback a todos los wikilinks del cuerpo excepto índices (`_`, "indice", "00 ") y la propia nota. Esto implementa la regla del pseudo-código: "Si no existe el heading → todos los wikilinks excepto índices y la propia nota".

### 4.5. Derivación de metadatos (líneas 355-510)

- `_first_h1()`, `_title_from_filename()`: fallbacks de título (H1 → nombre de archivo sin prefijo numérico).
- `_area_from_path()`: primera carpeta del path relativo al vault (limpiando prefijo numérico).
- `_default_volatility()`, `_resolve_volatility()`: resuelven volatilidad con prioridad concept override > area override > tags > mapping por área > default `semi_stable`. Coincide con "override por concepto > override por área > … > defaults".
- `_resolve_list_override()`: resuelve listas (`professional_roles`, `preferred_domains`, `seed_urls`) con la misma prioridad (concept > area > area_* map > global > strategy nested) + dedup. Es la implementación de la tabla de derivación del pseudo-código.

### 4.6. `read_concept()` (líneas 512-651)

Es la función que materializa un `ConceptMeta` a partir de una nota. Sigue exactamente el pseudo-código de "Lectura de un concepto (read_concept)" de la Capa 2:

1. Lee bytes y decodifica UTF-8 (línea 514-516).
2. Detecta BOM y newline (515, 519).
3. Parsea frontmatter (523).
4. Deriva título: frontmatter → H1 → nombre de archivo (528-536).
5. Deriva área: frontmatter → primera carpeta (538-545).
6. Extrae tags/aliases/numero (547-562).
7. Extrae key_ideas y connections con headings configurables (563-576).
8. Calcula marcadores y hashes (578-582).
9. Calcula concept_id = slug del path (584-589).
10. Resuelve overrides (volatility, roles, domains, seeds) (591-611).
11. Calcula concept_dir a partir de workdir (612-619).
12. Captura mtime (620-624).
13. Devuelve `ConceptMeta` (626-651).

Si falta title o area no derivables → `MissingRequiredFieldError` (líneas 536, 545). Si el frontmatter es inválido → `InvalidFrontmatterError` (desde `parse_frontmatter`). Esto implementa "Si falta un campo obligatorio no derivable → failed, sin procesar".

### 4.7. `scan_vault()` (líneas 654-708)

Implementa "Descubrimiento de notas (scan)" del pseudo-código de la Capa 2:

1. Resuelve vault_root (660).
2. Toma exclude_globs de config o default (661-663).
3. Toma include_glob de config (664-666).
4. Recorre `vault_root.glob(glob_pattern)` (668-681), excluyendo según exclude_globs.
5. Para cada archivo: si tiene bloque válido → es concepto (lee metadatos con `read_concept`); si no → nota sin bloque (683-708).
6. Detecta colisión de `concept_id` → `ConceptModelError` fatal (703-705). Es la regla "id único; colisión → error fatal del scan".
7. Devuelve `(conceptos, notas_sin_bloque)`.

`load_concepts()` (719-722) es un wrapper de conveniencia que devuelve solo la lista de conceptos.

### 4.8. `_glob_match()` (711-716)

Match simple de glob con soporte de `**`, usando `fnmatch`. Se usa para los exclude_globs.

---

## 5. `config.yaml` — la configuración base

Archivo: `it-concept-map\config.yaml` (122 líneas). Es el "panel de control" de la Capa 1 y prefigura las capas futuras:

- `vault_path` y `workdir` (líneas 4-5): dónde leer y dónde escribir artefactos.
- `include_glob` / `exclude_globs` (8-12): descubrimiento de notas.
- `markers.start` / `markers.end` (14-16): marcadores del bloque autorizado.
- `backend` (18-33): provider (`fake` por ahora) y timeouts. Ya se configura el backend fake para desarrollo sin red (alineado con Capa 4).
- `pacing` (35-39): backoff y reintentos (Capa 3/9).
- `key_ideas_headings` / `connections_headings` (41-54): aliases de secciones.
- `area_overrides` (56-64): volatilidad por área.
- `area_domains` / `area_roles` (66-81): dominios preferidos y roles por área.
- `concepts` (82-89): overrides por concepto (vacío por ahora).
- `strategy` (91-103): seeds, dominios bloqueados, max/min sources, ventanas de frescura por volatilidad.
- `validation` (104-122): strict_mode, required_sections, min_words por sección.

Decisión: toda la configuración de las 11 capas vive en un solo archivo desde el día 1, aunque muchas secciones (backend, pacing, validation) no se usen hasta que se implementen esas capas. Esto evita tener que "inventar" config después y mantiene un único lugar donde mirar cómo se comporta el sistema.

---

## 6. `pyproject.toml` y `README.md`

- `pyproject.toml`: nombre `it-concept-map`, versión `0.1.0`, requiere Python ≥3.11, dependencia `pyyaml>=6.0`, opcional `pytest`. Declara `py-modules = ["models", "registry"]` y `testpaths = ["tests"]`. Es el mínimo para que el proyecto sea instalable/testeable.
- `README.md`: documenta estructura, módulos, uso rápido (`load_concepts`), reglas seguidas y estado ("Capa 1 implementada. Capas siguientes pendientes"). Es la "tarjeta de presentación" de la capa.

---

## 7. Cómo se conecta con el pseudo-código

El pseudo-código define 11 capas. La Capa 1 de implementación cubre la **materialización** de las Capas 1 y 2 del pseudo-código:

| Pseudo-código | Implementación |
|---|---|
| Capa 1 — Modelo de datos (`ConceptMeta`) | `models.py`: `ConceptMeta` (líneas 71-112), enums, excepciones. |
| Capa 1 — Reglas de derivación de campos | `registry.py`: `read_concept()` (512-651) + helpers de derivación (355-510). |
| Capa 1 — Content hash (outside/inside) | `registry.py`: `content_hash_outside()` (201-206), `content_hash_inside()` (209-214), `extract_outside()` (191-198), `find_markers()` (169-188). |
| Capa 2 — Lectura de una nota | `registry.py`: `read_concept()` + `parse_frontmatter()` (134-166) + `detect_newline()` (124-127) + `has_bom_bytes()` (130-131). |
| Capa 2 — Descubrimiento de notas (scan) | `registry.py`: `scan_vault()` (654-708) + `load_concepts()` (719-722). |
| Capa 2 — Extracción de key_ideas/connections | `registry.py`: `extract_key_ideas()` (252-275), `extract_connections()` (302-347), `_section_lines()` (222-249). |
| Capa 2 — id = slug del path | `registry.py`: `slugify_path()` (105-116). |

Lo que **no** se implementó todavía (y está pendiente) son las Capas 3-11 del pseudo-código: estados, backend, writer, investigación, síntesis, validación, orquestador, CLI, piloto. El README lo deja explícito: "Capas siguientes (estados, backend, writer, investigación, síntesis, validación, orquestador, CLI) pendientes."

Sin embargo, los **contratos** de esas capas futuras ya están definidos en `models.py` (Source, ResearchQuestion, RawResearch, Synthesis, CheckResult, ValidationReport, WriteResult, ConceptState). Esa es la "inversión" de la Capa 1: fijar los contratos ahora para que las capas siguientes no los redefinan.

---

## 8. Decisiones de diseño y por qué

1. **Fusionar Capa 1 y Capa 2 del pseudo-código en una sola entrega.** El modelo sin lector es abstracto; el lector sin modelo no tiene salida. Separarlos habría obligado a definir interfaces entre dos archivos que se escriben juntos. Se priorizó coherencia sobre pureza de capas.

2. **El registry solo lee.** Ninguna función de `registry.py` escribe en disco. Esto respeta el principio de mínimo privilegio y evita que una capa de lectura pueda corromper el vault por accidente.

3. **Prioridad de derivación consistente.** En todo el registry se usa la misma cadena: override por concepto > override por área > frontmatter > cuerpo > defaults. `_resolve_volatility()` y `_resolve_list_override()` la implementan. Esto hace predecible el comportamiento y coincide con el pseudo-código.

4. **Hashes sobre texto crudo (con newlines originales).** `content_hash_outside()` y `content_hash_inside()` hashean el texto tal como está en disco, respetando CRLF/LF. No se normaliza antes de hashear. Así el hash detecta cualquier cambio real, incluyendo cambios de newline.

5. **BOM preservado, no eliminado.** `has_bom_bytes()` solo detecta; `read_concept()` quita el BOM solo para parsear internamente, pero el flag `has_bom` queda en `ConceptMeta`. La escritura futura sabrá que debe preservarlo.

6. **Colisión de id = error fatal.** `scan_vault()` lanza `ConceptModelError` si dos notas generan el mismo `concept_id`. No se intenta desambiguar automáticamente: es mejor fallar fuerte que procesar el concepto equivocado.

7. **Fallbacks explícitos, nunca silenciosos.** Si falta title → H1 → nombre de archivo; si falta área → primera carpeta. Si ninguna fuente da valor → `MissingRequiredFieldError`. Cada fallback está documentado en el código y en el pseudo-código.

8. **Configuración adelantada.** `config.yaml` incluye secciones de capas no implementadas (backend, pacing, validation). Costo: un archivo más largo. Beneficio: un único lugar de verdad para todo el sistema, y las capas futuras no tienen que "inventar" claves.

9. **Contratos adelantados en `models.py`.** Se definieron DTOs de capas 3-8 ahora. Costo: código que aún no se usa. Beneficio: cuando se implementen esas capas, el contrato ya está fijado y no hay drift.

10. **Python ≥3.11 y `pyyaml` como única dependencia.** Minimiza fricción de instalación y mantiene el proyecto testeable con pytest sin dependencias pesadas.

---

## 9. Referencias rápidas de líneas clave

`models.py`:
- `SCHEMA_VERSION` → línea 20.
- Enums → líneas 27-64.
- `ConceptMeta` → líneas 71-112.
- `RawResearch` → líneas 178-199.
- `Synthesis` → líneas 233-252.
- `ValidationReport`/`ValidationResult` → líneas 280-295.
- `ConceptState` → líneas 326-340.
- `to_dict` → líneas 356-372.
- Excepciones → líneas 379-396.

`registry.py`:
- Constantes y helpers de config → líneas 32-88.
- `slugify_path` → líneas 105-116.
- `parse_frontmatter` → líneas 134-166.
- `find_markers` → líneas 169-188.
- `content_hash_outside` / `content_hash_inside` → líneas 201-214.
- `extract_key_ideas` → líneas 252-275.
- `extract_connections` → líneas 302-347.
- `_resolve_volatility` → líneas 421-457.
- `_resolve_list_override` → líneas 459-510.
- `read_concept` → líneas 512-651.
- `scan_vault` → líneas 654-708.
- `load_concepts` → líneas 719-722.

`config.yaml`:
- `vault_path` / `workdir` → líneas 4-5.
- `markers` → líneas 14-16.
- `area_overrides` → líneas 56-64.
- `strategy.freshness_window_days` → líneas 99-103.
- `validation.required_sections` → líneas 107-114.

---

## 10. Qué sigue (para ubicar esta capa en el roadmap)

Esta capa deja listo el "átomo" y el "lector". Las siguientes capas del pseudo-código (3-11) se apoyan en ella:

- Capa 3 (estados) consumirá `ConceptState` y `ConceptStatus` de `models.py`.
- Capa 4 (backend) consumirá `ConceptMeta`, `Source`, `ResearchQuestion`, `ResearchPlan`, `Claim`.
- Capa 5 (writer) consumirá `ConceptMeta`, `WriteResult`, y las primitivas `find_markers`, `content_hash_outside`, `content_hash_inside`, `detect_newline`.
- Capa 6 (investigación) consumirá `RawResearch` y `ConceptMeta`.
- Capa 7 (síntesis) consumirá `Synthesis` y `PromptContext`.
- Capa 8 (validación) consumirá `CheckResult`, `ValidationReport`, `Severity`.

Mientras esas capas no existan, el proyecto solo puede **leer y describir** el vault: `load_concepts(cfg["vault_path"], cfg)` devuelve la lista de `ConceptMeta` con todos sus campos derivados. Eso ya es suficiente para inspeccionar el vault, contar conceptos, ver áreas, ideas clave y conexiones, y verificar que los hashes se calculan correctamente — base para empezar a construir el resto.
