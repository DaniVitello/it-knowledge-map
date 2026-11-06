---
title: "Analytics Metrics"
area: "Database / Data Analytics"
numero: 22
aliases: ["Analytics Metrics"]
tags: [concepto, it/database-data-analytics]
---
# Analytics Metrics

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 22 de 25**

## Qué abarca
- KPIs
- métricas
- dimensiones
- ratios

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **Analytics Metrics** para transformar datos crudos en indicadores accionables que guían decisiones de negocio y de producto. Resuelvo el problema de “¿qué está pasando?” y “¿cómo lo medimos?” al definir métricas que combinan valores numéricos (KPIs, ratios) con contextos (dimensiones). En mi día a día como ingeniero de datos y analista senior, las métricas aparecen al diseñar modelos de datos, crear dashboards y validar hipótesis. Después de entenderlas, puedo diseñar pipelines que calculen métricas en tiempo real, comparar resultados entre segmentos y automatizar alertas. No necesito preocuparme cuando el objetivo es simplemente explorar datos sin necesidad de seguimiento continuo o cuando los stakeholders no requieren indicadores de rendimiento.

## Esqueleto (el 20% esencial)
1. **KPI (Key Performance Indicator)** – Métrica clave alineada con objetivos de negocio.  
2. **Dimensiones** – Atributos (p. ej. fecha, región, canal) que segmentan la métrica.  
3. **Ratios** – Relaciones entre dos o más métricas que revelan eficiencia o calidad.  
4. **Métricas derivadas** – Cálculos (p. ej. crecimiento % mensual) construidos a partir de métricas base.  

## Como funciona
1. **Definir objetivo** → selecciono el KPI que refleje la meta (p. ej. “ventas netas”).  
2. **Identificar dimensiones** → determino los atributos que permitirán segmentar el KPI (fecha, producto).  
3. **Modelar la métrica** → creo la expresión SQL o la lógica de transformación que calcule el KPI.  
4. **Agregar ratios** → si necesito eficiencia, divido el KPI entre otra métrica (p. ej. “ventas / visitas”).  
5. **Persistir y exponer** → almaceno el resultado en una tabla de métricas o lo envío a una herramienta de BI.  

## Detalles
- **Básico**: Selección de KPI y dimensiones; cálculo directo con `SUM`, `COUNT`.  
- **Intermedio**: Uso de ventanas (`OVER`) para ratios y comparaciones temporales; creación de tablas de hechos de métricas.  
- **Avanzado**: Métricas de tipo *slowly changing dimensions*, cálculo de percentiles, integración con pipelines de streaming para métricas en tiempo real, y modelado de métricas compuestas (p. ej. LTV = ARPU × churn‑rate⁻¹).  

## Ejemplo minimo
```sql
-- KPI: ingresos netos por día y categoría
SELECT
    DATE(order_timestamp)      AS fecha,
    product_category           AS categoria,
    SUM(order_amount)          AS ingresos_neto,
    COUNT(*)                   AS total_ordenes,
    SUM(order_amount) / COUNT(*) AS ticket_promedio
FROM orders
WHERE order_status = 'completed'
GROUP BY DATE(order_timestamp), product_category;
```

## Errores comunes
- **Confundir KPI con métrica operativa** → elegir una métrica que no se alinea con la meta del negocio.  
- **Olvidar dimensiones** → perder capacidad de segmentar y detectar patrones.  
- **Dividir por cero en ratios** → generar valores nulos o errores; validar denominadores.  

## Estado actual
- **Fundamentos estables**: definición de KPI, uso de dimensiones y cálculo de ratios con SQL estándar.  
- **Práctica moderna**: pipelines de métricas en tiempo real con herramientas como dbt + Snowflake, métricas almacenadas en *data vault* para auditoría, y visualización automática mediante plataformas de BI que consumen modelos de métricas predefinidos.  

## Conexiones
- **Data Visualization**: las métricas alimentan gráficos y dashboards que hacen comprensible el rendimiento.  
- **BI & Reporting**: los KPI son los bloques centrales de los informes corporativos y de auto‑servicio.  
- **Product Metrics**: los ratios de uso (p. ej. “retención 30‑días”) son métricas analíticas aplicadas al ciclo de vida del producto.  

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de modelado dimensional (hechos y dimensiones).  
2. **Fundamentos**: aprender a definir KPI y a crear métricas simples con `GROUP BY`.  
3. **Intermedio**: dominar funciones de ventana y cálculo de ratios; diseñar tablas de métricas.  
4. **Avanzado**: implementar pipelines de métricas en tiempo real (dbt, streaming), versionado de métricas y auditoría.  
5. **Especialización**: adaptar métricas a dominios específicos (marketing, producto, operaciones) y conectar con herramientas de BI.  

## Preguntas de repaso
1. ¿Qué diferencia hay entre un KPI y una métrica operativa?  
2. ¿Cómo se usan las dimensiones para segmentar un KPI?  
3. ¿Cuál es la forma segura de calcular un ratio que pueda dividir por cero?  
4. ¿Qué ventajas aporta un pipeline de métricas en tiempo real frente a un cálculo batch?  
5. ¿De qué manera una métrica de producto puede influir en un dashboard de BI?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-22-analytics-metrics written_at=2026-11-05T23:06:23.532019+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]]
- [[04 - Database & Data Analytics/21 - Statistics|Statistics]]
- [[04 - Database & Data Analytics/23 - Data Visualization|Data Visualization]]
- [[04 - Database & Data Analytics/24 - BI & Reporting|BI & Reporting]]
- [[08 - UX & UI/23 - UX Metrics|UX Metrics]] · *UX / UI*
- [[09 - Product Management/17 - Product Metrics|Product Metrics]] · *Product Management*
- [[10 - Project Management/24 - Project Metrics|Project Metrics]] · *Project Management*

---
← [[04 - Database & Data Analytics/21 - Statistics|Statistics]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/23 - Data Visualization|Data Visualization]] →
