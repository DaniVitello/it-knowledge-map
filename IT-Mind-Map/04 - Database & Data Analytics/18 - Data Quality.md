---
title: "Data Quality"
area: "Database / Data Analytics"
numero: 18
aliases: ["Data Quality"]
tags: [concepto, it/database-data-analytics]
---
# Data Quality

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 18 de 25**

## Qué abarca
- Missing data
- duplicados
- inconsistencias
- validación

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la **Data Quality** para asegurar que los datos que consumo o entrego en mis pipelines sean fiables y útiles. Resuelvo problemas de valores ausentes, filas duplicadas, inconsistencias de formato y violaciones de reglas de negocio que, de otro modo, producirían análisis erróneos o decisiones basadas en información corrupta. En mi día a día como ingeniero de datos y analista senior, la calidad de los datos es la base para modelar esquemas, escribir consultas eficientes y generar dashboards confiables. Cuando entiendo cómo medir y mejorar la calidad, puedo diseñar procesos de ingestión automáticos, definir métricas de calidad y priorizar esfuerzos de limpieza. No necesito preocuparme de la Data Quality cuando trabajo con datos de prueba internos que no impactan decisiones productivas.

## Esqueleto (el 20% esencial)
1. **Missing data** – Identificar y decidir cómo tratar valores nulos o ausentes según el contexto del negocio.  
2. **Duplicados** – Detectar filas repetidas que inflan métricas y distorsionan agregaciones.  
3. **Inconsistencias** – Uniformizar formatos, unidades y codificaciones para evitar comparaciones inválidas.  
4. **Validación** – Aplicar reglas de integridad (unicidad, rangos, referencias) que garantizan que los datos cumplan con los requisitos del dominio.  

## Como funciona
1. **Perfilado**: se escanean tablas o streams para cuantificar ausentes, duplicados e inconsistencias.  
2. **Definición de reglas**: se establecen criterios de validación (p. ej., `NOT NULL`, rangos aceptables, claves únicas).  
3. **Detección**: mediante consultas o herramientas de profiling se marcan los registros que violan las reglas.  
4. **Corrección**: se aplican estrategias – imputación, eliminación de duplicados o normalización – según la gravedad y el coste.  
5. **Monitoreo continuo**: se programan métricas de calidad (porcentaje de nulos, tasa de duplicados) en dashboards de Data Ops.

## Detalles
- **Básico**: usar `COUNT(*)`, `COUNT(column)` y `DISTINCT` para cuantificar nulos y duplicados.  
- **Intermedio**: crear constraints (`UNIQUE`, `CHECK`) y vistas de calidad que expongan filas problemáticas.  
- **Avanzado**: integrar pruebas de calidad en CI/CD con frameworks como Great Expectations o Deequ, y automatizar alertas cuando las métricas superen umbrales definidos.

## Ejemplo minimo
```sql
-- Detectar filas con valores nulos críticos y duplicados en la tabla ventas
WITH nulled AS (
    SELECT *
    FROM ventas
    WHERE cliente_id IS NULL OR monto IS NULL
),
dup AS (
    SELECT cliente_id, fecha, monto, COUNT(*) AS cnt
    FROM ventas
    GROUP BY cliente_id, fecha, monto
    HAVING COUNT(*) > 1
)
SELECT 'Nulos' AS tipo, * FROM nulled
UNION ALL
SELECT 'Duplicado' AS tipo, cliente_id, fecha, monto FROM dup;
```

## Errores comunes
- **Eliminar todos los nulos sin analizar** – puede perder información valiosa; evaluar imputación primero.  
- **Usar `DISTINCT` como solución definitiva a duplicados** – solo oculta el problema sin corregir la fuente.  
- **Definir reglas de validación demasiado estrictas** – genera falsos positivos y retrasa pipelines; calibrar umbrales con datos reales.  

## Estado actual
- **Fundamentos estables**: perfilado con `COUNT`, constraints de integridad y procesos manuales de limpieza siguen siendo la base.  
- **Práctica moderna**: adopción de frameworks de pruebas de calidad de datos (Great Expectations, Deequ), integración con pipelines de orquestación (Airflow, Dagster) y métricas de calidad en observabilidad (DataDog, Monte Carlo).  

## Conexiones
- **Data Cleaning**: la calidad de datos define qué registros deben limpiarse y cómo priorizar esas tareas.  
- **Data Governance**: establece políticas y roles que garantizan la aplicación consistente de reglas de calidad.  
- **Machine Learning**: modelos entrenados con datos de alta calidad reducen sesgos y mejoran la precisión predictiva.  

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de modelado relacional y manejo de tipos de datos.  
2. **Fundamentos**: aprender a perfilar datos (profiling) y a crear constraints en bases relacionales.  
3. **Herramientas**: explorar Great Expectations o Deequ para pruebas automatizadas.  
4. **Operacionalización**: integrar métricas de calidad en pipelines de Airflow y configurar alertas.  
5. **Especialización**: profundizar en técnicas de imputación avanzada y en gobernanza de datos con herramientas como Collibra.  

## Preguntas de repaso
1. ¿Qué criterios utilizo para decidir si imputo o elimino valores nulos?  
2. ¿Cómo detecto duplicados que aparecen en distintas columnas de clave compuesta?  
3. ¿Cuál es la diferencia entre una regla de `CHECK` y una política de Data Governance?  
4. ¿Qué ventaja aporta un framework como Great Expectations frente a consultas SQL manuales?  
5. ¿En qué situaciones la calidad de datos deja de ser una prioridad para un proyecto?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-18-data-quality written_at=2026-11-05T23:03:09.432427+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/19 - Data Cleaning|Data Cleaning]]
- [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]]

---
← [[04 - Database & Data Analytics/17 - Data Pipelines|Data Pipelines]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/19 - Data Cleaning|Data Cleaning]] →
