---
title: "OLTP vs OLAP"
area: "Database / Data Analytics"
numero: 15
aliases: ["OLTP vs OLAP"]
tags: [concepto, it/database-data-analytics]
---
# OLTP vs OLAP

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 15 de 25**

## Qué abarca
- Operaciones transaccionales vs analíticas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la distinción entre OLTP y OLAP para decidir cómo estructurar y consultar los datos que manejo a diario. Resuelvo el problema de mezclar cargas de trabajo transaccionales (alta concurrencia, escrituras rápidas) con análisis de gran volumen (consultas complejas, agregaciones). En mi rol de ingeniero de datos, aplico OLTP al diseñar bases operacionales que soportan aplicaciones de negocio y OLAP al construir almacenes de datos donde los analistas generan reportes y modelos predictivos. Después de comprender esta separación, puedo definir esquemas, elegir tecnologías y planificar pipelines de carga sin que una carga degrade a la otra. Cuando solo trabajo con datos de referencia estáticos o con consultas triviales, no es necesario preocuparse por la separación OLTP/OLAP.

## Esqueleto (el 20% esencial)
1. **OLTP**: sistemas optimizados para transacciones rápidas, consistencia inmediata y alta concurrencia.  
2. **OLAP**: entornos diseñados para consultas analíticas, agregaciones y exploración de historiales.  
3. **Separación de cargas**: mantener bases operacionales y de análisis independientes evita cuellos de botella.  
4. **Modelo de datos distinto**: OLTP usa esquemas normalizados; OLAP emplea esquemas dimensionales (estrella, copo de nieve).  

## Como funciona
1. **Ingreso de datos**: la aplicación escribe en la base OLTP (INSERT/UPDATE) garantizando ACID.  
2. **Extracción**: un proceso ETL/ELT copia los cambios a un staging area.  
3. **Transformación**: los datos se desnormalizan y se organizan en tablas de hechos y dimensiones.  
4. **Carga**: el resultado se inserta en el almacén OLAP.  
5. **Consulta analítica**: los analistas ejecutan SELECT con GROUP BY, WINDOW y funciones de agregación contra OLAP, sin impactar la latencia de OLTP.

## Detalles
- **Básico**: distinguir los tipos de consultas (transaccional vs analítica) y elegir la base adecuada.  
- **Intermedio**: diseñar esquemas; normalización para OLTP, modelado dimensional para OLAP; definir índices de inserción vs índices de lectura.  
- **Avanzado**: implementar replicación en tiempo real (CDC), particionar tablas de hechos, usar materialized views y columnar storage para acelerar OLAP, y aplicar políticas de retención de datos en OLTP.

## Ejemplo minimo
```sql
-- OLTP: tabla de órdenes operacionales
CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    client_id  INTEGER,
    amount     NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (client_id, amount) VALUES (101, 250.00);

-- OLAP: tabla de hechos desnormalizada (copia simplificada)
CREATE TABLE fact_orders (
    order_id   INTEGER,
    client_id  INTEGER,
    amount     NUMERIC,
    year_month TEXT
);

INSERT INTO fact_orders
SELECT order_id, client_id, amount,
       strftime('%Y-%m', created_at) AS year_month
FROM orders;

-- Consulta analítica en OLAP
SELECT year_month, SUM(amount) AS total_sales
FROM fact_orders
GROUP BY year_month
ORDER BY year_month;
```

## Errores comunes
- **Usar la misma base para OLTP y OLAP** → la carga analítica degrada la respuesta transaccional; evitarlo separando los sistemas.  
- **Normalizar excesivamente en OLAP** → dificulta agregaciones; usar esquemas dimensionales.  
- **Olvidar la captura de cambios (CDC)** → los datos analíticos quedan desactualizados; implementar procesos de extracción incremental.

## Estado actual
- **Fundamentos estables**: la separación OLTP/OLAP, los principios de ACID para transacciones y los modelos dimensionales para análisis siguen siendo la base.  
- **Práctica moderna**: se adopta la arquitectura Lambda o Kappa con streaming CDC, almacenes columnar en la nube (Snowflake, BigQuery) y materialized views para reducir la latencia entre OLTP y OLAP.

## Conexiones
- **Data Warehouse**: el almacén OLAP es la pieza central del Data Warehouse, donde se consolidan los datos para reporting.  
- **ETL / ELT**: estos procesos trasladan y transforman datos desde OLTP hacia OLAP, habilitando la separación de cargas.  
- **Data Pipelines**: orquestan la extracción continua (CDC) y la carga incremental, manteniendo sincronizados los entornos transaccional y analítico.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de transacciones y normalización.  
2. **Fundamentos**: estudiar diferencias de workload, modelos de datos OLTP vs OLAP y principios de ACID vs BASE.  
3. **Intermedio**: aprender modelado dimensional (estrella, copo de nieve) y diseñar pipelines ETL/ELT simples.  
4. **Avanzado**: profundizar en CDC, streaming de datos, almacenes columnar y optimizaciones de consultas analíticas.  
5. **Especialización**: explorar herramientas específicas (Snowflake, Redshift, Apache Flink) y patrones de arquitectura Lambda/Kappa.

## Preguntas de repaso
1. ¿Qué característica de rendimiento distingue a un sistema OLTP de uno OLAP?  
2. ¿Por qué es problemático ejecutar consultas agregadas complejas directamente sobre una base OLTP?  
3. ¿Cuál es la diferencia principal entre un esquema normalizado y uno dimensional?  
4. ¿Cómo ayuda un proceso CDC a mantener actualizado un almacén OLAP?  
5. ¿Qué tipo de índice es más apropiado en una tabla de hechos de un Data Warehouse?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-15-oltp-vs-olap written_at=2026-11-05T23:00:13.658503+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/14 - Data Warehouses|Data Warehouses]]
- [[04 - Database & Data Analytics/16 - ETL - ELT|ETL / ELT]]
- [[04 - Database & Data Analytics/17 - Data Pipelines|Data Pipelines]]

---
← [[04 - Database & Data Analytics/14 - Data Warehouses|Data Warehouses]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/16 - ETL - ELT|ETL / ELT]] →
