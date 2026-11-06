---
title: "Transacciones"
area: "Backend"
numero: 15
aliases: ["Transacciones"]
tags: [concepto, it/backend]
---
# Transacciones

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 15 de 25**

## Qué abarca
- ACID
- isolation
- locks
- consistency

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo transacciones para garantizar que un conjunto de operaciones sobre la base de datos se ejecuten como una unidad indivisible. Resuelvo problemas de inconsistencia cuando varios procesos modifican datos concurrentemente, asegurando que el estado final sea siempre válido. En mi día a día como ingeniero backend senior, las transacciones aparecen al diseñar endpoints que crean o actualizan varios recursos relacionados, como una orden que escribe en tablas de pedidos, inventario y pagos. Después de entenderlas, puedo diseñar APIs idempotentes y manejar fallos sin dejar datos corruptos. No necesito preocuparme cuando la operación es solo una lectura simple o cuando el almacenamiento no soporta transacciones.

## Esqueleto (el 20% esencial)
1. **Atomicidad (A de ACID)** – Todas las operaciones dentro de la transacción se completan o ninguna lo hace.  
2. **Consistencia** – Al finalizar, la base de datos cumple con todas las reglas de integridad definidas.  
3. **Aislamiento** – Cada transacción se ejecuta como si fuera la única, evitando interferencias de otras concurrentes.  
4. **Bloqueos (locks)** – El motor usa locks para implementar el aislamiento y prevenir lecturas/escrituras sucias.  
5. **Commit / Rollback** – El punto de decisión donde se persiste o se descarta el conjunto de cambios.

## Como funciona
1. El código abre una transacción (`BEGIN`).  
2. Se ejecutan las operaciones de escritura/lectura requeridas. Cada operación adquiere los locks necesarios según el nivel de aislamiento configurado.  
3. Si todas las operaciones son exitosas, se llama a `COMMIT`; el motor libera los locks y persiste los cambios.  
4. Si ocurre un error, se invoca `ROLLBACK`; el motor revierte todas las modificaciones y libera los locks.  
5. El nivel de aislamiento (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) determina cuántas anomalías concurrentes pueden aparecer.

## Detalles
- **Básico:** Uso de `BEGIN … COMMIT/ROLLBACK` en consultas SQL o mediante el ORM del framework.  
- **Intermedio:** Selección del nivel de aislamiento adecuado; por ejemplo, `READ COMMITTED` evita lecturas sucias pero permite lecturas no repetibles.  
- **Avanzado:** Manejo de deadlocks mediante reintentos exponenciales y uso de lock timeouts; aplicación de patrones como “Saga” cuando la base de datos no soporta transacciones distribuidas.

## Ejemplo minimo
```python
# Python con psycopg2 (PostgreSQL)
import psycopg2

conn = psycopg2.connect(dsn)
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO orders (id, total) VALUES (1, 100)")
            cur.execute("UPDATE inventory SET qty = qty - 1 WHERE product_id = 42")
    # al salir del bloque with, se hace COMMIT automáticamente
except Exception:
    conn.rollback()   # se ejecuta automáticamente al salir del bloque con error
```

## Errores comunes
- **Olvidar el `COMMIT`** → los cambios quedan pendientes y se liberan al cerrar la conexión.  
- **Usar un nivel de aislamiento demasiado estricto** → genera bloqueos innecesarios y reduce el rendimiento; elegir el nivel mínimo que satisfaga la consistencia requerida.  
- **No manejar deadlocks** → la aplicación falla; envolver la transacción en lógica de reintento evita el problema.

## Estado actual
- **Fundamentos estables:** ACID, los comandos `BEGIN`, `COMMIT`, `ROLLBACK` y los niveles de aislamiento estándar están consolidados en los principales RDBMS.  
- **Práctica moderna:** Se complementan con patrones de compensación (Sagas) para microservicios que requieren consistencia eventual, y con herramientas de gestión de transacciones distribuidas (e.g., XA, 2PC) cuando varios recursos participan.

## Conexiones
- **Locking** – Los locks son el mecanismo que permite implementar el aislamiento y evitar condiciones de carrera.  
- **Eventual Consistency** – En arquitecturas de microservicios, las transacciones locales se combinan con eventos para lograr consistencia eventual.  
- **Circuit Breaker** – Cuando una transacción falla repetidamente, un circuit breaker protege al servicio evitando sobrecargar la base de datos.

## Ruta de estudio
1. **Prerequisitos:** SQL básico, conceptos de bases de datos relacionales y manejo de conexiones.  
2. **Fundamentos:** Practicar `BEGIN/COMMIT/ROLLBACK`, experimentar con los niveles de aislamiento y observar efectos de bloqueos.  
3. **Intermedio:** Estudiar manejo de deadlocks y estrategias de reintento; leer la documentación del motor de base de datos usado.  
4. **Avanzado:** Explorar patrones Saga, transacciones distribuidas y herramientas de orquestación (e.g., Temporal, Zeebe).  

## Preguntas de repaso
1. ¿Qué garantiza la atomicidad dentro de una transacción?  
2. ¿Cómo afecta el nivel de aislamiento `SERIALIZABLE` al rendimiento y a la consistencia?  
3. ¿Cuál es la diferencia entre un `ROLLBACK` implícito y uno explícito?  
4. ¿Por qué es importante manejar deadlocks en servicios de alta concurrencia?  
5. ¿En qué casos preferirías un patrón Saga sobre una transacción distribuida tradicional?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-15-transacciones written_at=2026-11-05T19:48:58.981347+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/10 - Transactions|Transactions]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/11 - ACID & Isolation|ACID & Isolation]] · *Database / Data Analytics*

---
← [[03 - Backend/14 - ORM - Data Access|ORM / Data Access]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/16 - Autenticación|Autenticación]] →
