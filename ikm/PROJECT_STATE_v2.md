# PROJECT_STATE_v2 — IT Knowledge Map v2

> Estado compartido entre sesiones. **Leer esto primero.** El plan vive en disco, no en la memoria del chat.

**Proyecto:** `C:\Users\DGVit\Proyectos\IT Career\ikm\`
**Rama actual:** `v2/L10-frontend` (frontend navegable + base de release).
**Servidor OpenCode (laptop 1):** `http://192.168.0.107:26826` · Basic `opencode:<password>` (password en `C:\Users\DGVit\Proyectos\run_opencode*.bat`, NUNCA en chat/docs).
**Sitio navegable (dev, laptop 1):** `http://192.168.0.107:5173/` · backend chat stub `127.0.0.1:8000`.

---

## Capa en curso

**L10 — Frontend (20a navegable + 20b chat): IMPLEMENTADA Y VERIFICADA.** Entrega 1 (sitio navegable sin backend) lista para probar. Pendiente de confirmación del usuario para avanzar.

## Qué está hecho

- **L0 — Contratos (completa).** `ikm/contracts/` + 23 JSON Schema + 38 TS generados. **Fix L10:** los TS ahora importan los tipos que referencian (`generate.py`, DR-L10-04) — antes no compilaban como módulos.
- **L1 — Inventario y parseo (completa).** `content/inventory.py` (C0), `parse.py` (C1). 255 notas, 10 secciones, vault intacto.
- **L2–L4 — Identidad, grafo, relaciones, gate, derivados, release (plano de contenido C2–C9).** Implementado por OpenCode (sin commitear hasta esta sesión). **Base L10:** release ahora autocontenido y verificado (ver abajo).
- **L10 — Frontend (completa, verificada).** `ikm/web/`:
  - Stack: React 18 + Vite 5 + TS strict + Tailwind (tokens dark-first) + React Router 6 + TanStack Query 5 + Framer Motion.
  - Vistas: Home, KB por área, ficha de concepto (10 secciones + marcas + relaciones quoted), grafo 2D canvas (selección/vecindad/camino BFS/filtro por área/teclado), chat cliente (estados + procedencia), Journey/Tours/Privacy/NotFound honestos.
  - Capa de datos: cliente del release estático, búsqueda full-text cliente, grafo (BFS/vecinos), ExplorationState en IndexedDB, wikilinks, contratos TS.
  - Command palette Ctrl+K, temas claro/oscuro, responsive, `prefers-reduced-motion`.
  - **43 tests Vitest passing · build verde · JS inicial 117.86 KB gz (< 250 KB, §15.5).**
  - Explicación: `ikm/docs/L10_frontend_explicacion.md` (+ copia en `OneDrive\Escritorio`). Decisiones: `ikm/docs/decisions/DR-L10-frontend.md`.

## Base de release corregida en L10 (100% reutilizable)

El release estaba incompleto (C9 solo escribía manifest). Se corrigió el plano de contenido:
- `content/package.py`: C9 escribe cada payload atómico + verifica hash contra disco (fail-closed).
- `content/release_files.py`: arma release.json, areas.json, graph.json, concepts/<uid>.json, relations.json, client-index.json, chunks.json, graph-positions.json.
- `content/areas_catalog.py`: áreas reales (uid=slug, orden, color_token).
- `content/derivados.py`: layout phyllotaxis por área (determinista, legible).
- `content/release_build.py`: encadena C0–C9 con área real y slug canónico.

**Release `2026-11-19-77912eef`: 255 conceptos · 913 relaciones (todas quoted) · 2295 chunks · 10 áreas · 262 archivos verificados.** Idempotente (rebuild → mismo id). Gate C7 PASSED, vault intacto.

## Datos del vault (relevamiento)

- 266 `.md`: 255 conceptos + 11 índices (excluidos). 255 notas con las 10 secciones.
- 913 relaciones conceptuales en `Relacionados` (todas con explicación quoted); 14 tipificadas.
- 37 marcas de verificación. Títulos duplicados reales (p.ej. "HTTP" en backend y networking, "routing" ×3) — el grafo los distingue por uid/área.

## Qué falta (orden de entregas, Apéndice A)

1. **Confirmar L10 con el usuario** y publicar el release (C7 gate + revisión humana del diff → `releases/`, L11).
2. **Entrega 2 — Journey (C5/C6):** curar registros del material crudo (`OneDrive\Escritorio/IT Career - Documentacion del dia` + `docs/`). El autor aprueba; el pipeline no escribe Journey solo. Vistas frontend ya listas (estado honesto con 0 registros).
3. **Entrega 3 — Chat con LLM real:** el backend actual es stub (echo). Falta auth, limits, retrieval (BM25 ya funcional), verify, adaptador Groq, orquestador. El cliente frontend ya parsea la forma real (`blocks`+`basis`) y etiqueta procedencia.
4. **Entrega 4 — Eval/CI/operación (L11):** reglas duras 100%, recall@8, publicación tras revisión humana.
5. **Diferidos por condición:** grafo 3D (Three.js, §15.3), tours, embeddings.

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

El plano de contenido C2–C9 y el plano de servicio `api/`/`eval/` fueron implementados por OpenCode en sesiones previas (estaban sin commitear). Esta sesión (Hermes) implementó **L10 frontend** y la **base de release** (C9 autocontenido, áreas, layout, imports TS), y commiteó el conjunto v2 funcional en `v2/L10-frontend` para preservarlo. Sin push.