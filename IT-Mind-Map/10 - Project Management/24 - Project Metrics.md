---
title: "Project Metrics"
area: "Project Management"
numero: 24
aliases: ["Project Metrics"]
tags: [concepto, it/project-management]
---
# Project Metrics

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 24 de 25**

## Qué abarca
- Velocity
- cycle time
- throughput
- predictability

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **Project Metrics** para medir el ritmo y la calidad del trabajo del equipo durante la planificación y la ejecución del proyecto. Resuelvo la incertidumbre sobre si estamos cumpliendo los compromisos y detecto cuellos de botella antes de que impacten la fecha de entrega. Aparecen en cada fase de seguimiento: al crear el roadmap, al ajustar el sprint y al cerrar el proyecto con una retrospectiva. Después de entenderlas, puedo establecer umbrales de desempeño, comunicar progreso a los stakeholders y priorizar mejoras en los procesos. No necesito preocuparme por ellas cuando el proyecto es extremadamente pequeño o cuando el cliente solo requiere entregas puntuales sin seguimiento de desempeño continuo.

## Esqueleto (el 20% esencial)
1. **Velocity** – cantidad de trabajo completado por iteración, sirve para estimar la capacidad futura.  
2. **Cycle Time** – tiempo que tarda una unidad de trabajo en pasar de “en progreso” a “terminado”, indica rapidez del flujo.  
3. **Throughput** – número de ítems entregados en un periodo, muestra la productividad total del equipo.  
4. **Predictability** – consistencia entre lo planificado y lo entregado, permite confiar en los compromisos.  

## Como funciona
1. Defino los ítems medibles (historias, tickets, features).  
2. Registro la fecha de inicio y fin de cada ítem en el tablero.  
3. Calculo la **Velocity** sumando los puntos completados por sprint.  
4. Extraigo el **Cycle Time** de cada ítem y calculo el promedio.  
5. Determino el **Throughput** contando los ítems terminados por semana.  
6. Comparo la **Velocity** y el **Throughput** con la planificación para evaluar la **Predictability** y decidir ajustes.

## Detalles
- **Básico**: usar un tablero Kanban o Scrum y anotar fechas de inicio/fin.  
- **Intermedio**: automatizar la captura de datos con herramientas de analytics y generar gráficos de tendencia.  
- **Avanzado**: aplicar análisis de series temporales para predecir la Velocity futura y simular escenarios de riesgo.

## Ejemplo minimo
```json
{
  "sprint": 5,
  "velocity": 42,
  "cycleTimeDays": 3.2,
  "throughput": 12,
  "predictability": "high"
}
```
En este sprint el equipo completó 42 puntos, cada historia tardó 3.2 días en promedio, entregó 12 ítems y la predictibilidad se calificó como alta.

## Errores comunes
- **Mide solo la velocidad** sin observar el Cycle Time → se ignoran cuellos de botella.  
- **Confundir throughput con calidad** → alta cantidad no garantiza que el trabajo cumpla los criterios de aceptación.  
- **Ignorar la variabilidad** de la predictabilidad → se asume que la tendencia siempre será lineal.

## Estado actual
- **Fundamentos estables**: Velocity, Cycle Time, Throughput y Predictability siguen siendo los indicadores básicos aceptados en la mayoría de los marcos ágiles.  
- **Práctica moderna**: integración de métricas en dashboards en tiempo real, uso de machine learning para pronosticar la Velocity y adopción de métricas de valor de negocio (por ejemplo, impacto en ingresos) junto a las métricas de proceso.

## Conexiones
- **Engineering Processes**: los Project Metrics se alimentan de la forma en que el equipo implementa CI/CD y revisiones de código, reflejando la eficiencia del proceso técnico.  
- **Product Metrics**: la predictabilidad del proyecto influye en la capacidad de entregar funcionalidades que impacten métricas de uso y satisfacción del producto.  
- **Retrospectives & Improvement**: los resultados de Velocity y Cycle Time son los datos clave que el equipo analiza en cada retrospectiva para definir acciones de mejora.

## Ruta de estudio
1. **Prerequisitos**: comprender Scrum/Kanban, saber leer un backlog y manejar herramientas de seguimiento (Jira, Azure Boards).  
2. **Fundamentos**: practicar la captura manual de Velocity y Cycle Time en un proyecto piloto.  
3. **Intermedio**: configurar reportes automáticos y aprender a interpretar gráficos de tendencia.  
4. **Avanzado**: estudiar técnicas de forecasting (Monte Carlo, regresión) y explorar la correlación entre Project Metrics y Product Metrics.  
5. **Especialización**: aplicar métricas en entornos híbridos (SAFe, LeSS) y combinar con indicadores de calidad (defect density, test coverage).

## Preguntas de repaso
1. ¿Cómo utilizo la Velocity para ajustar la planificación de futuros sprints?  
2. ¿Qué información me brinda el Cycle Time que la Velocity no muestra?  
3. ¿De qué manera el Throughput afecta la percepción de la productividad del equipo?  
4. ¿Cuál es la diferencia entre medir predictability y simplemente comparar la planificación con la entrega?  
5. ¿Qué pasos sigo para transformar datos de métricas en acciones concretas durante una retrospectiva?

<!-- trazabilidad: run_id=run-20261109-180427-504790 concept=10-project-management-24-project-metrics written_at=2026-11-09T21:05:14.062490+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/30 - Engineering Processes|Engineering Processes]] · *Software Engineering*
- [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]] · *Database / Data Analytics*
- [[08 - UX & UI/23 - UX Metrics|UX Metrics]] · *UX / UI*
- [[09 - Product Management/17 - Product Metrics|Product Metrics]] · *Product Management*
- [[10 - Project Management/08 - Estimation|Estimation]]
- [[10 - Project Management/25 - Retrospectives & Improvement|Retrospectives & Improvement]]

---
← [[10 - Project Management/23 - Budget & Cost|Budget & Cost]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/25 - Retrospectives & Improvement|Retrospectives & Improvement]] →
