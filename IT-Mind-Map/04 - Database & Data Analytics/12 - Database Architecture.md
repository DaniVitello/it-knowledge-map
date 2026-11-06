---
title: "Database Architecture"
area: "Database / Data Analytics"
numero: 12
aliases: ["Database Architecture"]
tags: [concepto, it/database-data-analytics]
---
# Database Architecture

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 12 de 25**

## Qué abarca
- Storage engine
- query engine
- connections

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la arquitectura de base de datos para organizar cómo se almacenan, procesan y acceden los datos en los sistemas que gestiono. Resuelvo problemas de rendimiento y escalabilidad al separar la capa de almacenamiento físico (storage engine) de la capa de interpretación de consultas (query engine) y de la gestión de conexiones de clientes. Aparece en mi día a día cuando diseño esquemas, optimizo consultas y configuro clústeres de datos. Después de entenderla puedo elegir el motor adecuado, ajustar índices y dimensionar recursos. No necesito preocuparme cuando trabajo con bases de datos embebidas de un solo proceso o con consultas triviales que no superan los límites de la configuración por defecto.

## Esqueleto (el 20% esencial)
1. **Storage engine** – administra la persistencia física de tablas, índices y transacciones.  
2. **Query engine** – interpreta y ejecuta sentencias SQL o de otro lenguaje, generando planes de ejecución.  
3. **Connections** – controla la apertura, autenticación y multiplexado de sesiones de cliente.  
4. **Separación de responsabilidades** – permite escalar cada capa de forma independiente.  
5. **Compatibilidad con tipos de bases** – la arquitectura se adapta tanto a bases relacionales como a NoSQL.

## Como funciona
1. Un cliente abre una **connection** y se autentica.  
2. La **query engine** recibe la sentencia, la analiza y elige un plan óptimo usando metadatos y **indexes**.  
3. El plan se envía al **storage engine**, que localiza los bloques de datos en disco o en memoria y aplica los algoritmos de acceso (B‑Tree, LSM, etc.).  
4. Los resultados se devuelven a través de la **connection** al cliente.  
5. Cada capa puede estar distribuida: el storage engine en nodos de almacenamiento, el query engine en servidores de cómputo y el gestor de connections en un proxy o load balancer.

## Detalles
- **Básico**: Entender que la arquitectura separa *persistencia* (storage) de *cómputo* (query) y de *acceso* (connections).  
- **Intermedio**: Configurar parámetros del storage engine (p. ej., innodb_buffer_pool_size) y del query engine (p. ej., optimizer_switch) para mejorar latencia.  
- **Avanzado**: Desplegar arquitectura distribuida, usando sharding o replicación; integrar un pool de connections y un router de consultas para balancear carga entre varios motores (relacionales y NoSQL).  

## Ejemplo minimo
```sql
-- 1. Abrir conexión (implícita en la herramienta cliente)
-- 2. Ejecutar consulta simple
SELECT name, total_sales
FROM sales
WHERE sale_date >= '2024-01-01'
ORDER BY total_sales DESC
LIMIT 5;
```
El motor de consultas genera un plan que usa el índice `idx_sale_date`, el storage engine lee los bloques correspondientes y la conexión devuelve las filas al cliente.

## Errores comunes
- **Confundir storage engine con query engine** – evitar asignar tareas de optimización de consultas al motor de almacenamiento.  
- **No dimensionar el pool de connections** – puede saturar el servidor; ajustar `max_connections` según carga esperada.  
- **Ignorar la afinidad entre índices y storage engine** – crear índices que el motor no soporta reduce el rendimiento; usar tipos de índice compatibles.

## Estado actual
- **Fundamentos estables**: la separación de storage engine, query engine y connections sigue siendo la base de sistemas como MySQL, PostgreSQL y MongoDB.  
- **Práctica moderna**: se combinan motores híbridos (p. ej., PostgreSQL con extensiones de columnar), se emplean proxies de connections (p. ej., PgBouncer) y se orquestan clústeres de storage mediante soluciones de nube (p. ej., Amazon Aurora, Google Cloud Spanner).

## Conexiones
- **Bases de datos** – la arquitectura define cómo cualquier base de datos expone sus datos al usuario.  
- **Relational Databases** – utilizan storage y query engines especializados para ejecutar SQL y mantener ACID.  
- **NoSQL** – adapta la arquitectura para modelos de datos flexibles, a menudo con un query engine menos complejo pero con storage engine optimizado para escrituras masivas.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de sistemas operativos (memoria y disco) y redes (sockets).  
2. **Fundamentos**: estudiar storage engines (InnoDB, RocksDB) y query optimizers (cost‑based).  
3. **Práctica**: configurar pools de connections, analizar planes de ejecución con `EXPLAIN`.  
4. **Avanzado**: implementar sharding, replicación y usar proxies de connections; comparar arquitecturas relacionales vs NoSQL.  

## Preguntas de repaso
1. ¿Qué papel juega el storage engine en la latencia de una consulta?  
2. ¿Cómo afecta el pool de connections al número máximo de usuarios concurrentes?  
3. ¿Por qué es importante que el query engine conozca los índices disponibles?  
4. ¿En qué situaciones elegirías una arquitectura híbrida que combine motores relacionales y NoSQL?  
5. ¿Qué pasos seguirías para diagnosticar un cuello de botella en la capa de storage?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-12-database-architecture written_at=2026-11-05T22:57:47.793512+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/11 - Bases de datos|Bases de datos]] · *Backend*
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]]
- [[04 - Database & Data Analytics/09 - Indexes|Indexes]]
- [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]]

---
← [[04 - Database & Data Analytics/11 - ACID & Isolation|ACID & Isolation]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]] →
