---
title: "Issue Management"
area: "Project Management"
numero: 14
aliases: ["Issue Management"]
tags: [concepto, it/project-management]
---
# Issue Management

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 14 de 25**

## Qué abarca
- Problemas que ya ocurrieron

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Issue Management para registrar, clasificar y dar seguimiento a los problemas que ya han ocurrido en el proyecto. Resuelvo la falta de visibilidad y la demora en la respuesta a incidentes, evitando que se conviertan en bloqueos o en pérdidas de calidad. Aparece cada vez que un miembro del equipo reporta un bug, una dependencia incumplida o una desviación del plan; yo lo priorizo, asigno responsables y defino plazos de resolución. Después de entenderlo, puedo integrar el proceso con los tableros de trabajo y con la gestión de riesgos, garantizando que los problemas se conviertan en información útil para la toma de decisiones. No necesito preocuparme cuando el proyecto está en fase de cierre y no quedan problemas abiertos que impacten entregas futuras.

## Esqueleto (el 20% esencial)
1. **Registro inmediato** – Cada problema se captura en un ítem único con datos básicos (descripción, fecha, origen).  
2. **Clasificación y prioridad** – Se asigna una severidad y una prioridad que orientan la rapidez de la respuesta.  
3. **Asignación y seguimiento** – Un responsable se designa y se monitoriza el estado hasta su cierre.  
4. **Comunicación** – Se notifica a los interesados relevantes cada cambio de estado.  
5. **Lección aprendida** – Al cerrar, se documenta la causa raíz y la acción preventiva.

## Como funciona
1. Un integrante detecta un problema y abre un *issue* en el sistema de seguimiento.  
2. El project manager revisa la información, añade la clasificación de severidad y define la prioridad.  
3. Se asigna el *issue* al recurso más adecuado y se establece una fecha objetivo de resolución.  
4. El responsable actualiza el estado (abierto, en progreso, bloqueado, resuelto) y el PM notifica a los stakeholders críticos.  
5. Cuando el problema se soluciona, se cierra el *issue* y se registra la lección aprendida para futuros proyectos.

## Detalles
- **Básico:** Uso de un tablero sencillo (p. ej., Trello) donde cada tarjeta representa un *issue*; campos obligatorios: descripción, responsable y estado.  
- **Intermedio:** Implementación de un sistema dedicado (Jira, Azure DevOps) que permite campos personalizados, flujos de trabajo automáticos y métricas de tiempo de resolución.  
- **Avanzado:** Integración con herramientas de monitoreo (Sentry, New Relic) que generan *issues* automáticamente, y con el módulo de Risk Management para recalcular el nivel de riesgo cuando la severidad aumenta.

## Ejemplo minimo
```python
# Simulación mínima de Issue Management en Python
issues = []

def crear_issue(descripcion, origen):
    issue = {
        "id": len(issues) + 1,
        "descripcion": descripcion,
        "origen": origen,
        "severidad": "Media",
        "prioridad": "Normal",
        "responsable": None,
        "estado": "Abierto"
    }
    issues.append(issue)
    return issue

# Crear un issue de ejemplo
nuevo = crear_issue("Falla al exportar reporte PDF", "Tester")
print(nuevo)
```

## Errores comunes
- **No registrar inmediatamente** – El problema se olvida; evitarlo estableciendo una política de captura al instante.  
- **Ignorar la clasificación** – Todas las incidencias se tratan igual; usar una matriz de severidad‑prioridad.  
- **No asignar responsable** – El *issue* queda estancado; siempre designar un dueño al crear el ítem.  
- **Falta de cierre formal** – Se pierde la lección aprendida; cerrar sólo después de validar la solución.  

## Estado actual
**Fundamentos estables:** El registro, la clasificación y la asignación siguen siendo los pilares de Issue Management en cualquier metodología de proyecto.  
**Práctica moderna:** Las plataformas integradas permiten automatizar la generación de *issues* a partir de logs de producción y enlazarlos con la gestión de riesgos, ofreciendo una visión en tiempo real del impacto del problema en el cronograma y el presupuesto.

## Conexiones
- **Risk Management:** Un *issue* de alta severidad eleva el nivel de riesgo del proyecto y puede desencadenar acciones de mitigación.  
- **Change Management:** La solución de un *issue* a menudo implica cambios en el alcance o en los entregables, requiriendo un proceso formal de gestión de cambios.  
- **Quality Assurance:** Los *issues* reportados por QA alimentan los indicadores de calidad y guían la mejora continua del proceso de desarrollo.

## Ruta de estudio
1. **Prerequisitos:** Conocer los conceptos básicos de planificación de proyectos y de gestión de tareas (tableros Kanban, WBS).  
2. **Fundamentos:** Aprender a usar una herramienta de seguimiento (p. ej., Jira) y a definir severidad y prioridad.  
3. **Intermedio:** Configurar flujos de trabajo automáticos y métricas de tiempo de resolución.  
4. **Avanzado:** Integrar Issue Management con sistemas de monitoreo y con Risk Management; estudiar técnicas de análisis de causa raíz (5 Why, Ishikawa).  

## Preguntas de repaso
1. ¿Cuál es el objetivo principal de registrar un *issue* inmediatamente después de detectarlo?  
2. ¿Cómo influye la clasificación de severidad en la priorización de la respuesta?  
3. ¿Qué pasos sigue el project manager para asegurar la comunicación adecuada de un *issue*?  
4. ¿En qué situaciones un *issue* debe desencadenar una revisión del plan de riesgos?  
5. ¿Qué beneficio aporta cerrar formalmente un *issue* con una lección aprendida?

<!-- trazabilidad: run_id=run-20261109-173358-ca143c concept=10-project-management-14-issue-management written_at=2026-11-09T20:35:15.894321+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/13 - Risk Management|Risk Management]]
- [[10 - Project Management/15 - Change Management|Change Management]]

---
← [[10 - Project Management/13 - Risk Management|Risk Management]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/15 - Change Management|Change Management]] →
