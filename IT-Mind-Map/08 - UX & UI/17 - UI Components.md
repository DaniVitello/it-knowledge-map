---
title: "UI Components"
area: "UX / UI"
numero: 17
aliases: ["UI Components"]
tags: [concepto, it/ux-ui]
---
# UI Components

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 17 de 25**

## Qué abarca
- Buttons
- inputs
- modals
- cards
- tables
- etc.

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo UI Components para construir interfaces consistentes y reutilizables, lo que me permite centrarme en la experiencia del usuario sin reinventar cada elemento visual. Resuelvo el problema de la fragmentación del diseño, garantizando que botones, inputs, modales y tarjetas mantengan la misma apariencia y comportamiento en todo el producto. En mi día a día como diseñador de producto senior, los componentes son la base sobre la que defino flujos, pruebo hipótesis y entrego especificaciones a los desarrolladores. Una vez que entiendo cómo estructurarlos y documentarlos, puedo crear sistemas de diseño escalables, acelerar la iteración y reducir errores de implementación. Cuando el proyecto es un prototipo rápido o una prueba de concepto aislada, no es necesario preocuparse por la componentización exhaustiva.

## Esqueleto (el 20% esencial)
1. **Botones** – disparan acciones y comunican prioridad visual.  
2. **Inputs** – recogen datos del usuario y deben validar en tiempo real.  
3. **Modales** – enfocan la atención para tareas críticas sin abandonar la vista actual.  
4. **Cards** – agrupan información relacionada y facilitan la escaneabilidad.  
5. **Tables** – presentan datos estructurados y permiten interacción (ordenar, filtrar).

## Como funciona
1. Identifico la necesidad de interacción (p. ej., “el usuario debe confirmar una compra”).  
2. Selecciono el componente adecuado del inventario (botón primario).  
3. Configuro sus propiedades (texto, estado disabled, icono).  
4. Lo inserto en la jerarquía de la pantalla, respetando la guía de espaciado y tipografía.  
5. Si el componente necesita datos externos (tabla), lo conecto a la fuente y defino comportamientos (paginación).  
6. Valido con usuarios y desarrollo, ajustando estilos o estados según el feedback.

## Detalles
- **Básico:** Uso de componentes atómicos (botón, input) con estilos predefinidos y estados (default, hover, disabled).  
- **Intermedio:** Creación de componentes compuestos (card con botón y avatar) y parametrización mediante props o variantes.  
- **Avanzado:** Implementación de componentes inteligentes que gestionan su propio estado (modal que controla apertura/cierre) y adopción de patrones de lazy‑loading y accesibilidad (ARIA roles, focus trap).

## Ejemplo minimo
```html
<!-- Botón primario reutilizable -->
<button class="btn btn-primary" type="button">
  Comprar ahora
</button>

<style>
  .btn { padding: .5rem 1rem; border: none; cursor: pointer; }
  .btn-primary { background:#0066ff; color:#fff; }
  .btn-primary:hover { background:#0052cc; }
</style>
```

## Errores comunes
- **Sobrecargar un componente** con lógica de negocio; evitarlo delegando esa responsabilidad al contenedor.  
- **Ignorar estados accesibles** (focus, aria‑label); corregir añadiendo atributos ARIA y estilos de foco visibles.  
- **Duplicar estilos** en lugar de reutilizar variables; mantener una hoja de tokens de color y tipografía.

## Estado actual
- **Fundamentos estables:** los componentes básicos (botón, input, modal) siguen siendo los bloques de construcción esenciales para cualquier interfaz.  
- **Práctica moderna:** la tendencia es integrar los UI Components dentro de Design Systems que incluyen documentación viva, pruebas visuales automatizadas y herramientas de versionado (por ejemplo, Storybook). La componentización se alinea con arquitecturas frontend basadas en micro‑frontends y frameworks declarativos (React, Vue, Svelte).

## Conexiones
- **Componentización** – la disciplina de dividir la UI en piezas reutilizables es la base que permite crear y mantener UI Components de forma coherente.  
- **Arquitectura Frontend** – define cómo los componentes se organizan en módulos, librerías y bundles, impactando la escalabilidad del producto.  
- **Design Systems** – agrupan UI Components, guías de estilo y patrones de interacción en un repositorio único que facilita la alineación entre diseño y desarrollo.

## Ruta de estudio
1. **Prerequisitos:** fundamentos de usabilidad, principios de diseño visual y conocimientos básicos de HTML/CSS.  
2. **Fundamentos:** crear y documentar botones e inputs, aplicar estados y validar accesibilidad.  
3. **Intermedio:** combinar componentes en cards y modales, usar variantes y tokens de diseño.  
4. **Avanzado:** integrar componentes en un Design System, automatizar pruebas visuales y gestionar versiones con herramientas como Storybook o Bit.  
5. **Especialización:** explorar patrones de micro‑frontends y arquitectura basada en componentes para grandes plataformas.

## Preguntas de repaso
1. ¿Qué problema de diseño resuelve la reutilización de UI Components?  
2. ¿Cómo se diferencia un componente atómico de uno compuesto en la práctica diaria?  
3. ¿Qué pasos seguirías para validar la accesibilidad de un modal?  
4. ¿Por qué es importante documentar variantes de un botón dentro de un Design System?  
5. ¿En qué situaciones podrías prescindir de una arquitectura basada en componentes?

<!-- trazabilidad: run_id=run-20261106-202829-0ce3ce concept=08-ux-ui-17-ui-components written_at=2026-11-06T23:29:05.281597+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/13 - Componentización|Componentización]] · *Frontend*
- [[02 - Frontend/25 - Arquitectura Frontend|Arquitectura Frontend]] · *Frontend*
- [[08 - UX & UI/16 - Design Systems|Design Systems]]

---
← [[08 - UX & UI/16 - Design Systems|Design Systems]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/18 - States & Feedback|States & Feedback]] →
