# DR-L10d — Jerarquía por área: cada área con su cabeza

Estado: aceptada e implementada. Rama `v2/L10-frontend`. Corrección sobre L10c.
Contexto: pedido de Dani — "cada área tenga su cabeza, y no solamente conectar todos a mismo nivel jerarquico". Referencia: graph view de Obsidian (hub central + anillo de cabezas secundarias + nubes de miembros orbitando).

## DR-L10d-01 — La cabeza de área es el concepto más conectado (data-driven)

Decisión: `computeHeads` (forceLayout.ts) elige por área el nodo de mayor grado, desempate alfabético por título (determinista). Cabeza global = mayor grado del mapa.
Por qué: la jerarquía sale de los datos reales, no de un nodo padre inventado ni de relaciones falsas (respeta provenance). El concepto más conectado es el líder natural del área.
Nota: hay dos cabezas "HTTP" (Backend y Networking) porque son dos conceptos reales distintos del vault, no un duplicado.

## DR-L10d-02 — Layout que orbita la cabeza

Decisión: cabeza fija en el centroide de su área (`fx/fy` 2D, `fx/fy/fz` 3D); miembros atraídos a la posición viva de su cabeza (strength 0.25); fuerza de links debilitada (0.06) y charge bajo (-25) para que la jerarquía domine el layout y no se infiltren miembros entre áreas.
Por qué: con links fuertes la cabeza derivaba a la periferia y los miembros se mezclaban entre áreas (mesh). Fijar la cabeza + gravedad fuerte al head + links débiles da clusters compactos con la cabeza al centro y miembros orbitando (hub-and-spoke).
Drag: al soltar una cabeza se restaura su ancla (fx/fy = anchor); un miembro se libera (null).

## DR-L10d-03 — La cabeza se ve como cabeza

Decisión: radio realzado (3D `nodeRadius` ×2.1 + 10, ~4–6× el miembro; 2D +8), anillo en 2D (accent para la cabeza global), label fijo siempre visible (2D y 3D), en 3D label con caja mayor + negrita + borde accent (`.graph3d-label-head`). Spokes (aristas que tocan una cabeza) más visibles; inter-área tenues.
Por qué: la jerarquía tiene que leerse de una, incluso encuadrado. Tamaño + anillo + label fijo + glow comunican "esto es la cabeza" sin ambigüedad.

## Verificación

Browser real: 2D con cabezas centradas, clusters compactos, spokes radiales, una cabeza por área separada, mesh central minimizado. 3D con cabezas 4–6× mayores, glow y labels bold accent, miembros orbitando. 58 tests (6 nuevos de jerarquía) + build verde (~120 KB gz inicial).
Pendiente menor (no rompe la jerarquía): simetría perfecta de algún cluster, un par de nodos inter-área sueltos cerca del centro. Las aristas inter-área tenues son relaciones reales y se conservan.