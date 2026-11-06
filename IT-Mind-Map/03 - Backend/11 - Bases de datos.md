---
title: "Bases de datos"
area: "Backend"
numero: 11
aliases: ["Bases de datos"]
tags: [concepto, it/backend]
---
# Bases de datos

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 11 de 25**

## Qué abarca
- Persistencia
- tablas
- documentos
- relaciones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo bases de datos para guardar de forma duradera la información que mis servicios y APIs necesitan leer y escribir. Resuelvo el problema de la pérdida de estado entre peticiones y de la concurrencia segura cuando varios procesos acceden a los mismos datos. Aparecen en cada endpoint que necesita crear, consultar, actualizar o eliminar recursos, y en los procesos batch que sincronizan información externa. Después de entenderlas puedo diseñar esquemas que reduzcan la latencia y el coste de operación, elegir el motor adecuado (relacional o NoSQL) y aplicar patrones de consistencia. No necesito preocuparme cuando el servicio es puramente computacional y no maneja datos persistentes.

## Esqueleto (el 20% esencial)
1. **Persistencia** – los datos sobreviven al ciclo de vida de la aplicación y a reinicios del servidor.  
2. **Tablas y documentos** – estructuras de almacenamiento; tablas para modelos relacionales, documentos para modelos orientados a JSON.  
3. **Relaciones** – enlaces entre entidades que permiten consultas conjuntas y garantizan integridad referencial.  
4. **Índices** – estructuras auxiliares que aceleran búsquedas y filtrados frecuentes.  
5. **Arquitectura de base de datos** – elección entre un motor único, clústeres o servicios gestionados según requisitos de escalabilidad y disponibilidad.

## Como funciona
1. Defino el modelo de datos (tablas o colecciones) según los objetos del dominio.  
2. Creo la estructura física (DDL) y los índices que soportarán los filtros más usados.  
3. Cada petición del API ejecuta una operación CRUD contra la base mediante un driver o ORM.  
4. El motor gestiona transacciones o versiones de documentos para asegurar consistencia.  
5. Los resultados se devuelven al controlador, que los serializa y los envía al cliente.

## Detalles
- **Básico**: conexión, creación de tablas/colecciones, operaciones CRUD simples.  
- **Intermedio**: uso de transacciones, manejo de claves foráneas, diseño de índices compuestos y consultas parametrizadas.  
- **Avanzado**: sharding, replicación, tuning de rendimiento, patrones de eventual consistency y event sourcing.

## Ejemplo minimo
```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO users (name) VALUES ('Ana')")
conn.commit()

cur.execute("SELECT * FROM users WHERE name = ?", ("Ana",))
print(cur.fetchone())   # (1, 'Ana')
conn.close()
```

## Errores comunes
- **Olvidar índices** en columnas usadas en filtros → consultas lentas; crear índices antes de medir rendimiento.  
- **Usar tipos de datos incorrectos** (e.g., almacenar fechas como texto) → errores de ordenación; definir tipos adecuados en el esquema.  
- **Ignorar transacciones** en operaciones que deben ser atómicas → datos inconsistentes; envolver en `BEGIN…COMMIT`.  

## Estado actual
- **Fundamentos estables**: modelo relacional, operaciones CRUD, índices B‑Tree, ACID.  
- **Práctica moderna**: adopción de bases de datos distribuidas, uso de ORMs con soporte para migraciones automáticas, integración de observabilidad (metrics, tracing) en consultas, y despliegues de bases como servicio (DBaaS) que abstraen la gestión de clústeres.

## Conexiones
- **Relational Databases**: comparten el concepto de tablas y claves foráneas; la elección entre un motor relacional y otro depende de los requisitos de consistencia.  
- **Indexes**: son esenciales para que las consultas de API sean rápidas; su diseño está directamente ligado al modelo de datos.  
- **NoSQL**: ofrece colecciones de documentos cuando la flexibilidad del esquema supera la necesidad de relaciones estrictas.

## Ruta de estudio
1. **Prerequisitos**: conocimientos de SQL básico, estructuras de datos y conceptos de HTTP/REST.  
2. **Fundamentos**: practicar CRUD con SQLite o PostgreSQL, crear índices y entender transacciones.  
3. **Intermedio**: aprender sobre claves foráneas, normalización y patrones de acceso (Repository, Unit of Work).  
4. **Avanzado**: estudiar replicación, sharding, tuning de consultas, y comparar motores relacionales vs NoSQL según casos de uso.  
5. **Especialización**: profundizar en observabilidad de bases de datos y en herramientas de migración (Flyway, Liquibase).

## Preguntas de repaso
1. ¿Por qué es importante crear índices en columnas que aparecen en filtros de consultas API?  
2. ¿Cómo garantiza una transacción la atomicidad de varias operaciones CRUD?  
3. ¿En qué situaciones elegirías una base de datos de documentos sobre una relacional?  
4. ¿Qué diferencia hay entre consistencia fuerte y eventual en el contexto de replicación?  
5. ¿Cuál es el efecto de un esquema mal normalizado sobre el rendimiento y la integridad de los datos?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-11-bases-de-datos written_at=2026-11-05T19:45:15.698614+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/09 - Indexes|Indexes]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/12 - Database Architecture|Database Architecture]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]] · *Database / Data Analytics*

---
← [[03 - Backend/10 - Arquitectura de aplicaciones|Arquitectura de aplicaciones]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/12 - SQL|SQL]] →
