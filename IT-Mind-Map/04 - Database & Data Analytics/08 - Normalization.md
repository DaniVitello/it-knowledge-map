---
title: "Normalization"
area: "Database / Data Analytics"
numero: 8
aliases: ["Normalization"]
tags: [concepto, it/database-data-analytics]
---
# Normalization

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 8 de 25**

## Qué abarca
- Reducción de redundancia y anomalías

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la normalización cuando diseño esquemas relacionales para garantizar que los datos se almacenen una sola vez y que las actualizaciones, inserciones y borrados no generen inconsistencias. Resuelvo problemas de redundancia y de anomalías de inserción, actualización y eliminación que aparecen al trabajar con grandes volúmenes de transacciones o al preparar datos para análisis. En mi día a día como ingeniero de datos, la normalización me permite crear modelos de datos claros, optimizar consultas y reducir el coste de almacenamiento. Después de dominarla, puedo pasar a diseñar modelos dimensionales para data warehouses o a aplicar técnicas de desnormalización controlada para mejorar el rendimiento de consultas analíticas. No es necesario preocuparse por ella cuando trabajo exclusivamente con fuentes de datos ya estructuradas en formato de tabla plana sin relaciones.

## Esqueleto (el 20% esencial)
1. **Eliminar redundancia**: Cada hecho se guarda en una sola tabla, evitando repeticiones que inflan el tamaño y generan inconsistencias.  
2. **Prevenir anomalías**: La normalización elimina anomalías de inserción, actualización y eliminación que aparecen en esquemas no estructurados.  
3. **Usar claves y restricciones**: Primary keys y foreign keys son los pilares que conectan las tablas normalizadas y garantizan la integridad referencial.  
4. **Aplicar formas normales**: Se avanza progresivamente desde 1NF a 3NF (y más allá) para lograr un equilibrio entre integridad y complejidad.  

## Como funciona
1. **Identifico atributos repetidos** en la tabla origen y los separo en una tabla nueva.  
2. **Asigno una primary key** a la tabla original y a la tabla nueva.  
3. **Establezco foreign keys** que enlazan los registros mediante la clave primaria recién creada.  
4. **Verifico que cada tabla cumpla 1NF** (valores atómicos) y, si es necesario, continúo a 2NF y 3NF para eliminar dependencias parciales y transitivas.  
5. **Ejecutó pruebas de inserción/actualización/borrado** para confirmar que las anomalías han desaparecido.

## Detalles
- **Básico**: 1NF garantiza atomicidad; se elimina la repetición de grupos de valores.  
- **Intermedio**: 2NF elimina dependencias parciales sobre claves compuestas; cada atributo no clave depende completamente de la clave primaria.  
- **Avanzado**: 3NF y BCNF suprimen dependencias transitivas y garantizan que cada atributo no clave dependa solo de la clave primaria, no de otros atributos no clave.  
- **Optimización práctica**: En entornos de analítica, a veces se desnormalizan tablas de referencia para reducir joins costosos, pero siempre manteniendo la lógica de integridad mediante vistas o materialized views.

## Ejemplo minimo
```sql
-- Tabla original con redundancia
CREATE TABLE ventas_brutas (
    id INT,
    cliente VARCHAR(50),
    producto VARCHAR(50),
    precio DECIMAL(10,2)
);

-- Normalización a 3NF
CREATE TABLE cliente (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE producto (
    producto_id INT PRIMARY KEY,
    nombre VARCHAR(50),
    precio DECIMAL(10,2)
);

CREATE TABLE venta (
    venta_id INT PRIMARY KEY,
    cliente_id INT REFERENCES cliente(cliente_id),
    producto_id INT REFERENCES producto(producto_id)
);
```

## Errores comunes
- **Normalizar en exceso**: crear demasiadas tablas pequeñas que degradan el rendimiento de los joins; evitarlo evaluando la carga de consultas.  
- **Olvidar claves foráneas**: rompe la integridad referencial; siempre definir constraints explícitos.  
- **Confundir 2NF y 3NF**: aplicar 2NF sin revisar dependencias transitivas; revisar cada atributo no clave para asegurar que depende solo de la clave primaria.  

## Estado actual
- **Fundamentos estables**: Las formas normales (1NF‑3NF) y el uso de primary/foreign keys siguen siendo la base aceptada para diseñar bases relacionales.  
- **Práctica moderna**: En data warehouses se combina la normalización con esquemas dimensionales (estrella, copo de nieve) y se emplean herramientas de modelado automático que generan scripts de normalización y desnormalización según patrones de acceso.  

## Conexiones
- **Modelado de datos**: La normalización es una técnica esencial dentro del modelado de datos para estructurar relaciones lógicas antes de implementar el esquema físico.  
- **Relational Databases**: Las bases de datos relacionales dependen de la normalización para aplicar eficientemente constraints y optimizar el motor de consultas.  
- **Keys & Constraints**: Las claves primarias y foráneas son los mecanismos que hacen posible la integridad que la normalización persigue.  

## Ruta de estudio
1. **Prerequisitos**: comprender tipos de datos SQL, conceptos de primary key y foreign key, y la noción de atomicidad.  
2. **Fundamentos**: estudiar 1NF, 2NF y 3NF con ejemplos de tablas reales; practicar con ejercicios de descomposición.  
3. **Avanzado**: explorar BCNF y 4NF, y casos de desnormalización controlada en entornos de BI.  
4. **Herramientas**: usar ER diagram tools (dbdiagram.io, MySQL Workbench) para visualizar esquemas normalizados.  
5. **Aplicación**: diseñar un modelo de datos completo para un caso de negocio (por ejemplo, sistema de pedidos) y validar con pruebas de integridad.  

## Preguntas de repaso
1. ¿Qué anomalía de actualización se evita al pasar de una tabla no normalizada a 3NF?  
2. ¿Cómo se identifica una dependencia parcial que requiere aplicar 2NF?  
3. ¿Cuál es la diferencia práctica entre una foreign key y una simple columna que almacena un ID?  
4. ¿En qué situaciones puede ser conveniente desnormalizar una tabla normalizada?  
5. ¿Qué forma normal elimina dependencias transitivas y por qué es importante para la integridad?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-08-normalization written_at=2026-11-05T22:53:23.600344+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/13 - Modelado de datos|Modelado de datos]] · *Backend*
- [[04 - Database & Data Analytics/02 - Data Modeling|Data Modeling]]
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]]
- [[04 - Database & Data Analytics/07 - Keys & Constraints|Keys & Constraints]]

---
← [[04 - Database & Data Analytics/07 - Keys & Constraints|Keys & Constraints]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/09 - Indexes|Indexes]] →
