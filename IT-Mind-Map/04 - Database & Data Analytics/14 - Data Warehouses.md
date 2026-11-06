---
title: "Data Warehouses"
area: "Database / Data Analytics"
numero: 14
aliases: ["Data Warehouses"]
tags: [concepto, it/database-data-analytics]
---
# Data Warehouses

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 14 de 25**

## Qué abarca
- Sistemas optimizados para análisis

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo un Data Warehouse para consolidar datos procedentes de múltiples fuentes operacionales y transformarlos en un entorno optimizado para consultas analíticas de gran escala. Resuelvo el problema de ejecutar reportes y análisis de tendencias sin afectar los sistemas de producción (OLTP). En mi día a día como ingeniero de datos, el Data Warehouse me permite diseñar modelos dimensionales, crear métricas históricas y ofrecer a los analistas un acceso rápido a información agregada. Después de comprender su arquitectura, puedo planificar pipelines de carga, definir esquemas de hechos y dimensiones, y evaluar cuándo una solución de análisis en tiempo real (por ejemplo, un lakehouse) es más adecuada. No necesito preocuparme por el Data Warehouse cuando solo realizo transformaciones ligeras o consultas ad‑hoc sobre datos operacionales.

## Esqueleto (el 20% esencial)
1. **Modelo dimensional**: hechos (medidas) y dimensiones (contexto) organizados en esquemas estrella o copo de nieve.  
2. **Separación OLTP/OLAP**: los datos de transacciones se extraen, transforman y cargan (ETL/ELT) en un repositorio especializado para consultas analíticas.  
3. **Optimización de consultas**: uso de particiones, índices column‑store y agregados pre‑calculados para acelerar lecturas masivas.  
4. **Data Pipelines**: flujos automatizados que alimentan el warehouse de forma periódica o continua.  

## Como funciona
1. **Extracción**: los sistemas OLTP exportan datos (p. ej., tablas de ventas).  
2. **Transformación**: se limpian, se unen y se convierten a formatos dimensionales (creación de claves surrogate, normalización de atributos).  
3. **Carga**: los datos transformados se insertan en tablas de hechos y dimensiones del warehouse.  
4. **Indexación y agregación**: se crean índices column‑store y vistas materializadas según los patrones de consulta.  
5. **Consulta**: los analistas ejecutan consultas OLAP que aprovechan la estructura dimensional y los índices para obtener resultados en segundos.

## Detalles
- **Básico**: definición de hechos (p. ej., `sales_amount`) y dimensiones (p. ej., `date_dim`, `product_dim`).  
- **Intermedio**: diseño de particiones por rango de tiempo, uso de `DISTKEY`/`SORTKEY` en Redshift o `CLUSTERED COLUMNSTORE INDEX` en SQL Server.  
- **Avanzado**: implementación de ELT con herramientas como dbt, generación de cubos de agregación y uso de materialized views para métricas de alta frecuencia.

## Ejemplo minimo
```sql
-- Dimensión producto
CREATE TABLE dim_product (
    product_key   INT IDENTITY PRIMARY KEY,
    product_id    VARCHAR(20) NOT NULL,
    product_name  VARCHAR(100),
    category      VARCHAR(50)
);

-- Tabla de hechos ventas
CREATE TABLE fact_sales (
    sales_key     INT IDENTITY PRIMARY KEY,
    product_key   INT NOT NULL,
    sales_date    DATE NOT NULL,
    quantity      INT,
    sales_amount  DECIMAL(12,2),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
);

-- Consulta analítica simple
SELECT d.category,
       SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product d ON f.product_key = d.product_key
WHERE f.sales_date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY d.category;
```

## Errores comunes
- **Cargar datos transaccionales directamente**: genera consultas lentas; evitarlo definiendo esquemas dimensionales.  
- **No crear claves surrogate**: dificulta la gestión de cambios lentos; usar claves artificiales en dimensiones.  
- **Olvidar particionar por fecha**: provoca escaneos completos; aplicar particiones basadas en la columna de tiempo más consultada.

## Estado actual
- **Fundamentos estables**: modelo dimensional, proceso ETL/ELT y separación OLTP/OLAP siguen siendo la base de los warehouses tradicionales.  
- **Práctica moderna**: adopción de cloud warehouses (Snowflake, BigQuery, Redshift) con arquitectura ELT, uso de dbt para transformación declarativa y soporte nativo de semi‑estructurados (JSON, Parquet) dentro del mismo repositorio.

## Conexiones
- **OLTP vs OLAP**: el Data Warehouse constituye el lado OLAP, mientras que los sistemas transaccionales (OLTP) alimentan sus datos.  
- **ETL / ELT**: los pipelines que extraen, transforman y cargan datos son la columna vertebral que llena el warehouse.  
- **Data Pipelines**: orquestadores como Airflow o Prefect gestionan la periodicidad y la fiabilidad de la carga del warehouse.

## Ruta de estudio
1. **Prerequisitos**: SQL avanzado, conceptos de modelado relacional y fundamentos de bases de datos OLTP.  
2. **Fundamentos**: estudiar esquemas estrella y copo de nieve, práctica con tablas de hechos y dimensiones.  
3. **Herramientas ETL/ELT**: aprender a usar dbt, Apache Airflow o Azure Data Factory para mover datos.  
4. **Optimización**: profundizar en índices column‑store, particionamiento y materialized views en un warehouse cloud.  
5. **Especialización**: explorar funcionalidades específicas de Snowflake (Zero‑Copy Cloning), BigQuery (partitioned tables) o Redshift (Concurrency Scaling).  

## Preguntas de repaso
1. ¿Cuál es la diferencia funcional entre una tabla de hechos y una tabla de dimensiones en un Data Warehouse?  
2. ¿Por qué es importante separar los sistemas OLTP y OLAP al diseñar una arquitectura de datos?  
3. ¿Qué ventaja ofrece el uso de claves surrogate en las dimensiones?  
4. ¿Cómo ayuda la partición por rango de tiempo a mejorar el rendimiento de consultas analíticas?  
5. ¿Qué rol juega una herramienta como dbt dentro del proceso ELT para un Data Warehouse?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-14-data-warehouses written_at=2026-11-05T22:59:21.486091+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/15 - OLTP vs OLAP|OLTP vs OLAP]]
- [[04 - Database & Data Analytics/16 - ETL - ELT|ETL / ELT]]
- [[04 - Database & Data Analytics/17 - Data Pipelines|Data Pipelines]]

---
← [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/15 - OLTP vs OLAP|OLTP vs OLAP]] →
