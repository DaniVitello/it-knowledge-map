---
title: "Product Discovery"
area: "Product Management"
numero: 14
aliases: ["Product Discovery"]
tags: [concepto, it/product-management]
---
# Product Discovery

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 14 de 25**

## Qué abarca
- Explorar soluciones antes de construir

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Product Discovery para validar que el problema que quiero resolver realmente existe y que la solución propuesta genera valor antes de invertir recursos en su construcción. Resuelvo la incertidumbre de “¿estamos construyendo lo correcto?” y lo aplico en la fase inicial de cualquier iniciativa de producto digital, cuando defino la visión, priorizo el backlog y alineo a los stakeholders. Después de entenderlo, puedo diseñar hipótesis, planificar experimentos y decidir si avanzar a un MVP o descartar la idea. No necesito preocuparme por Product Discovery cuando el producto ya está en fase de crecimiento estable y las decisiones se basan en métricas de rendimiento consolidadas.

## Esqueleto (el 20% esencial)
1. **Identificar una necesidad real del usuario** mediante entrevistas, observación o análisis de datos.  
2. **Formular hipótesis de solución** que puedan ser validadas rápidamente.  
3. **Diseñar experimentos de bajo costo** (prototipos, pruebas de concepto) para probar esas hipótesis.  
4. **Medir resultados y decidir** si se avanza, se pivota o se abandona la idea.  

## Como funciona
1. Reúno insights de usuarios y del mercado para definir una necesidad clara.  
2. Con esa necesidad, redacto una hipótesis concreta: “Si entregamos X, los usuarios aumentarán Y”.  
3. Selecciono el método de experimentación más barato (paper prototype, mockup clickable, landing page).  
4. Ejecutó el experimento con un grupo representativo y recojo métricas cualitativas y cuantitativas.  
5. Analizo los datos; si la hipótesis se confirma, paso a diseñar un MVP; si no, pivoto o descarto.

## Detalles
- **Básico:** entrevistas breves y mapas de empatía para captar la necesidad.  
- **Intermedio:** creación de prototipos de baja fidelidad y pruebas A/B en landing pages para validar la hipótesis.  
- **Avanzado:** simulaciones de flujo de usuario, pruebas de usabilidad con métricas de tiempo y éxito, y análisis estadístico de resultados para decisiones de pivote.

## Ejemplo minimo
```python
# Simulación rápida de una landing page para validar interés en una nueva función
import random

def simulate_visitors(n):
    conversions = 0
    for _ in range(n):
        # supongamos una tasa de conversión esperada del 10%
        if random.random() < 0.10:
            conversions += 1
    return conversions / n

tasa = simulate_visitors(200)
print(f"Tasa de conversión simulada: {tasa:.2%}")
```
Si la tasa supera el umbral definido (p. ej. 8 %), la hipótesis se considera validada y se procede al MVP.

## Errores comunes
- **Asumir que la necesidad está confirmada** sin datos reales; evitarlo con entrevistas y pruebas tempranas.  
- **Construir un prototipo demasiado completo** que consume tiempo y recursos; mantener la mínima fidelidad necesaria.  
- **Interpretar resultados sin métricas claras**; definir criterios de éxito antes del experimento.

## Estado actual
- **Fundamentos estables:** la práctica de validar hipótesis antes de construir es un pilar del Lean Product Development y se mantiene como base del proceso de descubrimiento.  
- **Práctica moderna:** uso de herramientas de prototipado colaborativo (Figma, Miro) y plataformas de pruebas rápidas (LaunchDarkly, Optimizely) para acelerar la experimentación y obtener datos en tiempo real.

## Conexiones
- **MVP:** el resultado validado del Product Discovery alimenta la definición del Minimum Viable Product, que lleva la solución probada al mercado con el menor esfuerzo.  
- **Experimentation:** la fase de descubrimiento se apoya en técnicas de experimentación para probar hipótesis de forma controlada.  
- **User Research:** las entrevistas y observaciones que inician el descubrimiento provienen de prácticas estructuradas de investigación de usuarios.

## Ruta de estudio
1. **Prerequisitos:** fundamentos de User Research y métricas de producto.  
2. **Fundamental:** leer casos de estudio de Product Discovery y practicar entrevistas estructuradas.  
3. **Intermedio:** aprender a crear prototipos de baja fidelidad y a diseñar pruebas A/B.  
4. **Avanzado:** dominar herramientas de prototipado colaborativo y análisis estadístico de experimentos.  
5. **Especialización:** integrar descubrimiento con roadmaps estratégicos y gestión de stakeholders.

## Preguntas de repaso
1. ¿Cómo diferencia el Product Discovery de la fase de desarrollo de un MVP?  
2. ¿Qué criterios utilizas para decidir si una hipótesis está suficientemente validada?  
3. ¿Por qué es importante mantener la mínima fidelidad en los prototipos durante el descubrimiento?  
4. ¿Qué papel juega la experimentación en la reducción del riesgo de producto?  
5. ¿Cómo integras los insights obtenidos en el descubrimiento al roadmap de producto?

<!-- trazabilidad: run_id=run-20261109-163407-558bda concept=09-product-management-14-product-discovery written_at=2026-11-09T19:35:28.108582+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/15 - MVP|MVP]]
- [[09 - Product Management/16 - Experimentation|Experimentation]]

---
← [[09 - Product Management/13 - User Stories|User Stories]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/15 - MVP|MVP]] →
