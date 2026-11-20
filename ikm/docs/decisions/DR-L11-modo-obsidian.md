# DR-L11 — Modo Obsidian: mind-map del vault con raíz y color editable

Estado: aceptada e implementada. Rama `v2/L10-frontend`.
Contexto: Dani pidió dos formas de ver el grafo — el mapa actual (L10d) y otro como el graph view de Obsidian (imagen de referencia): raíz central "Mercado IT" conectada a todo, áreas como cabezas medianas, conceptos como hojas, todos del mismo color editable. Corrección previa: la cabeza de área debe ser el ÁREA, no un concepto.

## DR-L11-01 — Segundo modo de vista (mapa / obsidian), no reemplazo

Decisión: toggle Obsidian/Mapa en GraphPage, estado en URL (`?mode=obsidian`). El modo mapa (L10d) queda intacto.
Por qué: son dos lecturas distintas del mismo conocimiento. El mapa por áreas con cabezas-concepto sirve para explorar relaciones; el mind-map jerárquico sirve para ver la estructura del vault (raíz→áreas→conceptos). Conviven.

## DR-L11-02 — El grafo Obsidian replica la jerarquía real del vault

Decisión: `buildObsidianGraph` (obsidianGraph.ts) agrega raíz "Mercado IT" + 10 cabezas de área (nombre del área) + enlaces jerárquicos (raíz→área, raíz→concepto, área→concepto) + las 472 relaciones reales. 266 nodos, 992 enlaces.
Por qué: se recorrió el vault IT-Mind-Map. La raíz `00 - Indice Maestro IT` enlaza a las 10 áreas Y a los 255 conceptos; cada índice de área enlaza a su raíz y a sus conceptos. Eso produce el abanico denso del centro en Obsidian. Los nodos raíz/área representan los índices (excluidos como conceptos en el release); no se inventan relaciones entre conceptos.
Tamaño por grado: raíz ~265 (gigante), áreas ~26 (medianas), hojas pocas (chicas). Raíz fija al centro; fuerza dispone áreas alrededor y hojas en periferia.

## DR-L11-03 — Color uniforme editable (como los grupos de Obsidian)

Decisión: en modo Obsidian todos los nodos del mismo color (gris #94a3b8 por defecto). Editor (ObsidianColors.tsx) con selector global + colores por área opcionales. Persiste en localStorage (obsidianColors.ts). Se aplica en vivo.
Por qué: pedido explícito — "todos del mismo color, con capacidad de editarse a elección del usuario". Los colores por área del mapa no aplican acá.

## DR-L11-04 — 2D y 3D; bloom reducido en Obsidian

Decisión: ambos renderers soportan el modo (prop `obsidian` + `monoColor` + `areaColors`). En 3D Obsidian el bloom baja (0.35/0.5 vs 0.9/0.18) para que no lave los tamaños; charge más fuerte para dispersar.
Por qué: el 2D replica la imagen de referencia; el 3D da la versión volumétrica. Con bloom alto el centro se volvía una masa blanca sin jerarquía legible.
Límite honesto: en 3D las labels del centro se solapan y el contraste cabeza/hoja es más modesto que en 2D. Funcional, pero el 2D es la lectura más fina.

## Verificación

Browser real: 2D Obsidian = imagen de referencia (raíz Mercado IT central gigante, áreas medianas alrededor, hojas chicas, gris uniforme). Editor de color en vivo (todo cambia de color, raíz incluida). 3D Obsidian renderiza monocromo con glow suave. Modo mapa intacto al alternar (255 nodos / 472 relaciones). 64 tests (6 nuevos) + build verde (~120 KB gz inicial).