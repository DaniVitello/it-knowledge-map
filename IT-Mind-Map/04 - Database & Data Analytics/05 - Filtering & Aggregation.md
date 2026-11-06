---
title: "Filtering & Aggregation"
area: "Database / Data Analytics"
numero: 5
aliases: ["Filtering & Aggregation"]
tags: [concepto, it/database-data-analytics]
---
# Filtering & Aggregation

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 5 de 25**

## Qué abarca
- WHERE
- GROUP BY
- HAVING
- funciones agregadas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el filtrado y la agregación para extraer información concreta de grandes volúmenes de datos y para resumir esos datos en métricas útiles. Resuelvo el problema de identificar subconjuntos relevantes (filtrado) y de calcular indicadores como sumas, promedios o conteos (agregación) sin tener que procesar fila a fila en la capa de aplicación. En mi día a día como ingeniero de datos y analista senior, estos operadores aparecen en consultas que alimentan dashboards, validan la calidad de los datos o generan tablas de hechos para un data warehouse. Después de comprenderlos, puedo diseñar pipelines de extracción‑transformación‑carga (ETL) más eficientes y crear reportes ad‑hoc sin sobrecargar el motor de base de datos. No necesito preocuparme cuando trabajo con datos ya pre‑agregados o cuando la lógica de negocio se implementa fuera de SQL.

## Esqueleto (el 20% esencial)
1. **WHERE** filtra filas antes de cualquier operación de agregación.  
2. **GROUP BY** define los grupos sobre los que se aplicarán las funciones agregadas.  
3. **Funciones agregadas** (SUM, AVG, COUNT, MIN, MAX) calculan valores resumidos por grupo.  
4. **HAVING** filtra grupos después de la agregación, usando resultados de funciones agregadas.  

## Como funciona
1. La consulta recibe una tabla origen.  
2. **WHERE** evalúa cada fila y descarta las que no cumplen la condición.  
3. El conjunto resultante se reparte en grupos según los campos listados en **GROUP BY**.  
4. Sobre cada grupo se ejecutan las **funciones agregadas** especificadas en el SELECT.  
5. Opcionalmente, **HAVING** evalúa una condición sobre los valores agregados y elimina los grupos que no la cumplen.  
6. El motor devuelve una tabla con una fila por grupo y las columnas solicitadas.

## Detalles
- **Básico**: uso de `WHERE` y una única función agregada (`COUNT(*)`) para obtener el número de registros que cumplen una condición.  
- **Intermedio**: combinación de varios campos en `GROUP BY` y uso simultáneo de varias funciones (`SUM`, `AVG`). Introducción de `HAVING` para filtrar por, por ejemplo, grupos con ventas > 10 000.  
- **Avanzado**: agregaciones anidadas mediante sub‑consultas o CTEs, uso de funciones de ventana (`OVER`) para cálculos acumulados que complementan `GROUP BY`, y aplicación de índices parciales que optimizan el filtrado previo.

## Ejemplo minimo
```sql
-- Ventas por producto que superen los 5 pedidos
SELECT product_id,
       COUNT(*)        AS pedidos,
       SUM(amount)     AS total_ventas
FROM   sales
WHERE  sale_date >= '2024-01-01'
GROUP BY product_id
HAVING COUNT(*) > 5;
```

## Errores comunes
- Colocar la condición de filtrado de grupos en `WHERE` en lugar de `HAVING`; evitarlo usando `HAVING` solo para expresiones que involucren funciones agregadas.  
- Olvidar incluir en `GROUP BY` todas las columnas no agregadas del `SELECT`; corregir añadiendo esas columnas al `GROUP BY`.  
- Asumir que `HAVING` se ejecuta antes que `WHERE`; recordar que el orden es primero `WHERE`, luego `GROUP BY`, luego `HAVING`.

## Estado actual
- **Fundamentos estables**: la sintaxis `WHERE … GROUP BY … HAVING …` y las funciones agregadas estándar (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) son parte del ANSI SQL desde hace décadas y se mantienen sin cambios.  
- **Práctica moderna**: los motores actuales (PostgreSQL, Snowflake, BigQuery) añaden extensiones como `GROUPING SETS`, `ROLLUP` y `CUBE` para agregaciones multidimensionales, y permiten combinar `HAVING` con expresiones de ventana para filtros más expresivos. El uso de índices parciales y de columnas materializadas mejora significativamente el rendimiento del filtrado previo.

## Conexiones
- **SQL**: el lenguaje que implementa `WHERE`, `GROUP BY` y `HAVING`; sin él no podríamos expresar filtrado y agregación declarativamente.  
- **JOINs**: a menudo se combinan con agregaciones para resumir datos provenientes de varias tablas antes de aplicar `GROUP BY`.  
- **Data Warehousing**: las agregaciones son la base de las tablas de hechos y de los cubos OLAP que alimentan los informes de negocio.

## Ruta de estudio
1. **Prerequisitos**: comprender tipos de datos, operadores lógicos y la estructura básica de una tabla.  
2. **Fundamentos**: practicar `SELECT … WHERE …`, luego añadir `GROUP BY` y una función agregada simple.  
3. **Profundización**: introducir `HAVING`, usar múltiples funciones agregadas y combinar con `JOINs`.  
4. **Avanzado**: explorar `GROUPING SETS`, `ROLLUP`, `CUBE` y funciones de ventana; optimizar consultas con índices y columnas materializadas.  
5. **Aplicación**: diseñar un pipeline ETL que genere tablas de hechos usando agregaciones y validar su rendimiento en un data warehouse.

## Preguntas de repaso
1. ¿Qué diferencia hay entre la cláusula `WHERE` y la cláusula `HAVING` en una consulta con agregación?  
2. ¿Cómo afecta el orden de ejecución (`WHERE` → `GROUP BY` → `HAVING`) al resultado final?  
3. ¿Cuál es el efecto de omitir una columna no agregada del `GROUP BY` en la lista `SELECT`?  
4. ¿En qué situaciones usarías `GROUPING SETS` en lugar de un simple `GROUP BY`?  
5. ¿Cómo podrías mejorar el rendimiento de una consulta que filtra millones de filas antes de agrupar?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-05-filtering-aggregation written_at=2026-11-05T22:50:01.125223+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/12 - SQL|SQL]] · *Backend*
- [[04 - Database & Data Analytics/04 - SQL|SQL]]
- [[04 - Database & Data Analytics/06 - JOINs|JOINs]]

---
← [[04 - Database & Data Analytics/04 - SQL|SQL]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/06 - JOINs|JOINs]] →
