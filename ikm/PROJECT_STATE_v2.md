# PROJECT_STATE_v2 — IT Knowledge Map v2

> Estado compartido entre sesiones. **Leer esto primero.** El plan vive en disco, no en la memoria del chat.

**Proyecto:** `C:\Users\DGVit\Proyectos\IT Career\ikm\`
**Rama actual:** `v2/L1-contenido` (commit `90373af`)
**Servidor OpenCode (laptop 1):** `http://192.168.0.107:26826` · Basic `opencode:<password>` (password en `C:\Users\DGVit\Proyectos\run_opencode*.bat`, NUNCA en chat/docs).

---

## Capa en curso

**L2 — Identidad y grafo (C2–C3).** No empezada.

## Qué está hecho

- **L0 — Contratos (completa, verificada).** `ikm/contracts/` + 23 JSON Schema + 38 TS generados. 22 tests. Commit `66d970d`.
- **L1 — Inventario y parseo (completa, verificada).** `ikm/content/`:
  - `inventory.py` (C0), `parse.py` (C1), `publish_config.py`, `schemas.py`, `pipeline.py`, `cli.py`.
  - `fixtures/vault/` (7 notas sintéticas) y `tests/test_l1_content.py` (**40 passed**).
  - Explicación: `ikm/docs/L1_contenido_explicacion.md`.
  - Commit `90373af` (+ ajuste `ideas_clave`).
  - Verificado sobre el vault real (recuperado por el autor): **255 notas**, 64 con señales; **940 wikilinks** conceptuales, 37 marcas, **255 completas / 0 sin secciones**. Vault intacto (hash).

## Datos del vault (relevamiento L1)

- 266 `.md`: 255 conceptos + 11 índices (excluidos por config).
- Las 255 notas tienen las 10 secciones (vault recuperado). La 2ª sección se llama `## Ideas clave` → canónica `ideas_clave`.
- Wikilinks: 940 en `Relacionados` (conceptuales), 255 de navegación (blockquote), 725 de pie.
- 37 marcas de verificación. 64 notas con señales de escaneo.

## Qué falta (orden)

1. **L2** — C2 registro de identidad (uid opaco + detección de renombres + tombstones), C3 grafo (resolver los 940 wikilinks de `Relacionados`, excluir navegación/Mis notas/bloques de código).
2. **L3** — C4 relaciones tipadas + C5 Journey + C6 vínculos.
3. **L4** — C7 compuerta, C8 derivados, C9 release.
4. **L5–L10** — backend, límites, RAG, chat, verificación, frontend.
5. **L11** — eval, CI, operación.
6. **P1–P5** (reparar v1) se resuelven al importar v1; L2 no lo necesita (trabajo nuevo).

## Decisiones registradas

- **DR-L0-01:** Pydantic v2 como única fuente de verdad (JSON Schema + TS generados).
- **DR-L0-02:** los enums de Python se emiten como alias de tipo TS propios.
- **DR-L0-03:** `Config.hash_config()` con `json.dumps(..., sort_keys=True)` (el build de pydantic del venv no acepta `sort_keys` en `model_dump_json`).
- **DR-L1-01:** rebuild limpio para parseo (no importar `main/registry` roto). Toma v1 como referencia.
- **DR-L1-02:** el bloque AI es una zona única; los `##` internos se resuelven como `seccion` del link/marca, no como zonas.
- **DR-L1-03:** las secciones del contrato se normalizan (sin tildes, sin sufijo entre paréntesis) para tolerar las variantes reales del vault.
- **DR-L1-04:** `workdir/` es estado y está gitignored; los artefactos con hashes viven ahí.
- **DR-L1-05:** la 2ª sección del contrato se llama `ideas_clave` (el vault usa `## Ideas clave`); `esqueleto` queda como variante legacy. Solo los encabezados canónicos abren sección; los subtítulos `##` internos no truncan.
- **Decisiones de encuadre del informe de aplicabilidad (§4)** siguen vigentes.

## Cómo reanudar (checklist)

1. Cargar skill `opencode-remote` + `it-career-pipeline`.
2. Verificar `GET /api/info` (password desde los launchers locales).
3. Leer `ikm/PROJECT_STATE_v2.md` (este archivo) + la explicación de la capa anterior.
4. Leer la capa del pseudocódigo + la sección del diseño que corresponda.
5. Implementar en `ikm/`, verificar con `.venv/Scripts/python.exe -m pytest ikm/tests -q` vía `/api/shell`, commit en la rama de capa.
6. **No avanzar de capa sin confirmar con el usuario.**

## Reglas operativas (recordatorio)

- Vault `IT-Mind-Map/` solo lectura. No modificar código v1 (`it-concept-map/`) sin orden.
- Git: commit local por capa; **push solo con confirmación del usuario** (dry-run primero).
- HTTP API, no CLI/TUI de OpenCode (0 tokens).
- Windows: `;` no `&&`; `py` no `python`; venv `.venv/Scripts/python.exe`; URL-encode completo del path.
- El output de `/api/shell` es UTF-8 (con `errors='replace'`); si sale mojibake CJK, re-codificar a UTF-16LE.
