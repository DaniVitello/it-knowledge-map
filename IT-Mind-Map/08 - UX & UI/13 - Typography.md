---
title: "Typography"
area: "UX / UI"
numero: 13
aliases: ["Typography"]
tags: [concepto, it/ux-ui]
---
# Typography

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 13 de 25**

## Qué abarca
- Tipografía
- escala
- legibilidad
- jerarquía

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la tipografía para transformar texto en una herramienta de comunicación visual que guía al usuario, mejora la legibilidad y refuerza la jerarquía de la información. Resuelvo el problema de que el contenido escrito sea difícil de escanear o interpretar, especialmente en interfaces con mucho texto o con diferentes niveles de importancia. Aparece en cada pantalla que contiene etiquetas, botones, encabezados o cuerpos de texto, y es una de mis primeras decisiones al crear un mockup o un prototipo de alta fidelidad. Después de dominarla, puedo definir sistemas de escala tipográfica, combinar fuentes de forma coherente y alinear la tipografía con la identidad de marca. No necesito preocuparme de la tipografía cuando el proyecto usa componentes predefinidos de un design system que ya establecen la escala y los estilos.

## Esqueleto (el 20% esencial)
1. **Escala tipográfica** – Define tamaños relativos (por ejemplo, 12 px, 16 px, 24 px) que crean una progresión visual clara.  
2. **Legibilidad** – Garantiza que el texto sea fácil de leer mediante contraste adecuado, interlineado y longitud de línea.  
3. **Jerarquía visual** – Usa variaciones de peso, tamaño y estilo para señalar la importancia de cada elemento textual.  
4. **Consistencia de familia** – Selecciona una o dos familias tipográficas que se complementen y mantengan la coherencia en todo el producto.  

## Como funciona
1. **Analizo el contenido** y determino cuántos niveles de información (título, subtítulo, cuerpo, microcopy) necesita la pantalla.  
2. **Establezco una escala** asignando un tamaño base y calculando múltiplos (por ejemplo, 1 rem, 1.25 rem, 1.5 rem).  
3. **Aplico estilos de peso y estilo** (regular, bold, italic) para diferenciar cada nivel y reforzar la jerarquía.  
4. **Ajusto interlineado y tracking** para maximizar la legibilidad según el ancho del contenedor.  
5. **Valido en diferentes dispositivos** asegurándome de que la escala sea responsiva y mantenga la claridad.

## Detalles
- **Básico:** Selección de una familia legible, definición del tamaño de cuerpo (p.ej., 16 px) y uso de negrita para encabezados.  
- **Intermedio:** Creación de una escala modular (p.ej., 4:5 ratio), ajuste de line‑height (1.4 – 1.6) y uso de variantes de peso para sub‑niveles.  
- **Avanzado:** Implementación de variables CSS para la escala, tipografía variable (variable fonts) que permite ajustes dinámicos, y pruebas de accesibilidad de contraste y tamaño mínimo en diferentes contextos de uso.

## Ejemplo minimo
```html
<!-- Tipografía mínima con escala modular -->
<style>
  :root {
    --font-base: 1rem;               /* 16px */
    --scale-ratio: 1.25;
  }
  body { font-family: "Inter", sans-serif; font-size: var(--font-base); line-height: 1.5; }
  h1 { font-size: calc(var(--font-base) * var(--scale-ratio) * var(--scale-ratio)); font-weight: 700; }
  p  { margin-top: 0.5rem; }
</style>

<h1>Guía de estilo</h1>
<p>Este texto muestra la escala tipográfica básica.</p>
```

## Errores comunes
- Usar demasiadas familias tipográficas → limita la coherencia; elijo una principal y una de apoyo.  
- Ignorar el contraste entre texto y fondo → dificulta la lectura; verifico con herramientas de accesibilidad.  
- Aplicar tamaños absolutos sin considerar la responsividad → rompe la jerarquía en móviles; utilizo unidades relativas (rem, em).  

## Estado actual
**Fundamentos estables:** La necesidad de una escala tipográfica clara, la importancia del contraste y la legibilidad, y la práctica de limitar familias tipográficas siguen siendo principios aceptados.  
**Práctica moderna:** El uso de variable fonts para ajustar peso y ancho en tiempo real, y la integración de sistemas de diseño que exponen la escala tipográfica como tokens CSS, son tendencias actuales adoptadas por equipos de producto avanzados.

## Conexiones
- **Visual Hierarchy** – La tipografía define niveles de importancia que estructuran la jerarquía visual de la interfaz.  
- **Color** – El contraste de color entre texto y fondo es esencial para la legibilidad y refuerza la distinción jerárquica.  
- **Spacing & Layout** – El interlineado y los márgenes alrededor del texto interactúan con el espaciado general para crear una composición equilibrada.

## Ruta de estudio
1. **Prerequisitos:** Conocer los principios básicos de usabilidad y tener nociones de CSS (font‑family, font‑size, line‑height).  
2. **Fundamentos:** Estudiar escalas tipográficas (modular, perfecta) y pruebas de legibilidad (WCAG contrast).  
3. **Intermedio:** Practicar la creación de tokens tipográficos en un design system y usar variable fonts.  
4. **Avanzado:** Implementar tipografía responsiva con media queries y explorar herramientas de medición de lectura (e.g., eye‑tracking).  
5. **Especialización:** Integrar tipografía con motion design y adaptar la escala a interfaces de voz o AR/VR.

## Preguntas de repaso
1. ¿Cómo determina la escala tipográfica la jerarquía visual en una pantalla?  
2. ¿Qué ajustes de interlineado y tracking favorecen la legibilidad en bloques de texto extensos?  
3. ¿Por qué es arriesgado usar más de dos familias tipográficas en un mismo producto?  
4. ¿Cómo se puede validar que el contraste de color entre texto y fondo cumple con los estándares de accesibilidad?  
5. ¿Qué ventajas aportan las variable fonts frente a las fuentes estáticas en un design system?

<!-- trazabilidad: run_id=run-20261106-202442-de1a89 concept=08-ux-ui-13-typography written_at=2026-11-06T23:25:17.693149+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]]
- [[08 - UX & UI/14 - Color|Color]]
- [[08 - UX & UI/15 - Spacing & Layout|Spacing & Layout]]

---
← [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/14 - Color|Color]] →
