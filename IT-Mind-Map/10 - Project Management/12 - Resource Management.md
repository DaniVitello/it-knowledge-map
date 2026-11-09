---
title: "Resource Management"
area: "Project Management"
numero: 12
aliases: ["Resource Management"]
tags: [concepto, it/project-management]
---
# Resource Management

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 12 de 25**

## Qué abarca
- Personas
- tiempo
- presupuesto
- infraestructura

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la gestión de recursos para asegurar que las personas, el tiempo, el presupuesto y la infraestructura estén alineados con los entregables del proyecto. Resuelvo el problema de sobrecarga o subutilización de recursos, que suele generar retrasos, costos inesperados y baja calidad. Aparece en cada fase del proyecto: al crear el plan de trabajo, al asignar tareas al equipo y al monitorear el consumo de presupuesto e infraestructura. Después de entenderlo, puedo diseñar planes de asignación, anticipar cuellos de botella y negociar ajustes con los patrocinadores. No necesito preocuparme cuando el proyecto es tan pequeño que un solo recurso ejecuta todas las actividades y el presupuesto es fijo y sin variaciones.

## Esqueleto (el 20% esencial)
1. **Personas** – identificar habilidades, disponibilidad y carga de trabajo de cada miembro del equipo.  
2. **Tiempo** – estimar duración de actividades y definir hitos realistas.  
3. **Presupuesto** – asignar costos a recursos humanos y materiales, y controlar el gasto.  
4. **Infraestructura** – asegurar que herramientas, entornos y equipos estén disponibles cuando se necesiten.  

## Como funciona
1. **Inventario de recursos**: se listan todas las personas, equipos y licencias disponibles.  
2. **Asignación inicial**: se emparejan tareas del cronograma con los recursos que mejor cubren las habilidades y la capacidad.  
3. **Balanceo**: se revisan sobrecargas y huecos; se redistribuyen tareas o se solicitan recursos adicionales.  
4. **Seguimiento**: se registran horas trabajadas y consumo de presupuesto contra la planificación.  
5. **Ajuste continuo**: al detectar desviaciones, se re‑asignan recursos o se renegocian plazos y costos.  

## Detalles
- **Básico**: crear una hoja de cálculo con columnas → Recurso, Habilidad, Disponibilidad, Costo y Asignación.  
- **Intermedio**: usar un software de gestión (p. ej., MS Project, Jira + Tempo) para visualizar la carga y generar alertas de sobrecarga.  
- **Avanzado**: aplicar técnicas de optimización (algoritmos de asignación, análisis de valor ganado) y vincular la gestión de recursos con la gestión de riesgos para anticipar impactos de escasez.  

## Ejemplo minimo
```python
# Tabla mínima de asignación de recursos
recursos = {
    "Ana": {"rol": "Desarrollador", "horas_disp": 30},
    "Luis": {"rol": "Tester", "horas_disp": 20}
}

tareas = {
    "Implementar API": {"horas_nec": 25, "rol_req": "Desarrollador"},
    "Pruebas funcionales": {"horas_nec": 15, "rol_req": "Tester"}
}

asignacion = {}
for t, d in tareas.items():
    for r, info in recursos.items():
        if info["rol"] == d["rol_req"] and info["horas_disp"] >= d["horas_nec"]:
            asignacion[t] = r
            recursos[r]["horas_disp"] -= d["horas_nec"]
            break

print(asignacion)  # {'Implementar API': 'Ana', 'Pruebas funcionales': 'Luis'}
```

## Errores comunes
- **Sobrecargar a una persona**: revisar siempre la disponibilidad antes de asignar.  
- **Ignorar la infraestructura**: validar que herramientas y entornos estén provisionados antes de iniciar la tarea.  
- **No actualizar el consumo real**: registrar horas y costos diariamente para evitar desviaciones inesperadas.  

## Estado actual
- **Fundamentos estables**: la identificación de personas, tiempo, presupuesto e infraestructura sigue siendo la base de cualquier proyecto.  
- **Práctica moderna**: la integración de herramientas de gestión ágil con módulos de capacity planning y el uso de análisis de valor ganado (Earned Value Management) para medir el desempeño de recursos en tiempo real.  

## Conexiones
- **Budget & Cost**: el presupuesto determina cuánto se puede invertir en recursos humanos y materiales; una asignación ineficiente eleva los costos.  
- **Risk Management**: la falta de recursos críticos es una amenaza que se gestiona anticipando contingencias y planes de mitigación.  
- **Stakeholder Management**: los patrocinadores y clientes esperan visibilidad sobre cómo se utilizan los recursos para cumplir sus expectativas.  

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de planificación de proyectos y cronogramas (WBS, Gantt).  
2. **Fundamentos**: aprender a crear un registro de recursos y a usar hojas de cálculo para asignaciones simples.  
3. **Herramientas**: dominar MS Project o Jira + Tempo para capacity planning.  
4. **Avanzado**: estudiar Earned Value Management y técnicas de optimización de asignación.  
5. **Especialización**: explorar la integración con gestión de riesgos y con metodologías ágiles (Scrum, Kanban).  

## Preguntas de repaso
1. ¿Cómo determina la gestión de recursos la carga de trabajo adecuada para cada persona?  
2. ¿Qué pasos sigue el proceso de balanceo cuando se detecta una sobrecarga?  
3. ¿Por qué es importante registrar el consumo real de presupuesto y tiempo durante la ejecución?  
4. ¿Cuál es la relación entre la gestión de recursos y la gestión de riesgos?  
5. ¿Qué herramienta moderna permite visualizar la capacidad del equipo y generar alertas de sobrecarga?

<!-- trazabilidad: run_id=run-20261109-173134-638230 concept=10-project-management-12-resource-management written_at=2026-11-09T20:32:43.768090+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/23 - Budget & Cost|Budget & Cost]]

---
← [[10 - Project Management/11 - Prioritization|Prioritization]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/13 - Risk Management|Risk Management]] →
