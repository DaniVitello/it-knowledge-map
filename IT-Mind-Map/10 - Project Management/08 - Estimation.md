---
title: "Estimation"
area: "Project Management"
numero: 8
aliases: ["Estimation"]
tags: [concepto, it/project-management]
---
# Estimation

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 8 de 25**

## Qué abarca
- Tiempo
- esfuerzo
- complejidad

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la estimación para traducir la visión del proyecto en números de tiempo, esfuerzo y complejidad que permitan construir un plan realista. Resuelvo la incertidumbre que surge al decidir cuánto trabajo puede asumir el equipo y cuándo se podrá entregar cada incremento. Aparece en la fase de planificación, cuando defino el alcance y asigno recursos, y también durante la coordinación, al ajustar el cronograma frente a cambios. Después de comprender la estimación, puedo crear planes de proyecto más fiables, negociar compromisos con stakeholders y medir el desempeño del proyecto con métricas de variación. No necesito preocuparme por la estimación cuando el proyecto está en ejecución y los entregables ya están definidos y medidos.

## Esqueleto (el 20% esencial)
1. **Descomposición del trabajo** – Partir el producto en paquetes manejables (WBS) para identificar unidades de medida.  
2. **Asignación de esfuerzo** – Relacionar cada paquete con la cantidad de horas‑persona que requiere, considerando la complejidad.  
3. **Cálculo de duración** – Convertir el esfuerzo total en tiempo de calendario usando la disponibilidad del equipo y sus tasas de productividad.  
4. **Revisión de riesgos** – Ajustar la estimación con factores de incertidumbre (contingencia).  
5. **Comunicación de resultados** – Presentar la estimación al equipo y a los patrocinadores para validar el plan.

## Como funciona
1. **Crear el WBS**: desgloso el alcance en tareas concretas.  
2. **Estimar esfuerzo**: para cada tarea asigno horas‑persona basándome en experiencias pasadas y en la complejidad percibida.  
3. **Aplicar disponibilidad**: divido el esfuerzo total entre la capacidad diaria del equipo (horas‑disponibles) para obtener la duración en días.  
4. **Incluir contingencia**: añado un porcentaje de reserva según el nivel de riesgo identificado.  
5. **Validar con el equipo**: reviso las cifras con los responsables de cada área y ajusto según feedback.  
6. **Integrar al cronograma**: inserto las duraciones en el planning y establezco dependencias entre tareas.

## Detalles
- **Básico**: Uso de listas simples y valores promedio de productividad (ej. 8 h/día).  
- **Intermedio**: Aplicación de técnicas como *Planning Poker* o *Three‑Point Estimation* para refinar el esfuerzo y capturar la variabilidad.  
- **Avanzado**: Modelos de Monte Carlo o algoritmos de simulación que incorporan distribuciones probabilísticas y permiten generar curvas de probabilidad para la fecha de entrega.

## Ejemplo minimo
```python
# Estimación simple de esfuerzo
tareas = {
    "Diseño UI": 16,   # horas
    "Desarrollo API": 40,
    "Pruebas": 24
}
horas_por_dia = 8
esfuerzo_total = sum(tareas.values())
duracion_dias = esfuerzo_total / horas_por_dia
print(f"Duración estimada: {duracion_dias:.1f} días")
```

## Errores comunes
- **Subestimar la complejidad** – Ignorar factores técnicos lleva a cronogramas irrealistas; mitigarlo con revisión de riesgos.  
- **Usar una sola opinión** – Confiar en un estimador sin consenso genera sesgos; aplicar técnicas colaborativas.  
- **No actualizar la estimación** – Mantener valores estáticos después de cambios de alcance produce desviaciones; revisarla periódicamente.  
- **Olvidar la capacidad del equipo** – Multiplicar esfuerzo por 1 sin considerar vacaciones o carga existente inflará la duración; incluir disponibilidad real.

## Estado actual
**Fundamentos estables**: La práctica de descomponer el trabajo, asignar esfuerzo y convertirlo en duración sigue siendo la base de la gestión de proyectos.  
**Práctica moderna**: Se complementa con estimaciones ágiles (Planning Poker), análisis de riesgos cuantitativo y herramientas de simulación que generan probabilidades de cumplimiento, mejorando la precisión y la comunicación con stakeholders.

## Conexiones
- **Work Breakdown Structure**: Provee la estructura de paquetes de trabajo que se estiman; sin un WBS la estimación carece de unidades claras.  
- **Scheduling**: La duración obtenida de la estimación alimenta directamente el cronograma, definiendo fechas de inicio y fin de cada actividad.  
- **Project Metrics**: Las estimaciones sirven como línea base para métricas de variación (Earned Value, Schedule Variance) que evalúan el desempeño del proyecto.

## Ruta de estudio
1. **Prerequisitos**: Conocer los conceptos de alcance, WBS y capacidad del equipo.  
2. **Fundamentos**: Practicar estimaciones de esfuerzo con datos históricos y técnicas de tres puntos.  
3. **Intermedio**: Aprender Planning Poker y cómo integrar riesgos mediante factores de contingencia.  
4. **Avanzado**: Dominar simulaciones Monte Carlo y herramientas de análisis de valor ganado.  
5. **Aplicación**: Implementar estimaciones en un proyecto piloto, comparar la línea base con resultados reales y ajustar el proceso.

## Preguntas de repaso
1. ¿Cómo transforma la estimación de esfuerzo en una duración de calendario?  
2. ¿Qué papel juega el WBS en la generación de una estimación fiable?  
3. ¿Cuál es la diferencia entre una estimación puntual y una basada en tres puntos?  
4. ¿Por qué es importante revisar y actualizar la estimación durante la ejecución del proyecto?  
5. ¿Cómo se utilizan las estimaciones para calcular métricas de variación en Earned Value Management?

<!-- trazabilidad: run_id=run-20261109-172638-e4927d concept=10-project-management-08-estimation written_at=2026-11-09T20:27:48.348997+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/30 - Engineering Processes|Engineering Processes]] · *Software Engineering*
- [[10 - Project Management/05 - Work Breakdown Structure|Work Breakdown Structure]]
- [[10 - Project Management/06 - Task Management|Task Management]]
- [[10 - Project Management/07 - Dependencies|Dependencies]]
- [[10 - Project Management/09 - Planning|Planning]]
- [[10 - Project Management/10 - Scheduling|Scheduling]]
- [[10 - Project Management/24 - Project Metrics|Project Metrics]]

---
← [[10 - Project Management/07 - Dependencies|Dependencies]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/09 - Planning|Planning]] →
