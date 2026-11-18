# PROJECT_STATE_v2 — IT Knowledge Map v2

> Estado compartido entre sesiones. **Leer esto primero.** El plan vive en disco, no en la memoria del chat.

**Proyecto:** `C:\Users\DGVit\Proyectos\IT Career\ikm\`
**Rama actual:** `v2/L0-contratos` (commit `66d970d`)
**Servidor OpenCode (laptop 1):** `http://192.168.0.107:26826` · Basic `opencode:<password>` (password en `C:\Users\DGVit\Proyectos\run_opencode*.bat`, NUNCA en chat/docs).

---

## Capa en curso

**L1 — Inventario y parseo (C0–C1).** No empezada.

## Qué está hecho

- **L0 — Contratos y núcleo compartido (completa, verificada).**
  - `ikm/contracts/`: `__init__.py`, `ids.py`, `release.py`, `service.py`, `config.py`, `errors.py`, `utils.py`, `validate.py`, `generate.py`.
  - Generados y commiteados: 23 JSON Schema + 38 tipos TS en `ikm/contracts/generated/`.
  - Tests: `ikm/tests/test_l0_contracts.py` → **22 passed**.
  - Explicación educativa: `ikm/docs/L0_contratos_explicacion.md`.
  - Estructura del repo: `contracts/ content/ api/ web/ eval/ fixtures/ releases/ docs/decisions/ tests/`.
  - `.venv` del proyecto: pydantic 2.14.3 + pytest 9.2.0 (se instaló pydantic).

## Qué falta (orden)

1. **L1** — C0 inventario + C1 parseo sobre el vault real (`IT-Mind-Map/`). Solo lectura; reporta zonas/secciones ausentes y marcas de verificación.
2. **L2** — C2 registro de identidad (uid opaco + renombres + tombstones), C3 grafo (resolver WikiLinks de `Relacionados`, excluir navegación y bloques de código).
3. **L3** — C4 relaciones tipadas + C5 Journey + C6 vínculos.
4. **L4** — C7 compuerta, C8 derivados, C9 release.
5. **L5–L10** — backend, límites, RAG, chat, verificación, frontend.
6. **L11** — eval, CI, operación.
7. **P1–P5** (reparar v1) se resuelven al importar v1 en L1+, no bloquean.

## Decisiones registradas

- **DR-L0-01:** contratos en Pydantic v2 como única fuente de verdad (JSON Schema + TS generados). Alternativa descartada: escribir schemas a mano (deriva entre Python/TS).
- **DR-L0-02:** los enums de Python se emiten como alias de tipo TS propios; sin eso `Relation.type` queda `unknown`.
- **DR-L0-03:** `Config.hash_config()` se calcula con `json.dumps(..., sort_keys=True)` (la build de pydantic del venv no acepta `sort_keys` en `model_dump_json`).
- **Decisiones de encuadre del informe de aplicabilidad (§4)** siguen vigentes: rebuild para contratos/parseo; import para writer/areas/state; el vault es el corpus documentado (clase A); uid opaco nuevo; C1 tolera estructura variable; los wikilinks de navegación no son relaciones; los marcadores de verificación se conservan.

## Cómo reanudar (checklist)

1. Cargar skill `opencode-remote` + `it-career-pipeline`.
2. Verificar `GET /api/info` (password desde los launchers locales).
3. Leer `ikm/PROJECT_STATE_v2.md` (este archivo) + `ikm/docs/L0_contratos_explicacion.md`.
4. Leer la capa del pseudocódigo (`IT_Knowledge_Map_v2_Pseudocode_por_Capas.md`) + la sección del diseño que corresponda.
5. Implementar en `ikm/`, verificar con `.venv/Scripts/python.exe -m pytest ikm/tests -q` vía `/api/shell`, commit en la rama de capa.
6. **No avanzar de capa sin confirmar con el usuario.**

## Reglas operativas (recordatorio)

- Vault `IT-Mind-Map/` solo lectura. No modificar código v1 (`it-concept-map/`) sin orden.
- Git: commit local por capa; **push solo con confirmación del usuario** (dry-run primero).
- HTTP API, no CLI/TUI de OpenCode (0 tokens).
- Windows: `;` no `&&`; `py` no `python`; venv `.venv/Scripts/python.exe`; URL-encode completo del path.
- El output de `/api/shell` a veces viene UTF-16; decodificar con `errors='replace'` y, si hay mojibake, re-codificar.
