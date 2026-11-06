---
title: "Data Fundamentals"
area: "Database / Data Analytics"
numero: 1
aliases: ["Data Fundamentals"]
tags: [concepto, it/database-data-analytics]
---
# Data Fundamentals

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 1 de 25**

## Qué abarca
- Datos
- registros
- atributos
- entidades
- relaciones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los fundamentos de datos para estructurar la información que ingiere mi pipeline y para diseñar consultas que extraigan insights fiables. Resuelvo problemas de ambigüedad y redundancia al transformar datos crudos en registros consistentes, lo que permite análisis reproducibles y decisiones basadas en evidencia. En mi día a día como ingeniero de datos y analista senior, estos conceptos aparecen al modelar esquemas relacionales, al definir tablas de hechos y dimensiones, y al validar la calidad de los datos antes de cargarlos en un data lake. Después de comprenderlos, puedo diseñar modelos de datos escalables, optimizar consultas y detectar anomalías de forma automática. No necesito preocuparme cuando trabajo exclusivamente con datos ya normalizados y documentados en un catálogo de metadatos.

## Esqueleto (el 20% esencial)
1. **Dato**: unidad mínima de información que puede ser almacenada y procesada.  
2. **Registro**: conjunto de datos relacionados que forman una fila en una tabla.  
3. **Atributo**: columna que describe una característica del registro.  
4. **Entidad**: concepto del mundo real que modelamos como una tabla.  
5. **Relación**: vínculo lógico entre dos o más entidades, implementado mediante claves.

## Como funciona
1. Identifico la **entidad** que representa el dominio del problema (p. ej., Cliente).  
2. Defino los **atributos** que describen esa entidad (id, nombre, email).  
3. Cada **registro** se inserta como una fila con valores para esos atributos.  
4. Cuando necesito conectar dos entidades (Cliente y Pedido), creo una **relación** mediante una clave foránea.  
5. Los **datos** fluyen a través de este modelo, permitiendo consultas que combinan registros según las relaciones definidas.

## Detalles
- **Básico**: reconocer datos estructurados vs. no estructurados; crear tablas simples con atributos atómicos.  
- **Intermedio**: aplicar normalización (1NF, 2NF, 3NF) para eliminar redundancia y asegurar integridad referencial mediante claves primarias y foráneas.  
- **Avanzado**: diseñar esquemas de estrella o copo de nieve para data warehouses, usar particionamiento y clustering para consultas de gran volumen, y gestionar esquemas evolutivos con migraciones controladas.

## Ejemplo minimo
```sql
-- Definición de entidad Cliente
CREATE TABLE cliente (
    cliente_id INT PRIMARY KEY,
    nombre      VARCHAR(100),
    email       VARCHAR(150)
);

-- Definición de entidad Pedido con relación a Cliente
CREATE TABLE pedido (
    pedido_id   INT PRIMARY KEY,
    cliente_id  INT REFERENCES cliente(cliente_id),
    fecha       DATE,
    total       DECIMAL(10,2)
);
```

## Errores comunes
- **Duplicar atributos** en varias tablas → genera inconsistencias; usar claves y normalizar.  
- **Usar tipos de datos inadecuados** (p. ej., almacenar fechas como texto) → dificulta filtros y cálculos; elegir tipos nativos.  
- **Olvidar la clave primaria** → impide identificar registros únicos; siempre definir una.  
- **Crear relaciones sin índices** → consultas lentas; indexar claves foráneas.

## Estado actual
- **Fundamentos estables**: los conceptos de dato, registro, atributo, entidad y relación siguen siendo la base de cualquier modelo relacional y de los sistemas de análisis estructurado.  
- **Práctica moderna**: se complementan con técnicas de modelado dimensional para analytics, uso de esquemas flexibles (JSON/BSON) en bases NoSQL cuando la variedad de atributos es alta, y automatización de migraciones de esquema mediante herramientas como Liquibase o Flyway.

## Conexiones
- **ETL**: los fundamentos de datos guían la extracción, transformación y carga, pues cada paso depende de la correcta identificación de entidades y relaciones.  
- **Data Warehouse**: el modelado dimensional se construye a partir de entidades (dimensiones) y hechos (registros) definidos por estos conceptos.  
- **Machine Learning**: la calidad de los atributos y la integridad de los registros son críticas para entrenar modelos predictivos confiables.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de tipos de datos y operaciones CRUD.  
2. **Fundamentos**: estudiar datos, registros, atributos, entidades y relaciones mediante ejercicios de modelado de casos de negocio simples.  
3. **Normalización**: practicar con ejemplos que requieran 1NF‑3NF y detectar redundancias.  
4. **Modelado dimensional**: aprender esquemas de estrella y copo de nieve para analytics.  
5. **Optimización**: profundizar en índices, particionamiento y estrategias de migración de esquema.  
6. **Especialización**: explorar integración con pipelines ETL y preparación de datos para Machine Learning.

## Preguntas de repaso
1. ¿Cómo se diferencia un atributo de un registro en un modelo relacional?  
2. ¿Qué problema resuelve la normalización y en qué forma se refleja en una tabla?  
3. ¿Cuál es la función de una clave foránea dentro de una relación entre entidades?  
4. ¿En qué situaciones preferirías un modelo dimensional sobre un modelo estrictamente normalizado?  
5. ¿Qué impacto tiene no indexar una columna que actúa como clave foránea en el rendimiento de una consulta?

<!-- trazabilidad: run_id=run-20261105-141116-975ae2 concept=04-database-data-analytics-01-data-fundamentals written_at=2026-11-05T17:11:57.209793+00:00 -->
<!-- ai:end -->

---
[[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/02 - Data Modeling|Data Modeling]] →
