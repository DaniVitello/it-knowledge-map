# Explicacion del codigo — v2 Capa L1: inventario y parseo (C0–C1)

> Documento educativo. Explica, con palabras, qué es la **capa L1** de IT Knowledge Map v2, cómo se tradujo el pseudocódigo de las etapas C0 y C1 a código real, y por qué se tomó cada decisión. No copia bloques de código: solo referencia módulos y funciones clave.
>
> Proyecto: `C:\Users\DGVit\Proyectos\IT Career\ikm\` · Rama: `v2/L1-contenido` · Commit: `90373af`
> Diseño de referencia: `IT_Knowledge_Map_v2_Technical_Pipeline_Design.md` §6.1, §6.2 (C0–C1), §22.2.
> Pseudocódigo de referencia: `IT_Knowledge_Map_v2_Pseudocode_por_Capas.md` capa 1.

---

## 1. Que es L1 y que resuelve

L1 es la **entrada del plano de contenido**: lee el vault (solo lectura) y produce dos cosas — un **inventario** de todo lo que existe (C0) y el **parseo estructural** de cada nota (C1). Todavía no decide qué se publica, ni resuelve links, ni asigna identidades: eso es L2 (C2–C3) y L4 (C7–C9).

El objetivo del pseudocódigo es explícito: *"producir el inventario clasificado y el parseo estructural de la Knowledge Base, sin decidir publicación ni resolver links"*.

Las dos etapas:

- **C0 — Inventario y clasificación.** Recorre el vault y el material crudo del Journey. Cada elemento nace `private`. Los escaneos producen **señales**, nunca decisiones. Reporta cobertura y señales.
- **C1 — Parseo de la Knowledge Base.** Clasifica las **zonas** de cada nota, extrae las 10 secciones del contrato de v1, registra las **marcas de verificación** y cosecha los **WikiLinks** con su posición y su oración.

### El relevamiento que sustenta la capa

Antes de codear se relevó el vault real (255 conceptos + 11 índices, 266 `.md` en total):

| Dato | Valor |
|---|---|
| Notas de concepto | 255 |
| Índices excluidos por config | 11 |
| Con el bloque `ai:start`/`ai:end` | 255 |
| Con las 10 secciones completas | **255** |
| Sin secciones del contrato | **0** |
| Wikilinks en `Relacionados` | 940 |
| Wikilinks de navegación (blockquote) | 255 |
| Wikilinks de pie (prev/next) | 725 |
| Marcas de verificación | 37 |

El vault fue recuperado por el autor durante esta capa: las 255 notas tienen ahora las 10 secciones. La segunda sección se llama **`## Ideas clave`** (antes `## Esqueleto`); el contrato la nombra `ideas_clave` y acepta `esqueleto` como variante legacy. C1 sigue tolerando estructura variable: lo que no encuentra va a `sections_missing` como **reporte**, no como aborto.

---

## 2. Archivos creados

| Archivo | Rol |
|---|---|
| `content/__init__.py` | Docstring del plano de contenido. |
| `content/publish_config.py` | `PublishConfig`: inclusión/exclusión, zonas publicables, secciones del contrato y sus variantes, patrones de escaneo. |
| `content/schemas.py` | Esquemas Pydantic de salida de C0 y C1 (`Inventory`, `InventoryItem`, `ParsedConcept`, `Zone`, `WikiLink`, `VerificationMark`, `RunLog`). |
| `content/inventory.py` | **C0**: `C0_inventario`. |
| `content/parse.py` | **C1**: `_zonas_de`, `_wikilinks_de`, `_secciones_de`, `C1_parseo`. |
| `content/pipeline.py` | Reglas comunes L1.0: solo lectura verificada, idempotencia, determinismo, guardado atómico, `run.json`. |
| `content/cli.py` | CLI `ikm inventory` / `ikm parse`. |
| `fixtures/vault/` | Vault sintético (7 notas) con los casos de parseo. |
| `tests/test_l1_content.py` | 15 tests. |

---

## 3. Reglas comunes (L1.0) — `pipeline.py`

El pseudocódigo define seis reglas que aplican a **todo** el pipeline de contenido (L1–L4). Se implementaron una sola vez, en `ContentRunner` + `ejecutar_etapa`:

1. **Solo lectura sobre el vault.** `hash_arbol_vault()` antes y después; si difiere, `AbortStage("vault_modified")`.
2. **Idempotencia.** `clave_cache(entrada, version_etapa, hash_config)`; si la clave ya está, la etapa se omite (`cache_hit=True`).
3. **Validación de la salida** contra el esquema de la etapa.
4. **Solo lectura verificada** (el hash del vault otra vez, después de ejecutar).
5. **Determinismo.** `escribir_json_atomico` con `sort_keys=True`; sin marcas de tiempo en los artefactos de contenido.
6. **`run.json`** con etapas, hashes, duraciones, warnings y errores. Es la traza de la corrida.

`ContentRunner` mantiene `workdir/run.json` y `workdir/parsed/*.json`. `workdir/` está en `.gitignore` (es estado, no fuente).

---

## 4. C0 — `inventory.py`

### 4.1 Contrato de entrada y salida

`C0_inventario(config: PublishConfig) -> Inventory`. Si `vault_root` está vacío o el config no existe, aborta con `invalid_config`. Por cada archivo: `id_temporal`, `hash_de_ruta`, `tipo`, `sha256`, `clasificacion="private"` y `signals[]`.

El punto de diseño: **todo elemento nace `private`**. La publicación se decide en C5/C7, nunca en el inventario. Es la materialización de "publicación negada por defecto".

### 4.2 Escaneos que producen señales, no decisiones

`_senales_de_texto()` aplica, sobre el texto de cada `.md`:

- `config.scan_patterns`: secretos y tokens (`BEGIN PRIVATE KEY`, `AKIA…`, `sk-…`, `ghp_…`, `AIza…`).
- Emails, teléfonos, rutas absolutas (`/Users/…`, `/home/…`), rutas de sistema Windows (`C:\Users\…`).
- URLs privadas (`localhost`, `127.0.0.1`, `192.168.*`, `10.*`).

Cada coincidencia es un `ScanSignal(kind, excerpt)`. **No clasifica ni excluye**: C7 decide. En el vault real, 20 notas tienen señales.

### 4.3 Verificación de solo lectura

`hash_arbol_vault()` se calcula antes y después de recorrer. Si cambió, `AbortStage("vault_modified")`. Es la garantía de que el pipeline no escribe en el vault.

---

## 5. C1 — `parse.py`

### 5.1 Zonas de la nota

`_zonas_de(cuerpo, config)` clasifica la nota. Es la pieza más delicada, porque de ella depende **qué wikilinks cuentan como relaciones conceptuales** (C3) y qué texto es publicable.

Zonas detectadas: `titulo` (H1), `navegacion` (blockquote `> **Área:** …`), `que_abarca` (`## Qué abarca`), `mis_notas` (`## Mis notas`), `relacionados` (`## Relacionados`), `bloque_ai` (entre `<!-- ai:start -->` y `<!-- ai:end -->`), `pie` (línea `← [[…]] · [[…]] →`), y `otro`.

Dos decisiones de implementación que importan:

- **El bloque AI es una zona única.** Los encabezados `## Objetivo`, `## Conexiones`, etc. que están dentro del bloque **no generan zonas propias**: están cubiertos por `bloque_ai`. La sección semántica se resuelve aparte con `_seccion_de(cuerpo, offset)` (el `##` más cercano antes del offset).
- **Las zonas se solapan** (`mis_notas` abarca hasta el siguiente `##`, que puede estar dentro del bloque AI). `_zona_de_offset` desempata por prioridad: `relacionados > que_abarca > bloque_ai > mis_notas > otro > navegacion > pie > titulo`. Sin eso, un wikilink dentro del bloque AI caería en `mis_notas` y se perdería.

Zonas que **nunca** se publican (constante `ZONAS_SIEMPRE_EXCLUIDAS`, no configurable): `navegacion`, `pie`, `mis_notas`, `frontmatter`, `titulo`. Por defecto son publicables `bloque_ai`, `relacionados` y `que_abarca`.

### 5.2 Secciones del contrato y variantes

`_secciones_de(bloque_ai)` extrae las 10 secciones del contrato del bloque AI. Solo los encabezados que mapean a una sección canónica **abren** una sección: los subtítulos `##` internos (`## Uso`, `## Metricas`, ejemplos de código) quedan dentro del texto de la sección vigente y no la truncan. `_canon_seccion()` normaliza tildes y sufijos entre paréntesis; `## Ideas clave` mapea a `ideas_clave`. Lo que no encuentra va a `sections_missing`, que es un **reporte**, no un aborto.

### 5.3 WikiLinks con posición y oración

`_wikilinks_de()` recorre `[[…]]` y, por cada uno:

- **ignora** los que están dentro de bloques de código (` ``` … ``` `);
- **descarta** los de zonas no publicables (navegación, pie, Mis notas);
- registra `destino_textual`, `alias`, `heading`, `seccion` (el `##` que lo contiene), `oracion` (la oración o línea que lo contiene), `offset` y `zona`.

El resultado sobre el vault real:

| Zona | Wikilinks | ¿Publicable? |
|---|---|---|
| `relacionados` | 940 | sí |
| `navegacion` (blockquote) | 255 | no |
| `pie` (prev/next) | 725 | no |
| sin zona / otro | 23 | no |

Es decir: **940 relaciones conceptuales**, que es exactamente lo que C3 va a resolver. Los 980 de navegación y pie quedan fuera, como manda la decisión de encuadre del informe de aplicabilidad.

### 5.4 Marcas de verificación

`_marcas_de()` registra `sin verificar` y `⚠️ verificar` **por sección**, con la sección `##` que los contiene. **Nunca los stripea**: son señales de integridad de la spec. En el vault real: 35 marcas, todas `sin verificar` (coherente con el relevamiento previo).

### 5.5 Abortas de C1

- `invalid_frontmatter`: el frontmatter no existe o no parsea como YAML.
- `unresolvable_title`: no hay `title` en frontmatter ni `# Título` en el cuerpo.
- `unreadable_file`: el archivo no se puede leer.

---

## 6. CLI

`ikm/content/cli.py` expone dos comandos por ahora (en L4 se suma `ikm release build`):

```
.venv/Scripts/python.exe -m ikm.content.cli inventory
.venv/Scripts/python.exe -m ikm.content.cli parse
```

`parse` requiere `inventory.json` en el `workdir`? No: recorre el vault con `_iter_archivos` (el inventario es la fuente de verdad de *qué existe*, pero el parseo no depende de re-ubicar por hash, que era O(n²)).

---

## 7. Verificación ejecutada

**Tests** (venv `.venv/Scripts/python.exe`):

```
.venv/Scripts/python.exe -m pytest ikm/tests/test_l1_content.py -q
40 passed (22 L0 + 18 L1)
```

Cubren: inventario y clasificación `private`, no modificación del vault, detección de señales, exclusión de índices, config inválida, parseo completo, secciones ausentes, variantes de título, wikilinks con oración y exclusiones, marcas por sección, fuentes, zonas publicables/excluidas, frontmatter inválido, título no resoluble y round-trip del esquema.

**Ejecución real sobre el vault** (laptop 1):

```
inventory: 255 elementos | por_tipo={'markdown': 255} | con_senales=64
  01 - Software Engineering: 30
  02..10: 25 c/u
parse: 255 notas | wikilinks=940 | marcas=37 | completas=255 | sin_secciones=0
vault intacto: True
```

---

## 8. Criterios de aceptación

- [x] cada concepto del release proviene de una nota del inventario — el inventario es la fuente de verdad; C7 (L4) verifica el vínculo.
- [x] el vault no cambia (hashes) — `hash_arbol_vault` antes/después en C0 y en cada etapa.
- [x] marcas de verificación registradas por sección — `_marcas_de`, 37 reales.
- [x] WikiLinks con posición y oración — 940 reales, con `offset` y `oracion`.
- [ ] pipeline C0–C9 completo sobre el vault sintético — **pendiente L2–L4**.

---

## 9. Qué NO hace L1

- No decide publicación (C5/C7).
- No resuelve links ni asigna identidades (C2/C3).
- No tipifica ni explica relaciones (C4).
- No toca el vault.
- No juzga la calidad del contenido de los 193 conceptos sin secciones (fuera de alcance por decisión del autor).

---

## 10. Mapa de referencia rápida

| Concepto del pseudocódigo | Código |
|---|---|
| `C0_inventario` | `content/inventory.py::C0_inventario` |
| escaneos = señales | `content/inventory.py::_senales_de_texto` |
| `C1_parseo` | `content/parse.py::C1_parseo` |
| `detectar_zonas` | `content/parse.py::_zonas_de` |
| `extraer_secciones_contrato_v1` | `content/parse.py::_secciones_de` |
| WikiLinks con posición/oración | `content/parse.py::_wikilinks_de` |
| marcas `sin verificar` / `⚠️ verificar` | `content/parse.py::_marcas_de` |
| reglas comunes L1.0 | `content/pipeline.py::ContentRunner` |
| `publish.config.yml` | `content/publish_config.py::PublishConfig` |
| Aceptación L1 | `tests/test_l1_content.py` |
