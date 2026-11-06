---
title: "NoSQL"
area: "Database / Data Analytics"
numero: 13
aliases: ["NoSQL"]
tags: [concepto, it/database-data-analytics]
---
# NoSQL

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 13 de 25**

## Qué abarca
- Document
- key-value
- wide-column
- graph databases

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo bases de datos NoSQL cuando necesito almacenar y consultar datos que no encajan bien en tablas rígidas, como documentos JSON con esquemas variables, pares clave‑valor de alta velocidad, columnas anchas para series temporales o grafos de relaciones complejas. Resuelvo problemas de escalabilidad horizontal, latencia mínima y flexibilidad de modelo, que aparecen al diseñar pipelines de ingestión masiva, catálogos de eventos o análisis de redes sociales. Después de entender NoSQL puedo elegir la familia adecuada (document, key‑value, wide‑column o graph) y combinarla con herramientas de análisis como Spark o Power BI. No necesito preocuparme cuando los datos son perfectamente estructurados, las transacciones ACID son críticas y el volumen es bajo; en esos casos una base relacional sigue siendo la mejor opción.

## Esqueleto (el 20% esencial)
1. **Document databases** – almacenan documentos auto‑descriptivos (JSON/BSON) y permiten consultas por campos internos.  
2. **Key‑value stores** – pares simples de clave y valor, optimizados para lecturas/escrituras ultra‑rápidas.  
3. **Wide‑column stores** – tablas con filas que pueden tener un número variable de columnas, ideales para series temporales y datos de gran ancho.  
4. **Graph databases** – representan nodos y aristas, facilitando consultas de caminos y vecindades en redes.  

## Como funciona
1. **Selección del modelo** según la forma del dato y el patrón de acceso (ej. documentos para datos semi‑estructurados).  
2. **Definición del esquema lógico** (opcional en documentos y key‑value, obligatorio en wide‑column).  
3. **Creación de la colección/tablas** en el motor NoSQL elegido.  
4. **Inserción de datos** mediante APIs específicas (REST, drivers).  
5. **Consulta** usando lenguajes propios (MongoDB Query Language, CQL, Gremlin) que aprovechan índices internos.  
6. **Escalado horizontal** añadiendo nodos al clúster; el motor redistribuye particiones automáticamente.

## Detalles
- **Básico:** entender que NoSQL sacrifica algunas garantías ACID a cambio de rendimiento y flexibilidad.  
- **Intermedio:** diseñar índices secundarios, modelar relaciones embebidas vs referencias, y configurar réplicas para alta disponibilidad.  
- **Avanzado:** aplicar particionamiento (sharding) fino, usar transacciones multi‑documento cuando el motor lo permite, y combinar NoSQL con pipelines de procesamiento (e.g., Spark Structured Streaming) para análisis en tiempo real.

## Ejemplo minimo
```python
# Inserción en MongoDB (document database)
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["analytics"]
col = db["events"]

col.insert_one({"user_id": 123, "action": "click", "ts": "2026-11-05T12:00:00Z"})
print(col.find_one({"user_id": 123}))
```

## Errores comunes
- **Usar NoSQL para transacciones financieras críticas** → perder consistencia; prefiera RDBMS.  
- **Ignorar el diseño de índices** → consultas lentas; analice patrones de acceso antes de crear índices.  
- **Sobredimensionar la flexibilidad del esquema** → datos desordenados y difíciles de validar; mantenga convenciones de campo.

## Estado actual
- **Fundamentos estables:** los cuatro tipos de bases NoSQL (document, key‑value, wide‑column, graph) y sus APIs de consulta.  
- **Práctica moderna:** integración con arquitecturas de datos en tiempo real, uso de contenedores/Kubernetes para despliegues escalables y adopción de modelos híbridos (poliglot persistence) en pipelines de datos.

## Conexiones
- **Relational Databases** – a menudo coexisten en una arquitectura poliglota, delegando a NoSQL las cargas de alta velocidad y flexibilidad.  
- **Database Architecture** – NoSQL influye en decisiones de particionamiento, replicación y consistencia dentro del diseño global del sistema.  
- **Vector Databases** – comparten el enfoque de almacenar datos no tabulares y se combinan con NoSQL para búsquedas semánticas basadas en embeddings.

## Ruta de estudio
1. **Prerequisitos:** SQL básico, conceptos de modelo de datos y programación en Python/Java.  
2. **Fundamentos:** tutoriales oficiales de MongoDB, Redis y Cassandra; ejercicios de inserción y consulta.  
3. **Intermedio:** diseño de índices, sharding y replicación; casos de uso de grafos con Neo4j.  
4. **Avanzado:** integración con Spark, patrones de poliglot persistence, pruebas de consistencia bajo carga.

## Preguntas de repaso
1. ¿En qué situaciones elegirías una base de datos document sobre una key‑value?  
2. ¿Cómo afecta el modelo de particionamiento a la latencia de lectura en un wide‑column store?  
3. ¿Qué limitaciones de consistencia tiene una base de datos graph típica?  
4. ¿Cuál es el impacto de no crear índices secundarios en una colección de MongoDB con millones de documentos?  
5. ¿Cómo combinarías una base NoSQL con una herramienta de análisis en tiempo real como Spark?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-13-nosql written_at=2026-11-05T22:58:17.905487+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/11 - Bases de datos|Bases de datos]] · *Backend*
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]]
- [[04 - Database & Data Analytics/12 - Database Architecture|Database Architecture]]
- [[07 - AI Engineering/09 - Embeddings|Embeddings]] · *AI Engineering*
- [[07 - AI Engineering/15 - Vector Databases|Vector Databases]] · *AI Engineering*

---
← [[04 - Database & Data Analytics/12 - Database Architecture|Database Architecture]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/14 - Data Warehouses|Data Warehouses]] →
