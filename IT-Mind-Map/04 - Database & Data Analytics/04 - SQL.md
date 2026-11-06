---
title: "SQL"
area: "Database / Data Analytics"
numero: 4
aliases: ["SQL"]
tags: [concepto, it/database-data-analytics]
---
# SQL

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 4 de 25**

## Qué abarca
- SELECT
- INSERT
- UPDATE
- DELETE
- queries

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo SQL para expresar de forma declarativa qué datos necesito y cómo modificarlos dentro de una base de datos relacional. Resuelvo el problema de extraer, insertar, actualizar o eliminar información sin escribir código procedural, lo que permite que los pipelines de ingestión, los dashboards analíticos y los procesos de limpieza de datos se construyan de manera reproducible y escalable. En mi día a día como ingeniero de datos y analista senior, SQL es la herramienta que me permite validar modelos, generar métricas de negocio y alimentar modelos de machine‑learning con datos consistentes. Después de dominarlo, puedo diseñar consultas complejas, optimizarlas y combinarlas con herramientas de orquestación; solo cuando trabajo con bases NoSQL o sistemas de streaming no necesito preocuparme por SQL.

## Esqueleto (el 20% esencial)
1. **SELECT** – especifica columnas y filas que quiero leer.  
2. **INSERT** – agrega nuevas filas a una tabla.  
3. **UPDATE** – modifica valores existentes bajo condiciones.  
4. **DELETE** – elimina filas que cumplen un criterio.  
5. **Queries** – combinación de las operaciones anteriores con cláusulas como `WHERE`, `GROUP BY` y `ORDER BY`.

## Como funciona
1. El motor recibe la sentencia SQL y la parsea.  
2. El optimizador traduce la consulta a un plan de ejecución basado en estadísticas de la tabla.  
3. El plan se ejecuta: para `SELECT` se leen filas, para `INSERT/UPDATE/DELETE` se modifican bloques de datos.  
4. Los resultados (filas o número de filas afectadas) se devuelven al cliente.  
5. Si la consulta incluye `WHERE` o `GROUP BY`, el motor filtra y agrupa antes de producir la salida final.

## Detalles
- **Básico**: `SELECT` con `WHERE` permite filtrar registros; `INSERT` agrega una fila simple.  
- **Intermedio**: `UPDATE` y `DELETE` usan condiciones complejas; `GROUP BY` y funciones de agregación generan métricas resumidas.  
- **Avanzado**: sub‑consultas, CTE (`WITH`), y transacciones garantizan consistencia en operaciones múltiples; el uso de índices y estadísticas mejora el plan de ejecución.

## Ejemplo minimo
```sql
-- Crear tabla de ejemplo
CREATE TABLE ventas (
    id INT PRIMARY KEY,
    producto VARCHAR(50),
    cantidad INT,
    fecha DATE
);

-- Insertar una fila
INSERT INTO ventas (id, producto, cantidad, fecha)
VALUES (1, 'Camisa', 3, '2024-10-01');

-- Consultar la fila insertada
SELECT id, producto, cantidad
FROM ventas
WHERE id = 1;
```

## Errores comunes
- Olvidar la cláusula `WHERE` en `UPDATE` o `DELETE`, lo que afecta a todas las filas; revisa siempre la condición antes de ejecutar.  
- No especificar columnas en `INSERT` y confiar en el orden de la tabla; declara explícitamente los nombres de columna.  
- Usar `SELECT *` en producción, generando transferencia innecesaria de datos; selecciona solo las columnas requeridas.

## Estado actual
- **Fundamentos estables**: la sintaxis básica de `SELECT`, `INSERT`, `UPDATE`, `DELETE` y las cláusulas `WHERE`, `GROUP BY`, `ORDER BY` están definidas por el estándar SQL y son compatibles con la mayoría de los RDBMS.  
- **Práctica moderna**: el uso de CTE, ventanas (`OVER`), y funciones JSON está extendido en sistemas como PostgreSQL, Snowflake y BigQuery; además, la integración de SQL con motores de procesamiento distribuido (e.g., Spark SQL, Presto) permite consultas a petabytes de datos.

## Conexiones
- **Filtering & Aggregation**: las cláusulas `WHERE` y `GROUP BY` de SQL son la base para filtrar filas y calcular agregados, facilitando análisis de métricas.  
- **JOINs**: combinan datos de múltiples tablas dentro de una sola consulta, esencial para modelar relaciones entre entidades.  
- **Data Modeling**: el diseño de esquemas relacionales determina cómo se estructuran las sentencias `SELECT` y `INSERT`, impactando la eficiencia de las consultas.

## Ruta de estudio
1. **Prerequisitos**: conceptos de tablas, tipos de datos y claves primarias.  
2. **Fundamentos**: practicar `SELECT`, `INSERT`, `UPDATE`, `DELETE` con filtros simples.  
3. **Intermedio**: aprender `GROUP BY`, funciones de agregación y sub‑consultas.  
4. **Avanzado**: dominar CTE, ventanas, manejo de transacciones y optimización con índices.  
5. **Especialización**: explorar SQL en entornos distribuidos (Spark SQL, BigQuery) y extensiones JSON/XML.

## Preguntas de repaso
1. ¿Cómo evito que un `UPDATE` modifique todas las filas de una tabla?  
2. ¿Qué diferencia hay entre `WHERE` y `HAVING` en una consulta que usa `GROUP BY`?  
3. ¿Cuál es la ventaja de declarar explícitamente las columnas en un `INSERT`?  
4. ¿En qué casos una sub‑consulta en la cláusula `FROM` (derived table) es más útil que un `JOIN`?  
5. ¿Qué papel juegan los índices al ejecutar una sentencia `SELECT` con filtro?

<!-- trazabilidad: run_id=run-20261105-151808-34f931 concept=04-database-data-analytics-04-sql written_at=2026-11-05T18:20:29.346355+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/12 - SQL|SQL]] · *Backend*
- [[04 - Database & Data Analytics/05 - Filtering & Aggregation|Filtering & Aggregation]]
- [[04 - Database & Data Analytics/06 - JOINs|JOINs]]

---
← [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/05 - Filtering & Aggregation|Filtering & Aggregation]] →
