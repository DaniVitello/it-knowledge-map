---
title: "Agile"
area: "Project Management"
numero: 16
aliases: ["Agile"]
tags: [concepto, it/project-management]
---
# Agile

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 16 de 25**

## Qué abarca
- Iteración
- adaptación
- feedback

## Mis notas
<!-- ai:start -->
## Objetivo  
Utilizo Agile para mantener el proyecto alineado con la realidad del negocio y con la capacidad del equipo, resolviendo la incertidumbre que surge cuando los requisitos cambian o aparecen riesgos inesperados. En mi día a día como project manager senior, Agile me permite planificar en ciclos cortos, obtener feedback continuo y adaptar el alcance sin perder la visión de entrega. Después de comprender Agile, puedo estructurar sprints, priorizar el backlog y medir el progreso con métricas de valor entregado; cuando el proyecto tiene requisitos fijos y un entorno estable, puedo prescindir de la sobrecarga de ceremonias ágiles y optar por una planificación tradicional.

## Esqueleto (el 20% esencial)  
1. **Iteración** – El trabajo se divide en ciclos de tiempo fijo (sprints) que entregan incrementos funcionales.  
2. **Adaptación** – Al final de cada iteración se revisan los resultados y se ajustan el plan y el backlog.  
3. **Feedback** – Clientes y stakeholders aportan retroalimentación continua que guía la priorización.  
4. **Colaboración constante** – El equipo se reúne diariamente para sincronizarse y remover impedimentos.  
5. **Valor entregado** – Cada incremento se valida contra criterios de aceptación que representan valor de negocio.

## Como funciona  
1. **Planificación del sprint**: se seleccionan del backlog los ítems que el equipo considera completables en la iteración.  
2. **Desarrollo y daily stand‑up**: durante la iteración el equipo trabaja los ítems y se reúne cada día para compartir avances y bloquear obstáculos.  
3. **Revisión del sprint**: al cierre del ciclo se muestra el incremento a los stakeholders y se recoge su feedback.  
4. **Retrospectiva**: el equipo reflexiona sobre el proceso, identifica mejoras y las incorpora al siguiente sprint.  
5. **Re‑priorización**: el product owner actualiza el backlog con la nueva información y se repite el ciclo.

## Detalles  
- **Básico**: definir un backlog, establecer la duración de los sprints (ej. 2 weeks) y realizar daily stand‑up.  
- **Intermedio**: introducir métricas de velocidad, definir Definition of Done y usar burndown charts para visualizar el progreso.  
- **Avanzado**: escalar Agile con frameworks como SAFe o LeSS, integrar DevOps para entrega continua y aplicar técnicas de refinamiento de backlog basadas en valor de negocio.

## Ejemplo minimo  
```json
{
  "sprint": "Sprint 1",
  "duration": "2 weeks",
  "backlogItems": [
    { "id": "US-101", "description": "Login de usuario", "estimate": 5 },
    { "id": "US-102", "description": "Recuperar contraseña", "estimate": 3 }
  ],
  "dailyStandup": ["Qué hice ayer", "Qué haré hoy", "Bloqueos"]
}
```
Este bloque muestra la estructura mínima de un sprint: duración, ítems estimados y la agenda de la reunión diaria.

## Errores comunes  
- **Confundir Agile con falta de planificación** – Mantener una visión de alto nivel y un backlog priorizado evita la improvisación.  
- **Iteraciones demasiado largas** – Reducir la duración permite obtener feedback más rápido y limitar el riesgo.  
- **No cerrar el sprint con una revisión** – Sin la demo al cliente el feedback no llega y la adaptación se vuelve teórica.  
- **Sobrecargar las ceremonias** – Limitar el tiempo de stand‑up y retrospectiva mantiene la productividad.

## Estado actual  
**Fundamentos estables**: la división del trabajo en iteraciones, la retroalimentación continua y la adaptación del backlog son prácticas consolidadas en la gestión de proyectos.  
**Práctica moderna**: la integración de métricas de flujo (cumulative flow diagram), la automatización de pruebas en pipelines CI/CD y la adopción de frameworks de escalado (SAFe, LeSS) son tendencias actuales que complementan el núcleo ágil.

## Conexiones  
- **Engineering Processes**: Agile provee un marco de trabajo que guía la ejecución de procesos de ingeniería, asegurando que el desarrollo se alinee con entregas incrementales.  
- **Scrum**: es una implementación concreta de Agile que estructura la iteración, los roles y las ceremonias descritas.  
- **Kanban**: comparte con Agile el enfoque en flujo y visualización, y puede combinarse con Scrum para gestionar el trabajo en curso.

## Ruta de estudio  
1. **Prerequisitos**: conceptos básicos de gestión de proyectos (alcance, cronograma, riesgos) y fundamentos de trabajo en equipo.  
2. **Fundamentos**: leer la guía de Scrum, practicar la creación y priorización de un backlog, ejecutar un sprint piloto.  
3. **Intermedio**: aprender a medir velocidad, usar burndown y cumulative flow, introducir Definition of Done.  
4. **Avanzado**: estudiar escalado Agile (SAFe, LeSS), integrar pipelines CI/CD y explorar métricas de valor de negocio.  
5. **Especialización**: certificaciones Scrum Master, Product Owner o Agile Coach según el rol deseado.

## Preguntas de repaso  
1. ¿Cómo ayuda la iteración a reducir la incertidumbre en un proyecto?  
2. ¿Qué información se recoge en la retrospectiva y cómo se utiliza en el siguiente sprint?  
3. ¿Cuál es la diferencia práctica entre un backlog priorizado y una lista de requisitos estática?  
4. ¿En qué situaciones podría ser más adecuado usar Kanban que Scrum dentro de un proyecto Agile?  
5. ¿Qué métricas utilizas para decidir si el equipo está entregando valor de forma sostenible?

<!-- trazabilidad: run_id=run-20261109-173624-4aef4f concept=10-project-management-16-agile written_at=2026-11-09T20:37:11.939278+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/30 - Engineering Processes|Engineering Processes]] · *Software Engineering*
- [[10 - Project Management/17 - Scrum|Scrum]]
- [[10 - Project Management/18 - Kanban|Kanban]]

---
← [[10 - Project Management/15 - Change Management|Change Management]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/17 - Scrum|Scrum]] →
