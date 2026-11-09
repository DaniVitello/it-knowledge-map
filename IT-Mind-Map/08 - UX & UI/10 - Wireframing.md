---
title: "Wireframing"
area: "UX / UI"
numero: 10
aliases: ["Wireframing"]
tags: [concepto, it/ux-ui]
---
# Wireframing

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 10 de 25**

## Qué abarca
- Estructura antes del diseño visual

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el wireframing para estructurar la arquitectura de una pantalla antes de invertir tiempo en el diseño visual. Resuelvo la incertidumbre sobre la disposición de los elementos, la jerarquía de información y los flujos de interacción, lo que me permite validar conceptos con stakeholders y usuarios de forma rápida y económica. Aparece en la fase inicial de cualquier proyecto de producto, cuando defino la ruta de navegación y los contenedores principales. Después de dominar el wireframing, puedo pasar a crear prototipos de alta fidelidad o a definir especificaciones de interacción detalladas. Cuando el layout ya está aprobado y los requisitos son estables, ya no es necesario volver a wireframear y puedo centrarme en los detalles visuales y de animación.

## Esqueleto (el 20% esencial)
1. **Definir la estructura de contenido**: se decide qué bloques (cabecera, cuerpo, barra lateral, pie) aparecen y en qué orden.  
2. **Establecer la jerarquía visual**: se asignan tamaños y posiciones relativas para guiar la atención del usuario.  
3. **Mapear los flujos de interacción**: se indican los puntos de entrada y salida de cada pantalla mediante enlaces o anotaciones.  
4. **Mantener la simplicidad**: se usan formas básicas (rectángulos, líneas) y texto placeholder para evitar distracciones visuales.  
5. **Iterar rápidamente**: se crean versiones ligeras que pueden modificarse en minutos según feedback.

## Como funciona
1. Reúno los requisitos funcionales y de negocio.  
2. Esbozo en papel o herramienta digital los bloques principales siguiendo la idea 1 del esqueleto.  
3. Ajusto tamaños y alineaciones para reflejar la jerarquía (idea 2).  
4. Añado anotaciones que describen acciones y transiciones (idea 3).  
5. Reviso con el equipo; si algo no cuadra, modifico el esquema manteniendo la simplicidad (idea 4).  
6. Repetimos el ciclo hasta obtener un consenso rápido antes de pasar al prototipo.

## Detalles
- **Básico**: uso de papel y lápiz o herramientas de arrastrar‑y‑soltar (ej. Balsamiq). Se centra en bloques y texto placeholder.  
- **Intermedio**: incorporación de anotaciones de interacción y de métricas de usabilidad (p. ej. tiempo estimado de tarea). Se empieza a usar rejillas para alinear componentes.  
- **Avanzado**: wireframes interactivos con enlaces navegables, componentes reutilizables y documentación de decisiones de diseño. Se integran con sistemas de diseño para asegurar consistencia futura.

## Ejemplo minimo
```html
<!-- Wireframe simple de una página de login -->
<div class="wireframe">
  <header style="height:60px; background:#eee;">Logo</header>
  <main style="padding:20px;">
    <label>Usuario</label><br>
    <input type="text" placeholder="ejemplo@dominio.com"><br><br>
    <label>Contraseña</label><br>
    <input type="password" placeholder="••••••"><br><br>
    <button>Acceder</button>
  </main>
  <footer style="height:40px; background:#eee;">Enlaces de ayuda</footer>
</div>
```

## Errores comunes
- Dibujar con demasiados detalles visuales; evita usar colores o tipografías reales.  
- Ignorar la jerarquía y colocar todos los elementos al mismo nivel; prioriza la información clave.  
- No validar con usuarios o stakeholders; solicita feedback temprano y frecuente.  
- Creer que el wireframe es un entregable final; úsalo solo como paso intermedio.

## Estado actual
**Fundamentos estables**: la práctica de separar estructura de presentación y de validar flujos antes del diseño visual sigue siendo la base del proceso de diseño de productos.  
**Práctica moderna**: se prefiere el uso de herramientas colaborativas en la nube que permiten comentarios en tiempo real y la generación automática de especificaciones para desarrolladores. Además, la integración de wireframes con sistemas de diseño facilita la transición a prototipos de alta fidelidad.

## Conexiones
- **Interaction Design**: el wireframe define los puntos de interacción que luego se detallan en los patrones de Interaction Design.  
- **Prototyping**: los wireframes sirven como base para crear prototipos navegables que prueban la usabilidad antes del desarrollo.  
- **Information Architecture**: la organización de bloques en un wireframe refleja la estructura de la Information Architecture del producto.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de usabilidad, principios de layout y manejo de herramientas de dibujo digital.  
2. **Fundamento**: práctica de sketching rápido y creación de wireframes de baja fidelidad.  
3. **Intermedio**: aprendizaje de anotaciones de interacción y uso de rejillas para alineación consistente.  
4. **Avanzado**: dominio de herramientas colaborativas (Figma, Adobe XD) y generación de wireframes interactivos vinculados a sistemas de diseño.  
5. **Especialización**: integración con pruebas de usabilidad temprana y documentación de decisiones de diseño para equipos de desarrollo.

## Preguntas de repaso
1. ¿Qué problema principal resuelve el wireframing en el proceso de diseño de producto?  
2. ¿Cómo se relaciona la jerarquía visual del wireframe con la experiencia del usuario?  
3. ¿Cuál es la diferencia entre un wireframe de baja fidelidad y uno interactivo?  
4. ¿Qué error suele surgir al incluir demasiados detalles visuales y cómo se evita?  
5. ¿De qué manera el wireframe alimenta al prototyping y al Interaction Design?

<!-- trazabilidad: run_id=run-20261106-202206-63799a concept=08-ux-ui-10-wireframing written_at=2026-11-06T23:23:08.749573+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/08 - Interaction Design|Interaction Design]]
- [[08 - UX & UI/11 - Prototyping|Prototyping]]

---
← [[08 - UX & UI/09 - User Flows|User Flows]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/11 - Prototyping|Prototyping]] →
