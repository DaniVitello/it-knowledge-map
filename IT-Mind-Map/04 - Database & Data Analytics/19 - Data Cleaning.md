---
title: "Data Cleaning"
area: "Database / Data Analytics"
numero: 19
aliases: ["Data Cleaning"]
tags: [concepto, it/database-data-analytics]
---
# Data Cleaning

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 19 de 25**

## Qué abarca
- Normalización
- transformación
- deduplicación

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el data cleaning para transformar datos crudos en información fiable que pueda alimentar modelos analíticos y consultas de negocio. Resuelvo problemas de valores faltantes, inconsistencias de formato y registros duplicados que, de otro modo, distorsionarían métricas y decisiones. En mi día a día como ingeniero de datos y analista senior, aplico estas técnicas antes de cargar datos en un data warehouse o de ejecutar dashboards de BI, garantizando que los resultados reflejen la realidad del negocio. Después de dominar el data cleaning, puedo diseñar pipelines automatizados, validar la calidad de datos y enfocarme en análisis avanzados sin preocuparme por errores de base. Sólo cuando los datos provienen de fuentes controladas y ya han sido validados previamente, el data cleaning exhaustivo no es necesario.

## Esqueleto (el 20% esencial)
1. **Normalización** – Unificar formatos y unidades para que los valores sean comparables.  
2. **Transformación** – Aplicar reglas (p. ej., parsing, casting) que convierten datos sucios en tipos adecuados.  
3. **Deduplicación** – Identificar y eliminar registros repetidos que inflarían conteos y promedios.  
4. **Manejo de valores faltantes** – Decidir entre imputación, eliminación o flagging según el impacto analítico.  
5. **Validación de reglas de negocio** – Verificar que los datos cumplan restricciones lógicas (rango, unicidad, consistencia referencial).

## Como funciona
1. **Exploración inicial**: se inspeccionan los datasets para detectar patrones de suciedad (ej. fechas en distintos formatos).  
2. **Normalización**: se aplican funciones de formato (e.g., `to_date`, `lower`) para homogeneizar columnas.  
3. **Transformación**: se convierten tipos (string → integer) y se crean columnas derivadas (p. ej., edad a partir de fecha de nacimiento).  
4. **Deduplicación**: se generan claves compuestas y se usan `GROUP BY` o `ROW_NUMBER()` para conservar solo la fila “más completa”.  
5. **Manejo de faltantes**: se elige una estrategia (media, mediana, valor constante) y se ejecuta la imputación.  
6. **Validación**: se ejecutan checks (`CHECK` constraints, pruebas de integridad) y se registran los registros que fallan para revisión.

## Detalles
- **Básico**: uso de funciones SQL (`TRIM`, `UPPER`, `CAST`) y de pandas (`fillna`, `drop_duplicates`).  
- **Intermedio**: creación de pipelines con herramientas como dbt o Apache Airflow que encadenan pasos de normalización, transformación y deduplicación.  
- **Avanzado**: aplicación de técnicas de detección de outliers (Z‑score, IQR) y de imputación multivariante (KNN, regresión) dentro de entornos de Spark o Python, integrando pruebas de calidad automatizadas (Great Expectations).

## Ejemplo minimo
```sql
-- Tabla cruda con fechas en distintos formatos y duplicados
WITH raw AS (
  SELECT 1 AS id, '2023-01-05' AS fecha UNION ALL
  SELECT 2, '05/01/2023' UNION ALL
  SELECT 2, '05/01/2023'   -- duplicado
)

-- Data cleaning: normalizar fecha, deduplicar
SELECT DISTINCT
       id,
       TO_DATE(
         CASE
           WHEN fecha LIKE '%/%' THEN TO_DATE(fecha, 'DD/MM/YYYY')
           ELSE TO_DATE(fecha, 'YYYY-MM-DD')
         END
       ) AS fecha_normalizada
FROM raw;
```

## Errores comunes
- **Eliminar duplicados sin revisar**: se pierden datos útiles; usar `ROW_NUMBER()` con criterio de prioridad.  
- **Imputar valores faltantes con la media en variables categóricas**: genera categorías inexistentes; usar una categoría “Desconocido”.  
- **Normalizar sin validar zona horaria**: produce desalineación temporal; incluir conversión explícita a UTC.

## Estado actual
- **Fundamentos estables**: normalización de tipos, deduplicación mediante claves, manejo de nulos con imputación simple.  
- **Práctica moderna**: pipelines declarativos (dbt), pruebas de calidad automatizadas (Great Expectations), imputación basada en aprendizaje automático y detección de duplicados con fuzzy matching (e.g., `recordlinkage`).

## Conexiones
- **Data Quality**: el data cleaning es la primera capa para alcanzar alta calidad, ya que corrige errores antes de medir la calidad global.  
- **Data Analysis**: datos limpios permiten análisis estadísticos y visualizaciones sin sesgos introducidos por valores erróneos.  
- **Machine Learning**: los modelos dependen de datos consistentes; el cleaning reduce ruido y mejora la precisión predictiva.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, pandas, conceptos de tipos de datos y claves primarias.  
2. **Fundamentos**: ejercicios de normalización y deduplicación en SQL y pandas.  
3. **Herramientas de pipeline**: aprender dbt o Airflow para orquestar pasos de cleaning.  
4. **Validación automática**: implementar Great Expectations o Deequ.  
5. **Imputación avanzada**: estudiar técnicas de KNN y regresión en scikit‑learn o Spark ML.  
6. **Especialización**: fuzzy matching y deduplicación a gran escala con librerías como `recordlinkage` o `dedupe`.

## Preguntas de repaso
1. ¿Qué diferencia hay entre normalizar y transformar datos en un proceso de cleaning?  
2. ¿Cómo evitarías eliminar información valiosa al deduplicar un dataset?  
3. ¿Cuál es una estrategia adecuada para imputar valores faltantes en una columna categórica?  
4. ¿Qué herramienta moderna permite definir pruebas de calidad de datos como código?  
5. ¿Por qué el data cleaning es un paso crítico antes de entrenar un modelo de machine learning?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-19-data-cleaning written_at=2026-11-05T23:03:54.011697+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/18 - Data Quality|Data Quality]]
- [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]]

---
← [[04 - Database & Data Analytics/18 - Data Quality|Data Quality]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]] →
