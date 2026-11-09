---
title: "Project Fundamentals"
area: "Project Management"
numero: 1
aliases: ["Project Fundamentals"]
tags: [concepto, it/project-management]
---
# Project Fundamentals

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 1 de 25**

## Qué abarca
- Proyecto
- objetivos
- alcance
- restricciones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los fundamentos del proyecto para establecer la base sobre la que planifico, coordino y entrego resultados con criterios de éxito claros. Resuelvo la ambigüedad inicial que impide al equipo saber qué se quiere lograr, qué está incluido y qué limitaciones existen. Aparecen en la fase de iniciación y en la definición del alcance, sirviendo de referencia para todas las decisiones posteriores. Después de comprenderlos, puedo estructurar el charter, fijar metas medibles y alinear a los stakeholders. Cuando el proyecto ya está en ejecución y el alcance está formalmente aprobado, ya no necesito volver a revisar los fundamentos salvo que haya cambios significativos.

## Esqueleto (el 20% esencial)
1. **Objetivo del proyecto** – la razón de ser que guía todas las decisiones.  
2. **Alcance** – lo que está incluido y lo que queda fuera, delimitando el trabajo.  
3. **Restricciones** – limitaciones de tiempo, costo, recursos o calidad que condicionan la ejecución.  
4. **Entregables** – productos o resultados concretos que demuestran el cumplimiento del objetivo.  

## Como funciona
1. Defino el objetivo con los patrocinadores para que todos compartan la visión.  
2. Traduzco esa visión en un alcance claro, listando funcionalidades y exclusiones.  
3. Identifico restricciones críticas (fecha de lanzamiento, presupuesto máximo, disponibilidad de personal).  
4. Derivo los entregables que evidenciarán que el alcance se ha cumplido dentro de las restricciones.  
5. Comunico este conjunto a todo el equipo y lo utilizo como referencia para la planificación detallada y el control de cambios.

## Detalles
- **Básico:** redactar una declaración de objetivo concisa y un enunciado de alcance simple.  
- **Intermedio:** desglosar el alcance en paquetes de trabajo, mapear cada restricción a riesgos y asignar entregables a hitos.  
- **Avanzado:** aplicar técnicas de gestión de valor ganado (Earned Value Management) para medir el progreso respecto a objetivo, alcance y restricciones, y ajustar el plan en tiempo real.

## Ejemplo minimo
```json
{
  "project": "Lanzamiento App móvil",
  "objective": "Incrementar la base de usuarios en 20% en 6 meses",
  "scope": {
    "incluye": ["Diseño UI", "Desarrollo iOS", "Pruebas beta"],
    "excluye": ["Desarrollo Android", "Marketing offline"]
  },
  "constraints": {
    "budget": 50000,
    "deadline": "2024-06-30",
    "resources": 3 developers
  },
  "deliverables": ["App iOS v1.0", "Informe de pruebas", "Guía de usuario"]
}
```

## Errores comunes
- Confundir objetivo con entregable: el objetivo es el *por qué*, el entregable es el *qué*; evitarlo clarificando ambos por separado.  
- Definir alcance sin excluir nada: generar ambigüedad; siempre listar explícitamente exclusiones.  
- Ignorar restricciones tempranas: provocan replanificaciones costosas; registrar todas las limitaciones antes de la planificación detallada.  

## Estado actual
Los **fundamentos** (objetivo, alcance, restricciones y entregables) siguen siendo estables y forman la columna vertebral de cualquier metodología de gestión de proyectos, ya sea tradicional o ágil. En la práctica moderna, los equipos ágiles incorporan estos conceptos en artefactos como el *Product Vision*, el *Product Backlog* (que representa el alcance) y los *Definition of Done* (entregables), manteniendo la disciplina de las restricciones mediante *time‑boxing* y *budget tracking*.

## Conexiones
- **Scope**: el alcance deriva directamente del objetivo y delimita los entregables que se producirán.  
- **Requirements**: los requisitos son la especificación detallada del alcance; sin un alcance definido, los requisitos se dispersan.  
- **Deliverables**: los entregables son la materialización tangible del alcance aprobado y sirven para validar que el objetivo se ha alcanzado.

## Ruta de estudio
1. **Pre‑requisitos:** comprender la diferencia entre visión, misión y objetivo de negocio; familiarizarse con la estructura de un Project Charter.  
2. **Fundamentos:** practicar la redacción de objetivos SMART, crear enunciados de alcance y listar restricciones en casos de estudio.  
3. **Avanzado:** estudiar técnicas de gestión de valor ganado y de control de cambios; aplicar la integración de fundamentos en marcos ágiles (Scrum, SAFe).  

## Preguntas de repaso
1. ¿Cómo se traduce un objetivo de negocio en un alcance concreto?  
2. ¿Qué papel juegan las restricciones al definir los entregables?  
3. ¿Por qué es importante listar explícitamente lo que queda fuera del alcance?  
4. ¿Cómo se verifica que un entregable cumple con el objetivo del proyecto?  
5. ¿De qué manera los equipos ágiles incorporan los fundamentos del proyecto en sus artefactos?

<!-- trazabilidad: run_id=run-20261109-170734-d38194 concept=10-project-management-01-project-fundamentals written_at=2026-11-09T20:08:21.026340+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/02 - Scope|Scope]]
- [[10 - Project Management/03 - Requirements|Requirements]]
- [[10 - Project Management/04 - Deliverables|Deliverables]]

---
[[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/02 - Scope|Scope]] →
