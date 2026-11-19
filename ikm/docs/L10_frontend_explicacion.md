# Explicacion del codigo — v2 Capa L10: frontend navegable (20a) + cliente de chat (20b)

> Documento educativo. Explica, con palabras, qué es la **capa L10** de IT Knowledge Map v2, cómo se implementó el sitio navegable sin backend (Entrega 1) y el cliente de chat (Entrega 3), y por qué se tomó cada decisión. No copia bloques de código: solo referencia módulos y funciones clave.
>
> Proyecto: `C:\Users\DGVit\Proyectos\IT Career\ikm\web\` · Rama: `v2/L10-frontend`.
> Diseño de referencia: `diseno-tecnico-pipeline-v3.md` §15 (Frontend y visualización), §6.6 (estado de exploración), Apéndice A (orden de entregas).
> Skill de capa: `.opencode/skills/ikm-v2-layer-coder` (checklist Frontend L4).

---

## 1. Que es L10 y que resuelve

L10 es la **cara visible** del Knowledge Map: el sitio que el lector usa para interactuar con los 255 conceptos, sus relaciones y el Development Journey. El objetivo de negocio de v2 es exactamente este: *exponer la funcionalidad de manera robusta, fluida y bien implementada*. El chatbot es una vía adicional, no el centro.

La capa se divide en dos cortes, siguiendo el Apéndice A:

- **20a — Frontend navegable sin backend (Entrega 1, primer corte publicable).** Presentación, Knowledge Base por área, fichas de concepto, grafo 2D, relaciones con su explicación `quoted`, vistas de vecindad y camino, estado de exploración. **Consume SOLO el release estático**: no depende de la API. Esto es lo que se puede probar hoy sin levantar ningún servidor de backend.
- **20b — Cliente de chat (Entrega 3).** Cliente de la API de chat, con etiquetas de procedencia y estados explícitos (disponible / degradado / no-disponible). Cuando el backend no está, el sitio sigue siendo navegable y el chat lo dice honestamente.

### El principio rector: el release es la única fuente de datos

Toda la navegación sale de archivos JSON estáticos e inmutables que el pipeline (C0–C9) publica en `workdir/releases/<release_id>/`. El frontend los copia a `web/public/release/` con `npm run sync:release` y los sirve como assets. No hay base de datos, no hay fetch a una API para navegar. Esto cumple §15.2 (*"Al iniciar: release.json, areas.json, graph.json; bajo demanda: concepto, relations.json, índice de búsqueda"*) y garantiza que el sitio funcione offline y sin backend.

---

## 2. La base de contenido que hizo falta (y por qué es 100% reutilizable)

Antes del frontend, el release estaba **incompleto**: C9 escribía solo `manifest.json` y referenciaba `graph.json`/`chunks.json` que nunca copiaba al directorio del release. Los conceptos no tenían área asignada (`area_uid: null`) y el layout del grafo amontonaba los nodos. Sin un release autocontenido y legible, no hay frontend posible. Se corrigió el plano de contenido con cambios quirúrgicos que benefician a **todas** las capas posteriores (frontend, backend loader, publicación):

| Archivo | Cambio | Por qué es reusable |
|---|---|---|
| `content/package.py` | C9 ahora escribe cada payload de forma atómica y verifica el hash **contra los bytes reales en disco** (fail-closed). `escribir_archivos_release`, `empaquetar(release_dir=...)`, `calcular_release_id`. | El backend (`api/release/loader`) y cualquier publicación consumen un release con hashes verificables. |
| `content/release_files.py` | Armado puro de `release.json` (bootstrap), `areas.json`, `graph.json` (nodos+aristas con uid de relación), y la ficha `concepts/<uid>.json`. Serialización canónica. | Una sola definición de la forma del release para todos los consumidores. |
| `content/areas_catalog.py` | Mapeo directorio del vault → área (uid = slug, orden, color_token). `area_uid_por_ruta`. | Áreas reales para grafo, badges, filtros y conteos. |
| `content/derivados.py` | Layout del grafo **phyllotaxis por área** (ángulo áureo, radio ~√i), determinista. Antes: círculo apretado. | Posiciones legibles precalculadas que el frontend dibuja sin coste de layout. |
| `content/release_build.py` | Encadena C0–C9 asignando área real, slug con `slugify`, y empaqueta los 262 archivos verificados. | El comando `release build` produce el release completo que el frontend sincroniza. |
| `contracts/generate.py` | Los tipos TS generados ahora **importan** los tipos que referencian (cada archivo es un módulo). Antes: nombres desnudos que no compilaban. | Cualquier consumidor TS (frontend, futuro SDK) puede importar los contratos. |

El release resultante (`2026-11-19-77912eef`): **255 conceptos, 913 relaciones (todas con explicación quoted), 2295 chunks, 10 áreas, 262 archivos** con hash verificado. Idempotente: rebuild → mismo `release_id`. La compuerta C7 sigue en PASSED y el vault intacto.

---

## 3. Stack y decisiones de arquitectura

| Decisión | Elección | Referencia |
|---|---|---|
| Framework | React 18 + Vite 5 + TypeScript 5 (strict) | §15.1, skill L4 |
| Estilos | Tailwind 3 con **tokens CSS** (dark-first, paleta por área) | DR-L10-03 |
| Routing | React Router 6, rutas de §15.2 | §15.2 |
| Datos | TanStack Query 5, `staleTime: Infinity` (release inmutable) | §15.1 |
| Animaciones | Framer Motion, `MotionConfig reducedMotion="user"` | §15.5 |
| Grafo | **Canvas 2D propio**, sin librería de grafos | DR-L10-02 |
| Markdown | react-markdown + remark-gfm (sin HTML crudo), carga diferida | seguridad |
| Tipos | Importados de `contracts/generated/ts` (fuente única) | skill L4 |
| Tests | Vitest + Testing Library (jsdom) | skill testing |

**DR-L10-02 (grafo 2D canvas, no Three.js para Entrega 1).** §15.3 permite decidir 2D vs 3D por utilidad/rendimiento. Se eligió canvas 2D propio: 255 nodos / 913 aristas se dibujan a ≥30 fps sin dependencias pesadas, con posiciones precalculadas del release. Three.js queda como exploración opcional futura (no bloquea entregas 1–3). El canvas resuelve sus colores desde los tokens CSS (canvas no lee variables CSS directamente), así que adapta su paleta al tema claro/oscuro.

**DR-L10-03 (tokens de diseño).** `styles/tokens.css` define variables RGB para base/surface/ink/muted/accent en `:root` (claro) y `.dark` (oscuro), más una variable por área (`--area-<slug>`). Tailwind las consume con alpha. El tema se persiste en localStorage y se aplica antes del primer paint (script en `index.html`) para evitar FOUC.

---

## 4. La capa de datos (`web/src/lib/`)

| Módulo | Responsabilidad |
|---|---|
| `types.ts` | Tipos del release; extienden los contratos `Concept`/`Relation` de L0. |
| `release.tsx` | `ReleaseProvider` carga los 4 archivos de arranque y los indexa (`byUid`, `byArea`, `areaByUid`). Hooks `useConcept`, `useRelations`, `useClientIndex` bajo demanda. Falla con pantalla de error + reintento si el release no está. |
| `search.ts` | Índice invertido liviano sobre títulos + chunks. Scoring título > cuerpo, tolerante a tildes (`normalizeText`), AND suave, snippet contextual. Determinista y testeable sin DOM. |
| `graph.ts` | `buildAdjacency`, `neighborsOf`, `shortestPath` (BFS), `subgraphAround` (vecindad), `edgesAlongPath`. Puras, vecinos ordenados por uid. |
| `exploration.ts` | `ExplorationState` v1 serializable en **IndexedDB** (§15.4/§6.6). `appendView` (dedupe + cap 50), `pruneUnknown` (descarta uids que ya no existen). Degradación a memoria si no hay IndexedDB. |
| `useExploration.tsx` | Contexto + `useRecordView` para registrar vistas; las del chat llevan `origin: 'chat'`. |
| `wikilinks.ts` | Parseo de `[[...]]`, resolución contra el release (`resolveWikiTarget`), conversión a links `ikm://`, limpieza de explicaciones quoted (`cleanExplanationText`). |
| `format.ts` | Etiquetas de sección, `canonicalSectionKey` (heading humano → clave canónica), colores por área, etiquetas de marcas y tipos de relación. |
| `api.ts` | Cliente de chat: `probeChatAvailability` (sondea `/health`), `sendChat` (parsea `blocks[].text` + `basis` del orquestador real), etiquetas de procedencia. |
| `theme.ts` | Hook de tema dark/light persistido. |

**Detalle de integridad:** las marcas de verificación (`sin verificar` / `⚠️ verificar`) se conservan y se muestran por sección. Como el vault guarda el heading humano ("Estado actual") y el contrato usa snake_case ("estado_actual"), `canonicalSectionKey` normaliza tildes y sufijos para que el badge aparezca en la sección correcta. Nunca se eliminan las marcas: son señales de integridad, no ruido.

---

## 5. Las vistas (`web/src/routes/`)

| Ruta | Vista | Qué hace |
|---|---|---|
| `/` | `Home` | Hero, métricas del release, grilla de áreas, "cómo leer el mapa". |
| `/kb` | `KbIndex` | Áreas + listado completo filtrable por título. |
| `/kb/:area` | `KbArea` | Conceptos del área en orden del vault, filtro, marcas. |
| `/kb/c/:uid/:slug` | `Concept` | Ficha: 10 secciones con markdown, marcas por sección, relaciones quoted, fuentes, prev/next, "ver en el grafo". Redirige al slug canónico. |
| `/graph` | `GraphPage` | Grafo completo: canvas, filtro por área, modo camino, panel de selección, lista accesible por teclado. |
| `/graph/view/:uid` | `GraphPage` | Vista contextual: vecindad del concepto (subgrafo profundidad 1). |
| `/chat` | `Chat` | Cliente de chat con estados y procedencia. |
| `/journey`, `/journey/r/:uid/:slug` | `Journey`, `JourneyRecord` | Estado honesto: 0 registros curados en este release. |
| `/tours/:id` | `Tours` | Diferido: recorridos guiados aún no publicados. |
| `/privacy` | `Privacy` | Sin cuentas, sin tracking, exploración en IndexedDB local. |
| `*` | `NotFound` | 404 con vuelta al inicio. |

Las vistas simples se codifican en la URL (§15.2): `?focus=<uid>` (selección), `?area=<slug>` (filtro), `?from=&to=` (camino). Grafo, ficha y chat se cargan de forma diferida (`React.lazy`) para no pesar en el arranque.

---

## 6. El grafo 2D (`web/src/components/GraphCanvas.tsx`)

Componente canvas con cámara propia (pan/zoom), hit-testing de nodos y aristas, y dibujo por frames. Puntos clave:

- **Rendimiento:** loop `requestAnimationFrame` que dibuja solo cuando hay cambios o animación de cámara. 255 nodos / 913 aristas muy por debajo del presupuesto de 30 fps.
- **Primer paint síncrono:** un `useLayoutEffect` mide, encuadra y dibuja al montar, sin depender de rAF (las pestañas en background lo throttlean). El tamaño también se auto-verifica en cada frame (self-healing) por si `ResizeObserver` llega tarde.
- **Labels solo en hover, selección y vecinos** (criterio §15.3), no en todos los nodos.
- **Accesibilidad (§15.5):** el canvas es focable y responde a flechas (pan), +/− (zoom), 0 (encuadrar), Esc (deseleccionar). Además hay una **lista de conceptos paralela** (plegable) para navegar por teclado sin canvas, y chips de vecinos en el panel.
- **`prefers-reduced-motion`:** sin animaciones de cámara (salto directo). Las transiciones de ruta también se reducen con `MotionConfig`.
- **Modo camino:** `shortestPath` (BFS) resalta nodos y aristas del camino sobre el grafo atenuado, con panel de pasos.
- **Tema:** la paleta se resuelve desde los tokens CSS y se refresca con un `MutationObserver` sobre la clase `dark` del `<html>`.

---

## 7. Verificacion

| Criterio | Resultado |
|---|---|
| Tests unitarios (Vitest) | **43 passed** (search, graph, exploration, wikilinks, format, rutas estáticas). |
| Build de producción (`tsc && vite build`) | Verde, sin errores de tipos. |
| JS inicial comprimido (§15.5 < 250 KB) | **117.86 KB gz** (+ 6.64 KB CSS). Grafo 7.72 KB, ficha 54 KB, chat 2.98 KB, diferidos. |
| Release | 262 archivos, hashes verificados contra disco, idempotente. |
| Navegación real (browser, laptop 2 → laptop 1) | Home, grafo (selección/vecindad/camino), ficha (10 secciones + marcas), palette Ctrl+K (búsqueda full-text), chat en vivo contra backend, temas claro/oscuro, responsive mobile. |
| `prefers-reduced-motion` / teclado | Respetado; lista accesible y foco visible. |

**Cómo probarlo hoy:** el dev server corre en laptop 1 (`http://192.168.0.107:5173/`, vite en 0.0.0.0). El backend stub de chat en `127.0.0.1:8000` (proxy de Vite). Para levantar todo de cero: `npm run sync:release` → `npm run dev` (frontend) y `py -m uvicorn ikm.api.main:app --port 8000` (chat, opcional).

---

## 8. Pendiente (no bloquea la Entrega 1)

- **Journey (C5/C6):** 0 registros curados. Las vistas existen y muestran estado honesto; el contenido lo cura el autor.
- **Chat con LLM real:** el backend actual es un stub (echo). El cliente ya parsea la forma real (`blocks` + `basis`) y etiqueta procedencia; la integración con Groq/retrieval/verify es trabajo de backend (Entrega 3).
- **Tours y grafo 3D:** diferidos por condición (§15.3, Apéndice A).
- **Publicación:** el release está en `workdir/` (gitignored). Publicar a `releases/` requiere la compuerta + revisión humana del diff (C7/C9, L11).