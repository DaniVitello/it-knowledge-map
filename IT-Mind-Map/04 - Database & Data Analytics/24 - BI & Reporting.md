---
title: "BI & Reporting"
area: "Database / Data Analytics"
numero: 24
aliases: ["BI & Reporting"]
tags: [concepto, it/database-data-analytics]
---
# BI & Reporting

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 24 de 25**

## Qué abarca
- Dashboards
- reports
- self-service analytics

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo BI & Reporting para transformar datos brutos en información accionable que pueda ser consumida rápidamente por tomadores de decisiones. Resuelvo el problema de que los analistas y gerentes necesitan una visión consolidada y actualizada del desempeño del negocio sin escribir consultas complejas cada vez. En mi día a día como ingeniero de datos, diseño los pipelines que alimentan dashboards y reportes, garantizo la consistencia de los indicadores y habilito el acceso self‑service a los usuarios. Después de entender BI & Reporting puedo crear cuadros de mando interactivos, automatizar la generación de informes periódicos y medir el impacto de cambios en los procesos de datos. Cuando el consumo de datos es puntual y no requiere visualización continua, puedo prescindir de una capa de BI y trabajar directamente con consultas ad‑hoc.

## Esqueleto (el 20% esencial)
1. **Dashboards** – paneles visuales que consolidan métricas clave en tiempo real.  
2. **Reports** – documentos estructurados (tablas, PDFs) que resumen resultados periódicos.  
3. **Self‑service analytics** – capacidad de que usuarios finales construyan sus propias consultas y visualizaciones sin intervención del equipo de datos.  
4. **Data refresh** – procesos automáticos que actualizan los datos subyacentes para mantener la información vigente.  
5. **Metric governance** – definición y control de los indicadores que aparecen en los dashboards y reports.

## Como funciona
1. **Modelado**: se definen las tablas de hechos y dimensiones que soportarán los indicadores.  
2. **ETL/ELT**: los pipelines cargan datos limpios en un data warehouse o lake, aplicando transformaciones necesarias para los KPIs.  
3. **Definición de métricas**: se crean vistas o tablas de métricas con lógica de negocio (ej. ventas netas, churn).  
4. **Construcción del dashboard/report**: herramientas de BI consumen esas métricas y generan visualizaciones interactivas o documentos estáticos.  
5. **Programación de refresco**: se agenda la actualización de los datasets (incremental o completa) para que la capa de presentación siempre muestre datos actuales.  
6. **Self‑service**: los usuarios acceden a catálogos de métricas y, mediante filtros o consultas simples, crean sus propios análisis.

## Detalles
- **Básico**: conectar una fuente (SQL, CSV) a una herramienta de BI, crear una vista simple y arrastrar‑soltar a un gráfico.  
- **Intermedio**: diseñar esquemas estrella, aplicar modelado de métricas con lógica de negocio, configurar refrescos incrementales y establecer roles de acceso.  
- **Avanzado**: implementar métricas calculadas en tiempo real con streaming, usar modelado de datos semánticos (tablas de métricas reutilizables), integrar control de versiones de dashboards y aplicar pruebas de regresión de métricas.

## Ejemplo minimo
```sql
-- Vista que alimenta un KPI de ventas diarias
CREATE OR REPLACE VIEW vw_daily_sales AS
SELECT
    DATE(order_timestamp) AS sales_date,
    SUM(total_amount) AS revenue,
    COUNT(*)           AS orders_cnt
FROM orders
WHERE order_status = 'completed'
GROUP BY DATE(order_timestamp);
```
En una herramienta de BI, esta vista se arrastra a un gráfico de líneas para crear un dashboard de ventas diarias.

## Errores comunes
- **Métricas inconsistentes**: usar distintas definiciones de un mismo KPI en varios dashboards; evitarlo documentando y versionando las métricas.  
- **Refresh insuficiente**: programar actualizaciones poco frecuentes y presentar datos obsoletos; definir una frecuencia acorde al SLA del negocio.  
- **Sobrecarga de visualizaciones**: incluir demasiados gráficos en un dashboard, lo que dificulta la interpretación; priorizar los indicadores críticos y aplicar jerarquía visual.

## Estado actual
- **Fundamentos estables**: modelado dimensional, ETL/ELT programado, definición de KPIs y uso de herramientas de BI consolidadas (Power BI, Tableau, Looker).  
- **Práctica moderna**: adopción de data warehouses en la nube (Snowflake, BigQuery), pipelines de datos en tiempo real (Kafka, dbt), y plataformas de self‑service con catálogos de métricas semánticas.

## Conexiones
- **Data Analysis**: BI convierte los resultados de análisis exploratorios en informes estructurados que pueden ser distribuidos a gran escala.  
- **Data Visualization**: los dashboards son la manifestación visual de los datos, usando principios de visual hierarchy para guiar la interpretación.  
- **Analytics Metrics**: los indicadores que aparecen en los reports provienen de métricas calculadas y gobernadas dentro del modelo de datos.

## Ruta de estudio
1. **Prerequisitos**: SQL avanzado, conceptos de modelado dimensional y fundamentos de ETL.  
2. **Fundamentos**: crear vistas de métricas, conectar fuentes a una herramienta de BI y diseñar dashboards simples.  
3. **Intermedio**: implementar control de versiones de métricas con dbt, programar refrescos incrementales y gestionar permisos de acceso.  
4. **Avanzado**: explorar streaming de datos para métricas en tiempo real, usar catálogos de métricas semánticas y aplicar pruebas automatizadas de dashboards.  
5. **Especialización**: profundizar en una herramienta específica (ej. Power BI Service, Looker) y en arquitectura de data mesh para BI distribuido.

## Preguntas de repaso
1. ¿Cómo se relaciona la definición de una métrica con la consistencia de los dashboards?  
2. ¿Qué pasos siguen los datos desde la extracción hasta aparecer en un reporte de BI?  
3. ¿Por qué es importante programar un refresh adecuado y cómo se determina la frecuencia?  
4. ¿Cuál es la diferencia entre un dashboard y un report en términos de consumo y actualización?  
5. ¿Qué ventajas aporta el self‑service analytics a los usuarios finales y qué riesgos implica?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-24-bi-reporting written_at=2026-11-05T23:07:52.052994+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]]
- [[04 - Database & Data Analytics/21 - Statistics|Statistics]]
- [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]]
- [[04 - Database & Data Analytics/23 - Data Visualization|Data Visualization]]
- [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]] · *UX / UI*

---
← [[04 - Database & Data Analytics/23 - Data Visualization|Data Visualization]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/25 - Advanced Data Architecture|Advanced Data Architecture]] →
