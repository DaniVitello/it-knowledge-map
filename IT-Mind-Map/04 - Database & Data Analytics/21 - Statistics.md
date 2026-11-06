---
title: "Statistics"
area: "Database / Data Analytics"
numero: 21
aliases: ["Statistics"]
tags: [concepto, it/database-data-analytics]
---
# Statistics

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 21 de 25**

## Qué abarca
- Media
- mediana
- distribución
- varianza
- probabilidad

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la estadística para transformar valores crudos en información accionable que guía decisiones de modelado, optimización de consultas y generación de métricas de negocio. Resuelvo problemas como identificar valores atípicos, comparar distribuciones de rendimiento entre tablas o validar hipótesis antes de invertir en pipelines de datos. En mi día a día como ingeniero de datos y analista senior, la estadística aparece al diseñar esquemas de partición, al crear alertas basadas en desviaciones estándar y al producir dashboards que resumen tendencias históricas. Después de dominarla, puedo diseñar experimentos A/B, calibrar modelos de machine learning y comunicar hallazgos con confianza. Cuando los datos son simplemente descriptivos y no requieren inferencia ni control de calidad, no es necesario profundizar en estadística.

## Esqueleto (el 20% esencial)
1. **Media** – valor promedio que resume la tendencia central de un conjunto de registros.  
2. **Mediana** – punto medio que protege contra valores atípicos y muestra la posición central real.  
3. **Distribución** – forma en que los valores se reparten; esencial para detectar sesgos y seleccionar pruebas estadísticas.  
4. **Varianza y desviación estándar** – medida de dispersión que indica cuán dispersos están los datos respecto a la media.  
5. **Probabilidad** – base para estimar la ocurrencia de eventos futuros y validar hipótesis en análisis de datos.

## Como funciona
1. **Recolección**: extraigo la columna de interés mediante una consulta (`SELECT columna FROM tabla`).  
2. **Cálculo de la media**: sumo todos los valores y los divido por el conteo (`AVG(columna)`).  
3. **Cálculo de la mediana**: ordeno los valores y tomo el elemento central (`PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY columna)`).  
4. **Evaluación de la distribución**: genero histogramas o calculo percentiles para observar la forma (p.ej., `WIDTH_BUCKET`).  
5. **Cálculo de varianza y desviación estándar**: uso funciones `VAR_SAMP` y `STDDEV_SAMP` para cuantificar la dispersión.  
6. **Aplicación de probabilidad**: con la media y la desviación estándar, aplico la regla empírica (68‑95‑99.7) o calculo p‑values en pruebas de hipótesis.

## Detalles
- **Básico**: media, mediana y conteo (`COUNT`) son suficientes para reportes rápidos y detección de outliers simples.  
- **Intermedio**: varianza y desviación estándar permiten definir umbrales dinámicos (p.ej., alertas cuando `valor > media + 3*desv`).  
- **Avanzado**: modelado de distribuciones (normal, log‑normal) y cálculo de probabilidades condicionadas para experimentos A/B y predicciones de carga futura.

## Ejemplo minimo
```sql
-- Tabla de ejemplo: ventas(id, monto)
SELECT
    AVG(monto)                              AS media,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monto) AS mediana,
    VAR_SAMP(monto)                         AS varianza,
    STDDEV_SAMP(monto)                      AS desviacion_estandar
FROM ventas;
```

## Errores comunes
- **Confundir varianza poblacional con muestral**: usar `VAR_POP` cuando la muestra es pequeña genera sesgo; elegir la función adecuada según el contexto.  
- **Aplicar media a datos altamente sesgados**: la media se ve arrastrada por outliers; prefiera la mediana o percentiles.  
- **Ignorar la distribución subyacente**: asumir normalidad sin verificar puede invalidar pruebas de hipótesis; siempre inspeccione histogramas o pruebas de bondad de ajuste.

## Estado actual
- **Fundamentos estables**: cálculo de media, mediana, varianza y desviación estándar está soportado por todos los sistemas SQL modernos y es considerado fiable.  
- **Práctica moderna**: integración de funciones analíticas (`PERCENTILE_CONT`, `APPROX_PERCENTILE`) y uso de extensiones de estadística (p.ej., `MAD` para desviación absoluta mediana) para análisis a gran escala; adopción de notebooks y pipelines de datos que combinan SQL con Python/R para visualizaciones y pruebas de hipótesis más complejas.

## Conexiones
- **Data Analysis**: la estadística provee los indicadores numéricos que alimentan los procesos de exploración y limpieza de datos.  
- **Data Visualization**: medias, desviaciones y distribuciones se representan en gráficos de barras, box‑plots y curvas de densidad para comunicar hallazgos.  
- **Machine Learning Fundamentals**: la estimación de parámetros (media, varianza) es la base para algoritmos supervisados como regresión lineal y para la normalización de features.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de tipos de datos numéricos y manejo de tablas.  
2. **Fundamentos**: practicar funciones de agregación (`AVG`, `COUNT`, `VAR_SAMP`) y percentiles en entornos de bases de datos.  
3. **Intermedio**: estudiar histogramas, box‑plots y la regla empírica; implementar alertas basadas en desviaciones estándar.  
4. **Avanzado**: aprender pruebas de hipótesis (t‑test, chi‑cuadrado) y modelado de distribuciones con extensiones SQL o lenguajes como Python (pandas, scipy).  
5. **Especialización**: combinar estadística con pipelines de ETL y notebooks para experimentos A/B y entrenamiento de modelos ML.

## Preguntas de repaso
1. ¿Cómo se calcula la mediana en SQL y por qué es más robusta que la media frente a outliers?  
2. ¿Qué información aporta la desviación estándar al definir umbrales de calidad de datos?  
3. ¿En qué situaciones es preferible usar `APPROX_PERCENTILE` en lugar de `PERCENTILE_CONT`?  
4. ¿Cómo afecta la suposición de normalidad a la interpretación de p‑values en pruebas de hipótesis?  
5. ¿De qué manera la estadística se conecta con la visualización de datos para detectar sesgos en un dataset?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-21-statistics written_at=2026-11-05T23:05:49.079820+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]]
- [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]]
- [[04 - Database & Data Analytics/23 - Data Visualization|Data Visualization]]
- [[04 - Database & Data Analytics/24 - BI & Reporting|BI & Reporting]]
- [[07 - AI Engineering/01 - AI - ML Fundamentals|AI / ML Fundamentals]] · *AI Engineering*
- [[07 - AI Engineering/04 - Machine Learning Fundamentals|Machine Learning Fundamentals]] · *AI Engineering*

---
← [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]] →
