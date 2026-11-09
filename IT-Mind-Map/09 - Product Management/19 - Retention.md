---
title: "Retention"
area: "Product Management"
numero: 19
aliases: ["Retention"]
tags: [concepto, it/product-management]
---
# Retention

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 19 de 25**

## Qué abarca
- Uso recurrente y comportamiento a lo largo del tiempo

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la métrica de **retention** para saber cuántos usuarios vuelven a usar mi producto después de su primera interacción. Resuelvo el problema de identificar si el valor entregado es sostenible en el tiempo y si las mejoras que implementamos realmente generan hábito. Aparece en mi día a día cuando analizo cohortes, priorizo funcionalidades de mejora y justifico inversiones en activación o engagement. Después de entenderla, puedo diseñar experimentos que apunten a aumentar la retención y comunicar su impacto a stakeholders. No necesito preocuparme de la retención cuando el producto está en fase de descubrimiento puro o cuando el objetivo principal es validar una hipótesis de mercado antes de lanzar.

## Esqueleto (el 20% esencial)
1. **Uso recurrente**: la retención mide cuántos usuarios vuelven a usar el producto en periodos definidos.  
2. **Comportamiento a lo largo del tiempo**: se analiza por cohortes para observar la evolución de la lealtad.  
3. **Indicador de valor entregado**: una alta retención indica que el producto satisface una necesidad continua.  
4. **Base para decisiones de inversión**: permite priorizar mejoras que impacten la frecuencia de uso.  

## Como funciona
1. Defino el horizonte temporal (día 1, 7, 30) y el criterio de “uso” (login, sesión, acción clave).  
2. Agrupo a los usuarios que realizaron su primera acción en el mismo día (cohorte).  
3. Para cada cohorte calculo el porcentaje que repite la acción en los periodos posteriores.  
4. Interpreto la curva de retención: caídas bruscas señalan fricción; mantenciones estables indican valor sostenido.  
5. Uso los resultados para decidir si invertir en onboarding, nuevas funcionalidades o campañas de re‑engagement.

## Detalles
- **Básico**: cálculo de retención día‑a‑día y visualización de la curva de cohortes.  
- **Intermedio**: segmentación por origen de adquisición, tipo de dispositivo o plan tarifario para identificar grupos con mayor fuga.  
- **Avanzado**: modelado predictivo de churn a partir de la retención histórica y pruebas A/B que comparen variantes de onboarding o notificaciones push.

## Ejemplo minimo
```python
# cálculo simple de retención día 7 en Python
import pandas as pd

# df: columnas user_id, signup_date, event_date
df['day'] = (df['event_date'] - df['signup_date']).dt.days
cohort = df[df['day'] == 0].groupby('signup_date')['user_id'].nunique()
day7   = df[df['day'] == 7].groupby('signup_date')['user_id'].nunique()
retention_day7 = (day7 / cohort).fillna(0)
print(retention_day7)
```

## Errores comunes
- Confundir retención con activación: la primera mide uso recurrente, la segunda la primera acción clave.  
- Usar periodos demasiado largos y diluir la señal de fuga temprana.  
- Ignorar la segmentación y asumir que una curva promedio representa a todos los usuarios.  

## Estado actual
**Fundamentos estables**: la definición de retención como porcentaje de usuarios que repiten una acción en un horizonte temporal definido y el uso de cohortes para su cálculo.  
**Práctica moderna**: integración de retención en dashboards de Product Analytics, combinación con modelos de churn y experimentación continua mediante feature flags y pruebas A/B.

## Conexiones
- **Product Metrics**: la retención es una de las métricas clave que complementa a adquisición, activación y revenue en el marco de métricas de producto.  
- **Funnels**: la caída entre etapas del funnel afecta directamente la retención; mejorar la conversión en etapas tempranas suele elevar la retención.  
- **Product Analytics**: las herramientas de analytics proporcionan los datos de eventos y cohortes necesarios para calcular y visualizar la retención.

## Ruta de estudio
1. **Prerequisitos**: conceptos de cohort analysis, eventos de tracking y fundamentos de SQL o Python para manipular datos.  
2. **Fundamentos**: tutoriales de cálculo de retención y visualización de cohortes en herramientas como Mixpanel o Amplitude.  
3. **Intermedio**: cursos sobre segmentación de usuarios y análisis de causas de churn.  
4. **Avanzado**: especializaciones en modelado predictivo de churn y diseño de experimentos de retención.  

## Preguntas de repaso
1. ¿Qué diferencia hay entre retención y activación en la gestión de un producto?  
2. ¿Cómo se construye una cohorte para medir la retención día 7?  
3. ¿Qué decisiones de producto pueden derivarse de una caída abrupta en la curva de retención?  
4. ¿Por qué es importante segmentar la retención por origen de adquisición?  
5. ¿Cómo se relaciona la retención con los funnels y qué implicaciones tiene para la optimización del funnel?

<!-- trazabilidad: run_id=run-20261106-210151-b56bae concept=09-product-management-19-retention written_at=2026-11-07T00:02:58.055207+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/17 - Product Metrics|Product Metrics]]
- [[09 - Product Management/18 - Funnels|Funnels]]
- [[09 - Product Management/20 - Product Analytics|Product Analytics]]

---
← [[09 - Product Management/18 - Funnels|Funnels]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/20 - Product Analytics|Product Analytics]] →
