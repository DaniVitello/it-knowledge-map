---
title: "Budget & Cost"
area: "Project Management"
numero: 23
aliases: ["Budget & Cost"]
tags: [concepto, it/project-management]
---
# Budget & Cost

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 23 de 25**

## Qué abarca
- Recursos financieros y trade-offs

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el concepto de **Budget & Cost** para garantizar que el proyecto se ejecute dentro de los límites financieros acordados, evitando sorpresas que comprometan la entrega o la calidad. Resuelvo el problema de la sobrecarga de gastos inesperados al alinear los recursos disponibles con los objetivos del proyecto. Aparece en cada fase del trabajo de un project manager senior: al iniciar la planificación, al monitorear el avance y al cerrar el proyecto con una evaluación de la rentabilidad. Después de entenderlo, puedo diseñar estructuras de control financiero, negociar trade‑offs y reportar el estado económico a los patrocinadores. No necesito preocuparme cuando el proyecto es de muy bajo costo y no requiere seguimiento financiero formal.

## Esqueleto (el 20% esencial)
1. **Definir el presupuesto total**: suma de todos los costos estimados que el proyecto podrá absorber.  
2. **Desglosar los costos**: asignar partidas a recursos, materiales, herramientas y contingencias.  
3. **Monitorear el gasto real vs. el planificado**: comparar periódicamente el gasto incurrido con el presupuesto.  
4. **Gestionar trade‑offs**: decidir entre alcance, calidad y tiempo cuando el gasto supera el presupuesto.  
5. **Comunicar el estado financiero**: informar a stakeholders sobre variaciones y decisiones correctivas.

## Como funciona
1. Al iniciar la planificación, reúno estimaciones de cada actividad y calculo el **budget** total.  
2. Creo una **estructura de desglose de costos (WBS)** que vincula cada paquete de trabajo con su partida presupuestaria.  
3. Durante la ejecución, registro los costos reales en el sistema de control financiero.  
4. Cada revisión de estado (semanal o mensual) genera un **variance report** que muestra desviaciones.  
5. Si la variación supera el umbral definido, evalúo trade‑offs y ajusto alcance, recursos o cronograma, comunicando la decisión al patrocinador.

## Detalles
- **Básico**: establecer un presupuesto simple basado en horas estimadas y tarifa promedio.  
- **Intermedio**: incorporar costos indirectos, reservas de contingencia y métricas de desempeño como CPI (Cost Performance Index).  
- **Avanzado**: aplicar técnicas de earned value management (EVM) para predecir desviaciones futuras y ejecutar escenarios de re‑presupuesto.

## Ejemplo minimo
```python
# Simulación mínima de control de presupuesto
presupuesto = 10000          # $10.000 asignados
gasto_acumulado = 0

def registrar_gasto(monto):
    global gasto_acumulado
    gasto_acumulado += monto
    print(f"Gasto total: ${gasto_acumulado} / ${presupuesto}")

registrar_gasto(2500)   # primera actividad
registrar_gasto(4000)   # segunda actividad
```

## Errores comunes
- **Subestimar costos**: usar estimaciones optimistas sin reservas. *Evitar*: aplicar factores de ajuste basados en datos históricos.  
- **Ignorar variaciones**: no revisar el gasto real frecuentemente. *Evitar*: establecer revisiones regulares y alertas de umbral.  
- **No comunicar**: ocultar desviaciones a los stakeholders. *Evitar*: reportar siempre con claridad y proponer acciones correctivas.

## Estado actual
Los fundamentos del presupuesto y control de costos son estables: definición del budget, desglose de partidas y seguimiento de variaciones. En la práctica moderna se complementa con herramientas de EVM, dashboards en tiempo real y análisis predictivo basados en IA para anticipar overruns.

## Conexiones
- **Resource Management**: los costos están directamente ligados a la asignación y utilización de recursos humanos y materiales.  
- **Risk Management**: las reservas de contingencia son una respuesta financiera a los riesgos identificados.  
- **Stakeholder Management**: la comunicación del estado financiero es clave para mantener el apoyo y la confianza de los patrocinadores.

## Ruta de estudio
1. Prerrequisitos: conceptos básicos de planificación de proyectos y estimación de esfuerzo.  
2. Fundamentos: aprender a crear un presupuesto y una WBS de costos.  
3. Intermedio: dominar earned value management y métricas CPI/ SPI.  
4. Avanzado: integrar herramientas de BI y análisis predictivo para gestión proactiva del presupuesto.  
5. Certificaciones recomendadas: PMI‑PMBOK® (sección de Cost Management) y PRINCE2 (tema de Costes).

## Preguntas de repaso
1. ¿Cuál es la diferencia entre presupuesto total y partida de costo desglosada?  
2. ¿Cómo se utiliza un variance report para decidir un trade‑off?  
3. ¿Qué métricas de earned value indican que el proyecto está sobrecostado?  
4. ¿Por qué es importante comunicar las desviaciones financieras a los stakeholders?  
5. ¿Qué papel juegan las reservas de contingencia dentro del manejo de riesgos?

<!-- trazabilidad: run_id=run-20261109-180350-01d70a concept=10-project-management-23-budget-cost written_at=2026-11-09T21:04:26.213722+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/12 - Resource Management|Resource Management]]

---
← [[10 - Project Management/22 - Team Coordination|Team Coordination]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/24 - Project Metrics|Project Metrics]] →
