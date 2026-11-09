---
title: "Planning"
area: "Project Management"
numero: 9
aliases: ["Planning"]
tags: [concepto, it/project-management]
---
# Planning

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 9 de 25**

## Qué abarca
- Secuencia y organización del trabajo

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **Planning** para transformar la visión del proyecto en una hoja de ruta operativa que indique qué se hará, cuándo y por quién. Resuelvo la incertidumbre de “¿por dónde empezamos?” y alineo al equipo con los criterios de éxito definidos. Aparece en la fase inicial de cualquier proyecto que gestiono, justo antes de asignar tareas y establecer entregas. Después de comprender Planning, puedo diseñar la estructura de trabajo, estimar esfuerzos y crear un calendario realista; cuando el proyecto ya está en ejecución y el plan está aprobado, no necesito volver a preocuparte por la planificación básica, solo por su seguimiento y ajuste.

## Esqueleto (el 20% esencial)
1. **Secuencia lógica**: ordenar actividades de forma que cada una tenga sentido respecto a la anterior y la siguiente.  
2. **Organización del trabajo**: agrupar tareas en paquetes manejables (WBS) y asignar responsables.  
3. **Identificación de dependencias**: reconocer qué tareas deben completarse antes de que otras puedan iniciar.  
4. **Estimación de esfuerzo**: asignar valores de tiempo y recursos a cada paquete de trabajo.  
5. **Definición de hitos**: marcar puntos de control críticos que indican progreso y permiten decisiones de ajuste.

## Como funciona
1. Parto del **Product Roadmap** y desgloso los objetivos en un **Work Breakdown Structure** (WBS).  
2. Para cada elemento del WBS determino sus **dependencias** y establezco el orden de ejecución.  
3. Realizo **estimaciones** de esfuerzo (horas, días) usando datos históricos o técnicas de juicio experto.  
4. Con la información anterior creo un **schedule** que incluye fechas de inicio, fin y **milestones**.  
5. El plan resultante se comunica al equipo y se usa como base para el **Task Management** diario.

## Detalles
- **Básico**: definir los entregables principales y dividirlos en paquetes de trabajo (WBS).  
- **Intermedio**: mapear dependencias y aplicar técnicas de estimación (puntos de historia, PERT).  
- **Avanzado**: integrar riesgos, recursos limitados y buffers de tiempo; ajustar el schedule con herramientas de optimización y validar contra el **Product Roadmap** para asegurar alineación estratégica.

## Ejemplo minimo
```json
{
  "project": "Lanzamiento App Móvil",
  "wbs": [
    {"id": "1", "name": "Diseño UI", "estimateDays": 5},
    {"id": "2", "name": "Desarrollo Backend", "estimateDays": 10, "dependsOn": ["1"]},
    {"id": "3", "name": "Integración", "estimateDays": 3, "dependsOn": ["1","2"]},
    {"id": "4", "name": "Pruebas", "estimateDays": 4, "dependsOn": ["3"]},
    {"id": "5", "name": "Release", "estimateDays": 1, "dependsOn": ["4"], "milestone": true}
  ]
}
```

## Errores comunes
- **Ignorar dependencias**: genera cuellos de botella; evitarlo revisando siempre la tabla “dependsOn”.  
- **Subestimar esfuerzos**: provoca retrasos; usar datos históricos y técnicas de estimación múltiple.  
- **No fijar hitos claros**: dificulta el seguimiento; definir al menos un hito por fase crítica.  
- **Planificar sin validar con el roadmap**: riesgo de desalineación estratégica; revisar la coherencia antes de cerrar el plan.

## Estado actual
Los fundamentos de **Planning** (WBS, estimación y dependencias) son estables y se aplican en la mayoría de los marcos de gestión de proyectos. En la práctica moderna, se complementan con herramientas de planificación colaborativa que permiten actualizar el schedule en tiempo real y sincronizarlo con el **Product Roadmap** y los tableros de **Task Management**.

## Conexiones
- **Product Roadmap**: el Planning traduce la visión estratégica del roadmap en actividades concretas y fechas de entrega.  
- **Work Breakdown Structure**: sirve como esqueleto estructural que el Planning organiza y programa.  
- **Scheduling**: el resultado del Planning es un schedule que define cuándo se ejecutarán las tareas y se alcanzarán los hitos.

## Ruta de estudio
1. **Prerequisitos**: comprender conceptos de alcance, entregables y gestión de riesgos.  
2. **Fundamentos**: estudiar WBS, identificación de dependencias y técnicas básicas de estimación.  
3. **Práctica**: crear planes en una herramienta de gestión (Jira, MS Project) y validar contra un roadmap real.  
4. **Avanzado**: aprender a incorporar buffers, gestión de recursos y alineación continua con el roadmap.  
5. **Especialización**: explorar metodologías ágiles (Scrum, SAFe) que adaptan el Planning a ciclos iterativos.

## Preguntas de repaso
1. ¿Cómo transforma el Product Roadmap en actividades concretas dentro del Planning?  
2. ¿Qué papel juegan las dependencias al crear el schedule de un proyecto?  
3. ¿Cuál es la diferencia entre una estimación de esfuerzo y un hito?  
4. ¿Qué riesgo implica planificar sin validar contra el roadmap y cómo se evita?  
5. ¿Qué pasos seguirías para pasar de un WBS básico a un schedule con buffers de tiempo?

<!-- trazabilidad: run_id=run-20261109-172749-e195ec concept=10-project-management-09-planning written_at=2026-11-09T20:28:31.033798+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/10 - Product Roadmap|Product Roadmap]] · *Product Management*
- [[10 - Project Management/05 - Work Breakdown Structure|Work Breakdown Structure]]
- [[10 - Project Management/06 - Task Management|Task Management]]
- [[10 - Project Management/07 - Dependencies|Dependencies]]
- [[10 - Project Management/08 - Estimation|Estimation]]
- [[10 - Project Management/10 - Scheduling|Scheduling]]
- [[10 - Project Management/19 - Milestones & Releases|Milestones & Releases]]

---
← [[10 - Project Management/08 - Estimation|Estimation]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/10 - Scheduling|Scheduling]] →
