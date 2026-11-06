---
title: "ACID & Isolation"
area: "Database / Data Analytics"
numero: 11
aliases: ["ACID & Isolation"]
tags: [concepto, it/database-data-analytics]
---
# ACID & Isolation

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 11 de 25**

## Qué abarca
- Consistencia
- concurrencia
- niveles de aislamiento

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo ACID y los niveles de Isolation para garantizar que cada operación de escritura sobre mis bases de datos sea fiable, predecible y libre de efectos colaterales inesperados. Resuelvo problemas de pérdida de datos, lecturas sucias y resultados inconsistentes que aparecen cuando varios procesos acceden concurrentemente a los mismos registros. En mi día a día como ingeniero de datos y analista senior, aplico estas garantías al diseñar pipelines ETL, al ejecutar actualizaciones masivas y al ofrecer dashboards que dependen de datos siempre consistentes. Después de entender ACID puedo decidir cuándo usar transacciones explícitas, cuándo ajustar el nivel de aislamiento y cuándo confiar en mecanismos de control de concurrencia de la base. No necesito preocuparme por ACID cuando trabajo con almacenes de solo lectura o con sistemas que aceptan consistencia eventual por diseño.

## Esqueleto (el 20% esencial)
1. **Atomicidad** – una transacción se ejecuta completa o no se aplica nada.  
2. **Consistencia** – al finalizar la transacción la base respeta todas sus reglas de integridad.  
3. **Isolation (niveles)** – controla cómo las transacciones concurrentes se ven entre sí, evitando lecturas sucias, no repetibles y fantasmas.  
4. **Durabilidad** – los cambios confirmados persisten aun ante fallos del sistema.  

## Como funciona
1. El cliente inicia una **transacción** (`BEGIN`).  
2. El motor reserva los recursos necesarios según el **nivel de Isolation** seleccionado (por ejemplo `READ COMMITTED`).  
3. Cada sentencia (`INSERT`, `UPDATE`, `DELETE`) se ejecuta dentro del contexto aislado; los bloqueos o versiones de fila evitan interferencias.  
4. Al ejecutar `COMMIT`, el motor verifica que la **consistencia** no se haya violado y escribe los cambios en el log de recuperación, garantizando **durabilidad**.  
5. Si ocurre un error o se llama a `ROLLBACK`, se revierte todo, manteniendo la **atomicidad**.

## Detalles
- **Básico**: usar `BEGIN … COMMIT` con el nivel por defecto (`READ COMMITTED`) para la mayoría de los procesos ETL.  
- **Intermedio**: elegir niveles más estrictos (`REPEATABLE READ`, `SERIALIZABLE`) cuando se necesita evitar lecturas no repetibles o fenómenos de fantasmas en reportes críticos.  
- **Avanzado**: combinar aislamiento con técnicas como **MVCC** (Multi‑Version Concurrency Control) para escalar lecturas sin bloquear, y emplear **two‑phase commit** en transacciones distribuidas que abarcan varios nodos.

## Ejemplo minimo
```sql
-- PostgreSQL: transacción con aislamiento SERIALIZABLE
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

UPDATE orders
SET status = 'shipped'
WHERE order_id = 1024
  AND status = 'processed';

COMMIT;
```
El bloque garantiza que ningún otro proceso pueda modificar la fila `order_id = 1024` mientras se evalúa la condición y se actualiza, evitando lecturas sucias y garantizando consistencia.

## Errores comunes
- **Usar el nivel más alto por defecto**: genera bloqueos excesivos y degrada el rendimiento; elegir el nivel adecuado según la necesidad.  
- **Olvidar `COMMIT` o `ROLLBACK`**: deja transacciones abiertas y bloquea recursos; siempre cerrar explícitamente.  
- **Confundir aislamiento con consistencia**: el aislamiento controla la interacción entre transacciones, mientras que la consistencia se refiere a las reglas de integridad definidas por el esquema.

## Estado actual
- **Fundamentos estables**: los cuatro principios ACID siguen siendo la base de cualquier motor transaccional relacional (PostgreSQL, MySQL, SQL Server, Oracle).  
- **Práctica moderna**: se favorece el uso de **MVCC** y niveles de aislamiento configurables para equilibrar concurrencia y consistencia; en entornos distribuidos se complementa con protocolos de consenso (Raft, Paxos) y **distributed transactions** que extienden ACID más allá de un solo nodo.

## Conexiones
- **Data Warehousing**: los procesos de carga (ELT) suelen ejecutarse en transacciones ACID para asegurar que los datos de origen y destino permanezcan consistentes.  
- **Eventual Consistency**: contrasta con ACID en sistemas NoSQL donde se sacrifica aislamiento para lograr alta disponibilidad y partición tolerante.  
- **Distributed Transactions**: amplían los conceptos de ACID a múltiples bases de datos, requiriendo coordinadores de commit como el two‑phase commit.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de claves primarias/foráneas y manejo de índices.  
2. **Fundamentos**: estudiar los cuatro principios ACID y los niveles de Isolation en la documentación oficial de PostgreSQL o MySQL.  
3. **Intermedio**: practicar con bloqueos explícitos, observar bloqueos con `pg_locks`, y experimentar con `READ COMMITTED` vs `SERIALIZABLE`.  
4. **Avanzado**: profundizar en MVCC, analizar fenómenos de aislamiento (phantom reads) y aprender two‑phase commit con herramientas como `pg_prepared_xact`.  
5. **Especialización**: explorar ACID en bases de datos distribuidas (CockroachDB, Google Spanner) y comparar con modelos de consistencia eventual.

## Preguntas de repaso
1. ¿Qué garantiza la atomicidad dentro de una transacción y cómo se revierte si ocurre un error?  
2. ¿En qué situaciones elegirías el nivel de aislamiento `SERIALIZABLE` en lugar de `READ COMMITTED`?  
3. ¿Cómo evita MVCC los bloqueos de lectura mientras mantiene la consistencia de los datos?  
4. ¿Cuál es la diferencia principal entre ACID y la consistencia eventual en sistemas NoSQL?  
5. ¿Qué papel juega el protocolo two‑phase commit en una transacción distribuida?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-11-acid-isolation written_at=2026-11-05T22:56:18.908400+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/15 - Transacciones|Transacciones]] · *Backend*
- [[04 - Database & Data Analytics/10 - Transactions|Transactions]]

---
← [[04 - Database & Data Analytics/10 - Transactions|Transactions]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/12 - Database Architecture|Database Architecture]] →
