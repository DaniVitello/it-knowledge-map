# Explicacion del proyecto por capas v1 - pseudo codigo

> Documento hermano de `explicacion del proyecto por capas v1.md`. Contiene UNICAMENTE pseudo-codigo de alto nivel del proyecto (las 11 capas): que se hace, por que, como, cuando y donde. Sin codigo real, snippets, comandos de shell ni detalles de implementacion de bajo nivel. La estructura de capas y las decisiones de diseño se preservan.

---

## Orden de las capas del pseudo-codigo (con justificacion)

El orden sigue el Apendice A del diseño técnico y la prioridad de decisiones (integridad > correctitud > fuentes > contexto > coherencia > actualidad > pedagogia > robustez > automatizacion > velocidad/costo).

### Capa 1 — Modelo de datos (ConceptMeta)
Por que primero: todo lo demas depende de que es un "concepto". Sin definir los campos y sus reglas de derivacion, no se puede leer el vault, ni construir prompts, ni validar. Es el atomo del sistema.

### Capa 2 — Vault como fuente de verdad (vault.py)
Por que segundo: antes de investigar, hay que leer las notas sin romperlas. El vault es la unica fuente de verdad de los metadatos (titulo, area, key_ideas, connections). Tambien se definen los marcadores ai:start/end, el hash del bloque, y la escritura atomica. Sin esto, no se puede persistir nada de forma segura.

### Capa 3 — Pipeline de estados (state.py + ConceptState)
Por que tercero: una vez que se sabe leer notas y que es un concepto, se necesita la maquina de estados (pending → researching → ... → completed) y la persistencia por concepto. Es lo que hace al sistema recuperable e idempotente. Sin estados, no se sabe si reanudar o saltar.

### Capa 4 — Backend (interfaz + fake + notebooklm)
Por que cuarto: recien despues de tener estados y persistencia, se abstrae el acceso a NotebookLM. El backend fake permite probar todo sin red. El adaptador real (async, API directa) evita el bug de encoding. La interfaz ResearchBackend permite cambiar de proveedor sin tocar el resto.

### Capa 5 — Escritura segura (writer.py)
Por que quinto: antes de generar contenido real, hay que garantizar que la escritura no rompa la nota. El writer implementa: backup, hash del afuera antes/despues, escritura atomica, verificacion, proteccion de ediciones manuales, modo dry-run. Se prueba con el backend fake antes de tocar datos reales.

### Capa 6 — Investigacion (research.py + strategy.py)
Por que sexto: ahora que hay backend, estados y writer, se implementa la busqueda y evaluacion de fuentes. Incluye: construccion del plan (preguntas por dimension), estrategia de actualidad por volatilidad, seeds + dominios preferidos + busqueda abierta, ciclo de cobertura, manejo de brechas (gap/sin verificar). Persiste sources.json y raw_research.json.

### Capa 7 — Sintesis (synthesis.py + prompts)
Por que septimo: con las fuentes persistidas, se genera el contenido pedagogico. 3 preguntas a NotebookLM (grupos a/b/c), trazabilidad por afirmacion (claim → source_id), normalizacion a Markdown, separacion fundamento estable / practica moderna. Los prompts son editables y versionados.

### Capa 8 — Validacion (validation.py)
Por que octavo: antes de escribir, se valida la sintesis. Dos capas: determinista (formato, enlaces, hashes) y semantica (contenido, contexto, relaciones, profundidad, pedagogia). 17 chequeos con severidad error/warn. Falla cerrado: ante la duda, no escribe.

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

## Capa 1 — Modelo de datos (ConceptMeta)

### Objetivo
Definir que es un "concepto" en el vault: el atomo sobre el que se construye todo el pipeline. Fija los campos, sus tipos y las reglas de derivacion desde el archivo .md. Es la unica fuente de verdad del "que" se procesa.

### Que es un concepto en el vault
Un concepto es una nota Markdown del vault de Obsidian que cumple TODAS estas condiciones:
- Es un archivo .md dentro del glob configurado.
- Tiene un bloque autorizado ai:start ... ai:end (o se registra como "sin bloque" para reporte).
- Representa una unidad de conocimiento atomica: un tema con titulo, area, ideas clave y relaciones.

Un concepto tiene dos "vidas": los metadatos (fuera del bloque, editados a mano por el autor) y el contenido generado (dentro del bloque, gestionado por el pipeline). El pipeline solo toca el interior. Los metadatos son la unica fuente de verdad del "que investigar": titulo, area, key_ideas, connections. El pipeline nunca los modifica. La identidad (concept_id) se deriva del path: mientras el path sea estable, el id es estable. Si se mueve el archivo, se considera un concepto nuevo (y el viejo queda huerfano en estado.json).

### ConceptMeta — definicion del atomo
Campos (conceptualmente):
- Identidad: id (slug del path), path (ruta absoluta), slug (alias de id).
- Metadatos (solo lectura, fuera del bloque): title, area, numero, aliases, tags.
- Contenido estructurado (fuera del bloque): key_ideas (bullets de "Que abarca"), connections (wikilinks de "Relacionados").
- Integridad/sincronizacion: has_ai_block, outside_hash, inside_hash, mtime_at_read, outside_hash_at_read, newline, has_frontmatter, has_bom.
- Derivados (calculados): concept_dir (workdir/concepts/<id>/).

Reglas: ConceptMeta es un DTO con identidad inmutable (id y path no cambian). Los campos de metadatos se leen del vault y NUNCA se escriben de vuelta. outside_hash e inside_hash se calculan en la lectura (Capa 2) y se usan para integridad y deteccion de ediciones manuales. concept_dir apunta al directorio de artefactos del pipeline.

### Reglas de derivacion de cada campo
Identidad:
- id = slug del path relativo al vault root, normalizado (minúsculas, espacios→-, se mantienen los números). Debe ser único en el vault; colision → error fatal del scan.
- path = ruta absoluta resuelta.
- slug = alias de id.

Metadatos (frontmatter YAML, si existe): title (frontmatter → primer H1 → nombre de archivo). area (frontmatter → primera carpeta del path → default_area). numero (frontmatter → número leading del nombre de archivo → None). aliases (frontmatter → []). tags (frontmatter → [], normalizados a minúsculas sin #).

Contenido estructurado (cuerpo, fuera del bloque): key_ideas = bullets bajo "Que abarca" (o alias configurado). connections = wikilinks bajo "Relacionados" (o todos los wikilinks excepto indices y la propia nota si no existe el heading).

Bloque ai: has_ai_block = True si existe exactamente un ai:start y un ai:end en ese orden. outside_hash = sha256 del afuera si hay bloque, si no None. inside_hash = sha256 del interior si hay bloque, si no None.

Sincronizacion: mtime_at_read = mtime del archivo al leer. outside_hash_at_read = copia del outside_hash al leer. newline = CRLF o LF detectado. has_frontmatter = True si empieza con ---. has_bom = True si los primeros bytes son UTF-8 BOM (se preserva).

Reglas de precedencia (cuando un campo se puede derivar de varias fuentes): 1) Frontmatter explícito > extracción del cuerpo > inferencia del path > default. 2) Si una fuente da vacío/None, se intenta la siguiente. 3) Si todas fallan, se usa el default documentado y se registra warning (nunca se inventa un valor silenciosamente).

Reglas de unicidad al scan: id único (colision → error fatal). path único por construcción. title y area no vacíos (fallback garantiza). key_ideas puede ser [] (warning, no bloquea).

### Content hash: que es y para que sirve
Un content hash es el resumen criptografico (SHA-256) del contenido de un archivo o de una seccion de él. Se usan dos:
- outside_hash = SHA-256 de todo el archivo EXCEPTO el interior del bloque ai (los marcadores se incluyen en el "afuera").
- inside_hash = SHA-256 del interior del bloque ai (el contenido generado por el pipeline).

Para que sirve (usos en el sistema):
1. Integridad del "afuera" (Capa 5): antes de escribir se calcula outside_hash_before; después se recalcula. Si difieren → el writer toco algo que no debía → restaurar backup y marcar failed. Garantiza que el pipeline solo modifica el interior del bloque.
2. Deteccion de ediciones manuales (Capa 5/8): comparando inside_hash actual del archivo con el inside_hash persistido en estado.json (tras la última escritura). Si difieren → el autor edito el bloque a mano → se marca para revision (no se sobrescribe silenciosamente).
3. Deteccion de edición concurrente (Capa 5): comparando outside_hash_at_read (snapshot de la lectura) con el hash actual del archivo en el momento de la escritura. Si difiere → Obsidian (o el autor) modifico el archivo entre lectura y escritura → ConcurrentEditError, se reintenta o se marca failed.
4. Idempotencia (Capa 3): si al re-procesar un concepto el inside_hash actual coincide con el hash de la sintesis nueva, no se reescribe (evita writes innecesarios y preserva mtime).
5. Trazabilidad/auditoria: los hashes se persisten en estado.json (done → content_hash_outside, content_hash_inside), permitiendo verificar post-mortem que el archivo en disco coincide con lo que el pipeline cree haber escrito.
6. Verificacion byte a byte (Capa 5): además del hash, se compara el "afuera" byte a byte (no solo hash) para descartar colisiones de hash (defensa en profundidad).

Propiedades: SHA-256 es determinista. Se calcula sobre el texto completo de la seccion (incluyendo newlines), no sobre una version normalizada. El hash NO es un secreto ni una firma. No se usa para comparar contenido entre conceptos; es por-concepto y por-seccion. Un hash None (concepto sin bloque ai) significa "no aplica"; no se compara.

Reglas de uso: siempre se hashea el texto completo de la seccion (incluyendo newlines). El hash se persiste siempre junto con writer_version y written_at para poder invalidar caches si cambia el formato de escritura.

### Por que esta capa va primero
Todo lo demás depende de saber que es un "concepto". Es el "atomo" del sistema: el modelo de datos es el contrato que todas las capas consumen. Cambiar un campo aca impacta a todas las demás capas, por eso se fija primero. Evita que cada capa invente su propia noción de "concepto" (drift entre módulos). Las reglas de derivacion determinan que es editable por el autor (metadatos) vs. que es generado (interior del bloque), base de la política de "mínimo privilegio" del writer (Capa 5). El content hash, definido aca, es la primitiva de integridad que Capa 5 y Capa 8 usan; sin él no hay verificación posible.

Regla de dependencia: ninguna capa puede redefinir ConceptMeta. Si se necesita un campo nuevo, se agrega aca y se propaga. Esto mantiene una única fuente de verdad del modelo.

---

## Capa 2 — El vault como fuente de verdad

### Objetivo
Leer y escribir notas del vault sin romper nada fuera del bloque autorizado, verificando integridad antes y después.

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

### Reglas de negocio
- Solo se modifica el interior del bloque ai:start/ai:end. Todo lo demás se verifica byte a byte.
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

## Capa 3 — Pipeline de estados (state machine)

### Objetivo
Maquina de estados por concepto (pending → researching → ... → completed) y persistencia por concepto. Hace al sistema recuperable e idempotente.

### Estados del pipeline por concepto
- PENDING: en cola, sin procesar.
- RESEARCHING: buscando/evaluando fuentes.
- SYNTHESIZING: generando contenido pedagogico.
- VALIDATING: validando la sintesis.
- WRITING: escribiendo en el vault.
- DONE: terminal exitoso.
- FAILED: terminal por error (reintentable).
- BLOCKED: terminal por bloqueo humano.

### Transiciones validas y reglas
Transiciones lineales: no se salta ninguna fase (pending → ... → done). done es estado terminal: nunca se reejecuta. failed y blocked son terminales operativos: requieren reintento explicito o accion humana. Un reintento vuelve al estado que fallo (no reinicia desde pending), conservando el checkpoint previo.

### Idempotencia y resume desde checkpoint
Al arrancar se lee estado.json por concepto (status + ultimo checkpoint). Si el status es terminal (done/failed/blocked) → no se reejecuta. Si es no-terminal → se reanuda desde el ultimo checkpoint persistido (no desde cero).

Pseudo-flujo:
- cargar estado del concepto
- si status es terminal → devolver estado (no reejecutar)
- fase = checkpoint o primera fase
- mientras haya fase:
  - ejecutar fase
  - persistir checkpoint y status
  - avanzar a la siguiente fase
  - si falla → manejar fallo y cortar

### Reintentos max 3 por estado con backoff
Max 3 intentos por fase. Backoff exponencial: intento 1 → 2s, intento 2 → 4s, intento 3 → 8s (configurable). Al agotar los reintentos, la fase se marca failed y se persiste el error.

### Estados terminales y que se persiste
- done → status, content_hash_outside, content_hash_inside, writer_version, validation_result, written_at.
- failed → status, error, fase_fallida, timestamp.
- blocked → status, blocker, detalle, quien debe resolverlo.

### Orquestacion del bucle sobre los conceptos (cola, orden, serial con backoff)
- Cola FIFO de conceptos en pending (resultado del scan).
- Orden: scan order / orden numerico del concepto.
- Procesamiento serial por concepto: se transiciona y persiste el estado (checkpoint) ANTES de avanzar a la fase siguiente.
- Un concepto que falla no detiene el lote; se registra y se sigue con el siguiente.

### Relacion con checkpoint (estado.json)
estado.json agrupa por concept_id: status + checkpoint + datos de la fase. Se escribe de forma atomica en cada transicion validada. El runner consulta estado.json para decidir reejecutar o reanudar. Es la unica fuente de verdad del progreso: sin el, no hay recuperacion ni idempotencia.

---

## Capa 4 — Backend: interfaz + fake + notebooklm

### Objetivo
Abstraer el acceso a NotebookLM detras de una interfaz unica (ResearchBackend) para que el resto del pipeline (investigacion, sintesis) no dependa de un proveedor concreto. Permitir probar todo el flujo sin red mediante un backend fake, y usar el adaptador real (API Python async de notebooklm-py) en produccion, evitando el bug de encoding del CLI.

### Interfaz del backend (ResearchBackend)
Contrato comun que implementan todos los backends. El pipeline solo habla con esta interfaz. Metodos (todos async):
- create_notebook(concept) → notebook_id
- delete(notebook_id) → idempotente
- add_sources(notebook_id, sources) → lista de source_ids
- research(notebook_id, plan) → ResearchResult (respuestas con trazabilidad afirmacion → source_id)
- generate_report(notebook_id, spec) → report_id
- download(notebook_id, report_id, dest) → path

Estructuras de datos compartidas: Source, ResearchQuestion, ResearchPlan, Claim, ResearchAnswer, ResearchResult, ReportSpec.

Reglas del contrato: todos los metodos son async (incluso el fake). notebook_id es un string opaco. research debe devolver respuestas agrupadas por grupo (a/b/c) y con claims trazables a source_id. Ningun metodo bloquea el event loop. Los metodos son idempotentes cuando tiene sentido (delete no falla si el notebook ya no existe).

### Backend fake (para tests sin red)
Implementacion en memoria que simula respuestas deterministas, sin tocar la red. Usado por tests, dry-run de desarrollo y CI.
Caracteristicas: determinista (mismas entradas → mismas salidas). Fixtures opcionales por concepto/qid. Registra llamadas (calls) para assertions en tests. Simula latencia configurable. No requiere credenciales ni red.
Usos: tests unitarios de investigacion/sintesis/writer; --backend fake en CLI para desarrollo sin NotebookLM; modo dry-run de pipelines largos (smoke test).

### Backend notebooklm (wrapper async de notebooklm-py)
Adaptador real que envuelve la API Python de notebooklm-py. Todo es async (la libreria expone metodos async o se delega a executor si es sync). Evita el bug de encoding del CLI al usar la API directa (sin subprocess).
Notas de implementacion: autenticacion desde cookies/session exportadas (no password en codigo), validada al arrancar (fail-fast si falta). Cliente creado una vez por proceso (connection pooling). Semaforo limita notebooks concurrentes (limites de cuenta NotebookLM). Timeouts por operacion. Escritura de download en bytes para evitar problemas de encoding. parse_claims compartido con el fake.

### Como se elige que backend usar (config)
Configuracion en config.yaml (o env vars / CLI flags), leida al arrancar. Factory create_backend(config) devuelve FakeBackend o NotebookLMBackend segun provider.
Reglas: validacion fail-fast al arrancar (si se pide notebooklm y faltan credenciales → error claro antes de procesar conceptos). Override por CLI (--backend fake|notebooklm) y por env var, en ese orden de precedencia: CLI > env > config. El backend se instancia una vez por corrida y se inyecta en el orquestador (no se crea por concepto). Cambiar de backend no requiere tocar el resto del pipeline (solo config).

### Manejo de errores y timeouts
Jerarquia de excepciones: BackendError (base), BackendTimeout, BackendAuthError, BackendNetworkError, BackendNotFoundError, BackendRateLimitError.
Estrategia: timeouts por operacion aplicados con wait_for. Reintentos en operaciones idempotentes (research, download) hasta MAX_RETRIES con backoff exponencial. delete no reintenta (idempotente). Mapeo a estados del pipeline: BackendTimeout/Network/RateLimit → failed reintentable; BackendAuthError → blocked (requiere accion humana); BackendNotFoundError → failed con detalle. Limpieza best-effort de notebooks huerfanos ante fallo. Circuit breaker simple: si N fallos consecutivos de red → pausar el lote y marcar blocked. Logging estructurado: cada llamada al backend se registra (metodo, target, duracion, resultado/error) en JSON Lines. No se exponen secretos en logs.

---

## Capa 5 — Escritura segura (writer.py)

### Objetivo
Garantizar que la escritura del contenido generado no rompa la nota del vault: solo se modifica el interior del bloque autorizado (ai:start/ai:end), todo lo demás se verifica byte a byte. Implementa backup, hash del afuera antes/despues, escritura atomica, verificacion, proteccion de ediciones manuales, deteccion de concurrencia y modo dry-run.

### Escritura atomica con backup y restore
Flujo de escritura de un concepto:
1. Leer la nota completa en bytes y decodificar.
2. Calcular outside_hash_before (hash del afuera ANTES).
3. Validar marcadores (exactamente uno de cada, en orden). Si faltan/duplicados/orden incorrecto → error.
4. Detectar edicion concurrente (mtime/hash entre lectura y ahora). Si detecta → ConcurrentEditError.
5. Backup de la nota en workdir/backups/<concept_id>/ con timestamp compacto.
6. Construir nuevo interior (solo el contenido sintetizado y validado, normalizado a Markdown).
7. Dry-run: mostrar diff y salir sin escribir.
8. Escritura atomica: archivo temporal en el MISMO filesystem que el vault + renombre atomico (os.replace). Nunca se escribe directo sobre la nota.
9. Verificar releyendo desde disco: outside_hash_after == outside_hash_before, interior coincide con la sintesis validada, frontmatter/titulo/navegacion/wikilinks siguen presentes, marcadores siguen siendo 1/1.
10. Si alguna verificacion falla → restaurar backup byte a byte y marcar failed.
11. Si todo OK → estado written.

Reglas: backup ANTES de escribir. Escritura atomica con archivo temporal en el mismo filesystem + renombre atomico. Si falla cualquier verificacion → restaurar backup byte a byte y marcar failed. shutil.copy2 preserva mtime. El directorio temporal debe estar en el mismo filesystem que el vault. El writer es la unica pieza que toca el vault; investigacion/sintesis/validacion solo leen.

### Marcadores ai:start/ai:end y reemplazo del bloque
Marcadores exactos: <!-- ai:start --> y <!-- ai:end -->. Exactamente uno de cada, en ese orden. Si faltan o hay mas de uno → error (no se insertan automaticamente). El reemplazo toca UNICAMENTE las líneas entre los marcadores. Las líneas de los marcadores se preservan verbatim (mismo texto, mismo newline). El interior nuevo se inserta con el mismo estilo de newline del archivo. Si el interior nuevo está vacío, se deja una línea vacía entre los marcadores (no se colapsan). No se normaliza el contenido fuera del bloque.

### Verificacion de hash del contenido fuera del bloque (integridad)
Hash SHA-256 del "afuera" calculado ANTES y DESPUES. Si difiere → restaurar backup. Verificacion adicional byte a byte del afuera (no solo hash). La verificacion se hace RELEIENDO el archivo desde disco (no confiar en el buffer en memoria). Se verifica también que el interior escrito coincida con la sintesis validada.

### Frontmatter YAML preservado
El frontmatter YAML (entre ---) se preserva byte a byte. Si difiere → error. Comparacion semantica (dict) como red de seguridad, pero la verificacion principal es byte a byte del bloque ---...---. Si el archivo no tiene frontmatter, no se agrega uno. Campos como title, area, numero, aliases, tags nunca se tocan. El writer NUNCA reescribe el frontmatter; solo lo verifica.

### Normalizacion de newlines
Se detecta el fin de linea del archivo original (CRLF o LF) y se respeta. Toda escritura normaliza el interior nuevo al estilo detectado. El afuera (no tocado) conserva sus newlines originales porque no se reescribe. Codificacion siempre UTF-8 (sin BOM). Si el archivo original tenía BOM, se preserva el BOM en el afuera. No se normalizan espacios finales ni se agregan trailing newlines fuera del bloque.

### Que se escribe y que no
Se escribe UNICAMENTE: interior del bloque ai:start/ai:end (contenido sintetizado y validado, Markdown).
NO se escribe: frontmatter YAML, titulo H1 y headings, seccion "Que abarca" (key_ideas manuales), seccion "Relacionados" (wikilinks manuales), navegacion/indices/links fuera del bloque, archivos de estado (estado.json → state.py), backups, archivos de log (runner.py).

Principio de mínimo privilegio: el writer solo tiene permiso de modificar el interior del bloque. Todo lo demás es read-only para el writer; se verifica pero no se toca. Si faltan marcadores, no se insertan automáticamente (salvo config explicita). El writer no crea notas nuevas; solo modifica existentes con bloque. No borra archivos ni hace operaciones de git. No escribe en estado.json ni en logs.

### Integracion con el estado (Capa 3) y validacion (Capa 8)
Flujo writing_phase: cargar concepto → writer.write_concept → si dry_run, loguear diff y salir sin cambiar estado → si OK, marcar estado DONE con checkpoint "writing" y persistir write_result (backup_path, outside_hash, inside_hash, written_at, writer_version). Si falla (MissingMarkers, DuplicateMarkers, MarkerOrder, ConcurrentEdit, OutsideIntegrity, FrontmatterChanged, InsideMismatch, MarkerCount, WriteFailed) → marcar failed en fase "writing" (el backup ya fue restaurado dentro del writer) y propagar.

### Excepciones del writer
WriterError (base), MissingMarkersError, DuplicateMarkersError, MarkerOrderError, ConcurrentEditError, OutsideIntegrityError, OutsideByteMismatchError, FrontmatterChangedError, FrontmatterSemanticMismatchError, InsideMismatchError, MarkerCountError, WriteFailedError.

---

## Capa 6 — Investigacion (research.py + strategy.py)

### Objetivo
Construir el plan de investigación para un concepto, ejecutarlo contra el backend (deep research), seleccionar y deduplicar fuentes, y persistir tanto las fuentes (sources.json) como el resultado crudo (raw_research.json). Esta capa NO escribe en el vault: solo lee el concepto y persiste artefactos en workdir/concepts/<concept_id>/.

### Contexto de investigacion (ResearchContext)
Antes de generar queries, se arma un contexto a partir del ConceptMeta y del estado del concepto. Es la "materia prima" que alimenta tanto el generador de queries como la estrategia de fuentes.
Campos: concept_id, title, area, key_ideas, connections, volatility (STABLE | SEMI_STABLE | DYNAMIC, derivada del area + tags con override en config), last_researched_at (para decidir re-investigar), manual_notes (contenido manual fuera del bloque), extra_hints (hints del usuario via CLI --hint).
Reglas: volatility se deriva del area + tags, con override en config. Si last_researched_at está dentro de la ventana de frescura (freshness_window_days[volatility]) → se puede saltar la investigación (idempotencia/cache), salvo --force. manual_notes se incluye en el prompt como "contexto previo del autor".

### Generacion de queries de investigacion según contexto del concepto
El generador produce un ResearchPlan (lista de ResearchQuestion con qid y group a/b/c) a partir del contexto. Las preguntas se agrupan por dimension pedagogica:
- a) fundamento estable (conceptos, definiciones, historia, invariantes)
- b) practica moderna (estado del arte, versiones, herramientas, pitfalls)
- c) relaciones y casos de uso (relaciones, casos de uso, comparaciones, anti-patrones)
Cada grupo tiene entre 1 y N preguntas (configurable, default 3 por grupo = 9 en total). Ademas se generan preguntas derivadas de connections y key_ideas (auto), deduplicadas.

Reglas: las templates de preguntas viven en archivos editables (prompts/research_group_a.md) y se pueden sobrescribir por area. dedup_questions evita preguntas repetidas (normalizacion de texto). El número total de preguntas se limita por max_questions_per_concept (config, default 12); si se excede, se priorizan a > b > c > derived y se truncan. Cada pregunta debe ser autocontenida (incluye el nombre del concepto). Las preguntas NO piden formato de salida; el formato lo impone la sintesis (Capa 7).

### Estrategia de fuentes (strategy.py)
La estrategia define donde buscar: seeds (URLs fijas), dominios preferidos y dominios por area. Se combina con la volatilidad para definir la ventana de frescura.
Campos de SourceStrategy: seed_urls (siempre incluidas), preferred_domains (prioridad alta), blocked_domains (excluir), area_domains (dominios sugeridos por area), max_sources (tope de fuentes a subir al backend), min_sources (minimo para considerar cobertura suficiente), freshness_window_days por volatilidad.

Reglas: seed_urls se incluyen SIEMPRE. preferred_domains ordenan/priorizan; no excluyen otras fuentes. blocked_domains se filtran antes de subir al backend. La estrategia es por concepto (se resuelve con el area del concepto) pero se puede sobrescribir por concepto (concepts/<id>.yaml). Dominios por area se cargan de config; si un area no está, se usa la lista global. max_sources limita cuántas fuentes se suben (costo/tiempo). min_sources es el piso para considerar cobertura suficiente.

### Deep research via backend
La fase de investigación usa el backend (Capa 4) para ejecutar el plan. El ciclo incluye: crear notebook, subir fuentes, ejecutar las preguntas por grupo, evaluar cobertura, y si hay brechas (gap), hacer una segunda pasada con preguntas refinadas.

Flujo research_phase:
1. Cargar backend singleton, estado, plan (QueryGenerator), estrategia (StrategyResolver), fuentes (SourceSelector: seeds + candidatas).
2. Crear notebook (si no existe, persistir notebook_id en phase_data).
3. Subir fuentes (idempotente: si ya existen source_ids, saltar; persistir).
4. Ejecutar preguntas (grupo a, b, c) — reanudable por pregunta (saltar las ya respondidas; persistir answers + coverage tras cada pregunta).
5. Ciclo de cobertura: si coverage < threshold y no se hizo gap_pass → detectar gaps (preguntas sin respuesta o respuesta corta) → re-preguntar reformuladas (tope 3) → persistir.
6. Persistir artefactos: sources.json y raw_research.json.
7. Limpiar notebook (best-effort) si config.cleanup_notebooks.

Reglas: reanudable por pregunta. El notebook se crea una vez por concepto y se persiste su id. Cobertura objetivo: coverage_threshold (config, default 0.7). Si no se alcanza tras la pasada de gaps, se persiste igual pero se marca low_coverage: true en raw_research.json (la sintesis y validacion lo tendrán en cuenta). Limpieza de notebooks best-effort. open_search es pluggable: en v1 puede ser una lista estatica por concepto o un buscador externo. El backend (NotebookLM) NO busca en la web por su cuenta; las URLs se le entregan como fuentes.

### Seleccion y deduplicacion de fuentes
Antes de subir al backend, las fuentes candidatas se deduplican y rankean.
- Dedup por URL normalizada (sin tracking params, sin trailing slash) y por (host, path). Fuentes de texto pegado (kind="text") se dedupan por titulo normalizado.
- Rankeo: seeds y preferred_domains primero (mayor peso), luego el resto; orden estable (no aleatorio) para reproducibilidad.
- Cap en max_sources (default 12). Si hay menos de min_sources tras dedup → se registra low_sources: true en raw_research.json (no falla, pero la validacion lo penaliza).
- blocked_domains se filtran antes de dedup (no se cuentan).
- Si una seed URL falla al subirse (timeout), se registra pero no detiene el resto (best-effort por fuente).

### Estructura del resultado de investigacion
Artefactos en workdir/concepts/<concept_id>/:
- sources.json: lista final de fuentes usadas (post dedup/cap), con strategy, counts.
- raw_research.json: plan + respuestas + cobertura + metadata (volatility, freshness_window_days, low_coverage, low_sources, gap_pass_done, gaps_detected, gaps_resolved, notebook_id, source_ids, duration_ms, backend_provider).

Reglas: sources.json y raw_research.json se escriben de forma atomica (temp + rename) en workdir. Nunca en el vault. answers se persisten con claims trazables a source_id; si un claim no tiene source_id, se marca unverified: true (la validacion lo penaliza). notebook_id se persiste mientras exista el notebook; si se limpio, queda null. low_coverage/low_sources son flags para la validacion y para el reporte final; no bloquean por si solos. Si ya existe raw_research.json válido y está dentro de la ventana de frescura → se salta la investigación (idempotencia), salvo --force o --re-research. Los artefactos se versionan por timestamp solo si keep_history: true; por defecto se sobrescriben (ultimo gana), pero se hace backup en workdir/backups/<concept_id>/ antes de sobrescribir.

### Integracion con el estado (Capa 3)
Al terminar OK: status → SYNTHESIZING, checkpoint "researching", phase_data.research_done = True, coverage, sources_path, raw_research_path.

Mapeo de errores: BackendAuthError → blocked (renovar credenciales). BackendTimeout/Network/RateLimit → failed reintentable (vuelve a researching). LowCoverageError (si bloqueante) → blocked. Errores de IO → failed reintentable.

### Excepciones de la capa
ResearchError (base), QueryGenerationError, StrategyError, InsufficientSourcesError, CoverageTooLowError, ResearchPersistError.

### Reglas de negocio
- La investigación NO escribe en el vault; solo persiste sources.json y raw_research.json en workdir.
- El plan de queries se deriva del contexto del concepto y es editable via templates versionados.
- Las fuentes se seleccionan con seeds + preferred_domains + dominios por area + busqueda abierta; se deduplican y capan por max_sources.
- Deep research se ejecuta via backend (Capa 4), con ciclo de cobertura y segunda pasada de gaps si no se alcanza el threshold.
- El resultado persistido incluye trazabilidad claim → source_id, cobertura, flags de baja cobertura/fuentes.
- Idempotencia: si raw_research.json esta fresco (dentro de la ventana por volatilidad), se salta la investigación salvo --force.
- Reanudable por pregunta: un corte a mitad no repite las preguntas ya respondidas.
- low_coverage/low_sources no bloquean por si solos; la validacion (Capa 8) decide si son error o warning.
- El writer (Capa 5) y la sintesis (Capa 7) consumen sources.json y raw_research.json; esta capa no toca el vault.

---

## Capa 7 — Sintesis (synthesis.py + prompts)

### Objetivo
A partir de las fuentes persistidas (sources.json + raw_research.json), generar el contenido pedagogico (study guide) que se va a insertar en el vault. Transforma la investigación cruda (respuestas con claims trazables) en un documento Markdown normalizado, con secciones requeridas, separacion entre fundamento estable y practica moderna, y cross-links a conceptos vecinos. Los prompts que guian la generacion son editables y versionados, y se seleccionan por contexto (frontend vs general, por area). Esta capa NO escribe en el vault: produce un objeto Synthesis validado que la Capa 8 (validacion) chequea y la Capa 5 (writer) persiste.

### Contexto de sintesis (SynthesisContext)
Combina el concepto (Capa 1), la investigación (Capa 6) y la configuracion de prompts.
Campos: concept (ConceptMeta), raw_research (RawResearch), sources (lista de PersistedSource), volatility, low_coverage, low_sources, manual_notes, neighbor_concepts (conceptos conectados, para cross-links), prompt_context (FRONTEND | BACKEND | DATA | INFRA | GENERAL), prompt_version.

Reglas: prompt_context se deriva del area del concepto con un mapeo configurable (area_to_context). Si el area no esta mapeada → GENERAL. neighbor_concepts se resuelve a partir de concept.connections (wikilinks) cruzando con el indice de conceptos del vault (Capa 2 scan). Solo se incluyen los que existen como concepto (con bloque ai). Los que no existen se marcan como "pendientes de crear" pero no se linkean como concepto. manual_notes se inyecta en el prompt como "contexto previo del autor". low_coverage/low_sources se propagan para que la sintesis marque secciones inciertas y la validacion las penalice.

### Templates de prompt por contexto (frontend vs general)
Los prompts son archivos Markdown editables y versionados en prompts/. Se organizan por contexto y por "rol" (system, synthesis, sections). La seleccion es por prompt_context + override por concepto.

Estructura de archivos:
- prompts/_base.md (instrucciones comunes: tono, formato, idioma)
- prompts/system.md (rol del modelo: pedagogo, tecnico, preciso)
- prompts/contexts/{frontend,backend,data,infra,general}.md
- prompts/sections/{definition,how_it_works,examples,common_errors,cross_links}.md
- prompts/synthesis.md (prompt principal de sintesis: study guide)
- prompts/versions.yaml (versionado de prompts)

Reglas: los prompts son la unica fuente de "como" se redacta. El codigo de sintesis no hardcodea texto pedagogico; solo orquesta variables y secciones. Fallback de contexto: si no existe contexts/<ctx>.md, se usa general.md. Nunca falla por falta de template de contexto. Override por concepto: config/concepts/<id>.yaml puede fijar prompt_version y prompt_context. El hash del template se persiste en el resultado de sintesis para trazabilidad. Los prompts se versionan en git junto al codigo; cambiar un prompt es un cambio de codigo (review + test).

### Generacion del resumen/study guide a partir de las fuentes
La sintesis toma el raw_research (respuestas agrupadas a/b/c con claims trazables) y genera un study guide Markdown. Se hace en pasos:
1. Preparar el material de entrada (investigacion cruda → bloque de contexto: fuentes disponibles + respuestas por grupo con claims trazables).
2. Cargar y renderizar el prompt principal (variables: title, area, key_ideas, connections, volatility, low_coverage, low_sources, manual_notes, research_block, neighbor_concepts, sections_required).
3. Invocar la generacion (backend como LLM de sintesis reutilizando el notebook de investigacion, o LLM directo segun config). El backend fake permite probar sin red.
4. Normalizar la salida a Markdown canonico (headings, code fences, listas, espacios).
5. Separar fundamento estable / practica moderna (por headings canonicos: ## Fundamento y ## Practica moderna).
6. Armar cross-links (conceptos vecinos).
7. Ensamblar el Synthesis final (markdown, sections, stable_foundation, modern_practice, cross_links, claims_index, prompt_template_hash, prompt_version, prompt_context, generated_at, coverage, low_coverage).

Reglas: la sintesis se alimenta SIEMPRE de raw_research.json + sources.json (no re-investiga). Si faltan → error MissingResearchError. Si low_coverage es true, se agrega una nota al prompt para que el modelo marque secciones inciertas. La generacion puede ir por backend (reutilizando el notebook) o por LLM directo (configurable). normalize_markdown corrige formato sin cambiar contenido. La separacion fundamento/practica es por headings canonicos.

### Secciones requeridas del output
El study guide generado debe contener, como minimo, estas secciones (en este orden sugerido). La validacion (Capa 8) verifica su presencia y calidad:
- definicion: que es y por que importa
- como_funciona: mecanismo, modelo mental, flujo
- ejemplos: codigo/ejemplos concretos (al menos 2, uno minimo y uno con caso limite; code fence con lenguaje)
- errores_comunes: pitfalls y como evitarlos (3-6 errores tipicos con sintoma, causa raiz, correccion)
- fundamento: base estable (invariantes, historia, estandares; NO versiones ni herramientas)
- practica: estado del arte, versiones, herramientas actuales, qué se considera obsoleto
- relacionados: cross-links a conceptos vecinos (wikilinks)

Reglas: las secciones son obligatorias salvo config (required_sections configurable, default todas). Si falta una → la validacion la marca como error (no se escribe). El orden canonico es el de REQUIRED_SECTIONS; el modelo puede agregar subsecciones, pero las canonicas deben existir con ese heading exacto. fundamento y practica son la separacion clave del diseño: fundamento estable (cambia cada 90d) vs practica moderna (cambia cada 7-30d). Permite re-sintetizar solo la parte practica cuando hay nueva info sin tocar el fundamento. Cada afirmación factual debe llevar cita [src-N] apuntando a un source_id de sources.json. Las afirmaciones sin cita se marcan [UNVERIFIED] (la validacion las penaliza).

### Conexion con conceptos vecinos (cross-links)
Los cross-links conectan el concepto sintetizado con sus vecinos (de concept.connections y del indice del vault). Se generan como wikilinks de Obsidian con una frase explicativa, y se validan contra el vault (no se inventan conceptos).
- Solo se generan wikilinks a conceptos que existen en el indice del vault (o se marcan como "pendiente de crear"). Nunca se inventan titulos de conceptos.
- Los wikilinks usan el concept_id (slug del path) como target, con alias al titulo: [[concept_id|Título]]. Esto garantiza que Obsidian resuelva el link aunque el archivo se renombre.
- Si un concepto vecino no existe, el wikilink queda "roto" intencionalmente (Obsidian lo muestra como no creado) y se marca como pendiente. La validacion lo reporta como warning, no error.
- La direccion (out/in/both) se registra para futuras mejoras (backlinks). En v1 solo se usan out (del concepto actual hacia el vecino).
- build_cross_links es idempotente: re-ejecutar con los mismos inputs produce los mismos links (orden estable por orden de concept.connections).

### Como se estructura el resultado de sintesis
El resultado de la sintesis es un objeto Synthesis que se persiste como artefacto intermedio (synthesis.json) y se pasa a la validacion (Capa 8) y al writer (Capa 5).
Campos: concept_id, title, markdown (lo que se escribe en el vault), sections (dict section_name → contenido md), stable_foundation, modern_practice, cross_links, claims_index (afirmaciones → source_id, trazabilidad), prompt_template_hash, prompt_version, prompt_context, generated_at, coverage, low_coverage.

Persistencia: synthesis.json se escribe de forma atomica (temp + rename) en workdir/concepts/<concept_id>/. Nunca en el vault. El markdown del Synthesis es lo que el writer (Capa 5) inserta en el bloque ai:start/ai:end. Es el único campo que toca el vault (via writer). claims_index permite trazabilidad end-to-end. Si ya existe synthesis.json válido y la investigación no cambió (mismo hash de raw_research) → se salta la sintesis (idempotencia), salvo --force o --re-synthesize. La sintesis NO escribe en el vault; solo persiste synthesis.json. La escritura la hace el writer (Capa 5) después de la validación (Capa 8).

### Integracion con el estado (Capa 3)
Al terminar OK: status → VALIDATING, checkpoint "synthesizing", phase_data.synthesis_done = True, synthesis_path, prompt_version, prompt_hash, sections_present, unverified_claims.

Mapeo de errores: MissingResearchError (no hay raw_research.json) → failed reintentable (volver a researching). PromptNotFoundError (falta un template requerido) → failed no reintentable hasta arreglar config (tratar como blocked si es config). SynthesisGenerationError (el LLM/backend fallo al generar) → failed reintentable (vuelve a synthesizing). LowCoverageError (si bloqueante) → blocked. Errores de IO → failed reintentable.

### Excepciones de la capa
SynthesisError (base), MissingResearchError, PromptNotFoundError, SynthesisGenerationError, NormalizationError, MissingSectionError, CrossLinkError, SynthesisPersistError.

### Reglas de negocio
- La sintesis NO escribe en el vault; solo persiste synthesis.json en workdir. La escritura la hace el writer (Capa 5) tras la validacion (Capa 8).
- Se alimenta SIEMPRE de raw_research.json + sources.json (Capa 6). Si faltan → failed reintentable (volver a investigar).
- Los prompts son editables y versionados en prompts/; se seleccionan por contexto (frontend/backend/data/infra/general) con fallback a general.
- Override por concepto: config/concepts/<id>.yaml puede fijar prompt_context y prompt_version.
- Secciones requeridas del output: definicion, como funciona, ejemplos, errores comunes, fundamento (estable), practica (moderna), relacionados. Faltante → error de validacion.
- Separacion fundamento estable vs practica moderna: fundamento cambia cada ~90d, practica cada ~7-30d. Permite re-sintetizar solo la practica.
- Cada afirmación factual lleva cita [src-N] a un source_id. Sin cita → [UNVERIFIED] (la validacion las penaliza).
- Cross-links solo a conceptos existentes en el vault (o marcados como pendiente de crear). Nunca se inventan conceptos.
- Wikilinks usan [[concept_id|Título]] para resolucion estable en Obsidian.
- Idempotencia: si synthesis.json es válido y la investigación no cambió (mismo hash de raw_research) → se salta, salvo --force o --re-synthesize.
- Trazabilidad: prompt_template_hash + prompt_version + claims_index permiten auditar qué prompt y qué fuentes generaron cada contenido.
- low_coverage/low_sources se propagan: la sintesis marca secciones inciertas con '⚠️ por verificar' y la validacion las penaliza.

---

## Capa 8 — Validacion (validation.py)

### Objetivo
Validar la sintesis (Synthesis) antes de que el writer la persista en el vault. Dos capas: determinista (formato, estructura, enlaces, hashes, frontmatter) y semantica (contenido, contexto, relaciones, profundidad, pedagogia, trazabilidad). 17 chequeos con severidad error/warn. Falla cerrado: ante la duda, no escribe. Esta capa NO escribe en el vault: produce un ValidationResult que el orquestador consulta para decidir si pasa a writing o marca failed/blocked.

### Conceptos clave (ValidationResult, Check, Severity, Gate)
- Severity: ERROR (bloquea la escritura) / WARN (se registra; puede bloquear si supera umbral).
- CheckResult: check_id, name, layer (deterministic/semantic), severity, passed, message, evidence, duration_ms.
- ValidationResult: concept_id, synthesis_path, checked_at, prompt_template_hash, checks (lista), errors (subset error y no passed), warnings (subset warn y no passed), is_valid (gate final), blocked_reason, score (0..1, fraccion de checks pasados ponderado).

Cada chequeo es una funcion pura (ctx) → CheckResult: no tiene efectos secundarios, no toca el vault ni el disco. Los chequeos son independientes: el fallo de uno no impide ejecutar los demás (se reportan todos los problemas de una pasada). ValidationResult se persiste como artefacto (validation.json) para auditoria y para el reporte final del lote. is_valid se calcula al final por el gate, no por los chequeos individuales.

### Catalogo de los 17 chequeos
Deterministas:
1. V_STRUCT_SECTIONS — error — todas las secciones requeridas presentes.
2. V_STRUCT_HEADINGS — error — headings canonicos exactos (## Título).
3. V_STRUCT_ORDER — warn — orden canonico de secciones.
4. V_CONTENT_MIN_LENGTH — error/warn — longitud mínima por sección (palabras).
5. V_CONTENT_NO_PLACEHOLDERS — error — sin placeholders/TODO/XXX/[...]/lorem.
6. V_CONTENT_CODE_FENCES — warn — code fences cerrados y con lenguaje declarado.
7. V_LINKS_RESOLVE — warn — cross-links resuelven o están marcados pendiente.
8. V_LINKS_NO_INVENTED — error — no se inventan conceptos (wikilink a inexistente no marcado).
9. V_LINKS_FORMAT — warn — formato [[concept_id|Título]].
10. V_FRONTMATTER_PARSE — error — frontmatter parseable (YAML válido).
11. V_FRONTMATTER_FIELDS — error — campos requeridos presentes (title, area).
12. V_FRONTMATTER_MATCH — error — frontmatter coincide con el ConceptMeta.

Semanticos:
13. V_SEM_TRACES — warn — afirmaciones con cita [src-N] (ratio de trazabilidad).
14. V_SEM_UNVERIFIED_MARKED — error — claims sin fuente marcados [UNVERIFIED].
15. V_SEM_SEPARATION — error — fundamento vs practica separados (no versiones en fundamento).
16. V_SEM_DEPTH_PEDAGOGY — warn — profundidad mínima + tono pedagogico/definicion clara.
17. V_SEM_CONTEXT — warn — coherencia con key_ideas y connections del concepto.

### Validacion estructural (secciones requeridas presentes)
- V_STRUCT_SECTIONS es bloqueante (error): si falta una seccion requerida, no se escribe.
- V_STRUCT_HEADINGS es bloqueante (error): los headings deben coincidir exactamente con SECTION_TITLES (ej. ## Fundamento (estable)), porque el writer y la re-sintesis dependen de ellos.
- V_STRUCT_ORDER es warning: el orden canonico se recomienda pero no bloquea (subsecciones extras son válidas).
- Las secciones requeridas son configurables (required_sections en config), por defecto las 7 de REQUIRED_SECTIONS.
- Secciones extra (no canonicas) se permiten y no penalizan, pero se registran en evidence para auditoria.

### Validacion de contenido (longitud mínima, sin placeholders)
- V_CONTENT_MIN_LENGTH: si una seccion tiene menos de la mitad del minimo → error (bloquea); si está entre la mitad y el minimo → warning (se registra pero no bloquea por si solo). Si está sobre el minimo pero bajo el target → no penaliza.
- V_CONTENT_NO_PLACEHOLDERS es error: un placeholder indica que la sintesis no termino; nunca se escribe contenido con TODO/XXX/[...].
- V_CONTENT_CODE_FENCES: si hay fences sin cerrar → warning (el writer normaliza, pero se reporta). Si falta el lenguaje → warning (se asume text).
- Los umbrales (MIN_WORDS, TARGET_WORDS) viven en validation.yaml y se pueden ajustar por area.
- PLACEHOLDER_PATTERNS se carga de config para permitir agregar patrones por proyecto.

### Validacion de cross-links (conceptos existentes)
- V_LINKS_RESOLVE es warning: los wikilinks rotos son validos SI están marcados como pendiente de crear (Obsidian los muestra como no creados). Sin marcar → se reporta pero no bloquea por si solo.
- V_LINKS_NO_INVENTED es error: un wikilink a un concepto inexistente NO marcado como pendiente se considera un concepto inventado por el modelo → bloquea. Proteccion contra alucinacion de conceptos vecinos.
- V_LINKS_FORMAT es warning: el formato canonico es [[concept_id|Título]] (alias al titulo). Sin alias, Obsidian usa el id como texto visible (menos legible) pero no rompe.
- La validacion cruza contra vault_index (indice de conceptos del scan de Capa 2), no contra el filesystem en tiempo real.
- Los wikilinks a conceptos inexistentes marcados como pendiente se cuentan en broken_links del PersistedSynthesis (Capa 7) y se reportan al final del lote para crearlos.

### Validacion de frontmatter
- V_FRONTMATTER_PARSE es error: si el frontmatter no es YAML válido, no se puede confiar en los metadatos; bloquea.
- V_FRONTMATTER_FIELDS es error: title y area son obligatorios (configurable). Si faltan, el concepto no se puede identificar correctamente.
- V_FRONTMATTER_MATCH es error: el frontmatter de la nota debe coincidir con el ConceptMeta extraido (Capa 2). Una discrepancia indica que la nota cambio manualmente o que el scan extrajo mal → bloquea para revision.
- La validacion de frontmatter NO modifica el frontmatter (eso es responsabilidad del writer, que lo preserva byte a byte). Aqui solo se verifica.
- Si el archivo no tiene frontmatter, V_FRONTMATTER_PARSE y V_FRONTMATTER_FIELDS se marcan como no aplicables (passed=True con evidence applicable=False) salvo que config exija frontmatter (require_frontmatter: true).
- frontmatter_required_fields es configurable (default ["title", "area"]); se puede exigir numero, aliases, tags en proyectos mas estrictos.

### Validacion semantica (contenido, contexto, relaciones, profundidad, pedagogia, trazabilidad)
- V_SEM_TRACES: mide la fraccion de afirmaciones con cita [src-N]. Umbral configurable (default 0.6). Es warning, no bloquea por si solo, pero se combina con V_SEM_UNVERIFIED_MARKED.
- V_SEM_UNVERIFIED_MARKED es error: si una afirmacion no tiene cita, DEBE estar marcada [UNVERIFIED]. Afirmar sin fuente ni marca es alucinacion → bloquea.
- V_SEM_SEPARATION es error: el fundamento (estable) no debe contener versiones, herramientas ni términos de obsolescencia; eso va en practica. Mezclarlos rompe la re-sintesis parcial.
- V_SEM_DEPTH_PEDAGOGY es warning: verifica profundidad (secciones no superficiales) y pedagogia (definicion de 2-4 oraciones, ejemplos con code fence). No bloquea, pero se reporta.
- V_SEM_CONTEXT es warning: verifica que el contenido refleje los key_ideas y connections del concepto. Si el modelo ignoro el contexto del vault → se reporta.
- Los chequeos semanticos usan heurísticas (regex, conteo de palabras, keywords). No son perfectos; por eso son warnings salvo V_SEM_UNVERIFIED_MARKED y V_SEM_SEPARATION que son errores.
- extract_factual_claims, has_citation, split_sentences, extract_keywords son helpers heuristicos (implementacion en validation_helpers.py).

### Gate: cómo se decide si un resumen es válido o no
Falla cerrado:
- Si hay al menos un check de severidad error que falló → is_valid = False (bloquea, no se escribe). Regla principal.
- Si strict_mode = True y hay warnings → bloquea (modo para calibracion/piloto).
- Si el número de warnings supera max_warnings_before_block (default 5) → bloquea (requiere revisión humana).
- Si algun check listado en blocking_checks falla (aunque sea warn) → bloquea.
- En cualquier otro caso (0 errores y warnings dentro del umbral) → is_valid = True (pasa a writing).
- Principio "falla cerrado": si un chequeo lanza una excepcion interna (no capturada), se trata como error fallido (no se asume válido). El runner captura la excepcion y marca el check como passed=False con message="internal error: ...".
- El gate NO considera el score (es informativo). Un resumen con score alto pero un error bloqueante sigue siendo invalido.
- Los warnings NO bloquean por si solos (salvo strict_mode o umbral). Se persisten en validation.json y se reportan al final del lote para revision.

### Persistencia del resultado (validation.json)
validation.json se escribe de forma atomica (temp + rename) en workdir/concepts/<concept_id>/. Nunca en el vault. Si ya existe validation.json válido y la sintesis no cambió (mismo prompt_template_hash y mismo hash de synthesis.json) → se salta la validacion (idempotencia), salvo --force o --re-validate. errors y warnings se persisten como listas de check_id para consultas rápidas. El score es informativo (fraccion de checks pasados). No se usa en el gate.

### Integracion con el estado (Capa 3)
Flujo validation_phase: cargar concepto, estado, sintesis (si falta → MissingSynthesisError), vault_index, frontmatter_raw. Ejecutar run_validation. Persistir validation.json. Si is_valid → status WRITING, checkpoint "validating", phase_data.validation_done, validation_path, validation_score, validation_warnings. Si no → si "errors" en blocked_reason → mark_failed (fase "validating"); si no → mark_blocked ("validation", blocked_reason). Persistir estado. Lanzar ValidationError.

Mapeo de errores: MissingSynthesisError (no hay synthesis.json) → failed reintentable (volver a synthesizing). ValidationError con blocked_reason conteniendo "errors" → failed (los checks de error fallaron; se puede reintentar tras corregir la sintesis/config). ValidationError por warnings/umbral → blocked (requiere revision humana). Excepcion interna no capturada → failed (falla cerrado). Errores de IO → failed reintentable.

Reglas: si is_valid = True → el orquestador pasa a writing (Capa 5). El writer recibe la Synthesis validada. Si is_valid = False por errores → failed (reintentable). Si is_valid = False por warnings/umbral → blocked (requiere revision humana; no se reintenta automaticamente). La validacion NO modifica la sintesis: si falla, la Synthesis queda persistida (synthesis.json) para inspeccion/debugging. El writer (Capa 5) asume que la sintesis que recibe ya paso la validacion. No la re-valida.

### Excepciones de la capa
ValidationError (base, lleva el ValidationResult completo), MissingSynthesisError, StructuralValidationError, ContentValidationError, CrossLinkValidationError, FrontmatterValidationError, SemanticValidationError.

### Reglas de negocio
- La validacion NO escribe en el vault; solo persiste validation.json en workdir. La escritura la hace el writer (Capa 5) tras pasar el gate.
- Dos capas: determinista (formato, estructura, enlaces, hashes, frontmatter) y semantica (contenido, contexto, relaciones, profundidad, pedagogia, trazabilidad).
- 17 chequeos con severidad error/warn. Falla cerrado: ante la duda, no escribe.
- Un check de severidad error que falla bloquea la escritura (no se escribe). Los warn se registran y solo bloquean si superan el umbral o en modo estricto.
- La validacion es idempotente: si validation.json es válido y la sintesis no cambió (mismo prompt_template_hash) → se salta, salvo --force o --re-validate.
- Los chequeos son funciones puras e independientes: el fallo de uno no impide ejecutar los demás.
- Si un chequeo lanza una excepcion interna, se trata como error fallido (falla cerrado).
- La validacion cruza los cross-links contra el vault_index (indice del scan), no contra el filesystem en tiempo real.
- El frontmatter se verifica pero NO se modifica (preservacion byte a byte es responsabilidad del writer).
- V_SEM_UNVERIFIED_MARKED y V_SEM_SEPARATION son los únicos chequeos semanticos bloqueantes (error); el resto de los semanticos son warnings.
- Los umbrales (min_words, trace_threshold, max_warnings_before_block) viven en validation.yaml y son ajustables por area/concepto.
- validation.json se persiste de forma atomica y se incluye en el reporte final del lote (errores/warnings agregados por concepto).
- El writer (Capa 5) asume que la sintesis que recibe ya paso la validacion; no la re-valida.
- Trazabilidad: prompt_template_hash se persiste en ValidationResult para auditar qué prompt generó el contenido validado.
- score es informativo (fraccion de checks pasados); no se usa en el gate.

---

## Capa 9 — Orquestador (runner.py) + logging

### Objetivo
Encadenar todas las fases del pipeline (investigacion, sintesis, validacion, escritura) por concepto y por lote. Decide que ejecutar, en qué orden, cómo reintentar, cómo reanudar tras un corte, cómo registrar todo en logs estructurados, y cómo producir el reporte final. Es el único componente que "sabe" del pipeline completo; las fases individuales (Capas 6-8) no se llaman entre sí directamente. Esta capa NO toca el vault: solo coordina, persiste estado (via state.py) y escribe logs/reportes en workdir.

### Bucle principal sobre los conceptos (cola, orden)
El runner arranca con un scan del vault (Capa 2) para obtener la cola de conceptos. La cola es FIFO y el orden es el del scan (numérico por concepto, configurable). Se procesa un concepto a la vez (serial), con pacing entre conceptos para no saturar el backend. Un concepto que falla no detiene el lote.

Reglas de la cola:
- scan_concepts (Capa 2) devuelve la lista de conceptos con bloque ai:start/end + notas sin bloque.
- La cola incluye solo conceptos cuyo estado NO es terminal (done/failed/blocked) salvo --force o --retry-failed.
- Filtros: --only <ids>, --from <concept_id> (reanudar desde un concepto), --area <area>, --status <status>.
- Orden: scan order / orden numérico del concepto. Configurable (concept_order: numeric | scan | mtime).
- concurrency_concepts en v1 es 1 (serial). El campo queda para futuro; el diseño asume serialidad para simplificar checkpoints y evitar race conditions en el vault.
- Un concepto que lanza una excepcion no capturada NO detiene el lote: se marca failed, se registra y se sigue con el siguiente.
- Pacing configurable entre conceptos (pacing_between_concepts_s, default 1s) para no saturar NotebookLM / rate limits.

### Transiciones de estado por concepto
El runner ejecuta las fases en orden lineal. Cada fase es una funcion async que recibe concept_id y devuelve el control al runner, que entonces persiste el estado y avanza. Las transiciones válidas son las de la Capa 3 (TRANSITIONS). El runner no salta fases ni las reordena.

Orden de fases fijo: researching → synthesizing → validating → writing. No se salta ninguna (salvo --stop-after, que detiene el pipeline entero, no la fase).

Pseudo-flujo run_concept:
- cargar estado (o crear nuevo)
- si terminal y no force → skip
- determinar fase de inicio (resume)
- para cada fase desde la de inicio:
  - si --stop-after alcanzado → break
  - ejecutar fase con reintentos
  - si falla → clasificar (failed/blocked), persistir error, devolver resultado (no sigue)
  - si OK → avanzar estado (next_status), persistir checkpoint
- si llega al final sin error → asegurar status DONE

Reglas de transicion: cada fase persiste su estado (estado.json) ANTES de avanzar a la siguiente. Si el proceso se corta, el checkpoint permite reanudar sin repetir la fase terminada. next_status(phase) devuelve el estado siguiente del enum (RESEARCHING → SYNTHESIZING, etc.; WRITING → DONE). Si una fase falla, el estado pasa a failed o blocked (según la clasificación del error) y el concepto se deja en ese estado terminal operativo. --stop-after <phase> detiene el concepto (y el lote) tras completar la fase indicada. Útil para calibración. El runner NO llama a las fases directamente con logica de negocio: delega en research_phase, synthesis_phase, etc. (Capas 6-8). El runner solo coordina, reintenta y persiste estado.

Clasificacion de fallos (mapeo centralizado excepcion → estado terminal):
- BackendAuthError → BLOCKED (requiere accion humana: renovar credenciales)
- ValidationError con "errors" en blocked_reason → FAILED (reintentable tras corregir sintesis/config)
- ValidationError (warnings/umbral) → BLOCKED (requiere revision humana)
- Errores del writer por markers/integridad → FAILED (reintentable tras resolver la causa)
- BlockedError → BLOCKED
- default → FAILED (reintentable)

### Checkpoint y resume
El checkpoint es el par (status, checkpoint) persistido en estado.json por concepto. Al arrancar un concepto, el runner lee el estado y decide desde qué fase reanudar. Si el estado es terminal, no se reejecuta (salvo --force). Si es no-terminal, se reanuda desde el último checkpoint persistido, sin repetir las fases ya completadas.

Reglas de checkpoint/resume:
- estado.json es la única fuente de verdad del progreso. Sin él no hay recuperación ni idempotencia.
- El checkpoint se persiste de forma atómica en cada transición validada (Capa 3). El runner no mantiene estado en memoria que no esté persistido: si el proceso muere, el estado en disco es suficiente para reanudar.
- Reanudación fina dentro de una fase: la investigación (Capa 6) es reanudable por pregunta; la síntesis y la validación se re-ejecutan completas si se cortan (son idempotentes y más baratas que la investigación). La escritura (Capa 5) es idempotente por hash del afuera.
- --force ignora el estado terminal y re-ejecuta desde la primera fase (útil para re-procesar tras cambiar prompts o config). Con --force, el runner NO borra los artefactos previos: las fases individuales deciden si reutilizan o regeneran (por hash de entrada).
- --retry-failed solo reintenta conceptos en failed/blocked (no toca los done).
- Si estado.json está corrupto o ilegible, el runner lo reporta como blocked con "estado corrupto" y NO intenta adivinar. Se puede reparar manualmente o con --reset-state <concept_id>.
- El runner persiste el run_id en cada estado.json actualizado, para poder correlacionar logs y estados con la corrida que los generó.

### Logging estructurado
El logging es en formato JSON Lines (un objeto JSON por línea), escrito en workdir/logs/run-<run_id>.jsonl. Cada línea tiene campos estándar para poder filtrar, agregar y auditar. No se usan logs de texto libre en producción (solo en --verbose para debug). Los secretos (auth, cookies) nunca se registran.

Eventos mínimos a registrar (por concepto y por corrida): run_start, run_end (con resumen agregado); queue_built (total, filtros, orden); concept_start, concept_end, concept_error, concept_skipped_terminal; phase_ok, phase_failed, phase_retry, phase_start; checkpoint (cada vez que se persiste un checkpoint); backend_call (método, target, duración, ok/error) — nivel debug, activable con --verbose; validation_summary (is_valid, score, errors, warnings); report_written (path del reporte final); circuit_breaker_open; cleanup_failed.

Reglas de logging: formato JSON Lines (una línea = un evento). Parseable con jq, pandas, o cualquier herramienta de logs. Flush por línea: si el proceso muere, no se pierden eventos. Niveles: debug (backend calls, checkpoints), info (fases, conceptos), warn (reintentos, warnings de validación), error (fallos, excepciones). --verbose activa nivel debug; por defecto info. Rotación: un archivo por corrida (run-<run_id>.jsonl). No se sobrescriben corridas previas. Limpieza manual o por política de retención (config: log_retention_days, default 30). Los logs NO contienen secretos ni contenido de notas (solo ids, paths relativos, counts, errores). El contenido generado se persiste en workdir/concepts/<id>/, no en el log. run_id se genera al arrancar (run-YYYYMMDD-HHMMSS-<shortuuid>) y se propaga a todos los registros y a estado.json. El logger se cierra al final de la corrida (close()). En caso de excepción no capturada, un handler de atexit/finally asegura el flush y cierre.

### Manejo de errores y reintentos
Cada fase se ejecuta con reintentos y backoff exponencial. El manejo distingue errores reintentables (red, timeout, rate limit, IO transitorio) de los no reintentables (auth, validación con errores, markers faltantes). Los reintentos son por fase, no por concepto completo: si researching falla 3 veces, el concepto queda failed en researching y el lote sigue.

Reglas de reintentos: max 3 intentos por fase (configurable: max_retries). Backoff exponencial: intento 1 → 2s, intento 2 → 4s, intento 3 → 8s (configurable en backoff_seconds). Errores reintentables: BackendTimeout, BackendNetworkError, BackendRateLimitError, errores de IO/transitorios. Se reintenta con backoff. Errores no reintentables: BackendAuthError (requiere acción humana), errores del writer por markers/integridad (requieren intervención), ValidationError (la síntesis no pasó; reintentar la misma síntesis no ayuda; hay que regenerar). Se propagan de inmediato sin reintentar. Al agotar los reintentos, la fase se marca failed (o blocked según clasificación) y se persiste el error (fase_fallida, error, timestamp). El lote sigue con el siguiente concepto. Limpieza best-effort ante fallo: si create_notebook OK pero add_sources falla → intentar delete(notebook_id) para no dejar notebooks huerfanos. Si la limpieza falla, se registra en log (cleanup_failed) pero no bloquea. Los notebooks huerfanos se reportan al final del lote. Circuit breaker simple: si se acumulan N fallos consecutivos de red/backend (config: circuit_breaker_threshold, default 5), el runner pausa el lote por circuit_breaker_cooldown_s (default 60s) y registra circuit_breaker_open. Si tras la pausa sigue fallando, marca el concepto como blocked con "backend no disponible" y sigue. Esto evita hammering al backend. Los reintentos NO repiten trabajo ya persistido: la investigación reanuda por pregunta, la síntesis/validación son idempotentes por hash, la escritura es idempotente por hash del afuera. Un reintento de una fase que falló a mitad continúa desde el checkpoint, no desde cero. --max-retries N (CLI) sobrescribe el config para una corrida puntual.

### Reporte final
Al terminar el lote, el runner genera un reporte final en workdir/reports/run-<run_id>.json (y opcionalmente .md). El reporte agrega métricas por concepto y por lote, lista los conceptos fallidos/bloqueados, los de baja cobertura/fuentes, los wikilinks rotos, los notebooks huerfanos y los tiempos. Es la "foto" de la corrida para revisión humana y para el CLI (ai status, ai review).

Contenido del reporte: run_id, started_at, finished_at, duration_ms, config_summary (sin secretos), totals (total, done, failed, blocked, skipped), by_status, by_phase_failed, by_area (metricas por area), concepts (lista de ConceptRunResult), failed_concepts, blocked_concepts, low_coverage_concepts, low_sources_concepts, broken_links_total, broken_links_by_concept, orphan_notebooks, orphan_notes_without_block, validation_warnings_agg, timings, recommendations.

Reglas del reporte: se genera SIEMPRE al final de la corrida, incluso si hubo fallos o interrupción (con --interrupted se marca como parcial). No se pierde la información de lo procesado. El reporte JSON es la fuente para el CLI: ai status lee el último reporte + estado.json; ai review muestra los conceptos bloqueados/fallidos con su detalle. Los conceptos done se incluyen en el reporte con su score de validación y coverage, para poder detectar regresiones. recommendations se genera con reglas simples: si hay bloqueados por auth → "renovar credenciales"; si hay muchos low_coverage → "revisar fuentes de los conceptos X"; si hay notebooks huerfanos → "limpiar manualmente". El reporte NO incluye contenido de notas ni secretos. Solo ids, métricas, errores resumidos y paths relativos a workdir. Si el lote se interrumpe (Ctrl+C / SIGTERM), el runner captura la señal, persiste el estado actual, genera un reporte parcial con interrupted: true y sale limpiamente (no corrompe estado.json). Idempotencia del reporte: re-correr genera un reporte nuevo con nuevo run_id; los anteriores se conservan (no se sobrescriben). Limpieza por política de retención (report_retention_days, default 30).

### Integracion con CLI (Capa 10, adelanto)
El runner expone una interfaz mínima para que la CLI lo invoque sin conocer detalles: run_one(concept_id, **overrides) procesa un solo concepto; run_batch(concept_ids, **overrides) procesa el lote; status() devuelve el estado agregado leyendo estado.json + ultimo reporte; review(concept_id) devuelve conceptos bloqueados/fallidos con detalle para revision humana.

### Excepciones del runner
RunnerError (base), QueueBuildError, StateCorruptError, InterruptedRunError, ReportWriteError.

### Reglas de negocio
- El orquestador es el único que conoce el pipeline completo. Las fases (Capas 6-8) no se llaman entre sí; el runner las coordina.
- Procesamiento serial por concepto: se transiciona y persiste el estado (checkpoint) ANTES de avanzar a la fase siguiente.
- Un concepto que falla no detiene el lote; se registra y se sigue con el siguiente.
- Cola FIFO de conceptos en pending (resultado del scan), orden configurable (default numérico).
- Reintentos por fase (max 3, backoff exponencial) con clasificación de errores reintentables vs no reintentables.
- Checkpoint y resume: el runner lee estado.json al arrancar cada concepto y reanuda desde el último checkpoint. Sin estado.json no hay recuperación.
- --force re-ejecuta desde la primera fase; --retry-failed solo reintenta terminales reintentables.
- Logging estructurado (JSON Lines) con flush por línea, un archivo por corrida, sin secretos ni contenido de notas.
- Reporte final siempre (incluso parcial/interrumpido) en workdir/reports/run-<run_id>.json (+ .md opcional).
- Circuit breaker ante fallos consecutivos de backend para evitar hammering.
- Limpieza best-effort de notebooks huerfanos ante fallo; se reportan al final.
- Manejo de señales (Ctrl+C/SIGTERM): persiste estado, genera reporte parcial, sale limpio.
- El runner NO toca el vault: solo coordina, persiste estado (via state.py) y escribe logs/reportes en workdir.
- El runner NO re-valida la sintesis: confía en que la validación (Capa 8) ya pasó antes de writing.

---

## Capa 10 — CLI (cli.py)

### Objetivo
Ser la interfaz de entrada para humanos y agentes sobre el orquestador (Capa 9). Expone subcomandos para escanear, inspeccionar, ejecutar, consultar estado, revisar bloqueados/fallidos y resetear conceptos, mas un reporte final legible. Sin prompts interactivos: todo se controla por flags y argumentos. Produce salida humana (colores, tablas) o JSON (--json) para consumo por agentes/CI. La CLI no contiene logica de negocio: valida argumentos, carga config, instancia el runner y delega. Toda la verdad del progreso vive en estado.json y en los reportes del runner.

### Como se invoca y se configura
Punto de entrada: python -m cli o el script ai (entry point). La CLI es un wrapper delgado sobre Runner (Capa 9). No importa fases ni backend directamente.

Configuración (precedencia, de mayor a menor): 1) Flags de CLI (--backend, --workdir, --vault, --force, etc.). 2) Variables de entorno (AI_WORKDIR, AI_VAULT_ROOT, BACKEND_PROVIDER, AI_CONFIG, NO_COLOR). 3) Archivo de config (config.yaml o el path de --config / AI_CONFIG). 4) Defaults internos.

Reglas de invocacion: la CLI se ejecuta siempre desde la raíz del proyecto o con --workdir/--vault explícitos. No asume rutas relativas al CWD si no encuentra config.yaml (error claro). Sin prompts interactivos: si falta un argumento requerido, falla con código de salida != 0 y mensaje de uso. Nunca llama a input(). --config <path> permite usar configs alternativas. --json activa salida estructurada (un JSON por comando) para agentes/CI. En modo JSON se suprimen colores, spinners y tablas. --quiet / -q reduce la salida a errores y al resultado final. --verbose / -v activa debug. --no-color (o env NO_COLOR) desactiva colores. En Windows se detecta soporte ANSI; si no, se cae a texto plano. Exit codes: 0 OK, 1 error genérico / concepto fallido, 2 error de uso/argumentos, 130 interrumpido (Ctrl+C).

### Comandos principales
- scan — descubrir conceptos del vault. Flags: --json, --area <area>, --orphans (solo notas sin bloque), --count.
- inspect <concept_id> — inspeccionar un concepto (metadatos, estado, artefactos presentes y su frescura). Flags: --json, --show-markdown, --show-sources, --show-validation.
- run <concept_id> — procesar un solo concepto. Flags: --force, --dry-run, --stop-after <phase>, --re-research, --re-synthesize, --re-validate, --backend <provider>, --max-retries N, --json, --hint "..." (se agrega a extra_hints del concepto).
- run-batch — procesar el lote. Hereda todos los de run más los de filtrado (--only, --from, --area, --status, --concept-order).
- status — estado agregado del lote (lee estado.json + ultimo reporte; NO ejecuta nada). Flags: --json, --failed, --blocked, --low, --area <area>, --limit N, --run <run_id>, --watch.
- review — revisar conceptos bloqueados/fallidos con detalle (error, checks fallidos, sugerencias). Flags: --json, --show-markdown, --errors <structural|content|semantic|all>, --orphans.
- reset — resetear estado de un concepto (o del lote). Flags: --to <status>, --artifacts <list>, --all, --area <area>, --status <status>, --yes, --dry-run, --json.
- report — generar/mostrar el reporte de una corrida (solo lectura). Flags: --run <run_id>, --last, --md, --summary, --out <path>, --format <json|md|csv>, --failed, --blocked, --low, --orphans, --json, --limit N.

Reglas de reset: reset modifica estado.json (y opcionalmente artefactos en workdir). NUNCA toca el vault ni las notas. --all sin --yes falla (exit 2). Resetear a pending vuelve a correr todo desde la primera fase. Resetear a un estado intermedio reanuda desde esa fase. Si se resetea un concepto done, el runner NO revierte el vault: la próxima corrida reescribe el bloque (idempotente por hash del afuera). Se recomienda --force en el run posterior.

Reglas de report: report es de solo lectura: no ejecuta el pipeline ni modifica estado. Solo lee estado.json y los reportes en workdir/reports/.

### Flags y opciones (transversales)
Flags globales (válidos en todos los subcomandos): --config <path> / AI_CONFIG; --workdir <path> / AI_WORKDIR; --vault <path> / AI_VAULT_ROOT; --backend <fake|notebooklm> / BACKEND_PROVIDER; --json; --quiet / -q; --verbose / -v; --no-color / NO_COLOR; --max-retries N; --pacing <seg>.

Flags de filtrado (para run-batch, status, reset, report): --area <area>; --concept <id> / --only <ids>; --from <concept_id>; --hasta <concept_id>; --status <status>; --concept-order <numeric|scan|mtime>.

Flags de ejecución: --dry-run (genera todo y muestra diff/resultados SIN escribir en el vault ni cambiar estado); --force (ignora idempotencia/frescura y re-ejecuta desde la primera fase); --retry-failed (solo reintenta conceptos en failed/blocked); --stop-after <phase>; --re-research (fuerza re-investigación aunque raw_research.json esté fresco); --re-synthesize (fuerza re-síntesis aunque synthesis.json sea válido); --re-validate (fuerza re-validación aunque validation.json sea válido); --strict (activa strict_mode en validación); --cleanup-notebooks / --no-cleanup-notebooks; --keep-history (versiona artefactos por timestamp en lugar de sobrescribir); --hint "..." (agrega un hint manual al contexto de investigación, repetible).

Reglas de combinación: --from y --hasta definen un rango por el orden configurado. Si solo se pasa --from, procesa desde ahí hasta el final. Si solo --hasta, desde el inicio hasta ahí. --concept/--only tiene prioridad sobre --from/--hasta/--area. --dry-run es compatible con run y run-batch (y con reset para previsualizar). --force + --dry-run es válido. --stop-after no se puede combinar con --dry-run (dry-run ya detiene antes de writing; se ignora con warning). Flags desconocidos / combinaciones inválidas → error de uso (exit 2) con mensaje claro, sin ejecutar nada.

### Output y feedback al usuario
Principios: modo humano por defecto (colores si el terminal lo soporta, tablas alineadas, spinners para operaciones largas, mensajes claros con iconos ✓, ✗, ⚠, ℹ). Modo --json: un único objeto JSON por comando en stdout (sin colores, sin spinners, sin texto extra). Los logs del runner van a workdir/logs/, no a stdout. Los errores van a stderr. --quiet: solo el resultado final (una línea) y los errores. Separación stdout/stderr: datos y resultados en stdout; progreso/logs/errores en stderr. En --json, stdout contiene únicamente el JSON.

Feedback durante la ejecución (run / run-batch): spinner animado mientras una fase está en curso (solo modo humano, sin --json/--quiet). Por concepto: se muestra el estado final (done/failed/blocked), la duración, el score de validación y la cobertura. Por lote: al final se imprime el resumen (Total / Done / Failed / Blocked / Skipped) y las listas de fallidos/bloqueados/baja cobertura/links rotos (truncadas con --limit, default 20). Si el lote se interrumpe (Ctrl+C): se imprime "Interrumpido. Estado persistido. Reporte parcial en <path>." y se sale con código 130.

Códigos de salida: 0 OK, 1 hubo conceptos failed/blocked o un concepto run terminó en estado no-done, 2 error de uso/argumentos/config, 130 interrumpido por el usuario. En --json, el código de salida sigue siendo el mismo; el JSON en stdout incluye un campo exit_code y error para que el agente no dependa solo del código.

Mensajes de error: siempre incluyen qué falló, por qué (causa raíz resumida) y qué hacer (siguiente paso sugerido). Errores de config: "config.yaml no encontrado en <path>. Usá --config o AI_CONFIG." / "credenciales de NotebookLM inválidas: ejecutá opencode mcp auth notebooklm o revisá auth_file." Errores de estado: "concepto 'X' no existe en el vault. Ejecutá ai scan para ver los disponibles." Errores de reset: "--all requiere --yes en modo no interactivo." En --json, los errores se emiten como {"error": "...", "code": 2, "hint": "..."} en stderr y el proceso sale con el código correspondiente.

Feedback específico por comando: scan ("Escaneados N archivos .md, M conceptos con bloque, K sin bloque."); inspect (tarjeta con metadatos, estado, artefactos presentes y su frescura); run <id> (línea final "✓ <id> → done (12.3s, score 0.92, coverage 0.83)" o "✗ <id> → failed en validating: V_SEM_SEPARATION"); run-batch (resumen + "Reporte guardado en workdir/reports/run-<run_id>.json"); status (dashboard con barras por estado y por área; "Última corrida: run-... (hace 2h, 240/255 done)"); review (por cada concepto bloqueado/fallido, muestra el blocked_reason/error, los checks fallidos con severidad y una sugerencia); reset ("Reseteados N conceptos a 'pending'. Artefactos borrados: synthesis, validation. (vault intacto)"); report (imprime el reporte (resumen/tabla/markdown) y, si --out, "Reporte exportado a <path>").

### Integración con el runner (Capa 9)
La CLI solo coordina; toda la lógica vive en Runner. La CLI instancia un único Runner por invocación (backend singleton, state store, writer, logger). No se crea un runner por concepto. La CLI no llama a fases ni al backend directamente; todo pasa por runner.run_one / runner.run_batch / runner.status / runner.review. Los filtros (--area, --concept, --from, --hasta, --status) se traducen a only_concept_ids / area_filter / from_concept del RunConfig (Capa 9). --dry-run se propaga como RunConfig.dry_run = True. El runner y las fases respetan el flag (el writer muestra diff sin escribir; el estado no cambia). --json no cambia la ejecución, solo el formato de salida. En --json, el progreso (spinners) se suprime y el resultado final se imprime como un único JSON en stdout. Señales: Ctrl+C se captura en main() y se delega a runner.handle_interrupt(), que persiste estado y genera reporte parcial (Capa 9). La CLI imprime el mensaje de interrupción y sale con 130. La CLI no mantiene estado propio: todo el progreso vive en estado.json y en los reportes del runner. Re-ejecutar un comando es idempotente a nivel de "qué se procesa" (el runner decide por estado).

### Excepciones de la capa
CLIError (base), UsageError, ConfigError, ConceptNotFoundError, ConfirmationRequiredError.

Reglas: la CLI captura CLIError y las excepciones del runner (RunnerError, StateCorruptError, etc.) y las traduce a mensajes amigables + código de salida. Nunca muestra un traceback al usuario salvo en --verbose. En --json, el error se serializa como {"error": "...", "code": N, "hint": "..."} en stderr. KeyboardInterrupt se maneja aparte (exit 130) sin traceback.

### Reglas de negocio
- La CLI es la única interfaz para humanos y agentes; no hay prompts interactivos. Toda decisión se pasa por flag.
- Sin logica de negocio en la CLI: valida argumentos, carga config, instancia el runner y delega. Las fases (Capas 6-8) y el estado (Capa 3) no se tocan directamente.
- Precedencia de config: CLI > env > archivo > defaults. Se valida fail-fast al arrancar (config inexistente o inválida → exit 2 antes de procesar).
- --json produce salida parseable por agentes/CI; modo humano produce salida legible con colores/tablas (degradan a texto plano sin ANSI).
- Exit codes estables: 0 OK, 1 fallidos/bloqueados, 2 error de uso/config, 130 interrumpido.
- --dry-run nunca escribe en el vault ni cambia estado; muestra diff y resultados.
- reset nunca toca el vault; solo estado.json y artefactos en workdir. Operaciones destructivas (--all) requieren --yes.
- report es de solo lectura: no ejecuta el pipeline.
- stdout = datos/resultados; stderr = progreso/logs/errores. En --json, stdout contiene únicamente el JSON.
- La CLI no mantiene estado propio: toda la verdad vive en estado.json y en workdir/reports/. Re-ejecutar es seguro.
- Secretos (auth, cookies) nunca se imprimen ni se registran, incluso en --verbose.
- En Windows se usan rutas y comandos apropiados (PowerShell, py para Python). La CLI detecta el SO solo para elegir colores/ANSI; la lógica es idéntica.
- La CLI se invoca como ai <subcomando> [flags] (entry point) o py -m cli <subcomando> [flags]. Sin subcomando, equivale a run-batch sobre toda la cola.

---

## Capa 11 — Piloto + calibracion

### Objetivo
Cerrar el ciclo: con las 10 capas anteriores implementadas y probadas en aislamiento (backend fake, tests unitarios), se ejecuta un piloto end-to-end sobre un único concepto real y representativo (frontend-01-internet-web). El piloto valida que todo el pipeline (investigación → síntesis → validación → escritura) funciona sobre datos reales, que la integridad del vault se mantiene, y que los parámetros por defecto son razonables. A partir del piloto se calibran los parámetros y se definen los criterios de aceptación que habilitan el escalamiento al frontend completo y luego a las demás áreas. Esta capa NO agrega lógica de negocio nueva: orquesta, mide y decide.

### Proceso de piloto con 1 concepto (frontend-01)
Selección del concepto piloto: frontend-01-internet-web (Internet y la web). Se elige porque: es estable (fundamento invariante: TCP/IP, HTTP, DNS, navegador) → permite probar la separación fundamento/práctica; tiene conexiones ricas (HTTP, DNS, navegador, protocolos) → prueba cross-links; hay abundante fuente canónica (MDN, RFCs, web.dev) → prueba seeds/preferred domains y trazabilidad; área frontend → prueba el contexto de prompts frontend; tiene contenido manual previo (notas del autor) → prueba preservación del afuera y manual_notes. El concepto debe tener bloque ai:start/end válido (Capa 2) antes de arrancar. Si no lo tiene, se agrega manualmente (NO automáticamente) y se registra en el reporte.

Preparación del entorno (config.pilot.yaml): concept_id = frontend-01-internet-web; backend notebooklm (o fake para dry-run sin red); dry_run_first = true (siempre dry-run antes del run real); keep_history = true (versionar artefactos); strict_validation = true (warnings bloquean en el piloto, calibración); cleanup_notebooks = true; report_markdown = true. Checklist pre-piloto: ai scan → confirmar que frontend-01 aparece con bloque; ai inspect → verificar metadatos; backup del vault (copia completa) y snapshot de workdir/ si existía; verificar credenciales de NotebookLM; confirmar que no hay cambios sin commitear en el vault (git status limpio) para poder comparar.

Ejecución paso a paso (dry-run primero, luego real):
1. Dry-run completo (no escribe en el vault, no cambia estado): ai run frontend-01-internet-web --dry-run --force --strict --verbose.
2. Inspeccionar el diff y la validación antes de escribir: ai inspect ... --show-markdown --show-validation.
3. Run real: ai run frontend-01-internet-web --force --strict.
4. Verificar el resultado: ai inspect ...; ai review ... --show-markdown.

Captura de métricas del piloto (PilotEvidence): integridad del vault (outside_hash_before/after, outside_integrity_ok, markers_count_after, frontmatter_byte_identical, headings_preserved, manual_sections_preserved); pipeline (research_coverage, research_sources_count, research_low_coverage, research_low_sources, synthesis_sections_present, synthesis_unverified_claims, synthesis_cross_links_total, synthesis_broken_links, validation_score, validation_errors, validation_warnings); tiempos (research/synthesis/validation/writing/total en ms); contenido (word_count_by_section, code_fences_count, citations_count, unverified_marked_count). Toda la evidencia se persiste en workdir/pilot/pilot_report.json (más el reporte de la corrida en workdir/reports/).

Reglas del piloto: el piloto se ejecuta siempre con --dry-run primero. Si el dry-run falla (validación con errores), NO se ejecuta el run real hasta corregir. El piloto usa --force para ignorar idempotencia (es la primera corrida real; no hay artefactos previos). El piloto usa --strict (warnings bloquean) para detectar problemas de calibración temprano. El piloto mantiene historial (keep_history: true) para poder comparar versiones si se recalibra. El piloto NO modifica otros conceptos: solo frontend-01-internet-web. Si el piloto falla en cualquier fase, se detiene (no se reintenta automáticamente en modo piloto) para poder inspeccionar. El reintento manual se hace con ai run ... --retry tras corregir.

### Validación de resultados
La validación del piloto tiene dos capas: la automática (Capa 8, ya ejecutada) y la revisión humana (checklist manual). El piloto NO se considera exitoso solo porque is_valid = True; se requiere revisión humana del contenido.

Checklist de validación automática (ya cubierto por Capa 8): validation_score >= 0.85 (17 checks, al menos 15/17 pasando; warnings dentro del umbral); 0 checks de severidad error fallidos; is_valid = True con strict_mode = True.

Checklist de validación manual (revisión humana del contenido): definition_clear, how_it_works_accurate, examples_runnable, common_errors_relevant; foundation_stable, practice_modern, separation_clean; citations_accurate, unverified_justified; cross_links_valid, no_invented_concepts; outside_untouched, frontmatter_untouched, manual_notes_respected; spanish_rioplatense, no_placeholders. El humano revisa el markdown generado (ai review <id> --show-markdown) y completa el checklist. Se persiste en workdir/pilot/manual_review.json.

Integridad del vault (verificación automatizada post-piloto): se compara el backup pre-piloto con el archivo actual. outside hash idéntico, marcadores 1/1, frontmatter byte a byte, headings requeridos presentes (Que abarca, Relacionados). Se genera un IntegrityReport con all_ok.

Reglas de validación de resultados: el piloto se considera "validado" solo cuando: (a) la validación automática pasa en modo estricto, (b) la checklist manual está completa con todos los items en True, y (c) la integridad del vault es 100% (outside hash idéntico, marcadores 1/1, frontmatter byte a byte). Si algún item manual es False, se registra como "hallazgo del piloto" y se decide: corregir el prompt/config (y re-correr) o aceptar como limitación documentada. La validación del piloto NO se salta: no hay "piloto automático". El humano revisa el contenido generado. Los hallazgos se persisten en workdir/pilot/findings.json con severidad (bloqueante / no bloqueante) para alimentar la calibración.

### Calibración de parámetros
A partir de los hallazgos del piloto se ajustan los parámetros que controlan calidad, costo y estabilidad. La calibración se hace en dos niveles: (a) parámetros de validación (umbrales de calidad) y (b) parámetros operativos (pacing, timeouts, concurrencia).

Parámetros a calibrar (con valores iniciales y rango): trace_threshold (0.6), min_words por sección, max_warnings_before_block (5), strict_mode_pilot (True, en producción False); coverage_threshold (0.7), max_sources (12), min_sources (4), max_questions_per_concept (12), freshness_window_days (stable 90, semi_stable 30, dynamic 7); max_concurrent_notebooks (2), timeouts por operación (create_notebook 30, add_source 60, research 120, generate_report 180, download 60, delete 30); max_retries (3), backoff_seconds [2,4,8], pacing_between_concepts_s (1.0), circuit_breaker_threshold (5), circuit_breaker_cooldown_s (60).

Método de calibración: si la trazabilidad (citas) quedó por debajo del umbral pero el contenido es bueno → bajar trace_threshold o mejorar el prompt (preferir mejorar el prompt). Si alguna sección quedó corta (V_CONTENT_MIN_LENGTH warning) → ajustar min_words a lo observado. Si la cobertura de investigación fue baja (low_coverage) pero el contenido es bueno → bajar coverage_threshold o mejorar queries. Si hubo timeouts o rate limits → subir timeouts / bajar concurrencia / subir pacing. Si el tiempo total del piloto fue alto (> 5 min por concepto) → reducir max_sources / max_questions_per_concept. Si strict_mode bloqueó por warnings que son aceptables → desactivar strict en producción.

Versionado de config (piloto vs producción): config/config.yaml (producción, valores calibrados tras el piloto); config/config.pilot.yaml (piloto: strict, keep_history, dry_run_first); config/config.pilot.calibrated.yaml (resultado de la calibración, para comparar).

Reglas: la calibración produce un config.pilot.calibrated.yaml con los valores ajustados. El humano revisa el diff (diff config.yaml config.pilot.calibrated.yaml) y decide qué aplicar a config.yaml. NUNCA se aplica la calibración automáticamente a config.yaml: requiere revisión humana y commit en git (los prompts/config son código versionado). Cada ajuste lleva reason y se persiste en workdir/pilot/calibration.json para auditoría. Si un parámetro se ajusta, se re-corre el piloto (ai run frontend-01-internet-web --force --config config.pilot.calibrated.yaml) para verificar que el ajuste no rompe nada (regresión). Iterar: calibrar → re-correr piloto → validar. Máximo 3 iteraciones antes de escalar (si no converge, escalar con los valores por defecto y seguir calibrando en el lote).

### Criterios de aceptación para escalar
El piloto debe cumplir TODOS los criterios (gate de escalamiento) antes de pasar al frontend completo. Si alguno falla, NO se escala: se corrige y se re-corre el piloto.

Criterios de integridad (bloqueantes): vault_integrity_100 (outside hash idéntico, marcadores 1/1, frontmatter byte a byte), zero_data_loss (ningún archivo del vault modificado fuera del bloque), backup_restore_tested (se probó restaurar un backup y queda idéntico).

Criterios de validación automática: validation_strict_pass (is_valid=True con strict_mode=True en el piloto), validation_score_min (>= 0.85), zero_error_checks (0 checks de severidad error fallidos).

Criterios de calidad de contenido (revisión humana): manual_review_complete (checklist manual 100% True), no_hallazgos_bloqueantes (sin hallazgos de severidad "bloqueante" en findings), citations_verified (las citas [src-N] fueron verificadas por el humano).

Criterios de pipeline/operación: idempotency_verified (re-correr el piloto sin --force NO re-procesa, salta por frescura), resume_verified (cortar a mitad y reanudar produce el mismo resultado), dry_run_matches_real (el diff del dry-run coincide con la escritura real).

Criterios de performance: duration_per_concept_acceptable (tiempo por concepto dentro del presupuesto, ej. < 5 min), no_backend_timeouts (0 timeouts en el piloto, o timeouts manejados sin fallo).

Criterios de configuración: calibration_applied (config calibrada y commiteada en git), prompts_versioned (prompts usados versionados en git, hash trazable).

Verificaciones auxiliares del gate: verify_idempotency (re-correr sin --force: el runner debe saltar, status skipped); verify_resume (resetear a "researching" sin borrar artefactos, cortar a mitad con --stop-after synthesizing, reanudar → mismo resultado final); verify_dry_run_match (el diff del dry-run debe coincidir byte a byte con la escritura real); test_restore (forzar un fallo de verificación y verificar que el backup se restaure; se hace en un concepto de prueba o en dry-run, NUNCA en el concepto piloto real sin backup).

Reglas del gate de escalamiento: el gate es binario: TODOS los criterios deben ser True. Un solo False → NO-GO. Los criterios de integridad (vault_integrity_100, zero_data_loss) son bloqueantes absolutos: si fallan, NO se escala bajo ninguna circunstancia, y se investiga la causa (bug en el writer). Los criterios de validación (validation_strict_pass, zero_error_checks) son bloqueantes. Los criterios de calidad de contenido (manual_review_complete, no_hallazgos_bloqueantes) son bloqueantes: el humano debe revisar y aprobar. Los criterios de pipeline (idempotency_verified, resume_verified, dry_run_matches_real) son bloqueantes: si la idempotencia o el resume fallan, el sistema no es confiable para 255 conceptos. Los criterios de performance (duration_per_concept_acceptable) son NO bloqueantes por sí solos: si un concepto tarda más de lo esperado, se escala igual pero con pacing ajustado y monitoreo. Se registra como riesgo. Los criterios de configuración (calibration_applied, prompts_versioned) son bloqueantes: no se escala con config sin versionar (no se puede reproducir ni auditar). La decisión GO/NO-GO se persiste en workdir/pilot/scaling_decision.json con la lista de criterios fallidos y sus razones.

### Plan de escalamiento (frontend completo, luego otras áreas)
El escalamiento se hace en fases incrementales, no de golpe sobre los 255 conceptos. Cada fase tiene su propio mini-gate antes de pasar a la siguiente.

Fase A — Frontend completo (conceptos frontend-01 ... frontend-NN): scope frontend-*, order numeric, pacing 2.0s, strict False, gate: min_success_rate 0.90, max_blocked_rate 0.05, max_failed_rate 0.10, max_avg_duration_ms 300000, required_manual_review_sample 0.10 (revisar manualmente el 10% de los done). Ejecución: ai scan --area frontend; dry-run sobre los primeros 3 conceptos (smoke test post-piloto); run real del frontend completo (ai run-batch --area frontend --concept-order numeric --pacing 2.0); monitoreo (ai status --area frontend --failed --blocked --low); revisión de bloqueados/fallidos (ai review --area frontend); reporte final (ai report --last --md --out ...). Mini-gate Fase A: success_rate >= 0.90, blocked_rate <= 0.05, failed_rate <= 0.10 (los failed son reintentables; se reintenta con --retry-failed), revisión manual del 10% de los conceptos done con el checklist manual (si la muestra tiene hallazgos bloqueantes → NO-GO), tiempo promedio por concepto dentro del presupuesto, 0 problemas de integridad del vault (outside hash en todos los done), notebooks huerfanos <= 5%.

Fase B — Backend (backend-*): área cercana (APIs, servidores); prompts similares. Se reutiliza la calibración del frontend con ajustes menores (area_domains, ejemplos en Python/Node).

Fase C — Data (data-*): área más distinta (pipelines, ML, SQL); requiere revisar los prompts de contexto data y posiblemente ajustar min_words (ejemplos con SQL/Python).

Fase D — Infra (infra-*): área con más contenido de comandos/config (Docker, K8s); revisar prompts infra y code fences (bash/yaml).

Entre fases: al terminar cada fase, generar el reporte (ai report --last) y revisar bloqueados/fallidos/baja cobertura. Reintentar los failed con --retry-failed antes de pasar a la siguiente fase. Los blocked (validación por warnings/umbral) se revisan manualmente; si son sistemáticos (mismo check fallando en muchos), se recalibra el umbral o el prompt y se re-corre la fase. Si una fase tiene success_rate < 0.80 → STOP: no pasar a la siguiente área. Investigar la causa (prompts, fuentes, timeouts) y re-calibrar.

Fase E — Lote completo (255 conceptos) (opcional, tras Fases A-D): scope toda la cola (sin filtro de area), order numeric, pacing 2.0s, strict False, gate: min_success_rate 0.95, max_blocked_rate 0.02, max_failed_rate 0.05. Se ejecuta preferentemente en horario de baja carga (NotebookLM tiene límites de cuenta). Monitoreo en tiempo real con ai status --watch (refresca cada 30s). Si el lote se interrumpe (Ctrl+C), el runner persiste estado y genera reporte parcial. Se reanuda con ai run-batch --retry-failed (los done se saltan).

Cronograma sugerido: semana 1 implementar Capas 1-10 (ya hecho) y preparar entorno de piloto; semana 2 ejecutar piloto (dry-run + real) sobre frontend-01, revisión manual; semana 3 calibración (iterar hasta 3 veces), gate de escalamiento; semana 4 Fase A frontend completo, revisión de muestra; semana 5 Fase B backend, recalibración si es necesario; semana 6 Fase C data; semana 7 Fase D infra; semana 8 Fase E lote completo (si todas las fases pasaron sus gates); semana 9+ revisión final, limpieza de notebooks huerfanos, reporte consolidado.

Reglas del plan de escalamiento: NO se escala al lote completo sin pasar el gate de escalamiento del piloto. Cada fase de área tiene su mini-gate; si falla, se detiene y recalibra (no se salta a la siguiente área). El escalamiento es incremental y reversible: si una fase sale mal, los conceptos done ya escritos permanecen (son válidos), y los failed/blocked se reintentan. No se revierte el vault. El pacing se ajusta por fase según la calibración (default 2s entre conceptos; puede subir si hay rate limits). El monitoreo es continuo: ai status + reportes por fase. Los hallazgos sistemáticos (mismo check fallando en muchos conceptos) indican un problema de prompt/config, no de contenido individual → recalibrar y re-correr la fase afectada. Los notebooks huerfanos se limpian al final de cada fase (manual o con un script de limpieza que liste orphan_notebooks del reporte). La decisión de escalar a la siguiente fase se documenta (commit en git del scaling_decision.json o anotación en el reporte) para trazabilidad.

### Reglas de negocio (de la spec)
- El piloto se ejecuta sobre un único concepto (frontend-01-internet-web) con dry-run primero y run real después, siempre con --strict para detectar problemas de calibración.
- El piloto requiere revisión humana del contenido (checklist manual) además de la validación automática (Capa 8). No es suficiente is_valid = True.
- La integridad del vault se verifica byte a byte (outside hash, marcadores, frontmatter) antes y después del piloto. Cualquier diferencia es bloqueante.
- La calibración ajusta parámetros de validación, investigación, backend y orquestador a partir de los hallazgos del piloto. Cada ajuste lleva reason y se persiste para auditoría.
- La calibración NO se aplica automáticamente a config.yaml: requiere revisión humana y commit en git.
- El gate de escalamiento es binario: TODOS los criterios deben pasar. Un solo fallo → NO-GO.
- El escalamiento es incremental por área: frontend → backend → data → infra → lote completo. Cada fase tiene mini-gate; si falla, se detiene y recalibra.
- La idempotencia y el resume se verifican explícitamente en el piloto (re-correr sin --force salta; cortar y reanudar produce el mismo resultado).
- El dry-run debe coincidir byte a byte con la escritura real (verificación de que el writer es determinista).
- Los notebooks huerfanos se reportan y se limpian al final de cada fase.
- El piloto y la calibración son la última capa: no agregan lógica de negocio nueva, solo orquestan, miden y deciden si el sistema está listo para escalar.
