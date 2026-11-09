---
title: "Team Coordination"
area: "Project Management"
numero: 22
aliases: ["Team Coordination"]
tags: [concepto, it/project-management]
---
# Team Coordination

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 22 de 25**

## Qué abarca
- Dependencias y colaboración

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la coordinación de equipos para alinear a los miembros en torno a entregas interdependientes, garantizando que cada pieza del proyecto avance sin bloqueos. Resuelvo el problema de la falta de sincronía que genera retrasos y retrabajo, y aparece en cada fase donde el trabajo de varios roles se superpone: planificación de sprints, revisiones de hitos y entregas parciales. Después de entender la coordinación de equipos, puedo diseñar flujos de trabajo claros, definir puntos de integración y anticipar cuellos de botella. No necesito preocuparme cuando el proyecto es de una sola persona o cuando las tareas son totalmente independientes.

## Esqueleto (el 20% esencial)
1. **Identificar dependencias** – Detectar qué entregables requieren la salida de otros equipos antes de poder avanzar.  
2. **Establecer canales de colaboración** – Definir reuniones, herramientas y protocolos que permitan el intercambio rápido de información.  
3. **Sincronizar tiempos** – Alinear fechas de inicio y fin de actividades interdependientes para evitar esperas.  
4. **Monitorear el estado** – Registrar avances y bloqueos en un punto visible para todos los involucrados.  
5. **Facilitar decisiones** – Proveer al líder técnico la información necesaria para resolver conflictos de prioridad.

## Como funciona
1. Durante la planificación, el PM lista todas las tareas y marca las dependencias entre ellas.  
2. Se asignan responsables y se elige el canal de comunicación (Slack, reuniones diarias, tablero Kanban).  
3. Se crean hitos que agrupan actividades con dependencias comunes y se fijan fechas de integración.  
4. Cada día el equipo actualiza su progreso en el tablero; los bloqueos se reportan inmediatamente.  
5. El PM revisa el reporte, informa al Technical Leader y, si es necesario, re‑prioriza o negocia con los Stakeholders.

## Detalles
- **Básico:** Reconocer quién entrega qué y cuándo; usar un tablero simple con columnas “Por hacer”, “En progreso” y “Hecho”.  
- **Intermedio:** Introducir “dependencias visuales” (líneas entre tarjetas) y reuniones de coordinación de 15 min cada mañana para alinear prioridades.  
- **Avanzado:** Automatizar notificaciones de bloqueos mediante integraciones (por ejemplo, GitHub Actions que avisan cuando un PR depende de otro) y aplicar métricas de lead time para ajustar la sincronización de sprints.

## Ejemplo minimo
```json
{
  "team": [
    {"name": "Ana", "role": "Frontend"},
    {"name": "Luis", "role": "Backend"}
  ],
  "tasks": [
    {"id": "T1", "owner": "Ana", "dependsOn": []},
    {"id": "T2", "owner": "Luis", "dependsOn": ["T1"]}
  ]
}
```
En este JSON, la tarea *T2* no puede iniciarse hasta que *T1* esté completada, lo que obliga a Ana y Luis a coordinar sus entregas.

## Errores comunes
- Asumir que la comunicación informal es suficiente; evitarlo estableciendo canales oficiales.  
- Ignorar pequeñas dependencias que, acumuladas, generan grandes retrasos; revisarlas en cada planificación.  
- No actualizar el tablero en tiempo real; usar recordatorios automáticos para mantener la información fresca.  
- Delegar la coordinación completa al líder técnico sin supervisión del PM; mantener la visión global.

## Estado actual
**Fundamentos estables:** La identificación de dependencias y la actualización visible del estado son prácticas consolidadas en metodologías ágiles y tradicionales.  
**Práctica moderna:** El uso de integraciones CI/CD para señalizar bloqueos y la adopción de métricas de flujo (flow metrics) para optimizar la sincronización de equipos están ganando adopción en organizaciones que buscan entrega continua.

## Conexiones
- **Technical Leadership**: Provee la autoridad técnica para decidir cómo resolver dependencias críticas y priorizar refactorizaciones.  
- **Engineering Processes**: Define los pasos (code review, integración continua) que deben respetarse para que la coordinación sea efectiva.  
- **Stakeholder Management**: Necesita información de la coordinación de equipos para comunicar avances realistas y negociar cambios de alcance.

## Ruta de estudio
1. **Prerequisitos:** Conocer los fundamentos de gestión de proyectos (WBS, cronograma) y manejo de tableros Kanban.  
2. **Fundamento:** Practicar la identificación de dependencias en proyectos pequeños y usar un tablero visual.  
3. **Intermedio:** Implementar reuniones de coordinación y herramientas de notificación automática.  
4. **Avanzado:** Integrar métricas de flujo y automatizaciones CI/CD; estudiar casos de escalado de coordinación en equipos distribuidos.  
5. **Especialización:** Explorar frameworks de Release Train Engineering (RTE) y técnicas de Program Increment (PI) Planning.

## Preguntas de repaso
1. ¿Cómo identificas una dependencia que pueda bloquear el progreso de otro equipo?  
2. ¿Qué canales de colaboración prefieres para una coordinación diaria y por qué?  
3. ¿Cuál es el papel del Technical Leader al resolver un conflicto de prioridad entre tareas dependientes?  
4. ¿Cómo usarías una métrica de lead time para ajustar la sincronización de sprints?  
5. ¿Qué riesgos aparecen si el tablero de estado no se actualiza en tiempo real?

<!-- trazabilidad: run_id=run-20261109-180240-bdd99d concept=10-project-management-22-team-coordination written_at=2026-11-09T21:03:49.220644+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/29 - Technical Leadership|Technical Leadership]] · *Software Engineering*
- [[01 - Software Engineering/30 - Engineering Processes|Engineering Processes]] · *Software Engineering*
- [[10 - Project Management/20 - Status & Reporting|Status & Reporting]]
- [[10 - Project Management/21 - Stakeholder Management|Stakeholder Management]]

---
← [[10 - Project Management/21 - Stakeholder Management|Stakeholder Management]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/23 - Budget & Cost|Budget & Cost]] →
