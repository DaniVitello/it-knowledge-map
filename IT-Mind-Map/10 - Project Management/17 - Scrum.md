---
title: "Scrum"
area: "Project Management"
numero: 17
aliases: ["Scrum"]
tags: [concepto, it/project-management]
---
# Scrum

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 17 de 25**

## Qué abarca
- Sprints
- backlog
- ceremonies
- roles

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Scrum para estructurar el trabajo del equipo en ciclos cortos y predecibles, lo que me permite entregar valor de forma incremental y detectar desviaciones antes de que se vuelvan críticas. Resuelvo la incertidumbre de los requisitos cambiantes y la falta de visibilidad del progreso, garantizando que el proyecto avanza alineado con los objetivos del cliente. En mi día a día como project manager senior, Scrum aparece cuando necesito coordinar a varios perfiles técnicos, priorizar funcionalidades y mantener una cadencia de entregas. Después de comprenderlo, puedo planificar releases, gestionar riesgos y facilitar la toma de decisiones basada en datos reales. No necesito preocuparme por Scrum cuando el proyecto es estático, con requisitos fijos y entregas únicas, o cuando el equipo no está dispuesto a trabajar en iteraciones.

## Esqueleto (el 20% esencial)
1. **Sprint** – ciclo de tiempo fijo (usualmente 2‑4 semanas) donde se entrega un incremento de producto.  
2. **Product Backlog** – lista priorizada de todo lo que el producto necesita, gestionada por el Product Owner.  
3. **Ceremonias** – eventos estructurados (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective) que sincronizan al equipo.  
4. **Roles** – Scrum Master (facilitador), Product Owner (visionario) y Development Team (creadores).  
5. **Definition of Done** – criterio compartido que determina cuándo un ítem está realmente terminado.

## Como funciona
1. **Planificación del Sprint**: el equipo selecciona del Product Backlog los ítems que pueden completar en el próximo Sprint, creando el Sprint Backlog.  
2. **Daily Scrum**: cada día, 15 min de sincronización para inspeccionar el progreso y ajustar el plan.  
3. **Desarrollo**: el Development Team trabaja los ítems, respetando la Definition of Done.  
4. **Sprint Review**: al final del Sprint se muestra el incremento al cliente y se recoge feedback, que alimenta el Product Backlog.  
5. **Sprint Retrospective**: el equipo reflexiona sobre el proceso y define mejoras para el siguiente Sprint.

## Detalles
- **Básico**: comprender los tres artefactos (Product Backlog, Sprint Backlog, Increment) y los cuatro eventos.  
- **Intermedio**: aplicar técnicas de estimación (Planning Poker), refinar el Backlog continuamente y usar métricas como Velocity para predecir capacidad.  
- **Avanzado**: escalar Scrum (Scrum of Scrums, Nexus), integrar DevOps para automatizar la entrega del Increment y combinar con otras metodologías ágiles (Kanban) para flujos híbridos.

## Ejemplo minimo
```yaml
# Sprint Planning (2‑week sprint)
SprintBacklog:
  - US001: "Como usuario, quiero registrarme"
  - US002: "Como usuario, quiero iniciar sesión"
DefinitionOfDone:
  - Código compilado
  - Pruebas unitarias 100 %
  - Documentación mínima
```
En la Daily Scrum cada miembro indica: *Qué hice ayer, qué haré hoy, qué bloquea*; al final del sprint el Product Owner acepta los dos user stories como “Done”.

## Errores comunes
- **Convertir la Daily en una reunión de reporte** → mantenerla enfocada en el progreso del Sprint.  
- **Sobrecargar el Sprint Backlog** → respetar la capacidad real del equipo.  
- **Ignorar la Definition of Done** → asegurar calidad y evitar “deuda técnica”.  
- **No actualizar el Product Backlog** → perder la visión del cliente y la priorización.  

## Estado actual
- **Fundamentos estables**: Sprint, Backlog, ceremonias y roles siguen siendo la base aceptada por la guía Scrum.  
- **Práctica moderna**: adopción de métricas de flujo (Lead Time, Cycle Time), integración continua y entrega continua (CI/CD) para acortar el tiempo entre “Done” y despliegue al cliente.

## Conexiones
- **Agile** – Scrum es una de las implementaciones más extendidas del enfoque Agile, compartiendo valores de colaboración y adaptación.  
- **Kanban** – se puede combinar con Kanban para visualizar el flujo de trabajo dentro del Sprint y limitar el WIP.  
- **Engineering Processes** – la Definition of Done y la entrega de Incrementes dependen de procesos de calidad, pruebas automatizadas y gestión de configuración.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de gestión de proyectos y principios Agile.  
2. **Fundamentos**: leer la Guía Scrum, practicar Scrum ceremonies en un proyecto piloto.  
3. **Intermedio**: aprender estimación de historias, métricas de rendimiento y refinamiento continuo del Backlog.  
4. **Avanzado**: estudiar escalado (Scrum of Scrums, Nexus), integración con DevOps y adaptación a entornos híbridos con Kanban.  

## Preguntas de repaso
1. ¿Cómo ayuda el Sprint Planning a alinear la capacidad del equipo con la prioridad del negocio?  
2. ¿Qué diferencia hay entre la Definition of Done y la Definition of Ready?  
3. ¿Cuál es el objetivo principal de la Sprint Retrospective y cómo se traduce en mejora continua?  
4. ¿En qué situaciones combinar Scrum con Kanban aporta valor añadido?  
5. ¿Qué métricas usarías para estimar la velocidad del equipo y predecir la entrega de un release?

<!-- trazabilidad: run_id=run-20261109-173713-24cfea concept=10-project-management-17-scrum written_at=2026-11-09T20:38:13.038133+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/30 - Engineering Processes|Engineering Processes]] · *Software Engineering*
- [[10 - Project Management/16 - Agile|Agile]]
- [[10 - Project Management/18 - Kanban|Kanban]]

---
← [[10 - Project Management/16 - Agile|Agile]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/18 - Kanban|Kanban]] →
