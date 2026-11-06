---
title: "Data Modeling"
area: "Database / Data Analytics"
numero: 2
aliases: ["Data Modeling"]
tags: [concepto, it/database-data-analytics]
---
# Data Modeling

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 2 de 25**

## Qué abarca
- Modelar entidades
- relaciones y estructuras

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el data modeling para traducir los requerimientos del negocio en una estructura de datos que sea fácil de consultar y mantener. Resuelvo problemas de redundancia, inconsistencia y consultas lentas al organizar la información en entidades y relaciones bien definidas. En mi día a día como ingeniero de datos y analista senior, el modelo guía la creación de esquemas en bases relacionales, la generación de pipelines ETL y la construcción de dashboards fiables. Después de dominarlo, puedo diseñar bases de datos que escalen, optimizar consultas y validar la calidad de los datos. No necesito preocuparme por el data modeling cuando trabajo exclusivamente con datos no estructurados almacenados en lagos de datos sin esquema fijo.

## Esqueleto (el 20% esencial)
1. **Entidades**: representan objetos o conceptos del dominio que necesitan ser almacenados (clientes, órdenes, productos).  
2. **Relaciones**: describen cómo se conectan las entidades entre sí (una orden pertenece a un cliente).  
3. **Atributos y tipos**: definen la información concreta de cada entidad y su formato (fecha, número, texto).  
4. **Claves primarias y foráneas**: garantizan unicidad y permiten enlazar registros de distintas tablas.  
5. **Normalización**: organiza los atributos en tablas para eliminar redundancia y evitar anomalías de actualización.

## Como funciona
1. Identifico las **entidades** a partir de los requerimientos de negocio.  
2. Para cada entidad, enumero sus **atributos** y selecciono un **tipo de dato** apropiado.  
3. Defino una **clave primaria** que identifique de forma única cada fila.  
4. Analizo cómo se relacionan las entidades y creo **claves foráneas** que establezcan esas conexiones.  
5. Aplico reglas de **normalización** (1NF, 2NF, 3NF) para distribuir los atributos en tablas sin duplicación.  
6. El esquema resultante se implementa en la base de datos y sirve como guía para consultas y ETL.

## Detalles
- **Básico**: reconocimiento de entidades y atributos; elección de tipos simples (INT, VARCHAR).  
- **Intermedio**: diseño de relaciones 1‑to‑1, 1‑to‑many y many‑to‑many mediante tablas de unión; uso de claves compuestas.  
- **Avanzado**: aplicación de normalización avanzada (BCNF, 4NF), modelado de historización (temporal tables), y técnicas de desnormalización controlada para rendimiento de analítica.  

## Ejemplo minimo
```sql
-- Entidad Cliente
CREATE TABLE cliente (
    cliente_id INT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE
);

-- Entidad Orden vinculada a Cliente
CREATE TABLE orden (
    orden_id    INT PRIMARY KEY,
    cliente_id  INT NOT NULL,
    fecha       DATE NOT NULL,
    total       DECIMAL(10,2),
    FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id)
);
```

## Errores comunes
- **Olvidar la clave primaria** → genera filas duplicadas; siempre definir una PK única.  
- **Usar claves foráneas incorrectas** → rompe la integridad referencial; validar que los tipos coincidan.  
- **Sobrenormalizar** → crea demasiadas tablas y consultas lentas; desnormalizar cuando el rendimiento lo justifique.  
- **Ignorar la tipificación adecuada** → provoca conversiones costosas; elegir tipos precisos desde el inicio.

## Estado actual
- **Fundamentos estables**: entidad‑relación, claves primarias/foráneas y normalización siguen siendo la base para cualquier esquema relacional.  
- **Práctica moderna**: se complementa con modelado de datos en lagos (schema‑on‑read), uso de herramientas de modelado visual (dbdiagram.io, ER/Studio) y patrones como Data Vault para entornos de big data.

## Conexiones
- **Relational Databases**: el data modeling define la estructura que las bases relacionales utilizan para almacenar y consultar datos.  
- **Keys & Constraints**: las claves y restricciones son los mecanismos que hacen que el modelo sea consistente y fiable.  
- **Normalization**: la normalización es la disciplina que refina el modelo para eliminar redundancia y evitar anomalías.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de SQL, tipos de datos y operaciones CRUD.  
2. **Fundamentos**: estudiar diagramas entidad‑relación y practicar con ejercicios de identificación de entidades y relaciones.  
3. **Intermedio**: profundizar en claves compuestas, relaciones many‑to‑many y reglas de normalización hasta 3NF.  
4. **Avanzado**: explorar BCNF, modelado temporal, Data Vault y estrategias de desnormalización para data warehouses.  
5. **Aplicación**: diseñar esquemas reales, generar scripts de creación y validar con casos de uso de ETL y reporting.

## Preguntas de repaso
1. ¿Cómo determino cuál atributo debe ser la clave primaria de una entidad?  
2. ¿Qué diferencia hay entre una relación 1‑to‑many y una many‑to‑many en el modelo?  
3. ¿En qué situaciones es aceptable desnormalizar una tabla después de haberla normalizado?  
4. ¿Cómo afecta la elección del tipo de dato a la eficiencia de una consulta analítica?  
5. ¿Qué problemas de integridad aparecen si una clave foránea no coincide con la clave primaria referenciada?

<!-- trazabilidad: run_id=run-20261105-151808-34f931 concept=04-database-data-analytics-02-data-modeling written_at=2026-11-05T18:18:53.857121+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/13 - Modelado de datos|Modelado de datos]] · *Backend*
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]]
- [[04 - Database & Data Analytics/07 - Keys & Constraints|Keys & Constraints]]
- [[04 - Database & Data Analytics/08 - Normalization|Normalization]]

---
← [[04 - Database & Data Analytics/01 - Data Fundamentals|Data Fundamentals]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]] →
