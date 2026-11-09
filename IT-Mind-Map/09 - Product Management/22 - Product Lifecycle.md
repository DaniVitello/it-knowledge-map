---
title: "Product Lifecycle"
area: "Product Management"
numero: 22
aliases: ["Product Lifecycle"]
tags: [concepto, it/product-management]
---
# Product Lifecycle

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 22 de 25**

## Qué abarca
- Discovery → launch → growth → maturity

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Product Lifecycle para planificar y guiar cada fase del producto digital, asegurando que las decisiones de inversión, priorización y comunicación estén alineadas con la realidad del mercado y la capacidad del equipo. Resuelvo la incertidumbre de *cuándo* lanzar nuevas funcionalidades, *cómo* escalar el producto y *cuándo* iniciar la transición a mantenimiento o sustitución. Aparece en mi día a día cuando defino el roadmap, evalúo métricas de adopción y decido si seguimos invirtiendo en crecimiento o empezamos a optimizar costos. Después de entenderlo, puedo estructurar experimentos, negociar recursos y comunicar el estado del producto a stakeholders. No necesito preocuparme cuando el producto está en fase de descontinuación o cuando la estrategia corporativa define un cierre inmediato sin fase de madurez.

## Esqueleto (el 20% esencial)
1. **Discovery** – Identifico oportunidades y valido hipótesis antes de construir.  
2. **Launch** – Entrego el MVP al mercado y comienzo a medir la respuesta real.  
3. **Growth** – Escalo funcionalidades y canales basándome en datos de adopción.  
4. **Maturity** – Optimizo costos, estabilizo ingresos y gestiono la eventual declinación.

## Como funciona
1. En **Discovery** reúno insights de usuarios y analizo la competencia; defino el problema a resolver.  
2. Paso a **Launch** construyendo un MVP que pruebe el Product‑Market Fit; lo lanzo a un segmento piloto y recojo métricas clave (activación, retención).  
3. Con evidencia de ajuste, entro en **Growth**: priorizo mejoras que aumenten el LTV y el CAC, activo campañas de Go‑to‑Market y escalo la infraestructura.  
4. Cuando las métricas de crecimiento se estabilizan, entro en **Maturity**: reduzco la velocidad de releases, foco en eficiencia operativa y preparo planes de sunset o de expansión a nuevos mercados.

## Detalles
- **Básico**: entender que cada fase tiene objetivos claros (validación, entrega, escalado, optimización).  
- **Intermedio**: aplicar métricas específicas por fase (por ejemplo, *product‑market fit score* en Launch, *growth rate* en Growth).  
- **Avanzado**: gestionar transiciones entre fases mediante *stage‑gate reviews*, alineando recursos y ajustando el Go‑to‑Market según la evolución del mercado.

## Ejemplo minimo
```python
# Simulación simple de transición de fase basada en métricas
def next_phase(active_users, growth_rate):
    if active_users < 1000:
        return "Discovery"
    elif growth_rate > 0.20:
        return "Growth"
    else:
        return "Maturity"

print(next_phase(active_users=1500, growth_rate=0.25))  # → Growth
```

## Errores comunes
- **Confundir MVP con producto final** – Evitar lanzar sin validar el Product‑Market Fit.  
- **Ignorar la fase de Discovery** – No dedicar tiempo a la investigación genera pivotes costosos.  
- **Pasar a Growth sin métricas de retención** – Asegurar que los usuarios vuelvan antes de escalar.

## Estado actual
Los fundamentos del Product Lifecycle (Discovery, Launch, Growth, Maturity) son estables y ampliamente adoptados en metodologías ágiles y de gestión de productos digitales. La práctica moderna incorpora métricas en tiempo real y automatiza los *stage‑gate* con plataformas de analytics, pero la secuencia de fases sigue siendo la misma.

## Conexiones
- **MVP**: el entregable mínimo que permite validar el Product‑Market Fit durante la fase de Launch.  
- **Product‑Market Fit**: criterio que determina si el producto está listo para entrar en Growth.  
- **Go‑to‑Market**: estrategia de lanzamiento y expansión que se diseña en la transición de Launch a Growth.

## Ruta de estudio
1. **Prerequisitos**: fundamentos de UX research, métricas de producto (CAC, LTV, churn).  
2. **Fundamentos**: estudiar casos de Discovery y técnicas de validación de hipótesis.  
3. **Intermedio**: profundizar en diseño de MVP y metodologías de lanzamiento rápido.  
4. **Avanzado**: aprender a diseñar planes de Growth basados en cohort analysis y a gestionar la fase de Maturity con técnicas de optimización de costos y roadmap de sunset.

## Preguntas de repaso
1. ¿Qué objetivo principal persigue la fase de Discovery dentro del Product Lifecycle?  
2. ¿Cómo determina el MVP si el producto está listo para pasar a la fase de Launch?  
3. ¿Qué métricas son críticas para decidir que un producto ha alcanzado Product‑Market Fit?  
4. ¿Cuál es la diferencia clave entre las decisiones de inversión en la fase de Growth y en la de Maturity?  
5. ¿Cómo se relaciona la estrategia Go‑to‑Market con la transición de Launch a Growth?

<!-- trazabilidad: run_id=run-20261106-210412-bd32dc concept=09-product-management-22-product-lifecycle written_at=2026-11-07T00:05:11.146876+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/15 - MVP|MVP]]
- [[09 - Product Management/21 - Product-Market Fit|Product-Market Fit]]
- [[09 - Product Management/24 - Go-to-Market|Go-to-Market]]

---
← [[09 - Product Management/21 - Product-Market Fit|Product-Market Fit]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/23 - Stakeholder Management|Stakeholder Management]] →
