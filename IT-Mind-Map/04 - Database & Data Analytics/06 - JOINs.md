---
title: "JOINs"
area: "Database / Data Analytics"
numero: 6
aliases: ["JOINs"]
tags: [concepto, it/database-data-analytics]
---
# JOINs

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 6 de 25**

## Qué abarca
- INNER
- LEFT
- RIGHT
- relaciones entre tablas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los JOINs para combinar filas de dos o más tablas en una sola vista lógica, de modo que pueda analizar relaciones entre entidades como clientes y sus órdenes. Resuelvo el problema de datos fragmentados, donde la información necesaria está distribuida en distintas tablas con claves comunes. En mi día a día como ingeniero de datos y analista senior, los JOINs aparecen cada vez que construyo modelos dimensionales, preparo datasets para dashboards o escribo consultas que alimentan pipelines ETL. Después de entenderlos, puedo diseñar esquemas más eficientes, evitar lecturas redundantes y aplicar agregaciones correctas. No necesito preocuparme por ellos cuando trabajo con fuentes de datos ya denormalizadas o cuando utilizo herramientas de visualización que hacen el merge internamente.

## Esqueleto (el 20% esencial)
1. **INNER JOIN**: devuelve solo las filas con coincidencias en ambas tablas.  
2. **LEFT (OUTER) JOIN**: conserva todas las filas de la tabla izquierda y agrega datos de la derecha cuando existen coincidencias.  
3. **RIGHT (OUTER) JOIN**: conserva todas las filas de la tabla derecha y agrega datos de la izquierda cuando existen coincidencias.  
4. **Cláusula ON**: define la condición de emparejamiento basada en columnas clave.  
5. **Orden de evaluación**: los JOINs se procesan de izquierda a derecha, influyendo en planes de ejecución y uso de índices.

## Como funciona
1. El motor de base de datos identifica la **cláusula ON** y crea un conjunto de pares de filas que cumplen la condición.  
2. Según el tipo de JOIN, filtra ese conjunto:  
   - *INNER* mantiene solo los pares coincidentes.  
   - *LEFT* añade pares donde la tabla izquierda tiene fila pero la derecha no, rellenando con NULL.  
   - *RIGHT* hace lo inverso.  
3. El resultado parcial se combina con la siguiente tabla del FROM, repitiendo el proceso.  
4. Finalmente, el motor aplica **SELECT**, **WHERE**, **GROUP BY** y demás cláusulas sobre el conjunto unido.

## Detalles
- **Básico**: uso de INNER y LEFT con claves primarias‑foráneas; aprovechamiento de índices para acelerar la búsqueda de coincidencias.  
- **Intermedio**: JOINs múltiples, uso de alias para claridad, y control de cardinalidad con `DISTINCT` o subconsultas.  
- **Avanzado**: estrategias de *join reordering*, *hash join* vs *nested loop*, y particionamiento de datos para reducir shuffles en entornos distribuidos (e.g., Spark SQL).  

## Ejemplo minimo
```sql
-- Tablas de ejemplo
CREATE TABLE clientes(id INT PRIMARY KEY, nombre VARCHAR(50));
CREATE TABLE ordenes(id INT PRIMARY KEY, cliente_id INT, total DECIMAL);

-- INNER JOIN: solo clientes con órdenes
SELECT c.id, c.nombre, o.total
FROM clientes c
INNER JOIN ordenes o ON c.id = o.cliente_id;
```

## Errores comunes
- Olvidar la cláusula **ON** y usar **WHERE** para filtrar, lo que convierte un INNER en un CROSS JOIN inesperado.  
- Usar LEFT cuando se necesita INNER, generando filas con NULL que distorsionan agregados.  
- No indexar las columnas de unión, provocando escaneos completos y bajo rendimiento.  

## Estado actual
Los conceptos de INNER, LEFT y RIGHT JOIN son fundamentos estables y están soportados por todos los sistemas SQL. En la práctica moderna, los motores optimizan automáticamente el orden y el algoritmo de unión (hash, merge, nested‑loop) y ofrecen extensiones como **FULL OUTER JOIN** y **CROSS APPLY** en entornos específicos.

## Conexiones
- **SQL**: el lenguaje que define la sintaxis y los operadores de JOIN.  
- **Filtering & Aggregation**: después de unir tablas, se aplican filtros (`WHERE`) y agregaciones (`GROUP BY`) sobre el conjunto resultante.  
- **Data Modeling**: la elección de claves y la normalización determinan cuántos y qué tipo de JOINs serán necesarios en los análisis.

## Ruta de estudio
1. Prerrequisitos: comprender claves primarias/foráneas y la sintaxis básica de SELECT.  
2. Practicar INNER y LEFT JOIN con datasets pequeños en una base de datos local.  
3. Explorar planes de ejecución (`EXPLAIN`) para observar cómo el motor elige algoritmos de unión.  
4. Avanzar a JOINs múltiples y a optimizaciones de índices.  
5. Profundizar en técnicas de rendimiento en entornos distribuidos (Spark, Presto) y en JOINs especiales como FULL OUTER y SEMI JOIN.

## Preguntas de repaso
1. ¿Qué diferencia hay entre un INNER JOIN y un LEFT JOIN en el conjunto de filas resultante?  
2. ¿Cómo afecta la ausencia de índices en las columnas usadas en la cláusula ON al rendimiento de un JOIN?  
3. ¿Cuál es el orden de evaluación de varios JOINs en una misma consulta y por qué importa?  
4. ¿En qué casos preferirías usar un FULL OUTER JOIN frente a combinar LEFT y RIGHT JOIN por separado?  
5. ¿Cómo puedes verificar qué algoritmo de unión está utilizando tu motor de base de datos?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-06-joins written_at=2026-11-05T22:51:17.710792+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/12 - SQL|SQL]] · *Backend*
- [[04 - Database & Data Analytics/04 - SQL|SQL]]
- [[04 - Database & Data Analytics/05 - Filtering & Aggregation|Filtering & Aggregation]]

---
← [[04 - Database & Data Analytics/05 - Filtering & Aggregation|Filtering & Aggregation]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/07 - Keys & Constraints|Keys & Constraints]] →
