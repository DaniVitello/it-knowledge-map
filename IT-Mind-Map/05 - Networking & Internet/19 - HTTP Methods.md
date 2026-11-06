---
title: "HTTP Methods"
area: "Networking / Internet"
numero: 19
aliases: ["HTTP Methods"]
tags: [concepto, it/networking-internet]
---
# HTTP Methods

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 19 de 25**

## Qué abarca
- GET
- POST
- PUT
- PATCH
- DELETE

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los métodos HTTP para indicar al servidor qué acción quiero que realice sobre un recurso web. Resuelvo problemas de conectividad como respuestas inesperadas o errores 4xx/5xx al interactuar con APIs, balanceadores de carga o firewalls que filtran tráfico según el verbo. En mi día a día como ingeniero de redes senior, los métodos aparecen al diagnosticar peticiones fallidas, al diseñar reglas de ACL que permitan solo GET y POST, o al validar que un proxy respete la semántica de PUT y DELETE. Después de entenderlos, puedo crear políticas de seguridad más precisas, interpretar logs de servidores y depurar problemas de capa 7. No necesito preocuparme cuando la comunicación se limita a tráfico de capa 3/4 (TCP/UDP) sin involucrar HTTP.

## Esqueleto (el 20% esencial)
1. **GET**: solicita la representación actual de un recurso sin modificarlo.  
2. **POST**: envía datos al servidor para crear un nuevo recurso o ejecutar una operación.  
3. **PUT / PATCH**: reemplaza (PUT) o actualiza parcialmente (PATCH) la representación de un recurso existente.  
4. **DELETE**: indica al servidor que elimine el recurso especificado.  

## Como funciona
1. El cliente abre una conexión TCP (usualmente sobre puerto 80 o 443).  
2. Envía una línea de solicitud que comienza con el verbo elegido (GET, POST, etc.) seguida de la URI y la versión HTTP.  
3. El servidor interpreta el verbo y ejecuta la lógica correspondiente: lee, crea, actualiza o elimina el recurso.  
4. El servidor devuelve una respuesta con un código de estado que refleja el resultado del verbo.  
5. Opcionalmente, el cliente incluye cabeceras (Headers) o cuerpo (Body) según el método (por ejemplo, cuerpo en POST o PUT).  

## Detalles
- **Básico**: GET y POST son los únicos verbos que la mayoría de firewalls permiten por defecto; se usan para navegación y formularios.  
- **Intermedio**: PUT y PATCH requieren que el servidor exponga la capacidad de sobrescribir o parchear recursos; son críticos en APIs RESTful y en pruebas de integridad de datos.  
- **Avanzado**: DELETE puede estar restringido por políticas de seguridad; su uso combinado con encabezados como `If-Match` permite borrados condicionales y evita condiciones de carrera. Además, la idempotencia de PUT y DELETE influye en la configuración de balanceadores de carga y cachés.  

## Ejemplo minimo
```bash
# GET simple a un endpoint público
curl -i http://example.com/api/resource
```
Salida típica:
```
HTTP/1.1 200 OK
Content-Type: application/json
...

{"id":1,"name":"Recurso"}
```

## Errores comunes
- Usar POST cuando el verbo idempotente requerido es PUT → genera duplicados.  
- Enviar cuerpo en una solicitud GET → algunos servidores lo ignoran y pueden devolver 400.  
- Olvidar el encabezado `Content-Type` en POST/PUT con JSON → el servidor no parsea el cuerpo.  
- Confiar en que DELETE siempre elimina el recurso; algunos servidores responden 202 (aceptado) y la eliminación es asíncrona.  

## Estado actual
- **Fundamentos estables**: los verbos GET, POST, PUT, PATCH y DELETE están definidos en RFC 7231 y su comportamiento básico es ampliamente soportado.  
- **Práctica moderna**: el uso de PATCH para actualizaciones parciales se ha popularizado con APIs GraphQL y JSON‑Patch; los balanceadores de capa 7 (por ejemplo, NGINX, Envoy) permiten reglas específicas por verbo para mejorar la seguridad y el enrutamiento.  

## Conexiones
- **HTTP**: los métodos son parte integral del protocolo y determinan cómo se construye la línea de solicitud.  
- **Request / Response**: cada método genera una solicitud que el servidor traduce en una respuesta con un código de estado correspondiente.  
- **HTTP Status Codes**: los códigos (200, 201, 204, 400, 404, 405, 500) indican el éxito o la falla del verbo aplicado al recurso.  

## Ruta de estudio
1. **Prerequisitos**: comprensión de TCP/IP, puertos 80/443 y conceptos de cliente/servidor.  
2. **Fundamentos**: leer RFC 7231, practicar con `curl` y `httpie` usando cada verbo.  
3. **Intermedio**: explorar APIs RESTful, probar idempotencia con PUT/DELETE y usar herramientas como Postman.  
4. **Avanzado**: configurar reglas de firewall y balanceadores que filtren por método, implementar autenticación basada en tokens y manejar respuestas asíncronas (202 Accepted).  

## Preguntas de repaso
1. ¿Qué diferencia fundamental hay entre GET y POST en términos de efectos sobre el recurso?  
2. ¿En qué situaciones es preferible usar PATCH en lugar de PUT?  
3. ¿Cómo afecta la idempotencia de un método a la configuración de un balanceador de carga?  
4. ¿Qué código de estado indica que una solicitud DELETE se aceptó pero la eliminación es asíncrona?  
5. ¿Cuál es el riesgo de enviar un cuerpo en una solicitud GET y cómo lo detecta un servidor?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-19-http-methods written_at=2026-11-05T23:31:22.624918+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/01 - Internet & Web|Internet & Web]] · *Frontend*
- [[03 - Backend/02 - HTTP|HTTP]] · *Backend*
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[05 - Networking & Internet/18 - Request - Response|Request / Response]]
- [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]]
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]]

---
← [[05 - Networking & Internet/18 - Request - Response|Request / Response]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]] →
