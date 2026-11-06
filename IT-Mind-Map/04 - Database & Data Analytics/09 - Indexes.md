---
title: "Indexes"
area: "Database / Data Analytics"
numero: 9
aliases: ["Indexes"]
tags: [concepto, it/database-data-analytics]
---
# Indexes

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 9 de 25**

## Qué abarca
- Búsqueda eficiente
- B-trees
- índices compuestos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo índices para acelerar la búsqueda y filtrado de filas en tablas grandes, evitando escaneos completos que consumen tiempo y recursos. Resuelvo el problema de consultas lentas cuando debo localizar registros por valores de columnas clave, como fechas, IDs o combinaciones de campos. En mi día a día como ingeniero de datos, los índices aparecen al diseñar esquemas de data warehouses, al optimizar pipelines ETL y al crear dashboards interactivos que dependen de respuestas rápidas. Después de entender cómo funcionan, puedo decidir qué columnas indexar, elegir el tipo de estructura (B‑tree, hash, etc.) y balancear el costo de mantenimiento frente al beneficio de rendimiento. No necesito preocuparme por índices cuando trabajo con datasets pequeños que caben en memoria o cuando la carga de escritura es tan alta que cualquier índice degradaría el throughput.

## Esqueleto (el 20% esencial)
1. **Búsqueda eficiente** – Un índice permite localizar filas sin leer toda la tabla.  
2. **Estructura B‑tree** – La mayoría de los índices relacionales usan árboles balanceados que mantienen orden y permiten búsquedas logarítmicas.  
3. **Índices compuestos** – Combinar varias columnas en un solo índice sirve a consultas que filtran por esas columnas en conjunto.  
4. **Costo de mantenimiento** – Cada inserción, actualización o borrado debe actualizar los índices asociados.  
5. **Selección de columnas** – Indexar columnas con alta selectividad y uso frecuente en cláusulas `WHERE`, `JOIN` o `ORDER BY`.

## Como funciona
1. Al crear un índice, el motor de base de datos construye una estructura B‑tree que almacena los valores de la(s) columna(s) clave y punteros a las filas correspondientes.  
2. Cuando se ejecuta una consulta que incluye esas columnas en `WHERE`, `JOIN` o `ORDER BY`, el optimizador decide usar el índice y recorre el árbol para encontrar rápidamente los punteros relevantes.  
3. Si el índice es compuesto, el árbol está ordenado primero por la primera columna, luego por la segunda, etc., lo que permite búsquedas que aprovechan cualquier prefijo del conjunto.  
4. Durante operaciones DML (INSERT, UPDATE, DELETE), el motor actualiza el árbol para mantener su consistencia, lo que genera un costo adicional proporcional al número y tipo de índices.  
5. El plan de ejecución final combina los accesos al índice con lecturas de datos (index‑only scan o bookmark lookup) para devolver el resultado.

## Detalles
- **Básico**: Índices simples (una sola columna) con estructura B‑tree; uso típico en claves primarias y columnas frecuentemente filtradas.  
- **Intermedio**: Índices compuestos; cobertura parcial de consultas; índices únicos que impiden duplicados.  
- **Avanzado**: Índices parciales (filtrados), índices de tipo hash (para igualdad exacta), índices columnstore (optimización de analítica), y estrategias de mantenimiento como `REINDEX` o `DROP INDEX CONCURRENTLY`.  

## Ejemplo minimo
```sql
-- Tabla de eventos
CREATE TABLE eventos (
    id   BIGINT PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    datos JSONB
);

-- Índice simple para búsquedas por fecha
CREATE INDEX idx_eventos_fecha ON eventos(fecha);

-- Consulta que usa el índice
SELECT id, tipo
FROM eventos
WHERE fecha = '2023-10-15';
```

## Errores comunes
- Indexar columnas de baja selectividad (p.ej., columnas booleanas) → evita crear índices innecesarios.  
- Crear índices compuestos en orden que no coincide con los predicados de la consulta → ordena las columnas según su uso frecuente.  
- Olvidar que cada índice añade sobrecarga en escrituras → evalúa el balance lectura/escritura antes de añadir índices.  
- No actualizar estadísticas después de cambios masivos → ejecuta `ANALYZE` para que el optimizador reconozca el nuevo costo.

## Estado actual
- **Fundamentos estables**: B‑tree como estructura predeterminada, comportamiento de índices únicos y compuestos, y el principio de costo de mantenimiento.  
- **Práctica moderna**: Uso creciente de índices parciales y de tipo columnstore en data warehouses, y de herramientas de autogestión de índices que recomiendan o eliminan índices basándose en métricas de uso.

## Conexiones
- **Database Architecture** – Los índices son un componente clave del diseño físico que complementa la normalización lógica.  
- **Query Optimizer** – Determina si un índice es útil para una consulta y genera el plan de ejecución correspondiente.  
- **Data Modeling** – La elección de claves primarias y columnas de alta cardinalidad influye directamente en qué índices crear.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de tablas y claves primarias, y comprensión de cardinalidad.  
2. **Fundamentos**: Crear y usar índices simples; interpretar planes de ejecución (`EXPLAIN`).  
3. **Intermedio**: Índices compuestos, índices únicos y parciales; evaluar selectividad.  
4. **Avanzado**: Índices columnstore, hash y estrategias de mantenimiento automático; benchmarking de rendimiento.  
5. **Especialización**: Integrar índices en pipelines ETL y en modelos de datos de data lake/warehouse.

## Preguntas de repaso
1. ¿Por qué un índice basado en B‑tree permite búsquedas logarítmicas?  
2. ¿Qué criterios utilizas para decidir si una columna debe ser indexada?  
3. ¿Cómo afecta el orden de las columnas en un índice compuesto al plan de ejecución?  
4. ¿Qué diferencia hay entre un índice simple y uno parcial?  
5. ¿Cuál es el impacto de los índices en operaciones de inserción masiva y cómo lo mitigas?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-09-indexes written_at=2026-11-05T22:54:22.964606+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/11 - Bases de datos|Bases de datos]] · *Backend*
- [[04 - Database & Data Analytics/12 - Database Architecture|Database Architecture]]

---
← [[04 - Database & Data Analytics/08 - Normalization|Normalization]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/10 - Transactions|Transactions]] →
