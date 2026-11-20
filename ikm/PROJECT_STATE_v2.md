# PROJECT_STATE_v2 — IT Knowledge Map v2

> Estado compartido entre sesiones. **Leer esto primero.** El plan vive en disco, no en la memoria del chat.

**Proyecto:** `C:\Users\DGVit\Proyectos\IT Career\ikm\`
**Rama actual:** `v2/L10-frontend` (frontend navegable + base de release).
**Servidor OpenCode (laptop 1):** `http://192.168.0.107:26826` · Basic `opencode:<password>` (password en `C:\Users\DGVit\Proyectos\run_opencode*.bat`, NUNCA en chat/docs).
**Sitio navegable (dev, laptop 1):** `http://192.168.0.107:5173/` · backend chat stub `127.0.0.1:8000`.

---

## Capa en curso

**L10b — Grafo 3D + puente chat↔grafo + dedup: IMPLEMENTADA Y VERIFICADA.** Encima de L10 (frontend navegable + chat cliente). El grafo ahora es 3D (client-side), el chat activa relaciones en el grafo, y las conexiones duplicadas se canonicalizaron (913→472). **L10c (corrección):** el 2D ahora es como el graph view de Obsidian (layout de fuerzas en vivo + jerarquía por grado + nodos arrastrables). Pendiente de confirmación del usuario para publicar.

## Qué está hecho

- **L0 — Contratos (completa).** `ikm/contracts/` + 23 JSON Schema + 38 TS generados. **Fix L10:** los TS ahora importan los tipos que referencian (`generate.py`, DR-L10-04) — antes no compilaban como módulos.
- **L1 — Inventario y parseo (completa).** `content/inventory.py` (C0), `parse.py` (C1). 255 notas, 10 secciones, vault intacto.
- **L2–L4 — Identidad, grafo, relaciones, gate, derivados, release (plano de contenido C2–C9).** Implementado por OpenCode (sin commitear hasta esta sesión). **Base L10:** release ahora autocontenido y verificado (ver abajo).
- **L10 — Frontend (completa, verificada).** `ikm/web/`:
  - Stack: React 18 + Vite 5 + TS strict + Tailwind (tokens dark-first) + React Router 6 + TanStack Query 5 + Framer Motion.
  - Vistas: Home, KB por área, ficha de concepto (10 secciones + marcas + relaciones quoted), grafo 2D canvas (selección/vecindad/camino BFS/filtro por área/teclado), chat cliente (estados + procedencia), Journey/Tours/Privacy/NotFound honestos.
  - Capa de datos: cliente del release estático, búsqueda full-text cliente, grafo (BFS/vecinos), ExplorationState en IndexedDB, wikilinks, contratos TS.
  - Command palette Ctrl+K, temas claro/oscuro, responsive, `prefers-reduced-motion`.
  - **52 tests Vitest passing · build verde · JS inicial 120.30 KB gz (< 250 KB, §15.5).**
  - Explicación: `ikm/docs/L10_frontend_explicacion.md` (+ copia en `OneDrive\Escritorio`). Decisiones: `ikm/docs/decisions/DR-L10-frontend.md`.
- **L10b — Grafo 3D, chat↔grafo, dedup, motion (completa, verificada).**
  - L-data: dedup de relaciones recíprocas por par no ordenado (`content/relations.py::colapsar_reciprocas`), conserva tipo tipado y explicación quoted. 913 aristas dirigidas → 472 únicas. 7 tests.
  - L-3d: grafo 3D Three.js vanilla + d3-force-3d client-side (`src/components/Graph3D.tsx`, `src/lib/forceLayout.ts`). InstancedMesh + CSS2D labels + bloom neón. Lazy (~140 KB gz). Toggle 2D/3D por URL. Modos: selección, vecindad, camino encuadrado, multi-área. Auto-rotación idle.
  - L-chat-graph: puente chat↔grafo (`src/lib/chatBridge.ts`): entity linking contra el release → acción de grafo. Vista split en /chat; "Frontend y Backend" resalta esas conexiones. Funciona con backend stub. 9 tests.
  - L-ui: count-up en métricas, aurora en hero, auto-rotación idle. Todo con prefers-reduced-motion.
  - Explicación: `ikm/docs/L10b_grafo3d_chat_explicacion.md` (+ copia en Escritorio). Decisiones: `ikm/docs/decisions/DR-L10b-grafo3d-chat.md`.
- **L10c — Grafo 2D como Obsidian (corrección, verificada).** `GraphCanvas.tsx` reescrito: layout de fuerzas d3-force 2D en vivo (reutiliza d3-force-3d), jerarquía por grado (`nodeR=3+sqrt(grado)*2.8`), nodos arrastrables (fx/fy + reheat), foco al hover/selección, labels con text-fade por zoom, sin halos de área. Reemplaza el phyllotaxis fijo. Modos L10b siguen funcionando. DR-L10c + §9 en el doc L10b.
- **L10d — Jerarquía por área: cada área con su cabeza (corrección, verificada).** `computeHeads` (forceLayout.ts) elige la cabeza de cada área = mayor grado (data-driven, sin inventar nodos/relaciones). Cabeza fija en el centroide, miembros orbitándola (gravedad 0.25, links débiles 0.06), cabezas realzadas (radio ×2.1+10 en 3D, anillo en 2D, label fijo bold accent, cabeza global en accent). Spokes visibles, inter-área tenues. 2D y 3D. 6 tests nuevos (58 total). DR-L10d + §10 en el doc L10b.
- **L11 — Modo Obsidian: mind-map del vault con raíz y color editable (verificada).** Segundo modo de vista (toggle Obsidian/Mapa, `?mode=obsidian`). `buildObsidianGraph` (obsidianGraph.ts) replica la jerarquía del vault IT-Mind-Map: raíz "Mercado IT" (grado ~265, gigante al centro) + 10 cabezas de área (nombre del área, medianas) + 255 conceptos hoja + enlaces jerárquicos (raíz→área, raíz→concepto, área→concepto) + 472 relaciones reales = 266 nodos / 992 enlaces. Color uniforme editable (obsidianColors.ts + ObsidianColors.tsx, global + por área, localStorage). 2D replica la imagen de referencia; 3D con bloom reducido. Modo mapa L10d intacto. 6 tests nuevos (64 total). DR-L11 + §11 en el doc L10b.

## Base de release corregida en L10 (100% reutilizable)

El release estaba incompleto (C9 solo escribía manifest). Se corrigió el plano de contenido:
- `content/package.py`: C9 escribe cada payload atómico + verifica hash contra disco (fail-closed).
- `content/release_files.py`: arma release.json, areas.json, graph.json, concepts/<uid>.json, relations.json, client-index.json, chunks.json, graph-positions.json.
- `content/areas_catalog.py`: áreas reales (uid=slug, orden, color_token).
- `content/derivados.py`: layout phyllotaxis por área (determinista, legible).
- `content/release_build.py`: encadena C0–C9 con área real y slug canónico.

**Release vigente `2026-11-19-95e94e92` (post-dedup L-data): 255 conceptos · 472 relaciones únicas (todas quoted) · 2295 chunks · 10 áreas · archivos verificados.** Idempotente. Gate C7 PASSED, vault intacto. (El release L10 previo `77912eef` tenía 913 aristas dirigidas con reciprocidad duplicada.)

## Datos del vault (relevamiento)

- 266 `.md`: 255 conceptos + 11 índices (excluidos). 255 notas con las 10 secciones.
- 913 links dirigidos en `Relacionados` (cada relación aparece en ambas fichas) → 472 pares únicos tras dedup. Todas con explicación quoted; 14 tipificadas.
- 37 marcas de verificación. Títulos duplicados reales (p.ej. "HTTP" en backend y networking, "routing" ×3) — el grafo los distingue por uid/área.

## Qué falta (orden de entregas, Apéndice A)

1. **Confirmar L10 con el usuario** y publicar el release (C7 gate + revisión humana del diff → `releases/`, L11).
2. **Entrega 2 — Journey (C5/C6):** curar registros del material crudo (`OneDrive\Escritorio/IT Career - Documentacion del dia` + `docs/`). El autor aprueba; el pipeline no escribe Journey solo. Vistas frontend ya listas (estado honesto con 0 registros).
3. **Entrega 3 — Chat con LLM real:** el backend actual es stub (echo). Falta auth, limits, retrieval (BM25 ya funcional), verify, adaptador Groq, orquestador. El cliente frontend ya parsea la forma real (`blocks`+`basis`) y etiqueta procedencia.
4. **Entrega 4 — Eval/CI/operación (L11):** reglas duras 100%, recall@8, publicación tras revisión humana.
5. **Diferidos por condición:** tours guiados, embeddings (el grafo 3D de §15.3 ya está implementado en L10b).

## Cómo reanudar (checklist)

1. Cargar skills `opencode-remote` + `it-career-pipeline` (+ `.opencode/skills/ikm-v2-layer-coder` del proyecto).
2. Verificar `GET /api/info` (password desde los launchers locales).
3. Leer `ikm/PROJECT_STATE_v2.md` (este archivo) + la explicación de la capa anterior.
4. Frontend: `cd ikm/web; npm run sync:release; npm run dev` (dev server en 0.0.0.0:5173). Tests: `npm test`. Build: `npm run build`.
5. Release: `py -m ikm.content.cli release build` (PYTHONPATH=raíz del proyecto). Regenerar TS: `py ikm/_regen_ts.py`.
6. Backend chat (opcional): `py -m uvicorn ikm.api.main:app --port 8000`.
7. **No avanzar de capa sin confirmar con el usuario.**

## Reglas operativas (recordatorio)

- Vault `IT-Mind-Map/` solo lectura. No modificar código v1 (`it-concept-map/`) sin orden.
- Git: commit local por capa; **push solo con confirmación del usuario** (dry-run primero).
- HTTP API de OpenCode, no CLI/TUI (0 tokens). Hermes genera el código; la API lo escribe en laptop 1.
- Windows: `;` no `&&`; `py` no `python`; venv `.venv/Scripts/python.exe` si existe; URL-encode completo del path.
- El output de `/api/shell` es UTF-8 (`errors='replace'`); si sale mojibake CJK, re-codificar a UTF-16LE.
- Procesos largos: detach con `Start-Process` + PID file + log; matar instancias previas antes de relanzar.

## Nota de atribución

El plano de contenido C2–C9 y el plano de servicio `api/`/`eval/` fueron implementados por OpenCode en sesiones previas (estaban sin commitear). Esta sesión (Hermes) implementó **L10 frontend**, la **base de release** (C9 autocontenido, áreas, layout, imports TS) y **L10b** (dedup de relaciones, grafo 3D client-side, puente chat↔grafo, motion), y commiteó el conjunto v2 funcional en `v2/L10-frontend` para preservarlo. Sin push.

## Deploy público (Netlify) — 2026-11-19
- Sitio: https://it-knowledge-map-v2.netlify.app (siteId 59f9bd3c-f52a-43ba-a5b7-fc34da3bfa7b, público sin SSO).
- Frontend L10–L11 + fix labels + calidad 3D (MSAA/HDR) deployado. Build autocontenido (contratos vendorizados en src/contracts, release versionado).
- Rama v2/L10-frontend con commits hasta 49bddc8. Push a GitHub pendiente de confirmación de Dan (dry-run: rama nueva, seguro).
- Tests frontend 64/64. JS inicial ~120 KB gz, chunk 3D lazy ~131 KB gz.
