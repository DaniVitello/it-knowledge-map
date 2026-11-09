---
title: "Kanban"
area: "Project Management"
numero: 18
aliases: ["Kanban"]
tags: [concepto, it/project-management]
---
# Kanban

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 18 de 25**

## Qué abarca
- Flow
- WIP
- cycle time

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Kanban para visualizar el flujo de trabajo y limitar la cantidad de tareas en curso, lo que me permite detectar cuellos de botella y mejorar la predictibilidad de la entrega. Resuelvo el problema de sobrecarga del equipo y la falta de claridad sobre el estado real de cada actividad, una situación frecuente al planificar sprints o al coordinar múltiples dependencias. Aparece en la fase de ejecución del proyecto, cuando el equipo necesita una herramienta ligera para gestionar el trabajo diario sin la rigidez de un backlog estructurado. Después de entender Kanban, puedo combinarlo con otras prácticas ágiles, ajustar WIP (Work In Progress) y medir el cycle time para optimizar la capacidad del equipo. No es necesario preocuparse por Kanban cuando el proyecto es extremadamente pequeño o cuando ya se usa un método de gestión de tareas que cubre todas sus funciones de forma suficiente.

## Esqueleto (el 20% esencial)
1. **Visualizar el flujo** – Un tablero con columnas que representan los estados del trabajo permite que todo el equipo vea el progreso en tiempo real.  
2. **Limitar WIP** – Establecer un máximo de tareas simultáneas por columna evita la sobrecarga y fuerza la finalización antes de iniciar nuevas actividades.  
3. **Medir cycle time** – Registrar el tiempo que una tarea tarda en pasar de “En progreso” a “Hecho” brinda datos para predecir la velocidad del equipo.  
4. **Mejorar continuamente** – Revisar regularmente el tablero y los límites de WIP permite identificar y eliminar cuellos de botella.  

## Como funciona
1. **Diseño del tablero**: creo columnas que reflejan las etapas del proceso (por ejemplo, “Por hacer”, “En progreso”, “En revisión”, “Hecho”).  
2. **Definición de límites WIP**: asigno un número máximo de tarjetas que pueden estar simultáneamente en cada columna.  
3. **Ingreso de tareas**: cada historia o actividad se representa con una tarjeta que se coloca en la columna “Por hacer”.  
4. **Desplazamiento de tarjetas**: a medida que el trabajo avanza, muevo la tarjeta al siguiente estado, respetando siempre los límites de WIP.  
5. **Recolección de datos**: registro la fecha de entrada y salida de cada columna para calcular el cycle time.  
6. **Retrospectiva**: analizo los datos y los cuellos de botella detectados, ajusto los límites WIP o modifica el flujo y repito el ciclo.

## Detalles
- **Básico**: tablero simple, límites WIP estáticos y seguimiento manual del cycle time.  
- **Intermedio**: uso de métricas como lead time, implementación de políticas explícitas (por ejemplo, “definición de listo”) y reuniones diarias de seguimiento (stand‑up).  
- **Avanzado**: integración con herramientas de automatización (por ejemplo, triggers que mueven tarjetas al cerrar pull‑request), análisis de tendencias de cycle time y simulaciones de capacidad para planificación a medio plazo.

## Ejemplo minimo
```markdown
# Kanban board (markdown)

- [ ] Por hacer
  - 📌 Tarea A
  - 📌 Tarea B
- [ ] En progreso (WIP ≤ 2)
  - 📌 Tarea C
- [ ] Hecho
```
En este ejemplo, la columna “En progreso” tiene un límite de 2 tarjetas; si ya hay dos, no se puede mover otra tarea a esa columna hasta que alguna se complete.

## Errores comunes
- **Ignorar los límites WIP** – El tablero pierde su valor predictivo; evitarlo revisando los límites en cada stand‑up.  
- **Demasiadas columnas** – Complica la visualización y ralentiza el flujo; mantener solo los estados esenciales.  
- **No medir el cycle time** – Se pierde la capacidad de estimar entregas; registrar fechas de entrada y salida de cada tarjeta.  
- **Cambiar el tablero sin consenso** – Genera confusión; acordar cualquier cambio con todo el equipo.

## Estado actual
**Fundamentos estables**: la visualización del flujo, los límites de WIP y la medición del cycle time son prácticas consolidadas y ampliamente adoptadas en la gestión de proyectos.  
**Práctica moderna**: la integración de Kanban con herramientas de CI/CD, el uso de políticas explícitas (Definition of Done) y la aplicación de análisis de datos en tiempo real para predecir la capacidad del equipo están ganando tracción en entornos ágiles avanzados.

## Conexiones
- **Engineering Processes**: Kanban se superpone con los procesos de ingeniería al proporcionar un mecanismo visual para gestionar la entrega de código, pruebas y despliegues.  
- **Agile**: Kanban es una de las metodologías ágiles que comparte valores como la entrega incremental y la mejora continua.  
- **Scrum**: aunque Scrum usa sprints, los equipos pueden combinarlo con un tablero Kanban para gestionar el trabajo dentro y fuera del sprint, creando un “Scrumban”.

## Ruta de estudio
1. **Prerequisitos**: comprender los conceptos de backlog, sprint y roles de equipo en Agile.  
2. **Fundamentos**: crear y usar un tablero Kanban básico, establecer límites WIP y medir cycle time.  
3. **Intermedio**: aprender a definir políticas de “listo” y “hecho”, y a conducir retrospectivas enfocadas en el flujo.  
4. **Avanzado**: explorar integraciones con herramientas de gestión (Jira, Azure Boards), análisis de métricas en tiempo real y técnicas de simulación de capacidad.  
5. **Especialización**: estudiar casos de Scrumban y la aplicación de Kanban en entornos de DevOps.

## Preguntas de repaso
1. ¿Cómo ayuda el límite de WIP a prevenir cuellos de botella?  
2. ¿Qué información proporciona el cycle time para la planificación del proyecto?  
3. ¿En qué situaciones combinarías Kanban con Scrum?  
4. ¿Cuál es la diferencia entre “lead time” y “cycle time” en un tablero Kanban?  
5. ¿Qué pasos seguirías para ajustar el flujo cuando una columna está constantemente sobrepasada?

<!-- trazabilidad: run_id=run-20261109-181342-10314e concept=10-project-management-18-kanban written_at=2026-11-09T21:14:47.812558+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/30 - Engineering Processes|Engineering Processes]] · *Software Engineering*
- [[10 - Project Management/16 - Agile|Agile]]
- [[10 - Project Management/17 - Scrum|Scrum]]

---
← [[10 - Project Management/17 - Scrum|Scrum]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/19 - Milestones & Releases|Milestones & Releases]] →
