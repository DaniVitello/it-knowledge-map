---
title: "Requirements"
area: "Project Management"
numero: 3
aliases: ["Requirements"]
tags: [concepto, it/project-management]
---
# Requirements

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 3 de 25**

## Qué abarca
- Qué debe entregarse

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los **requirements** para definir con claridad qué debe entregarse al cliente y al equipo, evitando malentendidos que retrasen el proyecto. Resuelvo el problema de ambigüedad en la planificación, garantizando que el alcance (scope) y los entregables (deliverables) estén alineados con las expectativas del negocio. Aparecen en la fase de iniciación y en la elaboración del plan de proyecto, donde sirvan de base para estimar tiempo, costo y recursos. Después de comprenderlos, puedo estructurar el backlog, priorizar el trabajo y validar cada incremento contra lo acordado. No necesito preocuparme por los requirements cuando el proyecto es puramente de mantenimiento interno sin requisitos externos definidos.

## Esqueleto (el 20% esencial)
1. **Qué debe entregarse**: descripción concreta del producto o servicio que el proyecto debe producir.  
2. **Alineación con el alcance**: los requirements delimitan el scope y evitan la expansión no controlada.  
3. **Base para estimación y planificación**: sirven para calcular esfuerzo, costo y calendario.  
4. **Comunicación con stakeholders**: actúan como contrato verbal/escrito entre cliente y equipo.  
5. **Criterio de aceptación**: cada requirement incluye condiciones que deben cumplirse para considerarse completado.

## Como funciona
1. **Recopilación** – Reúno información de usuarios, patrocinadores y regulaciones.  
2. **Formalización** – Redacto cada requirement de forma clara, medible y verificable.  
3. **Validación** – Los reviso con los stakeholders para confirmar que reflejan sus necesidades.  
4. **Priorización** – Asigno valor de negocio y riesgo, definiendo el orden de implementación.  
5. **Desglose** – Transformo los requirements en User Stories o tareas técnicas que alimentan el backlog.  
6. **Seguimiento** – Durante la ejecución, comparo el trabajo realizado con los criterios de aceptación y actualizo el estado de cada requirement.

## Detalles
- **Básico**: identificar quiénes son los stakeholders y registrar sus expectativas en frases simples.  
- **Intermedio**: aplicar criterios SMART (Specific, Measurable, Achievable, Relevant, Time‑bound) y crear una matriz de trazabilidad entre requirements y entregables.  
- **Avanzado**: gestionar cambios mediante un proceso de control de versiones, integrar requisitos no funcionales (seguridad, rendimiento) y usar herramientas de gestión de requisitos para automatizar la trazabilidad y la generación de pruebas de aceptación.

## Ejemplo minimo
```json
{
  "requirementId": "REQ-001",
  "description": "El sistema debe permitir al usuario registrar una cuenta con email y contraseña.",
  "type": "Functional",
  "priority": "High",
  "acceptanceCriteria": [
    "El formulario valida formato de email.",
    "La contraseña requiere al menos 8 caracteres."
  ]
}
```

## Errores comunes
- **Ambigüedad**: redactar requisitos vagos genera interpretaciones distintas; evitarlo usando lenguaje preciso y medible.  
- **Sobrecarga**: incluir demasiados detalles técnicos en los requirements; mantenerlos enfocados en el “qué”, no en el “cómo”.  
- **Falta de trazabilidad**: no enlazar requisitos con entregables o pruebas; usar una matriz de trazabilidad para prevenirlo.  
- **Ignorar cambios**: no actualizar los requirements cuando cambian las necesidades del negocio; establecer un proceso de gestión de cambios.

## Estado actual
- **Fundamentos estables**: la necesidad de definir qué debe entregarse, la alineación con el scope y la validación con stakeholders son prácticas consolidadas en la gestión de proyectos.  
- **Práctica moderna**: la adopción de herramientas de gestión de requisitos (Jira, Azure DevOps, DOORS) y la integración continua de requisitos con pruebas automatizadas son tendencias actuales que mejoran la trazabilidad y la calidad del entregable.

## Conexiones
- **User Stories**: los requirements se desglosan en User Stories que el equipo de desarrollo implementa en sprints.  
- **Scope**: el conjunto de requirements define el alcance del proyecto y sirve para controlar la expansión del mismo.  
- **Deliverables**: cada deliverable debe cumplir con los requirements asociados, garantizando que el producto final satisface lo acordado.

## Ruta de estudio
1. **Prerequisitos**: comprender los conceptos de stakeholder, scope y entregables.  
2. **Fundamentos**: estudiar técnicas de captura de requisitos (entrevistas, workshops) y criterios SMART.  
3. **Herramientas**: aprender a usar un gestor de requisitos (p. ej., Jira) y a crear trazabilidad.  
4. **Avanzado**: profundizar en requisitos no funcionales, gestión de cambios y automatización de pruebas de aceptación.  
5. **Especialización**: explorar metodologías ágiles (Scrum, SAFe) y su relación con el backlog de requisitos.

## Preguntas de repaso
1. ¿Cómo ayuda la definición de requirements a controlar el scope de un proyecto?  
2. ¿Qué diferencia hay entre un requirement y una User Story?  
3. ¿Cuáles son los criterios clave para validar que un requirement está bien redactado?  
4. ¿Qué consecuencias puede generar la falta de trazabilidad entre requirements y entregables?  
5. ¿En qué situaciones es recomendable usar una herramienta de gestión de requisitos en lugar de una hoja de cálculo?

<!-- trazabilidad: run_id=run-20261109-170925-9b39ca concept=10-project-management-03-requirements written_at=2026-11-09T20:10:18.013859+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/12 - Requirements|Requirements]] · *Product Management*
- [[09 - Product Management/13 - User Stories|User Stories]] · *Product Management*
- [[10 - Project Management/01 - Project Fundamentals|Project Fundamentals]]
- [[10 - Project Management/02 - Scope|Scope]]
- [[10 - Project Management/04 - Deliverables|Deliverables]]

---
← [[10 - Project Management/02 - Scope|Scope]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/04 - Deliverables|Deliverables]] →
