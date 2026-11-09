---
title: "Color"
area: "UX / UI"
numero: 14
aliases: ["Color"]
tags: [concepto, it/ux-ui]
---
# Color

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 14 de 25**

## Qué abarca
- Paletas
- contraste
- significado
- estados

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el color para guiar la atención, comunicar significado y reforzar la identidad visual de un producto digital. Resuelvo la ambigüedad de qué elemento es interactivo, cuál está activo o deshabilitado, y cómo priorizo la información en pantalla. Aparece en cada fase del diseño: investigación de usuarios, definición de la paleta, creación de componentes y pruebas de usabilidad. Después de comprender el color, puedo diseñar sistemas de diseño consistentes, validar accesibilidad y adaptar la marca a diferentes contextos. Cuando el producto ya tiene una guía de estilo aprobada y la accesibilidad está certificada, no es necesario volver a profundizar en la selección cromática.

## Esqueleto (el 20% esencial)
1. **Paletas** – Conjunto limitado de colores que refleja la marca y facilita la consistencia.  
2. **Contraste** – Diferencia luminosa entre elementos que garantiza legibilidad y accesibilidad.  
3. **Significado** – Asociación cultural o psicológica que comunica estados (éxito, error, alerta).  
4. **Estados** – Variaciones cromáticas que indican interacción (hover, activo, deshabilitado).  

## Como funciona
1. Defino una paleta base alineada con la identidad de la marca.  
2. Selecciono colores de fondo y texto que cumplan ratios de contraste WCAG.  
3. Asigno significados (por ejemplo, rojo = error) y los aplico a componentes críticos.  
4. Creo variantes de cada color para los estados de interacción, asegurando que el contraste se mantenga en cada uno.  
5. Valido el esquema con usuarios y herramientas de accesibilidad antes de implementarlo.

## Detalles
- **Básico:** Elegir 1‑2 colores primarios, 1‑2 secundarios y neutros; aplicar la regla 60‑30‑10 para distribución visual.  
- **Intermedio:** Generar tonos y matices (tints, shades) para ampliar la paleta sin romper la coherencia; usar herramientas de contraste para validar cada combinación.  
- **Avanzado:** Implementar un sistema de tokens de color en el código, integrar pruebas automatizadas de contraste y adaptar la paleta a modos claros/ oscuros y a diferentes culturas.

## Ejemplo minimo
```css
/* Paleta mínima */
:root {
  --color-primary: #0066FF;   /* azul de marca */
  --color-primary-hover: #0052CC;
  --color-error: #D32F2F;
  --color-bg: #FFFFFF;
  --color-text: #212121;
}

/* Uso en un botón */
.button {
  background: var(--color-primary);
  color: var(--color-bg);
}
.button:hover {
  background: var(--color-primary-hover);
}
.error-msg {
  color: var(--color-error);
}
```

## Errores comunes
- **Contraste insuficiente:** usar colores que no cumplen WCAG; evitarlo probando con herramientas de contraste.  
- **Paleta excesiva:** mezclar demasiados colores y perder consistencia; limitarse a 5‑7 tonos.  
- **Significado inconsistente:** asignar el mismo color a estados diferentes; mantener una tabla de usos.  

## Estado actual
Los fundamentos del uso del color (paletas, contraste, significado y estados) son estables y se aplican en la mayoría de los sistemas de diseño. La práctica moderna incorpora tokens de color en CSS/Design Tokens y pruebas automatizadas de accesibilidad, además de adaptar paletas a modos oscuros y a consideraciones culturales.

## Conexiones
- **Visual Hierarchy:** El color refuerza la jerarquía visual al destacar elementos primarios sobre secundarios.  
- **Typography:** El contraste entre color de texto y fondo afecta la legibilidad tipográfica.  
- **Spacing & Layout:** Los bloques de color pueden crear separación visual que complementa el espaciado.

## Ruta de estudio
1. Prerrequisitos: principios básicos de percepción visual y normas WCAG de contraste.  
2. Fundamentos: crear y aplicar paletas, entender significado cultural del color.  
3. Intermedio: diseñar variantes de estado y validar contraste en diferentes dispositivos.  
4. Avanzado: implementar tokens de color, pruebas automatizadas y adaptación a modo oscuro y a mercados internacionales.

## Preguntas de repaso
1. ¿Cómo determina una paleta de colores la consistencia visual de un producto?  
2. ¿Qué ratio de contraste mínimo exige WCAG para texto normal?  
3. ¿Por qué es importante asignar significados consistentes a colores como rojo o verde?  
4. ¿Cómo se gestionan los colores de estado sin perder contraste?  
5. ¿Qué ventajas aporta el uso de Design Tokens para el color en un sistema de diseño?

<!-- trazabilidad: run_id=run-20261106-223649-6fc53c concept=08-ux-ui-14-color written_at=2026-11-07T01:37:50.648735+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]]
- [[08 - UX & UI/13 - Typography|Typography]]
- [[08 - UX & UI/15 - Spacing & Layout|Spacing & Layout]]

---
← [[08 - UX & UI/13 - Typography|Typography]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/15 - Spacing & Layout|Spacing & Layout]] →
