---
title: "Data Pipelines"
area: "Database / Data Analytics"
numero: 17
aliases: ["Data Pipelines"]
tags: [concepto, it/database-data-analytics]
---
# Data Pipelines

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 17 de 25**

## Qué abarca
- Ingesta
- transformación y movimiento de datos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los data pipelines para mover datos desde su origen hasta los entornos donde se analizan o se sirven a aplicaciones, garantizando que la información sea consistente, limpia y esté disponible en el momento necesario. Resuelvo el problema de la fragmentación de datos, evitando que los analistas tengan que extraer y transformar manualmente cada fuente. En mi día a día como ingeniero de datos, los pipelines aparecen cada vez que incorporo nuevos sistemas transaccionales, actualizo un data warehouse o preparo datos para modelos de machine‑learning. Después de comprenderlos, puedo diseñar arquitecturas escalables, automatizar la calidad de los datos y reducir el tiempo de entrega de insights. Cuando los datos ya están en un repositorio estable y las transformaciones son estáticas, no necesito preocuparme por construir un pipeline nuevo.

## Esqueleto (el 20% esencial)
1. **Ingesta** – captura de datos crudos desde bases OLTP, APIs o archivos.  
2. **Transformación** – limpieza, normalización y enriquecimiento para que los datos cumplan los requisitos analíticos.  
3. **Movimiento** – carga de los datos transformados a destinos como data warehouses, lagos de datos o sistemas de visualización.  
4. **Orquestación** – coordinación de los pasos anteriores mediante programación o herramientas de workflow.  
5. **Monitoreo** – detección automática de fallos y métricas de calidad.

## Como funciona
1. El pipeline inicia con la **ingesta**, donde un conector (por ejemplo, un driver JDBC) extrae filas de una tabla OLTP.  
2. Los datos crudos pasan al módulo de **transformación**, donde se aplican reglas de validación, se convierten tipos y se unen con catálogos de referencia.  
3. Una vez transformados, el motor de **movimiento** escribe los resultados en el data warehouse mediante una operación bulk‑insert.  
4. La **orquestación** programa la ejecución (por ejemplo, con Apache Airflow) y asegura que cada tarea se ejecute en el orden correcto.  
5. El **monitoreo** registra tiempos de ejecución y alertas; si una tarea falla, el workflow la reintenta o notifica al equipo.

## Detalles
- **Básico**: pipelines de una sola fase (ingesta → carga) usando scripts SQL o bash.  
- **Intermedio**: introducción de transformaciones ligeras con herramientas como dbt o pandas; uso de colas (Kafka) para ingestión en tiempo real.  
- **Avanzado**: arquitectura de micro‑servicios con streaming (Spark Structured Streaming), separación clara entre ETL (extract‑transform‑load) y ELT (load‑then‑transform), y despliegue continuo mediante CI/CD.

## Ejemplo minimo
```python
import pandas as pd
from sqlalchemy import create_engine

# 1. Ingesta: leer tabla OLTP
engine_src = create_engine('postgresql://user:pwd@src-db:5432/ventas')
df_raw = pd.read_sql('SELECT * FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL \'1 day\'', engine_src)

# 2. Transformación: eliminar columnas innecesarias y convertir fechas
df_clean = df_raw.drop(columns=['temp_flag']).assign(order_date=pd.to_datetime(df_raw['order_date']))

# 3. Movimiento: cargar en data warehouse
engine_dw = create_engine('postgresql://user:pwd@dw-db:5432/analytics')
df_clean.to_sql('stg_orders', engine_dw, if_exists='replace', index=False)
```

## Errores comunes
- **Olvidar la deduplicación** → genera datos inflados; usar `drop_duplicates()` antes de cargar.  
- **No validar tipos** → errores de carga; aplicar `astype()` o esquemas explícitos.  
- **Ignorar la latencia de la fuente** → timeouts; implementar reintentos con back‑off.  
- **Desconectar el monitoreo** → fallos silenciosos; integrar alertas en la orquestación.

## Estado actual
- **Fundamentos estables**: los conceptos de ingesta, transformación y carga siguen siendo la base de cualquier pipeline; herramientas como Apache Airflow, dbt y Spark son ampliamente adoptadas.  
- **Práctica moderna**: se favorece ELT sobre ETL cuando el data warehouse soporta procesamiento masivo; los pipelines se construyen como código (IaC) y se despliegan con pipelines de CI/CD, mientras que el streaming en tiempo real (Kafka + Flink/Spark) complementa los lotes tradicionales.

## Conexiones
- **Data Warehouses**: los pipelines alimentan los almacenes estructurados donde se ejecutan consultas OLAP.  
- **ETL / ELT**: los pipelines son la implementación práctica de estos procesos, diferenciándose en el momento de la transformación.  
- **AI Workflows**: los datos preparados por pipelines sirven como entrada para modelos de machine‑learning, cerrando el ciclo de datos a insights.

## Ruta de estudio
1. **Prerequisitos**: SQL avanzado, modelado relacional y conceptos de bases OLTP/OLAP.  
2. **Fundamentos**: aprender un lenguaje de scripting (Python) y una herramienta de orquestación (Airflow).  
3. **Intermedio**: practicar con dbt para transformaciones declarativas y con Kafka para ingestión en tiempo real.  
4. **Avanzado**: dominar Spark Structured Streaming, diseñar pipelines como código (Terraform, Docker) y aplicar pruebas automatizadas (unit & integration) en CI/CD.

## Preguntas de repaso
1. ¿Qué pasos del esqueleto de un data pipeline garantizan la calidad de los datos antes de cargarlos?  
2. ¿En qué situaciones prefiero ELT en lugar de ETL?  
3. ¿Cómo se relaciona la orquestación con el monitoreo en un pipeline productivo?  
4. ¿Qué ventaja aporta usar un data warehouse como destino frente a almacenar los datos en archivos planos?  
5. ¿Cuál es el beneficio de integrar un pipeline de datos con un AI workflow?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-17-data-pipelines written_at=2026-11-05T23:02:00.701656+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/14 - Data Warehouses|Data Warehouses]]
- [[04 - Database & Data Analytics/15 - OLTP vs OLAP|OLTP vs OLAP]]
- [[04 - Database & Data Analytics/16 - ETL - ELT|ETL / ELT]]
- [[07 - AI Engineering/17 - AI Workflows|AI Workflows]] · *AI Engineering*

---
← [[04 - Database & Data Analytics/16 - ETL - ELT|ETL / ELT]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/18 - Data Quality|Data Quality]] →
