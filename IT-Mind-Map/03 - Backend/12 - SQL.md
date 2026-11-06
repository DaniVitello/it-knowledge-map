---
title: "SQL"
area: "Backend"
numero: 12
aliases: ["SQL"]
tags: [concepto, it/backend]
---
# SQL

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 12 de 25**

## Qué abarca
- SELECT
- JOIN
- índices
- transacciones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo SQL para leer y escribir datos estructurados que sustentan la lógica de negocio de mis servicios y APIs. Resuelvo la necesidad de consultar información de forma declarativa, combinar tablas relacionadas y garantizar la consistencia mediante transacciones. Aparece cada vez que un endpoint necesita obtener, filtrar o actualizar datos en una base relacional, ya sea para devolver un listado, calcular agregados o mantener la integridad de operaciones críticas. Después de entender SQL puedo diseñar esquemas eficientes, escribir consultas que escalen y manejar errores de concurrencia. No necesito preocuparme cuando el servicio usa únicamente almacenamiento en memoria o bases NoSQL que no soportan el lenguaje SQL.

## Esqueleto (el 20% esencial)
1. **SELECT** – declara qué columnas o expresiones se devuelven de una o más tablas.  
2. **JOIN** – combina filas de tablas distintas según una condición de relación.  
3. **Índices** – estructuras que aceleran la búsqueda de filas para consultas frecuentes.  
4. **Transacciones** – agrupan operaciones de lectura/escritura garantizando atomicidad, consistencia, aislamiento y durabilidad (ACID).  

## Como funciona
1. El motor recibe una sentencia `SELECT` y analiza su árbol sintáctico.  
2. Determina los `JOIN` necesarios y el orden de ejecución óptimo usando estadísticas de los índices.  
3. Accede a los índices para localizar rápidamente las filas que cumplen los predicados de filtrado.  
4. Si la consulta está dentro de una transacción, el motor registra los cambios en el log antes de aplicar los writes, asegurando rollback en caso de error.  
5. Finalmente, proyecta las columnas solicitadas y devuelve el conjunto de resultados al cliente.

## Detalles
- **Básico**: `SELECT` con `WHERE` para filtrar; uso de `PRIMARY KEY` implícito como índice único.  
- **Intermedio**: `INNER/LEFT JOIN` para relaciones uno‑a‑muchos; creación de índices secundarios (`CREATE INDEX`) para columnas usadas en filtros y joins.  
- **Avanzado**: `EXPLAIN` para inspeccionar planes de ejecución; ajuste de índices compuestos; manejo de aislamiento de transacciones (`READ COMMITTED`, `SERIALIZABLE`) y control de bloqueos para evitar deadlocks.

## Ejemplo minimo
```sql
-- Crear tabla simple
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insertar un registro
INSERT INTO users (email) VALUES ('alice@example.com');

-- Consulta básica con SELECT
SELECT id, email FROM users WHERE email LIKE '%@example.com';
```

## Errores comunes
- **Olvidar índices** en columnas usadas en `WHERE` o `JOIN`, lo que degrada el rendimiento; solución: crear índices adecuados antes de lanzar consultas en producción.  
- **Usar SELECT *** en tablas grandes, generando transferencia innecesaria; solución: proyectar solo columnas requeridas.  
- **No manejar transacciones** en operaciones multi‑step, provocando datos inconsistentes; solución: envolver los cambios críticos en `BEGIN … COMMIT`.

## Estado actual
- Los conceptos de `SELECT`, `JOIN`, índices e `ACID` son fundamentos estables y soportados por todos los sistemas de bases de datos relacionales modernos (PostgreSQL, MySQL, SQL Server).  
- En la práctica contemporánea se combinan con técnicas de partición horizontal, índices column‑store y motores de ejecución vectorizada para mejorar la escalabilidad de servicios de alta carga.

## Conexiones
- **Filtering & Aggregation**: las cláusulas `WHERE`, `GROUP BY` y funciones de agregación (`COUNT`, `SUM`) amplían el poder de `SELECT` para resumir datos antes de enviarlos al cliente.  
- **JOINs**: la capacidad de combinar tablas es la base para modelar relaciones de dominio y evitar duplicación de datos en la capa de negocio.  
- **Caching**: resultados de consultas frecuentes se pueden almacenar en cachés (Redis, Memcached) para reducir la carga de la base y acelerar respuestas de API.

## Ruta de estudio
1. **Prerequisitos**: comprensión de estructuras de datos, modelo relacional y comandos básicos de terminal.  
2. **Fundamentos**: practicar `SELECT`, `WHERE`, `ORDER BY` y creación de índices simples.  
3. **Relaciones**: dominar `INNER`, `LEFT` y `FULL JOIN`, y diseñar esquemas normalizados.  
4. **Transacciones**: estudiar niveles de aislamiento y manejo de bloqueos.  
5. **Optimización**: usar `EXPLAIN`, crear índices compuestos y explorar particionamiento.  
6. **Integración**: conectar consultas SQL desde código backend (ORMs, drivers) y aplicar patrones de repositorio.

## Preguntas de repaso
1. ¿Qué ventaja aporta un índice a una cláusula `WHERE` y cómo afecta al plan de ejecución?  
2. ¿Cómo se diferencia un `INNER JOIN` de un `LEFT JOIN` en el resultado devuelto?  
3. ¿Qué garantiza una transacción ACID y cuándo es crítico usarla en un endpoint de API?  
4. ¿Por qué es una mala práctica usar `SELECT *` en una tabla con millones de filas?  
5. ¿Cómo puedes validar que una consulta está usando el índice esperado?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-12-sql written_at=2026-11-05T19:46:00.872840+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/04 - SQL|SQL]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/05 - Filtering & Aggregation|Filtering & Aggregation]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/06 - JOINs|JOINs]] · *Database / Data Analytics*

---
← [[03 - Backend/11 - Bases de datos|Bases de datos]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/13 - Modelado de datos|Modelado de datos]] →
