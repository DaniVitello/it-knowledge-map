---
title: "Product Analytics"
area: "Product Management"
numero: 20
aliases: ["Product Analytics"]
tags: [concepto, it/product-management]
---
# Product Analytics

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 20 de 25**

## Qué abarca
- Análisis del comportamiento dentro del producto

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Product Analytics para observar cómo los usuarios interactúan con nuestro producto digital, identificar cuellos de botella y validar hipótesis de negocio. Resuelvo la falta de evidencia objetiva al decidir qué mejoras priorizar, y lo aplico cada vez que necesito medir el impacto de una nueva funcionalidad o de un cambio de diseño. Después de entenderlo, puedo diseñar experimentos, definir métricas clave y traducir los datos en decisiones de roadmap. No me preocupo por Product Analytics cuando el producto está en fase de concepto sin usuarios reales o cuando la decisión se basa exclusivamente en requisitos regulatorios que no dependen del comportamiento del usuario.

## Esqueleto (el 20% esencial)
1. **Definir eventos clave**: seleccionar acciones de usuario que reflejen valor (p. ej., “añadir al carrito”).  
2. **Construir funnels**: ordenar eventos para visualizar la caída entre pasos críticos.  
3. **Medir retención**: seguir a los usuarios a lo largo del tiempo para evaluar la stickiness del producto.  
4. **Establecer métricas de producto**: transformar los eventos en indicadores accionables (conversion rate, churn).  
5. **Iterar con decisiones basadas en datos**: usar los insights para priorizar mejoras y validar experimentos.

## Como funciona
1. **Recolectar datos**: instrumentamos el front‑end o el backend con eventos definidos.  
2. **Almacenar y procesar**: los eventos se envían a un almacén de datos (p. ej., Snowflake) y se transforman en tablas de análisis.  
3. **Crear funnels**: con una herramienta de analytics (Mixpanel, Amplitude) configuramos la secuencia de eventos y observamos la tasa de caída en cada paso.  
4. **Calcular métricas**: a partir de los funnels extraemos conversiones, tiempo medio entre pasos y tasas de abandono.  
5. **Analizar retención**: agrupamos usuarios por cohortes de adquisición y medimos su actividad en semanas o meses posteriores.  
6. **Tomar decisiones**: los resultados guían la priorización del backlog y la definición de experimentos A/B.

## Detalles
- **Básico**: definir un pequeño conjunto de eventos (click, compra) y visualizar un funnel simple de adquisición → activación.  
- **Intermedio**: añadir segmentación por origen de tráfico y calcular cohortes de retención semanal; combinar con métricas de negocio (ARPU).  
- **Avanzado**: implementar modelado de atribución multicanal, usar análisis de correlación para descubrir drivers de churn y alimentar un dashboard en tiempo real para el equipo de producto.

## Ejemplo minimo
```javascript
// Registro de evento "Add to Cart" con Segment
analytics.track('Add to Cart', {
  productId: 'SKU_12345',
  price: 29.99,
  currency: 'USD'
});
```
Este fragmento envía el evento clave que luego podrá ser usado en un funnel de “Visita → Add to Cart → Compra”.

## Errores comunes
- **Medir lo que es fácil, no lo que importa** – evítalo alineando eventos con objetivos de negocio.  
- **Ignorar la segmentación** – corrige analizando por canal, dispositivo o cohortes.  
- **Confundir correlación con causalidad** – valida hipótesis con experimentos controlados.

## Estado actual
Los fundamentos de Product Analytics (definición de eventos, funnels y retención) son estables y ampliamente adoptados. En la práctica moderna, se complementan con plataformas de análisis en tiempo real, modelado de atribución y dashboards auto‑servicio que permiten a los equipos de producto consultar datos sin depender del equipo de datos.

## Conexiones
- **Product Metrics**: las métricas de producto son los indicadores que extraemos de los eventos analizados.  
- **Funnels**: los funnels estructuran la secuencia de eventos para detectar pérdidas en el recorrido del usuario.  
- **Retention**: la retención usa los mismos eventos para medir la continuidad del uso a lo largo del tiempo.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de eventos, bases de datos relacionales y SQL.  
2. **Fundamentos**: aprender a instrumentar eventos y crear funnels en una herramienta como Amplitude.  
3. **Intermedio**: profundizar en cohort analysis y métricas de retención, practicar con SQL de cohortes.  
4. **Avanzado**: estudiar atribución multicanal, experimentación A/B y visualización de datos en dashboards.  
5. **Especialización**: integrar Product Analytics con OKR y roadmaps estratégicos.

## Preguntas de repaso
1. ¿Qué tipo de evento consideraría “clave” para medir la activación de un nuevo usuario?  
2. ¿Cómo se construye un funnel y qué información revela sobre la caída de usuarios?  
3. ¿Cuál es la diferencia entre una métrica de producto y una métrica de negocio?  
4. ¿Qué pasos seguiría para analizar la retención de usuarios adquiridos en el último mes?  
5. ¿Por qué es importante validar una hipótesis con un experimento A/B después de observar un insight en Product Analytics?

<!-- trazabilidad: run_id=run-20261106-210258-f44aa1 concept=09-product-management-20-product-analytics written_at=2026-11-07T00:03:34.172351+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/17 - Product Metrics|Product Metrics]]
- [[09 - Product Management/18 - Funnels|Funnels]]
- [[09 - Product Management/19 - Retention|Retention]]

---
← [[09 - Product Management/19 - Retention|Retention]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/21 - Product-Market Fit|Product-Market Fit]] →
