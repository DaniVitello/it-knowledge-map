---
title: "Design Systems"
area: "UX / UI"
numero: 16
aliases: ["Design Systems"]
tags: [concepto, it/ux-ui]
---
# Design Systems

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 16 de 25**

## Qué abarca
- Tokens
- componentes
- patrones y reglas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo un Design System para crear interfaces consistentes y escalables sin reinventar cada elemento visual. Resuelvo el problema de la incoherencia visual y la sobrecarga de decisiones de diseño cuando trabajo en productos con múltiples pantallas y equipos. Aparece en mi día a día al definir la paleta de colores, tipografías y componentes reutilizables que guiarán a los desarrolladores y a otros diseñadores. Después de entenderlo, puedo estructurar la UI de forma modular, acelerar la entrega de funcionalidades y mantener la calidad a lo largo del tiempo. No necesito preocuparme por el Design System cuando el producto es un prototipo rápido o una prueba de concepto aislada que no será mantenida.

## Esqueleto (el 20% esencial)
1. **Tokens** – valores atómicos (colores, espaciado, tipografía) que se usan como fuente única de verdad.  
2. **Componentes** – bloques UI reutilizables construidos a partir de tokens.  
3. **Patrones** – combinaciones de componentes que resuelven problemas de interacción comunes.  
4. **Reglas** – guías de uso que dictan cuándo y cómo aplicar tokens, componentes y patrones.  

## Como funciona
1. Defino los tokens que describen la identidad visual del producto.  
2. Creo componentes (botones, tarjetas, formularios) que consumen esos tokens.  
3. Agrupo componentes en patrones (por ejemplo, “lista de resultados”) que cubren flujos de usuario.  
4. Documentó reglas de uso (por ejemplo, “el botón primario solo se usa para la acción principal”).  
5. Cuando diseño una pantalla, selecciono patrones y componentes según las reglas, garantizando consistencia y velocidad.

## Detalles
- **Básico:** Identificar los tokens esenciales (color primario, tipografía base) y crear un pequeño set de componentes (botón, input).  
- **Intermedio:** Expandir el catálogo de componentes, introducir variantes (estado disabled, tamaños) y definir patrones de interacción (modal, tabla).  
- **Avanzado:** Automatizar la generación de código a partir de los tokens, integrar el Design System con la arquitectura frontend (por ejemplo, Storybook) y establecer procesos de gobernanza para su evolución continua.

## Ejemplo minimo
```json
// tokens.json
{
  "colorPrimary": "#0066FF",
  "spacingSmall": "8px",
  "fontBase": "Roboto, sans-serif"
}
```

```tsx
// Button.tsx (React)
import tokens from './tokens.json';

export const Button = ({label}) => (
  <button style={{
    backgroundColor: tokens.colorPrimary,
    padding: tokens.spacingSmall,
    fontFamily: tokens.fontBase,
    color: '#fff',
    border: 'none',
    borderRadius: '4px'
  }}>
    {label}
  </button>
);
```

## Errores comunes
- **Crear componentes sin basarse en tokens:** genera incoherencia visual; evitarlo manteniendo siempre la referencia a los tokens.  
- **Sobrecargar el sistema con variantes innecesarias:** dificulta su mantenimiento; limitar variantes a casos de uso reales.  
- **Ignorar las reglas de uso:** lleva a decisiones arbitrarias; documentar y revisar reglas con todo el equipo.

## Estado actual
**Fundamentos estables:** la idea de tokens, componentes y patrones como bloques reutilizables está consolidada en la práctica de diseño de productos.  
**Práctica moderna:** la integración de Design Systems con herramientas de desarrollo (Storybook, Figma Tokens) y la automatización de la sincronización entre diseño y código son tendencias ampliamente adoptadas.

## Conexiones
- **Componentización:** el Design System provee los componentes que la estrategia de componentización reutiliza en la arquitectura de la UI.  
- **Arquitectura Frontend:** los tokens y componentes del Design System se alinean con la capa de presentación de la arquitectura frontend, facilitando la consistencia entre diseño y código.  
- **UI Components:** los componentes del Design System son un subconjunto especializado de UI Components, con la diferencia de estar gobernados por un conjunto de reglas y tokens comunes.

## Ruta de estudio
1. **Prerequisitos:** fundamentos de UX research, principios de diseño visual y nociones básicas de HTML/CSS.  
2. **Fundamentos:** aprender a crear y documentar tokens; construir componentes básicos en una herramienta de diseño (Figma, Sketch).  
3. **Intermedio:** definir patrones de interacción y reglas de uso; usar Storybook para documentar componentes.  
4. **Avanzado:** integrar el Design System con pipelines de CI/CD, automatizar la exportación de tokens a código y establecer procesos de gobernanza (review, versionado).  

## Preguntas de repaso
1. ¿Qué problema de incoherencia visual resuelve un Design System en un producto con varios equipos?  
2. ¿Cómo se relacionan los tokens con los componentes dentro del sistema?  
3. ¿Cuál es la diferencia entre un componente y un patrón en un Design System?  
4. ¿Qué riesgo implica crear variantes de componentes sin validar su necesidad real?  
5. ¿De qué manera la integración con Storybook mejora la gobernanza de un Design System?

<!-- trazabilidad: run_id=run-20261106-202725-52785e concept=08-ux-ui-16-design-systems written_at=2026-11-06T23:28:29.508851+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/13 - Componentización|Componentización]] · *Frontend*
- [[02 - Frontend/25 - Arquitectura Frontend|Arquitectura Frontend]] · *Frontend*
- [[08 - UX & UI/17 - UI Components|UI Components]]

---
← [[08 - UX & UI/15 - Spacing & Layout|Spacing & Layout]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/17 - UI Components|UI Components]] →
