---
title: "Autorización"
area: "Backend"
numero: 17
aliases: ["Autorización"]
tags: [concepto, it/backend]
---
# Autorización

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 17 de 25**

## Qué abarca
- Roles
- permissions
- RBAC
- ABAC

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la autorización para decidir **qué** operaciones puede ejecutar cada usuario o servicio dentro de una API. Resuelvo el problema de que, aunque la identidad esté verificada, no todos los clientes deben acceder a los mismos recursos; por ejemplo, un cliente “read‑only” no debe poder borrar datos. Aparece en cada punto donde expongo endpoints protegidos: controladores, microservicios y funciones serverless. Después de entenderla, puedo diseñar políticas de acceso coherentes, aplicar controles granulares y auditar quién hizo qué. No necesito preocuparme por autorización cuando el endpoint es público o cuando la lógica de negocio no depende de la identidad del solicitante.

## Esqueleto (el 20% esencial)
1. **Roles** – conjuntos estáticos de permisos que se asignan a usuarios o cuentas de servicio.  
2. **Permissions** – acciones concretas (p. ej. `read:order`, `delete:user`) que pueden ser concedidas o denegadas.  
3. **RBAC (Role‑Based Access Control)** – modelo que vincula roles a permissions y usuarios a roles.  
4. **ABAC (Attribute‑Based Access Control)** – modelo que evalúa atributos dinámicos (usuario, recurso, contexto) para decidir el acceso.  

## Como funciona
1. El cliente envía su token de autenticación (JWT, OAuth2, etc.).  
2. Un middleware extrae la identidad y los atributos (roles, claims).  
3. Según el modelo elegido (RBAC o ABAC), el middleware compara los permisos requeridos por el endpoint con los que posee el cliente.  
4. Si la evaluación es positiva, la petición continúa; de lo contrario, se devuelve `403 Forbidden`.  

## Detalles
- **Básico**: definir roles (`admin`, `editor`, `viewer`) y mapearlos a permisos estáticos.  
- **Intermedio**: combinar RBAC con scopes en el token para evitar consultas a bases de datos en cada request.  
- **Avanzado**: implementar ABAC usando atributos como `tenantId`, `timeOfDay` o `ipAddress`; integrar un PDP (Policy Decision Point) externo (OPA, XACML) para decisiones centralizadas y auditoría.  

## Ejemplo minimo
```js
// Express middleware simple de RBAC
function authorize(requiredPermission) {
  return (req, res, next) => {
    const perms = req.user.permissions; // extraído del JWT
    if (perms.includes(requiredPermission)) return next();
    res.status(403).json({ error: 'Forbidden' });
  };
}

// Uso en un endpoint
app.delete('/users/:id', authorize('delete:user'), (req, res) => {
  // lógica de borrado
  res.sendStatus(204);
});
```

## Errores comunes
- **Asignar permisos directamente a usuarios** → dificulta el mantenimiento; usar roles.  
- **Olvidar revocar tokens** después de cambiar roles → aplicar listas de revocación o tokens de corta vida.  
- **Confiar solo en el cliente** para decidir acceso → siempre validar en el servidor.  

## Estado actual
- **Fundamentos estables**: RBAC sigue siendo la práctica recomendada para la mayoría de los sistemas; la definición de roles y permisos es ampliamente soportada por frameworks (Spring Security, NestJS).  
- **Práctica moderna**: ABAC está ganando adopción en entornos multitenant y zero‑trust; herramientas como Open Policy Agent (OPA) y AWS IAM Policy permiten políticas declarativas y auditoría centralizada.  

## Conexiones
- **Security Engineering** – la autorización es una capa clave dentro del diseño de sistemas seguros, complementando la defensa en profundidad.  
- **Autenticación** – sin una identidad verificada, la autorización no tiene sujeto sobre el cual aplicar reglas.  
- **Seguridad** – la correcta autorización previene escaladas de privilegio y protege la confidencialidad e integridad de los datos.  

## Ruta de estudio
1. **Prerequisitos**: comprender autenticación (JWT, OAuth2) y conceptos básicos de HTTP (`401`, `403`).  
2. **Fundamentos**: leer la guía de RBAC de OWASP, implementar roles y permisos en un proyecto simple.  
3. **Intermedio**: explorar scopes y claims en tokens, integrar middleware de autorización en un framework elegido.  
4. **Avanzado**: estudiar ABAC y políticas declarativas con OPA, practicar la separación de PDP y PEP, y configurar auditoría de decisiones.  

## Preguntas de repaso
1. ¿En qué situación un endpoint público no necesita autorización?  
2. ¿Cómo se diferencia un permiso de un rol en RBAC?  
3. ¿Qué ventaja aporta ABAC frente a RBAC en un entorno multitenant?  
4. ¿Cuál es la respuesta HTTP estándar cuando la autorización falla?  
5. ¿Por qué es importante revocar o expirar tokens después de cambiar los roles de un usuario?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-17-autorizacion written_at=2026-11-05T19:51:23.680906+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/24 - Security Engineering|Security Engineering]] · *Software Engineering*
- [[02 - Frontend/19 - Autenticación en Frontend|Autenticación en Frontend]] · *Frontend*
- [[03 - Backend/16 - Autenticación|Autenticación]]
- [[03 - Backend/18 - Seguridad|Seguridad]]

---
← [[03 - Backend/16 - Autenticación|Autenticación]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/18 - Seguridad|Seguridad]] →
