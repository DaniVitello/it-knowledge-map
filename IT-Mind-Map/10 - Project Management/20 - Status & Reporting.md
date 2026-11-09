---
title: "Status & Reporting"
area: "Project Management"
numero: 20
aliases: ["Status & Reporting"]
tags: [concepto, it/project-management]
---
# Status & Reporting

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 20 de 25**

## Qué abarca
- Estado
- progreso
- bloqueos

## Mis notas
<!-- ai:start -->
## Objetivo  
Utilizo **Status & Reporting** para mantener a todos los involucrados al tanto del estado real del proyecto, detectar rápidamente los bloqueos y medir el progreso contra el plan. Resuelvo la falta de visibilidad que genera incertidumbre y retrasa la toma de decisiones. Aparece en cada fase del proyecto, desde la planificación inicial hasta la entrega final, y me permite ajustar recursos o prioridades antes de que los problemas se agraven. Después de comprenderlo, puedo diseñar informes que sirvan de base para reuniones de seguimiento, escalamiento de riesgos y cierre de proyecto. No necesito preocuparme cuando el proyecto es tan pequeño que la comunicación informal cubre todas las necesidades de seguimiento.

## Esqueleto (el 20% esencial)  
1. **Estado** – descripción actual de cada entregable o actividad (ej. “En progreso”, “Completado”, “Bloqueado”).  
2. **Progreso** – medida cuantitativa (porcentaje, puntos de historia) que indica cuánto se ha avanzado respecto al plan.  
3. **Bloqueos** – impedimentos que impiden avanzar y requieren intervención de stakeholders o re‑planificación.  

## Como funciona  
1. Defino los indicadores de estado y progreso que el equipo usará (p. ej., “% completado” y “Riesgo”).  
2. Cada día o sprint, el equipo actualiza su tabla de status con el valor actual y describe cualquier bloqueo.  
3. Compilo esas actualizaciones en un reporte estándar (dashboard, email o documento).  
4. Distribuyo el reporte a los stakeholders y lo discuto en la reunión de seguimiento.  
5. En base a la información, tomo decisiones: reasigno recursos, ajusto el alcance o escalo el bloqueo.

## Detalles  
- **Básico:** Uso una hoja de cálculo con columnas : Actividad, Estado, % Progreso, Bloqueo.  
- **Intermedio:** Automatizo la recolección de datos con herramientas de gestión (Jira, Azure DevOps) y genero gráficos de burn‑down y de riesgos.  
- **Avanzado:** Integro el reporting en un portal de gestión de portafolio, enlazando métricas de calidad y coste, y habilito alertas automáticas cuando el % Progreso cae bajo el umbral planificado.

## Ejemplo minimo  
```json
{
  "Sprint 5": {
    "Feature A": { "estado": "En progreso", "progreso": 60, "bloqueo": "" },
    "Feature B": { "estado": "Bloqueado", "progreso": 30, "bloqueo": "Dependencia externa" },
    "Feature C": { "estado": "Completado", "progreso": 100, "bloqueo": "" }
  }
}
```

## Errores comunes  
- Reportar solo el % Progreso sin indicar el estado real → se ocultan bloqueos.  
- Actualizar el reporte de forma esporádica → la información pierde valor para la toma de decisiones.  
- Usar terminología distinta entre equipos → genera confusión en la interpretación.  

## Estado actual  
**Fundamentos estables:** la práctica de registrar estado, progreso y bloqueos en un formato regular es una norma aceptada en la gestión de proyectos ágil y tradicional.  
**Práctica moderna:** la mayoría de los equipos utilizan dashboards interactivos y alertas automáticas integradas en herramientas de seguimiento, lo que reduce el tiempo de consolidación manual y mejora la rapidez de respuesta ante desviaciones.

## Conexiones  
- **Stakeholder Management** – los reportes son el canal principal para mantener informados a los patrocinadores y obtener su apoyo en la resolución de bloqueos.  
- **Team Coordination** – la actualización diaria del status sirve como base para la sincronización del equipo y la planificación de tareas.  
- **Risk Management** – los bloqueos identificados en los reportes se convierten en riesgos que deben ser evaluados y mitigados.

## Ruta de estudio  
1. **Prerequisitos:** conceptos de planificación de proyectos, definición de entregables y uso básico de una herramienta de seguimiento (Jira, Trello).  
2. **Fundamentos:** crear y mantener una tabla de status, interpretar % Progreso y reconocer bloqueos.  
3. **Intermedio:** generar dashboards y automatizar la recolección de datos.  
4. **Avanzado:** integrar reporting con gestión de riesgos y coste, y configurar alertas proactivas.  

## Preguntas de repaso  
1. ¿Qué información esencial debe contener cada fila de un reporte de status?  
2. ¿Cómo ayuda el reporte de bloqueos a la gestión de riesgos?  
3. ¿Cuál es la diferencia entre actualizar el estado y actualizar el progreso?  
4. ¿Qué ventaja aporta la automatización del reporting frente a la hoja de cálculo manual?  
5. ¿En qué momento puedes prescindir de un reporte formal y confiar en la comunicación informal?

<!-- trazabilidad: run_id=run-20261109-180021-ab077a concept=10-project-management-20-status-reporting written_at=2026-11-09T21:01:30.455250+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/21 - Stakeholder Management|Stakeholder Management]]
- [[10 - Project Management/22 - Team Coordination|Team Coordination]]

---
← [[10 - Project Management/19 - Milestones & Releases|Milestones & Releases]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/21 - Stakeholder Management|Stakeholder Management]] →
