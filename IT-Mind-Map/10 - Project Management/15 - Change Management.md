---
title: "Change Management"
area: "Project Management"
numero: 15
aliases: ["Change Management"]
tags: [concepto, it/project-management]
---
# Change Management

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 15 de 25**

## Qué abarca
- Control de cambios de alcance/requisitos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Change Management para controlar cualquier variación en el alcance o los requisitos del proyecto, evitando sorpresas que comprometan el cronograma, el presupuesto o la calidad. Resuelvo la incertidumbre que surge cuando un stakeholder solicita una nueva funcionalidad o cuando una condición externa obliga a ajustar el plan. Aparece en mi día a día al revisar solicitudes de cambio, evaluar su impacto y decidir si se aprueba, se rechaza o se pospone. Después de entenderlo, puedo estructurar un proceso de revisión, priorización y comunicación que mantenga al equipo alineado y al cliente informado. No necesito preocuparme cuando el proyecto está bajo un contrato fijo sin cláusulas de variación o cuando el alcance está completamente congelado y todas las partes han firmado una declaración de requisitos inalterable.

## Esqueleto (el 20% esencial)
1. **Registro de cambios** – Cada solicitud se documenta con origen, descripción y fecha.  
2. **Evaluación de impacto** – Se analizan efectos en tiempo, costo y calidad antes de decidir.  
3. **Aprobación formal** – Un comité o el sponsor autoriza o rechaza el cambio según criterios predefinidos.  
4. **Comunicación y actualización** – El cambio aprobado se difunde al equipo y se actualizan los artefactos del proyecto.  
5. **Seguimiento post‑cambio** – Se verifica que la implementación cumpla con lo esperado y se registran lecciones.

## Como funciona
1. Un stakeholder envía una *Change Request* al registro.  
2. El PM la asigna a un analista que calcula variaciones de tiempo y costo.  
3. El resultado se presenta al Change Control Board (CCB) para su aprobación.  
4. Si se aprueba, el plan del proyecto, el backlog y los documentos de requisitos se actualizan.  
5. Se notifica al equipo y se planifica la ejecución; al cerrar, se registra el resultado y se actualiza el historial de cambios.

## Detalles
- **Básico:** Mantener un formulario sencillo y un archivo (ej. hoja de cálculo) donde se capture la solicitud, el responsable y la fecha.  
- **Intermedio:** Introducir una matriz de impacto que relacione cada cambio con los tres factores críticos (tiempo, costo, calidad) y definir umbrales de aprobación automática.  
- **Avanzado:** Automatizar el flujo con una herramienta de gestión (Jira, Azure DevOps) que enlace la solicitud a los tickets de desarrollo, genere reportes de riesgo y actualice el cronograma en tiempo real.

## Ejemplo minimo
```json
{
  "changeId": "CR-001",
  "origin": "Cliente",
  "description": "Agregar campo 'fecha de entrega' al formulario de pedido",
  "impact": {
    "scheduleDays": 2,
    "budgetUSD": 1500,
    "quality": "sin impacto"
  },
  "status": "Pending Approval"
}
```

## Errores comunes
- **Ignorar la evaluación de impacto**, lo que genera sobrecostos inesperados; evitarlo usando siempre la matriz de impacto.  
- **Aprobar cambios sin autoridad**, creando conflictos de responsabilidad; evitarlo definiendo claramente quién compone el CCB.  
- **No comunicar la actualización**, provocando trabajo duplicado; evitarlo enviando notificaciones automáticas al equipo.

## Estado actual
- **Fundamentos estables:** El registro formal, la evaluación de impacto y la aprobación estructurada son prácticas consolidadas en PMBOK y PRINCE2.  
- **Práctica moderna:** La integración de Change Management con herramientas de DevOps y la trazabilidad automática entre cambios y artefactos de código son tendencias actuales adoptadas por organizaciones ágiles.

## Conexiones
- **Risk Management:** Cada cambio introduce nuevos riesgos; la evaluación de impacto alimenta el registro de riesgos.  
- **Issue Management:** Un cambio mal gestionado puede convertirse en un issue que requiere resolución inmediata.  
- **Scope Management:** El control de cambios es la forma operativa de mantener el alcance definido y evitar la expansión descontrolada.

## Ruta de estudio
1. **Prerequisitos:** Conocer los fundamentos de Scope Management y de la planificación de proyectos.  
2. **Fundamentos:** Estudiar el proceso de Change Control en PMBOK y practicar con plantillas de registro.  
3. **Intermedio:** Aprender a usar herramientas de gestión (Jira, Azure DevOps) para automatizar flujos de cambio.  
4. **Avanzado:** Integrar Change Management con pipelines de CI/CD y métricas de calidad; participar en un Change Control Board real.

## Preguntas de repaso
1. ¿Cuál es el objetivo principal de un registro de cambios?  
2. ¿Qué información esencial debe contener una evaluación de impacto?  
3. ¿Quiénes forman típicamente el Change Control Board y cuál es su responsabilidad?  
4. ¿Cómo se relaciona un cambio aprobado con el proceso de Risk Management?  
5. ¿Qué pasos se deben seguir para comunicar y actualizar el equipo después de aprobar un cambio?

<!-- trazabilidad: run_id=run-20261109-173517-8ab122 concept=10-project-management-15-change-management written_at=2026-11-09T20:36:22.572345+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/13 - Risk Management|Risk Management]]
- [[10 - Project Management/14 - Issue Management|Issue Management]]

---
← [[10 - Project Management/14 - Issue Management|Issue Management]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/16 - Agile|Agile]] →
