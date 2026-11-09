---
title: "UX Metrics"
area: "UX / UI"
numero: 23
aliases: ["UX Metrics"]
tags: [concepto, it/ux-ui]
---
# UX Metrics

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 23 de 25**

## Qué abarca
- Completion rate
- time-on-task
- retention
- conversion

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los UX Metrics para cuantificar cómo los usuarios interactúan con una interfaz y detectar cuellos de botella en la experiencia. Resuelvo la incertidumbre de si un flujo de usuario está cumpliendo sus objetivos y si el producto está generando valor sostenido. Aparecen en cada fase del diseño de producto senior: al validar prototipos, al priorizar mejoras y al demostrar el impacto de decisiones de diseño a stakeholders. Después de entenderlos, puedo definir experimentos, comparar versiones y alinear el roadmap con datos reales. No necesito preocuparme cuando el producto está en fase de ideación sin usuarios reales o cuando la métrica no aporta información accionable para la decisión actual.

## Esqueleto (el 20% esencial)
1. **Completion rate** – porcentaje de usuarios que finalizan una tarea clave.  
2. **Time‑on‑task** – tiempo medio que tarda un usuario en completar esa tarea.  
3. **Retention** – frecuencia con la que los usuarios vuelven al producto después de la primera visita.  
4. **Conversion** – proporción de usuarios que pasan de un estado a otro deseado (p. ej. registro, compra).  

## Como funciona
1. Defino la tarea o evento crítico que quiero medir (p. ej. completar el checkout).  
2. Configuro la captura de datos en la herramienta de analítica (eventos de “start” y “complete”).  
3. Calculo el **completion rate** dividiendo completados entre iniciados.  
4. Registro timestamps para cada evento y obtengo el **time‑on‑task** promedio.  
5. Analizo la **retention** mediante cohortes que comparan la actividad de usuarios nuevos a lo largo del tiempo.  
6. Mido la **conversion** en cada paso del funnel y la relaciono con cambios de diseño para validar hipótesis.

## Detalles
- **Básico**: elegir métricas alineadas con los objetivos de negocio y configurar eventos simples.  
- **Intermedio**: segmentar los datos por dispositivo, canal de adquisición o perfil de usuario para identificar patrones ocultos.  
- **Avanzado**: combinar UX Metrics con **Analytics Metrics** (páginas vistas, bounce rate) y con indicadores de **Product Metrics** (ARPU, churn) para crear un cuadro de mando integral que guíe decisiones estratégicas.

## Ejemplo minimo
```json
{
  "event": "checkout_complete",
  "userId": "12345",
  "timestamp": "2026-11-06T14:23:10Z",
  "task": "checkout",
  "durationMs": 8420
}
```
Este registro permite calcular tanto el completion rate (contando eventos “checkout_start” vs “checkout_complete”) como el time‑on‑task (duración en milisegundos).

## Errores comunes
- Medir métricas sin vincularlas a un objetivo de negocio → evita la acción al no saber qué mejorar.  
- Ignorar la segmentación de usuarios → se pierden diferencias críticas entre grupos.  
- Confundir correlación con causalidad → no atribuyas mejoras de métricas a cambios de diseño sin pruebas controladas.  

## Estado actual
**Fundamentos estables**: los cuatro indicadores (completion rate, time‑on‑task, retention, conversion) siguen siendo la base para evaluar usabilidad y efectividad de flujos.  
**Práctica moderna**: se integran con plataformas de análisis de eventos en tiempo real y se combinan con métricas de **Usability Testing** (task success, error rate) para validar hipótesis antes de lanzar cambios a producción.

## Conexiones
- **Analytics Metrics**: proporcionan el contexto cuantitativo (tráfico, fuentes) que complementa los UX Metrics centrados en la experiencia.  
- **Usability**: los UX Metrics son indicadores operacionales que reflejan la usabilidad percibida por los usuarios.  
- **Product Metrics**: la conversión y retención alimentan métricas de negocio como ingresos y churn, cerrando el ciclo entre experiencia y resultados comerciales.  

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de investigación de usuarios, definición de tareas y familiaridad con herramientas de analítica de eventos.  
2. **Fundamentos**: aprender a definir y capturar completion rate y time‑on‑task; practicar con datasets simples.  
3. **Intermedio**: profundizar en cohort analysis para retention y en funnel analysis para conversion; usar dashboards para visualización.  
4. **Avanzado**: integrar UX Metrics con Analytics Metrics y Product Metrics; diseñar experimentos A/B que midan impacto directo de cambios de UI.  

## Preguntas de repaso
1. ¿Qué diferencia hay entre completion rate y conversion en el contexto de un funnel de compra?  
2. ¿Cómo se calcula el time‑on‑task a partir de eventos de “start” y “complete”?  
3. ¿Por qué es importante segmentar la retención por cohortes en lugar de usar un promedio global?  
4. ¿Qué riesgo implica interpretar una mejora en conversion sin validar mediante Usability Testing?  
5. ¿Cómo pueden los UX Metrics influir en la priorización del roadmap de producto?

<!-- trazabilidad: run_id=run-20261106-203414-2d3968 concept=08-ux-ui-23-ux-metrics written_at=2026-11-06T23:35:12.700132+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]] · *Database / Data Analytics*
- [[08 - UX & UI/21 - Usability|Usability]]
- [[08 - UX & UI/22 - Usability Testing|Usability Testing]]
- [[09 - Product Management/17 - Product Metrics|Product Metrics]] · *Product Management*
- [[10 - Project Management/24 - Project Metrics|Project Metrics]] · *Project Management*

---
← [[08 - UX & UI/22 - Usability Testing|Usability Testing]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/24 - Behavior & Psychology|Behavior & Psychology]] →
