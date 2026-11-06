---
title: "Transactions"
area: "Database / Data Analytics"
numero: 10
aliases: ["Transactions"]
tags: [concepto, it/database-data-analytics]
---
# Transactions

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 10 de 25**

## Qué abarca
- Commit
- rollback
- atomicidad

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo las transacciones para garantizar que un conjunto de operaciones sobre la base de datos se ejecuten como una unidad indivisible. Resuelvo problemas de inconsistencia cuando una serie de cambios depende mutuamente: si alguna operación falla, revierto todo el bloque y mantengo los datos en un estado coherente. En mi día a día como ingeniero de datos, las transacciones aparecen al cargar lotes, actualizar tablas de hechos o al aplicar correcciones de calidad; me permiten asegurar que los indicadores analíticos no se vean contaminados por datos parciales. Después de comprenderlas, puedo diseñar pipelines robustos, definir puntos de control y optimizar el rendimiento mediante aislamiento adecuado. No necesito preocuparme por transacciones cuando trabajo con datos inmutables o lecturas simples que no alteran el estado de la base.

## Esqueleto (el 20% esencial)
1. **Atomicidad** – Todas las operaciones dentro de la transacción se tratan como una sola acción: se confirman todas o ninguna.  
2. **Commit** – Marca el punto en que los cambios temporales se hacen permanentes y visibles para otras sesiones.  
3. **Rollback** – Revierte los cambios realizados desde el inicio de la transacción cuando ocurre un error.  
4. **Aislamiento** – Define cómo se ven los datos modificados por una transacción a otras transacciones concurrentes.  

## Como funciona
1. Se inicia la transacción (por ejemplo, `BEGIN`).  
2. Se ejecutan las operaciones de lectura/escritura; cada una queda en un buffer provisional.  
3. Si todas terminan sin error, se llama a `COMMIT`, que escribe los cambios en el log y los hace visibles.  
4. Si alguna falla, se ejecuta `ROLLBACK`, que descarta el buffer y restaura el estado anterior.  
5. El nivel de aislamiento determina si otras sesiones pueden leer datos intermedios o deben esperar al `COMMIT`.

## Detalles
- **Básico**: Uso de `BEGIN`, `COMMIT` y `ROLLBACK` en SQL estándar; comprensión de la atomicidad.  
- **Intermedio**: Configuración de niveles de aislamiento (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) y su impacto en bloqueos y rendimiento.  
- **Avanzado**: Manejo de transacciones distribuidas (two‑phase commit), control de puntos de guardado (savepoints) y estrategias de retry en entornos de alta concurrencia.

## Ejemplo minimo
```sql
-- Inicia la transacción
BEGIN;

-- Operación que debe ser atómica
INSERT INTO ventas (producto_id, cantidad, fecha)
VALUES (42, 10, CURRENT_DATE);

-- Si todo está bien, confirma
COMMIT;
-- Si ocurre un error, deshace
-- ROLLBACK;
```

## Errores comunes
- Olvidar el `COMMIT` y dejar la transacción abierta, provocando bloqueos; siempre cerrar explícitamente.  
- Usar `ROLLBACK` después de un `COMMIT`; el `ROLLBACK` solo tiene efecto antes del commit.  
- Seleccionar un nivel de aislamiento demasiado estricto sin necesidad, lo que degrada el rendimiento; elegir el nivel mínimo que garantice la consistencia requerida.  

## Estado actual
**Fundamentos estables**: la semántica de `BEGIN/COMMIT/ROLLBACK` y los cuatro niveles de aislamiento son parte del estándar SQL y se implementan de forma consistente en los principales RDBMS.  
**Práctica moderna**: los sistemas de bases de datos en la nube ofrecen transacciones sin servidor y APIs de control de versiones; además, los frameworks de procesamiento de datos (por ejemplo, Apache Spark) incorporan soporte para transacciones en fuentes externas mediante conectores que implementan el two‑phase commit.

## Conexiones
- **ACID**: las transacciones son la pieza central que materializa la atomicidad, consistencia, aislamiento y durabilidad en una base de datos.  
- **Locking**: los mecanismos de bloqueo son la infraestructura que permite el aislamiento entre transacciones concurrentes.  
- **Data Warehousing**: en la carga de datos ETL, las transacciones aseguran que los hechos y dimensiones se inserten de forma coherente antes de que los reportes se actualicen.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de tablas y claves primarias.  
2. **Fundamentos**: practicar `BEGIN/COMMIT/ROLLBACK` en un entorno local (PostgreSQL, MySQL).  
3. **Aislamiento**: experimentar con diferentes niveles y observar bloqueos con consultas concurrentes.  
4. **Avanzado**: estudiar savepoints, transacciones distribuidas y patrones de retry en microservicios.  
5. **Especialización**: integrar transacciones en pipelines de datos (Airflow, dbt) y en sistemas de streaming (Kafka Connect con Exactly‑Once semantics).

## Preguntas de repaso
1. ¿Qué garantiza la atomicidad dentro de una transacción?  
2. ¿En qué momento se vuelve visible un cambio a otras sesiones?  
3. ¿Cómo afecta el nivel de aislamiento READ COMMITTED al fenómeno de “dirty reads”?  
4. ¿Cuál es la diferencia entre `ROLLBACK` y un savepoint?  
5. ¿Por qué una transacción larga puede degradar el rendimiento de un data warehouse?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-10-transactions written_at=2026-11-05T22:55:23.174065+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/15 - Transacciones|Transacciones]] · *Backend*
- [[04 - Database & Data Analytics/11 - ACID & Isolation|ACID & Isolation]]

---
← [[04 - Database & Data Analytics/09 - Indexes|Indexes]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/11 - ACID & Isolation|ACID & Isolation]] →
