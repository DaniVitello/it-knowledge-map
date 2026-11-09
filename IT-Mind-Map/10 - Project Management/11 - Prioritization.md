---
title: "Prioritization"
area: "Project Management"
numero: 11
aliases: ["Prioritization"]
tags: [concepto, it/project-management]
---
# Prioritization

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 11 de 25**

## Qué abarca
- Orden de ejecución

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la priorización para decidir qué actividades del proyecto se ejecutan primero, alineando el trabajo del equipo con los objetivos de negocio y los plazos críticos. Resuelvo la sobrecarga de tareas y la incertidumbre sobre qué abordar cuando los recursos son limitados. Aparece en la planificación de sprints, la elaboración del cronograma y la gestión de cambios, donde debo garantizar que el valor entregado sea máximo con el menor riesgo. Después de entenderla, puedo estructurar backlog, negociar alcance y comunicar decisiones de forma transparente. No necesito preocuparme cuando el proyecto está en fase de cierre o cuando todas las tareas ya están definidas y asignadas.

## Esqueleto (el 20% esencial)
1. **Valor de negocio** – Priorizo las tareas que generan mayor retorno o alineación estratégica.  
2. **Urgencia y dependencia** – Ordeno según fechas límite y relaciones de precedencia entre actividades.  
3. **Capacidad del equipo** – Ajusto la lista a la disponibilidad y habilidades del personal.  
4. **Riesgo** – Doy preferencia a los ítems que reducen incertidumbres críticas.  
5. **Feedback continuo** – Reviso y actualizo la prioridad al recibir nueva información.

## Como funciona
1. Reúno los criterios de valor, urgencia, capacidad y riesgo.  
2. Asigno una puntuación o categoría a cada ítem del backlog.  
3. Ordeno los ítems de mayor a menor puntuación, respetando dependencias técnicas.  
4. Comunico el orden al equipo y al sponsor, obteniendo su validación.  
5. Durante la ejecución, reviso el ranking en cada reunión de planificación y lo ajusto si cambian los criterios.

## Detalles
- **Básico:** Uso una matriz simple (valor × urgencia) para clasificar tareas en alta, media y baja prioridad.  
- **Intermedio:** Implemento un modelo de puntuación ponderada que incluye riesgo y capacidad, facilitado por una hoja de cálculo compartida.  
- **Avanzado:** Integro herramientas de gestión (Jira, Azure DevOps) con algoritmos de scoring automático y reglas de negocio que reordenan el backlog en tiempo real.

## Ejemplo minimo
```python
# Lista de tareas con atributos (valor, urgencia, riesgo)
tasks = [
    {"id": "A", "value": 8, "urgency": 5, "risk": 2},
    {"id": "B", "value": 5, "urgency": 9, "risk": 4},
    {"id": "C", "value": 7, "urgency": 3, "risk": 1},
]

# Scoring simple: value*urgency - risk
for t in tasks:
    t["score"] = t["value"] * t["urgency"] - t["risk"]

# Ordenar por score descendente
tasks.sort(key=lambda x: x["score"], reverse=True)

print([t["id"] for t in tasks])   # Resultado: ['B', 'A', 'C']
```

## Errores comunes
- **Priorizar solo por valor** sin considerar urgencia o dependencia → se generan cuellos de botella.  
- **Ignorar la capacidad del equipo** → sobrecarga y retrasos.  
- **No actualizar la prioridad** después de cambios → decisiones desalineadas.  
- **Usar puntuaciones arbitrarias** sin consenso → pérdida de confianza.  
*Cómo evitarlos:* establecer criterios claros, validar con el equipo y revisar periódicamente.

## Estado actual
Los fundamentos de priorización (valor, urgencia, riesgo) son estables y se aplican en la mayoría de los marcos ágiles y tradicionales. La práctica moderna incorpora automatización mediante herramientas de gestión que calculan scores en tiempo real y sincronizan prioridades con métricas de flujo de trabajo.

## Conexiones
- **Backlog grooming** – La priorización define qué ítems se refinan y cuándo se incluyen en el sprint.  
- **Risk management** – El factor de riesgo dentro de la priorización ayuda a mitigar amenazas tempranas.  
- **Resource allocation** – La capacidad del equipo, evaluada en la priorización, guía la asignación de recursos.

## Ruta de estudio
1. **Prerequisitos:** Conocer los conceptos de valor de negocio, dependencias y capacidad del equipo.  
2. **Fundamentos:** Practicar matrices de valor × urgencia y crear scoring simple en una hoja de cálculo.  
3. **Intermedio:** Aprender a usar filtros y campos personalizados en Jira o Azure DevOps para automatizar scores.  
4. **Avanzado:** Implementar reglas de negocio que ajusten prioridades según métricas de riesgo y velocidad del equipo, y validar con retrospectives.

## Preguntas de repaso
1. ¿Cómo influye la capacidad del equipo en la decisión de qué tarea priorizar?  
2. ¿Qué riesgo corre un proyecto si solo se prioriza por valor de negocio?  
3. Describe el paso en que se valida el orden de prioridades con el sponsor.  
4. ¿Cuál es la diferencia entre una matriz de valor × urgencia y un modelo de puntuación ponderada?  
5. ¿Por qué es importante revisar y actualizar la prioridad después de cada sprint?

<!-- trazabilidad: run_id=run-20261109-173020-9b0b97 concept=10-project-management-11-prioritization written_at=2026-11-09T20:31:32.589946+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/11 - Prioritization|Prioritization]] · *Product Management*

---
← [[10 - Project Management/10 - Scheduling|Scheduling]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/12 - Resource Management|Resource Management]] →
