# Explicación del código — v2 Capa L10b: grafo 3D, puente chat↔grafo y dedup de relaciones

> Documento educativo. Cuenta qué se hizo encima del frontend L10, por qué, y qué se aprendió en el camino (incluidos los errores). No pega bloques de código: referencia módulos y funciones.
>
> Proyecto: `C:\Users\DGVit\Proyectos\IT Career\ikm\web\`. Rama: `v2/L10-frontend`.
> Diseño de referencia: `diseno-tecnico-pipeline-v3.md` §15 (frontend y visualización), §6.6 (estado de exploración), §8.7 (el chat conecta con la UI).
> Skill de capa: `.opencode/skills/ikm-v2-layer-coder`. Puente de negocio↔técnica: skill Hermes `business-alignment-review`.
> Redacción: principios de `github.com/blader/humanizer` (menos robot, más persona).

---

## 1. De dónde venimos

L10 dejó un sitio navegable sin backend: fichas, Knowledge Base por área, un grafo 2D en canvas y un cliente de chat honesto sobre su procedencia. Funcionaba. Pero tenía dos cosas que no cerraban con el objetivo de v2, que es exponer la funcionalidad con fluidez y animaciones, y que el chat sirva para explorar.

La primera: las relaciones se veían duplicadas. Un concepto mostraba seis conexiones cuando en realidad eran dos o tres, repetidas. La segunda: el grafo era plano. Para un mapa de 255 conceptos interconectados, quedarse en 2D era desaprovechar la mejor herramienta que tenemos para entender relaciones, que es el espacio.

Esta capa ataca esas dos cosas y suma el puente entre el chat y el grafo. La dividí en cuatro cortes chicos, cada uno con su commit y su verificación: L-data (dedup), L-3d (grafo tridimensional), L-chat-graph (el chat activa el grafo) y L-ui (motion).

## 2. L-data: por qué había seis conexiones donde debía haber dos

El vault de Obsidian guarda cada relación en las dos fichas involucradas. Si HTTP se relaciona con DNS, el link aparece en la ficha de HTTP y también en la de DNS. Es lo correcto para navegar en Obsidian, donde cada nota es un punto de entrada. Pero el pipeline de v1 emitía cada link como una arista dirigida separada. Resultado: el mismo vínculo conceptual contado dos veces, una por cada dirección.

En el grafo eso se traducía en aristas superpuestas y en paneles de relaciones inflados. HTTP llegaba a mostrar veinte entradas cuando sus vínculos reales eran seis.

El arreglo es canonicalizar por par no ordenado. En `content/relations.py`, `colapsar_reciprocas` agrupa las relaciones por el par `{uid menor, uid mayor}` y emite una sola conexión por par (descarta self-loops). De las dos direcciones conserva el tipo tipado si existe y la explicación `quoted` que tiene texto, así que la provenance del autor no se pierde. El uid de la relación sale de `uid_relacion(a, b)`, estable entre rebuilds.

El release pasó de 913 aristas dirigidas a 472 relaciones únicas. El release resultante es `2026-11-19-95e94e92`, con la compuerta C7 en PASSED y siete tests nuevos que cubren el dedup (par recíproco, conservación de la explicación, estabilidad del uid). El vault no se tocó: el dedup vive en el derivado, no en la fuente.

Lo que me llevé de acá: el dato de origen no estaba mal, estaba duplicado por diseño. Antes de "corregir" un conteo raro, conviene entender por qué el origen lo produce. Si hubiera borrado links a ciegas para bajar el número, habría perdido explicaciones.

## 3. L-3d: el grafo en tres dimensiones, calculado en tu navegador

### Por qué client-side

Discutimos si precomputar las posiciones en el pipeline o calcularlas en el navegador. Elegí client-side por una razón de experiencia de usuario: un layout que se calcula en el cliente está vivo. Los nodos se asientan con una simulación de fuerzas que podés ver acomodarse, y la cámara, el hover y la selección responden en el momento sin ida y vuelta al servidor. Precomputar habría dado un grafo estático, más barato de renderizar pero muerto. Para un producto cuyo objetivo es la exploración, vale la pena el coste.

El layout usa `d3-force-3d` corriendo en el browser. En `src/lib/forceLayout.ts`, `areaCentroids` ubica cada área en una esfera de Fibonacci (reparte los centroides sin amontonarlos) y `nodeRadius` escala cada nodo por su grado, así los conceptos muy conectados se ven más grandes. La simulación combina fuerza de links, repulsión, colisión y un atraente suave hacia el centroide del área de cada nodo. Eso mantiene los clusters por área legibles sin que el grafo se vuelva una bola.

### Por qué Three.js a mano y no react-three-fiber

Para 255 nodos y 472 aristas necesitaba control fino del rendimiento. Three.js vanilla me deja usar `InstancedMesh` (las 255 esferas se dibujan en una sola llamada), `CSS2DRenderer` para los labels (texto HTML nítido, no texturas) y `UnrealBloomPass` para el glow neón. react-three-fiber habría sido más cómodo de escribir, pero agrega una capa de reconciliación de React sobre el loop de render que no necesito y que complicaría el presupuesto de cuadros por segundo. El componente `src/components/Graph3D.tsx` maneja el ciclo de vida a mano: crea la escena al montar, la destruye al desmontar, y usa refs para el estado que cambia por frame sin disparar re-renders de React.

Los detalles que importan para que se sienta bien:

- Los labels aparecen solo en hover, selección y vecinos. Mostrar 255 labels a la vez sería ruido.
- El raycasting distingue nodos de aristas, así podés clickear una relación y ver su explicación, no solo un nodo.
- La cámara se mueve con tweens suaves (`focusNode`, `fitCamera`, `frameNodes`), no a saltos.
- Auto-rotación lenta cuando no interactuás hace unos segundos. Se pausa al hover, al seleccionar, al arrastrar o cuando hay un camino activo. Respeta `prefers-reduced-motion`.

### Rendimiento y carga diferida

El motor 3D (Three.js + bloom + d3-force-3d) pesa. Lo cargo con `React.lazy`, así va en un chunk aparte de ~140 KB gz que solo se baja cuando entrás al grafo o al chat con el panel visible. El JS inicial del sitio queda en ~120 KB gz, por debajo del presupuesto de 250 KB de §15.5. La vista 2D original sigue disponible con `?view=2d`; el 3D es el default. El toggle vive en la URL, así que un enlace a una vista 2D se puede compartir.

### Los modos de exploración

El grafo no es solo un dibujo. Tiene modos que responden a la URL:

- Selección: clickeás un nodo y se iluminan sus vecinos, el resto se atenúa.
- Vecindad (`/graph/view/:uid`): subgrafo de un concepto y sus conexiones directas.
- Camino (`?from=X&to=Y`): BFS sobre la adyacencia (`src/lib/graph.ts`, `shortestPath`), resalta la cadena y encuadra la cámara sobre ella.
- Multi-área (`?areas=a,b`): resalta los nodos de dos áreas y las aristas que las cruzan. Esto es lo que usa el chat para "frontend y backend".

### Los errores que me enseñaron algo

Tres bugs me costaron vueltas y vale la pena anotarlos:

El canvas aparecía en 300×150 y el grafo vacío. La causa no era el código de dibujo sino el entorno de prueba: la pestaña del browser estaba en background, y Chrome throttlea `requestAnimationFrame` y `ResizeObserver` ahí. El primer paint dependía de un rAF que nunca llegaba. Lo resolví con un `useLayoutEffect` que mide, encuadra y dibuja de forma síncrona al montar, sin esperar al loop. Moraleja: no confiar el primer render a un rAF.

La vista de vecindad mostraba los vecinos fuera de pantalla. `centerOn` forzaba un zoom mínimo de 1.4, que acercaba tanto que los vecinos quedaban fuera del encuadre. Lo cambié para que solo panea, sin tocar el zoom. La lección: centrar no es acercar.

El modo camino calculaba bien la ruta pero se veía perdida entre los 255 nodos, porque la cámara encuadraba el grafo entero. Agregué `frameNodes`, que encuadra solo los nodos de la ruta. Ahora la cadena DNS→IP→HTTP se ve brillante y clara. Resaltar no alcanza si la cámara no acompaña.

## 4. L-chat-graph: pedirle al chat que active el grafo

El pedido concreto era: si le pido al chat "relación entre frontend y backend", tiene que activar esas relaciones en el grafo. No solo responder texto.

### Cómo se resuelve sin depender del backend

El backend de chat todavía es un stub que hace echo. Si el puente dependiera de que el modelo entendiera la pregunta y devolviera entidades, no funcionaría hoy. Así que la intención se resuelve en el cliente, contra los datos documentados del release. Nunca se inventa una relación: solo se activan vínculos que existen en el grafo.

En `src/lib/chatBridge.ts`:

- `linkEntities` busca entidades en el mensaje. Los conceptos se matchean por título completo con límites de palabra (normalizando tildes y espacios), contra el índice del release. Las áreas, por nombre. El límite de palabra importa: "IP" no debe matchear dentro de "equipment".
- `deriveAction` traduce las entidades en una acción de grafo. Dos áreas nombradas → resaltar relaciones entre áreas. Dos conceptos → camino entre ellos. Un concepto → vecindad. Un área → resaltar el área.
- `actionToUrl` convierte la acción en una URL del grafo, y `actionVerb` en la frase legible que muestra la UI.

Para "¿Cómo se relacionan Frontend y Backend?", `linkEntities` encuentra las áreas Frontend y Backend (y ningún concepto, porque ningún título completo de concepto aparece en esa frase). `deriveAction` devuelve una acción de áreas. El grafo resalta los nodos de ambas áreas y las aristas que las cruzan.

### La vista split

En `/chat` (`src/routes/Chat.tsx`) el chat ocupa la izquierda y el grafo 3D la derecha. Cada consulta deriva una acción y el panel de grafo se actualiza en vivo con el resaltado correspondiente. Un banner sobre el input dice qué se va a activar ("Resaltar las relaciones entre Frontend ↔ Backend") con un botón Abrir que lleva a la vista completa del grafo. Clickear un nodo en el panel embebido abre su vecindad.

El chat sigue mostrando su procedencia y sus estados (disponible / degradado / no-disponible). El puente es una capa encima: aunque el backend no esté, la exploración visual funciona, porque sale del release. Cuando haya un LLM real detrás del chat, esta misma UI sirve sin cambios.

Nueve tests cubren el puente (`src/lib/chatBridge.test.ts`): las dos áreas, el camino entre conceptos, la vecindad, el límite de palabra, el caso sin entidades y las URLs.

## 5. L-ui: motion que suma, no que distrae

El objetivo pedía animaciones fluidas y una estética moderna y tecnológica. La base ya era dark-first con tokens CSS por área y acentos neón. Sumé tres cosas puntuales, todas con `prefers-reduced-motion` respetado:

- Count-up en las métricas del home (`src/routes/Home.tsx`, componente `CountUp` con `useMotionValue` de Framer Motion). Los números suben desde cero al valor real al montar.
- Una aurora sutil detrás del hero del home, que deriva lento con solo transform y opacity (compone en GPU, no repinta). Clase `.hero-aurora` en `src/styles/index.css`.
- La auto-rotación idle del grafo 3D, ya contada arriba.

Nada de esto es decorativo por sí mismo: el count-up dirige la mirada a las métricas, la aurora da profundidad al hero sin robar atención, y la rotación idle le dice al usuario que el grafo es manipulable. Si una animación no comunica algo, sobra.

## 6. Lo que no está hecho, sin chamuyo

Para que el handoff no mienta por omisión:

- El backend de chat, auth, límites, retrieval, verificación y LLM siguen siendo stubs. El chat responde echo con etiqueta de "conocimiento general del modelo". El puente chat↔grafo no depende de ellos, pero una respuesta real con citas todavía no existe.
- El Development Journey no tiene registros reales cargados.
- Nada está publicado. El release es local, no hubo push, y la compuerta de revisión humana sigue pendiente. El sitio se prueba en dev, no está en producción.
- El grafo 3D no tiene tests de render WebGL: jsdom no expone WebGL, así que el render se verifica en browser real, no en la suite. La lógica de grafo (BFS, vecindad, dedup, puente) sí está testeada.

## 7. Cómo probarlo

En laptop 1, `ikm/web`: `npm run dev` levanta Vite en `0.0.0.0:5173`. El backend stub opcional se levanta con `py -m uvicorn ikm.api.main:app --port 8000` (el chat lo detecta y muestra "disponible"; sin él, muestra "no disponible" y el sitio sigue navegable).

Recorridos que cubren esta capa:

- `/graph`: grafo 3D, arrastrar para rotar, rueda para zoom, clickear nodos y aristas. Botón 2D para la vista plana.
- `/graph?from=c_LJXCYJ6ING&to=c_267BQAZTKD`: camino DNS→HTTP, cadena resaltada y encuadrada.
- `/chat`: escribir "¿Cómo se relacionan Frontend y Backend?" y mirar el panel derecho. También "Camino entre HTTP y DNS" y "Explorá AI / ML Fundamentals".
- `/`: count-up de métricas y aurora del hero.

## 8. Verificación

- Frontend: 52 tests en verde (7 archivos), build de producción OK, JS inicial ~120 KB gz.
- Pipeline: 93 tests base + 7 del dedup, compuerta C7 PASSED, release `95e94e92` con hashes verificados contra disco.
- Browser real (laptop 2 apuntando a laptop 1): render 3D con glow, selección con vecinos iluminados, camino encuadrado, chat→grafo activando Frontend↔Backend, conteos deduplicados (HTTP con 6 relaciones únicas).

Los números y el estado vivo están en `ikm/PROJECT_STATE_v2.md`. Las decisiones puntuales, en `ikm/docs/decisions/DR-L10b-grafo3d-chat.md`.