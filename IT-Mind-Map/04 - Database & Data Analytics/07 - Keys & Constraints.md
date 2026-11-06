---
title: "Keys & Constraints"
area: "Database / Data Analytics"
numero: 7
aliases: ["Keys & Constraints"]
tags: [concepto, it/database-data-analytics]
---
# Keys & Constraints

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 7 de 25**

## Qué abarca
- Primary keys
- foreign keys
- unique
- constraints

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **keys** y **constraints** para garantizar la integridad y la consistencia de los datos que modelizo y consulto. Resuelvo problemas como filas duplicadas, referencias rotas entre tablas y valores fuera de los rangos esperados, que aparecen constantemente al diseñar esquemas de bases relacionales o al crear pipelines de extracción‑transformación‑carga (ETL). Cuando entiendo cómo definir y aplicar primary keys, foreign keys, unique constraints y otras restricciones, puedo construir modelos que evitan errores de calidad y facilitan consultas eficientes, además de habilitar auditorías y reportes confiables. No necesito preocuparme por estas estructuras cuando trabajo exclusivamente con almacenes de datos NoSQL sin esquema rígido o cuando la consistencia eventual es aceptable.

## Esqueleto (el 20% esencial)
1. **Primary key**: identifica de forma única cada fila de una tabla y sirve de punto de anclaje para relaciones.  
2. **Foreign key**: enlaza una columna con la primary key de otra tabla, asegurando que la referencia exista.  
3. **Unique constraint**: impide valores duplicados en columnas que no son clave primaria.  
4. **Check constraint**: valida que los datos cumplan condiciones lógicas (rango, formato, etc.).  
5. **Not‑null constraint**: obliga a que una columna siempre reciba un valor.

## Como funciona
1. Al crear una tabla, se declara la **primary key**; el motor crea un índice único que impide filas con el mismo valor.  
2. Cuando se define una **foreign key**, el motor verifica en tiempo de inserción o actualización que el valor exista en la tabla referenciada; si no, rechaza la operación.  
3. Las **unique constraints** generan índices adicionales que bloquean inserciones duplicadas en las columnas especificadas.  
4. Cada **check constraint** se evalúa para cada fila modificada; si la expresión es falsa, la transacción falla.  
5. La **not‑null** se comprueba antes de aceptar la fila, garantizando que la columna nunca quede vacía.

## Detalles
- **Básico**: primary key y not‑null son obligatorios para identificar registros y evitar nulos críticos.  
- **Intermedio**: foreign keys y unique constraints añaden relaciones y reglas de unicidad que simplifican joins y evitan datos redundantes.  
- **Avanzado**: check constraints permiten reglas de negocio complejas (p. ej., `salary > 0 AND salary < 1_000_000`). En bases de datos con alta concurrencia, los índices creados por keys pueden requerir ajustes de bloqueo y particionamiento.

## Ejemplo minimo
```sql
CREATE TABLE empleados (
    emp_id      INT PRIMARY KEY,
    nombre      VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    dept_id     INT,
    salario     NUMERIC(10,2) CHECK (salario > 0)
);

CREATE TABLE departamentos (
    dept_id     INT PRIMARY KEY,
    nombre_dept VARCHAR(50) NOT NULL
);

ALTER TABLE empleados
ADD CONSTRAINT fk_dept FOREIGN KEY (dept_id)
REFERENCES departamentos(dept_id);
```

## Errores comunes
- **Olvidar la not‑null** en columnas clave → inserciones fallan inesperadamente; revisar siempre la definición de la tabla.  
- **Crear foreign keys sin índices** en la tabla referenciada → consultas JOIN lentas; agregar índices manualmente si el motor no lo hace.  
- **Usar unique en columnas con valores nulos** pensando que evitará duplicados; los valores nulos no se consideran duplicados en la mayoría de los SGBD.  

## Estado actual
- **Fundamentos estables**: la sintaxis de `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK` y `NOT NULL` está soportada por los principales RDBMS (PostgreSQL, MySQL, SQL Server, Oracle) y su comportamiento es consistente.  
- **Práctica moderna**: se recomienda combinar constraints con políticas de datos (p. ej., `DEFERRABLE` en PostgreSQL) y con herramientas de gestión de esquemas como dbt o Liquibase para versionar cambios de forma controlada.

## Conexiones
- **Data Modeling**: las keys son los pilares que convierten un modelo lógico en un modelo físico coherente.  
- **Normalization**: las foreign keys permiten aplicar las formas normales al separar datos y evitar redundancia.  
- **Relational Databases**: los constraints son mecanismos internos que hacen posible la integridad referencial que caracteriza a los sistemas relacionales.

## Ruta de estudio
1. **Prerequisitos**: comprender tipos de datos SQL y operaciones básicas de SELECT/INSERT.  
2. **Fundamentos**: practicar creación de tablas con primary key y not‑null; ejecutar inserciones que violen y respeten esas reglas.  
3. **Relaciones**: añadir foreign keys y observar el comportamiento en DELETE/UPDATE con `ON DELETE CASCADE` o `RESTRICT`.  
4. **Unicidad y validación**: experimentar con unique y check constraints en escenarios de negocio (p. ej., rangos de edad).  
5. **Herramientas de versionado**: aprender a describir constraints en scripts dbt o Liquibase y a aplicar migraciones en entornos de staging/producción.  

## Preguntas de repaso
1. ¿Qué ventaja aporta una primary key frente a una columna con `UNIQUE` y `NOT NULL`?  
2. ¿Cómo impide una foreign key que se inserte un registro huérfano?  
3. ¿En qué casos una `CHECK` constraint es preferible a validar datos en la capa de aplicación?  
4. ¿Qué efecto tiene un `UNIQUE` constraint sobre columnas que pueden contener valores nulos?  
5. ¿Por qué es importante versionar los cambios de constraints con herramientas como dbt?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-07-keys-constraints written_at=2026-11-05T22:52:11.829787+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/13 - Modelado de datos|Modelado de datos]] · *Backend*
- [[04 - Database & Data Analytics/02 - Data Modeling|Data Modeling]]
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]]
- [[04 - Database & Data Analytics/08 - Normalization|Normalization]]

---
← [[04 - Database & Data Analytics/06 - JOINs|JOINs]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/08 - Normalization|Normalization]] →
