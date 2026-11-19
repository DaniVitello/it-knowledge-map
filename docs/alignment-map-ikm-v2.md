# Alignment Map — IT Knowledge Map v2

**Spec:** `references/spec-ikm-v2.md` (Especificación maestra v2.0, 2026-11-17) · también en laptop 1 `docs/especificacion-maestra-v2.md`.
**Scope:** auditoría completa del estado actual (post capa L10 frontend).
**Code state:** rama `v2/L10-frontend`, commit `ce255e5` · estado en `ikm/PROJECT_STATE_v2.md`.
**Evidencia:** frontend verificado en browser real (laptop 2 → laptop 1:5173); release verificado vía HTTP API (262 archivos, hashes); backend leído (`ikm/api/main.py`) + `docs/estado-implementacion-v2.md`. Los stubs de auth/limits/retrieval/verify/llm se clasifican según el doc de estado y `main.py`, no como producción.

> "Implementado" ≠ "alineado". Un stub no es alineación. Clases: ALIGNED, PARTIAL, GAP, SILENT-CHANGE, OVER-BUILD, MISPLACED, PROVENANCE, CANDIDATE-AS-DECISION.

## 1. Resultados de negocio en alcance (spec §2, §3)

- Explorar conceptos y áreas; comprender relaciones y el motivo de cada conexión (§2, §6.3).
- Conocer cómo se desarrolló el proyecto (Development Journey, §2, §4.2, §7).
- Consultar por chatbot conectado al contenido documentado (§2, §8).
- Exposición pública sin explicación personal (§3.1); visibilidad profesional con evidencia (§3.2).
- Preservar la Knowledge Base de v1 sin alteración destructiva (§3.4, §4.1).

## 2. Scorecard — criterios de aceptación §16

| # | Criterio (spec §) | Veredicto | Evidencia (código/comportamiento) |
|---|---|---|---|
| 16.1a | Visitante nuevo comprende el objetivo | ALIGNED | `web/src/routes/Home.tsx` (hero + "cómo leer este mapa" + métricas); verificado en browser |
| 16.1b | Secciones accesibles desde navegación | ALIGNED | `web/src/components/Shell.tsx` (sidebar Inicio/Grafo/KB/Journey/Chat + 10 áreas) |
| 16.1c | Exploración libre + recorridos guiados | PARTIAL | libre ALIGNED; recorridos guiados GAP (`routes/Tours.tsx` stub honesto, §5.4) |
| 16.1d | Chatbot no es el único mecanismo | ALIGNED | sitio navegable completo sin backend; chat es vía adicional (`routes/Chat.tsx`) |
| 16.2a | Conceptos desde contenido existente | ALIGNED | `routes/Concept.tsx` consume `concepts/<uid>.json` del release; vault solo lectura |
| 16.2b | Relaciones con explicación accesible | ALIGNED | 913 relaciones quoted; `components/RelationCard.tsx`; release `relations.json` |
| 16.2c | Selección de nodos/relaciones profundiza | ALIGNED | `routes/GraphPage.tsx` (panel selección→ficha), `GraphCanvas.tsx` hit-testing |
| 16.2d | Fuentes consultables cuando existen | PARTIAL | `Concept.tsx` renderiza `sources_detail`; muchos conceptos con fuentes vacías o placeholder `example.com` (dato del vault, no bug de UI) |
| 16.2e | No altera contenido original destructivamente | ALIGNED | `content/pipeline.py` hash vault antes/después; release `vault_hash` verificado; gate PASSED |
| 16.3a | Sección propia de Journey | PARTIAL | ruta + nav existen (`routes/Journey.tsx`); contenido GAP (0 registros) |
| 16.3b | Registros con evidencias y conceptos | GAP | `content/journey.py`/`links.py` stubs; C5/C6 sin registros curados |
| 16.3c | Fechas/decisiones solo si documentadas | ALIGNED | estado vacío honesto, sin fabricación (`Journey.tsx`, `JourneyRecord.tsx`) |
| 16.3d | Contenido privado no expuesto | ALIGNED | nada de Journey publicado; gate con escaneo canario/secretos (`content/gate.py`) |
| 16.4a | Chat dentro del alcance temático | GAP | `api/chat/scope.py` stub; `main.py:chat_endpoint` echo sin control de tema |
| 16.4b | Consulta KB y Journey | GAP | retrieval no integrado al release real en el stub; `api/retrieval/bm25.py` funcional pero sin cablear |
| 16.4c | Distingue documentado vs general | PARTIAL | frontend etiquetas (`lib/api.ts`, `ProvenanceBadge`); backend stub devuelve `basis:general` |
| 16.4d | No presenta inferencia como confirmada | PARTIAL | frontend etiqueta; `api/verify/verifier.py` stub (V1–V10 sin implementar real) |
| 16.4e | Enlaza respuestas con elementos existentes | GAP | `api/chat/orchestrator.py` stub; sin acciones de grafo/apertura |
| 16.4f | Reconoce falta de documentación | PARTIAL | frontend estado offline honesto; backend stub no lo hace |
| 16.4g | Aplica auth y límites | GAP | `api/auth/*`, `api/limits/*` stubs (dicts en memoria); chat sin auth en dev |
| 16.5a | Chat no usable sin autenticación | GAP | `main.py:chat_endpoint` sin dependencia de auth; decisión confirmada §17.11 no realizada |
| 16.5b | Credenciales no expuestas en frontend | ALIGNED | grep empírico en `web/src`: sin keys/secrets (solo "tokens CSS"/tokenize); `config.example.yaml` secretos vacíos |
| 16.5c | Límites de consumo desde backend | GAP | `api/limits/{quotas,budget,abuse}.py` stubs |
| 16.5d | Errores externos sin perder control de sesión | PARTIAL | frontend chat maneja error/offline (`lib/api.ts`); backend manejo stub |
| 16.5e | Recursos publicados respetan acceso | ALIGNED | release actual gate PASSED; Journey no publicado |

## 3. Hallazgos por impacto de negocio (rankeados)

### F1 — Chatbot sin autenticación ni límites [GAP]
- **Spec:** §16.5a/c, §17.11–15 (decisiones confirmadas), §9.
- **Code:** `api/main.py:chat_endpoint` (sin auth), `api/auth/{oidc,sessions,csrf}.py`, `api/limits/{quotas,budget,abuse}.py` (stubs).
- **Evidencia:** chat responde echo sin sesión en dev; stubs en memoria según `estado-implementacion-v2.md`.
- **Impact:** el chatbot NO puede habilitarse públicamente (bloquea §3.1 para la vía chat). No bloquea Entrega 1 (navegable).
- **Recomendación:** implementar OAuth Google + sesiones + límites en backend antes de exponer el chat (Entrega 3/5). El cliente frontend ya está listo.

### F2 — Development Journey vacío [GAP]
- **Spec:** §2, §4.2, §7, §16.3; decisión confirmada §17.3.
- **Code:** `content/journey.py`, `content/links.py` (stubs); `routes/Journey.tsx` (estado honesto, 0 registros).
- **Evidencia:** release `journey_records: 0`, `evidence: 0`.
- **Impact:** falta la mitad "conocer el desarrollo" del valor central del producto (§22). Bloquea Entrega 2.
- **Recomendación:** relevar e inventariar el material crudo (`OneDrive/Escritorio/IT Career - Documentacion del dia` + `docs/`), curar registros con evidencias, aprobar publicación. El pipeline no escribe Journey solo (§7.3, §8.6).

### F3 — Chatbot sin respuesta real (retrieval+LLM+verify) [GAP]
- **Spec:** §8.1–8.9, §16.4.
- **Code:** `api/chat/orchestrator.py`, `api/llm/adapter.py`, `api/verify/verifier.py`, `api/retrieval/graph_expand.py` (stubs); `bm25.py` funcional.
- **Evidencia:** `main.py:chat_endpoint` devuelve `Echo: <message>`; verificado en browser.
- **Impact:** el chat no conecta conocimiento general con contenido del proyecto (§8.4/8.5), no diferencia procedencia real. Entrega 3.
- **Recomendación:** cablear retrieval sobre el release real + adaptador Groq + verificador determinista + orquestador con acciones de UI. Modelo/proveedor/RAG aún pendientes (§18.4).

### F4 — Plataforma no pública / sin despliegue [GAP]
- **Spec:** §3.1, §12.5, §16 (validación y publicación), Etapa 6.
- **Code:** release en `workdir/` (gitignored); sin hosting ni CI; `releases/` vacío (solo `.gitkeep`).
- **Evidencia:** dev server local; sin build desplegado.
- **Impact:** el objetivo de exposición pública (§3.1) no se cumple hasta desplegar. Hosting es decisión pendiente (§18.5, Netlify candidato §12.2).
- **Recomendación:** publicar release tras gate + revisión humana del diff (C7/C9, L11); definir hosting frontend + backend; CI de build/tests.

### F5 — Recorridos guiados ausentes [GAP]
- **Spec:** §5.4, §16.1c.
- **Code:** `routes/Tours.tsx` (stub honesto); sin datos de tours en el release.
- **Impact:** menor — la exploración libre y la presentación cubren la comprensión inicial; los tours son organización adicional.
- **Recomendación:** definir 3 tours iniciales (conocer proyecto / explorar conocimiento / conocer desarrollo) tras Journey. No bloquea Entrega 1.

### F6 — Calidad de fuentes (placeholders) [PARTIAL]
- **Spec:** §16.2d, §4.1.
- **Code:** `Concept.tsx` renderiza fuentes; datos del vault con `example.com` o vacías.
- **Impact:** menor para navegación; afecta la credibilidad de "fuentes consultables".
- **Recomendación:** curaduría de fuentes en el vault (v1) o marcar visualmente fuente no verificada. No es bug de frontend.

## 4. Checks no-negociables

| Check | Resultado | Evidencia |
|---|---|---|
| Secretos/keys no en frontend | PASS | grep empírico `web/src` sin credenciales; `config.example.yaml` vacío |
| Auth & límites en backend | FAIL (stubs) | `main.py` sin auth; `api/auth`/`api/limits` stubs — no producción |
| Etiquetas de procedencia | PARTIAL | frontend `ProvenanceBadge` listo; backend stub `basis:general` |
| Contenido original no alterado | PASS | hash vault verificado, solo lectura, gate PASSED |
| Inferido ≠ documentado | PARTIAL | frontend etiqueta; verify backend stub |
| Responsabilidades separadas UI/backend | PASS | frontend sin auth/limits/secretos; chat cliente llama API (§12.4) |
| Identificadores estables (uid, no título/ruta) | PASS | `contracts/ids.py`, registry C2, `content_hash`/`vault_hash` (§13) |

## 5. Stubs vs alineado

- **Construido y alineado (Entrega 1):** Home, KB por área, ficha (10 secciones + marcas + relaciones quoted), grafo 2D (selección/vecindad/camino/recuperar exploración), búsqueda Ctrl+K, temas, responsive, accesibilidad, Journey/Tours/Privacy honestos. Release autocontenido verificado. Contratos L0. Plano de contenido C0–C4, C7–C9.
- **Construido pero stub (NO alineado para producción):** `api/auth/*`, `api/limits/*`, `api/retrieval/{entities,graph_expand,journey_expand}`, `api/verify/verifier`, `api/llm/{adapter,prompts}`, `api/chat/{orchestrator,scope}`, `api/main.py` endpoints; `content/journey.py`, `content/links.py`, `content/runner.py`.
- **No construido (GAP):** registros Journey curados, tours, despliegue público, CI/eval (L11).
- **Decisión pendiente, NO requisito (no es GAP):** grafo 3D / Three.js. La spec lo deja abierto (§6.7: "no está decidido que el grafo deba ser completamente tridimensional"; §3.3 interés de aprendizaje; §12.2 candidata; §18.3 pendiente). El 2D canvas de L10 es plenamente conforme; 3D es una exploración opcional a decidir por utilidad/legibilidad/rendimiento/complejidad (§6.7, §19), no una funcionalidad faltante.

## 6. Riesgos

- **Provenance en producción:** si el chat se expone con el verify stub, podría mostrar inferencias como documentadas (violación dura §8.3/§22). Mitigación: no habilitar chat hasta verify real + auth.
- **Publicación prematura de Journey:** material crudo sin curar puede exponer secretos/privados (§10). Mitigación: gate + clasificación público/seleccionado/privado (aún pendiente §18.1).
- **Candidatas como decisiones:** Three.js, GPT-OSS 120B, Netlify, Groq son candidatas (§12.2), no aprobadas. El frontend eligió 2D canvas (DR-L10-02, permitido por §6.7) — decisión registrada, no silenciosa.

## 7. Recomendaciones (priorizadas)

1. **Publicar Entrega 1** (release navegable) tras gate + revisión humana — cumple §3.1 parcialmente sin chat. Impacto alto, esfuerzo M. Resuelve F4 (parcial).
2. **Relevar + curar Journey** — desbloquea la mitad "proceso" del producto. Impacto alto, esfuerzo L. Resuelve F2.
3. **Auth OAuth + límites backend** antes de exponer chat. Impacto alto (seguridad), esfuerzo L. Resuelve F1.
4. **Chat real** (retrieval+Groq+verify+orquestador) con procedencia. Impacto alto, esfuerzo L. Resuelve F3.
5. **Tours guiados** + curaduría de fuentes. Impacto medio, esfuerzo M. Resuelve F5/F6.
6. **CI/eval + despliegue** (L11). Impacto medio, esfuerzo M.

## 8. Optimizaciones de proceso

- **Orden delivery-first respetado en L10:** el sitio navegable sin backend (Entrega 1) se completó antes del chat real. Alineado con Apéndice A.
- **Desvío menor:** los stubs de `api/` (auth/limits/chat, Entrega 3) se construyeron antes de cerrar el primer corte publicable. Son stubs (bajo costo), pero el orden ideal es publicar Entrega 1 primero. No es OVER-BUILD dañino; anotar para no repetir.
- **Verificación empírica:** el frontend se probó en browser real, no solo tests. El release se verificó contra disco. Mantener esta disciplina.
- **Pendientes que bloquean:** §18.1 (ubicación/clasificación Journey) bloquea Entrega 2; §18.4 (modelo/RAG/retención) bloquea Entrega 3; §18.5 (hosting) bloquea publicación.

## 9. Decisiones pendientes surfaced (no asumidas, spec §18)

- Contenido: ubicación/cantidad/clasificación del material Journey; sincronización KB↔plataforma.
- UX: estructura definitiva de navegación, primera pantalla, tours iniciales, onboarding.
- Grafo: tipos de nodos/relaciones, almacenamiento de explicaciones, 2D vs 3D/Three.js.
- Chatbot: historial/retención, datos de cuenta, presentación de procedencia, conteo off-topic, modelo/proveedor, estrategia RAG.
- Arquitectura: React/Vite/Tailwind (usados en L10 como decisión registrada, no confirmadas en spec §17), base de datos, hosting, costos, logging/monitoreo.

## 10. Veredicto general

**Ready-with-caveats por entrega.** La **Entrega 1 (KB navegable sin backend)** está bien alineada con §16.1/16.2 y las decisiones confirmadas 9/10/16/17, y lista para revisión de publicación. El **chatbot (Entrega 3)** y el **Journey (Entrega 2)** son stubs/vacíos y NO alineados para uso público aún. Las decisiones confirmadas de **auth/límites (§17.11–15)** no están realizadas (stubs). El valor central de navegación está entregado; los bloqueos para lanzamiento público son despliegue + auth/límites (chat) + curaduría Journey. Ningún SILENT-CHANGE ni PROVENANCE activo detectado en lo construido; el riesgo de provenance está contenido mientras el chat no se exponga.
