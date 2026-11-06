---
title: "Modelado de datos"
area: "Backend"
numero: 13
aliases: ["Modelado de datos"]
tags: [concepto, it/backend]
---
# Modelado de datos

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 13 de 25**

## Qué abarca
- Relaciones
- normalización
- constraints

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el modelado de datos para estructurar la información que mis servicios y APIs van a almacenar y consultar. Resuelvo problemas de inconsistencia, redundancia y dificultad al escribir consultas eficientes, garantizando que la lógica de negocio tenga una base fiable. Aparece cada vez que diseño una nueva entidad, defino relaciones entre tablas o migraciones de esquema en un proyecto backend. Después de entenderlo, puedo crear esquemas que soporten transacciones, validar datos mediante constraints y optimizar el rendimiento de los endpoints. No necesito preocuparme cuando la aplicación solo maneja datos efímeros en memoria o cuando delego el almacenamiento a un servicio externo sin esquema propio.

## Esqueleto (el 20% esencial)
1. **Relaciones** – Definen cómo se conectan las entidades (uno‑a‑uno, uno‑a‑muchos, muchos‑a‑muchos).  
2. **Normalización** – Organiza los datos en tablas para eliminar redundancia y evitar anomalías de actualización.  
3. **Constraints** – Reglas de integridad (primary key, foreign key, unique, check) que el motor de base de datos aplica automáticamente.  
4. **Claves** – Identificadores únicos (primary key) y referencias (foreign key) que habilitan las relaciones.  
5. **Mapeo a código** – El modelo se refleja en clases o structs mediante un ORM o capa de acceso.

## Como funciona
1. Analizo los requisitos de negocio y extraigo las **entidades** (p. ej., Usuario, Pedido).  
2. Determino las **relaciones** entre ellas y elijo el tipo adecuado.  
3. Aplico **normalización** (hasta 3NF) para distribuir atributos en tablas sin duplicación.  
4. Defino **constraints** y **claves** en cada tabla para garantizar integridad.  
5. Genero el **esquema** en la base de datos y, si uso un ORM, creo las clases que lo representan.  
6. El código de la API utiliza esas clases para leer/escribir datos; el motor de base de datos valida los constraints en cada operación.

## Detalles
- **Básico**: crear tablas con columnas simples y una primary key.  
- **Intermedio**: introducir foreign keys, índices y reglas de unicidad; aplicar 1NF y 2NF.  
- **Avanzado**: diseñar relaciones muchos‑a‑muchos mediante tablas de unión, usar check constraints y triggers, y aplicar 3NF o BCNF para esquemas complejos; considerar particionamiento y sharding en entornos de alta escala.

## Ejemplo minimo
```sql
-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- Tabla de pedidos (uno‑a‑muchos con users)
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    total NUMERIC(10,2) NOT NULL,
    placed_at TIMESTAMP DEFAULT now()
);
```
En un ORM de Python (SQLAlchemy):
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    user = relationship("User", back_populates="orders")
```

## Errores comunes
- **Duplicar datos** en varias tablas → rompe la normalización; usar foreign keys en su lugar.  
- **Olvidar índices** en columnas de búsqueda frecuente → consultas lentas; crear índices explícitos.  
- **Usar claves compuestas sin necesidad** → complica el ORM; preferir surrogate keys.  
- **No definir constraints** → permite datos inválidos; siempre especificar NOT NULL, UNIQUE, etc.  
- **Sobrecargar relaciones muchos‑a‑muchos** con columnas extra en la tabla principal → crear tabla de unión dedicada.

## Estado actual
- **Fundamentos estables**: relaciones, normalización y constraints siguen siendo la base de cualquier RDBMS.  
- **Práctica moderna**: los ORMs (SQLAlchemy, TypeORM, Hibernate) automatizan gran parte del mapeo, pero se recomienda revisar el esquema generado y ajustar índices manualmente. En microservicios, el modelado de datos a menudo se combina con eventos de dominio para mantener consistencia eventual.

## Conexiones
- **ORM / Data Access**: el modelo de datos se traduce a clases que el ORM usa para generar consultas SQL.  
- **Relational Databases**: el modelado define la estructura física que el motor relacional ejecuta y valida.  
- **Keys & Constraints**: son los mecanismos que hacen posible que las relaciones definidas en el modelo sean enforceadas por la base de datos.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de tablas y tipos de datos.  
2. **Fundamentos**: estudiar normalización (1NF‑3NF) y tipos de relaciones.  
3. **Práctica**: crear esquemas en PostgreSQL o MySQL, aplicar constraints y probar inserciones/actualizaciones.  
4. **ORM**: mapear los esquemas a código con SQLAlchemy o TypeORM, observar el DDL generado.  
5. **Optimización**: aprender a crear índices, analizar planes de ejecución y aplicar particionamiento si es necesario.  
6. **Avanzado**: diseñar esquemas para alta disponibilidad (sharding, multi‑tenant) y entender trade‑offs de denormalización controlada.

## Preguntas de repaso
1. ¿Cómo decide si una relación debe ser uno‑a‑muchos o muchos‑a‑muchos?  
2. ¿Qué anomalías de actualización se evitan al aplicar la tercera forma normal (3NF)?  
3. ¿Cuál es la diferencia práctica entre una primary key y una unique constraint?  
4. ¿Por qué es importante crear índices en columnas usadas como foreign keys?  
5. ¿Cómo afecta la elección de una tabla de unión a la generación de código en un ORM?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-13-modelado-de-datos written_at=2026-11-05T19:46:42.661486+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/14 - ORM - Data Access|ORM / Data Access]]
- [[04 - Database & Data Analytics/02 - Data Modeling|Data Modeling]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/07 - Keys & Constraints|Keys & Constraints]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/08 - Normalization|Normalization]] · *Database / Data Analytics*

---
← [[03 - Backend/12 - SQL|SQL]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/14 - ORM - Data Access|ORM / Data Access]] →
