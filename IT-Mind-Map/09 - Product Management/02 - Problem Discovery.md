---
title: "Problem Discovery"
area: "Product Management"
numero: 2
aliases: ["Problem Discovery"]
tags: [concepto, it/product-management]
---
# Problem Discovery

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 2 de 25**

## Qué abarca
- Identificar problemas reales

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Problem Discovery para detectar, validar y priorizar los problemas reales que enfrentan mis usuarios antes de diseñar soluciones. Resuelvo la incertidumbre de “¿qué debemos construir?” al enfocarme en necesidades verificadas, lo que me permite alinear el roadmap con oportunidades de negocio tangibles. Aparece en la fase inicial del ciclo de vida del producto, justo después de la visión y antes de la definición de requisitos. Después de entenderlo, puedo estructurar hipótesis de solución, diseñar experimentos y comunicar de forma clara el valor esperado a stakeholders. No necesito preocuparme de Problem Discovery cuando el producto ya está en fase de optimización y los problemas críticos están bien documentados.

## Esqueleto (el 20% esencial)
1. **Identificar problemas reales**: observar comportamientos y síntomas que indican fricción o insatisfacción.  
2. **Validar con datos**: corroborar la existencia y magnitud del problema mediante métricas o entrevistas.  
3. **Priorizar por impacto**: comparar el costo de no resolverlo contra el valor potencial para el negocio.  
4. **Formular hipótesis de solución**: traducir el problema en una pregunta de experimentación clara.  

## Como funciona
1. **Observación** – Recojo señales de uso (abandonos, tickets, comentarios) que sugieren un dolor.  
2. **Investigación** – Conduzco user research (entrevistas, encuestas) y market research para confirmar que el síntoma corresponde a un problema estructural.  
3. **Análisis de datos** – Mido frecuencia, severidad y segmento afectado; utilizo métricas como churn rate o NPS.  
4. **Matriz de priorización** – Ubico el problema en una cuadrícula impacto‑esfuerzo y lo comparo con otros hallazgos.  
5. **Hipótesis** – Redacto una hipótesis “Si cambiamos X, entonces Y mejorará en Z%”. Esta guía la siguiente fase de experimentación.

## Detalles
- **Básico**: reconocer patrones visibles (p. ej., alta tasa de rebote) y registrar preguntas abiertas.  
- **Intermedio**: aplicar técnicas de user research (jobs‑to‑be‑done, mapas de empatía) y combinar con datos cuantitativos para validar la hipótesis del problema.  
- **Avanzado**: usar análisis causal (A/B testing preliminar, cohort analysis) para aislar la raíz del problema y estimar el ROI de su solución, integrando insights de Product Thinking para alinear con la visión estratégica.

## Ejemplo minimo
```python
# Simulación simple de detección de problema de alta tasa de abandono en onboarding
import pandas as pd

data = pd.read_csv('onboarding_events.csv')
abandon_rate = data['completed'].mean()
if abandon_rate < 0.6:
    print("Problema detectado: alta tasa de abandono (>40%)")
else:
    print("No hay problema crítico en onboarding")
```

## Errores comunes
- **Confundir síntomas con problemas** – profundizar solo en lo visible sin validar la causa raíz.  
- **Priorizar por facilidad** – elegir problemas fáciles de resolver en lugar de los de mayor impacto.  
- **Ignorar datos cuantitativos** – basarse solo en opiniones cualitativas sin medir magnitud.  

## Estado actual
- **Fundamentos estables**: la práctica de combinar observación, investigación de usuarios y análisis de datos para descubrir problemas está consolidada en metodologías de Product Management.  
- **Práctica moderna**: la integración de herramientas de analytics en tiempo real y frameworks de hipótesis (Lean Startup, Opportunity Solution Tree) permite iterar más rápido y validar problemas con menor sesgo.

## Conexiones
- **Product Thinking**: aporta la mentalidad de enfocarse en el valor para el usuario, lo que guía la selección de problemas a investigar.  
- **User Research**: provee los métodos cualitativos (entrevistas, pruebas de usabilidad) que alimentan la fase de validación del problema.  
- **Market Research**: contextualiza el problema dentro de tendencias y competidores, asegurando que la solución tenga relevancia de mercado.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de métricas de producto (KPIs, funnel), fundamentos de user research y análisis de datos.  
2. **Fundamentos**: leer casos de estudio de discovery, practicar entrevistas estructuradas y análisis de abandono.  
3. **Intermedio**: aprender a construir matrices de priorización y a formular hipótesis medibles.  
4. **Avanzado**: dominar técnicas de causalidad (experimentación, cohort analysis) y aplicar frameworks como Opportunity Solution Tree.  
5. **Especialización**: combinar Problem Discovery con estrategias de growth hacking y roadmap estratégico.

## Preguntas de repaso
1. ¿Cómo diferencio un síntoma de un problema real en la gestión de un producto?  
2. ¿Qué métricas usaría para validar la magnitud de un problema detectado?  
3. ¿Por qué es importante priorizar problemas por impacto antes que por facilidad de solución?  
4. ¿Cómo se traduce un problema validado en una hipótesis de solución ejecutable?  
5. ¿Qué rol juegan Product Thinking, User Research y Market Research en el proceso de Problem Discovery?

<!-- trazabilidad: run_id=run-20261106-203825-9fb962 concept=09-product-management-02-problem-discovery written_at=2026-11-06T23:39:07.636501+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/01 - Product Thinking|Product Thinking]]
- [[09 - Product Management/03 - User Research|User Research]]
- [[09 - Product Management/04 - Market Research|Market Research]]

---
← [[09 - Product Management/01 - Product Thinking|Product Thinking]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/03 - User Research|User Research]] →
