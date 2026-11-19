# Frontend web (L4, capa 20)

Stack propuesto (seccion 15.1): React, Vite, TypeScript; Tailwind CSS con tokens de diseño; React Router; TanStack Query.

Los tipos se generan desde los contratos (`ikm/contracts/generated/ts/`).

## Estructura sugerida

```text
ikm/web/
├── package.json
├── vite.config.ts
├── tailwind.config.ts
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes/          # /, /graph, /graph/view/:id, /kb/:area, /kb/c/:uid/:slug, /journey, ...
│   ├── components/      # grafo 2D, ficha de concepto, chatbot, ...
│   ├── lib/             # cliente de release, api, estado de exploracion (IndexedDB)
│   └── styles/          # tokens de diseño
└── public/
```

## Rutas (seccion 15.2)

/, /graph, /graph/view/:id, /kb/:area, /kb/c/:uid/:slug, /journey, /journey/r/:uid/:slug, /tours/:id, /privacy

## Grafo (seccion 15.3)

2D para vistas contextuales; prototipo comparativo 2D vs 3D para la exploracion inicial (Three.js, nodos instanciados, posiciones precalculadas).

## Estado de exploracion (seccion 15.4)

ExplorationState serializable y versionado; historial en IndexedDB del navegador, sin cuenta.

## Accesibilidad y rendimiento (seccion 15.5)

Navegacion por teclado en el grafo; JS inicial <250 KB comprimido; grafo y bibliotecas cargados de forma diferida.

Estado: pendiente de implementacion. El frontend depende solo del release (estatico), no de la API.
```