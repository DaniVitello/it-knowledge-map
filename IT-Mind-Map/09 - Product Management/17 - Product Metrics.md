---
title: "Product Metrics"
area: "Product Management"
numero: 17
aliases: ["Product Metrics"]
tags: [concepto, it/product-management]
---
# Product Metrics

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 17 de 25**

## Qué abarca
- Métricas para evaluar el producto

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo las product metrics para medir si el producto está cumpliendo los objetivos de negocio y de experiencia de usuario que definí en la hoja de ruta. Resuelvo la incertidumbre sobre qué funcionalidades están generando valor y cuáles deben ser descartadas o mejoradas. Aparecen en cada ciclo de descubrimiento, desarrollo y evaluación, cuando necesito decidir si priorizo una nueva característica, ajusto el pricing o invierto en retención. Después de entenderlas, puedo diseñar experimentos, comunicar resultados a stakeholders y alinear al equipo en torno a indicadores claros. No me preocupo por ellas cuando el producto está en fase de ideación sin hipótesis cuantificables o cuando la métrica principal es simplemente la entrega a tiempo de un proyecto interno.

## Esqueleto (el 20% esencial)
1. **Definir la métrica alineada al objetivo del producto** – la métrica debe reflejar directamente el valor que queremos crear.  
2. **Instrumentar la captura de datos** – integrar herramientas de analytics que registren el comportamiento relevante.  
3. **Monitorear y comparar contra umbrales** – establecer rangos de desempeño (p.ej., 5 % de churn mensual) y alertas.  
4. **Iterar basándose en los resultados** – usar la métrica para validar hipótesis y priorizar el backlog.  
5. **Comunicar el impacto** – traducir los números en historias comprensibles para el equipo y la dirección.

## Como funciona
1. **Identifico el objetivo** (crecer usuarios activos, reducir churn, aumentar conversiones).  
2. **Selecciono la métrica** que mejor lo represente (DAU, churn rate, conversion funnel).  
3. **Configuro la herramienta** (Mixpanel, Amplitude, Google Analytics) para registrar los eventos necesarios.  
4. **Recojo datos en tiempo real** y los visualizo en dashboards.  
5. **Comparo con los umbrales** definidos en la fase de planificación.  
6. **Decido**: si la métrica está bajo, propongo experimentos; si está sobre, escalo la solución.  
7. **Reporto** los hallazgos y actualizo la hoja de ruta.

## Detalles
- **Básico:** elegir una única métrica de negocio (p.ej., revenue) y observar su tendencia semanal.  
- **Intermedio:** combinar métricas de producto (engagement) con métricas de negocio (LTV) para crear un cuadro de mando equilibrado.  
- **Avanzado:** aplicar cohort analysis, segmentación y modelado predictivo para anticipar comportamientos y guiar decisiones estratégicas de roadmap.

## Ejemplo minimo
```json
{
  "event": "purchase_completed",
  "properties": {
    "user_id": "12345",
    "amount_usd": 49.99,
    "timestamp": "2026-11-05T14:23:00Z"
  }
}
```
Este evento alimenta la métrica *Revenue per Paying User* que se monitorea diariamente.

## Errores comunes
- **Métrica equivocada:** elegir un indicador que no está ligado al objetivo del negocio; evitarlo alineando métricas con OKR.  
- **Sobrecarga de datos:** medir demasiadas cosas a la vez y perder foco; limitarse a 3‑5 métricas clave.  
- **Umbrales estáticos:** no actualizar los rangos de desempeño cuando el producto escala; revisarlos trimestralmente.

## Estado actual
- **Fundamentos estables:** la práctica de definir métricas alineadas a objetivos y usar dashboards para seguimiento es ampliamente aceptada.  
- **Práctica moderna:** la integración de product analytics con machine learning para predicción de churn y la adopción de métricas de salud del producto (health scores) están en crecimiento.

## Conexiones
- **Analytics Metrics**: proporcionan los datos brutos que convierto en product metrics para evaluar el desempeño.  
- **Retention**: una métrica de retención (p. ej., 30‑day retention) es una product metric clave para decidir inversiones en mejoras de experiencia.  
- **Funnels**: los funnels de conversión generan métricas de tasa de conversión que guían la priorización de funcionalidades.

## Ruta de estudio
1. **Prerequisitos:** conceptos básicos de métricas de negocio (KPIs), fundamentos de analytics y manejo de herramientas como Google Analytics.  
2. **Fundamentos:** aprender a definir métricas SMART y a crear dashboards simples.  
3. **Intermedio:** estudiar cohort analysis y cómo combinar métricas de producto con métricas financieras.  
4. **Avanzado:** profundizar en modelado predictivo, health scores y automatización de alertas.  
5. **Aplicación práctica:** liderar un experimento A/B y presentar los resultados a la dirección.

## Preguntas de repaso
1. ¿Cómo elijo una product metric que esté alineada al objetivo de negocio?  
2. ¿Qué pasos sigo para instrumentar la captura de datos de una métrica nueva?  
3. ¿Por qué es importante establecer umbrales y cómo los mantengo actualizados?  
4. ¿Cuál es la diferencia entre una analytics metric y una product metric?  
5. ¿Cómo utilizo los resultados de una métrica de retención para priorizar el backlog?

<!-- trazabilidad: run_id=run-20261106-205722-d93e01 concept=09-product-management-17-product-metrics written_at=2026-11-06T23:58:28.652199+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]] · *Database / Data Analytics*
- [[08 - UX & UI/23 - UX Metrics|UX Metrics]] · *UX / UI*
- [[09 - Product Management/18 - Funnels|Funnels]]
- [[09 - Product Management/19 - Retention|Retention]]
- [[09 - Product Management/20 - Product Analytics|Product Analytics]]
- [[10 - Project Management/24 - Project Metrics|Project Metrics]] · *Project Management*

---
← [[09 - Product Management/16 - Experimentation|Experimentation]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/18 - Funnels|Funnels]] →
