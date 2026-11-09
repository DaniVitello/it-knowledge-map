---
title: "Scope"
area: "Project Management"
numero: 2
aliases: ["Scope"]
tags: [concepto, it/project-management]
---
# Scope

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 2 de 25**

## Qué abarca
- Qué está y qué no está dentro del proyecto

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el concepto de **Scope** para delimitar con precisión qué se incluye y qué se excluye del proyecto, lo que me permite evitar trabajos fuera de contrato y controlar los costos. Resuelvo el problema de la expansión descontrolada (scope creep) al establecer un marco claro para la planificación, la asignación de recursos y la comunicación con el cliente. Aparece en la fase de iniciación y se revisa continuamente durante la planificación y la ejecución. Después de comprenderlo, puedo crear una declaración de alcance, priorizar requisitos y negociar cambios de forma estructurada. No necesito preocuparme por el Scope cuando el proyecto es una tarea interna de mantenimiento sin entregables formales.

## Esqueleto (el 20% esencial)
1. **Definir qué está dentro del proyecto**: lista de funcionalidades, productos o resultados que se entregarán.  
2. **Definir qué está fuera del proyecto**: exclusiones que evitan malentendidos y controlan expectativas.  
3. **Alinear el Scope con los requisitos del cliente**: cada ítem del alcance debe rastrearse a un requisito aprobado.  
4. **Comunicar el Scope a todo el equipo**: la declaración de alcance sirve como referencia para decisiones y cambios.  

## Como funciona
1. Reúno a los stakeholders y documento los requisitos críticos.  
2. Transformo esos requisitos en entregables claros y los agrupo en la **declaración de alcance**.  
3. Identifico explícitamente las exclusiones y las añado al documento.  
4. Distribuyo la declaración de alcance y obtengo la aprobación formal.  
5. Durante la ejecución, cualquier solicitud de cambio se compara con la declaración; si no está dentro, se procesa como cambio formal.  

## Detalles
- **Básico**: crear una declaración de alcance simple (objetivo, entregables, exclusiones).  
- **Intermedio**: usar una Work Breakdown Structure (WBS) para descomponer los entregables en paquetes de trabajo y vincular cada paquete a un requisito.  
- **Avanzado**: integrar el control de cambios mediante un Change Control Board (CCB) y métricas de variación del alcance (por ejemplo, % de requisitos añadidos vs. planificados).  

## Ejemplo minimo
```json
{
  "projectScope": {
    "inScope": [
      "Desarrollo módulo de facturación",
      "Pruebas unitarias y de integración"
    ],
    "outOfScope": [
      "Migración de datos legacy",
      "Soporte post‑lanzamiento por 6 meses"
    ]
  }
}
```

## Errores comunes
- **Confundir requisitos con alcance** – evitar incluir cada deseo del cliente sin validar su valor.  
- **No documentar exclusiones** – genera expectativas falsas y aumenta el riesgo de scope creep.  
- **Ignorar la aprobación formal** – decisiones informales dificultan el control de cambios.  

## Estado actual
- **Fundamentos estables**: la declaración de alcance, la identificación de inclusiones/exclusiones y la alineación con requisitos siguen siendo prácticas esenciales en PMBOK y PRINCE2.  
- **Práctica moderna**: el uso de herramientas colaborativas (Jira, Azure DevOps) para rastrear la trazabilidad del alcance y la automatización de flujos de control de cambios está ganando adopción.  

## Conexiones
- **Project Fundamentals**: el Scope constituye uno de los pilares que define el éxito del proyecto junto con tiempo, costo y calidad.  
- **Requirements**: cada ítem del Scope debe trazarse a un requisito aprobado, garantizando que lo que se entrega satisface la necesidad del cliente.  
- **Deliverables**: el Scope determina los entregables que se producirán; sin un Scope claro, los entregables pueden quedar incompletos o fuera de objetivo.  

## Ruta de estudio
1. **Prerequisitos**: comprender los conceptos de *Stakeholder* y *Requirement* y familiarizarse con la estructura de un *Project Charter*.  
2. **Fundamentos**: estudiar la elaboración de la declaración de alcance y la creación de una WBS.  
3. **Avanzado**: aprender a implementar un proceso de control de cambios y a usar métricas de variación del alcance en informes de estado.  

## Preguntas de repaso
1. ¿Cómo diferencia una declaración de alcance entre lo que está dentro y lo que está fuera del proyecto?  
2. ¿Qué riesgo principal se mitiga al alinear el Scope con los requisitos del cliente?  
3. ¿Cuál es el papel de la aprobación formal del Scope en la gestión de cambios?  
4. ¿Qué herramienta o técnica permite descomponer los entregables en paquetes de trabajo manejables?  
5. ¿Cómo influye la trazabilidad del Scope en la calidad de los entregables?

<!-- trazabilidad: run_id=run-20261109-170822-a47759 concept=10-project-management-02-scope written_at=2026-11-09T20:09:23.502300+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/01 - Project Fundamentals|Project Fundamentals]]
- [[10 - Project Management/03 - Requirements|Requirements]]
- [[10 - Project Management/04 - Deliverables|Deliverables]]

---
← [[10 - Project Management/01 - Project Fundamentals|Project Fundamentals]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/03 - Requirements|Requirements]] →
