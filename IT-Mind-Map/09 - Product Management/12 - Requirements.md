---
title: "Requirements"
area: "Product Management"
numero: 12
aliases: ["Requirements"]
tags: [concepto, it/product-management]
---
# Requirements

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 12 de 25**

## Qué abarca
- Necesidades funcionales y no funcionales

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los **requirements** para traducir lo que el usuario necesita y lo que el producto debe cumplir en instrucciones claras y medibles. Resuelvo la ambigüedad que surge entre la visión del negocio y la implementación técnica, garantizando que el equipo de desarrollo trabaje sobre una base consensuada. Aparecen en cada fase del ciclo de vida del producto: desde la fase de descubrimiento, cuando se priorizan funcionalidades, hasta la planificación de sprints, cuando se convierten en criterios de aceptación. Después de entender los requirements puedo estructurar el backlog, definir métricas de éxito y validar entregas. No necesito preocuparme de ellos cuando el producto está en fase de mantenimiento puro y solo se realizan correcciones menores sin impacto en funcionalidades ni en calidad.

## Esqueleto (el 20% esencial)
1. **Necesidades funcionales** – describen *qué* debe hacer el producto (p.ej., “el usuario puede crear una cuenta”).  
2. **Necesidades no funcionales** – establecen *cómo* debe comportarse (p.ej., “el tiempo de carga no supera 2 s”).  
3. **Prioridad y alineación** – cada requirement se valora según su impacto en objetivos de negocio y viabilidad técnica.  
4. **Criterios de aceptación** – convierten el requirement en condiciones verificables para el equipo de QA.  

## Como funciona
1. **Recopilación**: a partir de entrevistas, datos de uso y análisis de mercado, se identifican necesidades funcionales y no funcionales.  
2. **Formalización**: se redactan como statements claros, asignándoles una prioridad (p.ej., Must‑have, Should‑have).  
3. **Desglose**: cada requirement se transforma en una o varias *user stories* que el equipo pueda estimar.  
4. **Validación**: se añaden criterios de aceptación que permiten comprobar que el requisito quedó satisfecho.  
5. **Seguimiento**: durante el sprint, el product manager verifica que el desarrollo respete los requisitos y ajusta prioridades si aparecen nuevos datos.

## Detalles
- **Básico**: distinguir entre funcional y no funcional; usar un formato simple (“Como <rol>, quiero <acción> para <beneficio>”).  
- **Intermedio**: aplicar técnicas de *MoSCoW* o *Weighted Shortest Job First* (WSJF) para priorizar; enlazar cada requirement a métricas de negocio (p.ej., tasa de conversión).  
- **Avanzado**: gestionar requisitos regulatorios o de seguridad; usar *traceability matrices* para asegurar que cada requirement está cubierto por pruebas automatizadas y documentación de arquitectura.

## Ejemplo minimo
```json
{
  "id": "REQ-001",
  "type": "functional",
  "statement": "El usuario puede iniciar sesión con email y contraseña",
  "priority": "must-have",
  "acceptanceCriteria": [
    "El login responde en ≤ 1 s",
    "Muestra mensaje de error claro si las credenciales son inválidas"
  ]
}
```

## Errores comunes
- **Confundir requisitos con soluciones** – evitar describir la tecnología a usar; centrarse en el *qué* y no en el *cómo*.  
- **Olvidar requisitos no funcionales** – incluir siempre desempeño, seguridad y usabilidad.  
- **Priorizar sin datos** – validar la prioridad con métricas de negocio o feedback de usuarios.  

## Estado actual
Los fundamentos de los requirements (distinción funcional/no funcional, prioridad y criterios de aceptación) son estables y ampliamente adoptados en metodologías ágiles. En la práctica moderna, se complementan con herramientas de gestión de backlog que permiten trazabilidad automática y alineación con OKR, así como con pruebas de aceptación basadas en *behavior‑driven development* (BDD).

## Conexiones
- **User Stories**: los requirements se desglosan en user stories que el equipo estima y planifica.  
- **Roadmap**: la priorización de requirements alimenta la construcción del roadmap del producto.  
- **KPIs**: los requisitos funcionales y no funcionales se vinculan a indicadores clave que miden el éxito del producto.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de gestión de producto, visión de negocio y técnicas de descubrimiento de usuarios.  
2. **Fundamentos**: aprender a redactar requisitos claros y a aplicar MoSCoW.  
3. **Intermedio**: practicar la transformación de requisitos en user stories y definir criterios de aceptación.  
4. **Avanzado**: dominar la trazabilidad, integrar requisitos regulatorios y usar BDD para validar entregas.  

## Preguntas de repaso
1. ¿Cuál es la diferencia principal entre un requisito funcional y uno no funcional?  
2. ¿Cómo conviertes un requirement en una user story y por qué es importante?  
3. ¿Qué papel juegan los criterios de aceptación dentro del proceso de validación?  
4. ¿Por qué es crítico priorizar requisitos con datos de negocio antes de planificar sprints?  
5. ¿Cómo se relacionan los requirements con los KPIs del producto?

<!-- trazabilidad: run_id=run-20261106-205249-4dbd7c concept=09-product-management-12-requirements written_at=2026-11-06T23:53:20.607001+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/13 - User Stories|User Stories]]
- [[10 - Project Management/03 - Requirements|Requirements]] · *Project Management*

---
← [[09 - Product Management/11 - Prioritization|Prioritization]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/13 - User Stories|User Stories]] →
