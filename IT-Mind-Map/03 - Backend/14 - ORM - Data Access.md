---
title: "ORM / Data Access"
area: "Backend"
numero: 14
aliases: ["ORM / Data Access"]
tags: [concepto, it/backend]
---
# ORM / Data Access

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 14 de 25**

## Qué abarca
- Prisma
- Hibernate
- SQLAlchemy
- EF
- etc.

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo un ORM (Object‑Relational Mapping) para traducir objetos del código a filas de una base de datos relacional y viceversa, evitando escribir SQL manual en cada operación. Resuelvo el problema de la fricción entre la lógica de negocio escrita en el lenguaje del servidor (por ejemplo, TypeScript, Java o Python) y el esquema de la base de datos, garantizando consistencia y reduciendo errores de tipado. En mi día a día como ingeniero backend senior, el ORM aparece cada vez que creo, actualizo o consulto datos dentro de un servicio o API; me permite concentrarme en la lógica de negocio y en la arquitectura del servicio. Después de dominarlo, puedo diseñar repositorios reutilizables, aplicar migraciones automáticas y optimizar consultas sin abandonar la comodidad del código orientado a objetos. No es necesario usar un ORM cuando el acceso a datos es trivial, cuando se requiere un rendimiento extremo o cuando la base de datos no es relacional.

## Esqueleto (el 20% esencial)
1. **Mapeo entidad‑tabla** – Cada clase del dominio se asocia a una tabla y sus atributos a columnas.  
2. **CRUD automático** – El ORM genera consultas SQL para crear, leer, actualizar y borrar objetos sin código SQL explícito.  
3. **Migraciones de esquema** – Herramientas integradas (Prisma migrate, Hibernate DDL, Alembic) sincronizan el modelo de código con la base de datos.  
4. **Consultas expresivas** – Se construyen filtros y joins mediante API de lenguaje (query builders, LINQ‑like).  
5. **Gestión de sesiones/transactions** – El ORM controla la apertura y cierre de conexiones y la atomicidad de operaciones.

## Como funciona
1. Defino una clase (p. ej. `User`) y decoradores/annotations que indican la tabla y columnas.  
2. El ORM registra esa definición en su *metadata* al iniciar la aplicación.  
3. Cuando llamo a `userRepository.save(user)`, el ORM traduce el objeto a una sentencia `INSERT` o `UPDATE` según su estado.  
4. Para lecturas, `userRepository.find({ email })` se convierte en `SELECT * FROM users WHERE email = ?`.  
5. Si el modelo cambia, ejecuto una migración; el ORM genera el DDL necesario y lo aplica contra la base de datos.  
6. Durante la petición, una *session* mantiene el contexto de transacción; al final, se hace `commit` o `rollback`.

## Detalles
- **Básico**: Configuración del cliente (datasource), definición de entidades y uso de métodos CRUD.  
- **Intermedio**: Relaciones (one‑to‑many, many‑to‑many), carga diferida (*lazy loading*), consultas compuestas y uso de transacciones explícitas.  
- **Avanzado**: Optimización de consultas (eager loading, índices declarativos), manejo de *caching* de segundo nivel, extensiones de *query* con funciones nativas y generación de migraciones complejas (renombrado de columnas, data seeding).

## Ejemplo minimo
```ts
// Prisma (TypeScript)
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function crearUsuario() {
  const usuario = await prisma.user.create({
    data: { email: 'juan@example.com', nombre: 'Juan' },
  });
  console.log(usuario);
}
crearUsuario();
```

## Errores comunes
- **Olvidar sincronizar migraciones** → la tabla no coincide con la entidad; evitar ejecutando siempre `prisma migrate dev` o su equivalente.  
- **Usar carga perezosa en bucles** → genera N+1 consultas; prefiera *eager loading* con `include`.  
- **Mantener lógica de negocio dentro del ORM** → mezclar capas; mantenga la lógica en servicios y use el ORM solo para persistencia.  

## Estado actual
- **Fundamentos estables**: mapeo entidad‑tabla, generación automática de CRUD y soporte de transacciones son pilares consolidados en Prisma, Hibernate, SQLAlchemy y Entity Framework.  
- **Práctica moderna**: migraciones declarativas, generación de tipos TypeScript/Java a partir del esquema, y soporte de *shadow tables* para auditoría son tendencias adoptadas en los últimos años.

## Conexiones
- **Modelado de datos** – El ORM materializa el modelo de dominio en estructuras de tabla, garantizando que los cambios en el modelo se reflejen en la base de datos.  
- **Relational Databases** – El ORM actúa como puente que traduce operaciones de objetos a SQL compatible con PostgreSQL, MySQL, SQL Server, etc.  
- **Caching** – Los resultados de consultas ORM pueden ser almacenados en capas de caché (Redis, in‑memory) para reducir la carga de la base de datos y acelerar respuestas de API.

## Ruta de estudio
1. **Prerequisitos**: SQL básico, conceptos de programación orientada a objetos y manejo de paquetes en el lenguaje elegido.  
2. **Fundamentos**: Instalar un ORM (Prisma, Hibernate, SQLAlchemy), crear una entidad simple y ejecutar operaciones CRUD.  
3. **Intermedio**: Definir relaciones, trabajar con transacciones y aplicar migraciones; leer la documentación oficial de la herramienta.  
4. **Avanzado**: Optimizar consultas, implementar carga anticipada, integrar migraciones en CI/CD y explorar extensiones de *query* específicas del motor de base de datos.  

## Preguntas de repaso
1. ¿Cómo traduce un ORM un objeto de dominio a una sentencia SQL de inserción?  
2. ¿Qué problema resuelve la capa de migraciones y cuándo debe ejecutarse en el ciclo de desarrollo?  
3. ¿Cuál es la diferencia entre carga perezosa y carga anticipada, y cómo afecta al rendimiento?  
4. ¿En qué situaciones es preferible evitar un ORM y escribir SQL manual?  
5. ¿Cómo se relaciona el ORM con la capa de caché en una arquitectura de microservicios?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-14-orm-data-access written_at=2026-11-05T19:47:58.460388+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/13 - Modelado de datos|Modelado de datos]]
- [[04 - Database & Data Analytics/03 - Relational Databases|Relational Databases]] · *Database / Data Analytics*

---
← [[03 - Backend/13 - Modelado de datos|Modelado de datos]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/15 - Transacciones|Transacciones]] →
