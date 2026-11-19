# Decisiones de diseño — Capa L10 (frontend)

Registros de decisión de la capa L10 (frontend navegable + cliente de chat). Formato: contexto → decisión → consecuencia.

## DR-L10-01 — uid de área = slug del catálogo
- **Contexto:** el release no tenía `area_uid` (todo `null`). El vault tiene un directorio por área (`01 - Software Engineering` … `10 - Project Management`) y `ikm/areas/*.yaml` define el framing.
- **Decisión:** el uid de área es el slug legible (`software-engineering`, `networking`, …), con `order` del prefijo numérico y `color_token` = slug. Mapeo en `content/areas_catalog.py`.
- **Consecuencia:** grafo, badges, filtros y conteos usan áreas reales. El frontend resuelve el color desde `--area-<slug>`. Estable y legible, no opaco.

## DR-L10-02 — Grafo 2D en canvas propio (no Three.js en Entrega 1)
- **Contexto:** §15.3 pide decidir 2D vs 3D por utilidad, legibilidad, rendimiento y complejidad; el prototipo 3D es opcional y no bloquea entregas 1–3.
- **Decisión:** canvas 2D propio (`GraphCanvas.tsx`) con posiciones precalculadas del release (layout phyllotaxis por área, `content/derivados.py`). Sin librería de grafos.
- **Consecuencia:** 255 nodos / 913 aristas a ≥30 fps, bundle del grafo ~7.7 KB gz, labels solo en hover/selección/vecinos, teclado + lista accesible. Three.js queda como exploración futura.

## DR-L10-03 — Tokens de diseño dark-first con paleta por área
- **Contexto:** el objetivo de v2 es una UI robusta, fluida y bien implementada; se necesita consistencia visual y tema claro/oscuro.
- **Decisión:** variables CSS RGB en `styles/tokens.css` (`:root` claro, `.dark` oscuro) + una variable por área. Tailwind las consume con alpha. Tema persistido en localStorage, aplicado antes del primer paint.
- **Consecuencia:** el canvas resuelve su paleta desde los tokens (MutationObserver sobre la clase `dark`), así que grafo y UI adaptan el tema coherentemente.

## DR-L10-04 — Tipos TS generados como módulos con imports
- **Contexto:** `contracts/generate.py` emitía interfaces con nombres de tipos desnudos (sin import), que no compilaban como módulos ES.
- **Decisión:** cada archivo TS generado importa los tipos que referencia (`import type { X } from './X'`). Regenerado con `ikm/_regen_ts.py`.
- **Consecuencia:** el frontend importa los contratos de L0 como fuente única de tipos; cualquier consumidor TS futuro también. Idempotente.

## DR-L10-05 — Release autocontenido con hashes verificados en disco
- **Contexto:** C9 escribía solo `manifest.json` y referenciaba archivos que no copiaba; el release no era consumible.
- **Decisión:** `content/package.py` escribe cada payload atómicamente y verifica el sha256 contra los bytes reales en disco (fail-closed). `release_files.py` arma `release.json`, `areas.json`, `graph.json`, `concepts/<uid>.json`, `relations.json`, `client-index.json`, `chunks.json`, `graph-positions.json`.
- **Consecuencia:** el frontend (y el backend loader) consumen un release completo y verificable. Rebuild idempotente (mismo `release_id`). 262 archivos.

## DR-L10-06 — El frontend navegable no depende del backend
- **Contexto:** Apéndice A: el sitio navegable sin backend es el primer corte publicable (Entrega 1).
- **Decisión:** toda la navegación sale del release estático (`public/release/`, sincronizado con `npm run sync:release`). El chat (20b) es la única pieza que toca la API, y degrada honestamente a "no disponible" si el backend no está.
- **Consecuencia:** el sitio se prueba hoy sin levantar backend; el chat es una vía adicional, no el centro. Cumple §15.2.

## DR-L10-07 — Búsqueda cliente con índice invertido propio
- **Contexto:** se necesita búsqueda full-text sobre 255 conceptos + 2295 chunks sin backend ni dependencias pesadas.
- **Decisión:** `lib/search.ts` construye un índice invertido liviano (título + cuerpo de chunks), scoring título > cuerpo, normalización de tildes, AND suave, snippet contextual. Determinista.
- **Consecuencia:** búsqueda instantánea en la palette Ctrl+K, testeable sin DOM, sin coste de red tras cargar el client-index.