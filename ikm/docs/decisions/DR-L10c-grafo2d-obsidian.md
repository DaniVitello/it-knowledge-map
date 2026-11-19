# DR-L10c — Grafo 2D como el graph view de Obsidian

Estado: aceptada e implementada. Rama `v2/L10-frontend`. Corrección sobre L10b.
Contexto: el 2D de L10/L10b usaba posiciones fijas (phyllotaxis por área del release). Pedido: que la disponibilidad visual del 2D sea como la de Obsidian, no solo por la animación sino porque deja claras las jerarquías además de las conexiones.

## DR-L10c-01 — Layout de fuerzas en vivo, no posiciones fijas

Decisión: `GraphCanvas.tsx` calcula el layout con una simulación d3-force 2D en el cliente (reutiliza `d3-force-3d` en modo 2D), en vez de leer `graph-positions.json`.
Por qué: las posiciones fijas daban un anillo decorativo donde la proximidad no significaba nada. Obsidian usa fuerzas: los conectados se acercan, los no conectados se repelen. La cercanía pasa a reflejar la topología.
Fuerzas: link (distance 52, strength 0.28) + manyBody (-85) + collide (radio por grado, iterations 2) + forceX/Y suave al centroide de área (0.05). El timer interno de d3 se detiene (`.stop()`) y se tick-ea en el rAF propio; con `prefers-reduced-motion` se pre-resuelve (300 ticks) sin animación continua.

## DR-L10c-02 — Jerarquía por grado (tamaño de nodo)

Decisión: radio `nodeR(grado) = min(3 + sqrt(grado)*2.8, 26)`, escalado por zoom. Los hubs se ven notablemente mayores.
Por qué: es la señal de jerarquía de Obsidian. El tamaño por conectividad, más el layout que centra los hubs en su cluster, da la lectura de importancia además de las conexiones.

## DR-L10c-03 — Interacciones Obsidian: arrastre de nodo, foco, labels por zoom

Decisión: arrastrar un nodo lo fija (`fx/fy`) y recalienta la simulación (`alphaTarget(0.3)`); al soltar se libera. Hover/selección hacen foco (vecinos iluminados, resto atenuado). Labels con text-fade por zoom (`k>1.05`) además de los de foco.
Por qué: son los comportamientos que hacen que el graph view de Obsidian se sienta manipulable y legible. El arrastre de nodo (no solo pan de cámara) es clave.

## DR-L10c-04 — Estética: nodos planos, aristas finas, sin halos de área

Decisión: quitar los halos de área; aristas tenues por defecto (alpha 0.14) y brillantes al resaltar; nodos llenos por color de área.
Por qué: Obsidian es minimalista y no dibuja halos de grupo. Se mantiene la paleta neón por área del proyecto (identidad propia); la estructura/comportamiento son los de Obsidian, el vestido es el de IT Knowledge Map.

## Verificación

Browser real: layout orgánico con hubs grandes, foco al seleccionar HTTP, labels al zoom, arrastre de nodo con la simulación respondiendo (nodo desplazado + aristas tensadas). 52 tests Vitest + build verde, JS inicial ~120 KB gz (d3-force compartido 2D/3D en chunk común). Los modos de L10b (selección, vecindad, camino, multi-área, filtro) siguen funcionando sobre las posiciones vivas.