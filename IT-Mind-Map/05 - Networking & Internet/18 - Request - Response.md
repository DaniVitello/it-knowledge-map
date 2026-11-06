---
title: "Request / Response"
area: "Networking / Internet"
numero: 18
aliases: ["Request / Response"]
tags: [concepto, it/networking-internet]
---
# Request / Response

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 18 de 25**

## Qué abarca
- Modelo de comunicación web

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el modelo Request / Response para intercambiar información entre clientes y servidores en la capa de aplicación. Resuelvo problemas de conectividad como la imposibilidad de obtener recursos web o de validar que un servicio está activo. En mi día a día como ingeniero de redes senior, lo aplico al diagnosticar fallas de HTTP, validar encabezados y códigos de estado, y diseñar políticas de firewall que permitan o bloqueen tráfico según el tipo de petición. Después de comprender cómo se estructuran y procesan las solicitudes y respuestas, puedo interpretar trazas de paquetes, crear pruebas de carga y ajustar balanceadores de carga. No necesito preocuparme por Request / Response cuando solo trabajo en capas inferiores (por ejemplo, routing IP) o cuando el tráfico está cifrado y no inspeccionable.

## Esqueleto (el 20% esencial)
1. **Cliente envía una Request**: un mensaje estructurado que indica el recurso deseado y el método HTTP.  
2. **Servidor procesa la Request**: interpreta el método, la URI y los headers para generar la respuesta adecuada.  
3. **Servidor devuelve una Response**: contiene un código de estado, headers y, opcionalmente, un cuerpo con el recurso solicitado.  
4. **Headers y Cookies**: transportan metadatos que influyen en caché, autenticación y sesión.  
5. **Código de estado (HTTP Status)**: comunica el resultado de la operación (éxito, redirección, error).

## Como funciona
1. El cliente abre una conexión TCP (usualmente al puerto 80 o 443).  
2. Envía la línea de solicitud (`GET /index.html HTTP/1.1`) seguida de los headers (p. ej. `Host`, `User-Agent`).  
3. El servidor recibe la petición, la parsea y determina el recurso y el método.  
4. Ejecuta la lógica correspondiente (servir archivo estático, invocar backend, etc.).  
5. Genera una línea de estado (`HTTP/1.1 200 OK`) y los headers de respuesta (p. ej. `Content-Type`, `Set-Cookie`).  
6. Opcionalmente envía un cuerpo (HTML, JSON, etc.) y cierra o mantiene la conexión según `Connection` header.

## Detalles
- **Básico**: Entender la sintaxis de la línea de solicitud y la línea de estado, y la función de los headers más comunes.  
- **Intermedio**: Manejo de métodos avanzados (`POST`, `PUT`, `DELETE`), negociación de contenido mediante `Accept` y `Content-Type`, y uso de cookies para estado de sesión.  
- **Avanzado**: Optimización con `Keep-Alive`, compresión (`Content-Encoding`), y control de caché (`ETag`, `Cache-Control`). También incluye la interacción con proxies y balanceadores que pueden modificar o inspeccionar Request/Response.

## Ejemplo minimo
```bash
# Cliente: envía una petición GET simple
curl -i http://example.com

# Salida típica
HTTP/1.1 200 OK
Date: Sat, 05 Nov 2026 12:00:00 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 125

<html>…</html>
```
El comando `curl -i` muestra la línea de estado y los headers de la Response, demostrando el ciclo Request / Response.

## Errores comunes
- **Olvidar el header `Host`**: los servidores virtuales no pueden seleccionar el sitio correcto.  
- **Usar el método incorrecto** (`GET` para una operación que requiere `POST`).  
- **Ignorar códigos de estado** y asumir siempre éxito; revisar siempre el código antes de procesar el cuerpo.  
- **No cerrar la conexión** cuando se usa HTTP/1.0 sin `Connection: close`, lo que genera sockets colgados.  

## Estado actual
- **Fundamentos estables**: el modelo Request / Response, los métodos HTTP y los códigos de estado definidos en RFC 7231 siguen siendo la base de la comunicación web.  
- **Práctica moderna**: el uso de HTTP/2 y HTTP/3 introduce multiplexado y encabezados binarios, pero el concepto de solicitud y respuesta persiste. Los encabezados de seguridad (`Strict-Transport-Security`, `Content-Security-Policy`) y la gestión de cookies SameSite son prácticas recomendadas en entornos actuales.

## Conexiones
- **HTTP**: el protocolo que transporta las Request y Response en la capa de aplicación.  
- **Headers / Cookies**: mecanismos que acompañan a la Request y a la Response para transmitir metadatos y estado de sesión.  
- **HTTP Status Codes**: valores numéricos que la Response devuelve para indicar el resultado de la Request.

## Ruta de estudio
1. **Prerequisitos**: TCP/IP básico, conceptos de cliente/servidor y uso de herramientas como `curl` o `telnet`.  
2. **Fundamentos**: leer RFC 7230‑7235, practicar con peticiones GET/POST y analizar códigos de estado.  
3. **Intermedio**: profundizar en headers de control, cookies y manejo de sesiones.  
4. **Avanzado**: estudiar HTTP/2 y HTTP/3, seguridad de cabeceras, y configuración de proxies/balanceadores que inspeccionan Request/Response.  
5. **Aplicación**: diseñar pruebas de carga, crear reglas de firewall basadas en métodos y códigos, y depurar trazas con Wireshark.

## Preguntas de repaso
1. ¿Qué información esencial lleva la línea de solicitud de una Request?  
2. ¿Cómo se interpreta el código de estado `404` y qué acción debería tomar el cliente?  
3. ¿Cuál es la diferencia funcional entre los headers `Host` y `User-Agent`?  
4. ¿En qué situaciones un proxy puede modificar una Response sin alterar la Request original?  
5. ¿Qué ventajas aporta HTTP/2 respecto al modelo clásico Request / Response?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-18-request-response written_at=2026-11-05T23:30:20.878061+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/01 - Internet & Web|Internet & Web]] · *Frontend*
- [[03 - Backend/02 - HTTP|HTTP]] · *Backend*
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]]
- [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]]
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]]

---
← [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]] →
