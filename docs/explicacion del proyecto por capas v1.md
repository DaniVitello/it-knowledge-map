# Explicacion del proyecto por capas v1

## Orden de las capas del pseudo-codigo (con justificacion)

El orden sigue el Apendice A del diseno tecnico y la prioridad de decisiones (punto 32: integridad > correctitud > fuentes > contexto > coherencia > actualidad > pedagogia > robustez > automatizacion > velocidad/costo).

### Capa 1 — Modelo de datos (ConceptMeta)
Por que primero: todo lo demas depende de que es un "concepto". Sin definir los campos y sus reglas de derivacion, no podemos leer el vault, ni construir prompts, ni validar. Es el atomo del sistema.

### Capa 2 — Vault como fuente de verdad (vault.py)
Por que segundo: antes de investigar, necesitamos leer las notas sin romperlas. El vault es la unica fuente de verdad de los metadatos (titulo, area, key_ideas, connections). Tambien definimos los marcadores ai:start/end, el hash del bloque, y la escritura atomica. Sin esto, no podemos persistir nada de forma segura.

### Capa 3 — Pipeline de estados (state.py + ConceptState)
Por que tercero: una vez que sabemos leer notas y que es un concepto, necesitamos la maquina de estados (pending → researching → ... → completed) y la persistencia por concepto. Esto es lo que hace al sistema recuperable e idempotente. Sin estados, no sabemos si reanudar o saltar.

### Capa 4 — Backend (interfaz + fake + notebooklm)
Por que cuarto: recien despues de tener estados y persistencia, podemos abstraer el acceso a NotebookLM. El backend fake permite probar todo sin red. El adaptador real (async, API directa) evita el bug de encoding. La interfaz ResearchBackend permite cambiar de proveedor sin tocar el resto.

### Capa 5 — Escritura segura (writer.py)
Por que quinto: antes de generar contenido real, debemos garantizar que la escritura no rompe la nota. El writer implementa: backup, hash del afuera antes/despues, escritura atomica, verificacion, proteccion de ediciones manuales, modo dry-run. Se prueba con el backend fake antes de tocar datos reales.

### Capa 6 — Investigacion (research.py + strategy.py)
Por que sexto: ahora que tenemos backend, estados y writer, podemos implementar la busqueda y evaluacion de fuentes. Incluye: construccion del plan (preguntas por dimension), estrategia de actualidad por volatilidad, seeds + dominios preferidos + busqueda abierta, ciclo de cobertura, manejo de brechas (gap/sin verificar). Persiste sources.json y raw_research.json.

### Capa 7 — Sintesis (synthesis.py + prompts)
Por que septimo: con las fuentes persistidas, generamos el contenido pedagogico. 3 preguntas a NotebookLM (grupos a/b/c), trazabilidad por afirmacion (claim → source_id), normalizacion a Markdown, separacion fundamento estable / practica moderna. Los prompts son editables y versionados.

### Capa 8 — Validacion (validation.py)
Por que octavo: antes de escribir, validamos la sintesis. Dos capas: determinista (formato, enlaces, hashes) y semantica (contenido, contexto, relaciones, profundidad, pedagogia). 17 chequeos con severidad error/warn. Falla cerrado: ante la duda, no escribe.

### Capa 9 — Orquestador (runner.py) + logging
Por que noveno: una vez que todas las fases existen individualmente, el orquestador las encadena: ejecuta fases, reintenta, reanuda, no repite. El logging estructurado (JSON Lines) da trazabilidad completa por concepto y por corrida.

### Capa 10 — CLI (cli.py)
Por que decimo: la interfaz para humanos y agentes. Subcomandos: scan, inspect, run, run-batch, status, review, reset. --json, --force, --dry-run, --stop-after. Sin prompts interactivos.

### Capa 11 — Piloto + calibracion
Por que ultimo: con todo implementado, se prueba con ~8 conceptos variados (estables, dinamicos, con muchas conexiones, con poca info, otra area, con contenido manual). Se verifica idempotencia, recuperacion, integridad de archivos. Se calibran pacing, timeouts, severidad. Solo despues se escala al lote completo.

## Resumen visual

Capa 1:  Modelo de datos     (ConceptMeta)
Capa 2:  Vault / lectura     (vault.py)
Capa 3:  Estados             (state.py)
Capa 4:  Backend             (fake + notebooklm)
Capa 5:  Escritura segura    (writer.py)
Capa 6:  Investigacion       (research.py)
Capa 7:  Sintesis            (synthesis.py + prompts)
Capa 8:  Validacion          (validation.py)
Capa 9:  Orquestador         (runner.py + log)
Capa 10: CLI                 (cli.py)
Capa 11: Piloto + calibracion

Cada capa se apoya en las anteriores. No se puede validar sin sintesis, ni sintetizar sin fuentes, ni buscar fuentes sin backend, ni persistir sin estados, ni definir estados sin modelo de datos.

---

## Capa 1 — Modelo de datos (ConceptMeta) (pseudo-codigo de alto nivel)

### Objetivo de la capa
Definir el átomo del sistema: qué es un "concepto" y qué campos lo describen, con sus reglas de derivación. Todo lo demás (leer el vault, investigar, sintetizar, validar, escribir) depende de este modelo. Sin él no hay identidad estable para un concepto, ni forma de saber qué investigar, ni cómo validar que el contenido generado corresponde a la nota correcta. Esta capa no toca disco ni red: es pura definición de datos y reglas de derivación.

### 1) Qué es un concepto en el vault (`ConceptMeta`)

Un concepto es una nota del vault que contiene un bloque autorizado `<!-- ai:start --> ... <!-- ai:end -->`. Toda la información derivable de la nota (y de la config) se consolida en un único objeto `ConceptMeta`, que es la "ficha" que circula por todo el pipeline.

```python
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

class Volatility(Enum):
    STABLE      = "stable"       # fundamento: HTTP, TCP, Big-O, etc. (re-investigar cada ~90d)
    SEMI_STABLE = "semi_stable"  # frameworks con versiones: React, Vue (cada ~30d)
    DYNAMIC     = "dynamic"      # herramientas/CLI/APIs (cada ~7d)

@dataclass(frozen=True)
class ConceptMeta:
    # --- Identidad y ubicacion ---
    id: str                      # slug del path, ej. "frontend-01-internet-web" (unico en el vault)
    title: str                   # titulo humano del concepto
    area: str                    # area tematica: frontend | backend | data | infra | ...
    note_path: Path              # ruta a la nota .md dentro del vault

    # --- Contenido manual del autor (fuente de verdad del vault) ---
    key_ideas: list[str]         # bullets de la seccion "Que abarca"
    connections: list[str]       # wikilinks de "Relacionados" (conceptos vecinos)

    # --- Metadatos crudos de la nota ---
    frontmatter: dict | None     # bloque YAML --- ... --- parseado (title, area, numero, aliases, tags, ...)

    # --- Clasificacion y estrategia de investigacion ---
    volatility: Volatility       # STABLE | SEMI_STABLE | DYNAMIC
    professional_roles: list[str]# roles a los que aplica (ej. "frontend-dev", "sre", "data-engineer")
    preferred_domains: list[str] # dominios web con prioridad para investigar este concepto
    seed_urls: list[str]         # URLs canonicas fijas (docs oficiales, RFCs) siempre incluidas

    # --- Trazabilidad de lectura (integridad) ---
    has_ai_block: bool                 # True si existe bloque ai:start/end valido
    content_hash_outside: str | None   # sha256 del "afuera" (todo excepto interior del bloque ai)
    content_hash_inside: str | None    # sha256 del interior actual del bloque ai (ediciones manuales)
    mtime_at_read: float | None        # mtime del archivo al momento de la lectura
```

Reglas:
- `ConceptMeta` es inmutable en espiritu: se deriva de la nota + config en el scan (Capa 2) y no se modifica despues. Si la nota cambia, se re-deriva.
- Es la unica estructura que el resto del pipeline consume: investigacion (Capa 6), sintesis (Capa 7), validacion (Capa 8), escritura (Capa 5) y orquestador (Capa 9) hablan en terminos de `ConceptMeta`, nunca de paths sueltos ni de frontmatter crudo.
- `professional_roles`, `preferred_domains` y `seed_urls` pueden venir de la config global o de un override por concepto (`config/concepts/<id>.yaml`); si no hay override, se derivan del area (ver seccion 2).
- `volatility` determina la ventana de frescura de la investigacion (Capa 6): stable 90d, semi_stable 30d, dynamic 7d.

### 2) Reglas de derivacion de cada campo

Cada campo se deriva en el scan (`read_concept`, Capa 2) a partir de la nota y/o de la config. Regla general: primero frontmatter, luego cuerpo, luego config, luego defaults; nunca se adivina un valor faltante sin registrarlo.

| Campo | Fuente primaria | Fallback / regla de derivacion |
|---|---|---|
| `id` | slug del path de la nota (ej. `frontend-01-internet-web`) | Siempre se deriva del path; es la clave estable del concepto. Nunca se toma del frontmatter. |
| `title` | frontmatter `title` | Si falta -> primer H1 del cuerpo; si no -> nombre del archivo sin prefijo numerico (ej. `internet-web` -> "Internet web"). |
| `area` | frontmatter `area` | Si falta -> primera carpeta del path relativo al vault (ej. `frontend/...` -> `frontend`). |
| `note_path` | path del archivo `.md` encontrado en el scan | Siempre absoluto/normalizado; es la unica ruta que el writer usa. |
| `key_ideas` | bullets bajo el heading `## Que abarca` (o `# Que abarca`) | Si la seccion no existe -> lista vacia (se registra en el reporte; no se inventan ideas). |
| `connections` | wikilinks bajo `## Relacionados` | Si no existe la seccion -> todos los wikilinks del cuerpo excepto indices (`_...`) y la propia nota. Dedup por target. |
| `frontmatter` | bloque YAML entre `---` al inicio del archivo | Si no hay bloque -> `None`. Se parsea con YAML seguro (`yaml.safe_load`). Si es invalido -> error de scan (no se procesa el concepto). |
| `volatility` | config: `area_overrides[area]` o `concept_overrides[id].volatility` | Si no hay override -> mapping por area (frontend->semi_stable, backend->semi_stable, data->semi_stable, infra->semi_stable) y por tags (tag `stable`/`dynamic`); default `semi_stable`. |
| `professional_roles` | config: `concept_overrides[id].roles` o `area_roles[area]` | Si no hay -> `[area + "-dev"]` por defecto (ej. `frontend-dev`). Lista de roles a los que es relevante el concepto (para filtrar/priorizar). |
| `preferred_domains` | config: `concept_overrides[id].preferred_domains` + `area_domains[area]` + `strategy.preferred_domains` global | Merge + dedup. Si no hay ninguno -> lista global de `strategy.preferred_domains`. |
| `seed_urls` | config: `concept_overrides[id].seed_urls` + `strategy.seed_urls` global | Merge + dedup. Las seeds del concepto se suman a las globales; son URLs canonicas siempre incluidas. |
| `content_hash_outside` | sha256 del "afuera" del bloque `ai:start/end` (si existe) | Si no hay bloque -> `None`. Ver seccion 3. |
| `content_hash_inside` | sha256 del interior actual del bloque (si existe) | Si no hay bloque -> `None`. Sirve para detectar ediciones manuales del bloque. |
| `has_ai_block` | True si existe exactamente un `ai:start` y un `ai:end` en ese orden | `False` si no hay bloque valido (se reporta como "sin bloque"). |
| `mtime_at_read` | `path.stat().st_mtime` al momento de leer | Se guarda para deteccion de edicion concurrente (Obsidian tocando el archivo). |

Reglas de derivacion:
- Orden de resolucion de un campo (prioridad): `concept_overrides[id]` > `area_overrides`/`area_*` > frontmatter del archivo > cuerpo de la nota > defaults de config > default hardcodeado.
- Si un campo obligatorio no se puede derivar (ej. `title` sin frontmatter ni H1 ni nombre usable) -> el concepto se marca `failed` con `missing_required_field` en el scan; no se procesa.
- Los overrides por concepto viven en `config/concepts/<id>.yaml` (opcional). Si el archivo no existe, se usan los defaults del area. No es obligatorio tener override por cada concepto.
- `key_ideas` y `connections` son la "voz del autor": se leen del vault y NUNCA se sobrescriben (el writer no toca esas secciones). Son la fuente de verdad manual.
- `professional_roles`, `preferred_domains` y `seed_urls` NO se derivan de la nota: vienen de config/overrides. La nota solo aporta `title`, `area`, `key_ideas`, `connections`, `frontmatter`.
- Si `frontmatter` es `None` (sin bloque `---`), los campos que dependen de el (`title`, `area`) caen a sus fallbacks de cuerpo/path; no se falla por ausencia de frontmatter salvo que config exija `require_frontmatter: true`.

### 3) Content hash: que es y para que sirve

Hay dos hashes por concepto, ambos SHA-256 sobre texto UTF-8:

- `content_hash_outside` (hash del "afuera"): SHA-256 de TODO el contenido de la nota EXCEPTO el interior del bloque `ai:start/end` (los marcadores se incluyen en el "afuera"). Representa: frontmatter + titulo + headings + "Que abarca" + "Relacionados" + navegacion + cualquier contenido manual.
- `content_hash_inside` (hash del interior): SHA-256 del texto entre `ai:start` y `ai:end` (el contenido generado por el sistema).

Para que sirve:
1. Integridad en escritura (Capa 5): antes de escribir se calcula `outside_hash_before`; despues de escribir se relee y se calcula `outside_hash_after`. Si difieren -> algo toco el afuera -> restaurar backup y marcar `failed`. Garantiza que el writer solo modifico el interior.
2. Deteccion de edicion concurrente: si Obsidian (o el usuario) modifica la nota entre la lectura y la escritura, el hash del afuera cambia -> `ConcurrentEditError` -> no se sobrescribe.
3. Deteccion de edicion manual posterior: si el usuario edita a mano el bloque `ai:start/end` despues de una corrida, `content_hash_inside` cambia -> en la proxima corrida se detecta que el contenido manual difiere del generado -> se puede preservar o marcar para revision (no se pisa silenciosamente).
4. Idempotencia / cache (Capa 6 y 7): si el `content_hash_outside` no cambio desde la ultima corrida exitosa y los artefactos (`raw_research.json`, `synthesis.json`) siguen validos y frescos -> se salta la investigacion/sintesis (no se repite trabajo). El hash es la "huella" del input.
5. Trazabilidad/auditoria: el hash se persiste en `estado.json` (junto al `concept_id`) y en `validation.json`, permitiendo saber exactamente sobre que version de la nota se genero cada contenido.

Reglas:
- El hash se calcula sobre el texto normalizado (UTF-8, sin BOM anadido) del "afuera"/interior tal como esta en el archivo, respetando newlines originales (CRLF/LF). No se normalizan newlines antes de hashear el "afuera" (se hashea lo que hay en disco).
- `content_hash_outside` incluye los marcadores `ai:start`/`ai:end` (son parte del afuera), pero excluye el interior. Asi, mover un marcador cambia el hash (correcto: es un cambio estructural).
- Si no existe el bloque, ambos hashes son `None` y el concepto se considera "sin bloque" (no se procesa para escritura; se reporta en el scan).
- El hash NO es un id del concepto: el id es el slug del path. El hash cambia con el contenido; el id no.
- Colisiones: SHA-256 se asume sin colisiones para este dominio (notas de texto). No se implementa verificacion de colision.

```python
def content_hash_outside(text: str) -> str | None:
    span = find_markers(text)          # None si no hay bloque
    if span is None:
        return None
    outside = extract_outside(text)    # todo excepto interior (marcadores incluidos)
    return sha256(outside)

def content_hash_inside(text: str) -> str | None:
    span = find_markers(text)
    if span is None:
        return None
    return sha256(span.raw_inside)
```

### 4) Por que esta capa va primero

Todo lo demas depende de que exista una definicion unica y estable de "concepto":

- Capa 2 (vault) no puede leer ni escribir sin saber que campos extraer de una nota ni como derivarlos (`title`, `area`, `key_ideas`, `connections`). El scan produce `list[ConceptMeta]`; sin el modelo, no hay contrato de salida.
- Capa 3 (estados) agrupa el progreso por `concept_id`, que es el `id` de `ConceptMeta`. Sin id estable, no hay recuperacion ni idempotencia.
- Capa 4 (backend) recibe un `ConceptMeta` para crear el notebook y armar el plan de investigacion (titulo, area, key_ideas, connections, volatilidad).
- Capa 5 (writer) escribe para un `ConceptMeta` y verifica que el frontmatter/titulo/area coincidan con el (`V_FRONTMATTER_MATCH`).
- Capa 6 (investigacion) arma el `ResearchContext` a partir de `ConceptMeta` (titulo, area, key_ideas, connections, volatilidad, professional_roles, preferred_domains, seed_urls).
- Capa 7 (sintesis) consume `ConceptMeta` para el prompt y para los cross-links (connections).
- Capa 8 (validacion) cruza el contenido generado contra el `ConceptMeta` (key_ideas, connections, title, area).
- Capa 9 (orquestador) itera sobre `list[ConceptMeta]` y persiste estado por `concept_id`.

Reglas:
- `ConceptMeta` es el contrato compartido: si se agrega un campo, se actualiza esta capa primero y luego las consumidoras. No se "inventan" campos en capas posteriores.
- Cambiar la derivacion de un campo (ej. como se calcula `area`) afecta a todas las capas; por eso se documenta aqui y se versiona con el codigo.
- Esta capa no toca disco ni red: solo define la estructura y las reglas de derivacion. La materializacion (leer la nota) es responsabilidad de Capa 2.

### Excepciones de la capa

```python
class ConceptModelError(Exception): ...
class MissingRequiredFieldError(ConceptModelError): ...   # title/area no derivables
class InvalidFrontmatterError(ConceptModelError): ...     # YAML invalido en frontmatter
class UnknownAreaError(ConceptModelError): ...           # area no reconocida (solo si config lo exige)
class InvalidVolatilityError(ConceptModelError): ...     # volatilidad fuera del enum
```

### Reglas de negocio (de la spec)
- Un concepto = una nota del vault con bloque `ai:start/end`. Sin bloque -> no es concepto procesable (se reporta).
- `ConceptMeta` es la unica representacion de un concepto en el pipeline; ninguna capa posterior re-lee el frontmatter crudo (lo recibe via `ConceptMeta`).
- Los campos manuales (`key_ideas`, `connections`, frontmatter) son fuente de verdad del vault y nunca se sobrescriben.
- Los campos de estrategia (`volatility`, `professional_roles`, `preferred_domains`, `seed_urls`) vienen de config/overrides, no de la nota.
- Los hashes (`content_hash_outside`, `content_hash_inside`) son SHA-256 y sirven para integridad, deteccion de edicion concurrente/manual e idempotencia.
- La derivacion sigue prioridad: override por concepto > override por area > frontmatter > cuerpo > defaults.
- Si falta un campo obligatorio no derivable -> `failed` con `missing_required_field`, sin procesar el concepto.

---

## Capa 2 — El vault como fuente de verdad (pseudo-codigo de alto nivel)

### Objetivo de la capa
Leer y escribir notas del vault sin romper nada fuera del bloque autorizado, verificando integridad antes y despues.

### Lectura de una nota
1. Leer el archivo en bytes y decodificar como UTF-8.
2. Detectar el tipo de fin de linea (CRLF o LF) del archivo original.
3. Buscar exactamente un marcador ai:start y un ai:end, en ese orden. Si no existen o hay mas de uno → error.
4. Calcular el hash del "afuera": todo el contenido excepto el interior del bloque.
5. Parsear el frontmatter YAML (si existe).
6. Extraer del cuerpo (fuera del bloque): titulo, area, key_ideas (bullets de "Que abarca"), connections (wikilinks de "Relacionados").
7. Calcular el hash del interior del bloque (para detectar ediciones manuales posteriores).

### Escritura en una nota
1. Leer la nota completa y calcular outside_hash_before.
2. Validar marcadores: exactamente uno de cada, en orden. Si faltan → fallar (no insertar automaticamente).
3. Hacer backup de la nota en workdir/backups/<concept_id>/.
4. Reemplazar unicamente el interior del bloque con el nuevo contenido.
5. Escribir de forma atomica (archivo temporal + renombre).
6. Releer y verificar: outside_hash_after == outside_hash_before, interior coincide con la sintesis validada, frontmatter/titulo/navegacion/wikilinks siguen presentes.
7. Si alguna verificacion falla → restaurar backup y marcar failed.
8. Si todo OK → estado written.

### Reglas de negocio (de la spec)
- Solo se modifica el interior del bloque ai:start/ai:end. Todo lo demas se verifica byte a byte.
- Si faltan marcadores, no se insertan automaticamente (salvo config explicita). El concepto queda failed.
- Backup antes de escribir. Hash del afuera antes y despues.
- Fin de linea y codificacion se respetan (se detectan del archivo original).
- Deteccion de edicion concurrente: se compara mtime/hash para detectar si Obsidian modifico el archivo entre lectura y escritura.
- Modo --dry-run: genera todo y muestra el diff sin escribir.
- No se adivina: si faltan marcadores, falla (no se inventan).

### Descubrimiento de notas (scan)
1. Recorrer el vault buscando archivos .md segun el glob configurado.
2. Excluir archivos que matcheen los exclude_globs (indices, _, etc.).
3. Para cada archivo: si tiene bloque ai:start/end → es un concepto (leer metadatos). Si no → nota sin bloque (registrar para reporte).
4. Devolver lista de conceptos + lista de notas sin bloque.

### Lectura de un concepto (read_concept)
1. Extraer frontmatter (title, area, numero, aliases, tags).
2. Si falta title → usar primer H1 o nombre del archivo sin prefijo numerico.
3. Si falta area → usar primera carpeta del path.
4. Extraer key_ideas: bullets bajo el heading "Que abarca".
5. Extraer connections: wikilinks bajo el heading "Relacionados", o todos los wikilinks excepto indices y la propia nota.
6. Calcular concept_id = slug del path (ej: "frontend-01-internet-web").
7. Calcular content_hash_outside_ai si el bloque existe.

---

## Capa 3 — Pipeline de estados (state machine / pseudo-código de alto nivel)

### 1) Estados del pipeline por concepto (enum)

```python
class ConceptStatus(Enum):
    PENDING      = "pending"       # en cola, sin procesar
    RESEARCHING  = "researching"    # buscando/evaluando fuentes
    SYNTHESIZING = "synthesizing"  # generando contenido pedagogico
    VALIDATING   = "validating"     # validando la sintesis
    WRITING      = "writing"       # escribiendo en el vault
    DONE         = "done"          # terminal exitoso
    FAILED       = "failed"        # terminal por error (reintentable)
    BLOCKED      = "blocked"       # terminal por bloqueo humano
```

### 2) Transiciones válidas y reglas

```python
TRANSITIONS = {
    PENDING:      [RESEARCHING],
    RESEARCHING:  [SYNTHESIZING, FAILED],
    SYNTHESIZING: [VALIDATING,   FAILED],
    VALIDATING:   [WRITING,      FAILED, BLOCKED],
    WRITING:      [DONE,         FAILED],
    DONE:         [],              # terminal: no sale
    FAILED:       [RESEARCHING, SYNTHESIZING, VALIDATING, WRITING],  # retry del estado que fallo
    BLOCKED:      [RESEARCHING, SYNTHESIZING, VALIDATING, WRITING],  # retry manual
}

def can_transition(src, dst) -> bool:
    return dst in TRANSITIONS[src]
```

Reglas:
- Transiciones lineales: no se salta ninguna fase del enum (pending → ... → done).
- `done` es estado terminal: nunca se reejecuta.
- `failed` y `blocked` son terminales operativos: requieren reintento explicito o accion humana.
- Un reintento vuelve al estado que fallo (no reinicia desde pending), conservando el checkpoint previo.

### 3) Idempotencia y resume desde checkpoint

```python
def run_concept(concept_id):
    state = load_state(concept_id)            # lee estado.json del concepto

    if state.status in (DONE, FAILED, BLOCKED):
        return state                          # terminal: no reejecutar

    phase = state.checkpoint or first_phase()  # reanudar donde se quedo

    while phase is not None:
        try:
            phase_fn = PHASES[phase]
            phase_fn(concept_id)              # ejecuta la fase
            state.checkpoint = phase
            state.status = next_status(phase)
            persist_state(concept_id, state)   # atomica
            phase = next_phase(phase)
        except Exception as e:
            handle_failure(concept_id, phase, e)
            break

    return state
```

- Al arrancar se lee `estado.json` por concepto (status + ultimo checkpoint).
- Si el status es terminal (`done`/`failed`/`blocked`) → no se reejecuta.
- Si es no-terminal → se reanuda desde el ultimo checkpoint persistido (no desde cero).

### 4) Reintentos max 3 por estado con backoff

```python
MAX_RETRIES = 3
BACKOFF_SECONDS = [2, 4, 8]   # exponencial, configurable

def execute_phase_with_retry(phase_fn, concept_id):
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return phase_fn(concept_id)
        except Exception as e:
            last_error = e
            if attempt == MAX_RETRIES:
                raise
            sleep(BACKOFF_SECONDS[attempt - 1])
    raise last_error
```

- Max 3 intentos por fase.
- Backoff exponencial: intento 1 → 2s, intento 2 → 4s, intento 3 → 8s (configurable).
- Al agotar los reintentos, la fase se marca `failed` y se persiste el error.

### 5) Estados terminales y que se persiste

```python
# done
persist(concept_id, {
    "status": "done",
    "content_hash_outside":  <hash>,
    "content_hash_inside":   <hash>,
    "writer_version":        <str>,
    "validation_result":     <obj>,
    "written_at":            <iso8601>,
})

# failed
persist(concept_id, {
    "status": "failed",
    "error":         <msg>,
    "fase_fallida":  <phase>,
    "timestamp":     <iso8601>,
})

# blocked
persist(concept_id, {
    "status": "blocked",
    "blocker":   <str>,
    "detalle":   <str>,
    "resolver":  <quien debe resolverlo>,
})
```

- `done` → se persiste: status, content_hash_outside, content_hash_inside, writer_version, validation_result, written_at.
- `failed` → se persiste: status, error, fase_fallida, timestamp.
- `blocked` → se persiste: status, blocker, detalle, quien debe resolverlo.

### 6) Orquestacion del bucle sobre 255 conceptos (cola, orden, serial con backoff)

```python
def run_batch():
    queue = scan_concepts()            # FIFO, orden de scan / numerico del concepto

    for concept in queue:
        try:
            run_concept(concept.id)    # serial: checkpoint antes de avanzar de fase
        except Exception as e:
            mark_failed(concept.id, e) # no detiene el lote
            continue
        sleep(PACING_BETWEEN_CONCEPTS) # backoff entre conceptos
```

- Cola FIFO de conceptos en `pending` (resultado del scan).
- Orden: scan order / orden numerico del concepto.
- Procesamiento serial por concepto: se transiciona y persiste el estado (checkpoint) ANTES de avanzar a la fase siguiente.
- Un concepto que falla no detiene el lote; se registra y se sigue con el siguiente.

### 7) Relacion con checkpoint (estado.json)

```json
{
  "frontend-01-internet-web": {
    "status":     "synthesizing",
    "checkpoint": "researching",
    "phase_data": { "sources": [...], "coverage": 0.8 },
    "retries":    1,
    "updated_at": "2026-10-22T10:00:00Z"
  }
}
```

- `estado.json` agrupa por `concept_id`: status + checkpoint + datos de la fase.
- Se escribe de forma atomica en cada transicion validada.
- El runner consulta `estado.json` para decidir reejecutar o reanudar.
- Es la unica fuente de verdad del progreso: sin el, no hay recuperacion ni idempotencia.

---

## Capa 4 — Backend: interfaz + fake + notebooklm (pseudo-codigo de alto nivel)

### Objetivo de la capa
Abstraer el acceso a NotebookLM detras de una interfaz unica (`ResearchBackend`) para que el resto del pipeline (investigacion, sintesis) no dependa de un proveedor concreto. Permitir probar todo el flujo sin red mediante un backend fake, y usar el adaptador real (API Python async de `notebooklm-py`) en produccion, evitando el bug de encoding del CLI.

### 1) Interfaz del backend (`ResearchBackend`)

Contrato comun que implementan todos los backends. El pipeline solo habla con esta interfaz.

```python
class ResearchBackend(Protocol):
    # Ciclo de vida del notebook
    async def create_notebook(self, concept: ConceptMeta) -> str:
        """Crea un notebook vacio para el concepto. Devuelve notebook_id."""
        ...

    async def delete(self, notebook_id: str) -> None:
        """Elimina el notebook y todos sus artefactos. Idempotente."""
        ...

    # Fuentes
    async def add_sources(self, notebook_id: str, sources: list[Source]) -> list[str]:
        """Sube las fuentes (URLs/textos) al notebook. Devuelve source_ids asignados."""
        ...

    # Investigacion
    async def research(self, notebook_id: str, questions: ResearchPlan) -> ResearchResult:
        """Ejecuta las preguntas de investigacion (grupos a/b/c) y devuelve respuestas
        con trazabilidad afirmacion -> source_id."""
        ...

    # Reporte
    async def generate_report(self, notebook_id: str, spec: ReportSpec) -> str:
        """Genera un artefacto (reporte) dentro del notebook. Devuelve report_id."""
        ...

    async def download(self, notebook_id: str, report_id: str, dest: Path) -> Path:
        """Descarga el artefacto a disco. Devuelve la ruta final."""
        ...
```

Estructuras de datos compartidas (definidas en Capa 1 / modelo):

```python
@dataclass
class Source:
    source_id: str          # id interno (slug/url)
    url: str | None         # None si es texto pegado
    title: str
    snippet: str | None     # resumen corto para el prompt
    kind: Literal["url", "text", "file"]

@dataclass
class ResearchQuestion:
    qid: str                # ej. "a1", "b2"
    group: Literal["a", "b", "c"]
    text: str

@dataclass
class ResearchPlan:
    questions: list[ResearchQuestion]

@dataclass
class Claim:
    text: str
    source_ids: list[str]   # trazabilidad afirmacion -> fuentes

@dataclass
class ResearchAnswer:
    qid: str
    group: str
    answer_md: str
    claims: list[Claim]

@dataclass
class ResearchResult:
    notebook_id: str
    answers: list[ResearchAnswer]
    coverage: float         # 0..1

@dataclass
class ReportSpec:
    title: str
    format: Literal["markdown", "pdf"]
```

Reglas del contrato:
- Todos los metodos son `async` (incluso el fake, para mantener firma unica).
- `notebook_id` es un string opaco; el pipeline nunca lo interpreta.
- `research` debe devolver respuestas agrupadas por grupo (a/b/c) y con claims trazables a `source_id`.
- Ningun metodo bloquea el event loop (IO asincrono o delegado a executor).
- Los metodos son idempotentes cuando tiene sentido: `delete` no falla si el notebook ya no existe.

### 2) Backend fake (para tests sin red)

Implementacion en memoria que simula respuestas deterministas, sin tocar la red. Usado por tests, dry-run de desarrollo y CI.

```python
class FakeBackend(ResearchBackend):
    def __init__(self, fixtures_dir: Path | None = None, latency_ms: int = 0):
        self.notebooks: dict[str, FakeNotebook] = {}
        self.calls: list[BackendCall] = []          # para assertions en tests
        self._counter = 0
        self.latency_ms = latency_ms
        self.fixtures = load_fixtures(fixtures_dir) if fixtures_dir else {}

    async def create_notebook(self, concept):
        await self._delay()
        self._counter += 1
        nb_id = f"fake-nb-{self._counter}"
        self.notebooks[nb_id] = FakeNotebook(concept=concept)
        self._record("create_notebook", concept.id, nb_id)
        return nb_id

    async def add_sources(self, notebook_id, sources):
        await self._delay()
        nb = self._get(notebook_id)
        ids = []
        for s in sources:
            sid = f"src-{len(nb.sources)+1}"
            nb.sources[sid] = s
            ids.append(sid)
        self._record("add_sources", notebook_id, ids)
        return ids

    async def research(self, notebook_id, questions):
        await self._delay()
        nb = self._get(notebook_id)
        answers = []
        for q in questions.questions:
            # respuesta canned por (concept, qid) o generica
            raw = self.fixtures.get((nb.concept.id, q.qid)) or canned_answer(q)
            claims = parse_claims(raw, nb.sources)   # mapea a source_ids reales
            answers.append(ResearchAnswer(qid=q.qid, group=q.group,
                                         answer_md=raw, claims=claims))
        result = ResearchResult(notebook_id=notebook_id, answers=answers,
                                coverage=estimate_coverage(answers, nb.sources))
        self._record("research", notebook_id, result)
        return result

    async def generate_report(self, notebook_id, spec):
        await self._delay()
        rid = f"fake-report-{notebook_id}"
        self._get(notebook_id).reports[rid] = render_markdown(spec, ...)
        self._record("generate_report", notebook_id, rid)
        return rid

    async def download(self, notebook_id, report_id, dest):
        await self._delay()
        content = self._get(notebook_id).reports[report_id]
        dest.write_text(content, encoding="utf-8")
        self._record("download", notebook_id, str(dest))
        return dest

    async def delete(self, notebook_id):
        await self._delay()
        self.notebooks.pop(notebook_id, None)   # idempotente
        self._record("delete", notebook_id, None)

    # helpers
    async def _delay(self):
        if self.latency_ms:
            await asyncio.sleep(self.latency_ms / 1000)

    def _get(self, nb_id):
        if nb_id not in self.notebooks:
            raise BackendError(f"notebook no encontrado: {nb_id}")
        return self.notebooks[nb_id]

    def _record(self, method, *args):
        self.calls.append(BackendCall(method=method, args=args, ts=now()))
```

Caracteristicas:
- Determinista: mismas entradas → mismas salidas (para tests reproducibles).
- Fixtures opcionales: archivos JSON/MD por concepto/qid para simular respuestas reales capturadas.
- `calls` permite assertions: `assert backend.was_called("research")`.
- `latency_ms` simula red para probar timeouts/backoff.
- No requiere credenciales ni red.

Usos:
- Tests unitarios de investigacion/sintesis/writer.
- `--backend fake` en CLI para desarrollo sin NotebookLM.
- Modo dry-run de pipelines largos (smoke test).

### 3) Backend notebooklm (wrapper async de `notebooklm-py`)

Adaptador real que envuelve la API Python de `notebooklm-py`. Todo es `async` (la libreria expone metodos async o se delega a executor si es sync). Evita el bug de encoding del CLI al usar la API directa (sin subprocess).

```python
class NotebookLMBackend(ResearchBackend):
    def __init__(self, auth: NotebookLMAuth, config: BackendConfig):
        self.client = NotebookLMClient(auth=auth)   # de notebooklm-py
        self.config = config
        self.sem = asyncio.Semaphore(config.max_concurrent_notebooks)
        self.timeouts = config.timeouts

    async def create_notebook(self, concept):
        async with self.sem:
            try:
                nb = await asyncio.wait_for(
                    self.client.create_notebook(title=concept.title),
                    timeout=self.timeouts.create_notebook,
                )
                return nb.id
            except asyncio.TimeoutError:
                raise BackendTimeout("create_notebook", concept.id)
            except AuthError as e:
                raise BackendAuthError(str(e)) from e

    async def add_sources(self, notebook_id, sources):
        async with self.sem:
            ids = []
            for s in sources:
                try:
                    if s.kind == "url":
                        src = await asyncio.wait_for(
                            self.client.add_url_source(notebook_id, s.url),
                            timeout=self.timeouts.add_source,
                        )
                    elif s.kind == "text":
                        src = await asyncio.wait_for(
                            self.client.add_text_source(notebook_id, s.title, s.snippet),
                            timeout=self.timeouts.add_source,
                        )
                    else:
                        src = await asyncio.wait_for(
                            self.client.add_file_source(notebook_id, s.path),
                            timeout=self.timeouts.add_source,
                        )
                    ids.append(src.id)
                except asyncio.TimeoutError:
                    raise BackendTimeout("add_sources", notebook_id)
            return ids

    async def research(self, notebook_id, questions):
        async with self.sem:
            answers = []
            # Las 3 preguntas de cada grupo se pueden mandar en paralelo si la API lo permite,
            # o serializadas para respetar rate limits. Configurable.
            for q in questions.questions:
                try:
                    raw = await asyncio.wait_for(
                        self.client.chat(notebook_id, q.text),
                        timeout=self.timeouts.research,
                    )
                except asyncio.TimeoutError:
                    raise BackendTimeout("research", notebook_id)
                claims = parse_claims(raw, sources_of(notebook_id))  # trazabilidad
                answers.append(ResearchAnswer(qid=q.qid, group=q.group,
                                             answer_md=raw, claims=claims))
            coverage = estimate_coverage(answers, ...)
            return ResearchResult(notebook_id=notebook_id, answers=answers, coverage=coverage)

    async def generate_report(self, notebook_id, spec):
        async with self.sem:
            try:
                art = await asyncio.wait_for(
                    self.client.generate_report(notebook_id, title=spec.title, format=spec.format),
                    timeout=self.timeouts.generate_report,
                )
                return art.id
            except asyncio.TimeoutError:
                raise BackendTimeout("generate_report", notebook_id)

    async def download(self, notebook_id, report_id, dest):
        async with self.sem:
            try:
                data = await asyncio.wait_for(
                    self.client.download_artifact(notebook_id, report_id),
                    timeout=self.timeouts.download,
                )
                dest.write_bytes(data)   # escribir en bytes, luego decodificar UTF-8 si es texto
                return dest
            except asyncio.TimeoutError:
                raise BackendTimeout("download", notebook_id)

    async def delete(self, notebook_id):
        async with self.sem:
            try:
                await asyncio.wait_for(
                    self.client.delete_notebook(notebook_id),
                    timeout=self.timeouts.delete,
                )
            except NotFoundError:
                pass   # idempotente
            except asyncio.TimeoutError:
                raise BackendTimeout("delete", notebook_id)
```

Notas de implementacion:
- Autenticacion: `NotebookLMAuth` se construye desde cookies/session exportadas (no password en codigo). Se valida al arrancar; si falta → `BackendAuthError` fail-fast.
- El cliente se crea una vez por proceso y se reutiliza (connection pooling).
- `sem` limita notebooks concurrentes (NotebookLM tiene limites de cuenta); configurable.
- Escritura de `download` en bytes para evitar problemas de encoding; el caller decodifica UTF-8.
- `parse_claims` reutiliza la misma logica que el fake (compartida en modulo `claims.py`).

### 4) Como se elige que backend usar (config)

Configuracion en `config.yaml` (o env vars / CLI flags), leida al arrancar:

```yaml
backend:
  provider: "notebooklm"   # "fake" | "notebooklm"
  fake:
    fixtures_dir: "tests/fixtures/backend"
    latency_ms: 0
  notebooklm:
    auth_file: "~/.config/.../notebooklm_auth.json"
    max_concurrent_notebooks: 2
    timeouts:
      create_notebook: 30
      add_source: 60
      research: 120
      generate_report: 180
      download: 60
      delete: 30
```

Factory:

```python
def create_backend(config: Config) -> ResearchBackend:
    provider = config.backend.provider
    # override por CLI: --backend fake
    if os.getenv("BACKEND_PROVIDER"):
        provider = os.getenv("BACKEND_PROVIDER")

    if provider == "fake":
        return FakeBackend(
            fixtures_dir=config.backend.fake.fixtures_dir,
            latency_ms=config.backend.fake.latency_ms,
        )
    if provider == "notebooklm":
        auth = NotebookLMAuth.load(config.backend.notebooklm.auth_file)
        if not auth.is_valid():
            raise BackendAuthError("credenciales de NotebookLM invalidas o ausentes")
        return NotebookLMBackend(auth=auth, config=config.backend.notebooklm)
    raise ConfigError(f"backend desconocido: {provider}")
```

Reglas:
- Validacion fail-fast al arrancar: si se pide `notebooklm` y faltan credenciales → error claro antes de procesar conceptos.
- Override por CLI (`--backend fake|notebooklm`) y por env var, en ese orden de precedencia: CLI > env > config.
- El backend se instancia una vez por corrida y se inyecta en el orquestador (no se crea por concepto).
- Cambiar de backend no requiere tocar el resto del pipeline (solo config).

### 5) Manejo de errores y timeouts

Jerarquia de excepciones:

```python
class BackendError(Exception): ...
class BackendTimeout(BackendError):       # operacion excedio timeout
    def __init__(self, op, target): ...
class BackendAuthError(BackendError):     # credenciales invalidas/ausentes
class BackendNetworkError(BackendError):  # red caida, 5xx, etc.
class BackendNotFoundError(BackendError): # notebook/reporte inexistente
class BackendRateLimitError(BackendError):# 429 / cuota
```

Estrategia:
- Timeouts por operacion (ver config), aplicados con `asyncio.wait_for`. Si se excede → `BackendTimeout`.
- Reintentos: las operaciones idempotentes (`research`, `download`) se reintentan hasta `MAX_RETRIES` con backoff exponencial. `delete` no reintenta (idempotente). `create_notebook` reintenta solo si fallo antes de obtener id.
- Mapeo a estados del pipeline (Capa 3):
  - `BackendTimeout` / `BackendNetworkError` / `BackendRateLimitError` → fase `failed` reintentable (vuelve a la misma fase).
  - `BackendAuthError` → `blocked` (requiere accion humana: renovar credenciales).
  - `BackendNotFoundError` → `failed` con detalle (posible inconsistencia de estado).
- Limpieza en fallo: si `create_notebook` OK pero `add_sources` falla → intentar `delete(notebook_id)` (best-effort, no bloquear) para no dejar notebooks huerfanos. Registrar en log si la limpieza falla.
- Circuit breaker simple: si N fallos consecutivos de red → pausar el lote y marcar `blocked` con "backend no disponible" (evita hammering).
- Logging estructurado: cada llamada al backend se registra (metodo, target, duracion, resultado/error) en JSON Lines para trazabilidad.
- No se exponen secretos en logs (auth_file, cookies).

Integracion con el estado (Capa 3):
```python
async def research_phase(concept_id):
    backend = get_backend()                 # singleton de la corrida
    state = load_state(concept_id)
    notebook_id = state.phase_data.get("notebook_id")
    try:
        if not notebook_id:
            notebook_id = await backend.create_notebook(load_concept(concept_id))
            state.phase_data["notebook_id"] = notebook_id
            persist_state(concept_id, state)
        await backend.add_sources(notebook_id, load_sources(concept_id))
        result = await backend.research(notebook_id, build_plan(concept_id))
        state.phase_data["research_result"] = result
        persist_state(concept_id, state)
    except BackendAuthError as e:
        mark_blocked(concept_id, "auth", str(e))
        await safe_delete(backend, notebook_id)
        raise
    except (BackendTimeout, BackendNetworkError, BackendRateLimitError) as e:
        await safe_delete(backend, notebook_id)
        raise   # el reintento de Capa 3 se encarga
```

### Reglas de negocio (de la spec)
- El pipeline nunca importa `notebooklm-py` directamente; solo la interfaz `ResearchBackend`.
- El backend fake es la unica dependencia de los tests de investigacion/sintesis (no red en CI).
- Todos los metodos son async; prohibido bloquear el event loop.
- Timeouts obligatorios en toda llamada de red (sin timeout = bug).
- Limpieza best-effort de notebooks huerfanos ante fallo.
- Credenciales fuera del codigo (archivo de auth), validadas al arrancar.
- `delete` es idempotente: no falla si el recurso ya no existe.
- Trazabilidad: cada respuesta de `research` debe mapear afirmaciones a `source_id`.
```
---

## Capa 5 — Escritura segura (writer.py) (pseudo-código de alto nivel)

### Objetivo de la capa
Garantizar que la escritura del contenido generado no rompa la nota del vault: solo se modifica el interior del bloque autorizado (`ai:start`/`ai:end`), todo lo demás se verifica byte a byte. Implementa backup, hash del afuera antes/después, escritura atómica, verificación, protección de ediciones manuales, detección de concurrencia y modo dry-run. Se prueba con el backend fake antes de tocar datos reales.

### 1) Escritura atómica con backup y restore

```python
class SafeWriter:
    def __init__(self, config, vault_root: Path, workdir: Path):
        self.config = config
        self.vault_root = vault_root
        self.backup_root = workdir / "backups"
        self.tmp_root = workdir / "tmp"        # MISMO filesystem que el vault

    def write_concept(self, concept: ConceptMeta, synthesis: Synthesis, dry_run: bool = False) -> WriteResult:
        path = concept.path

        # 1. Leer nota completa en bytes y decodificar
        raw_bytes = path.read_bytes()
        original_text = raw_bytes.decode("utf-8")
        newline = detect_newline(original_text)            # "\r\n" o "\n"

        # 2. Hash del afuera ANTES
        outside_before = extract_outside(original_text)
        outside_hash_before = sha256(outside_before)

        # 3. Validar marcadores
        span = find_markers(original_text)
        if span is None:
            raise MissingMarkersError(path)
        if count_markers(original_text) != (1, 1):
            raise DuplicateMarkersError(path)
        if span.start_line >= span.end_line:
            raise MarkerOrderError(path)

        # 4. Detectar edicion concurrente (mtime/hash entre lectura y ahora)
        if concurrent_edit_detected(path, concept.mtime_at_read, concept.outside_hash_at_read):
            raise ConcurrentEditError(path)

        # 5. Backup
        backup_path = self._backup(path, concept.id)

        # 6. Construir nuevo interior (solo el contenido sintetizado y validado)
        new_inside = render_inside(synthesis, concept)     # Markdown normalizado
        new_text = replace_inside(original_text, span, new_inside, newline)
        new_text = normalize_newlines(new_text, newline)

        # 7. Dry-run: mostrar diff y salir sin escribir
        if dry_run:
            return DiffResult(path=path, original=original_text, proposed=new_text)

        # 8. Escritura atomica
        tmp_path = self._atomic_write(path, new_text)

        # 9. Verificar (releyendo desde disco)
        try:
            self._verify(path, original_text, new_text, outside_hash_before, new_inside, concept)
        except VerificationError as e:
            self._restore(backup_path, path)               # byte a byte
            tmp_path.unlink(missing_ok=True)
            raise WriteFailedError(path, cause=e) from e

        tmp_path.unlink(missing_ok=True)
        return WriteResult(
            path=path,
            backup_path=backup_path,
            outside_hash=outside_hash_before,
            inside_hash=sha256(new_inside),
        )

    def _backup(self, path: Path, concept_id: str) -> Path:
        dest_dir = self.backup_root / concept_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        ts = now_iso_compact()                            # ej. 20261022T100000Z
        dest = dest_dir / f"{path.name}.{ts}.bak"
        shutil.copy2(path, dest)                          # preserva mtime
        return dest

    def _atomic_write(self, path: Path, text: str) -> Path:
        self.tmp_root.mkdir(parents=True, exist_ok=True)
        tmp = self.tmp_root / f"{path.name}.{uuid4().hex}.tmp"
        tmp.write_bytes(text.encode("utf-8"))             # bytes, control exacto
        os.replace(tmp, path)                             # renombre atomico (mismo FS)
        return tmp

    def _restore(self, backup_path: Path, path: Path):
        shutil.copy2(backup_path, path)                   # restaura byte a byte
```

Reglas:
- Backup ANTES de escribir, en `workdir/backups/<concept_id>/`, con timestamp compacto.
- Escritura atómica: archivo temporal en el MISMO filesystem que el vault + `os.replace` (renombre atómico). Nunca se escribe directo sobre la nota.
- Si cualquier verificación falla → restaurar backup byte a byte y marcar `failed`.
- `shutil.copy2` preserva mtime para no disparar falsos positivos de edición concurrente.
- El directorio temporal debe estar en el mismo filesystem que el vault (si no, `os.replace` deja de ser atómico).
- El writer es la única pieza que toca el vault; investigación/síntesis/validación solo leen.

### 2) Marcadores `ai:start`/`ai:end` y reemplazo del bloque

```python
MARKER_START = "<!-- ai:start -->"
MARKER_END   = "<!-- ai:end -->"

@dataclass
class MarkerSpan:
    start_line: int      # indice de la linea del marcador start
    end_line: int        # indice de la linea del marcador end
    inside_start: int    # primera linea del interior (exclusiva del start)
    inside_end: int      # ultima linea del interior (exclusiva del end)
    raw_inside: str      # texto actual del interior (con newlines originales)

def find_markers(text: str) -> MarkerSpan | None:
    lines = text.splitlines(keepends=True)
    starts = [i for i, l in enumerate(lines) if MARKER_START in l]
    ends   = [i for i, l in enumerate(lines) if MARKER_END   in l]
    if len(starts) != 1 or len(ends) != 1:
        return None
    if starts[0] >= ends[0]:
        return None
    return MarkerSpan(
        start_line=starts[0],
        end_line=ends[0],
        inside_start=starts[0] + 1,
        inside_end=ends[0],
        raw_inside="".join(lines[starts[0] + 1:ends[0]]),
    )

def count_markers(text: str) -> tuple[int, int]:
    return (text.count(MARKER_START), text.count(MARKER_END))

def replace_inside(text: str, span: MarkerSpan, new_inside: str, newline: str) -> str:
    lines = text.splitlines(keepends=True)
    before = "".join(lines[:span.start_line + 1])   # incluye linea del start
    after  = "".join(lines[span.end_line:])        # incluye linea del end en adelante
    if new_inside and not new_inside.endswith(newline):
        new_inside = new_inside + newline
    if new_inside == "":
        new_inside = newline                       # deja una linea vacia entre marcadores
    return before + new_inside + after
```

Reglas:
- Marcadores exactos: `<!-- ai:start -->` y `<!-- ai:end -->`. Exactamente uno de cada, en ese orden. Si faltan o hay más de uno → error (no se insertan automáticamente).
- El reemplazo toca ÚNICAMENTE las líneas entre los marcadores. Las líneas de los marcadores se preservan verbatim (mismo texto, mismo newline).
- El interior nuevo se inserta con el mismo estilo de newline del archivo.
- Si el interior nuevo está vacío, se deja una línea vacía entre los marcadores (no se colapsan).
- No se normaliza el contenido fuera del bloque; solo se reemplaza el interior.
- La línea del marcador puede tener espacios alrededor? No: se busca el marcador como subcadena, pero el estilo canónico es la línea sola con el marcador. Se recomienda que los marcadores ocupen su propia línea.

### 3) Verificación de hash del contenido fuera del bloque (integridad)

```python
def extract_outside(text: str) -> str:
    # todo el texto EXCEPTO el interior del bloque (los marcadores se incluyen)
    span = find_markers(text)
    lines = text.splitlines(keepends=True)
    before = "".join(lines[:span.inside_start])   # incluye marcador start
    after  = "".join(lines[span.inside_end:])     # incluye marcador end en adelante
    return before + after

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def verify_outside_integrity(original_text: str, written_text: str, outside_hash_before: str):
    outside_after = extract_outside(written_text)
    outside_hash_after = sha256(outside_after)
    if outside_hash_after != outside_hash_before:
        raise OutsideIntegrityError(expected=outside_hash_before, actual=outside_hash_after)
    # verificacion adicional: byte a byte del "afuera" (no solo hash)
    if extract_outside(original_text) != outside_after:
        raise OutsideByteMismatchError()

def _verify(self, path, original_text, new_text, outside_hash_before, new_inside, concept):
    written = path.read_text(encoding="utf-8")       # releer desde disco
    # a) outside hash
    verify_outside_integrity(original_text, written, outside_hash_before)
    # b) interior coincide con la sintesis validada
    span = find_markers(written)
    if normalize(span.raw_inside) != normalize(new_inside):
        raise InsideMismatchError()
    # c) frontmatter/titulo/navegacion/wikilinks siguen presentes
    verify_frontmatter_preserved(original_text, written)
    verify_headings_preserved(original_text, written, required=["Que abarca", "Relacionados"])
    verify_wikilinks_preserved(original_text, written)
    # d) marcadores siguen siendo exactamente uno de cada
    if count_markers(written) != (1, 1):
        raise MarkerCountError()
```

Reglas:
- Hash SHA-256 del "afuera" (todo excepto interior) calculado ANTES y DESPUÉS. Si difiere → restaurar backup.
- Verificación adicional byte a byte del afuera (no solo hash) para detectar colisiones o cambios sutiles.
- Si falla cualquier verificación → restaurar backup y marcar `failed` (estado `failed`, fase `writing`).
- La verificación se hace RELEIENDO el archivo desde disco (no confiar en el buffer en memoria).
- Se verifica también que el interior escrito coincida con la síntesis validada (no se corrompió en el camino).

### 4) Frontmatter YAML preservado

```python
def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    # devuelve (frontmatter_dict, body_sin_frontmatter)
    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        return None, text
    # buscar cierre ---
    ...

def verify_frontmatter_preserved(original: str, written: str):
    fm_before, _ = parse_frontmatter(original)
    fm_after, _  = parse_frontmatter(written)
    # verificacion principal: byte a byte del bloque ---...---
    block_before = extract_frontmatter_block(original)
    block_after  = extract_frontmatter_block(written)
    if block_before != block_after:
        raise FrontmatterChangedError(before=block_before, after=block_after)
    # red de seguridad: comparacion semantica
    if fm_before != fm_after:
        raise FrontmatterSemanticMismatchError(before=fm_before, after=fm_after)

def extract_frontmatter_block(text: str) -> str | None:
    # devuelve el texto entre el primer --- y el cierre --- (inclusive), o None
    ...
```

Reglas:
- El frontmatter YAML (entre `---`) se preserva byte a byte. Si difiere → error.
- Comparación semántica (dict) como red de seguridad, pero la verificación principal es byte a byte del bloque `---...---`.
- Si el archivo no tiene frontmatter, no se agrega uno.
- Campos como `title`, `area`, `numero`, `aliases`, `tags` nunca se tocan.
- El writer NUNCA reescribe el frontmatter; solo lo verifica.
- Si se necesita regenerar el cuerpo completo (caso excepcional), se usa `preserve_frontmatter()` para reinyectar el frontmatter original al inicio.

### 5) Normalización de newlines

```python
def detect_newline(text: str) -> str:
    # detecta el fin de linea dominante del archivo original
    crlf = text.count("\r\n")
    lf   = text.count("\n") - crlf
    return "\r\n" if crlf > lf else "\n"

def normalize_newlines(text: str, target: str) -> str:
    # unificar a \n y luego convertir al estilo detectado
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if target == "\r\n":
        text = text.replace("\n", "\r\n")
    return text

def write_bytes(path: Path, text: str, newline: str):
    data = normalize_newlines(text, newline).encode("utf-8")
    path.write_bytes(data)
```

Reglas:
- Se detecta el fin de línea del archivo original (CRLF o LF) y se respeta.
- Toda escritura normaliza el interior nuevo al estilo detectado.
- El afuera (no tocado) conserva sus newlines originales porque no se reescribe.
- Codificación siempre UTF-8 (sin BOM). Si el archivo original tenía BOM, se preserva el BOM en el afuera (no se elimina).
- No se normalizan espacios finales ni se agregan trailing newlines fuera del bloque.
- Detección de edición concurrente también contempla cambios de newline (si el archivo cambió, el hash del afuera cambia).

### 6) Qué se escribe y qué no

```python
WRITES = {
    "interior del bloque ai:start/ai:end": "contenido sintetizado y validado (Markdown)",
}

DOES_NOT_WRITE = [
    "frontmatter YAML (title, area, numero, aliases, tags)",
    "titulo H1 y headings de la nota",
    "seccion 'Que abarca' (key_ideas manuales)",
    "seccion 'Relacionados' (wikilinks manuales)",
    "navegacion/indices/links fuera del bloque",
    "archivos de estado (estado.json)  -> eso lo hace state.py, no el writer",
    "backups -> se crean, no se modifican notas",
    "archivos de log -> runner.py",
]
```

Tabla de qué se escribe:

| Zona del archivo | ¿Se escribe? | Quién lo gestiona |
|---|---|---|
| Interior del bloque `ai:start`/`ai:end` | SÍ (solo esta zona) | writer.py |
| Marcadores `ai:start` / `ai:end` | NO (se preservan) | writer.py (verifica) |
| Frontmatter YAML | NO | writer.py (verifica) |
| Título, headings, navegación | NO | writer.py (verifica) |
| "Que abarca" / "Relacionados" | NO | writer.py (verifica) |
| Resto del cuerpo | NO | writer.py (verifica) |

Reglas:
- Principio de mínimo privilegio: el writer solo tiene permiso de modificar el interior del bloque.
- Todo lo demás es read-only para el writer; se verifica pero no se toca.
- Si se necesita agregar marcadores a una nota sin bloque → NO se hace automáticamente (queda `failed` con `missing_markers`), salvo config explícita (`auto_insert_markers: true`, desactivado por defecto).
- El writer no crea notas nuevas; solo modifica existentes con bloque.
- El writer no borra archivos ni hace operaciones de git.
- El writer no escribe en `estado.json` ni en logs; eso es responsabilidad de `state.py` y `runner.py`.

### Integración con el estado (Capa 3) y validación (Capa 8)

```python
def writing_phase(concept_id: str, synthesis: Synthesis, dry_run: bool = False):
    concept = load_concept(concept_id)
    writer = get_writer()                      # singleton de la corrida
    try:
        result = writer.write_concept(concept, synthesis, dry_run=dry_run)
        if dry_run:
            log_diff(concept_id, result)
            return                               # no cambia estado
        state = load_state(concept_id)
        state.status = ConceptStatus.DONE
        state.checkpoint = "writing"
        state.phase_data["write_result"] = {
            "backup_path": str(result.backup_path),
            "outside_hash": result.outside_hash,
            "inside_hash": result.inside_hash,
            "written_at": now_iso(),
            "writer_version": WRITER_VERSION,
        }
        persist_state(concept_id, state)          # atomica
    except (MissingMarkersError, DuplicateMarkersError, MarkerOrderError,
            ConcurrentEditError, OutsideIntegrityError, OutsideByteMismatchError,
            FrontmatterChangedError, FrontmatterSemanticMismatchError,
            InsideMismatchError, MarkerCountError, WriteFailedError) as e:
        mark_failed(concept_id, phase="writing", error=str(e))
        # el backup ya fue restaurado dentro del writer
        raise
```

### Excepciones del writer

```python
class WriterError(Exception): ...
class MissingMarkersError(WriterError): ...        # no hay ai:start o ai:end
class DuplicateMarkersError(WriterError): ...      # mas de uno de algun marcador
class MarkerOrderError(WriterError): ...          # start despues de end
class ConcurrentEditError(WriterError): ...       # el archivo cambio entre lectura y escritura
class OutsideIntegrityError(WriterError): ...     # hash del afuera difiere
class OutsideByteMismatchError(WriterError): ...  # afuera difiere byte a byte
class FrontmatterChangedError(WriterError): ...   # frontmatter byte a byte difiere
class FrontmatterSemanticMismatchError(WriterError): ...
class InsideMismatchError(WriterError): ...       # interior escrito != sintesis validada
class MarkerCountError(WriterError): ...          # marcadores != 1/1 tras escribir
class WriteFailedError(WriterError): ...          # fallo generico tras restore
```

### Reglas de negocio (de la spec)
- Solo se modifica el interior del bloque `ai:start`/`ai:end`. Todo lo demás se verifica byte a byte.
- Si faltan marcadores, no se insertan automáticamente (salvo config explícita). El concepto queda `failed`.
- Backup antes de escribir. Hash del afuera antes y después.
- Fin de línea y codificación se respetan (se detectan del archivo original).
- Detección de edición concurrente: se compara mtime/hash para detectar si Obsidian modificó el archivo entre lectura y escritura.
- Modo `--dry-run`: genera todo y muestra el diff sin escribir.
- No se adivina: si faltan marcadores, falla (no se inventan).
- Verificación releyendo desde disco (no confiar en buffer).
- Restauración byte a byte del backup ante cualquier fallo de verificación.
- El writer es la única pieza que toca el vault; investigación/síntesis/validación solo leen.

---

## Capa 6 — Investigación (research.py + strategy.py) (pseudo-código de alto nivel)

### Objetivo de la capa
Construir el plan de investigación para un concepto, ejecutarlo contra el backend (deep research), seleccionar y deduplicar fuentes, y persistir tanto las fuentes (`sources.json`) como el resultado crudo (`raw_research.json`). Todo ocurre después de tener backend, estados y writer, y antes de la síntesis (Capa 7). Esta capa NO escribe en el vault: solo lee el concepto y persiste artefactos en `workdir/concepts/<concept_id>/`.

### 1) Contexto de investigación (`ResearchContext`)

Antes de generar queries, se arma un contexto a partir del `ConceptMeta` (Capa 1) y del estado del concepto. Es la "materia prima" que alimenta tanto el generador de queries como la estrategia de fuentes.

```python
@dataclass
class ResearchContext:
    concept_id: str
    title: str
    area: str                           # ej. "frontend", "data", "infra"
    key_ideas: list[str]                # de "Que abarca"
    connections: list[str]              # wikilinks de "Relacionados"
    volatility: Volatility              # STABLE | SEMI_STABLE | DYNAMIC (de config/area)
    last_researched_at: datetime | None # para decidir re-investigar
    manual_notes: str | None            # contenido manual fuera del bloque (si existe)
    extra_hints: list[str]              # hints del usuario (CLI --hint)

class Volatility(Enum):
    STABLE     = "stable"      # fundamento (HTTP, TCP, Big-O): re-investigar cada 90d
    SEMI_STABLE= "semi_stable" # frameworks con versiones (React 18/19): 30d
    DYNAMIC    = "dynamic"     # herramientas/CLI/APIs: 7d
```

Reglas:
- `volatility` se deriva del área + tags del concepto, con override en config (ej. `area_overrides: {frontend: semi_stable}`).
- Si `last_researched_at` está dentro de la ventana de frescura (`freshness_window_days[volatility]`) → se puede saltar la investigación (idempotencia / cache), salvo `--force`.
- `manual_notes` se incluye en el prompt como "contexto previo del autor" para que la síntesis no lo contradiga sin justificar.

### 2) Generación de queries de investigación según contexto del concepto

El generador produce un `ResearchPlan` (lista de `ResearchQuestion` con `qid` y `group` a/b/c) a partir del contexto. Las preguntas se agrupan por dimensión pedagógica: **a) fundamento estable**, **b) práctica moderna**, **c) relaciones y casos de uso**. Cada grupo tiene entre 1 y N preguntas (configurable, default 3 por grupo = 9 en total).

```python
class QueryGenerator:
    def __init__(self, templates: PromptTemplates, config: ResearchConfig):
        self.templates = templates        # prompts editables (versionados)
        self.config = config

    def build_plan(self, ctx: ResearchContext) -> ResearchPlan:
        questions: list[ResearchQuestion] = []
        # Grupo A — fundamento estable (conceptos, definiciones, historia, invariantes)
        questions += self._group_a(ctx)
        # Grupo B — práctica moderna (estado del arte, versiones, herramientas, pitfalls)
        questions += self._group_b(ctx)
        # Grupo C — relaciones, casos de uso, comparaciones, anti-patrones
        questions += self._group_c(ctx)
        # Preguntas derivadas de connections y key_ideas (auto)
        questions += self._derived(ctx)
        return ResearchPlan(questions=dedup_questions(questions))

    def _group_a(self, ctx) -> list[ResearchQuestion]:
        base = [
            f"¿Qué es {ctx.title} y cuáles son sus conceptos fundamentales e invariantes?",
            f"¿Cuál es la historia/evolución de {ctx.title} y qué problemas resuelve?",
            f"¿Qué definiciones y modelos canónicos existen para {ctx.title}?",
        ]
        # enriquecer con key_ideas
        for idea in ctx.key_ideas:
            base.append(f"Explicá en profundidad: {idea} (en el contexto de {ctx.title}).")
        return [ResearchQuestion(qid=f"a{i+1}", group="a", text=q) for i, q in enumerate(base)]

    def _group_b(self, ctx) -> list[ResearchQuestion]:
        base = [
            f"¿Cuál es el estado del arte actual de {ctx.title} (versiones, herramientas, prácticas)?",
            f"¿Qué cambió recientemente en {ctx.title} y qué se considera obsoleto?",
            f"¿Cuáles son los pitfalls/errores comunes al usar {ctx.title} hoy?",
        ]
        # si es dinámico, agregar query de "última versión"
        if ctx.volatility == Volatility.DYNAMIC:
            base.append(f"¿Cuál es la última versión estable de las herramientas principales de {ctx.title} y sus breaking changes?")
        return [ResearchQuestion(qid=f"b{i+1}", group="b", text=q) for i, q in enumerate(base)]

    def _group_c(self, ctx) -> list[ResearchQuestion]:
        base = [
            f"¿Cómo se relaciona {ctx.title} con: {', '.join(ctx.connections)}?",
            f"¿En qué casos de uso reales se aplica {ctx.title} y cuándo NO usarlo?",
            f"¿Qué alternativas/tecnologías comparables existen y cómo se diferencian?",
        ]
        # hints manuales
        for h in ctx.extra_hints:
            base.append(h)
        return [ResearchQuestion(qid=f"c{i+1}", group="c", text=q) for i, q in enumerate(base)]

    def _derived(self, ctx) -> list[ResearchQuestion]:
        # preguntas auto-generadas a partir de key_ideas + connections (sin duplicar)
        out = []
        for conn in ctx.connections:
            out.append(ResearchQuestion(
                qid=f"d{len(out)+1}", group="c",
                text=f"¿Cómo interactúa {ctx.title} con {conn} en un sistema real?"))
        return out

def dedup_questions(qs: list[ResearchQuestion]) -> list[ResearchQuestion]:
    seen = set()
    out = []
    for q in qs:
        key = normalize(q.text)
        if key in seen:
            continue
        seen.add(key)
        out.append(q)
    # renumerar qids por grupo para que sean estables (a1..aN, b1..bN, c1..cN)
    return renumber(qs=out)
```

Reglas:
- Las templates de preguntas viven en archivos editables (ej. `prompts/research_group_a.md`) y se pueden sobrescribir por área (`prompts/areas/frontend.md`). El generador usa las templates si existen, si no, los defaults de arriba.
- `dedup_questions` evita preguntas repetidas (por normalización de texto: lowercase + colapso de espacios).
- El número total de preguntas se limita por `max_questions_per_concept` (config, default 12). Si se excede, se priorizan a > b > c > derived y se truncan.
- Cada pregunta debe ser autocontenida (incluye el nombre del concepto) porque el backend no tiene contexto previo del vault.
- Las preguntas NO piden formato de salida; el formato lo impone la síntesis (Capa 7). Aquí solo se pide contenido.

### 3) Estrategia de fuentes (`strategy.py`)

La estrategia define **dónde** buscar: seeds (URLs fijas), dominios preferidos y dominios por área. Se combina con la volatilidad para definir la ventana de frescura.

```python
@dataclass
class SourceStrategy:
    seed_urls: list[str]                # URLs fijas siempre incluidas (docs oficiales, RFCs)
    preferred_domains: list[str]        # dominios con prioridad alta (ej. developer.mozilla.org)
    blocked_domains: list[str]         # dominios a excluir (spam, paywalls duros)
    area_domains: dict[str, list[str]]  # dominios sugeridos por area
    max_sources: int                    # tope de fuentes a subir al backend
    min_sources: int                    # minimo para considerar "cobertura suficiente"
    freshness_window_days: dict[Volatility, int]

# config/strategy.yaml (ejemplo)
strategy:
  seed_urls:
    - "https://developer.mozilla.org/"
  preferred_domains:
    - "developer.mozilla.org"
    - "web.dev"
    - "github.com"
  blocked_domains:
    - "pinterest.com"
  area_domains:
    frontend:  ["developer.mozilla.org", "web.dev", "react.dev", "vuejs.org"]
    backend:   ["docs.python.org", "nodejs.org", "postgresql.org"]
    data:      ["pandas.pydata.org", "scikit-learn.org"]
    infra:     ["kubernetes.io", "docs.docker.com"]
  max_sources: 12
  min_sources: 4
  freshness_window_days:
    stable:      90
    semi_stable: 30
    dynamic:      7
```

```python
class StrategyResolver:
    def __init__(self, config: StrategyConfig, area_overrides: dict):
        self.config = config
        self.area_overrides = area_overrides

    def resolve(self, ctx: ResearchContext) -> ResolvedStrategy:
        seeds = list(self.config.seed_urls)                       # copia
        # seeds por concepto (de config/concepts/<id>.yaml si existe)
        seeds += load_concept_seeds(ctx.concept_id)                # puede estar vacio
        preferred = list(self.config.preferred_domains)
        preferred += self.config.area_domains.get(ctx.area, [])
        # override de area (si el concepto pide dominios extra)
        preferred += self.area_overrides.get(ctx.concept_id, [])
        preferred = dedup(preferred)
        blocked = list(self.config.blocked_domains)
        freshness = self.config.freshness_window_days[ctx.volatility]
        return ResolvedStrategy(
            seed_urls=seeds,
            preferred_domains=preferred,
            blocked_domains=blocked,
            max_sources=self.config.max_sources,
            min_sources=self.config.min_sources,
            freshness_days=freshness,
        )

    def is_preferred(self, url: str, strategy: ResolvedStrategy) -> bool:
        host = hostname(url)
        return any(host == d or host.endswith("." + d) for d in strategy.preferred_domains)

    def is_blocked(self, url: str, strategy: ResolvedStrategy) -> bool:
        host = hostname(url)
        return any(host == d or host.endswith("." + d) for d in strategy.blocked_domains)
```

Reglas:
- `seed_urls` se incluyen SIEMPRE (aunque el backend también haga búsqueda abierta). Son la base de "fuentes canónicas" (docs oficiales, RFCs).
- `preferred_domains` ordenan/priorizan; no excluyen otras fuentes, pero las seeds/preferred tienen peso mayor en la selección (seccion 5).
- `blocked_domains` se filtran antes de subir al backend.
- La estrategia es por concepto (se resuelve con el área del concepto) pero se puede sobrescribir por concepto (`concepts/<id>.yaml`).
- Dominios por área: se cargan de config; si un área no está, se usa la lista global.
- `max_sources` limita cuántas fuentes se suben al backend (costo/tiempo). `min_sources` es el piso para considerar cobertura suficiente.

### 4) Deep research vía backend

La fase de investigación usa el backend (Capa 4) para ejecutar el plan. El ciclo incluye: crear notebook, subir fuentes, ejecutar las preguntas por grupo, evaluar cobertura, y si hay brechas (gap), hacer una segunda pasada con preguntas refinadas.

```python
async def research_phase(concept_id: str, ctx: ResearchContext):
    backend = get_backend()                       # singleton de la corrida
    state = load_state(concept_id)
    plan = build_plan(ctx)                        # QueryGenerator
    strategy = resolve_strategy(ctx)               # StrategyResolver
    sources = build_sources(ctx, strategy)         # SourceSelector (seeds + candidatas)

    # notebook_id persistido para reanudar
    notebook_id = state.phase_data.get("notebook_id")
    try:
        if not notebook_id:
            notebook_id = await backend.create_notebook(load_concept(concept_id))
            state.phase_data["notebook_id"] = notebook_id
            persist_state(concept_id, state)

        # subir fuentes (idempotente: si ya existen source_ids, saltar)
        source_ids = state.phase_data.get("source_ids")
        if not source_ids:
            source_ids = await backend.add_sources(notebook_id, sources)
            state.phase_data["source_ids"] = source_ids
            persist_state(concept_id, state)

        # ejecutar preguntas (grupo a, b, c) — reanudable por pregunta
        answers = state.phase_data.get("answers", [])
        answered_qids = {a.qid for a in answers}
        for q in plan.questions:
            if q.qid in answered_qids:
                continue
            # backend.research puede ser por pregunta o batch; aca por pregunta
            result = await backend.research(notebook_id, ResearchPlan(questions=[q]))
            ans = result.answers[0]
            answers.append(ans)
            state.phase_data["answers"] = [asdict(a) for a in answers]
            state.phase_data["coverage"] = estimate_coverage(answers, sources)
            persist_state(concept_id, state)

        # ciclo de cobertura: si hay gap, segunda pasada con preguntas refinadas
        coverage = state.phase_data["coverage"]
        if coverage < config.coverage_threshold and not state.phase_data.get("gap_pass_done"):
            gap_questions = detect_gaps(answers, plan, sources)   # preguntas que quedaron sin respuesta
            if gap_questions:
                for q in gap_questions:
                    result = await backend.research(notebook_id, ResearchPlan(questions=[q]))
                    answers.append(result.answers[0])
                state.phase_data["answers"] = [asdict(a) for a in answers]
                state.phase_data["coverage"] = estimate_coverage(answers, sources)
                state.phase_data["gap_pass_done"] = True
                persist_state(concept_id, state)

        # persistir artefactos
        persist_sources(concept_id, sources)            # sources.json
        persist_raw_research(concept_id, plan, answers, sources, coverage)

        # limpiar notebook (best-effort) si config.cleanup_notebooks
        if config.cleanup_notebooks:
            await safe_delete(backend, notebook_id)
            state.phase_data.pop("notebook_id", None)
            persist_state(concept_id, state)

    except BackendAuthError as e:
        mark_blocked(concept_id, "auth", str(e))
        await safe_delete(backend, notebook_id)
        raise
    except (BackendTimeout, BackendNetworkError, BackendRateLimitError) as e:
        await safe_delete(backend, notebook_id)
        raise   # Capa 3 reintenta
```

Funciones auxiliares:

```python
def build_sources(ctx: ResearchContext, strategy: ResolvedStrategy) -> list[Source]:
    sources: list[Source] = []
    # 1. seeds (siempre)
    for url in strategy.seed_urls:
        sources.append(Source(source_id=slug(url), url=url, title=guess_title(url),
                              snippet=None, kind="url"))
    # 2. candidatas de busqueda abierta (si el backend soporta search; si no, solo seeds)
    candidates = open_search(ctx, strategy)            # ver abajo
    for c in candidates:
        if strategy.is_blocked(c.url, strategy):
            continue
        sources.append(c)
    # 3. dedup + cap
    sources = dedup_sources(sources)
    sources = rank_and_cap(sources, strategy)          # preferred primero, hasta max_sources
    return sources

def open_search(ctx, strategy) -> list[Source]:
    # Si el backend expone search (NotebookLM no siempre). Fallback: lista vacia -> solo seeds.
    # En v1, la "busqueda abierta" se simula con una lista de URLs candidatas
    # aportadas por config (concept_search_urls) o por un buscador externo pluggable.
    return search_provider.search(f"{ctx.title} {ctx.area}", preferred=strategy.preferred_domains)

def estimate_coverage(answers: list[ResearchAnswer], sources: list[Source]) -> float:
    # heuristica: fraccion de preguntas con al menos 1 claim trazable a source_id
    if not answers:
        return 0.0
    ok = sum(1 for a in answers if a.claims and any(c.source_ids for c in a.claims))
    base = ok / len(answers)
    # bonus por cantidad de fuentes distintas citadas
    cited = {sid for a in answers for c in a.claims for sid in c.source_ids}
    diversity = min(1.0, len(cited) / max(1, len(sources) * 0.5))
    return round(0.7 * base + 0.3 * diversity, 3)

def detect_gaps(answers, plan, sources) -> list[ResearchQuestion]:
    # preguntas cuya respuesta es vacia/corta o sin claims -> re-preguntar reformulada
    gaps = []
    for q in plan.questions:
        ans = next((a for a in answers if a.qid == q.qid), None)
        if ans is None or not ans.claims or len(ans.answer_md.strip()) < 120:
            gaps.append(reformulate(q))   # ej. agregar "con ejemplos y fuentes"
    return gaps[:3]   # tope de re-preguntas
```

Reglas:
- Reanudable por pregunta: si el proceso se corta, se retoma desde la última pregunta persistida (no se repiten las ya respondidas).
- El notebook se crea una vez por concepto y se persiste su id en `phase_data`. Si falla a mitad, el reintento reutiliza el mismo notebook (no crea otro).
- Cobertura objetivo: `coverage_threshold` (config, default 0.7). Si no se alcanza tras la pasada de gaps, se persiste igual pero se marca `low_coverage: true` en `raw_research.json` (la síntesis y validación lo tendrán en cuenta).
- Limpieza de notebooks: best-effort; si falla el delete, se registra en log pero no bloquea (el notebook queda huérfano, se reporta al final del lote).
- `open_search` es pluggable: en v1 puede ser una lista estática por concepto (`concept_search_urls` en config) o un buscador externo. El backend (NotebookLM) NO busca en la web por su cuenta en esta arquitectura; las URLs se le entregan como fuentes.

### 5) Selección y deduplicación de fuentes

Antes de subir al backend, las fuentes candidatas se deduplican y rankean.

```python
def dedup_sources(sources: list[Source]) -> list[Source]:
    seen_urls: set[str] = set()
    seen_hosts_paths: set[str] = set()
    out = []
    for s in sources:
        if s.url:
            norm = normalize_url(s.url)               # sin trailing slash, sin query params ruidosos, lowercase host
            if norm in seen_urls:
                continue
            seen_urls.add(norm)
            # dedup por (host, path) para evitar el mismo doc con params distintos
            key = f"{hostname(s.url)}{path(s.url)}"
            if key in seen_hosts_paths:
                continue
            seen_hosts_paths.add(key)
        # dedup por titulo normalizado (para fuentes de texto pegado)
        if s.kind == "text":
            tkey = normalize(s.title)
            if tkey in {normalize(x.title) for x in out if x.kind == "text"}:
                continue
        out.append(s)
    return out

def rank_and_cap(sources: list[Source], strategy: ResolvedStrategy) -> list[Source]:
    # score: seeds/preferred primero, luego el resto; estable por orden de llegada
    def score(s: Source) -> tuple[int, int]:
        is_seed = 1 if s.url in strategy.seed_urls else 0
        is_pref = 1 if (s.url and strategy.is_preferred(s.url, strategy)) else 0
        return (-(is_seed + is_pref), sources.index(s))   # mas alto primero, estable
    ranked = sorted(sources, key=score)
    return ranked[:strategy.max_sources]

def normalize_url(url: str) -> str:
    u = urlparse(url)
    # quitar fragmento y params de tracking (utm_*, fbclid, etc.)
    qs = {k: v for k, v in parse_qs(u.query).items() if not k.startswith("utm_") and k not in {"fbclid", "gclid"}}
    query = urlencode(qs, doseq=True)
    path = u.path.rstrip("/") or "/"
    return urlunparse((u.scheme, u.netloc.lower(), path, "", query, ""))

def build_sources(ctx, strategy) -> list[Source]:
    ...  # ver seccion 3/4
```

Reglas:
- Dedup por URL normalizada (sin tracking params, sin trailing slash) y por `(host, path)`.
- Fuentes de texto pegado (`kind="text"`) se dedupan por título normalizado.
- Rankeo: seeds y preferred_domains primero (mayor peso), luego el resto; orden estable (no aleatorio) para reproducibilidad.
- Cap en `max_sources` (default 12). Si hay menos de `min_sources` tras dedup → se registra `low_sources: true` en `raw_research.json` (no falla, pero la validación lo penaliza).
- `blocked_domains` se filtran antes de dedup (no se cuentan).
- Si una seed URL falla al subirse (timeout), se registra pero no detiene el resto (best-effort por fuente).

### 6) Estructura del resultado de investigación

Lo que se persiste en disco por concepto:

```
workdir/concepts/<concept_id>/
├── sources.json          # lista final de fuentes usadas (post dedup/cap)
└── raw_research.json     # plan + respuestas + cobertura + metadata
```

#### `sources.json`

```json
{
  "concept_id": "frontend-01-internet-web",
  "generated_at": "2026-10-22T10:00:00Z",
  "strategy": {
    "seed_urls": ["https://developer.mozilla.org/"],
    "preferred_domains": ["developer.mozilla.org", "web.dev"],
    "max_sources": 12,
    "min_sources": 4
  },
  "sources": [
    {
      "source_id": "src-1",
      "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP",
      "title": "HTTP - MDN",
      "snippet": null,
      "kind": "url",
      "preferred": true,
      "seed": true
    },
    {
      "source_id": "src-2",
      "url": null,
      "title": "RFC 9110 (pegado)",
      "snippet": "Resumen del RFC...",
      "kind": "text",
      "preferred": false,
      "seed": true
    }
  ],
  "counts": { "total": 8, "seeds": 2, "preferred": 5, "blocked_filtered": 1 }
}
```

#### `raw_research.json`

```json
{
  "concept_id": "frontend-01-internet-web",
  "researched_at": "2026-10-22T10:05:00Z",
  "volatility": "semi_stable",
  "freshness_window_days": 30,
  "plan": {
    "questions": [
      { "qid": "a1", "group": "a", "text": "¿Qué es Internet y cuáles son sus conceptos fundamentales?" },
      { "qid": "b1", "group": "b", "text": "¿Cuál es el estado del arte actual de HTTP/2 y HTTP/3?" }
    ]
  },
  "answers": [
    {
      "qid": "a1",
      "group": "a",
      "answer_md": "## Fundamento\nInternet es ...",
      "claims": [
        { "text": "TCP/IP es el protocolo base", "source_ids": ["src-1", "src-3"] }
      ]
    }
  ],
  "coverage": 0.83,
  "low_coverage": false,
  "low_sources": false,
  "gap_pass_done": true,
  "gaps_detected": 2,
  "gaps_resolved": 2,
  "notebook_id": null,
  "source_ids": ["src-1", "src-2", "src-3"],
  "duration_ms": 45230,
  "backend_provider": "notebooklm"
}
```

Estructuras Python:

```python
@dataclass
class PersistedSource:
    source_id: str
    url: str | None
    title: str
    snippet: str | None
    kind: Literal["url", "text", "file"]
    preferred: bool
    seed: bool

@dataclass
class PersistedAnswer:
    qid: str
    group: str
    answer_md: str
    claims: list[Claim]

@dataclass
class RawResearch:
    concept_id: str
    researched_at: str
    volatility: str
    freshness_window_days: int
    plan: ResearchPlan
    answers: list[PersistedAnswer]
    coverage: float
    low_coverage: bool
    low_sources: bool
    gap_pass_done: bool
    gaps_detected: int
    gaps_resolved: int
    notebook_id: str | None
    source_ids: list[str]
    duration_ms: int
    backend_provider: str

def persist_sources(concept_id: str, sources: list[Source]):
    path = workdir / "concepts" / concept_id / "sources.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "concept_id": concept_id,
        "generated_at": now_iso(),
        "strategy": {...},
        "sources": [asdict(normalize_source(s)) for s in sources],
        "counts": {...},
    }
    atomic_write_json(path, data)

def persist_raw_research(concept_id, plan, answers, sources, coverage):
    path = workdir / "concepts" / concept_id / "raw_research.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(RawResearch(...))
    atomic_write_json(path, data)
```

Reglas:
- `sources.json` y `raw_research.json` se escriben de forma atómica (temp + rename) en `workdir/concepts/<concept_id>/`. Nunca en el vault.
- `answers` se persisten con claims trazables a `source_id` (Capa 4). Si un claim no tiene source_id, se marca `unverified: true` (la validación lo penaliza).
- `notebook_id` se persiste mientras exista el notebook; si se limpió, queda `null`.
- `low_coverage` / `low_sources` son flags para la validación (Capa 8) y para el reporte final; no bloquean por sí solos.
- `freshness_window_days` se persiste para que la próxima corrida decida si re-investigar sin releer config.
- Si ya existe `raw_research.json` válido y está dentro de la ventana de frescura → se salta la investigación (idempotencia), salvo `--force` o `--re-research`.
- Los artefactos se versionan por timestamp solo si `keep_history: true` (config); por defecto se sobrescriben (último gana), pero se hace backup en `workdir/backups/<concept_id>/` antes de sobrescribir.

### 7) Integración con el estado (Capa 3)

```python
async def research_phase(concept_id: str):
    # ver seccion 4 (implementacion completa)
    ...
    # al terminar OK:
    state = load_state(concept_id)
    state.status = ConceptStatus.SYNTHESIZING   # siguiente fase
    state.checkpoint = "researching"
    state.phase_data["research_done"] = True
    state.phase_data["coverage"] = coverage
    state.phase_data["sources_path"] = str(workdir / "concepts" / concept_id / "sources.json")
    state.phase_data["raw_research_path"] = str(workdir / "concepts" / concept_id / "raw_research.json")
    persist_state(concept_id, state)
```

Mapeo de errores (Capa 4.5):
- `BackendAuthError` → `blocked` (renovar credenciales).
- `BackendTimeout` / `BackendNetworkError` / `BackendRateLimitError` → `failed` reintentable (vuelve a `researching`).
- `LowCoverageError` (si se configura como bloqueante) → `blocked` con detalle "cobertura insuficiente, revisar fuentes".
- Errores de IO (no se puede escribir `sources.json`) → `failed` reintentable.

### Excepciones de la capa

```python
class ResearchError(Exception): ...
class QueryGenerationError(ResearchError): ...     # no se pudo generar el plan
class StrategyError(ResearchError): ...           # estrategia invalida (ej. max_sources < min_sources)
class InsufficientSourcesError(ResearchError): ...# menos de min_sources tras dedup
class CoverageTooLowError(ResearchError): ...     # cobertura < threshold (solo si bloqueante)
class ResearchPersistError(ResearchError): ...    # fallo al escribir sources.json / raw_research.json
```

### Reglas de negocio (de la spec)
- La investigación NO escribe en el vault; solo persiste `sources.json` y `raw_research.json` en `workdir`.
- El plan de queries se deriva del contexto del concepto (título, área, key_ideas, connections, volatilidad, hints) y es editable vía templates versionados.
- Las fuentes se seleccionan con seeds + preferred_domains + dominios por área + búsqueda abierta; se deduplican y capan por `max_sources`.
- Deep research se ejecuta vía backend (Capa 4), con ciclo de cobertura y segunda pasada de gaps si no se alcanza el threshold.
- El resultado persistido incluye trazabilidad claim → source_id, cobertura, flags de baja cobertura/fuentes.
- Idempotencia: si `raw_research.json` está fresco (dentro de la ventana por volatilidad), se salta la investigación salvo `--force`.
- Reanudable por pregunta: un corte a mitad no repite las preguntas ya respondidas.
- `low_coverage` / `low_sources` no bloquean por sí solos; la validación (Capa 8) decide si son error o warning.
- El writer (Capa 5) y la síntesis (Capa 7) consumen `sources.json` y `raw_research.json`; esta capa no toca el vault.

---

## Capa 7 — Síntesis (synthesis.py + prompts) (pseudo-código de alto nivel)

### Objetivo de la capa
A partir de las fuentes persistidas (`sources.json` + `raw_research.json`), generar el contenido pedagógico (study guide) que se va a insertar en el vault. La síntesis transforma la investigación cruda (respuestas con claims trazables) en un documento Markdown normalizado, con secciones requeridas, separación entre fundamento estable y práctica moderna, y cross-links a conceptos vecinos. Los prompts que guían la generación son editables y versionados, y se seleccionan por contexto (frontend vs general, por área). Esta capa NO escribe en el vault: produce un objeto `Synthesis` validado que la Capa 8 (validación) chequea y la Capa 5 (writer) persiste.

### 1) Contexto de síntesis (`SynthesisContext`)

Antes de generar, se arma un contexto que combina el concepto (Capa 1), la investigación (Capa 6) y la configuración de prompts. Es la "materia prima" de la síntesis.

```python
@dataclass
class SynthesisContext:
    concept: ConceptMeta                  # titulo, area, key_ideas, connections
    raw_research: RawResearch              # plan + answers + claims + coverage
    sources: list[PersistedSource]         # sources.json
    volatility: Volatility                 # STABLE | SEMI_STABLE | DYNAMIC
    low_coverage: bool                      # flag de Capa 6
    low_sources: bool                      # flag de Capa 6
    manual_notes: str | None               # contenido manual previo del autor
    neighbor_concepts: list[ConceptMeta]   # conceptos conectados (para cross-links)
    prompt_context: PromptContext           # frontend | general | backend | data | infra
    prompt_version: str                    # version de los prompts usados

class PromptContext(Enum):
    FRONTEND = "frontend"
    BACKEND  = "backend"
    DATA     = "data"
    INFRA    = "infra"
    GENERAL  = "general"
```

Reglas:
- `prompt_context` se deriva del área del concepto con un mapeo configurable (`area_to_context: {frontend: frontend, backend: backend, ...}`). Si el área no está mapeada → `GENERAL`.
- `neighbor_concepts` se resuelve a partir de `concept.connections` (wikilinks) cruzando con el índice de conceptos del vault (Capa 2 scan). Solo se incluyen los que existen como concepto (con bloque ai). Los que no existen se marcan como "pendientes de crear" pero no se linkean como concepto.
- `manual_notes` se inyecta en el prompt como "contexto previo del autor" para que la síntesis no lo contradiga sin justificar (igual que en investigación).
- `low_coverage` / `low_sources` se propagan para que la síntesis marque secciones inciertas y la validación las penalice.

### 2) Templates de prompt por contexto (frontend vs general)

Los prompts son archivos Markdown editables y versionados en `prompts/`. Se organizan por contexto y por "rol" (system, synthesis, sections). La selección es por `prompt_context` + override por concepto.

Estructura de archivos:
```
prompts/
├── _base.md                     # instrucciones comunes (tono, formato, idioma)
├── system.md                    # rol del modelo (pedagogo, técnico, preciso)
├── contexts/
│   ├── frontend.md              # contexto frontend (ejemplos con HTML/CSS/JS, React)
│   ├── backend.md               # contexto backend (APIs, DB, servidores)
│   ├── data.md                  # contexto data (pipelines, ML, SQL)
│   ├── infra.md                 # contexto infra (Docker, K8s, CI/CD)
│   └── general.md               # fallback genérico
├── sections/
│   ├── definition.md            # cómo redactar la definición
│   ├── how_it_works.md          # cómo explicar el funcionamiento
│   ├── examples.md              # formato de ejemplos de código
│   ├── common_errors.md         # errores comunes y cómo evitarlos
│   └── cross_links.md           # cómo armar los cross-links
├── synthesis.md                 # prompt principal de síntesis (study guide)
└── versions.yaml                # versionado de prompts
```

```python
@dataclass
class PromptTemplate:
    name: str                      # ej. "synthesis"
    context: PromptContext          # frontend | general | ...
    version: str                   # ej. "1.2.0" (de versions.yaml)
    system: str                    # contenido de system.md + _base.md
    body: str                      # contenido del prompt principal
    sections: dict[str, str]       # nombre_seccion -> instrucciones
    hash: str                      # sha256 del contenido (para trazabilidad)

class PromptLoader:
    def __init__(self, prompts_dir: Path, versions_file: Path):
        self.prompts_dir = prompts_dir
        self.versions = load_versions(versions_file)   # versions.yaml

    def load(self, name: str, ctx: PromptContext, concept_override: str | None = None) -> PromptTemplate:
        # 1. resolver version activa
        version = self.versions.get(name, {}).get("active", "1.0.0")
        # override por concepto (config/concepts/<id>.yaml -> prompt_version)
        if concept_override:
            version = concept_override
        # 2. cargar base + system
        base = read_text(self.prompts_dir / "_base.md")
        system = read_text(self.prompts_dir / "system.md")
        # 3. cargar contexto (fallback a general si no existe)
        ctx_file = self.prompts_dir / "contexts" / f"{ctx.value}.md"
        if not ctx_file.exists():
            ctx_file = self.prompts_dir / "contexts" / "general.md"
        context_text = read_text(ctx_file)
        # 4. cargar prompt principal
        body = read_text(self.prompts_dir / f"{name}.md")
        # 5. cargar instrucciones por seccion
        sections = {}
        for sec in ["definition", "how_it_works", "examples", "common_errors", "cross_links"]:
            p = self.prompts_dir / "sections" / f"{sec}.md"
            if p.exists():
                sections[sec] = read_text(p)
        # 6. ensamblar
        full_system = base + "\n\n" + system + "\n\n" + context_text
        return PromptTemplate(
            name=name, context=ctx, version=version,
            system=full_system, body=body, sections=sections,
            hash=sha256(full_system + body + "".join(sections.values())),
        )

    def render(self, template: PromptTemplate, variables: dict) -> str:
        # reemplazo de variables {{var}} en body y sections
        text = template.body
        for k, v in variables.items():
            text = text.replace("{{" + k + "}}", str(v))
        return text
```

`versions.yaml` (ejemplo):
```yaml
prompts:
  synthesis:
    active: "1.2.0"
    history:
      - "1.0.0": "prompt inicial"
      - "1.1.0": "agregado seccion errores comunes"
      - "1.2.0": "templates por contexto frontend/backend"
  sections:
    definition: "1.0.0"
    how_it_works: "1.0.0"
    examples: "1.1.0"
    common_errors: "1.0.0"
    cross_links: "1.0.0"
```

Reglas:
- Los prompts son la única fuente de "cómo" se redacta. El código de síntesis no hardcodea texto pedagógico; solo orquesta variables y secciones.
- Fallback de contexto: si no existe `contexts/<ctx>.md`, se usa `general.md`. Nunca falla por falta de template de contexto.
- Override por concepto: `config/concepts/<id>.yaml` puede fijar `prompt_version` y `prompt_context` para casos especiales (ej. un concepto frontend que requiere contexto general).
- El hash del template se persiste en el resultado de síntesis para trazabilidad ("qué prompt generó este contenido").
- Los prompts se versionan en git junto al código; cambiar un prompt es un cambio de código (review + test).

Ejemplo de `contexts/frontend.md`:
```markdown
## Contexto: Frontend
- Usá ejemplos en HTML, CSS y JavaScript/TypeScript.
- Conectá con conceptos del navegador (DOM, eventos, fetch, rendering).
- Mencioná frameworks modernos (React, Vue, Svelte) solo como práctica, no como fundamento.
- Errores comunes típicos: CORS, hydration, memory leaks en efectos, re-renders.
- Cross-links esperados: HTTP, DOM, JavaScript async, CSS box model, bundlers.
```

Ejemplo de `contexts/general.md`:
```markdown
## Contexto: General
- Usá ejemplos en el lenguaje más natural para el concepto (Python o pseudocódigo si es agnóstico).
- Conectá con conceptos de ciencias de la computación (algoritmos, estructuras de datos, redes).
- Errores comunes típicos: off-by-one, null/undefined, race conditions.
- Cross-links esperados: los que figuren en "Relacionados" de la nota.
```

### 3) Generación del resumen/study guide a partir de las fuentes

La síntesis toma el `raw_research` (respuestas agrupadas a/b/c con claims trazables) y genera un study guide Markdown. Se hace en pasos: preparar el material, invocar el backend (o un LLM de síntesis) con el prompt ensamblado, normalizar la salida, separar fundamento/práctica, y armar cross-links.

```python
class Synthesizer:
    def __init__(self, backend: ResearchBackend, prompt_loader: PromptLoader, config: SynthesisConfig):
        self.backend = backend
        self.prompts = prompt_loader
        self.config = config

    async def synthesize(self, ctx: SynthesisContext) -> Synthesis:
        # 1. Preparar el material de entrada (investigacion cruda -> bloque de contexto)
        research_block = self._build_research_block(ctx.raw_research, ctx.sources)

        # 2. Cargar y renderizar el prompt principal
        template = self.prompts.load("synthesis", ctx.prompt_context, ctx.concept.prompt_version_override)
        variables = {
            "title": ctx.concept.title,
            "area": ctx.concept.area,
            "key_ideas": format_list(ctx.concept.key_ideas),
            "connections": format_list(ctx.concept.connections),
            "volatility": ctx.volatility.value,
            "low_coverage": str(ctx.low_coverage).lower(),
            "low_sources": str(ctx.low_sources).lower(),
            "manual_notes": ctx.manual_notes or "(sin notas manuales)",
            "research_block": research_block,
            "neighbor_concepts": format_list([c.title for c in ctx.neighbor_concepts]),
            "sections_required": ", ".join(REQUIRED_SECTIONS),
        }
        prompt_text = self.prompts.render(template, variables)

        # 3. Invocar la generacion (backend como LLM de sintesis, o LLM directo segun config)
        if self.config.use_backend_for_synthesis:
            # se reutiliza el notebook de investigacion (si existe) o se crea uno nuevo
            raw_md = await self._generate_via_backend(ctx, prompt_text)
        else:
            raw_md = await self._generate_via_llm(prompt_text, template.system)

        # 4. Normalizar la salida a Markdown canonico
        normalized = normalize_markdown(raw_md, ctx.concept)

        # 5. Separar fundamento estable / practica moderna
        sections = split_sections(normalized)          # dict section_name -> md
        stable = sections.get("fundamento", "")       # seccion de fundamento estable
        modern = sections.get("practica", "")         # seccion de practica moderna

        # 6. Armar cross-links (conceptos vecinos)
        cross_links = build_cross_links(ctx.concept, ctx.neighbor_concepts, sections)

        # 7. Ensamblar el Synthesis final
        synthesis = Synthesis(
            concept_id=ctx.concept.id,
            title=ctx.concept.title,
            markdown=render_final_markdown(sections, cross_links),
            sections=sections,
            stable_foundation=stable,
            modern_practice=modern,
            cross_links=cross_links,
            claims_index=extract_claims_index(ctx.raw_research),   # claim -> source_id
            prompt_template_hash=template.hash,
            prompt_version=template.version,
            prompt_context=ctx.prompt_context.value,
            generated_at=now_iso(),
            coverage=ctx.raw_research.coverage,
            low_coverage=ctx.low_coverage,
        )
        return synthesis

    def _build_research_block(self, raw: RawResearch, sources: list[PersistedSource]) -> str:
        # arma un bloque de texto con las respuestas agrupadas por grupo (a/b/c)
        # y la lista de fuentes, para inyectar en el prompt
        parts = []
        parts.append("## Fuentes disponibles")
        for s in sources:
            parts.append(f"- [{s.source_id}] {s.title} ({s.url or 'texto pegado'})")
        parts.append("")
        parts.append("## Investigación cruda (respuestas por grupo)")
        for group in ["a", "b", "c"]:
            parts.append(f"### Grupo {group.upper()} — {GROUP_LABELS[group]}")
            for ans in raw.answers:
                if ans.group != group:
                    continue
                parts.append(f"#### {ans.qid}")
                parts.append(ans.answer_md)
                if ans.claims:
                    parts.append("Claims trazables:")
                    for c in ans.claims:
                        srcs = ", ".join(c.source_ids) if c.source_ids else "(sin fuente)"
                        unverified = " [UNVERIFIED]" if getattr(c, "unverified", False) else ""
                        parts.append(f"  - {c.text} → {srcs}{unverified}")
        if raw.low_coverage:
            parts.append("")
            parts.append("NOTA: la cobertura de investigación fue baja; marcar secciones inciertas.")
        return "\n".join(parts)

    async def _generate_via_backend(self, ctx, prompt_text) -> str:
        # reutiliza el notebook de investigacion si existe y no se limpio;
        # si no, crea uno nuevo solo para sintesis
        backend = self.backend
        nb_id = ctx.raw_research.notebook_id
        if not nb_id:
            nb_id = await backend.create_notebook(ctx.concept)
        # envia el prompt de sintesis como una pregunta de chat
        result = await backend.research(nb_id, ResearchPlan(questions=[
            ResearchQuestion(qid="synth", group="s", text=prompt_text)
        ]))
        raw = result.answers[0].answer_md
        if ctx.raw_research.notebook_id is None and self.config.cleanup_notebooks:
            await safe_delete(backend, nb_id)
        return raw

    async def _generate_via_llm(self, prompt_text, system_text) -> str:
        # llamada directa a un LLM (configurable: openai/anthropic/local)
        # sin notebook; util para tests y desarrollo offline
        return await llm_client.complete(system=system_text, user=prompt_text)
```

Reglas:
- La síntesis se alimenta SIEMPRE de `raw_research.json` + `sources.json` (no re-investiga). Si faltan → error `MissingResearchError`.
- El material de entrada se agrupa por grupo (a/b/c) y se incluyen los claims trazables (claim → source_id) para que el modelo cite fuentes en el output.
- Si `low_coverage` es true, se agrega una nota al prompt para que el modelo marque secciones inciertas (y la validación lo penaliza si no lo hace).
- La generación puede ir por backend (reutilizando el notebook) o por LLM directo (configurable). El backend fake (Capa 4) permite probar sin red.
- `normalize_markdown` corrige formato (headings, code fences, listas) sin cambiar contenido.
- La separación fundamento/práctica es por headings canónicos (ver sección 4): `## Fundamento` y `## Práctica moderna`.

### 4) Secciones requeridas del output

El study guide generado debe contener, como mínimo, estas secciones (en este orden sugerido). La validación (Capa 8) verifica su presencia y calidad.

```python
REQUIRED_SECTIONS = [
    "definicion",        # qué es y por qué importa
    "como_funciona",     # mecanismo, modelo mental, flujo
    "ejemplos",          # código/ejemplos concretos
    "errores_comunes",   # pitfalls y cómo evitarlos
    "fundamento",        # base estable (invariantes, historia, estándares)
    "practica",          # estado del arte, versiones, herramientas actuales
    "relacionados",      # cross-links a conceptos vecinos
]

SECTION_TITLES = {
    "definicion":     "## Definición",
    "como_funciona":  "## Cómo funciona",
    "ejemplos":       "## Ejemplos",
    "errores_comunes":"## Errores comunes",
    "fundamento":     "## Fundamento (estable)",
    "practica":       "## Práctica moderna",
    "relacionados":   "## Relacionados / Ver también",
}

# Instrucciones por seccion (viven en prompts/sections/*.md, resumidas aqui)
SECTION_GUIDANCE = {
    "definicion": (
        "Definí el concepto en 2-4 oraciones, sin jerga innecesaria. "
        "Incluí: qué es, para qué sirve, y en qué contexto aparece. "
        "Cita la fuente principal entre corchetes [src-N]."
    ),
    "como_funciona": (
        "Explicá el mecanismo con un modelo mental claro. Usá pasos numerados o un diagrama textual. "
        "Separá lo que es invariante de lo que es implementación. "
        "Cita fuentes por afirmación [src-N]."
    ),
    "ejemplos": (
        "Al menos 2 ejemplos de código (o pseudocódigo) comentados. "
        "Un ejemplo mínimo (happy path) y uno con un caso límite o error. "
        "Indicá el lenguaje en el code fence. Cita la fuente del ejemplo si aplica."
    ),
    "errores_comunes": (
        "Lista de 3-6 errores típicos con: síntoma, causa raíz, y cómo evitarlo/corregirlo. "
        "Priorizá los que aparecen en la investigación (grupo b)."
    ),
    "fundamento": (
        "Base estable: definiciones canónicas, invariantes, estándares (RFCs), historia relevante. "
        "Este bloque cambia poco; citá fuentes estables [src-N]. "
        "NO incluir versiones ni herramientas específicas aquí."
    ),
    "practica": (
        "Estado del arte: versiones actuales, herramientas, prácticas recomendadas, qué se considera obsoleto. "
        "Separar claramente de 'fundamento'. Citar fuentes recientes [src-N]. "
        "Si low_coverage, marcar con '⚠️ por verificar'."
    ),
    "relacionados": (
        "Lista de conceptos vecinos con wikilink [[...]] y una frase de por qué se relacionan. "
        "Solo conceptos que existen en el vault; los inexistentes van como 'pendiente de crear'."
    ),
}
```

Reglas:
- Las secciones son obligatorias salvo config (`required_sections` configurable, default todas). Si falta una → la validación (Capa 8) la marca como error (no se escribe).
- El orden canónico es el de `REQUIRED_SECTIONS`; el modelo puede agregar subsecciones, pero las canónicas deben existir con ese heading exacto.
- `fundamento` y `practica` son la separación clave del diseño: fundamento estable (cambia cada 90d) vs práctica moderna (cambia cada 7-30d). Esto permite re-sintetizar solo la parte práctica cuando hay nueva info sin tocar el fundamento.
- Cada afirmación factual debe llevar cita `[src-N]` apuntando a un `source_id` de `sources.json`. Las afirmaciones sin cita se marcan `[UNVERIFIED]` (la validación las penaliza).
- `errores_comunes` se nutre principalmente del grupo b de investigación ("pitfalls"), pero puede incluir los del autor (manual_notes).
- `ejemplos` deben incluir al menos un code fence con lenguaje declarado; si el concepto no aplica código, se permite pseudocódigo con fence `text`.

### 5) Conexión con conceptos vecinos (cross-links)

Los cross-links conectan el concepto sintetizado con sus vecinos (de `concept.connections` y del índice del vault). Se generan como wikilinks de Obsidian con una frase explicativa, y se validan contra el vault (no se inventan conceptos).

```python
@dataclass
class CrossLink:
    target_concept_id: str | None    # None si el concepto no existe en el vault
    target_title: str                # titulo del concepto vecino (o texto del wikilink)
    wikilink: str                    # ej. "[[frontend-02-http|HTTP]]"
    reason: str                      # frase corta de por que se relacionan
    exists: bool                     # True si el concepto existe en el vault
    direction: Literal["out", "in", "both"]  # direccion de la relacion

def build_cross_links(concept: ConceptMeta, neighbors: list[ConceptMeta], sections: dict) -> list[CrossLink]:
    links: list[CrossLink] = []
    # 1. connections explicitas del concepto (de "Relacionados")
    for conn in concept.connections:
        target = find_concept_by_title_or_slug(conn, neighbors_index)  # busca en indice del vault
        if target is not None:
            links.append(CrossLink(
                target_concept_id=target.id,
                target_title=target.title,
                wikilink=f"[[{target.id}|{target.title}]]",
                reason=infer_reason(concept, target),   # del prompt o heuristica
                exists=True,
                direction="both",
            ))
        else:
            # concepto vecino no existe aun -> marcar como pendiente
            links.append(CrossLink(
                target_concept_id=None,
                target_title=conn,
                wikilink=f"[[{slug(conn)}|{conn}]]",   # wikilink "roto" intencional (Obsidian lo muestra como no creado)
                reason="concepto vecino aun no creado",
                exists=False,
                direction="out",
            ))
    # 2. cross-links adicionales sugeridos por la investigacion (grupo c: relaciones)
    extra = extract_suggested_links(sections.get("relacionados", ""))
    for e in extra:
        if e not in {l.target_title for l in links}:
            links.append(e)
    # 3. dedup por target
    return dedup_cross_links(links)

def infer_reason(concept: ConceptMeta, target: ConceptMeta) -> str:
    # heuristica: compartir area -> "mismo area"; sino, usar el texto de la seccion relacionados
    if concept.area == target.area:
        return f"mismo área ({concept.area}); se complementan"
    # buscar en manual_notes o en la investigacion una frase que mencione ambos
    return "relacionado (ver sección Relacionados)"

def render_cross_links(links: list[CrossLink]) -> str:
    lines = ["## Relacionados / Ver también", ""]
    for l in links:
        status = "" if l.exists else " *(pendiente de crear)*"
        lines.append(f"- {l.wikilink} — {l.reason}{status}")
    if not links:
        lines.append("- (sin conceptos vecinos registrados)")
    return "\n".join(lines)
```

Reglas:
- Solo se generan wikilinks a conceptos que existen en el índice del vault (o se marcan como "pendiente de crear"). Nunca se inventan títulos de conceptos.
- Los wikilinks usan el `concept_id` (slug del path) como target, con alias al título: `[[concept_id|Título]]`. Esto garantiza que Obsidian resuelva el link aunque el archivo se renombre.
- Si un concepto vecino no existe, el wikilink queda "roto" intencionalmente (Obsidian lo muestra como no creado) y se marca como pendiente. La validación lo reporta como warning, no error.
- La dirección (`out`/`in`/`both`) se registra para futuras mejoras (backlinks). En v1 solo se usan `out` (del concepto actual hacia el vecino).
- `build_cross_links` es idempotente: re-ejecutar con los mismos inputs produce los mismos links (orden estable por orden de `concept.connections`).
- Los cross-links se renderizan en la sección `## Relacionados / Ver también` del output (sección requerida).

### 6) Cómo se estructura el resultado de síntesis

El resultado de la síntesis es un objeto `Synthesis` que se persiste como artefacto intermedio (`synthesis.json`) y se pasa a la validación (Capa 8) y al writer (Capa 5).

```python
@dataclass
class Synthesis:
    concept_id: str
    title: str
    markdown: str                       # Markdown final normalizado (lo que se escribe en el vault)
    sections: dict[str, str]           # nombre_seccion -> contenido md (sin heading)
    stable_foundation: str             # seccion "fundamento" extraida
    modern_practice: str               # seccion "practica" extraida
    cross_links: list[CrossLink]
    claims_index: list[ClaimRef]        # afirmaciones -> source_id (trazabilidad)
    prompt_template_hash: str           # hash del prompt usado
    prompt_version: str                # version del prompt
    prompt_context: str                # frontend | general | ...
    generated_at: str                 # iso8601
    coverage: float                   # cobertura de la investigacion
    low_coverage: bool                # flag propagado

@dataclass
class ClaimRef:
    claim_text: str
    source_ids: list[str]
    section: str                       # en que seccion del output aparece
    unverified: bool                  # True si no tiene source_id

def extract_claims_index(raw: RawResearch) -> list[ClaimRef]:
    # recorre las respuestas y arma un indice plano claim -> source_id
    # (se usa para trazabilidad y para la validacion semantica)
    out = []
    for ans in raw.answers:
        for c in ans.claims:
            out.append(ClaimRef(
                claim_text=c.text,
                source_ids=list(c.source_ids),
                section=group_to_section(ans.group),   # a->fundamento, b->practica, c->relacionados
                unverified=(len(c.source_ids) == 0),
            ))
    return out

def group_to_section(group: str) -> str:
    return {"a": "fundamento", "b": "practica", "c": "relacionados"}.get(group, "definicion")

def render_final_markdown(sections: dict[str, str], cross_links: list[CrossLink]) -> str:
    # ensambla el Markdown final en orden canonico
    parts = []
    for sec in REQUIRED_SECTIONS:
        if sec not in sections:
            continue
        parts.append(SECTION_TITLES[sec])
        parts.append("")
        parts.append(sections[sec].strip())
        parts.append("")
    # seccion de relacionados se renderiza con los cross-links resueltos
    if "relacionados" in sections:
        # reemplazar el contenido de relacionados por el render de cross_links
        idx = parts.index(SECTION_TITLES["relacionados"]) if SECTION_TITLES["relacionados"] in parts else None
        ...
    parts.append(render_cross_links(cross_links))
    return "\n".join(parts).strip() + "\n"

def normalize_markdown(raw: str, concept: ConceptMeta) -> str:
    # 1. normalizar headings: asegurar que las secciones canonicas usen ## y el titulo exacto
    # 2. normalizar code fences: cerrar fences abiertos, declarar lenguaje si falta (default text)
    # 3. normalizar listas: bullets con "- ", numeradas con "1. "
    # 4. eliminar lineas vacias triples
    # 5. asegurar un solo trailing newline
    ...

def split_sections(md: str) -> dict[str, str]:
    # parsea headings ## y devuelve dict section_key -> contenido (sin el heading)
    # mapea titulo -> key via SECTION_TITLES invertido
    ...
```

Persistencia:
```
workdir/concepts/<concept_id>/
├── sources.json
├── raw_research.json
└── synthesis.json          # NUEVO: resultado de la sintesis
```

```python
@dataclass
class PersistedSynthesis:
    concept_id: str
    generated_at: str
    prompt_template_hash: str
    prompt_version: str
    prompt_context: str
    coverage: float
    low_coverage: bool
    sections_present: list[str]
    claims_count: int
    unverified_claims: int
    cross_links_count: int
    broken_links: int           # conceptos vecinos inexistentes
    markdown_path: str | None  # si se persiste el md aparte

def persist_synthesis(concept_id: str, synthesis: Synthesis):
    path = workdir / "concepts" / concept_id / "synthesis.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(synthesis)   # incluye markdown completo
    # no persistir el markdown duplicado si es muy grande? en v1 se persiste completo
    atomic_write_json(path, data)

def load_synthesis(concept_id: str) -> Synthesis | None:
    path = workdir / "concepts" / concept_id / "synthesis.json"
    if not path.exists():
        return None
    return Synthesis(**json.loads(path.read_text(encoding="utf-8")))
```

Reglas:
- `synthesis.json` se escribe de forma atómica (temp + rename) en `workdir/concepts/<concept_id>/`. Nunca en el vault.
- El `markdown` del `Synthesis` es lo que el writer (Capa 5) inserta en el bloque `ai:start`/`ai:end`. Es el único campo que toca el vault (vía writer).
- `claims_index` permite trazabilidad end-to-end: validación (Capa 8) cruza cada afirmación del markdown con sus source_ids y penaliza las `[UNVERIFIED]`.
- `prompt_template_hash` + `prompt_version` permiten reproducir exactamente qué prompt generó un contenido (para debugging y auditoría).
- Si ya existe `synthesis.json` válido y la investigación no cambió (mismo `raw_research` hash) → se salta la síntesis (idempotencia), salvo `--force` o `--re-synthesize`.
- La síntesis NO escribe en el vault; solo persiste `synthesis.json`. La escritura la hace el writer (Capa 5) después de la validación (Capa 8).

### 7) Integración con el estado (Capa 3)

```python
async def synthesis_phase(concept_id: str):
    concept = load_concept(concept_id)
    state = load_state(concept_id)
    # cargar investigacion persistida
    raw = load_raw_research(concept_id)
    if raw is None:
        raise MissingResearchError(concept_id)
    sources = load_sources(concept_id)
    # armar contexto
    ctx = build_synthesis_context(concept, raw, sources)   # resuelve neighbors, prompt_context, volatility
    synthesizer = get_synthesizer()                      # singleton de la corrida
    try:
        synthesis = await synthesizer.synthesize(ctx)
        persist_synthesis(concept_id, synthesis)
        state.status = ConceptStatus.VALIDATING          # siguiente fase
        state.checkpoint = "synthesizing"
        state.phase_data["synthesis_done"] = True
        state.phase_data["synthesis_path"] = str(workdir / "concepts" / concept_id / "synthesis.json")
        state.phase_data["prompt_version"] = synthesis.prompt_version
        state.phase_data["prompt_hash"] = synthesis.prompt_template_hash
        state.phase_data["sections_present"] = list(synthesis.sections.keys())
        state.phase_data["unverified_claims"] = sum(1 for c in synthesis.claims_index if c.unverified)
        persist_state(concept_id, state)
    except (MissingResearchError, PromptNotFoundError, SynthesisGenerationError) as e:
        mark_failed(concept_id, phase="synthesizing", error=str(e))
        raise
```

Mapeo de errores:
- `MissingResearchError` (no hay `raw_research.json`) → `failed` reintentable (volver a `researching`).
- `PromptNotFoundError` (falta un template requerido) → `failed` no reintentable hasta arreglar config (tratar como `blocked` si es config).
- `SynthesisGenerationError` (el LLM/backend falló al generar) → `failed` reintentable (vuelve a `synthesizing`).
- `LowCoverageError` (si se configura como bloqueante) → `blocked` con detalle "cobertura insuficiente para sintetizar".
- Errores de IO (no se puede escribir `synthesis.json`) → `failed` reintentable.

### Excepciones de la capa

```python
class SynthesisError(Exception): ...
class MissingResearchError(SynthesisError): ...      # no hay raw_research.json para el concepto
class PromptNotFoundError(SynthesisError): ...      # falta un template de prompt requerido
class SynthesisGenerationError(SynthesisError): ... # fallo al generar el contenido (LLM/backend)
class NormalizationError(SynthesisError): ...      # no se pudo normalizar el Markdown
class MissingSectionError(SynthesisError): ...     # falta una seccion requerida en el output
class CrossLinkError(SynthesisError): ...          # error al resolver conceptos vecinos
class SynthesisPersistError(SynthesisError): ...   # fallo al escribir synthesis.json
```

### Reglas de negocio (de la spec)

- La síntesis NO escribe en el vault; solo persiste `synthesis.json` en `workdir`. La escritura la hace el writer (Capa 5) tras la validación (Capa 8).
- Se alimenta SIEMPRE de `raw_research.json` + `sources.json` (Capa 6). Si faltan → `failed` reintentable (volver a investigar).
- Los prompts son editables y versionados en `prompts/`; se seleccionan por contexto (frontend/backend/data/infra/general) con fallback a `general`.
- Override por concepto: `config/concepts/<id>.yaml` puede fijar `prompt_context` y `prompt_version`.
- Secciones requeridas del output: definición, cómo funciona, ejemplos, errores comunes, fundamento (estable), práctica (moderna), relacionados. Faltante → error de validación.
- Separación fundamento estable vs práctica moderna: fundamento cambia cada ~90d, práctica cada ~7-30d. Permite re-sintetizar solo la práctica.
- Cada afirmación factual lleva cita `[src-N]` a un `source_id`. Sin cita → `[UNVERIFIED]` (la validación las penaliza).
- Cross-links solo a conceptos existentes en el vault (o marcados como pendiente de crear). Nunca se inventan conceptos.
- Wikilinks usan `[[concept_id|Título]]` para resolución estable en Obsidian.
- Idempotencia: si `synthesis.json` es válido y la investigación no cambió (mismo hash de `raw_research`) → se salta, salvo `--force` o `--re-synthesize`.
- Trazabilidad: `prompt_template_hash` + `prompt_version` + `claims_index` permiten auditar qué prompt y qué fuentes generaron cada contenido.
- `low_coverage` / `low_sources` se propagan: la síntesis marca secciones inciertas con '⚠️ por verificar' y la validación las penaliza.

---

## Capa 8 — Validación (validation.py) (pseudo-código de alto nivel)

### Objetivo de la capa
Validar la síntesis (`Synthesis`) antes de que el writer la persista en el vault. Dos capas: **determinista** (formato, estructura, enlaces, hashes, frontmatter) y **semántica** (contenido, contexto, relaciones, profundidad, pedagogía, trazabilidad). 17 chequeos con severidad `error`/`warn`. Falla cerrado: ante la duda, no escribe. Esta capa NO escribe en el vault: produce un `ValidationResult` que el orquestador consulta para decidir si pasa a `writing` o marca `failed`/`blocked`.

### 1) Conceptos clave (`ValidationResult`, `Check`, `Severity`, `Gate`)

```python
class Severity(Enum):
    ERROR = "error"   # bloquea la escritura
    WARN  = "warn"    # se registra; puede bloquear si supera umbral

@dataclass
class CheckResult:
    check_id: str              # ej. "V_STRUCT_SECTIONS"
    name: str                  # nombre legible
    layer: Literal["deterministic", "semantic"]
    severity: Severity         # severidad declarada del chequeo
    passed: bool
    message: str               # detalle legible (vacío si passed)
    evidence: dict | None      # datos para debugging (ej. secciones faltantes)
    duration_ms: int

@dataclass
class ValidationResult:
    concept_id: str
    synthesis_path: str
    checked_at: str            # iso8601
    prompt_template_hash: str  # para trazabilidad
    checks: list[CheckResult]
    errors: list[CheckResult]  # subset con severity=ERROR y passed=False
    warnings: list[CheckResult]# subset con severity=WARN y passed=False
    is_valid: bool            # gate final
    blocked_reason: str | None # si no es válido, por qué
    score: float              # 0..1 (fraccion de checks pasados, ponderado)

CHECKS: list[CheckSpec] = [...]  # catalogo de 17 (ver seccion 2)

def run_validation(concept_id: str, synthesis: Synthesis, concept: ConceptMeta,
                   vault_index: VaultIndex, config: ValidationConfig) -> ValidationResult:
    results: list[CheckResult] = []
    ctx = ValidationContext(concept=concept, synthesis=synthesis,
                            vault_index=vault_index, config=config)
    for spec in CHECKS:
        fn = CHECK_FUNCTIONS[spec.check_id]
        r = fn(ctx)            # cada chequeo es puro y aislado
        results.append(r)
    return build_result(concept_id, synthesis, results, config)

@dataclass
class ValidationContext:
    concept: ConceptMeta
    synthesis: Synthesis
    vault_index: VaultIndex     # indice de conceptos del vault (para cross-links)
    config: ValidationConfig
    frontmatter: dict | None   # frontmatter parseado de la nota original
    frontmatter_raw: str | None # texto crudo del bloque --- ... ---
    sections: dict[str, str]   # synthesis.sections
    markdown: str              # synthesis.markdown
```

Reglas:
- Cada chequeo es una función pura `(ctx) -> CheckResult`: no tiene efectos secundarios, no toca el vault ni el disco.
- Los chequeos son independientes: el fallo de uno no impide ejecutar los demás (se reportan todos los problemas de una pasada).
- `ValidationResult` se persiste como artefacto (`validation.json`) para auditoría y para el reporte final del lote.
- `is_valid` se calcula al final por el gate (sección 8), no por los chequeos individuales.

### 2) Catálogo de los 17 chequeos

| # | check_id | capa | severidad | qué verifica |
|---|---|---|---|---|
| 1 | `V_STRUCT_SECTIONS` | determinista | error | todas las secciones requeridas presentes |
| 2 | `V_STRUCT_HEADINGS` | determinista | error | headings canónicos exactos (`## Título`) |
| 3 | `V_STRUCT_ORDER` | determinista | warn | orden canónico de secciones |
| 4 | `V_CONTENT_MIN_LENGTH` | determinista | error/warn | longitud mínima por sección (palabras) |
| 5 | `V_CONTENT_NO_PLACEHOLDERS` | determinista | error | sin placeholders/TODO/XXX/[...]/lorem |
| 6 | `V_CONTENT_CODE_FENCES` | determinista | warn | code fences cerrados y con lenguaje declarado |
| 7 | `V_LINKS_RESOLVE` | determinista | warn | cross-links resuelven o están marcados pendiente |
| 8 | `V_LINKS_NO_INVENTED` | determinista | error | no se inventan conceptos (wikilink a inexistente no marcado) |
| 9 | `V_LINKS_FORMAT` | determinista | warn | formato `[[concept_id\|Título]]` |
| 10 | `V_FRONTMATTER_PARSE` | determinista | error | frontmatter parseable (YAML válido) |
| 11 | `V_FRONTMATTER_FIELDS` | determinista | error | campos requeridos presentes (title, area) |
| 12 | `V_FRONTMATTER_MATCH` | determinista | error | frontmatter coincide con el `ConceptMeta` |
| 13 | `V_SEM_TRACES` | semántica | warn | afirmaciones con cita `[src-N]` (ratio de trazabilidad) |
| 14 | `V_SEM_UNVERIFIED_MARKED` | semántica | error | claims sin fuente marcados `[UNVERIFIED]` |
| 15 | `V_SEM_SEPARATION` | semántica | error | fundamento vs práctica separados (no versiones en fundamento) |
| 16 | `V_SEM_DEPTH_PEDAGOGY` | semántica | warn | profundidad mínima + tono pedagógico/definición clara |
| 17 | `V_SEM_CONTEXT` | semántica | warn | coherencia con `key_ideas` y `connections` del concepto |

### 3) Validación estructural (secciones requeridas presentes)

```python
REQUIRED_SECTIONS = ["definicion", "como_funciona", "ejemplos", "errores_comunes",
                     "fundamento", "practica", "relacionados"]

def check_sections_present(ctx: ValidationContext) -> CheckResult:
    present = set(ctx.sections.keys())
    missing = [s for s in REQUIRED_SECTIONS if s not in present]
    extra = [s for s in present if s not in REQUIRED_SECTIONS]
    passed = (len(missing) == 0)
    return CheckResult(
        check_id="V_STRUCT_SECTIONS",
        name="Secciones requeridas presentes",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Faltan secciones: {missing}",
        evidence={"missing": missing, "extra": extra, "present": sorted(present)},
        duration_ms=0,
    )

def check_headings_canonical(ctx: ValidationContext) -> CheckResult:
    # verifica que cada seccion use el heading exacto de SECTION_TITLES
    bad = []
    for key, title in SECTION_TITLES.items():
        if key in ctx.sections:
            # el markdown debe contener el heading exacto
            if title not in ctx.markdown:
                bad.append((key, title))
    passed = (len(bad) == 0)
    return CheckResult(
        check_id="V_STRUCT_HEADINGS",
        name="Headings canónicos exactos",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Headings no canónicos o faltantes: {bad}",
        evidence={"bad": bad},
        duration_ms=0,
    )

def check_section_order(ctx: ValidationContext) -> CheckResult:
    # verifica que las secciones aparezcan en el orden canonico (no bloquea, warn)
    order_found = [s for s in REQUIRED_SECTIONS if s in ctx.sections]
    # extraer orden real del markdown
    real_order = extract_section_order(ctx.markdown)   # lista de keys en orden de aparicion
    canonical = [s for s in REQUIRED_SECTIONS if s in real_order]
    passed = (real_order == canonical)  # subseciones extras no rompen el orden canonico
    return CheckResult(
        check_id="V_STRUCT_ORDER",
        name="Orden canónico de secciones",
        layer="deterministic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else "Las secciones no siguen el orden canónico.",
        evidence={"real_order": real_order, "canonical": canonical},
        duration_ms=0,
    )

def extract_section_order(md: str) -> list[str]:
    # parsea headings ## y devuelve la lista de section keys en orden de aparicion
    ...
```

Reglas:
- `V_STRUCT_SECTIONS` es bloqueante (error): si falta una sección requerida, no se escribe.
- `V_STRUCT_HEADINGS` es bloqueante (error): los headings deben coincidir exactamente con `SECTION_TITLES` (ej. `## Fundamento (estable)`), porque el writer y la re-síntesis dependen de ellos.
- `V_STRUCT_ORDER` es warning: el orden canónico se recomienda pero no bloquea (subsecciones extras son válidas).
- Las secciones requeridas son configurables (`required_sections` en config), por defecto las 7 de `REQUIRED_SECTIONS`.
- Secciones extra (no canónicas) se permiten y no penalizan, pero se registran en `evidence` para auditoría.

### 4) Validación de contenido (longitud mínima, sin placeholders)

```python
# umbrales por seccion (palabras). Configurables en validation.yaml
MIN_WORDS = {
    "definicion":      40,
    "como_funciona":   80,
    "ejemplos":        60,
    "errores_comunes": 60,
    "fundamento":      80,
    "practica":        60,
    "relacionados":    10,
}
TARGET_WORDS = {k: v * 2 for k, v in MIN_WORDS.items()}   # objetivo "bueno"

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b", r"\bXXX\b", r"\bFIXME\b", r"\bHACK\b",
    r"\[\.\.\.\]", r"\[pendiente\]", r"\[completar\]",
    r"lorem ipsum", r"placeholder", r"xxx",
    r"<insertar", r"\{\{[^}]+\}\}",   # variables sin reemplazar
]

def check_min_length(ctx: ValidationContext) -> CheckResult:
    short = []
    for sec, content in ctx.sections.items():
        words = len(content.split())
        minimum = ctx.config.min_words.get(sec, MIN_WORDS.get(sec, 30))
        if words < minimum:
            short.append({"section": sec, "words": words, "min": minimum})
    # warn si esta entre min y target; error si esta muy por debajo (ej. < min/2)
    hard_fail = [s for s in short if s["words"] < s["min"] // 2]
    passed = (len(hard_fail) == 0)
    severity = Severity.ERROR if hard_fail else (Severity.WARN if short else Severity.WARN)
    return CheckResult(
        check_id="V_CONTENT_MIN_LENGTH",
        name="Longitud mínima por sección",
        layer="deterministic",
        severity=Severity.ERROR if hard_fail else Severity.WARN,
        passed=passed,
        message="" if passed else f"Secciones muy cortas: {hard_fail or short}",
        evidence={"short": short, "hard_fail": hard_fail},
        duration_ms=0,
    )

def check_no_placeholders(ctx: ValidationContext) -> CheckResult:
    hits = []
    for sec, content in ctx.sections.items():
        for pat in PLACEHOLDER_PATTERNS:
            for m in re.finditer(pat, content, flags=re.IGNORECASE):
                hits.append({"section": sec, "pattern": pat, "match": m.group(0),
                            "pos": m.start()})
    # tambien escanear el markdown completo (por si el placeholder esta en un heading)
    for pat in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, ctx.markdown, flags=re.IGNORECASE):
            if not any(h["pos"] == m.start() for h in hits):
                hits.append({"section": "_global", "pattern": pat, "match": m.group(0)})
    passed = (len(hits) == 0)
    return CheckResult(
        check_id="V_CONTENT_NO_PLACEHOLDERS",
        name="Sin placeholders",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Placeholders encontrados: {len(hits)}",
        evidence={"hits": hits[:20]},   # tope para no inflar el JSON
        duration_ms=0,
    )

def check_code_fences(ctx: ValidationContext) -> CheckResult:
    # verifica que todo code fence abierto este cerrado y tenga lenguaje declarado
    fences = parse_code_fences(ctx.markdown)   # lista de {lang, closed, line}
    unclosed = [f for f in fences if not f["closed"]]
    no_lang = [f for f in fences if not f["lang"]]
    issues = unclosed + no_lang
    passed = (len(issues) == 0)
    return CheckResult(
        check_id="V_CONTENT_CODE_FENCES",
        name="Code fences válidos",
        layer="deterministic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else f"Issues en code fences: {len(issues)}",
        evidence={"unclosed": unclosed, "no_lang": no_lang},
        duration_ms=0,
    )
```

Reglas:
- `V_CONTENT_MIN_LENGTH`: si una sección tiene menos de la mitad del mínimo → error (bloquea); si está entre la mitad y el mínimo → warning (se registra pero no bloquea por sí solo). Si está sobre el mínimo pero bajo el target → no penaliza.
- `V_CONTENT_NO_PLACEHOLDERS` es error: un placeholder indica que la síntesis no terminó; nunca se escribe contenido con TODO/XXX/[...].
- `V_CONTENT_CODE_FENCES`: si hay fences sin cerrar → warning (el writer normaliza, pero se reporta). Si falta el lenguaje → warning (se asume `text`).
- Los umbrales (`MIN_WORDS`, `TARGET_WORDS`) viven en `validation.yaml` y se pueden ajustar por área (ej. `frontend` exige más palabras en `ejemplos`).
- `PLACEHOLDER_PATTERNS` se carga de config para permitir agregar patrones por proyecto.

### 5) Validación de cross-links (conceptos existentes)

```python
def check_cross_links_resolve(ctx: ValidationContext) -> CheckResult:
    # cada wikilink del markdown debe resolver a un concepto existente
    # O estar marcado como "pendiente de crear" (wikilink roto intencional)
    links = extract_wikilinks(ctx.markdown)   # lista de {raw, target_id, alias}
    unresolved = []
    pending_ok = []
    for lk in links:
        target = ctx.vault_index.get(lk["target_id"])   # None si no existe
        if target is None:
            # es valido solo si esta marcado como pendiente en la seccion
            if not is_marked_pending(ctx.markdown, lk):
                unresolved.append(lk)
            else:
                pending_ok.append(lk)
    passed = (len(unresolved) == 0)
    return CheckResult(
        check_id="V_LINKS_RESOLVE",
        name="Cross-links resuelven o están marcados pendiente",
        layer="deterministic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else f"Wikilinks sin resolver ni marcar pendiente: {len(unresolved)}",
        evidence={"unresolved": unresolved, "pending_ok": len(pending_ok), "total": len(links)},
        duration_ms=0,
    )

def check_no_invented_concepts(ctx: ValidationContext) -> CheckResult:
    # un wikilink a un concepto inexistente que NO este marcado como pendiente
    # se considera "concepto inventado" -> error bloqueante
    links = extract_wikilinks(ctx.markdown)
    invented = []
    for lk in links:
        if ctx.vault_index.get(lk["target_id"]) is None:
            if not is_marked_pending(ctx.markdown, lk):
                # ademas, si el target_id no sigue el patron de slug del vault -> sospechoso
                invented.append(lk)
    passed = (len(invented) == 0)
    return CheckResult(
        check_id="V_LINKS_NO_INVENTED",
        name="No se inventan conceptos",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Conceptos inventados (wikilinks a inexistentes no marcados): {len(invented)}",
        evidence={"invented": invented},
        duration_ms=0,
    )

def check_wikilink_format(ctx: ValidationContext) -> CheckResult:
    # verifica el formato [[concept_id|Título]] (con alias) para resolucion estable
    links = extract_wikilinks(ctx.markdown)
    bad_format = [lk for lk in links if "|" not in lk["raw"] or not lk["target_id"]]
    passed = (len(bad_format) == 0)
    return CheckResult(
        check_id="V_LINKS_FORMAT",
        name="Formato de wikilinks",
        layer="deterministic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else f"Wikilinks sin alias o mal formados: {len(bad_format)}",
        evidence={"bad_format": bad_format},
        duration_ms=0,
    )

def extract_wikilinks(md: str) -> list[dict]:
    # devuelve lista de {raw, target_id, alias} para cada [[...]] encontrado
    ...

def is_marked_pending(md: str, lk: dict) -> bool:
    # True si el wikilink aparece seguido de "*(pendiente de crear)*" o equivalente
    ...
```

Reglas:
- `V_LINKS_RESOLVE` es warning: los wikilinks rotos son válidos SI están marcados como pendiente de crear (Obsidian los muestra como no creados). Sin marcar → se reporta pero no bloquea por sí solo.
- `V_LINKS_NO_INVENTED` es error: un wikilink a un concepto inexistente NO marcado como pendiente se considera un concepto inventado por el modelo → bloquea. Esto es la protección contra alucinación de conceptos vecinos.
- `V_LINKS_FORMAT` es warning: el formato canónico es `[[concept_id|Título]]` (alias al título). Sin alias, Obsidian usa el id como texto visible (menos legible) pero no rompe.
- La validación cruza contra `vault_index` (índice de conceptos del scan de Capa 2), no contra el filesystem en tiempo real (el índice se pasa como contexto).
- Los wikilinks a conceptos inexistentes marcados como pendiente se cuentan en `broken_links` del `PersistedSynthesis` (Capa 7) y se reportan al final del lote para crearlos.

### 6) Validación de frontmatter

```python
def check_frontmatter_parseable(ctx: ValidationContext) -> CheckResult:
    # el frontmatter de la nota original debe ser YAML valido (si existe)
    fm_raw = ctx.frontmatter_raw   # texto entre --- ... --- o None
    if fm_raw is None:
        # archivo sin frontmatter: valido (no se agrega uno)
        return CheckResult(check_id="V_FRONTMATTER_PARSE", ..., passed=True, ...)
    try:
        parsed = yaml.safe_load(fm_raw)
        ok = isinstance(parsed, dict) or parsed is None
    except yaml.YAMLError as e:
        ok = False
        err = str(e)
    return CheckResult(
        check_id="V_FRONTMATTER_PARSE",
        name="Frontmatter parseable",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=ok,
        message="" if ok else f"YAML inválido en frontmatter: {err}",
        evidence={"error": err if not ok else None},
        duration_ms=0,
    )

def check_frontmatter_fields(ctx: ValidationContext) -> CheckResult:
    # campos requeridos presentes: title y area (al menos)
    fm = ctx.frontmatter or {}
    required = ctx.config.frontmatter_required_fields  # default ["title", "area"]
    missing = [f for f in required if f not in fm or fm.get(f) in (None, "")]
    passed = (len(missing) == 0)
    return CheckResult(
        check_id="V_FRONTMATTER_FIELDS",
        name="Campos requeridos de frontmatter",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Campos de frontmatter faltantes: {missing}",
        evidence={"missing": missing, "present": list(fm.keys())},
        duration_ms=0,
    )

def check_frontmatter_match(ctx: ValidationContext) -> CheckResult:
    # el frontmatter de la nota debe coincidir con el ConceptMeta (title, area)
    fm = ctx.frontmatter or {}
    mismatches = []
    if "title" in fm and fm["title"] != ctx.concept.title:
        mismatches.append({"field": "title", "frontmatter": fm["title"],
                          "concept": ctx.concept.title})
    if "area" in fm and fm["area"] != ctx.concept.area:
        mismatches.append({"field": "area", "frontmatter": fm["area"],
                          "concept": ctx.concept.area})
    passed = (len(mismatches) == 0)
    return CheckResult(
        check_id="V_FRONTMATTER_MATCH",
        name="Frontmatter coincide con ConceptMeta",
        layer="deterministic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Discrepancias frontmatter vs concepto: {mismatches}",
        evidence={"mismatches": mismatches},
        duration_ms=0,
    )
```

Reglas:
- `V_FRONTMATTER_PARSE` es error: si el frontmatter no es YAML válido, no se puede confiar en los metadatos; bloquea.
- `V_FRONTMATTER_FIELDS` es error: `title` y `area` son obligatorios (configurable). Si faltan, el concepto no se puede identificar correctamente.
- `V_FRONTMATTER_MATCH` es error: el frontmatter de la nota debe coincidir con el `ConceptMeta` extraído (Capa 2). Una discrepancia indica que la nota cambió manualmente o que el scan extrajo mal → bloquea para revisión.
- La validación de frontmatter NO modifica el frontmatter (eso es responsabilidad del writer, que lo preserva byte a byte). Aquí solo se verifica.
- Si el archivo no tiene frontmatter, `V_FRONTMATTER_PARSE` y `V_FRONTMATTER_FIELDS` se marcan como no aplicables (passed=True con `evidence: {"applicable": False}`) salvo que config exija frontmatter (`require_frontmatter: true`).
- `frontmatter_required_fields` es configurable (default `["title", "area"]`); se puede exigir `numero`, `aliases`, `tags` en proyectos más estrictos.

### 7) Validación semántica (contenido, contexto, relaciones, profundidad, pedagogía, trazabilidad)

```python
def check_traces(ctx: ValidationContext) -> CheckResult:
    # ratio de afirmaciones con cita [src-N] sobre el total de afirmaciones
    claims = extract_factual_claims(ctx.markdown)   # oraciones afirmativas (heuristica)
    cited = [c for c in claims if has_citation(c)]
    ratio = (len(cited) / len(claims)) if claims else 1.0
    threshold = ctx.config.trace_threshold   # default 0.6
    passed = ratio >= threshold
    return CheckResult(
        check_id="V_SEM_TRACES",
        name="Trazabilidad (citas [src-N])",
        layer="semantic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else f"Trazabilidad baja: {ratio:.0%} (umbral {threshold:.0%})",
        evidence={"claims": len(claims), "cited": len(cited), "ratio": round(ratio, 3),
                  "threshold": threshold},
        duration_ms=0,
    )

def check_unverified_marked(ctx: ValidationContext) -> CheckResult:
    # si una afirmacion no tiene cita, debe estar marcada [UNVERIFIED]
    claims = extract_factual_claims(ctx.markdown)
    unmarked = []
    for c in claims:
        if not has_citation(c) and "[UNVERIFIED]" not in c:
            unmarked.append(c[:120])
    passed = (len(unmarked) == 0)
    return CheckResult(
        check_id="V_SEM_UNVERIFIED_MARKED",
        name="Claims sin fuente marcados [UNVERIFIED]",
        layer="semantic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Afirmaciones sin cita ni marca [UNVERIFIED]: {len(unmarked)}",
        evidence={"unmarked": unmarked[:10]},
        duration_ms=0,
    )

def check_separation(ctx: ValidationContext) -> CheckResult:
    # fundamento no debe contener versiones/herramientas especificas (eso va en practica)
    fund = ctx.sections.get("fundamento", "")
    version_patterns = [r"\bv\d+\.\d+", r"\bReact \d", r"\bNode \d", r"\bPython 3\.\d",
                        r"\búltima versión\b", r"\bdeprecated\b", r"\bobsoleto\b"]
    leaks = []
    for pat in version_patterns:
        for m in re.finditer(pat, fund, flags=re.IGNORECASE):
            leaks.append({"pattern": pat, "match": m.group(0)})
    passed = (len(leaks) == 0)
    return CheckResult(
        check_id="V_SEM_SEPARATION",
        name="Separación fundamento vs práctica",
        layer="semantic",
        severity=Severity.ERROR,
        passed=passed,
        message="" if passed else f"Fundamento contiene referencias de práctica: {len(leaks)}",
        evidence={"leaks": leaks[:10]},
        duration_ms=0,
    )

def check_depth_and_pedagogy(ctx: ValidationContext) -> CheckResult:
    # profundidad: cada seccion con contenido suficiente + definicion clara en 'definicion'
    issues = []
    # profundidad por seccion
    for sec, content in ctx.sections.items():
        if len(content.split()) < (MIN_WORDS.get(sec, 30) // 2):
            issues.append(f"{sec}: muy superficial")
    # pedagogia: la definicion debe ser 2-4 oraciones y no empezar con jerga
    definicion = ctx.sections.get("definicion", "")
    sentences = split_sentences(definicion)
    if len(sentences) < 2 or len(sentences) > 6:
        issues.append(f"definicion: {len(sentences)} oraciones (esperado 2-4)")
    # ejemplos: al menos un code fence con lenguaje
    if "ejemplos" in ctx.sections:
        fences = parse_code_fences(ctx.sections["ejemplos"])
        if not fences or not any(f["lang"] for f in fences):
            issues.append("ejemplos: sin code fence con lenguaje")
    passed = (len(issues) == 0)
    return CheckResult(
        check_id="V_SEM_DEPTH_PEDAGOGY",
        name="Profundidad y pedagogía",
        layer="semantic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else "; ".join(issues),
        evidence={"issues": issues},
        duration_ms=0,
    )

def check_context_coherence(ctx: ValidationContext) -> CheckResult:
    # el contenido debe reflejar los key_ideas y connections del concepto
    issues = []
    text = ctx.markdown.lower()
    # key_ideas: al menos la mitad mencionados (por palabras clave)
    mentioned_ideas = 0
    for idea in ctx.concept.key_ideas:
        keywords = extract_keywords(idea)
        if any(kw in text for kw in keywords):
            mentioned_ideas += 1
    if ctx.concept.key_ideas:
        idea_ratio = mentioned_ideas / len(ctx.concept.key_ideas)
        if idea_ratio < 0.5:
            issues.append(f"key_ideas poco reflejados ({mentioned_ideas}/{len(ctx.concept.key_ideas)})")
    # connections: los conceptos conectados deben aparecer en 'relacionados'
    relacionados = ctx.sections.get("relacionados", "").lower()
    missing_conns = []
    for conn in ctx.concept.connections:
        if slug(conn).lower() not in relacionados and conn.lower() not in relacionados:
            missing_conns.append(conn)
    if missing_conns:
        issues.append(f"connections no reflejadas en relacionados: {missing_conns}")
    passed = (len(issues) == 0)
    return CheckResult(
        check_id="V_SEM_CONTEXT",
        name="Coherencia con el concepto",
        layer="semantic",
        severity=Severity.WARN,
        passed=passed,
        message="" if passed else "; ".join(issues),
        evidence={"issues": issues, "idea_ratio": idea_ratio if ctx.concept.key_ideas else None,
                  "missing_conns": missing_conns},
        duration_ms=0,
    )
```

Reglas:
- `V_SEM_TRACES`: mide la fracción de afirmaciones con cita `[src-N]`. Umbral configurable (default 0.6). Es warning, no bloquea por sí solo, pero se combina con `V_SEM_UNVERIFIED_MARKED`.
- `V_SEM_UNVERIFIED_MARKED` es error: si una afirmación no tiene cita, DEBE estar marcada `[UNVERIFIED]`. Afirmar sin fuente ni marca es alucinación → bloquea.
- `V_SEM_SEPARATION` es error: el fundamento (estable) no debe contener versiones, herramientas ni términos de obsolescencia; eso va en práctica. Mezclarlos rompe la re-síntesis parcial.
- `V_SEM_DEPTH_PEDAGOGY` es warning: verifica profundidad (secciones no superficiales) y pedagogía (definición de 2-4 oraciones, ejemplos con code fence). No bloquea, pero se reporta.
- `V_SEM_CONTEXT` es warning: verifica que el contenido refleje los `key_ideas` y `connections` del concepto. Si el modelo ignoró el contexto del vault → se reporta.
- Los chequeos semánticos usan heurísticas (regex, conteo de palabras, keywords). No son perfectos; por eso son warnings salvo `V_SEM_UNVERIFIED_MARKED` y `V_SEM_SEPARATION` que son errores.
- `extract_factual_claims`, `has_citation`, `split_sentences`, `extract_keywords` son helpers heurísticos (implementación en `validation_helpers.py`).

### 8) Gate: cómo se decide si un resumen es válido o no

```python
@dataclass
class ValidationConfig:
    # umbrales
    trace_threshold: float = 0.6
    min_words: dict[str, int] = field(default_factory=lambda: MIN_WORDS)
    max_warnings_before_block: int = 5
    require_frontmatter: bool = False
    frontmatter_required_fields: list[str] = field(default_factory=lambda: ["title", "area"])
    # que checks son bloqueantes (ademas de severity=ERROR)
    blocking_checks: list[str] = field(default_factory=list)  # ids extra que bloquean aunque sean warn
    # si True, cualquier warning bloquea (modo estricto)
    strict_mode: bool = False

def build_result(concept_id, synthesis, results, config) -> ValidationResult:
    errors = [r for r in results if r.severity == Severity.ERROR and not r.passed]
    warnings = [r for r in results if r.severity == Severity.WARN and not r.passed]
    # gate: falla cerrado
    blocked = False
    blocked_reason = None
    if errors:
        blocked = True
        blocked_reason = "errors: " + ", ".join(r.check_id for r in errors)
    elif config.strict_mode and warnings:
        blocked = True
        blocked_reason = "strict_mode: warnings present"
    elif len(warnings) > config.max_warnings_before_block:
        blocked = True
        blocked_reason = f"too_many_warnings: {len(warnings)} > {config.max_warnings_before_block}"
    elif any(r.check_id in config.blocking_checks and not r.passed for r in results):
        blocked = True
        blocked_reason = "blocking_checks failed"
    is_valid = not blocked
    score = sum(1 for r in results if r.passed) / len(results) if results else 0.0
    return ValidationResult(
        concept_id=concept_id,
        synthesis_path=str(workdir / "concepts" / concept_id / "synthesis.json"),
        checked_at=now_iso(),
        prompt_template_hash=synthesis.prompt_template_hash,
        checks=results,
        errors=errors,
        warnings=warnings,
        is_valid=is_valid,
        blocked_reason=blocked_reason,
        score=round(score, 3),
    )

def is_valid_result(result: ValidationResult) -> bool:
    return result.is_valid
```

Reglas del gate (falla cerrado):
- Si hay **al menos un check de severidad `error` que falló** → `is_valid = False` (bloquea, no se escribe). Esta es la regla principal.
- Si `strict_mode = True` y hay warnings → bloquea (modo para calibración/piloto).
- Si el número de warnings supera `max_warnings_before_block` (default 5) → bloquea (requiere revisión humana).
- Si algún check listado en `blocking_checks` falla (aunque sea warn) → bloquea.
- En cualquier otro caso (0 errores y warnings dentro del umbral) → `is_valid = True` (pasa a writing).
- Principio "falla cerrado": si un chequeo lanza una excepción interna (no capturada), se trata como `error` fallido (no se asume válido). El runner captura la excepción y marca el check como `passed=False` con `message="internal error: ..."`.
- El gate NO considera el `score` (es informativo). Un resumen con score alto pero un error bloqueante sigue siendo inválido.
- Los warnings NO bloquean por sí solos (salvo strict_mode o umbral). Se persisten en `validation.json` y se reportan al final del lote para revisión.

### 9) Persistencia del resultado (`validation.json`)

```python
@dataclass
class PersistedValidation:
    concept_id: str
    validated_at: str
    is_valid: bool
    blocked_reason: str | None
    score: float
    prompt_template_hash: str
    checks: list[dict]        # cada CheckResult serializado
    errors: list[str]        # check_ids que fallaron como error
    warnings: list[str]      # check_ids que fallaron como warn
    duration_ms: int

def persist_validation(concept_id: str, result: ValidationResult):
    path = workdir / "concepts" / concept_id / "validation.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(PersistedValidation(
        concept_id=concept_id,
        validated_at=result.checked_at,
        is_valid=result.is_valid,
        blocked_reason=result.blocked_reason,
        score=result.score,
        prompt_template_hash=result.prompt_template_hash,
        checks=[asdict(c) for c in result.checks],
        errors=[r.check_id for r in result.errors],
        warnings=[r.check_id for r in result.warnings],
        duration_ms=sum(c.duration_ms for c in result.checks),
    ))
    atomic_write_json(path, data)

def load_validation(concept_id: str) -> ValidationResult | None:
    path = workdir / "concepts" / concept_id / "validation.json"
    if not path.exists():
        return None
    return ValidationResult(**json.loads(path.read_text(encoding="utf-8")))
```

Reglas:
- `validation.json` se escribe de forma atómica (temp + rename) en `workdir/concepts/<concept_id>/`. Nunca en el vault.
- Si ya existe `validation.json` válido y la síntesis no cambió (mismo `prompt_template_hash` y mismo hash de `synthesis.json`) → se salta la validación (idempotencia), salvo `--force` o `--re-validate`.
- `errors` y `warnings` se persisten como listas de `check_id` para consultas rápidas (el reporte del lote las agrega).
- El `score` es informativo (fracción de checks pasados). No se usa en el gate.

### 10) Integración con el estado (Capa 3)

```python
async def validation_phase(concept_id: str):
    concept = load_concept(concept_id)
    state = load_state(concept_id)
    synthesis = load_synthesis(concept_id)
    if synthesis is None:
        raise MissingSynthesisError(concept_id)
    vault_index = load_vault_index()            # indice de conceptos del scan
    frontmatter_raw = read_frontmatter_raw(concept.path)
    ctx = ValidationContext(
        concept=concept, synthesis=synthesis, vault_index=vault_index,
        config=get_validation_config(),
        frontmatter=parse_frontmatter(frontmatter_raw),
        frontmatter_raw=frontmatter_raw,
        sections=synthesis.sections,
        markdown=synthesis.markdown,
    )
    try:
        result = run_validation(concept_id, synthesis, concept, vault_index, ctx.config)
        persist_validation(concept_id, result)
        if result.is_valid:
            state.status = ConceptStatus.WRITING     # siguiente fase
            state.checkpoint = "validating"
            state.phase_data["validation_done"] = True
            state.phase_data["validation_path"] = str(workdir / "concepts" / concept_id / "validation.json")
            state.phase_data["validation_score"] = result.score
            state.phase_data["validation_warnings"] = [r.check_id for r in result.warnings]
            persist_state(concept_id, state)
        else:
            # bloqueado para revision humana o failed segun el motivo
            if "errors" in (result.blocked_reason or ""):
                mark_failed(concept_id, phase="validating", error=result.blocked_reason)
            else:
                mark_blocked(concept_id, "validation", result.blocked_reason)
            persist_state(concept_id, state)
            raise ValidationError(concept_id, result)
    except ValidationError:
        raise
    except Exception as e:
        # falla cerrada: cualquier excepcion interna se trata como error
        mark_failed(concept_id, phase="validating", error=f"internal: {e}")
        persist_state(concept_id, state)
        raise
```

Mapeo de errores:
- `MissingSynthesisError` (no hay `synthesis.json`) → `failed` reintentable (volver a `synthesizing`).
- `ValidationError` con `blocked_reason` conteniendo "errors" → `failed` (los checks de error fallaron; se puede reintentar tras corregir la síntesis/config).
- `ValidationError` por warnings/umbral → `blocked` (requiere revisión humana: revisar warnings y decidir).
- Excepción interna no capturada → `failed` (falla cerrada; se registra el error completo en el log).
- Errores de IO (no se puede escribir `validation.json`) → `failed` reintentable.

Reglas:
- Si `is_valid = True` → el orquestador pasa a `writing` (Capa 5). El writer recibe la `Synthesis` validada.
- Si `is_valid = False` por errores → `failed` (reintentable: se puede regenerar la síntesis y revalidar).
- Si `is_valid = False` por warnings/umbral → `blocked` (requiere revisión humana; no se reintenta automáticamente).
- La validación NO modifica la síntesis: si falla, la `Synthesis` queda persistida (`synthesis.json`) para inspección/debugging.
- El writer (Capa 5) asume que la síntesis que recibe ya pasó la validación. Si por algún bug llega una síntesis no validada, el writer no la re-valida (se confía en el estado del pipeline).

### 11) Excepciones de la capa

```python
class ValidationError(Exception):
    def __init__(self, concept_id: str, result: ValidationResult):
        self.concept_id = concept_id
        self.result = result
        super().__init__(f"validacion fallida para {concept_id}: {result.blocked_reason}")

class MissingSynthesisError(ValidationError): ...    # no hay synthesis.json
class StructuralValidationError(ValidationError): ...# fallo en checks estructurales
class ContentValidationError(ValidationError): ...   # fallo en checks de contenido
class CrossLinkValidationError(ValidationError): ...  # fallo en checks de cross-links
class FrontmatterValidationError(ValidationError): ...# fallo en checks de frontmatter
class SemanticValidationError(ValidationError): ...   # fallo en checks semanticos
```

Reglas:
- `ValidationError` lleva el `ValidationResult` completo para que el orquestador/CLI puedan mostrar qué checks fallaron (`ai validate --show`).
- Las subclases se usan para que el CLI pueda filtrar por tipo de error (ej. `--errors structural`).
- `MissingSynthesisError` es un caso especial: no hay resultado que validar; se trata como `failed` reintentable.

### 12) Reglas de negocio (de la spec)

- La validación NO escribe en el vault; solo persiste `validation.json` en `workdir`. La escritura la hace el writer (Capa 5) tras pasar el gate.
- Dos capas: determinista (formato, estructura, enlaces, hashes, frontmatter) y semántica (contenido, contexto, relaciones, profundidad, pedagogía, trazabilidad).
- 17 chequeos con severidad `error`/`warn`. Falla cerrado: ante la duda, no escribe.
- Un check de severidad `error` que falla bloquea la escritura (no se escribe). Los `warn` se registran y solo bloquean si superan el umbral o en modo estricto.
- La validación es idempotente: si `validation.json` es válido y la síntesis no cambió (mismo `prompt_template_hash`) → se salta, salvo `--force` o `--re-validate`.
- Los chequeos son funciones puras e independientes: el fallo de uno no impide ejecutar los demás.
- Si un chequeo lanza una excepción interna, se trata como `error` fallido (falla cerrado).
- La validación cruza los cross-links contra el `vault_index` (índice del scan), no contra el filesystem en tiempo real.
- El frontmatter se verifica pero NO se modifica (preservación byte a byte es responsabilidad del writer).
- `V_SEM_UNVERIFIED_MARKED` y `V_SEM_SEPARATION` son los únicos chequeos semánticos bloqueantes (error); el resto de los semánticos son warnings.
- Los umbrales (`min_words`, `trace_threshold`, `max_warnings_before_block`) viven en `validation.yaml` y son ajustables por área/concepto.
- `validation.json` se persiste de forma atómica y se incluye en el reporte final del lote (errores/warnings agregados por concepto).
- El writer (Capa 5) asume que la síntesis que recibe ya pasó la validación; no la re-valida.
- Trazabilidad: `prompt_template_hash` se persiste en `ValidationResult` para auditar qué prompt generó el contenido validado.
- `score` es informativo (fracción de checks pasados); no se usa en el gate.

## Capa 9 — Orquestador (runner.py) + logging (pseudo-código de alto nivel)

### Objetivo de la capa
Encadenar todas las fases del pipeline (investigación, síntesis, validación, escritura) por concepto y por lote. El orquestador decide qué ejecutar, en qué orden, cómo reintentar, cómo reanudar tras un corte, cómo registrar todo en logs estructurados, y cómo producir el reporte final. Es el único componente que "sabe" del pipeline completo; las fases individuales (Capas 6-8) no se llaman entre sí directamente. Esta capa NO toca el vault: solo coordina, persiste estado (vía state.py) y escribe logs/reportes en `workdir`.

### 1) Bucle principal sobre los 255 conceptos (cola, orden)

El runner arranca con un scan del vault (Capa 2) para obtener la cola de conceptos. La cola es FIFO y el orden es el del scan (numérico por concepto, configurable). Se procesa un concepto a la vez (serial), con pacing entre conceptos para no saturar el backend. Un concepto que falla no detiene el lote.

```python
@dataclass
class RunConfig:
    workdir: Path
    vault_root: Path
    backend_provider: str = "notebooklm"
    max_retries: int = 3
    backoff_seconds: list[int] = field(default_factory=lambda: [2, 4, 8])
    pacing_between_concepts_s: float = 1.0
    concurrency_concepts: int = 1           # v1: serial. Reservado para futuro.
    stop_after_phase: Phase | None = None   # --stop-after
    dry_run: bool = False
    force: bool = False                    # ignora frescura/idempotencia
    only_concept_ids: list[str] | None = None   # --only
    from_concept: str | None = None        # reanudar desde un concepto
    strict_validation: bool = False
    cleanup_notebooks: bool = True
    keep_history: bool = False

@dataclass
class RunSummary:
    run_id: str
    started_at: str
    finished_at: str | None
    total: int
    done: int
    failed: int
    blocked: int
    skipped: int
    low_coverage: int
    low_sources: int
    broken_links: int
    total_duration_ms: int
    concepts: list[ConceptRunResult]

class Runner:
    def __init__(self, config: RunConfig):
        self.config = config
        self.backend = create_backend(load_config(config))     # singleton de la corrida
        self.state_store = StateStore(config.workdir)          # estado.json
        self.writer = SafeWriter(config, config.vault_root, config.workdir)
        self.synthesizer = Synthesizer(self.backend, PromptLoader(...), SynthesisConfig(...))
        self.validator = Validator(ValidationConfig(...))
        self.logger = StructuredLogger(config.workdir, run_id=new_run_id())
        self.vault_index = None                                # se carga en scan

    async def run_batch(self) -> RunSummary:
        self.logger.run_start(self.config)
        scan = scan_concepts(self.config.vault_root)           # Capa 2
        self.vault_index = scan.index
        queue = self._build_queue(scan.concepts)               # FIFO, filtros, orden
        self.logger.info("queue_built", total=len(queue), order="scan")

        summary = RunSummary(run_id=self.logger.run_id, started_at=now_iso(),
                            finished_at=None, total=len(queue), done=0, failed=0,
                            blocked=0, skipped=0, low_coverage=0, low_sources=0,
                            broken_links=0, total_duration_ms=0, concepts=[])

        for idx, concept in enumerate(queue, start=1):
            t0 = now_ms()
            self.logger.concept_start(concept.id, idx, len(queue))
            try:
                result = await self.run_concept(concept)        # serial: checkpoint antes de avanzar
            except Exception as e:                            # no detiene el lote
                result = ConceptRunResult(concept_id=concept.id, status="failed",
                                         error=str(e), duration_ms=now_ms() - t0)
                self.logger.concept_error(concept.id, e)
            summary.concepts.append(result)
            self._tally(summary, result)
            self.logger.concept_end(concept.id, result.status, now_ms() - t0)
            if idx < len(queue):
                await asyncio.sleep(self.config.pacing_between_concepts_s)

        summary.finished_at = now_iso()
        summary.total_duration_ms = now_ms() - parse_ms(summary.started_at)
        await self._finalize(summary)                          # reporte final
        self.logger.run_end(summary)
        return summary
```

Reglas de la cola:
- `scan_concepts` (Capa 2) devuelve la lista de conceptos con bloque `ai:start/end` + notas sin bloque.
- La cola incluye solo conceptos cuyo estado NO es terminal (`done`/`failed`/`blocked`) salvo `--force` o `--retry-failed`.
- Filtros: `--only <ids>`, `--from <concept_id>` (reanudar desde un concepto), `--area <area>`, `--status <status>`.
- Orden: scan order / orden numérico del concepto. Configurable (`concept_order: numeric | scan | mtime`).
- `concurrency_concepts` en v1 es 1 (serial). El campo queda para futuro; el diseño asume serialidad para simplificar checkpoints y evitar race conditions en el vault.
- Un concepto que lanza una excepción no capturada NO detiene el lote: se marca `failed`, se registra y se sigue con el siguiente.
- Pacing configurable entre conceptos (`pacing_between_concepts_s`, default 1s) para no saturar NotebookLM / rate limits.

```python
def _build_queue(self, concepts: list[ConceptMeta]) -> list[ConceptMeta]:
    out = []
    for c in concepts:
        state = self.state_store.load(c.id)
        if self.config.force:
            pass                                           # incluir todos
        elif self.config.retry_failed and state and state.status in (FAILED, BLOCKED):
            pass                                           # reintentar terminales reintentables
        elif state and state.status in (DONE, FAILED, BLOCKED):
            self.logger.info("concept_skipped_terminal", concept_id=c.id, status=state.status)
            continue
        if self.config.only_concept_ids and c.id not in self.config.only_concept_ids:
            continue
        if self.config.from_concept and not self._passed_from(c, self.config.from_concept, concepts):
            continue
        if self.config.area_filter and c.area != self.config.area_filter:
            continue
        out.append(c)
    # orden
    out = sort_concepts(out, key=self.config.concept_order)
    return out
```

### 2) Transiciones de estado por concepto

El runner ejecuta las fases en orden lineal. Cada fase es una función async que recibe `concept_id` y devuelve el control al runner, que entonces persiste el estado y avanza. Las transiciones válidas son las de la Capa 3 (`TRANSITIONS`). El runner no salta fases ni las reordena.

```python
PHASE_ORDER: list[Phase] = [
    Phase.RESEARCHING,
    Phase.SYNTHESIZING,
    Phase.VALIDATING,
    Phase.WRITING,
]

PHASE_FN = {
    Phase.RESEARCHING:  research_phase,     # Capa 6
    Phase.SYNTHESIZING: synthesis_phase,  # Capa 7
    Phase.VALIDATING:   validation_phase,  # Capa 8
    Phase.WRITING:      writing_phase,    # Capa 5
}

async def run_concept(self, concept: ConceptMeta) -> ConceptRunResult:
    state = self.state_store.load(concept.id) or new_state(concept.id)
    t0 = now_ms()

    # terminal: no reejecutar (salvo force)
    if not self.config.force and state.status in (DONE, FAILED, BLOCKED):
        self.logger.info("concept_terminal_skip", concept_id=concept.id, status=state.status)
        return ConceptRunResult(concept_id=concept.id, status=state.status.value,
                                skipped=True, duration_ms=now_ms() - t0)

    # reanudar desde el checkpoint
    start_phase = self._resume_phase(state)   # ver seccion 3

    for phase in phases_from(start_phase):     # sublista de PHASE_ORDER
        if self.config.stop_after_phase and phase == self.config.stop_after_phase:
            self.logger.info("stop_after_reached", concept_id=concept.id, phase=phase.value)
            break

        # reintento por fase
        try:
            await self._run_phase_with_retry(concept.id, phase)
        except Exception as e:
            # clasificar y mapear a failed/blocked
            new_status = self._classify_failure(e)   # failed | blocked
            state = self.state_store.load(concept.id)
            state.status = new_status
            state.phase_data["error"] = str(e)
            state.phase_data["fase_fallida"] = phase.value
            state.phase_data["timestamp"] = now_iso()
            self.state_store.persist(concept.id, state)
            self.logger.phase_failed(concept.id, phase.value, e, new_status.value)
            return ConceptRunResult(concept_id=concept.id, status=new_status.value,
                                   error=str(e), failed_phase=phase.value,
                                   duration_ms=now_ms() - t0)

        # avanzar estado
        state = self.state_store.load(concept.id)
        state.status = next_status(phase)            # researching->synthesizing->...
        state.checkpoint = phase.value
        self.state_store.persist(concept.id, state)
        self.logger.phase_ok(concept.id, phase.value)

    # si llego aca sin break por error, marcar done (la fase WRITING ya lo hace,
    # pero el runner asegura el estado final)
    state = self.state_store.load(concept.id)
    if state.status != DONE:
        state.status = DONE
        state.checkpoint = Phase.WRITING.value
        self.state_store.persist(concept.id, state)

    return ConceptRunResult(concept_id=concept.id, status="done",
                           duration_ms=now_ms() - t0)
```

Reglas de transición:
- El orden de fases es fijo: `researching → synthesizing → validating → writing`. No se salta ninguna (salvo `--stop-after`, que detiene el pipeline entero, no la fase).
- Cada fase persiste su estado (`estado.json`) ANTES de avanzar a la siguiente. Si el proceso se corta, el checkpoint permite reanudar sin repetir la fase terminada.
- `next_status(phase)` devuelve el estado siguiente del enum (`RESEARCHING → SYNTHESIZING`, etc.). `WRITING → DONE`.
- Si una fase falla, el estado pasa a `failed` o `blocked` (según la clasificación del error) y el concepto se deja en ese estado terminal operativo. No se reintenta automáticamente dentro del mismo `run_concept` si se agotaron los reintentos de la fase.
- `--stop-after <phase>` detiene el concepto (y el lote) tras completar la fase indicada. Útil para calibración (ej. `--stop-after researching` para solo investigar).
- El runner NO llama a las fases directamente con lógica de negocio: delega en `research_phase`, `synthesis_phase`, etc. (Capas 6-8). El runner solo coordina, reintenta y persiste estado.

```python
def _classify_failure(self, e: Exception) -> ConceptStatus:
    # mapeo centralizado de excepciones -> estado terminal
    if isinstance(e, BackendAuthError):
        return BLOCKED          # requiere accion humana (renovar credenciales)
    if isinstance(e, ValidationError) and "errors" in (e.result.blocked_reason or ""):
        return FAILED           # reintentable tras corregir sintesis/config
    if isinstance(e, ValidationError):   # warnings/umbral
        return BLOCKED          # requiere revision humana
    if isinstance(e, (MissingMarkersError, DuplicateMarkersError, MarkerOrderError,
                      ConcurrentEditError, OutsideIntegrityError, FrontmatterChangedError,
                      InsideMismatchError)):
        return FAILED           # writer: reintentable tras resolver la causa
    if isinstance(e, BlockedError):
        return BLOCKED
    return FAILED               # default: reintentable
```

### 3) Checkpoint y resume

El checkpoint es el par `(status, checkpoint)` persistido en `estado.json` por concepto. Al arrancar un concepto, el runner lee el estado y decide desde qué fase reanudar. Si el estado es terminal, no se reejecuta (salvo `--force`). Si es no-terminal, se reanuda desde el último checkpoint persistido, sin repetir las fases ya completadas.

```python
def _resume_phase(self, state: ConceptState) -> Phase:
    # devuelve la fase por la que hay que empezar
    if state.status == PENDING or state.checkpoint is None:
        return Phase.RESEARCHING
    if state.status == RESEARCHING:
        return Phase.RESEARCHING          # reanudar investigacion (por pregunta)
    if state.status == SYNTHESIZING:
        return Phase.SYNTHESIZING
    if state.status == VALIDATING:
        return Phase.VALIDATING
    if state.status == WRITING:
        return Phase.WRITING
    # FAILED / BLOCKED: reanudar desde la fase que fallo
    if state.status in (FAILED, BLOCKED):
        failed_phase = state.phase_data.get("fase_fallida")
        if failed_phase:
            return Phase(failed_phase)
        # fallback: reanudar desde el checkpoint previo
        if state.checkpoint:
            return Phase(state.checkpoint)
        return Phase.RESEARCHING
    # DONE: no deberia llegar aca (se filtra antes), pero por seguridad
    return Phase.WRITING

def phases_from(self, start: Phase) -> list[Phase]:
    idx = PHASE_ORDER.index(start)
    return PHASE_ORDER[idx:]
```

Reglas de checkpoint/resume:
- `estado.json` es la única fuente de verdad del progreso. Sin él no hay recuperación ni idempotencia.
- El checkpoint se persiste de forma atómica en cada transición validada (Capa 3). El runner no mantiene estado en memoria que no esté persistido: si el proceso muere, el estado en disco es suficiente para reanudar.
- Reanudación fina dentro de una fase: la investigación (Capa 6) es reanudable por pregunta; la síntesis y la validación se re-ejecutan completas si se cortan (son idempotentes y más baratas que la investigación). La escritura (Capa 5) es idempotente por hash del afuera.
- `--force` ignora el estado terminal y re-ejecuta desde la primera fase (útil para re-procesar tras cambiar prompts o config). Con `--force`, el runner NO borra los artefactos previos: las fases individuales deciden si reutilizan o regeneran (por hash de entrada).
- `--retry-failed` solo reintenta conceptos en `failed`/`blocked` (no toca los `done`).
- Si `estado.json` está corrupto o ilegible, el runner lo reporta como `blocked` con "estado corrupto" y NO intenta adivinar. Se puede reparar manualmente o con `--reset-state <concept_id>`.
- El runner persiste el `run_id` en cada `estado.json` actualizado, para poder correlacionar logs y estados con la corrida que los generó.

Formato de `estado.json` (resumen, ver Capa 3):
```json
{
  "frontend-01-internet-web": {
    "status": "synthesizing",
    "checkpoint": "researching",
    "phase_data": {
      "notebook_id": null,
      "source_ids": ["src-1", "src-2"],
      "answers": [...],
      "coverage": 0.83,
      "research_done": true,
      "sources_path": "workdir/concepts/frontend-01-internet-web/sources.json",
      "raw_research_path": "workdir/concepts/frontend-01-internet-web/raw_research.json"
    },
    "retries": 1,
    "run_id": "run-20261022-100000",
    "updated_at": "2026-10-22T10:05:00Z"
  }
}
```

### 4) Logging estructurado

El logging es en formato JSON Lines (un objeto JSON por línea), escrito en `workdir/logs/run-<run_id>.jsonl`. Cada línea tiene campos estándar para poder filtrar, agregar y auditar. No se usan logs de texto libre en producción (solo en `--verbose` para debug). Los secretos (auth, cookies) nunca se registran.

```python
@dataclass
class LogRecord:
    ts: str                      # iso8601 con ms
    run_id: str
    level: Literal["debug", "info", "warn", "error"]
    event: str                   # nombre del evento (ej. "phase_ok", "phase_failed")
    concept_id: str | None
    phase: str | None
    duration_ms: int | None
    message: str | None
    data: dict | None            # payload estructurado (error, counts, paths)
    # NO incluir: secretos, paths absolutos del usuario, contenido de notas

class StructuredLogger:
    def __init__(self, workdir: Path, run_id: str):
        self.path = workdir / "logs" / f"run-{run_id}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self._fh = self.path.open("a", encoding="utf-8")

    def _write(self, level, event, **kwargs):
        rec = LogRecord(ts=now_iso_ms(), run_id=self.run_id, level=level,
                        event=event, **kwargs)
        self._fh.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")
        self._fh.flush()                      # flush por linea para no perder datos si el proceso muere

    def run_start(self, config):   self._write("info", "run_start", data={"config": redact(config)})
    def run_end(self, summary):    self._write("info", "run_end", data=asdict(summary))
    def concept_start(self, cid, idx, total):
        self._write("info", "concept_start", concept_id=cid, data={"idx": idx, "total": total})
    def concept_end(self, cid, status, dur):
        self._write("info", "concept_end", concept_id=cid, duration_ms=dur, data={"status": status})
    def concept_error(self, cid, e):
        self._write("error", "concept_error", concept_id=cid, message=str(e),
                    data={"type": type(e).__name__, "traceback": traceback.format_exc()})
    def phase_ok(self, cid, phase):
        self._write("info", "phase_ok", concept_id=cid, phase=phase)
    def phase_failed(self, cid, phase, e, new_status):
        self._write("error", "phase_failed", concept_id=cid, phase=phase,
                    message=str(e), data={"type": type(e).__name__, "new_status": new_status})
    def phase_retry(self, cid, phase, attempt, wait_s, e):
        self._write("warn", "phase_retry", concept_id=cid, phase=phase,
                    data={"attempt": attempt, "wait_s": wait_s, "error": str(e)})
    def backend_call(self, method, target, dur, ok, error=None):
        self._write("debug", "backend_call", data={"method": method, "target": target,
                    "duration_ms": dur, "ok": ok, "error": error})
    def validation_summary(self, cid, result):
        self._write("info", "validation_summary", concept_id=cid,
                    data={"is_valid": result.is_valid, "score": result.score,
                          "errors": [r.check_id for r in result.errors],
                          "warnings": [r.check_id for r in result.warnings]})
    def checkpoint(self, cid, phase):
        self._write("debug", "checkpoint", concept_id=cid, phase=phase)
    def info(self, event, **kw):   self._write("info", event, **kw)
    def warn(self, event, **kw):   self._write("warn", event, **kw)
    def error(self, event, **kw):  self._write("error", event, **kw)
    def debug(self, event, **kw):  self._write("debug", event, **kw)

    def close(self):
        self._fh.close()
```

Eventos mínimos a registrar (por concepto y por corrida):
- `run_start`, `run_end` (con resumen agregado).
- `queue_built` (total, filtros, orden).
- `concept_start`, `concept_end`, `concept_error`, `concept_skipped_terminal`.
- `phase_ok`, `phase_failed`, `phase_retry`, `phase_start`.
- `checkpoint` (cada vez que se persiste un checkpoint).
- `backend_call` (método, target, duración, ok/error) — nivel debug, activable con `--verbose`.
- `validation_summary` (is_valid, score, errors, warnings).
- `report_written` (path del reporte final).
- `circuit_breaker_open` (si se abre el circuit breaker).
- `cleanup_failed` (si falla el delete de un notebook huérfano).

Reglas de logging:
- Formato JSON Lines: una línea = un evento. Parseable con `jq`, pandas, o cualquier herramienta de logs.
- Flush por línea: si el proceso muere, no se pierden eventos (importante para debugging de cortes).
- Niveles: `debug` (backend calls, checkpoints), `info` (fases, conceptos), `warn` (reintentos, warnings de validación), `error` (fallos, excepciones).
- `--verbose` activa nivel `debug`; por defecto `info`.
- Rotación: un archivo por corrida (`run-<run_id>.jsonl`). No se sobrescriben corridas previas. Limpieza manual o por política de retención (config: `log_retention_days`, default 30).
- Los logs NO contienen secretos ni contenido de notas (solo ids, paths relativos, counts, errores). El contenido generado se persiste en `workdir/concepts/<id>/`, no en el log.
- `run_id` se genera al arrancar (`run-YYYYMMDD-HHMMSS-<shortuuid>`) y se propaga a todos los registros y a `estado.json`.
- El logger se cierra al final de la corrida (`close()`). En caso de excepción no capturada, un handler de `atexit`/`finally` asegura el flush y cierre.

### 5) Manejo de errores y reintentos

Cada fase se ejecuta con reintentos y backoff exponencial. El manejo distingue errores reintentables (red, timeout, rate limit, IO transitorio) de los no reintentables (auth, validación con errores, markers faltantes). Los reintentos son por fase, no por concepto completo: si `researching` falla 3 veces, el concepto queda `failed` en `researching` y el lote sigue.

```python
MAX_RETRIES = 3
BACKOFF_SECONDS = [2, 4, 8]   # exponencial, configurable

RETRYABLE_ERRORS = (
    BackendTimeout, BackendNetworkError, BackendRateLimitError,
    IOError, OSError, TimeoutError, ConnectionError,
)

NON_RETRYABLE_ERRORS = (
    BackendAuthError, MissingMarkersError, DuplicateMarkersError, MarkerOrderError,
    ConcurrentEditError, OutsideIntegrityError, FrontmatterChangedError,
    InsideMismatchError, ValidationError,  # (según clasificación)
)

async def _run_phase_with_retry(self, concept_id: str, phase: Phase):
    fn = PHASE_FN[phase]
    last_error = None
    for attempt in range(1, self.config.max_retries + 1):
        try:
            self.logger.debug("phase_attempt", concept_id=concept_id, phase=phase.value,
                              data={"attempt": attempt})
            await fn(concept_id)            # la fase lee/escribe su propio estado
            return
        except Exception as e:
            last_error = e
            retryable = isinstance(e, RETRYABLE_ERRORS) and not isinstance(e, NON_RETRYABLE_ERRORS)
            if not retryable or attempt == self.config.max_retries:
                # no reintentable o agotado: propagar para que run_concept clasifique
                raise
            wait = self.config.backoff_seconds[attempt - 1]
            self.logger.phase_retry(concept_id, phase.value, attempt, wait, e)
            await asyncio.sleep(wait)
    raise last_error
```

Reglas de reintentos:
- Max 3 intentos por fase (configurable: `max_retries`). Backoff exponencial: intento 1 → 2s, intento 2 → 4s, intento 3 → 8s (configurable en `backoff_seconds`).
- Errores reintentables: `BackendTimeout`, `BackendNetworkError`, `BackendRateLimitError`, errores de IO/transitorios. Se reintenta con backoff.
- Errores no reintentables: `BackendAuthError` (requiere acción humana), errores del writer por markers/integridad (requieren intervención), `ValidationError` (la síntesis no pasó; reintentar la misma síntesis no ayuda; hay que regenerar). Se propagan de inmediato sin reintentar.
- Al agotar los reintentos, la fase se marca `failed` (o `blocked` según clasificación) y se persiste el error (`fase_fallida`, `error`, `timestamp`). El lote sigue con el siguiente concepto.
- Limpieza best-effort ante fallo: si `create_notebook` OK pero `add_sources` falla → intentar `delete(notebook_id)` para no dejar notebooks huérfanos. Si la limpieza falla, se registra en log (`cleanup_failed`) pero no bloquea. Los notebooks huérfanos se reportan al final del lote.
- Circuit breaker simple: si se acumulan N fallos consecutivos de red/backend (config: `circuit_breaker_threshold`, default 5), el runner pausa el lote por `circuit_breaker_cooldown_s` (default 60s) y registra `circuit_breaker_open`. Si tras la pausa sigue fallando, marca el concepto como `blocked` con "backend no disponible" y sigue. Esto evita hammering al backend.
- Los reintentos NO repiten trabajo ya persistido: la investigación reanuda por pregunta, la síntesis/validación son idempotentes por hash, la escritura es idempotente por hash del afuera. Un reintento de una fase que falló a mitad continúa desde el checkpoint, no desde cero.
- `--max-retries N` (CLI) sobrescribe el config para una corrida puntual.

```python
class CircuitBreaker:
    def __init__(self, threshold: int = 5, cooldown_s: int = 60):
        self.threshold = threshold
        self.cooldown_s = cooldown_s
        self.consecutive_failures = 0
        self.opened_at: float | None = None

    def record_failure(self, e: Exception) -> bool:
        if not isinstance(e, (BackendTimeout, BackendNetworkError, BackendRateLimitError)):
            return False
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.threshold and self.opened_at is None:
            self.opened_at = now()
            return True   # se acaba de abrir
        return False

    def record_success(self):
        self.consecutive_failures = 0
        self.opened_at = None

    async def wait_if_open(self, logger):
        if self.opened_at is None:
            return
        elapsed = now() - self.opened_at
        if elapsed < self.cooldown_s:
            await asyncio.sleep(self.cooldown_s - elapsed)
        # tras el cooldown, se "cierra" a medias: se reintenta; si falla de nuevo, se reabre
        self.opened_at = None
```

Integración del circuit breaker en `run_concept`:
```python
async def run_concept(self, concept):
    ...
    for phase in phases_from(start_phase):
        await self.circuit_breaker.wait_if_open(self.logger)
        try:
            await self._run_phase_with_retry(concept.id, phase)
            self.circuit_breaker.record_success()
        except Exception as e:
            opened = self.circuit_breaker.record_failure(e)
            if opened:
                self.logger.warn("circuit_breaker_open", data={"threshold": self.circuit_breaker.threshold})
            # clasificar y marcar failed/blocked
            ...
```

### 6) Reporte final

Al terminar el lote, el runner genera un reporte final en `workdir/reports/run-<run_id>.json` (y opcionalmente `.md`). El reporte agrega métricas por concepto y por lote, lista los conceptos fallidos/bloqueados, los de baja cobertura/fuentes, los wikilinks rotos, los notebooks huérfanos y los tiempos. Es la "foto" de la corrida para revisión humana y para el CLI (`ai status`, `ai review`).

```python
@dataclass
class ConceptRunResult:
    concept_id: str
    status: str                    # done | failed | blocked | skipped
    duration_ms: int
    failed_phase: str | None = None
    error: str | None = None
    score: float | None = None      # validation score si aplica
    coverage: float | None = None
    low_coverage: bool = False
    low_sources: bool = False
    broken_links: int = 0
    unverified_claims: int = 0
    warnings: list[str] = field(default_factory=list)

@dataclass
class FinalReport:
    run_id: str
    started_at: str
    finished_at: str
    duration_ms: int
    config_summary: dict            # backend, max_retries, pacing, etc. (sin secretos)
    totals: dict                   # total, done, failed, blocked, skipped
    by_status: dict[str, int]
    by_phase_failed: dict[str, int] # cuantos fallaron en cada fase
    by_area: dict[str, dict]       # metricas por area
    concepts: list[ConceptRunResult]
    failed_concepts: list[dict]     # id, phase, error (resumido)
    blocked_concepts: list[dict]    # id, blocker, detalle
    low_coverage_concepts: list[str]
    low_sources_concepts: list[str]
    broken_links_total: int
    broken_links_by_concept: dict[str, int]
    orphan_notebooks: list[str]     # notebooks no limpiados
    orphan_notes_without_block: list[str]  # notas del vault sin bloque ai
    validation_warnings_agg: dict[str, int]  # check_id -> count
    timings: dict                  # min/max/avg por fase, total
    recommendations: list[str]     # sugerencias para el humano (ej. "renovar credenciales")

async def _finalize(self, summary: RunSummary) -> FinalReport:
    report = FinalReport(
        run_id=summary.run_id,
        started_at=summary.started_at,
        finished_at=summary.finished_at,
        duration_ms=summary.total_duration_ms,
        config_summary=redact_config(self.config),
        totals={"total": summary.total, "done": summary.done,
                "failed": summary.failed, "blocked": summary.blocked,
                "skipped": summary.skipped},
        by_status=self._count_by_status(summary.concepts),
        by_phase_failed=self._count_by_phase(summary.concepts),
        by_area=self._aggregate_by_area(summary.concepts),
        concepts=summary.concepts,
        failed_concepts=[{"id": c.concept_id, "phase": c.failed_phase, "error": c.error}
                        for c in summary.concepts if c.status == "failed"],
        blocked_concepts=[{"id": c.concept_id, "blocker": ..., "detalle": ...}
                         for c in summary.concepts if c.status == "blocked"],
        low_coverage_concepts=[c.concept_id for c in summary.concepts if c.low_coverage],
        low_sources_concepts=[c.concept_id for c in summary.concepts if c.low_sources],
        broken_links_total=sum(c.broken_links for c in summary.concepts),
        broken_links_by_concept={c.concept_id: c.broken_links for c in summary.concepts if c.broken_links},
        orphan_notebooks=await self._find_orphan_notebooks(),
        orphan_notes_without_block=self._scan_notes_without_block(),
        validation_warnings_agg=self._aggregate_validation_warnings(summary.concepts),
        timings=self._compute_timings(summary.concepts),
        recommendations=self._build_recommendations(summary),
    )

    # persistir JSON
    path = self.config.workdir / "reports" / f"run-{self.logger.run_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(path, asdict(report))

    # persistir Markdown (resumen legible) si config.report_markdown = True
    if self.config.report_markdown:
        md_path = path.with_suffix(".md")
        md_path.write_text(render_report_markdown(report), encoding="utf-8")

    self.logger.info("report_written", data={"path": str(path), "done": report.totals["done"],
                    "failed": report.totals["failed"], "blocked": report.totals["blocked"]})
    return report
```

Contenido del reporte (resumen humano en Markdown):
```markdown
# Reporte de corrida <run_id>

- Inicio: ...  Fin: ...  Duración: ...
- Total: 255  |  Done: 240  |  Failed: 10  |  Blocked: 3  |  Skipped: 2

## Fallidos (requieren reintento)
| Concepto | Fase | Error |
|---|---|---|
| ... | researching | BackendTimeout: ... |

## Bloqueados (requieren acción humana)
| Concepto | Blocker | Detalle |
|---|---|---|
| ... | auth | credenciales inválidas |

## Baja cobertura / pocas fuentes
- frontend-07-... (coverage 0.42)
- ...

## Wikilinks rotos (conceptos pendientes de crear)
- frontend-03-... -> [[backend-02-api]] (pendiente)

## Notebooks huérfanos
- fake-nb-42 (delete falló)

## Recomendaciones
- Renovar credenciales de NotebookLM antes de la próxima corrida.
- Revisar 3 conceptos bloqueados por validación (warnings > umbral).
```

Reglas del reporte:
- El reporte se genera SIEMPRE al final de la corrida, incluso si hubo fallos o interrupción (con `--interrupted` se marca como parcial). No se pierde la información de lo procesado.
- El reporte JSON es la fuente para el CLI: `ai status` lee el último reporte + `estado.json`; `ai review` muestra los conceptos bloqueados/fallidos con su detalle.
- Los conceptos `done` se incluyen en el reporte con su score de validación y coverage, para poder detectar regresiones (ej. un concepto que pasó con score bajo).
- `recommendations` se genera con reglas simples: si hay bloqueados por auth → "renovar credenciales"; si hay muchos `low_coverage` → "revisar fuentes de los conceptos X"; si hay notebooks huérfanos → "limpiar manualmente".
- El reporte NO incluye contenido de notas ni secretos. Solo ids, métricas, errores resumidos y paths relativos a `workdir`.
- Si el lote se interrumpe (Ctrl+C / SIGTERM), el runner captura la señal, persiste el estado actual, genera un reporte parcial con `interrupted: true` y sale limpiamente (no corrompe `estado.json`).
- Idempotencia del reporte: re-correr genera un reporte nuevo con nuevo `run_id`; los anteriores se conservan (no se sobrescriben). Limpieza por política de retención (`report_retention_days`, default 30).

### Integración con CLI (Capa 10, adelanto)
El runner expone una interfaz mínima para que la CLI (Capa 10) lo invoque sin conocer detalles:
```python
async def run_one(concept_id: str, **overrides) -> ConceptRunResult:
    # procesa un solo concepto (para `ai run <id>`)

async def run_batch(concept_ids: list[str] | None = None, **overrides) -> FinalReport:
    # procesa el lote (para `ai run-batch`)

def status() -> dict:
    # devuelve el estado agregado leyendo estado.json + ultimo reporte

def review(concept_id: str | None = None) -> dict:
    # devuelve conceptos bloqueados/fallidos con detalle para revision humana
```

### Excepciones del runner
```python
class RunnerError(Exception): ...
class QueueBuildError(RunnerError): ...          # fallo al armar la cola (scan, filtros)
class StateCorruptError(RunnerError): ...       # estado.json ilegible/corrupto
class InterruptedRunError(RunnerError): ...     # corrida interrumpida por senal
class ReportWriteError(RunnerError): ...        # no se pudo escribir el reporte final
```

### Reglas de negocio (de la spec)
- El orquestador es el único que conoce el pipeline completo. Las fases (Capas 6-8) no se llaman entre sí; el runner las coordina.
- Procesamiento serial por concepto: se transiciona y persiste el estado (checkpoint) ANTES de avanzar a la fase siguiente.
- Un concepto que falla no detiene el lote; se registra y se sigue con el siguiente.
- Cola FIFO de conceptos en `pending` (resultado del scan), orden configurable (default numérico).
- Reintentos por fase (max 3, backoff exponencial) con clasificación de errores reintentables vs no reintentables.
- Checkpoint y resume: el runner lee `estado.json` al arrancar cada concepto y reanuda desde el último checkpoint. Sin `estado.json` no hay recuperación.
- `--force` re-ejecuta desde la primera fase; `--retry-failed` solo reintenta terminales reintentables.
- Logging estructurado (JSON Lines) con flush por línea, un archivo por corrida, sin secretos ni contenido de notas.
- Reporte final siempre (incluso parcial/interrumpido) en `workdir/reports/run-<run_id>.json` (+ `.md` opcional).
- Circuit breaker ante fallos consecutivos de backend para evitar hammering.
- Limpieza best-effort de notebooks huérfanos ante fallo; se reportan al final.
- Manejo de señales (Ctrl+C/SIGTERM): persiste estado, genera reporte parcial, sale limpio.
- El runner NO toca el vault: solo coordina, persiste estado (vía state.py) y escribe logs/reportes en `workdir`.
- El runner NO re-valida la síntesis: confía en que la validación (Capa 8) ya pasó antes de writing.
---

## Capa 10 — CLI (cli.py) (pseudo-código de alto nivel)

### Objetivo de la capa
Ser la interfaz de entrada para humanos y agentes sobre el orquestador (Capa 9). Expone subcomandos para escanear, inspeccionar, ejecutar, consultar estado, revisar bloqueados/fallidos y resetear conceptos, más un reporte final legible. Sin prompts interactivos: todo se controla por flags y argumentos. Produce salida humana (colores, tablas) o JSON (`--json`) para consumo por agentes/CI. La CLI no contiene lógica de negocio: valida argumentos, carga config, instancia el runner y delega. Toda la verdad del progreso vive en `estado.json` y en los reportes del runner.

### 1) Cómo se invoca y se configura

Punto de entrada: `python -m cli` o el script `ai` (entry point en `pyproject.toml` / `setup.cfg`). La CLI es un wrapper delgado sobre `Runner` (Capa 9). No importa fases ni backend directamente.

```python
# cli.py (alto nivel)
import argparse, sys, asyncio
from pathlib import Path

def main(argv=None) -> int:
    parser = build_parser()          # define subcomandos y flags globales
    args = parser.parse_args(argv)
    config = load_config(args)       # config.yaml + env + flags (precedencia CLI > env > config)
    setup_logging(config)             # nivel (info/debug), formato
    runner = Runner(config)          # singleton de la corrida
    try:
        return asyncio.run(dispatch(args, runner))   # despacha al subcomando
    except KeyboardInterrupt:
        runner.handle_interrupt()     # persiste estado + reporte parcial
        return 130
    except RunnerError as e:
        print_error(e)
        return 2
    finally:
        runner.close()

if __name__ == "__main__":
    sys.exit(main())
```

Configuración (precedencia, de mayor a menor):
1. Flags de CLI (`--backend`, `--workdir`, `--vault`, `--force`, etc.).
2. Variables de entorno (`AI_WORKDIR`, `AI_VAULT_ROOT`, `BACKEND_PROVIDER`, `AI_CONFIG`, `NO_COLOR`).
3. Archivo de config (`config.yaml` o el path de `--config` / `AI_CONFIG`).
4. Defaults internos.

```python
def load_config(args) -> RunConfig:
    # 1. base desde archivo
    cfg_path = args.config or os.getenv("AI_CONFIG") or "config.yaml"
    base = load_yaml(cfg_path) if Path(cfg_path).exists() else {}
    # 2. env overrides
    if os.getenv("AI_WORKDIR"):      base["workdir"] = os.getenv("AI_WORKDIR")
    if os.getenv("AI_VAULT_ROOT"):   base["vault_root"] = os.getenv("AI_VAULT_ROOT")
    if os.getenv("BACKEND_PROVIDER"): base["backend"]["provider"] = os.getenv("BACKEND_PROVIDER")
    # 3. CLI overrides (ganan)
    if args.workdir:   base["workdir"] = args.workdir
    if args.vault:     base["vault_root"] = args.vault
    if args.backend:   base["backend"]["provider"] = args.backend
    if args.max_retries is not None: base["max_retries"] = args.max_retries
    if args.pacing is not None:       base["pacing_between_concepts_s"] = args.pacing
    # 4. validar y construir RunConfig (Capa 9)
    return RunConfig(**normalize(base, args))
```

Reglas de invocación:
- La CLI se ejecuta siempre desde la raíz del proyecto (`C:\Users\DGVit\Proyectos\...`) o con `--workdir`/`--vault` explícitos. No asume rutas relativas al CWD si no encuentra `config.yaml` (error claro).
- Sin prompts interactivos: si falta un argumento requerido, falla con código de salida != 0 y mensaje de uso. Nunca llama a `input()`.
- `--config <path>` permite usar configs alternativas (ej. `config.pilot.yaml`). Default `config.yaml` en el CWD.
- `--json` activa salida estructurada (un JSON por comando) para agentes/CI. En modo JSON se suprimen colores, spinners y tablas.
- `--quiet` / `-q` reduce la salida a errores y al resultado final. `--verbose` / `-v` activa debug (backend calls, checkpoints).
- `--no-color` (o env `NO_COLOR`) desactiva colores. En Windows se detecta soporte ANSI; si no, se cae a texto plano.
- Exit codes: `0` OK, `1` error genérico / concepto fallido, `2` error de uso/argumentos, `130` interrumpido (Ctrl+C). Los agentes pueden basarse en estos códigos.

### 2) Comandos principales

#### `scan` — descubrir conceptos del vault

```python
async def cmd_scan(args, runner) -> int:
    scan = scan_concepts(runner.config.vault_root)      # Capa 2
    concepts = scan.concepts
    notes_without_block = scan.notes_without_block
    if args.json:
        print_json({"concepts": [asdict(c) for c in concepts],
                    "notes_without_block": notes_without_block,
                    "total": len(concepts)})
        return 0
    print_table(concepts, columns=["id", "title", "area", "has_block"])
    print(f"\nTotal conceptos con bloque: {len(concepts)}")
    if notes_without_block:
        print(f"Notas sin bloque ai:start/end: {len(notes_without_block)} (ver `ai review --orphans`)")
    return 0
```

Flags de `scan`: `--json`, `--area <area>`, `--orphans` (solo notas sin bloque), `--count`.

#### `inspect` — inspeccionar un concepto

```python
async def cmd_inspect(args, runner) -> int:
    concept = load_concept(args.concept_id)               # Capa 2
    state = runner.state_store.load(args.concept_id)      # Capa 3
    sources = load_sources(args.concept_id)               # Capa 6 (si existe)
    synthesis = load_synthesis(args.concept_id)           # Capa 7 (si existe)
    validation = load_validation(args.concept_id)        # Capa 8 (si existe)
    if args.json:
        print_json({"concept": asdict(concept), "state": asdict(state) if state else None,
                    "sources": asdict(sources) if sources else None,
                    "synthesis": summarize(synthesis) if synthesis else None,
                    "validation": summarize(validation) if validation else None})
        return 0
    print_concept_card(concept, state, sources, synthesis, validation)
    return 0
```

Flags de `inspect`: `--json`, `--show-markdown` (imprime el markdown de la síntesis si existe), `--show-sources`, `--show-validation`.

#### `run` — procesar un solo concepto

```python
async def cmd_run(args, runner) -> int:
    concept_id = args.concept_id
    overrides = build_overrides(args)                    # force, dry_run, stop_after, etc.
    result = await runner.run_one(concept_id, **overrides)   # Capa 9
    if args.json:
        print_json(asdict(result))
    else:
        print_concept_result(result)                    # estado, duracion, score, coverage
    # exit code: 0 si done, 1 si failed/blocked
    return 0 if result.status == "done" else 1
```

Flags de `run`: `--force`, `--dry-run`, `--stop-after <phase>`, `--re-research`, `--re-synthesize`, `--re-validate`, `--backend <provider>`, `--max-retries N`, `--json`, `--hint "..."` (se agrega a `extra_hints` del concepto).

#### `run-batch` — procesar el lote

```python
async def cmd_run_batch(args, runner) -> int:
    concept_ids = resolve_concept_ids(args)              # --only, --from, --area, --status
    report = await runner.run_batch(concept_ids, **build_overrides(args))
    if args.json:
        print_json(asdict(report))
    else:
        print_report_summary(report)                    # tabla resumen + fallidos/bloqueados
    return 0 if report.totals["failed"] == 0 and report.totals["blocked"] == 0 else 1
```

Flags de `run-batch`: hereda todos los de `run` más los de filtrado (`--only`, `--from`, `--area`, `--status`, `--concept-order`).

#### `status` — estado agregado del lote

```python
async def cmd_status(args, runner) -> int:
    # lee estado.json + ultimo reporte; NO ejecuta nada
    state = runner.state_store.load_all()                # dict concept_id -> ConceptState
    last_report = load_latest_report(runner.config.workdir)
    agg = aggregate_status(state, last_report)           # counts por status, por area, etc.
    if args.json:
        print_json(agg)
        return 0
    print_status_dashboard(agg)                          # barras, counts, ultimo run
    if args.failed:    print_failed_list(state, args.limit)
    if args.blocked:   print_blocked_list(state, args.limit)
    if args.low:       print_low_coverage_list(state, last_report, args.limit)
    return 0
```

Flags de `status`: `--json`, `--failed`, `--blocked`, `--low` (baja cobertura/fuentes), `--area <area>`, `--limit N`, `--run <run_id>` (reporte específico), `--watch` (refresca cada N segundos, solo salida humana).

#### `review` — revisar conceptos bloqueados/fallidos con detalle

```python
async def cmd_review(args, runner) -> int:
    # muestra el detalle de un concepto bloqueado/fallido (o todos) para accion humana
    targets = [args.concept_id] if args.concept_id else list_blocked_and_failed(runner.state_store)
    for cid in targets:
        st = runner.state_store.load(cid)
        val = load_validation(cid)                       # Capa 8
        print_review_card(cid, st, val)                  # error, checks fallidos, sugerencias
        if args.show_markdown and has_synthesis(cid):
            print(read_synthesis_markdown(cid))
    if args.json:
        print_json([review_payload(cid) for cid in targets])
    return 0
```

Flags de `review`: `--json`, `--show-markdown`, `--errors <structural|content|semantic|all>` (filtra por tipo de check fallido), `--orphans` (notas sin bloque + notebooks huérfanos).

#### `reset` — resetear estado de un concepto (o del lote)

```python
async def cmd_reset(args, runner) -> int:
    if args.all:
        confirm_or_fail(args)                            # sin prompts: requiere --yes
        runner.state_store.reset_all(scope=args.scope)   # pending para todos (o filtrado)
    elif args.concept_id:
        runner.state_store.reset(args.concept_id, to=args.to or "pending")
        # opcionalmente borrar artefactos: sources.json, raw_research.json, synthesis.json, validation.json
        if args.artifacts:
            clean_artifacts(args.concept_id, kinds=args.artifacts)
    else:
        fail("falta concept_id o --all")
    # --dry-run muestra que se resetearia sin tocar estado
    if args.dry_run:
        print_what_would_reset(targets)
        return 0
    print_reset_summary(targets)
    return 0
```

Flags de `reset`: `--to <status>` (default `pending`), `--artifacts <list>` (sources, research, synthesis, validation, all), `--all`, `--area <area>`, `--status <status>` (resetear solo los que estén en ese estado), `--yes` (confirmación no interactiva, obligatoria con `--all`), `--dry-run`, `--json`.

Reglas de `reset`:
- `reset` modifica `estado.json` (y opcionalmente artefactos en `workdir`). NUNCA toca el vault ni las notas. El contenido ya escrito en el vault queda intacto; solo se resetea el pipeline para re-procesar.
- `--all` sin `--yes` falla (exit 2) para evitar borrados accidentales en modo no interactivo.
- Resetear a `pending` vuelve a correr todo desde la primera fase. Resetear a un estado intermedio (ej. `synthesizing`) reanuda desde esa fase (útil para re-sintetizar sin re-investigar).
- Si se resetea un concepto `done`, el runner NO revierte el vault: la próxima corrida reescribe el bloque (idempotente por hash del afuera). Se recomienda `--force` en el `run` posterior.

#### `report` — generar/mostrar el reporte de una corrida

```python
async def cmd_report(args, runner) -> int:
    if args.run_id:
        report = load_report(runner.config.workdir, args.run_id)
    elif args.last:
        report = load_latest_report(runner.config.workdir)
    else:
        # regenerar a partir del estado actual (sin re-ejecutar)
        report = build_report_from_state(runner.state_store, runner.config)
    if args.json:
        print_json(asdict(report))
        return 0
    if args.md:
        print(render_report_markdown(report))          # Markdown legible (ver Capa 9)
    elif args.summary:
        print_report_summary(report)                   # una linea por metrica
    else:
        print_full_report(report)                      # tablas: fallidos, bloqueados, baja cobertura, links rotos
    # exportar
    if args.out:
        write_report(args.out, report, fmt=args.format)   # json | md | csv
    return 0
```

Flags de `report`: `--run <run_id>`, `--last`, `--md`, `--summary`, `--out <path>`, `--format <json|md|csv>`, `--failed`, `--blocked`, `--low`, `--orphans`, `--json`, `--limit N`.

Reglas de `report`:
- `report` es de solo lectura: no ejecuta el pipeline ni modifica estado. Solo lee `estado.json` y los reportes en `workdir/reports/`.
- `--run <run_id>` permite consultar una corrida histórica (los reportes se conservan por `run_id`).
- `--out` exporta a un archivo (útil para compartir con el equipo o archivar). El formato se infiere de la extensión si no se pasa `--format`.
- `--failed`/`--blocked`/`--low`/`--orphans` filtran la salida a esas categorías (se pueden combinar).
- En modo `--json`, la salida es el `FinalReport` serializado (Capa 9) para consumo por agentes.

### 3) Flags y opciones (transversales)

Flags globales (válidos en todos los subcomandos):

| Flag | Env | Descripción |
|---|---|---|
| `--config <path>` | `AI_CONFIG` | Archivo de config alternativo |
| `--workdir <path>` | `AI_WORKDIR` | Directorio de trabajo (estado, logs, reportes) |
| `--vault <path>` | `AI_VAULT_ROOT` | Raíz del vault de Obsidian |
| `--backend <fake\|notebooklm>` | `BACKEND_PROVIDER` | Proveedor de backend |
| `--json` | — | Salida estructurada (JSON) |
| `--quiet` / `-q` | — | Solo errores y resultado final |
| `--verbose` / `-v` | — | Nivel debug (backend calls, checkpoints) |
| `--no-color` | `NO_COLOR` | Desactivar colores |
| `--max-retries N` | — | Sobrescribe `max_retries` |
| `--pacing <seg>` | — | Sobrescribe pacing entre conceptos |

Flags de filtrado (para `run-batch`, `status`, `reset`, `report`):

| Flag | Descripción |
|---|---|
| `--area <area>` | Filtra por área del concepto (ej. `frontend`, `backend`, `data`, `infra`) |
| `--concept <id>` / `--only <ids>` | Concepto(s) específico(s) (coma-separado o repetible) |
| `--from <concept_id>` | Reanudar desde un concepto (inclusive) en el orden configurado |
| `--hasta <concept_id>` | Procesar hasta un concepto (inclusive) — define un rango con `--from` |
| `--status <status>` | Filtra por estado (`pending`, `failed`, `blocked`, `done`, ...) |
| `--concept-order <numeric\|scan\|mtime>` | Orden de procesamiento |

Flags de ejecución:

| Flag | Descripción |
|---|---|
| `--dry-run` | Genera todo (investigación, síntesis, validación) y muestra el diff/resultados SIN escribir en el vault ni cambiar estado. No persiste artefactos de escritura. |
| `--force` | Ignora idempotencia/frescura y re-ejecuta desde la primera fase (no borra artefactos previos; las fases deciden por hash). |
| `--retry-failed` | Solo reintenta conceptos en `failed`/`blocked` (no toca los `done`). |
| `--stop-after <phase>` | Detiene el concepto (y el lote) tras completar la fase indicada (`researching`, `synthesizing`, `validating`, `writing`). Útil para calibración. |
| `--re-research` | Fuerza re-investigación aunque `raw_research.json` esté fresco. |
| `--re-synthesize` | Fuerza re-síntesis aunque `synthesis.json` sea válido. |
| `--re-validate` | Fuerza re-validación aunque `validation.json` sea válido. |
| `--strict` | Activa `strict_mode` en validación (warnings bloquean). |
| `--cleanup-notebooks` / `--no-cleanup-notebooks` | Limpia notebooks del backend tras cada concepto. |
| `--keep-history` | Versiona artefactos por timestamp en lugar de sobrescribir. |
| `--hint "..."` | Agrega un hint manual al contexto de investigación del concepto (repetible). |

Flags de `reset`:

| Flag | Descripción |
|---|---|
| `--to <status>` | Estado destino del reset (default `pending`). |
| `--artifacts <list>` | Artefactos a borrar: `sources`, `research`, `synthesis`, `validation`, `all`. |
| `--all` | Resetear todos los conceptos del scope (requiere `--yes`). |
| `--yes` | Confirmación no interactiva (obligatoria con `--all`). |

Reglas de combinación:
- `--from` y `--hasta` definen un rango por el orden configurado (`--concept-order`). Si solo se pasa `--from`, procesa desde ahí hasta el final. Si solo `--hasta`, desde el inicio hasta ahí.
- `--concept`/`--only` tiene prioridad sobre `--from`/`--hasta`/`--area` (si se pasa, los otros filtros se ignoran con un warning en `--verbose`).
- `--dry-run` es compatible con `run` y `run-batch` (y con `reset` para previsualizar). En `run`, no persiste estado ni artefactos de escritura; muestra el diff del writer y el resultado de validación.
- `--force` + `--dry-run` es válido: fuerza re-ejecución de las fases pero no escribe en el vault.
- `--stop-after` no se puede combinar con `--dry-run` (dry-run ya detiene antes de writing; se ignora con warning).
- Flags desconocidos / combinaciones inválidas → error de uso (exit 2) con mensaje claro, sin ejecutar nada.

### 4) Output y feedback al usuario

Principios:
- Modo humano por defecto: colores (si el terminal lo soporta), tablas alineadas, spinners para operaciones largas, mensajes claros con iconos (✓, ✗, ⚠, ℹ).
- Modo `--json`: un único objeto JSON por comando en stdout (sin colores, sin spinners, sin texto extra). Los logs del runner van a `workdir/logs/`, no a stdout. Los errores van a stderr.
- `--quiet`: solo el resultado final (una línea) y los errores. Útil para scripts.
- Separación stdout/stderr: datos y resultados en stdout; logs, progreso y errores en stderr. En `--json`, stdout contiene únicamente el JSON.

Feedback durante la ejecución (`run` / `run-batch`):
```python
def print_progress(concept_id, idx, total, phase, status):
    # stderr, para no contaminar stdout en --json
    line = f"[{idx}/{total}] {concept_id} — {phase} ... "
    sys.stderr.write(line); sys.stderr.flush()
    # al terminar la fase: "✓ researching (2.1s)" o "✗ synthesizing: BackendTimeout"
```

- Spinner animado mientras una fase está en curso (solo modo humano, sin `--json`/`--quiet`).
- Por concepto: se muestra el estado final (`done`/`failed`/`blocked`), la duración, el score de validación y la cobertura.
- Por lote: al final se imprime el resumen (`Total / Done / Failed / Blocked / Skipped`) y las listas de fallidos/bloqueados/baja cobertura/links rotos (truncadas con `--limit`, default 20).
- Si el lote se interrumpe (Ctrl+C): se imprime "Interrumpido. Estado persistido. Reporte parcial en <path>." y se sale con código 130.

Formatos de salida:
```python
# humano (default): tabla con columnas alineadas
print_table(rows, columns=["concept_id", "status", "phase", "score", "coverage", "duration_ms"])

# json: serializacion directa del dataclass
print_json(asdict(result))   # ensure_ascii=False, indent=2 si no es --quiet

# md: para `report --md`
print(render_report_markdown(report))

# csv: para `report --format csv --out <path>`
write_csv(path, rows, header=[...])
```

Códigos de salida:
- `0`: comando exitoso (sin conceptos fallidos/bloqueados, o consulta de solo lectura OK).
- `1`: hubo conceptos `failed`/`blocked`, o un concepto `run` terminó en estado no-`done`.
- `2`: error de uso/argumentos/config (falta concept_id, combinación inválida, config inexistente, credenciales inválidas al arrancar).
- `130`: interrumpido por el usuario (Ctrl+C).
- En `--json`, el código de salida sigue siendo el mismo; el JSON en stdout incluye un campo `exit_code` y `error` para que el agente no dependa solo del código.

Mensajes de error:
- Siempre incluyen: qué falló, por qué (causa raíz resumida) y qué hacer (siguiente paso sugerido).
- Errores de config: "config.yaml no encontrado en <path>. Usá --config o AI_CONFIG." / "credenciales de NotebookLM inválidas: ejecutá `opencode mcp auth notebooklm` o revisá auth_file."
- Errores de estado: "concepto 'X' no existe en el vault. Ejecutá `ai scan` para ver los disponibles."
- Errores de reset: "`--all` requiere `--yes` en modo no interactivo."
- En `--json`, los errores se emiten como `{"error": "...", "code": 2, "hint": "..."}` en stderr y el proceso sale con el código correspondiente.

Feedback específico por comando:
- `scan`: "Escaneados N archivos .md, M conceptos con bloque, K sin bloque."
- `inspect`: tarjeta con metadatos, estado, artefactos presentes (sources/raw_research/synthesis/validation) y su frescura.
- `run <id>`: línea final "✓ <id> → done (12.3s, score 0.92, coverage 0.83)" o "✗ <id> → failed en validating: V_SEM_SEPARATION".
- `run-batch`: resumen + "Reporte guardado en workdir/reports/run-<run_id>.json".
- `status`: dashboard con barras por estado y por área; "Última corrida: run-... (hace 2h, 240/255 done)".
- `review`: por cada concepto bloqueado/fallido, muestra el `blocked_reason`/`error`, los checks fallidos (con severidad) y una sugerencia ("revisar sección Fundamento: contiene versiones", "renovar credenciales de NotebookLM").
- `reset`: "Reseteados N conceptos a 'pending'. Artefactos borrados: synthesis, validation. (vault intacto)".
- `report`: imprime el reporte (resumen/tabla/markdown) y, si `--out`, "Reporte exportado a <path>".

Integración con el runner (Capa 9):
```python
# la CLI solo coordina; toda la logica vive en Runner
async def dispatch(args, runner):
    cmd = args.command
    if cmd == "scan":       return await cmd_scan(args, runner)
    if cmd == "inspect":    return await cmd_inspect(args, runner)
    if cmd == "run":        return await cmd_run(args, runner)
    if cmd == "run-batch":  return await cmd_run_batch(args, runner)
    if cmd == "status":     return await cmd_status(args, runner)
    if cmd == "review":     return await cmd_review(args, runner)
    if cmd == "reset":      return await cmd_reset(args, runner)
    if cmd == "report":     return await cmd_report(args, runner)
    # alias: `ai run` sin id == run-batch sobre toda la cola
    if cmd is None:
        return await cmd_run_batch(args, runner)
```

Reglas de integración:
- La CLI instancia un único `Runner` por invocación (backend singleton, state store, writer, logger). No se crea un runner por concepto.
- La CLI no llama a fases ni al backend directamente; todo pasa por `runner.run_one` / `runner.run_batch` / `runner.status` / `runner.review`.
- Los filtros (`--area`, `--concept`, `--from`, `--hasta`, `--status`) se traducen a `only_concept_ids` / `area_filter` / `from_concept` del `RunConfig` (Capa 9).
- `--dry-run` se propaga como `RunConfig.dry_run = True`. El runner y las fases respetan el flag (el writer muestra diff sin escribir; el estado no cambia).
- `--json` no cambia la ejecución, solo el formato de salida. En `--json`, el progreso (spinners) se suprime y el resultado final se imprime como un único JSON en stdout.
- Señales: Ctrl+C se captura en `main()` y se delega a `runner.handle_interrupt()`, que persiste estado y genera reporte parcial (Capa 9). La CLI imprime el mensaje de interrupción y sale con 130.
- La CLI no mantiene estado propio: todo el progreso vive en `estado.json` y en los reportes del runner. Re-ejecutar un comando es idempotente a nivel de "qué se procesa" (el runner decide por estado).

### Excepciones de la capa

```python
class CLIError(Exception): ...           # error genérico de la CLI (mensaje para el usuario)
class UsageError(CLIError): ...          # error de uso/argumentos (exit 2)
class ConfigError(CLIError): ...         # config inválida o inexistente (exit 2)
class ConceptNotFoundError(CLIError): ... # concepto no existe en el vault (exit 2)
class ConfirmationRequiredError(CLIError):... # falta --yes en operacion destructiva (exit 2)
```

Reglas:
- La CLI captura `CLIError` y las excepciones del runner (`RunnerError`, `StateCorruptError`, etc.) y las traduce a mensajes amigables + código de salida. Nunca muestra un traceback al usuario salvo en `--verbose`.
- En `--json`, el error se serializa como `{"error": "...", "code": N, "hint": "..."}` en stderr.
- `KeyboardInterrupt` se maneja aparte (exit 130) sin traceback.

### Reglas de negocio (de la spec)

- La CLI es la única interfaz para humanos y agentes; no hay prompts interactivos. Toda decisión se pasa por flag.
- Sin lógica de negocio en la CLI: valida argumentos, carga config, instancia el runner y delega. Las fases (Capas 6-8) y el estado (Capa 3) no se tocan directamente.
- Precedencia de config: CLI > env > archivo > defaults. Se valida fail-fast al arrancar (config inexistente o inválida → exit 2 antes de procesar).
- `--json` produce salida parseable por agentes/CI; modo humano produce salida legible con colores/tablas (degradan a texto plano sin ANSI).
- Exit codes estables: 0 OK, 1 fallidos/bloqueados, 2 error de uso/config, 130 interrumpido.
- `--dry-run` nunca escribe en el vault ni cambia estado; muestra diff y resultados.
- `reset` nunca toca el vault; solo `estado.json` y artefactos en `workdir`. Operaciones destructivas (`--all`) requieren `--yes`.
- `report` es de solo lectura: no ejecuta el pipeline.
- stdout = datos/resultados; stderr = progreso/logs/errores. En `--json`, stdout contiene únicamente el JSON.
- La CLI no mantiene estado propio: toda la verdad vive en `estado.json` y en `workdir/reports/`. Re-ejecutar es seguro.
- Secretos (auth, cookies) nunca se imprimen ni se registran, incluso en `--verbose`.
- En Windows se usan rutas y comandos apropiados (PowerShell, `py` para Python). La CLI detecta el SO solo para elegir colores/ANSI; la lógica es idéntica.
- La CLI se invoca como `ai <subcomando> [flags]` (entry point) o `py -m cli <subcomando> [flags]`. Sin subcomando, equivale a `run-batch` sobre toda la cola.

---

## Capa 11 — Piloto + calibración (pseudo-código de alto nivel)

### Objetivo de la capa

Cerrar el ciclo: con las 10 capas anteriores implementadas y probadas en aislamiento (backend fake, tests unitarios), se ejecuta un piloto end-to-end sobre un único concepto real y representativo (`frontend-01-internet-web`). El piloto valida que todo el pipeline (investigación → síntesis → validación → escritura) funciona sobre datos reales, que la integridad del vault se mantiene, y que los parámetros por defecto son razonables. A partir del piloto se calibran los parámetros y se definen los criterios de aceptación que habilitan el escalamiento al frontend completo y luego a las demás áreas. Esta capa NO agrega lógica de negocio nueva: orquesta, mide y decide.

### 1) Proceso de piloto con 1 concepto (frontend-01)

#### Selección del concepto piloto

- Concepto: `frontend-01-internet-web` (Internet y la web). Se elige porque:
  - Es estable (fundamento invariante: TCP/IP, HTTP, DNS, navegador) → permite probar la separación fundamento/práctica.
  - Tiene conexiones ricas (HTTP, DNS, navegador, protocolos) → prueba cross-links.
  - Hay abundante fuente canónica (MDN, RFCs, web.dev) → prueba seeds/preferred domains y trazabilidad.
  - Área frontend → prueba el contexto de prompts `frontend`.
  - Tiene contenido manual previo (notas del autor) → prueba preservación del afuera y `manual_notes`.
- El concepto debe tener bloque `ai:start/end` válido (Capa 2) antes de arrancar. Si no lo tiene, se agrega manualmente (NO automáticamente) y se registra en el reporte.

#### Preparación del entorno

```python
# config.pilot.yaml (variante del config.yaml para el piloto)
pilot:
  concept_id: "frontend-01-internet-web"
  backend: "notebooklm"          # o "fake" para dry-run sin red
  dry_run_first: true            # siempre dry-run antes del run real
  keep_history: true             # versionar artefactos (no sobrescribir)
  strict_validation: true       # warnings bloquean en el piloto (calibracion)
  cleanup_notebooks: true
  report_markdown: true

run:
  max_retries: 3
  pacing_between_concepts_s: 1.0
  stop_after_phase: null         # null = pipeline completo; o "researching"/etc. para cortar
```

Checklist pre-piloto:

1. `ai scan` → confirmar que `frontend-01-internet-web` aparece con bloque.
2. `ai inspect frontend-01-internet-web` → verificar metadatos (title, area, key_ideas, connections).
3. Backup del vault (copia completa) y snapshot de `workdir/` si existía.
4. Verificar credenciales de NotebookLM (`opencode mcp auth notebooklm` o validar `auth_file`).
5. Confirmar que no hay cambios sin commitear en el vault (git status limpio) para poder comparar.

#### Ejecución paso a paso (dry-run primero, luego real)

```python
@dataclass
class PilotConfig:
    concept_id: str = "frontend-01-internet-web"
    workdir: Path
    vault_root: Path
    backend: str = "notebooklm"
    dry_run_first: bool = True
    keep_history: bool = True
    strict: bool = True

async def run_pilot(cfg: PilotConfig) -> PilotReport:
    runner = Runner(build_run_config(cfg))

    # Fase 0: dry-run completo (no escribe en el vault, no cambia estado)
    if cfg.dry_run_first:
        logger.info("pilot_dry_run_start", concept_id=cfg.concept_id)
        dry_result = await runner.run_one(cfg.concept_id, dry_run=True, force=True)
        dump_artifact(cfg.workdir, "pilot/dry_run_result.json", dry_result)
        # mostrar diff del writer y resultado de validacion
        print_dry_run_summary(dry_result)
        if not confirm("¿Continuar con el run real? (s/n)") and not cfg.auto:
            return PilotReport(status="aborted_at_dry_run", dry_result=dry_result)
        logger.info("pilot_dry_run_ok", concept_id=cfg.concept_id)

    # Fase 1: run real completo
    t0 = now_ms()
    result = await runner.run_one(cfg.concept_id, force=True, strict=cfg.strict)
    duration_ms = now_ms() - t0

    # Fase 2: recolectar evidencia
    evidence = collect_pilot_evidence(cfg.concept_id, cfg.workdir, cfg.vault_root)

    report = PilotReport(
        concept_id=cfg.concept_id,
        status=result.status,
        duration_ms=duration_ms,
        run_result=result,
        evidence=evidence,
        started_at=iso(t0),
        finished_at=now_iso(),
    )
    persist_pilot_report(cfg.workdir, report)
    return report
```

Comandos del piloto (en orden):

```bash
# 1. dry-run (no escribe nada)
ai run frontend-01-internet-web --dry-run --force --strict --verbose

# 2. inspeccionar el diff y la validacion antes de escribir
ai inspect frontend-01-internet-web --show-markdown --show-validation

# 3. run real
ai run frontend-01-internet-web --force --strict

# 4. verificar el resultado
ai inspect frontend-01-internet-web
ai review frontend-01-internet-web --show-markdown
```

#### Captura de métricas del piloto

```python
@dataclass
class PilotEvidence:
    # Integridad del vault
    outside_hash_before: str
    outside_hash_after: str
    outside_integrity_ok: bool          # hash before == hash after
    markers_count_after: tuple[int, int] # (start, end) debe ser (1, 1)
    frontmatter_byte_identical: bool
    headings_preserved: bool
    manual_sections_preserved: bool     # "Que abarca", "Relacionados"
    # Pipeline
    research_coverage: float
    research_sources_count: int
    research_low_coverage: bool
    research_low_sources: bool
    synthesis_sections_present: list[str]
    synthesis_unverified_claims: int
    synthesis_cross_links_total: int
    synthesis_broken_links: int
    validation_score: float
    validation_errors: list[str]
    validation_warnings: list[str]
    # Tiempos
    research_duration_ms: int
    synthesis_duration_ms: int
    validation_duration_ms: int
    writing_duration_ms: int
    total_duration_ms: int
    # Contenido
    word_count_by_section: dict[str, int]
    code_fences_count: int
    citations_count: int
    unverified_marked_count: int

def collect_pilot_evidence(concept_id, workdir, vault_root) -> PilotEvidence:
    concept = load_concept(concept_id)
    state = load_state(concept_id)
    sources = load_sources(concept_id)
    raw = load_raw_research(concept_id)
    synthesis = load_synthesis(concept_id)
    validation = load_validation(concept_id)
    # leer la nota para verificar integridad del afuera (backup pre-piloto vs actual)
    ...
    return PilotEvidence(...)
```

Reglas del piloto:

- El piloto se ejecuta siempre con `--dry-run` primero. Si el dry-run falla (validación con errores), NO se ejecuta el run real hasta corregir.
- El piloto usa `--force` para ignorar idempotencia (es la primera corrida real; no hay artefactos previos).
- El piloto usa `--strict` (warnings bloquean) para detectar problemas de calibración temprano.
- El piloto mantiene historial (`keep_history: true`) para poder comparar versiones si se recalibra.
- El piloto NO modifica otros conceptos: solo `frontend-01-internet-web`. La cola del runner se filtra con `--only frontend-01-internet-web` (o `run_one`).
- Si el piloto falla en cualquier fase, se detiene (no se reintenta automáticamente en modo piloto) para poder inspeccionar. El reintento manual se hace con `ai run ... --retry` tras corregir.
- Toda la evidencia del piloto se persiste en `workdir/pilot/pilot_report.json` (más el reporte de la corrida en `workdir/reports/`).

### 2) Validación de resultados

La validación del piloto tiene dos capas: la automática (Capa 8, ya ejecutada) y la revisión humana (checklist manual). El piloto NO se considera exitoso solo porque `is_valid = True`; se requiere revisión humana del contenido.

#### Checklist de validación automática (ya cubierto por Capa 8)

- `validation_score >= 0.85` (17 checks, al menos 15/17 pasando; warnings dentro del umbral).
- 0 checks de severidad `error` fallidos (`V_STRUCT_SECTIONS`, `V_STRUCT_HEADINGS`, `V_CONTENT_NO_PLACEHOLDERS`, `V_LINKS_NO_INVENTED`, `V_FRONTMATTER_*`, `V_SEM_UNVERIFIED_MARKED`, `V_SEM_SEPARATION`).
- `is_valid = True` con `strict_mode = True`.

#### Checklist de validación manual (revisión humana del contenido)

```python
@dataclass
class ManualReviewChecklist:
    # Contenido
    definition_clear: bool              # definicion de 2-4 oraciones, sin jerga
    how_it_works_accurate: bool        # mecanismo correcto y con modelo mental claro
    examples_runnable: bool             # los ejemplos de codigo son validos/ejecutables
    common_errors_relevant: bool       # errores comunes reales y accionables
    # Separacion fundamento/practica
    foundation_stable: bool            # fundamento sin versiones ni herramientas especificas
    practice_modern: bool              # practica con versiones/herramientas actuales (2026)
    separation_clean: bool             # no se mezclan fundamento y practica
    # Trazabilidad
    citations_accurate: bool           # las citas [src-N] apuntan a fuentes que realmente soportan la afirmacion
    unverified_justified: bool        # los [UNVERIFIED] son razonables (no hay alucinacion)
    # Cross-links
    cross_links_valid: bool           # los wikilinks resuelven o estan bien marcados como pendiente
    no_invented_concepts: bool        # no hay conceptos vecinos inventados
    # Preservacion del vault
    outside_untouched: bool          # el afuera de la nota no cambio (hash byte a byte)
    frontmatter_untouched: bool      # frontmatter identico
    manual_notes_respected: bool     # el contenido manual del autor no fue contradicho sin justificar
    # Estilo/idioma
    spanish_rioplatense: bool        # redaccion en español argentino, tono pedagogico
    no_placeholders: bool            # sin TODO/XXX/[...]

def manual_review(concept_id: str) -> ManualReviewChecklist:
    # el humano revisa el markdown generado (ai review <id> --show-markdown)
    # y completa el checklist. Se persiste en workdir/pilot/manual_review.json
    ...
```

#### Integridad del vault (verificación automatizada post-piloto)

```python
def verify_vault_integrity(concept_id: str, backup_dir: Path, vault_root: Path) -> IntegrityReport:
    note_path = find_note(vault_root, concept_id)
    current = note_path.read_bytes()
    backup = (backup_dir / concept_id / note_path.name).read_bytes()  # backup pre-piloto
    # 1. outside hash
    outside_before = extract_outside(backup.decode("utf-8"))
    outside_after = extract_outside(current.decode("utf-8"))
    outside_ok = (sha256(outside_before) == sha256(outside_after))
    # 2. marcadores
    markers_ok = (count_markers(current.decode("utf-8")) == (1, 1))
    # 3. frontmatter byte a byte
    fm_ok = (extract_frontmatter_block(backup.decode("utf-8")) ==
             extract_frontmatter_block(current.decode("utf-8")))
    # 4. headings requeridos presentes
    headings_ok = all(h in current.decode("utf-8") for h in ["Que abarca", "Relacionados"])
    return IntegrityReport(outside_ok=outside_ok, markers_ok=markers_ok,
                          frontmatter_ok=fm_ok, headings_ok=headings_ok,
                          all_ok=outside_ok and markers_ok and fm_ok and headings_ok)
```

Reglas de validación de resultados:

- El piloto se considera "validado" solo cuando: (a) la validación automática pasa en modo estricto, (b) la checklist manual está completa con todos los items en `True`, y (c) la integridad del vault es 100% (outside hash idéntico, marcadores 1/1, frontmatter byte a byte).
- Si algún item manual es `False`, se registra como "hallazgo del piloto" y se decide: corregir el prompt/config (y re-correr) o aceptar como limitación documentada.
- La validación del piloto NO se salta: no hay "piloto automático". El humano revisa el contenido generado.
- Los hallazgos se persisten en `workdir/pilot/findings.json` con severidad (bloqueante / no bloqueante) para alimentar la calibración (sección 3).

### 3) Calibración de parámetros

A partir de los hallazgos del piloto se ajustan los parámetros que controlan calidad, costo y estabilidad. La calibración se hace en dos niveles: (a) parámetros de validación (umbrales de calidad) y (b) parámetros operativos (pacing, timeouts, concurrencia).

#### Parámetros a calibrar (con valores iniciales y rango)

```python
@dataclass
class CalibrationParams:
    # --- Validacion (Capa 8) ---
    trace_threshold: float = 0.6          # ratio minimo de afirmaciones con cita [src-N]
    min_words: dict[str, int] = field(default_factory=lambda: {
        "definicion": 40, "como_funciona": 80, "ejemplos": 60,
        "errores_comunes": 60, "fundamento": 80, "practica": 60,
        "relacionados": 10,
    })
    max_warnings_before_block: int = 5
    strict_mode_pilot: bool = True       # en produccion: False (warnings no bloquean)
    # --- Investigacion (Capa 6) ---
    coverage_threshold: float = 0.7       # cobertura minima de investigacion
    max_sources: int = 12
    min_sources: int = 4
    max_questions_per_concept: int = 12
    freshness_window_days: dict[str, int] = field(default_factory=lambda: {
        "stable": 90, "semi_stable": 30, "dynamic": 7,
    })
    # --- Backend (Capa 4) ---
    max_concurrent_notebooks: int = 2
    timeouts: dict[str, int] = field(default_factory=lambda: {
        "create_notebook": 30, "add_source": 60, "research": 120,
        "generate_report": 180, "download": 60, "delete": 30,
    })
    # --- Orquestador (Capa 9) ---
    max_retries: int = 3
    backoff_seconds: list[int] = field(default_factory=lambda: [2, 4, 8])
    pacing_between_concepts_s: float = 1.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_cooldown_s: int = 60
```

#### Método de calibración

```python
def calibrate(pilot_report: PilotReport, findings: list[Finding]) -> CalibrationResult:
    adjustments: list[Adjustment] = []

    # 1. Si la trazabilidad (citas) quedo por debajo del umbral pero el contenido es bueno
    #    -> bajar trace_threshold o mejorar el prompt (preferir mejorar el prompt)
    if pilot_report.evidence.validation_warnings.count("V_SEM_TRACES") > 0:
        if pilot_report.evidence.citations_count / max(1, pilot_report.evidence.claims_total) >= 0.5:
            adjustments.append(Adjustment("trace_threshold", 0.6, 0.5,
                reason="contenido bueno pero citas escasas; bajar umbral y mejorar prompt de citas"))
        else:
            adjustments.append(Adjustment("prompt", None, None,
                reason="mejorar prompt de sintesis para exigir citas [src-N] por afirmacion"))

    # 2. Si alguna seccion quedo corta (V_CONTENT_MIN_LENGTH warning)
    for sec, words in pilot_report.evidence.word_count_by_section.items():
        if words < PILOT_MIN_WORDS.get(sec, 30) * 1.2:
            adjustments.append(Adjustment(f"min_words.{sec}",
                PILOT_MIN_WORDS[sec], max(PILOT_MIN_WORDS[sec], words),
                reason=f"seccion {sec} quedo en {words} palabras; ajustar minimo a lo observado"))

    # 3. Si la cobertura de investigacion fue baja (low_coverage) pero el contenido es bueno
    #    -> bajar coverage_threshold o mejorar queries
    if pilot_report.evidence.research_low_coverage:
        if pilot_report.evidence.validation_score >= 0.9:
            adjustments.append(Adjustment("coverage_threshold", 0.7, 0.6,
                reason="baja cobertura pero buena validacion; relajar umbral"))
        else:
            adjustments.append(Adjustment("research.queries", None, None,
                reason="mejorar generacion de queries (grupo a/b/c) para subir cobertura"))

    # 4. Si hubo timeouts o rate limits -> subir timeouts / bajar concurrencia / subir pacing
    if pilot_report.run_result.had_backend_timeouts:
        adjustments.append(Adjustment("timeouts.research", 120, 180,
            reason="timeouts observados en research; subir timeout"))
        adjustments.append(Adjustment("pacing_between_concepts_s", 1.0, 2.0,
            reason="rate limit observado; espaciar conceptos"))

    # 5. Si el tiempo total del piloto fue alto -> ajustar max_sources / max_questions
    if pilot_report.evidence.total_duration_ms > 300_000:   # > 5 min por concepto
        adjustments.append(Adjustment("max_sources", 12, 8,
            reason="piloto lento; reducir fuentes para acelerar (trade-off cobertura)"))
        adjustments.append(Adjustment("max_questions_per_concept", 12, 9,
            reason="reducir preguntas por concepto"))

    # 6. Si strict_mode bloqueo por warnings que son aceptables -> desactivar strict en produccion
    if pilot_report.run_result.blocked_reason and "warnings" in pilot_report.run_result.blocked_reason:
        adjustments.append(Adjustment("strict_mode (produccion)", True, False,
            reason="warnings aceptables en piloto; en produccion no bloquear por warnings"))

    return CalibrationResult(adjustments=adjustments, calibrated_config=apply(adjustments, base_config))
```

#### Versionado de config (piloto vs producción)

```
config/
├── config.yaml              # produccion (valores calibrados tras el piloto)
├── config.pilot.yaml        # piloto (strict, keep_history, dry_run_first)
└── config.pilot.calibrated.yaml  # resultado de la calibracion (para comparar)
```

Reglas:

- La calibración produce un `config.pilot.calibrated.yaml` con los valores ajustados. El humano revisa el diff (`diff config.yaml config.pilot.calibrated.yaml`) y decide qué aplicar a `config.yaml`.
- NUNCA se aplica la calibración automáticamente a `config.yaml`: requiere revisión humana y commit en git (los prompts/config son código versionado).
- Cada ajuste lleva `reason` (por qué se cambió) y se persiste en `workdir/pilot/calibration.json` para auditoría.
- Si un parámetro se ajusta, se re-corre el piloto (`ai run frontend-01-internet-web --force --config config.pilot.calibrated.yaml`) para verificar que el ajuste no rompe nada (regresión).
- Iterar: calibrar → re-correr piloto → validar. Máximo 3 iteraciones antes de escalar (si no converge, escalar con los valores por defecto y seguir calibrando en el lote).

### 4) Criterios de aceptación para escalar

El piloto debe cumplir TODOS los criterios (gate de escalamiento) antes de pasar al frontend completo. Si alguno falla, NO se escala: se corrige y se re-corre el piloto.

```python
@dataclass
class ScalingAcceptanceCriteria:
    # --- Integridad (bloqueante) ---
    vault_integrity_100: bool          # outside hash identico, marcadores 1/1, frontmatter byte a byte
    zero_data_loss: bool               # ningun archivo del vault modificado fuera del bloque
    backup_restore_tested: bool        # se probo restaurar un backup y queda identico
    # --- Validacion automatica ---
    validation_strict_pass: bool       # is_valid=True con strict_mode=True en el piloto
    validation_score_min: float        # >= 0.85
    zero_error_checks: bool            # 0 checks de severidad error fallidos
    # --- Calidad de contenido (revision humana) ---
    manual_review_complete: bool       # checklist manual 100% True
    no_hallazgos_bloqueantes: bool    # sin hallazgos de severidad "bloqueante" en findings
    citations_verified: bool           # las citas [src-N] fueron verificadas por el humano
    # --- Pipeline / operacion ---
    idempotency_verified: bool        # re-correr el piloto (sin --force) NO re-procesa (salta por frescura)
    resume_verified: bool             # cortar a mitad y reanudar produce el mismo resultado
    dry_run_matches_real: bool       # el diff del dry-run coincide con la escritura real
    # --- Performance ---
    duration_per_concept_acceptable: bool  # tiempo por concepto dentro del presupuesto (ej. < 5 min)
    no_backend_timeouts: bool         # 0 timeouts en el piloto (o timeouts manejados sin fallo)
    # --- Configuracion ---
    calibration_applied: bool          # config calibrada y commiteada en git
    prompts_versioned: bool           # prompts usados versionados en git (hash trazable)

def evaluate_acceptance(pilot_report, manual_review, findings, integrity) -> ScalingDecision:
    criteria = ScalingAcceptanceCriteria(
        vault_integrity_100=integrity.all_ok,
        zero_data_loss=integrity.all_ok,
        backup_restore_tested=test_restore(pilot_report.concept_id),
        validation_strict_pass=pilot_report.run_result.status == "done",
        validation_score_min=pilot_report.evidence.validation_score >= 0.85,
        zero_error_checks=len(pilot_report.evidence.validation_errors) == 0,
        manual_review_complete=all(asdict(manual_review).values()),
        no_hallazgos_bloqueantes=not any(f.severity == "bloqueante" for f in findings),
        citations_verified=manual_review.citations_accurate,
        idempotency_verified=verify_idempotency(pilot_report.concept_id),
        resume_verified=verify_resume(pilot_report.concept_id),
        dry_run_matches_real=verify_dry_run_match(pilot_report),
        duration_per_concept_acceptable=pilot_report.evidence.total_duration_ms < 300_000,
        no_backend_timeouts=not pilot_report.run_result.had_backend_timeouts,
        calibration_applied=calibration_committed(),
        prompts_versioned=prompts_in_git(),
    )
    failed = [k for k, v in asdict(criteria).items() if v is False]
    decision = "GO" if not failed else "NO-GO"
    return ScalingDecision(decision=decision, failed_criteria=failed, criteria=criteria)
```

Verificaciones auxiliares del gate:

```python
def verify_idempotency(concept_id: str) -> bool:
    # re-correr sin --force: el runner debe saltar (status skipped) porque raw_research esta fresco
    result = run_concept(concept_id, force=False)
    return result.skipped is True and result.status in ("done", "skipped")

def verify_resume(concept_id: str) -> bool:
    # resetear a "researching" (sin borrar artefactos), cortar a mitad, reanudar -> mismo resultado final
    reset(concept_id, to="researching", artifacts=[])
    # simular corte: correr con --stop-after synthesizing, luego reanudar
    run_concept(concept_id, stop_after="synthesizing")
    final = run_concept(concept_id)   # reanuda desde validating
    return final.status == "done"

def verify_dry_run_match(pilot_report) -> bool:
    # el diff del dry-run debe coincidir byte a byte con la escritura real
    dry_inside = pilot_report.dry_result.proposed_inside
    real_inside = load_written_inside(pilot_report.concept_id)
    return normalize(dry_inside) == normalize(real_inside)

def test_restore(concept_id: str) -> bool:
    # forzar un fallo de verificacion (ej. corromper el interior) y verificar que el backup se restaure
    # se hace en un concepto de prueba o en dry-run; NUNCA en el concepto piloto real sin backup
    ...
```

Reglas del gate de escalamiento:

- El gate es binario: TODOS los criterios deben ser `True`. Un solo `False` → `NO-GO`.
- Los criterios de integridad (`vault_integrity_100`, `zero_data_loss`) son bloqueantes absolutos: si fallan, NO se escala bajo ninguna circunstancia, y se investiga la causa (bug en el writer).
- Los criterios de validación (`validation_strict_pass`, `zero_error_checks`) son bloqueantes: un piloto que no pasa validación estricta no se escala.
- Los criterios de calidad de contenido (`manual_review_complete`, `no_hallazgos_bloqueantes`) son bloqueantes: el humano debe revisar y aprobar.
- Los criterios de pipeline (`idempotency_verified`, `resume_verified`, `dry_run_matches_real`) son bloqueantes: si la idempotencia o el resume fallan, el sistema no es confiable para 255 conceptos.
- Los criterios de performance (`duration_per_concept_acceptable`) son NO bloqueantes por sí solos: si un concepto tarda más de lo esperado, se escala igual pero con pacing ajustado y monitoreo. Se registra como riesgo.
- Los criterios de configuración (`calibration_applied`, `prompts_versioned`) son bloqueantes: no se escala con config sin versionar (no se puede reproducir ni auditar).
- La decisión `GO`/`NO-GO` se persiste en `workdir/pilot/scaling_decision.json` con la lista de criterios fallidos y sus razones.

### 5) Plan de escalamiento (frontend completo, luego otras áreas)

El escalamiento se hace en fases incrementales, no de golpe sobre los 255 conceptos. Cada fase tiene su propio mini-gate antes de pasar a la siguiente.

#### Fase A — Frontend completo (conceptos frontend-01 ... frontend-NN)

```python
@dataclass
class ScalingPhase:
    name: str
    scope: list[str]            # concept_ids o filtro (area, rango)
    order: str = "numeric"
    pacing_s: float = 1.0
    backend: str = "notebooklm"
    strict: bool = False        # warnings no bloquean en produccion
    dry_run_first: bool = False
    gate: ScalingGate

# Fase A: frontend completo
phase_a = ScalingPhase(
    name="Fase A — Frontend completo",
    scope=["frontend-*"],        # todos los conceptos del area frontend
    order="numeric",
    pacing_s=2.0,               # calibrado en el piloto
    strict=False,
    gate=ScalingGate(
        min_success_rate=0.90,   # >= 90% done
        max_blocked_rate=0.05,   # <= 5% blocked
        max_failed_rate=0.10,    # <= 10% failed (reintentables)
        max_avg_duration_ms=300_000,
        required_manual_review_sample=0.10,  # revisar manualmente el 10% de los done
    ),
)
```

Ejecución Fase A:

```bash
# 1. scan para confirmar la cola
ai scan --area frontend

# 2. dry-run sobre los primeros 3 conceptos (smoke test post-piloto)
ai run-batch --area frontend --concept-order numeric --from frontend-01 --hasta frontend-03 --dry-run --force

# 3. run real del frontend completo
ai run-batch --area frontend --concept-order numeric --pacing 2.0

# 4. monitoreo
ai status --area frontend --failed --blocked --low

# 5. revision de bloqueados/fallidos
ai review --area frontend

# 6. reporte final
ai report --last --md --out workdir/reports/frontend_phase.md
```

Mini-gate Fase A (antes de pasar a Fase B):

- `success_rate >= 0.90` (done / total del área).
- `blocked_rate <= 0.05`.
- `failed_rate <= 0.10` (los failed son reintentables; se reintenta con `--retry-failed`).
- Revisión manual del 10% de los conceptos `done` (muestra aleatoria) con el checklist manual (sección 2). Si la muestra tiene hallazgos bloqueantes → NO-GO.
- Tiempo promedio por concepto dentro del presupuesto.
- 0 problemas de integridad del vault (outside hash en todos los `done`).
- Notebooks huérfanos <= 5% (limpieza best-effort; los restantes se limpian manualmente).

#### Fase B — Otras áreas (backend, data, infra)

```python
phase_b = ScalingPhase(
    name="Fase B — Backend",
    scope=["backend-*"],
    # ... mismos params que phase_a, con ajustes por area:
    # - prompt_context cambia (backend vs frontend)
    # - area_domains cambian (docs.python.org, nodejs.org, etc.)
    # - min_words puede variar por area (config por area)
)

phase_c = ScalingPhase(name="Fase C — Data",   scope=["data-*"])
phase_d = ScalingPhase(name="Fase D — Infra",  scope=["infra-*"])
```

Orden de áreas y justificación:

1. **Frontend** (Fase A): ya validado en el piloto; misma área, mismos prompts. Menor riesgo.
2. **Backend** (Fase B): área cercana (APIs, servidores); prompts similares. Se reutiliza la calibración del frontend con ajustes menores (area_domains, ejemplos en Python/Node).
3. **Data** (Fase C): área más distinta (pipelines, ML, SQL); requiere revisar los prompts de contexto `data` y posiblemente ajustar `min_words` (ejemplos con SQL/Python).
4. **Infra** (Fase D): área con más contenido de comandos/config (Docker, K8s); revisar prompts `infra` y code fences (bash/yaml).

Entre fases:

- Al terminar cada fase, generar el reporte (`ai report --last`) y revisar bloqueados/fallidos/baja cobertura.
- Reintentar los `failed` con `--retry-failed` antes de pasar a la siguiente fase.
- Los `blocked` (validación por warnings/umbral) se revisan manualmente; si son sistemáticos (mismo check fallando en muchos), se recalibra el umbral o el prompt y se re-corre la fase.
- Si una fase tiene `success_rate < 0.80` → STOP: no pasar a la siguiente área. Investigar la causa (prompts, fuentes, timeouts) y re-calibrar.

#### Fase E — Lote completo (255 conceptos) (opcional, tras Fases A-D)

```python
phase_e = ScalingPhase(
    name="Fase E — Lote completo (todas las areas)",
    scope=None,                  # toda la cola (sin filtro de area)
    order="numeric",
    pacing_s=2.0,
    strict=False,
    gate=ScalingGate(
        min_success_rate=0.95,   # gate mas estricto para el lote completo
        max_blocked_rate=0.02,
        max_failed_rate=0.05,
    ),
)
```

Ejecución:

```bash
ai run-batch --concept-order numeric --pacing 2.0
```

- Se ejecuta preferentemente en horario de baja carga (NotebookLM tiene límites de cuenta).
- Monitoreo en tiempo real con `ai status --watch` (refresca cada 30s).
- Si el lote se interrumpe (Ctrl+C), el runner persiste estado y genera reporte parcial. Se reanuda con `ai run-batch --retry-failed` (los `done` se saltan).

#### Cronograma sugerido

| Semana | Actividad |
|---|---|
| 1 | Implementar Capas 1-10 (ya hecho). Preparar entorno de piloto. |
| 2 | Ejecutar piloto (dry-run + real) sobre `frontend-01`. Revisión manual. |
| 3 | Calibración (iterar hasta 3 veces). Gate de escalamiento. |
| 4 | Fase A: frontend completo. Revisión de muestra. |
| 5 | Fase B: backend. Recalibración si es necesario. |
| 6 | Fase C: data. |
| 7 | Fase D: infra. |
| 8 | Fase E: lote completo (si todas las fases pasaron sus gates). |
| 9+ | Revisión final, limpieza de notebooks huérfanos, reporte consolidado. |

Reglas del plan de escalamiento:

- NO se escala al lote completo sin pasar el gate de escalamiento del piloto (sección 4). Un piloto fallido invalida el escalamiento.
- Cada fase de área tiene su mini-gate. Si una fase falla, se detiene y se recalibra (no se salta a la siguiente área).
- El escalamiento es incremental y reversible: si una fase sale mal, los conceptos `done` ya escritos permanecen (son válidos), y los `failed`/`blocked` se reintentan. No se revierte el vault.
- El pacing se ajusta por fase según la calibración (default 2s entre conceptos; puede subir si hay rate limits).
- El monitoreo es continuo: `ai status` + reportes por fase. Los hallazgos sistemáticos (mismo check fallando en muchos conceptos) indican un problema de prompt/config, no de contenido individual → recalibrar y re-correr la fase afectada.
- Los notebooks huérfanos se limpian al final de cada fase (manual o con un script de limpieza que liste `orphan_notebooks` del reporte).
- La decisión de escalar a la siguiente fase se documenta (commit en git del `scaling_decision.json` o anotación en el reporte) para trazabilidad.

### Reglas de negocio (de la spec)

- El piloto se ejecuta sobre un único concepto (`frontend-01-internet-web`) con dry-run primero y run real después, siempre con `--strict` para detectar problemas de calibración.
- El piloto requiere revisión humana del contenido (checklist manual) además de la validación automática (Capa 8). No es suficiente `is_valid = True`.
- La integridad del vault se verifica byte a byte (outside hash, marcadores, frontmatter) antes y después del piloto. Cualquier diferencia es bloqueante.
- La calibración ajusta parámetros de validación, investigación, backend y orquestador a partir de los hallazgos del piloto. Cada ajuste lleva `reason` y se persiste para auditoría.
- La calibración NO se aplica automáticamente a `config.yaml`: requiere revisión humana y commit en git.
- El gate de escalamiento es binario: TODOS los criterios deben pasar. Un solo fallo → `NO-GO`.
- El escalamiento es incremental por área: frontend → backend → data → infra → lote completo. Cada fase tiene mini-gate; si falla, se detiene y recalibra.
- La idempotencia y el resume se verifican explícitamente en el piloto (re-correr sin `--force` salta; cortar y reanudar produce el mismo resultado).
- El dry-run debe coincidir byte a byte con la escritura real (verificación de que el writer es determinista).
- Los notebooks huérfanos se reportan y se limpian al final de cada fase.
- El piloto y la calibración son la última capa: no agregan lógica de negocio nueva, solo orquestan, miden y deciden si el sistema está listo para escalar.
