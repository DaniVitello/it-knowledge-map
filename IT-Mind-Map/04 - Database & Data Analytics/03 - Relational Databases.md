---
title: "Relational Databases"
area: "Database / Data Analytics"
numero: 3
aliases: ["Relational Databases"]
tags: [concepto, it/database-data-analytics]
---
# Relational Databases

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 3 de 25**

## Qué abarca
- Tablas
- filas
- columnas
- relaciones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo bases de datos relacionales para estructurar datos en tablas con filas y columnas, de modo que pueda consultar y combinar información de forma predecible y eficiente. Resuelvo problemas de integridad, duplicación y consultas complejas que aparecen al consolidar datos de distintas fuentes en un data warehouse o al servir métricas a un dashboard analítico. Después de entender cómo funcionan, puedo diseñar esquemas normalizados, escribir consultas SQL optimizadas y elegir entre una base relacional o una alternativa NoSQL según el caso de uso. No necesito preocuparme por este concepto cuando trabajo exclusivamente con archivos planos o con sistemas de almacenamiento de objetos sin requerimientos de relaciones entre entidades.

## Esqueleto (el 20% esencial)
1. **Tablas**: estructuras bidimensionales donde cada fila representa un registro y cada columna un atributo.  
2. **Llaves (Keys) y restricciones**: garantizan unicidad y relaciones entre tablas (primary key, foreign key, unique, check).  
3. **Relaciones**: enlaces lógicos entre tablas mediante foreign keys que permiten JOINs y consultas integradas.  
4. **Normalización**: proceso de organizar tablas para eliminar redundancia y asegurar consistencia.  
5. **Consultas SQL**: lenguaje declarativo para crear, leer, actualizar y borrar datos dentro del esquema relacional.

## Como funciona
1. Defino el **modelo** creando tablas con columnas que describen los atributos del dominio.  
2. Asigno una **primary key** a cada tabla para identificar unívocamente cada fila.  
3. Cuando una entidad necesita referenciar a otra, añado una **foreign key** que apunta a la primary key correspondiente.  
4. Aplico **reglas de normalización** (1NF, 2NF, 3NF) para distribuir la información en varias tablas y evitar duplicados.  
5. Con **SQL** ejecuto consultas que usan `JOIN` para combinar datos de tablas relacionadas, obteniendo resultados analíticos o de reporte.

## Detalles
- **Básico**: creación de tablas simples, definición de primary keys y uso de `SELECT` con filtros (`WHERE`).  
- **Intermedio**: implementación de foreign keys, índices para acelerar `JOIN`s, y uso de `GROUP BY`/`HAVING` para agregaciones.  
- **Avanzado**: diseño de esquemas altamente normalizados, particionamiento de tablas, uso de vistas materializadas y optimización de planes de ejecución mediante hints y estadísticas.

## Ejemplo minimo
```sql
-- Creación de dos tablas relacionadas
CREATE TABLE clientes (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE pedidos (
    pedido_id INT PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    total DECIMAL(10,2)
);

-- Consulta que une ambas tablas
SELECT c.nombre, p.total
FROM clientes c
JOIN pedidos p ON c.cliente_id = p.cliente_id;
```

## Errores comunes
- Definir foreign keys sin índices: ralentiza los `JOIN`s.  
- Normalizar en exceso: genera demasiados `JOIN`s y afecta el rendimiento.  
- Olvidar actualizar estadísticas: el optimizador elige planes subóptimos.  
- Usar tipos de datos incompatibles entre columnas relacionadas: provoca errores de integridad.

## Estado actual
**Fundamentos estables**: el modelo relacional, ACID, SQL estándar y las reglas de normalización siguen siendo la base para la mayoría de los sistemas de gestión de bases de datos (PostgreSQL, MySQL, SQL Server, Oracle).  

**Práctica moderna**: se complementa con arquitecturas cloud‑native (Amazon RDS, Azure SQL), bases de datos distribuidas que preservan compatibilidad SQL (CockroachDB, Google Spanner) y herramientas de orquestación de migraciones (Flyway, Liquibase). Además, el uso de índices columnstore y consultas vectorizadas mejora el rendimiento de cargas analíticas.

## Conexiones
- **ORM / Data Access**: los mapeadores objeto‑relacional traducen clases de código a tablas y generan automáticamente las consultas `JOIN` necesarias.  
- **Normalization**: la normalización define cómo dividir la información en tablas para que los ORM puedan crear relaciones coherentes.  
- **NoSQL**: cuando los requisitos de flexibilidad de esquema o escala horizontal superan las ventajas de las relaciones, se evalúa migrar a bases de datos NoSQL.

## Ruta de estudio
1. **Prerequisitos**: conceptos de datos estructurados, lógica de bases de datos y sintaxis básica de SQL.  
2. **Fundamentos**: crear esquemas simples, practicar `SELECT`, `INSERT`, `UPDATE`, `DELETE` y definir claves primarias.  
3. **Intermedio**: diseñar relaciones, aplicar normalización hasta 3NF, crear índices y usar `JOIN`s avanzados.  
4. **Avanzado**: estudiar particionamiento, replicación, tuning de consultas, y explorar bases relacionales distribuidas en la nube.  
5. **Especialización**: integrar ORM en aplicaciones, comparar con modelos NoSQL y aprender migraciones de esquemas con herramientas de versionado.

## Preguntas de repaso
1. ¿Cómo garantiza una foreign key la integridad referencial entre dos tablas?  
2. ¿Qué problema resuelve la normalización y en qué nivel (1NF, 2NF, 3NF) se elimina la dependencia parcial?  
3. ¿Cuál es la diferencia práctica entre un `INNER JOIN` y un `LEFT JOIN` al combinar datos relacionales?  
4. ¿Por qué es importante crear índices sobre columnas usadas en condiciones de `JOIN`?  
5. ¿En qué situaciones considerarías reemplazar una base relacional por una solución NoSQL?

<!-- trazabilidad: run_id=run-20261105-151808-34f931 concept=04-database-data-analytics-03-relational-databases written_at=2026-11-05T18:19:42.510149+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/11 - Bases de datos|Bases de datos]] · *Backend*
- [[03 - Backend/13 - Modelado de datos|Modelado de datos]] · *Backend*
- [[03 - Backend/14 - ORM - Data Access|ORM / Data Access]] · *Backend*
- [[04 - Database & Data Analytics/02 - Data Modeling|Data Modeling]]
- [[04 - Database & Data Analytics/07 - Keys & Constraints|Keys & Constraints]]
- [[04 - Database & Data Analytics/08 - Normalization|Normalization]]
- [[04 - Database & Data Analytics/12 - Database Architecture|Database Architecture]]
- [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]]

---
← [[04 - Database & Data Analytics/02 - Data Modeling|Data Modeling]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/04 - SQL|SQL]] →
