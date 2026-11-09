---
title: "Scheduling"
area: "Project Management"
numero: 10
aliases: ["Scheduling"]
tags: [concepto, it/project-management]
---
# Scheduling

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 10 de 25**

## Qué abarca
- Fechas
- milestones
- deadlines

## Mis notas
<!-- ai:start -->
## Objetivo  
Utilizo el scheduling para transformar la visión del proyecto en un calendario operativo que indique cuándo se deben iniciar y terminar las actividades, alineando recursos y expectativas. Resuelvo la incertidumbre de “¿qué se hace y cuándo?” y garantizo que los hitos críticos (milestones) y las fechas de entrega (deadlines) sean visibles para todo el equipo. Aparece en la fase de planificación y se revisa continuamente durante la coordinación diaria; sin él, la gestión de riesgos y la comunicación con stakeholders se vuelve caótica. Después de dominar el scheduling puedo sincronizar el Product Roadmap con la ejecución real, anticipar cuellos de botella y ajustar el plan sin perder el foco en los objetivos. Cuando el proyecto es muy pequeño o está bajo control de un solo individuo, el detalle de scheduling puede simplificarse o omitirse.

## Esqueleto (el 20% esencial)  
1. **Fechas** – Cada tarea recibe una fecha de inicio y una de fin que define su ventana de trabajo.  
2. **Milestones** – Puntos de control que marcan entregas parciales o decisiones clave; no son tareas, sino indicadores de progreso.  
3. **Deadlines** – Límites inquebrantables que deben respetarse para cumplir compromisos externos o contractuales.  
4. **Dependencias** – Relaciones entre tareas que determinan el orden lógico del trabajo.  
5. **Estimación** – Cálculo de la duración realista de cada actividad, base para fijar fechas y deadlines.

## Como funciona  
1. Parto del **Work Breakdown Structure (WBS)** para identificar todas las tareas necesarias.  
2. Estimo la duración de cada tarea (horas, días) y asigno recursos.  
3. Defino las **dependencias** (finish‑to‑start, start‑to‑start, etc.) que condicionan el orden.  
4. Con esas duraciones y dependencias, calculo fechas de inicio y fin, creando el **schedule**.  
5. Inserto **milestones** en los momentos críticos (fin de fase, entrega al cliente).  
6. Verifico que los **deadlines** externos estén cubiertos; si no, ajusto estimaciones o recursos.  
7. Durante la ejecución, monitorizo el avance y actualizo el schedule para reflejar desviaciones.

## Detalles  
- **Básico**: Uso de una hoja de cálculo para listar tareas, duraciones y fechas; visualización simple de barras.  
- **Intermedio**: Herramientas de diagramas de Gantt que gestionan dependencias y generan alertas automáticas cuando una tarea supera su deadline.  
- **Avanzado**: Integración con metodologías ágiles (sprints) y con el **Product Roadmap**, permitiendo re‑planificación dinámica basada en capacidad real y cambios de prioridad. También se aplican técnicas de *critical path* para optimizar la secuencia de tareas y reducir la duración total del proyecto.

## Ejemplo minimo  
```python
# Ejemplo en Python usando la librería gantt
import gantt

# Definir recursos
dev = gantt.Resource('Desarrollador')

# Crear proyecto y tareas
p = gantt.Project(name='Demo')
t1 = gantt.Task(name='Diseño UI', start='2024-01-02', duration=3, resources=[dev])
t2 = gantt.Task(name='Implementación', start='2024-01-05', duration=5, resources=[dev])
t2.add_dependency(t1)   # dependencia finish‑to‑start

p.add_task(t1)
p.add_task(t2)

p.make_svg_for_tasks(filename='schedule.svg')
```
El script genera un diagrama con fechas, dependencia y muestra el milestone implícito al terminar la tarea “Diseño UI”.

## Errores comunes  
- **Subestimar duraciones** → genera retrasos; validar con datos históricos.  
- **Ignorar dependencias** → provoca cuellos de botella inesperados; mapear siempre.  
- **Confundir milestones con tareas** → dificulta el seguimiento; usar milestones solo como indicadores.  
- **No actualizar el schedule** → la información queda obsoleta; revisarlo al menos semanalmente.  

## Estado actual  
- **Fundamentos estables**: definición de fechas, milestones y deadlines; uso de WBS y estimación basada en experiencia.  
- **Práctica moderna**: adopción de herramientas colaborativas (Jira, Azure DevOps) que sincronizan el schedule con el backlog, y aplicación de algoritmos de *critical path* y *resource leveling* para optimizar la planificación en entornos híbridos (ágil + tradicional).

## Conexiones  
- **Product Roadmap** – El schedule traduce los objetivos estratégicos del roadmap en fechas operativas, asegurando que los entregables del roadmap tengan una base temporal realista.  
- **Work Breakdown Structure** – El WBS provee la descomposición de trabajo que alimenta el schedule; sin un WBS claro, el schedule carece de precisión.  
- **Dependencies** – Las dependencias determinan la secuencia de tareas dentro del schedule; gestionarlas correctamente evita retrasos en los milestones y deadlines.

## Ruta de estudio  
1. **Prerequisitos**: comprender el WBS, conceptos de estimación y gestión de recursos.  
2. **Fundamentos**: crear schedules manuales en hoja de cálculo, practicar la identificación de dependencias y milestones.  
3. **Herramientas**: aprender a usar un software de Gantt (MS Project, Jira Advanced Roadmaps) y a generar diagramas automáticos.  
4. **Avanzado**: estudiar *critical path method* y *resource leveling*, integrar el schedule con metodologías ágiles y con el Product Roadmap.  
5. **Especialización**: explorar técnicas de forecasting basadas en datos históricos y simulaciones de escenarios de riesgo.

## Preguntas de repaso  
1. ¿Cómo transforma una estimación de duración en una fecha de inicio y fin dentro del schedule?  
2. ¿Qué diferencia hay entre un milestone y una tarea y por qué es importante no confundirlos?  
3. ¿De qué manera una dependencia mal definida puede afectar un deadline crítico?  
4. ¿Qué beneficio aporta integrar el schedule con el Product Roadmap en un proyecto híbrido?  
5. ¿Cuál es el propósito del método de *critical path* y cuándo deberías aplicarlo?

<!-- trazabilidad: run_id=run-20261109-172832-7b4f23 concept=10-project-management-10-scheduling written_at=2026-11-09T20:30:18.613314+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/10 - Product Roadmap|Product Roadmap]] · *Product Management*
- [[10 - Project Management/05 - Work Breakdown Structure|Work Breakdown Structure]]
- [[10 - Project Management/06 - Task Management|Task Management]]
- [[10 - Project Management/07 - Dependencies|Dependencies]]
- [[10 - Project Management/08 - Estimation|Estimation]]
- [[10 - Project Management/09 - Planning|Planning]]
- [[10 - Project Management/19 - Milestones & Releases|Milestones & Releases]]

---
← [[10 - Project Management/09 - Planning|Planning]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/11 - Prioritization|Prioritization]] →
