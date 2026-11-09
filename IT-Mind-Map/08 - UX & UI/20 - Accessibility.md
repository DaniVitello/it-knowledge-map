---
title: "Accessibility"
area: "UX / UI"
numero: 20
aliases: ["Accessibility"]
tags: [concepto, it/ux-ui]
---
# Accessibility

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 20 de 25**

## Qué abarca
- WCAG
- teclado
- contraste
- screen readers

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la accesibilidad para que cualquier persona, sin importar sus capacidades físicas o sensoriales, pueda interactuar con la interfaz de forma eficaz. Resuelvo el problema de exclusión que surge cuando los diseños solo consideran a usuarios sin limitaciones, garantizando que los flujos de trabajo, los controles y la información sean percibibles y operables para todos. En mi día a día como diseñador de producto senior, la accesibilidad aparece al validar prototipos, al crear guías de estilo y al revisar los entregables de desarrollo. Después de comprenderla, puedo definir criterios de aceptación inclusivos, priorizar mejoras y comunicar su valor a los stakeholders. Sólo dejo de enfocarme en ella cuando el producto está destinado a un entorno controlado donde los usuarios comparten exactamente el mismo perfil de capacidad, lo cual es raro en la práctica.

## Esqueleto (el 20% esencial)
1. **WCAG como referencia mínima** – Las pautas de WCAG establecen criterios medibles (por ejemplo, contraste de 4.5:1) que guían decisiones de diseño accesible.  
2. **Navegación con teclado** – Todos los componentes interactivos deben ser alcanzables y operables mediante tabulación y atajos, sin depender de un puntero.  
3. **Contraste visual suficiente** – El texto y los elementos gráficos necesitan una relación de contraste que garantice legibilidad en distintas condiciones de visión.  
4. **Screen readers y atributos ARIA** – Proveer descripciones semánticas (aria‑label, role) permite que los lectores de pantalla transmitan la información a usuarios ciegos.  

## Como funciona
1. **Reviso los requisitos WCAG** y determino el nivel de conformidad (A, AA) que el proyecto debe alcanzar.  
2. **Evalúo el flujo con solo teclado**, asegurándome de que el orden de tabulación siga la lógica del usuario y que no haya “trampas” de foco.  
3. **Mido el contraste** entre texto y fondo usando herramientas de inspección; ajusto colores hasta cumplir la relación mínima.  
4. **Inyecto atributos ARIA** donde la semántica HTML no sea suficiente (por ejemplo, botones personalizados) y pruebo con un lector de pantalla para confirmar la narración.  
5. **Itero**: después de cada ajuste, vuelvo a validar WCAG, teclado, contraste y lectores para cerrar cualquier brecha.

## Detalles
- **Básico**: aplicar colores con contraste suficiente y usar etiquetas HTML nativas (button, input) que ya son accesibles.  
- **Intermedio**: crear un mapa de foco, usar `tabindex` de forma controlada y añadir `aria‑label` a iconos sin texto.  
- **Avanzado**: diseñar componentes complejos (modales, menús desplegables) con gestión de foco dinámico, roles ARIA avanzados y pruebas automatizadas de accesibilidad integradas en CI.

## Ejemplo minimo
```html
<!-- Botón accesible con contraste y descripción para screen reader -->
<button style="background:#0066cc;color:#fff;padding:8px 12px;">
  <span aria-hidden="true">🔍</span>
  <span class="sr-only">Buscar</span>
</button>

<style>
  .sr-only {
    position:absolute;
    width:1px;height:1px;
    padding:0;margin:-1px;
    overflow:hidden;clip:rect(0,0,0,0);
    border:0;
  }
</style>
```

## Errores comunes
- **Confiar solo en colores** para transmitir información; evitarlo añadiendo texto o íconos descriptivos.  
- **Olvidar el orden de foco**; revisarlo con la tecla Tab y corregir `tabindex`.  
- **Usar ARIA innecesario**; prefiera elementos nativos antes de añadir roles o atributos.  
- **No probar con lectores de pantalla**; validar con VoiceOver o NVDA para detectar fallas.  

## Estado actual
- **Fundamentos estables**: WCAG 2.1 sigue siendo la referencia principal; los principios de contraste, teclado y semántica HTML son ampliamente aceptados.  
- **Práctica moderna**: la integración de pruebas de accesibilidad en pipelines de CI, el uso de herramientas como axe-core y la adopción de componentes UI que exponen APIs accesibles por defecto están ganando terreno.

## Conexiones
- **Usabilidad**: una interfaz usable necesita que los usuarios puedan completar tareas sin fricción; la accesibilidad elimina barreras que afectan la usabilidad.  
- **Diseño de interacción**: los patrones de interacción deben considerar tanto gestos como atajos de teclado para ser inclusivos.  
- **Desarrollo front‑end**: los desarrolladores implementan los requisitos de accesibilidad mediante HTML semántico, CSS para contraste y JavaScript para gestión de foco.

## Ruta de estudio
1. **Prerequisitos**: conocer los principios básicos de UX, manejo de HTML5 y CSS.  
2. **Fundamentos**: estudiar WCAG 2.1 (niveles A y AA) y practicar con herramientas de contraste y auditoría de foco.  
3. **Intermedio**: aprender atributos ARIA y probar con lectores de pantalla (VoiceOver, NVDA).  
4. **Avanzado**: integrar pruebas automáticas (axe, pa11y) en CI, crear componentes UI accesibles y liderar auditorías de accesibilidad en proyectos.  

## Preguntas de repaso
1. ¿Qué criterios de contraste establece WCAG para texto normal y cómo los verifico?  
2. ¿Cómo garantizo que un modal sea navegable con solo el teclado?  
3. ¿Cuándo es apropiado usar `aria-label` en lugar de texto visible?  
4. ¿Qué diferencia hay entre los niveles A y AA de WCAG y qué nivel suele requerir un producto comercial?  
5. ¿Cuál es el beneficio de incluir pruebas de accesibilidad en el pipeline de CI?

<!-- trazabilidad: run_id=run-20261106-203119-dc2829 concept=08-ux-ui-20-accessibility written_at=2026-11-06T23:32:29.519594+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/20 - Accesibilidad|Accesibilidad]] · *Frontend*

---
← [[08 - UX & UI/19 - Responsive Design|Responsive Design]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/21 - Usability|Usability]] →
