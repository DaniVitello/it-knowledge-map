---
title: "Task Management"
area: "Project Management"
numero: 6
aliases: ["Task Management"]
tags: [concepto, it/project-management]
---
# Task Management

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 6 de 25**

## Qué abarca
- Tareas
- estados
- responsables

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Task Management para organizar, asignar y dar seguimiento a cada actividad que compone el proyecto, de modo que el equipo sepa qué hacer, cuándo y quién es responsable. Resuelvo la falta de visibilidad y el riesgo de que tareas críticas se pierdan o se retrasen, garantizando que el progreso sea medible y que los entregables se alineen con los hitos del proyecto. Aparece en la fase de planificación y se mantiene activo durante la ejecución, sirviendo de base para la coordinación diaria y la generación de reportes de estado. Después de entenderlo, puedo diseñar tableros de trabajo, definir flujos de estados y establecer métricas de desempeño; cuando el proyecto está bajo control y las tareas están automatizadas, no necesito enfocarme en los detalles de gestión de tareas.

## Esqueleto (el 20% esencial)
1. **Descomposición de trabajo** – Cada entrega se divide en tareas concretas (Work Breakdown Structure).  
2. **Asignación de responsables** – Cada tarea tiene un dueño claro que la ejecuta y la reporta.  
3. **Estados de la tarea** – Se define un ciclo (por ejemplo: To‑Do, In Progress, Done) que refleja su progreso.  
4. **Dependencias** – Algunas tareas no pueden iniciarse hasta que otras se completen.  
5. **Estimación y planificación** – Se estima el esfuerzo de cada tarea para construir el cronograma (Scheduling).

## Como funciona
1. Partiendo del WBS, identifico todas las tareas necesarias para cada entrega.  
2. Asigno a cada tarea un responsable según habilidades y carga de trabajo.  
3. Defino los estados que la tarea atravesará y los registro en la herramienta de gestión.  
4. Establezco dependencias entre tareas para evitar bloqueos y ordenar el flujo de trabajo.  
5. Estimo el esfuerzo (horas o story points) y, usando esas estimaciones, genero el cronograma del proyecto.  
6. Durante la ejecución, el equipo actualiza el estado de sus tareas, lo que permite al project manager monitorizar el avance y re‑planificar si surge alguna desviación.

## Detalles
- **Básico**: Crear una lista de tareas, asignar un responsable y marcar su estado.  
- **Intermedio**: Añadir dependencias y usar estimaciones para calcular la ruta crítica y ajustar el calendario.  
- **Avanzado**: Integrar métricas de velocidad, aplicar límites de WIP (Work In Progress) y automatizar notificaciones cuando una tarea cambia de estado o se rompe una dependencia.

## Ejemplo minimo
```yaml
# Tablero Kanban sencillo (formato YAML)
tasks:
  - id: T1
    name: "Diseñar mockups de la pantalla de login"
    owner: Ana
    estimate: 8h
    state: To-Do
    depends_on: []
  - id: T2
    name: "Implementar API de autenticación"
    owner: Luis
    estimate: 12h
    state: To-Do
    depends_on: [T1]
```

## Errores comunes
- **Asignar tareas sin definir claramente el responsable** → genera confusión; evitarlo asignando siempre un dueño.  
- **Olvidar dependencias** → produce bloqueos inesperados; revisa siempre la cadena de precedencia.  
- **No actualizar el estado** → pierde visibilidad; establece recordatorios diarios de actualización.  
- **Sobre‑estimar sin validar** → distorsiona el cronograma; usa datos históricos para calibrar estimaciones.

## Estado actual
Los fundamentos del Task Management (descomposición, asignación, estados y dependencias) son estables y se aplican en la mayoría de los marcos de trabajo ágiles y tradicionales. En la práctica moderna, se complementa con tableros digitales (Jira, Azure Boards, Trello) que automatizan flujos, integran métricas de velocidad y permiten reportes en tiempo real.

## Conexiones
- **Work Breakdown Structure**: provee la jerarquía de entregas que se desglosan en tareas gestionadas.  
- **Dependencies**: determinan el orden de ejecución y evitan que una tarea empiece antes de que su predecesora esté completa.  
- **Scheduling**: utiliza estimaciones de tareas para construir el cronograma y asignar recursos de forma equilibrada.

## Ruta de estudio
1. **Prerequisitos**: comprender los conceptos de alcance del proyecto y de WBS.  
2. **Fundamentos**: aprender a crear y asignar tareas, definir estados y registrar dependencias en una herramienta básica.  
3. **Intermedio**: practicar estimación de esfuerzo y generación de cronogramas con técnicas como PERT o Critical Path.  
4. **Avanzado**: dominar tableros digitales, métricas de velocidad, límites de WIP y automatizaciones de notificaciones.  
5. **Especialización**: explorar integraciones con gestión de riesgos y control de calidad.

## Preguntas de repaso
1. ¿Cómo transforma el Task Management la visión abstracta del alcance en acciones concretas para el equipo?  
2. ¿Qué ocurre si una tarea crítica no tiene dependencias definidas y se retrasa?  
3. ¿Cuál es la diferencia entre estimar en horas y estimar en story points dentro del Task Management?  
4. ¿Cómo ayuda la actualización de estados a detectar desviaciones en el cronograma?  
5. ¿Qué beneficio aporta limitar el WIP (Work In Progress) en un tablero de tareas?

<!-- trazabilidad: run_id=run-20261109-171234-b103ca concept=10-project-management-06-task-management written_at=2026-11-09T20:13:38.376156+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/05 - Work Breakdown Structure|Work Breakdown Structure]]
- [[10 - Project Management/07 - Dependencies|Dependencies]]
- [[10 - Project Management/08 - Estimation|Estimation]]
- [[10 - Project Management/09 - Planning|Planning]]
- [[10 - Project Management/10 - Scheduling|Scheduling]]

---
← [[10 - Project Management/05 - Work Breakdown Structure|Work Breakdown Structure]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/07 - Dependencies|Dependencies]] →
