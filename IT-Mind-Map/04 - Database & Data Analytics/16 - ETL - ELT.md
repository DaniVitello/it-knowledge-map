---
title: "ETL / ELT"
area: "Database / Data Analytics"
numero: 16
aliases: ["ETL / ELT"]
tags: [concepto, it/database-data-analytics]
---
# ETL / ELT

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 16 de 25**

## Qué abarca
- Extract
- Transform
- Load

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo ETL/ELT para mover datos desde sistemas operacionales (OLTP) hacia entornos analíticos (OLAP) donde pueden ser consultados y visualizados. Resuelvo el problema de que los datos crudos no están listos para el análisis: los limpio, los unifico y los estructuro según el modelo del data warehouse. En mi día a día como ingeniero de datos, defino los pasos de extracción, transformación y carga, programo los pipelines y monitorizo su ejecución. Después de comprender ETL/ELT puedo diseñar flujos de datos robustos, elegir la estrategia (ETL o ELT) adecuada y optimizar el rendimiento de consultas analíticas. Cuando los datos ya están en un data lake con capacidad de procesamiento interno, no necesito preocuparme por una fase de carga separada.

## Esqueleto (el 20% esencial)
1. **Extract** – Obtener datos de fuentes heterogéneas (bases OLTP, APIs, archivos) manteniendo la integridad de la información.  
2. **Transform** – Aplicar reglas de limpieza, normalización, agregación y enriquecimiento para que los datos cumplan el modelo analítico.  
3. **Load** – Insertar los datos transformados en el destino (data warehouse, data lake) de forma eficiente y consistente.  
4. **Orquestación** – Coordinar la secuencia y la periodicidad de los pasos para garantizar que el pipeline se ejecute sin solapamientos.  
5. **Monitoreo** – Detectar fallos y desviaciones de calidad para reaccionar rápidamente.

## Como funciona
1. **Extracción**: el motor de pipeline abre conexiones a cada origen y copia los registros nuevos o modificados (CDC, snapshots).  
2. **Transformación**: los datos pasan por funciones de filtrado, tipado, deduplicación y cálculo de métricas; estas operaciones pueden ejecutarse en un motor de procesamiento intermedio (Spark, dbt).  
3. **Carga**: el resultado se escribe en tablas de destino mediante inserciones masivas o “upserts”, respetando claves primarias y particiones.  
4. **Orquestación**: un scheduler (Airflow, Prefect) dispara los jobs en el orden Extract → Transform → Load y controla dependencias.  
5. **Monitoreo**: logs y métricas de tiempo, filas procesadas y errores se envían a dashboards para su revisión.

## Detalles
- **Básico**: ETL tradicional con scripts SQL/Python que extraen de una tabla, aplican una única transformación y cargan a otra tabla.  
- **Intermedio**: uso de herramientas de transformación declarativa (dbt) que permiten versionar lógica y ejecutar pruebas de calidad entre Extract y Load.  
- **Avanzado**: ELT en la nube donde la transformación se realiza directamente en el data warehouse (Snowflake, BigQuery) usando SQL nativo; integración con streaming (Kafka) y con pipelines de IA que consumen los datos recién cargados.

## Ejemplo minimo
```python
# ETL mínimo con pandas y SQLite
import pandas as pd, sqlite3

# Extract
src = sqlite3.connect('oltp.db')
df = pd.read_sql('SELECT id, amount_usd FROM sales WHERE date >= "2024-01-01"', src)

# Transform
df['amount_eur'] = df['amount_usd'] * 0.92   # conversión simple
df = df.drop_duplicates(subset='id')

# Load
dst = sqlite3.connect('dw.db')
df.to_sql('sales_fact', dst, if_exists='replace', index=False)
```

## Errores comunes
- **Extraer datos sin control de cambios** → genera duplicados; usar CDC o marcas de tiempo.  
- **Transformar en el mismo motor de origen** → sobrecarga el OLTP; mover a un entorno intermedio o usar ELT.  
- **Cargar sin validar claves** → rompe la integridad referencial; aplicar constraints antes de la carga.  
- **Ignorar el orden de ejecución** → produce datos parciales; definir dependencias claras en la orquestación.  

## Estado actual
- **Fundamentos estables**: la separación lógica de Extract, Transform y Load sigue siendo la base para cualquier pipeline de datos.  
- **Práctica moderna**: la tendencia es ELT, donde la carga ocurre primero y la transformación se ejecuta en el data warehouse usando SQL escalable; además, los pipelines se gestionan con herramientas de orquestación basadas en contenedores y se integran con flujos de trabajo de IA que consumen los datos recién cargados.

## Conexiones
- **Data Warehouses**: son el destino típico de la fase Load y, en ELT, también el motor donde se realizan las Transformaciones.  
- **Data Pipelines**: ETL/ELT es la arquitectura subyacente que define cómo fluye la información a través de los pipelines.  
- **AI Workflows**: los datos preparados por ETL/ELT alimentan modelos de machine learning, cerrando el ciclo de datos desde la captura hasta la inferencia.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de bases OLTP/OLAP, manejo de Python o Scala.  
2. **Fundamentos**: tutoriales de ETL con scripts, ejercicios de CDC y pruebas de calidad de datos.  
3. **Herramientas intermedias**: aprender dbt para transformaciones declarativas y Airflow para orquestación.  
4. **Modernización**: profundizar en ELT con Snowflake/BigQuery, practicar cargas masivas y transformaciones en‑SQL.  
5. **Especialización**: integrar pipelines con Kafka (streaming) y con plataformas de ML (MLflow, Vertex AI) para crear AI Workflows completos.

## Preguntas de repaso
1. ¿Qué ventaja tiene mover la fase de Transformación al data warehouse en una arquitectura ELT?  
2. ¿Cómo evita el uso de CDC la generación de registros duplicados durante la extracción?  
3. ¿Cuál es el rol de la orquestación en un pipeline ETL y qué herramienta popular la implementa?  
4. En el ejemplo mínimo, ¿qué operación garantiza la unicidad de los registros antes de la carga?  
5. ¿Por qué es importante validar claves primarias antes de la fase Load?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-16-etl-elt written_at=2026-11-05T23:01:20.183387+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/14 - Data Warehouses|Data Warehouses]]
- [[04 - Database & Data Analytics/15 - OLTP vs OLAP|OLTP vs OLAP]]
- [[04 - Database & Data Analytics/17 - Data Pipelines|Data Pipelines]]
- [[07 - AI Engineering/17 - AI Workflows|AI Workflows]] · *AI Engineering*

---
← [[04 - Database & Data Analytics/15 - OLTP vs OLAP|OLTP vs OLAP]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/17 - Data Pipelines|Data Pipelines]] →
