---
title: "Navigation"
area: "UX / UI"
numero: 7
aliases: ["Navigation"]
tags: [concepto, it/ux-ui]
---
# Navigation

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 7 de 25**

## Qué abarca
- Menús
- jerarquías
- breadcrumbs
- navegación global/local

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la navegación para guiar al usuario a través del producto, asegurando que encuentre la información o la función que necesita sin perderse. Resuelvo la confusión que surge cuando la estructura de la interfaz no refleja claramente la jerarquía del contenido ni los caminos de interacción. Aparece en cada proyecto de diseño de producto senior cuando defino la arquitectura de la información, creo los flujos de usuario y diseño los componentes visuales que permiten moverse entre pantallas. Después de entenderla, puedo estructurar menús, breadcrumbs y enlaces de forma coherente y validar su efectividad con pruebas de usabilidad. No necesito preocuparme cuando el producto es una única vista estática sin interacción de cambio de contexto.

## Esqueleto (el 20% esencial)
1. **Menús** – Agrupan enlaces a secciones principales y se presentan de forma visible y consistente.  
2. **Jerarquías** – Definen la relación de importancia entre páginas y ayudan a priorizar la información.  
3. **Breadcrumbs** – Muestran la ruta de navegación actual y permiten retroceder rápidamente.  
4. **Navegación global vs. local** – La global brinda acceso a áreas principales del producto; la local orienta dentro de una sección específica.

## Como funciona
1. Analizo la arquitectura de la información para identificar niveles de contenido.  
2. Diseño un menú global que refleje los top‑level items de la jerarquía.  
3. Dentro de cada sección, añado navegación local (sub‑menús o tabs) que siga la jerarquía interna.  
4. Inserto breadcrumbs en páginas profundas para que el usuario vea su posición y pueda volver a niveles superiores.  
5. Valido la estructura con pruebas de usabilidad, observando si los usuarios encuentran lo que buscan sin errores de ruta.

## Detalles
- **Básico**: Definir un menú principal y asegurarse de que cada enlace sea descriptivo y accesible.  
- **Intermedio**: Introducir sub‑menús y breadcrumbs, alineando la nomenclatura con la jerarquía de contenido y manteniendo la consistencia visual.  
- **Avanzado**: Implementar navegación adaptativa (responsive) que cambie de barra horizontal a drawer o bottom nav según el dispositivo, y usar patrones de navegación contextual (por ejemplo, “related links”) para reducir la carga cognitiva.

## Ejemplo minimo
```html
<nav aria-label="Navegación principal">
  <ul>
    <li><a href="/dashboard">Dashboard</a></li>
    <li><a href="/projects">Proyectos</a></li>
    <li><a href="/settings">Configuración</a></li>
  </ul>
</nav>

<!-- Breadcrumb en una página de proyecto -->
<nav aria-label="Miga de pan">
  <ol>
    <li><a href="/projects">Proyectos</a></li>
    <li><a href="/projects/42">Proyecto 42</a></li>
    <li>Detalles</li>
  </ol>
</nav>
```

## Errores comunes
- **Sobrecargar el menú** con demasiados ítems; evitarlo limitando los top‑level a 5‑7 opciones.  
- **Breadcrumbs inconsistentes** que no reflejan la verdadera jerarquía; mantenerlos sincronizados con la arquitectura.  
- **Navegación local ausente** en secciones complejas; añadir tabs o sub‑menús para reducir la profundidad de clics.  
- **Falta de adaptabilidad** en dispositivos móviles; usar patrones responsive para mantener la usabilidad.

## Estado actual
**Fundamentos estables**: los principios de jerarquía clara, consistencia visual y uso de etiquetas descriptivas siguen siendo la base de cualquier sistema de navegación.  
**Práctica moderna**: la navegación adaptativa y los patrones de “progressive disclosure” (revelado progresivo) se emplean para optimizar la experiencia en dispositivos móviles y reducir la sobrecarga cognitiva. Además, la integración de componentes de accesibilidad (ARIA roles, focus management) es ahora un requisito estándar.

## Conexiones
- **Information Architecture**: la navegación traduce la estructura de la información en componentes visuales que los usuarios pueden explorar.  
- **User Flows**: los flujos de usuario dependen de la navegación para mover al usuario de un punto a otro de manera lógica y sin fricción.  
- **Responsive Design**: la adaptación de la navegación a diferentes tamaños de pantalla es esencial para mantener la coherencia del producto en todos los dispositivos.

## Ruta de estudio
1. **Prerequisitos**: comprender los conceptos básicos de arquitectura de la información y usabilidad.  
2. **Fundamentos**: estudiar patrones de menú, jerarquía y breadcrumbs mediante guías de Nielsen Norman Group.  
3. **Práctica**: crear wireframes que incluyan navegación global y local, y probarlos con usuarios reales.  
4. **Avanzado**: aprender sobre navegación adaptativa, ARIA para accesibilidad y técnicas de “progressive disclosure”.  
5. **Especialización**: explorar casos de estudio de productos SaaS y móviles para ver cómo se resuelven desafíos específicos de navegación.

## Preguntas de repaso
1. ¿Cómo determina la jerarquía la cantidad y el orden de los ítems en un menú global?  
2. ¿En qué situaciones es más útil incluir breadcrumbs que un menú secundario?  
3. ¿Qué diferencia hay entre navegación global y local y cómo se coordinan?  
4. ¿Cuáles son los riesgos de un menú sobrecargado y cómo se pueden mitigar?  
5. ¿Cómo afecta la navegación adaptativa a la experiencia del usuario en dispositivos móviles?

<!-- trazabilidad: run_id=run-20261106-201856-c04615 concept=08-ux-ui-07-navigation written_at=2026-11-06T23:19:58.215656+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/06 - Information Architecture|Information Architecture]]
- [[08 - UX & UI/09 - User Flows|User Flows]]

---
← [[08 - UX & UI/06 - Information Architecture|Information Architecture]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/08 - Interaction Design|Interaction Design]] →
