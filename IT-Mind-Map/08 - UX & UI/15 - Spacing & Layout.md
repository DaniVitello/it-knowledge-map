---
title: "Spacing & Layout"
area: "UX / UI"
numero: 15
aliases: ["Spacing & Layout"]
tags: [concepto, it/ux-ui]
---
# Spacing & Layout

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 15 de 25**

## Qué abarca
- Grid
- spacing systems
- composición

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el sistema de spacing y layout para organizar visualmente los componentes de una interfaz, garantizando que la información se perciba de forma clara y que la interacción sea fluida. Resuelvo problemas de desorden visual, ambigüedad en la jerarquía y dificultad para escalar diseños a diferentes tamaños de pantalla. Aparece en cada fase del trabajo de un diseñador de producto senior: desde la creación de wireframes hasta la entrega de especificaciones de alta fidelidad. Después de entenderlo, puedo diseñar sistemas consistentes que aceleren la colaboración con desarrolladores y reduzcan la necesidad de ajustes posteriores. No necesito preocuparme cuando el proyecto es un prototipo de baja fidelidad que no será implementado o cuando el producto ya está bajo un sistema de diseño rígido que impone sus propias reglas de espaciado.

## Esqueleto (el 20% esencial)
1. **Grid** – estructura de columnas y filas que define dónde colocar los elementos y cómo alinearlos.  
2. **Spacing system** – escala de márgenes y paddings (por ejemplo 4‑8‑16‑32 px) que se aplica de forma coherente en todo el producto.  
3. **Composición** – organización de bloques de contenido dentro del grid, equilibrando densidad y respiración visual.  
4. **Consistencia responsiva** – adaptación del grid y del spacing a diferentes breakpoints sin romper la jerarquía.  
5. **Relación con la tipografía** – el espaciado vertical entre bloques de texto sigue la escala tipográfica para mantener ritmo visual.

## Como funciona
1. Defino el número de columnas y el gutter (espacio entre columnas) según el contenido y el contexto del producto.  
2. Selecciono la escala de spacing del sistema de diseño y la aplico a márgenes y paddings de los componentes.  
3. Distribuyo los componentes en el grid respetando la escala, alineando bordes y creando “gutters” visuales.  
4. Ajusto los valores de spacing en los breakpoints para que la composición siga siendo legible y equilibrada en móviles, tablets y desktop.  
5. Verifico que la distancia entre bloques de texto y entre elementos interactivos siga la regla de la tipografía, reforzando la jerarquía visual.

## Detalles
- **Básico:** elegir una cuadrícula de 8‑columnas y una escala de spacing basada en 8 px. Aplicar márgenes uniformes a contenedores principales.  
- **Intermedio:** crear variantes de columnas (por ejemplo 4‑4‑4 o 6‑6) para secciones con diferentes prioridades, y usar “nested grids” para componentes complejos. Introducir “spacing tokens” en el sistema de diseño para que desarrolladores los consuman directamente.  
- **Avanzado:** combinar grids flexibles (CSS Grid) con utilities de spacing dinámico (CSS variables) que respondan a la densidad de contenido. Implementar “layout shift detection” para asegurar que los cambios de spacing no generen saltos inesperados en la UI.

## Ejemplo minimo
```html
<!-- Grid de 4 columnas con spacing de 16 px -->
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px;">
  <div style="background:#e0f7fa; padding:16px;">Card 1</div>
  <div style="background:#e0f7fa; padding:16px;">Card 2</div>
  <div style="background:#e0f7fa; padding:16px;">Card 3</div>
  <div style="background:#e0f7fa; padding:16px;">Card 4</div>
</div>
```

## Errores comunes
- Usar valores de spacing arbitrarios en lugar de la escala definida; se evita manteniendo una tabla de tokens.  
- Ignorar el gutter del grid y colocar componentes directamente en los bordes; se corrige alineando siempre a la cuadrícula.  
- Cambiar el spacing entre breakpoints sin probar la legibilidad; se evita con pruebas de usabilidad responsiva.  
- Mezclar unidades (px, em, rem) sin una regla clara; se soluciona estandarizando en rem y vinculando a la escala tipográfica.  

## Estado actual
**Fundamentos estables:** la idea de un grid estructurado y una escala de spacing coherente sigue siendo la base de los sistemas de diseño modernos.  
**Práctica moderna:** el uso de CSS Grid y variables CSS para generar spacing dinámico, así como la integración de tokens de diseño en herramientas de desarrollo (Figma Tokens, Storybook) son tendencias consolidadas en la industria.

## Conexiones
- **Visual Hierarchy:** el spacing define la separación entre niveles de información, reforzando qué elementos deben captar la atención primero.  
- **Typography:** la escala de spacing vertical se alinea con la línea base y los leading de la tipografía para crear un ritmo legible.  
- **Color:** los bloques de color se delimitan mediante spacing, evitando que áreas de fondo se mezclen y manteniendo claridad visual.

## Ruta de estudio
1. **Prerequisitos:** comprender principios básicos de alineación, márgenes y paddings; familiarizarse con CSS Grid y Flexbox.  
2. **Fundamentos:** estudiar guías de sistemas de diseño (Material, Carbon) que describen grids y spacing systems.  
3. **Práctica:** crear un layout simple en Figma aplicando una escala de 8 px y exportar los tokens a código.  
4. **Avanzado:** implementar el layout con CSS Grid y variables CSS, probar en varios breakpoints y medir “layout shift”.  
5. **Especialización:** explorar herramientas de token management (Style Dictionary) y patrones de composición responsiva en aplicaciones reales.

## Preguntas de repaso
1. ¿Cómo influye la escala de spacing en la percepción de la jerarquía visual?  
2. ¿Qué pasos seguirías para adaptar un grid de 12 columnas a una pantalla móvil?  
3. ¿Por qué es importante alinear los bloques de texto al grid mediante la escala tipográfica?  
4. ¿Cuál es la diferencia entre gutter y padding dentro de un layout?  
5. ¿Cómo evitarías que los cambios de spacing generen “layout shift” en producción?

<!-- trazabilidad: run_id=run-20261106-202624-14c8a3 concept=08-ux-ui-15-spacing-layout written_at=2026-11-06T23:27:25.310204+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]]
- [[08 - UX & UI/13 - Typography|Typography]]
- [[08 - UX & UI/14 - Color|Color]]

---
← [[08 - UX & UI/14 - Color|Color]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/16 - Design Systems|Design Systems]] →
