---
title: "Advanced Data Architecture"
area: "Database / Data Analytics"
numero: 25
aliases: ["Advanced Data Architecture"]
tags: [concepto, it/database-data-analytics]
---
# Advanced Data Architecture

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 25 de 25**

## Qué abarca
- Lakehouse
- streaming
- distributed systems
- governance

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la Advanced Data Architecture para diseñar entornos donde datos estructurados y no estructurados conviven en una única capa accesible, lo que me permite ejecutar consultas analíticas y pipelines de streaming sin mover datos entre sistemas aislados. Resuelvo la fragmentación de datos que surge al combinar almacenes de datos tradicionales, lagos de datos y flujos en tiempo real, y así garantizo que los analistas y científicos de datos obtengan información consistente y oportuna. En mi día a día como ingeniero de datos, esta arquitectura aparece al definir la capa de Lakehouse que soporta tanto batch como streaming, aplicando políticas de governance para controlar el acceso y la calidad. Después de entenderla, puedo diseñar pipelines end‑to‑end, optimizar costos de almacenamiento y habilitar auto‑servicio de datos. Cuando los requerimientos son simples (solo un data warehouse o un data lake aislado) no es necesario adoptar una arquitectura avanzada.

## Esqueleto (el 20% esencial)
1. **Lakehouse** – combina la flexibilidad del data lake con la consistencia y el rendimiento de un data warehouse.  
2. **Streaming** – permite ingerir y procesar datos en tiempo real dentro de la misma capa de almacenamiento.  
3. **Distributed systems** – garantiza escalabilidad y tolerancia a fallos mediante nodos coordinados.  
4. **Governance** – define políticas de seguridad, calidad y linaje que se aplican de forma uniforme.  

## Como funciona
1. Se crea un **Lakehouse** sobre un storage distribuido (por ejemplo, S3 o ADLS) que soporta formatos transaccionales (Delta, Iceberg).  
2. Los **streams** de eventos (Kafka, Kinesis) se conectan directamente al Lakehouse mediante lecturas continuas, evitando la duplicación de datos.  
3. El motor de procesamiento (Spark, Flink) ejecuta consultas tanto batch como streaming sobre los mismos archivos, aprovechando la **distribución** de cómputo.  
4. Las capas de **governance** interceptan cada operación, aplicando control de acceso y validaciones de calidad antes de que los datos se materialicen.  

## Detalles
- **Básico**: Configurar un storage distribuido y habilitar un formato transaccional que soporte ACID.  
- **Intermedio**: Integrar un motor de streaming que lea directamente del storage y escriba en tablas Delta, manteniendo versiones.  
- **Avanzado**: Implementar políticas de governance automáticas (catalogos, etiquetas, linaje) y orquestar pipelines con herramientas como Airflow o Dagster, asegurando consistencia entre batch y streaming.  

## Ejemplo minimo
```python
# Spark 3.x + Delta Lake: crear una tabla Lakehouse y consumir un stream de Kafka
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("LakehouseDemo") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 1. Definir tabla Delta (Lakehouse)
spark.sql("""
CREATE TABLE IF NOT EXISTS sales
USING DELTA
LOCATION 's3://my-bucket/lakehouse/sales'
""")

# 2. Leer stream de Kafka y escribir en la tabla
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "sales_topic") \
    .load()

sales_df = kafka_stream.selectExpr("CAST(value AS STRING) as json") \
    .selectExpr("json_tuple(json, 'order_id','amount','ts') as (order_id, amount, ts)")

query = sales_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/checkpoints/sales") \
    .table("sales")

query.awaitTermination()
```

## Errores comunes
- **Ignorar el versionado**: escribir datos sin habilitar el formato transaccional genera inconsistencias; habilitar Delta/Iceberg evita el problema.  
- **Mezclar esquemas**: permitir que diferentes streams escriban con estructuras distintas rompe la consistencia; usar esquemas evolutivos controlados.  
- **Olvidar la governance**: no aplicar políticas de acceso lleva a brechas de seguridad; integrar el catalogo de metadatos desde el inicio.  

## Estado actual
- **Fundamentos estables**: uso de storage distribuido (S3, ADLS), formatos transaccionales (Delta, Iceberg) y motores de procesamiento (Spark, Flink).  
- **Práctica moderna**: integración nativa de streaming en Lakehouse, políticas de governance automatizadas mediante Unity Catalog o Hive Metastore, y orquestación de pipelines con herramientas de CI/CD para datos.  

## Conexiones
- **Distributed Systems**: la arquitectura se apoya en la capacidad de los sistemas distribuidos para escalar el cómputo y el almacenamiento de forma horizontal.  
- **Mensajería**: los sistemas de mensajería (Kafka, Kinesis) alimentan los pipelines de streaming que se consumen directamente en el Lakehouse.  
- **Sistemas distribuidos**: la consistencia y tolerancia a fallos del Lakehouse dependen de los algoritmos de consenso y replicación propios de los sistemas distribuidos.  

## Ruta de estudio
1. **Prerequisitos**: fundamentos de SQL, conceptos de data lake y data warehouse, y nociones básicas de sistemas distribuidos.  
2. **Fundamentos**: aprender Delta Lake o Iceberg, practicar lecturas/escrituras batch con Spark.  
3. **Streaming**: integrar Kafka con Spark Structured Streaming y escribir en tablas Delta.  
4. **Governance**: explorar Unity Catalog, etiquetas de calidad y linaje de datos.  
5. **Orquestación**: diseñar pipelines completos con Airflow/Dagster y aplicar CI/CD para despliegues de esquemas.  

## Preguntas de repaso
1. ¿Cómo el Lakehouse combina las ventajas de un data lake y un data warehouse?  
2. ¿Qué papel juega el versionado de archivos (Delta/Iceberg) en la consistencia de datos?  
3. ¿De qué manera un motor de streaming puede escribir directamente en una tabla Delta sin pasos intermedios?  
4. ¿Cuál es la función de la governance en una arquitectura avanzada de datos?  
5. ¿Qué riesgos aparecen al mezclar esquemas diferentes en streams que alimentan la misma tabla del Lakehouse?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-25-advanced-data-architecture written_at=2026-11-05T23:08:52.074446+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/28 - Distributed Systems|Distributed Systems]] · *Software Engineering*
- [[03 - Backend/21 - Mensajería|Mensajería]] · *Backend*
- [[03 - Backend/25 - Sistemas distribuidos|Sistemas distribuidos]] · *Backend*

---
← [[04 - Database & Data Analytics/24 - BI & Reporting|BI & Reporting]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]]
