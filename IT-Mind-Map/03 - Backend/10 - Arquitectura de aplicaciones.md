---
title: "Arquitectura de aplicaciones"
area: "Backend"
numero: 10
aliases: ["Arquitectura de aplicaciones"]
tags: [concepto, it/backend]
---
# Arquitectura de aplicaciones

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 10 de 25**

## Qué abarca
- Capas
- módulos
- services
- repositories

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la arquitectura de aplicaciones para organizar el código de un servicio backend en capas coherentes que separan la lógica de negocio, el acceso a datos y la exposición de la API. Resuelvo problemas de mantenibilidad, pruebas unitarias y escalabilidad al evitar que cambios en una capa afecten a las demás. Aparece en cada proyecto donde construyo o mantengo micro‑servicios, APIs REST o GraphQL, y me permite delegar responsabilidades a equipos especializados. Después de entenderla, puedo diseñar nuevos servicios rápidamente, refactorizar sistemas legacy y definir contratos claros entre capas. No necesito preocuparme de la arquitectura cuando el proyecto es un script puntual sin reutilización ni evolución prevista.

## Esqueleto (el 20% esencial)
1. **Capas** – separación lógica entre presentación (controllers), lógica de negocio (services) y persistencia (repositories).  
2. **Módulos** – agrupación de componentes relacionados en paquetes o directorios que facilitan la reutilización.  
3. **Services** – encapsulan reglas de negocio y orquestan llamadas a repositorios y a otros servicios externos.  
4. **Repositories** – abstraen el acceso a bases de datos o sistemas de almacenamiento, ofreciendo una API uniforme.  

## Como funciona
1. La petición HTTP llega al **controller** (capa de presentación).  
2. El controller delega la operación al **service** correspondiente.  
3. El service ejecuta la lógica de negocio y, cuando necesita datos, llama al **repository**.  
4. El repository traduce la solicitud a consultas de base de datos o a llamadas a otro micro‑servicio y devuelve el resultado al service.  
5. El service devuelve la respuesta al controller, que la serializa y la envía al cliente.

## Detalles
- **Básico**: definir una carpeta `controllers`, `services` y `repositories`; cada una expone una única función pública.  
- **Intermedio**: introducir interfaces (p. ej. TypeScript) para desacoplar la implementación del repository y permitir inyección de dependencias en los services.  
- **Avanzado**: aplicar patrones como Unit of Work, Domain Events o CQRS dentro de la capa de service, y usar contenedores IoC para gestionar la vida de los módulos.

## Ejemplo minimo
```ts
// repository.ts
export class UserRepository {
  async findById(id: string) {
    return await db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}

// service.ts
import { UserRepository } from './repository';
export class UserService {
  constructor(private repo = new UserRepository()) {}
  async getUser(id: string) {
    const user = await this.repo.findById(id);
    if (!user) throw new Error('Not found');
    return { id: user.id, name: user.name };
  }
}

// controller.ts (Express)
import { Router } from 'express';
import { UserService } from './service';
const router = Router();
router.get('/users/:id', async (req, res) => {
  const service = new UserService();
  try {
    const data = await service.getUser(req.params.id);
    res.json(data);
  } catch (e) {
    res.status(404).send(e.message);
  }
});
export default router;
```

## Errores comunes
- **Acoplar lógica de negocio al controller** – evita mezclar validaciones de entrada con reglas de dominio; mantén la responsabilidad en los services.  
- **Acceder directamente a la base desde el controller** – rompe la capa de repository y dificulta pruebas unitarias; usa siempre el repository.  
- **Crear repositorios monolíticos** – divide en repositorios por entidad o contexto para reducir dependencias y mejorar la reutilización.  

## Estado actual
- **Fundamentos estables**: la separación en capas (controller → service → repository) sigue siendo la práctica recomendada para la mayoría de los sistemas backend.  
- **Práctica moderna**: se complementa con inyección de dependencias, tipado fuerte (TypeScript), y patrones de arquitectura limpia que favorecen la independencia de frameworks y facilitan pruebas automatizadas.

## Conexiones
- **Architecture** – la arquitectura de aplicaciones es una especialización de la arquitectura de software, enfocada en la organización de componentes dentro de un backend.  
- **Arquitectura Frontend** – comparte la idea de capas (por ejemplo, UI → state → API), lo que permite alinear contratos entre cliente y servidor.  
- **AI System Architecture** – los principios de modularidad y separación de responsabilidades se aplican también al diseñar pipelines de inferencia que consumen APIs backend.

## Ruta de estudio
1. **Prerequisitos**: manejo sólido de JavaScript/TypeScript, conceptos de HTTP y bases de datos relacionales/no‑relacionales.  
2. **Fundamentos**: estudiar patrones MVC y la separación en capas; practicar con ejemplos simples como el anterior.  
3. **Intermedio**: aprender inyección de dependencias (p. ej. `tsyringe`), interfaces y pruebas unitarias con `jest`.  
4. **Avanzado**: explorar Domain‑Driven Design, Clean Architecture y patrones como CQRS o Event Sourcing; implementar micro‑servicios con Docker y orquestación ligera.  

## Preguntas de repaso
1. ¿Qué ventaja principal aporta la separación en capas al mantener un servicio backend?  
2. ¿Cómo se comunica un service con la base de datos sin romper la arquitectura?  
3. ¿Cuál es la diferencia funcional entre un controller y un repository?  
4. ¿Qué problema resuelve la inyección de dependencias en la arquitectura de aplicaciones?  
5. ¿En qué casos podrías prescindir de una capa de service y por qué?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-10-arquitectura-de-aplicaciones written_at=2026-11-05T19:44:38.356306+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/22 - Architecture|Architecture]] · *Software Engineering*
- [[02 - Frontend/25 - Arquitectura Frontend|Arquitectura Frontend]] · *Frontend*
- [[07 - AI Engineering/25 - AI System Architecture|AI System Architecture]] · *AI Engineering*

---
← [[03 - Backend/09 - Validación|Validación]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/11 - Bases de datos|Bases de datos]] →
