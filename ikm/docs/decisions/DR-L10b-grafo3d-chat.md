# DR-L10b — Grafo 3D, puente chat↔grafo y dedup de relaciones

Estado: aceptadas e implementadas. Rama `v2/L10-frontend`. Release `2026-11-19-95e94e92`.
Contexto: capa L10b encima del frontend L10. Ver explicación completa en `../L10b_grafo3d_chat_explicacion.md`.

## DR-L10b-01 — Layout del grafo calculado en el cliente

Decisión: el layout 3D se calcula en el navegador con `d3-force-3d`, no se precomputa en el pipeline.
Por qué: el objetivo de v2 es exploración fluida. Un layout client-side está vivo (los nodos se asientan, la cámara y el hover responden al instante) sin ida y vuelta al servidor. Precomputar daba un grafo estático, más barato pero muerto.
Alternativa descartada: posiciones fijas en el release (como el phyllotaxis 2D de `content/derivados.py`). Se mantiene para la vista 2D.
Costo asumido: ~140 KB gz de motor 3D, mitigado con carga diferida.

## DR-L10b-02 — Three.js vanilla, no react-three-fiber

Decisión: render con Three.js a mano (`InstancedMesh` + `CSS2DRenderer` + `UnrealBloomPass`) en `src/components/Graph3D.tsx`.
Por qué: control fino del rendimiento para 255 nodos / 472 aristas. Una sola draw call para los nodos, labels HTML nítidos, glow neón. El estado por-frame vive en refs, no en estado de React.
Alternativa descartada: react-three-fiber. Más cómodo, pero suma reconciliación de React sobre el loop de render que no hace falta.

## DR-L10b-03 — Dedup de relaciones por par no ordenado

Decisión: una conexión por par `{uid menor, uid mayor}`; se conserva el tipo tipado y la explicación `quoted` con texto. En `content/relations.py` (`colapsar_reciprocas`).
Por qué: el vault guarda cada relación en ambas fichas (navegación Obsidian). El pipeline las emitía como dos aristas dirigidas, duplicando el vínculo conceptual. 913 aristas dirigidas → 472 relaciones únicas.
Garantía: no se pierde información (la explicación se conserva); el dedup vive en el derivado, el vault no se toca. Uid de relación estable entre rebuilds. 7 tests.

## DR-L10b-04 — El puente chat↔grafo se resuelve en el cliente

Decisión: `src/lib/chatBridge.ts` enlaza entidades del mensaje contra el índice del release y deriva la acción de grafo, sin depender del backend.
Por qué: el backend de chat es un stub echo. Si el puente dependiera del LLM, no funcionaría hoy. Resolver la intención en el cliente contra datos documentados hace que funcione ya y que nunca se invente una relación.
Regla: solo se activan vínculos que existen en el grafo. Match de concepto por título completo con límites de palabra; áreas por nombre.
Cuando haya LLM real, la misma UI sirve sin cambios. 9 tests.

## DR-L10b-05 — 3D por defecto, toggle 2D por URL, carga diferida

Decisión: el grafo abre en 3D; `?view=2d` fuerza la vista plana. El motor 3D va en chunk lazy.
Por qué: el 3D es la mejor herramienta para entender relaciones espaciales; el 2D queda como fallback ligero y compartible. El estado de vista vive en la URL (enlace compartible). JS inicial ~120 KB gz, bajo el presupuesto de 250 KB (§15.5).

## DR-L10b-06 — Modo multi-área para relaciones entre áreas

Decisión: nuevo modo `?areas=a,b` (prop `highlightAreas` en ambos renderers) que resalta los nodos de dos áreas y las aristas que las cruzan.
Por qué: "relación entre frontend y backend" no es un camino entre dos conceptos sino el conjunto de vínculos entre dos áreas. El modo área simple (una sola) no alcanzaba. Este modo es el que activa el chat para el caso de dos áreas.

## Pendientes que estas decisiones no resuelven

Backend de chat/auth/limits/retrieval/verify/llm sigue stub. Journey sin registros. Sin publicar (gate humano pendiente). El render WebGL se verifica en browser real, no en jsdom.