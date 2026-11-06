---
title: "HTTP"
area: "Networking / Internet"
numero: 16
aliases: ["HTTP"]
tags: [concepto, it/networking-internet]
---
# HTTP

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 16 de 25**

## Qué abarca
- Protocolo fundamental de la Web

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo HTTP para intercambiar datos entre clientes y servidores web mediante peticiones y respuestas estructuradas. Resuelvo problemas de conectividad al verificar que los paquetes llegan al puerto 80/443, que la sesión TCP está establecida y que el mensaje sigue el formato esperado. En mi día a día como ingeniero de redes senior, reviso encabezados, códigos de estado y métodos HTTP para diagnosticar caídas de aplicaciones, bloqueos de firewalls o errores de balanceo de carga. Después de entender HTTP puedo diseñar reglas de ACL, configurar inspección profunda de paquetes (DPI) y validar la correcta terminación TLS en HTTPS. Cuando la comunicación se limita a nivel IP sin necesidad de contenido web, no es necesario profundizar en HTTP.

## Esqueleto (el 20% esencial)
1. **Petición‑Respuesta** – Un cliente envía una solicitud y el servidor devuelve una respuesta estructurada.  
2. **Métodos y códigos de estado** – GET, POST, PUT, DELETE, etc., indican la intención; 200, 404, 500 informan el resultado.  
3. **Encabezados** – Metadatos (Host, User‑Agent, Cookie) que influyen en enrutamiento, caché y seguridad.  
4. **Transporte sobre TCP** – HTTP usa TCP (puerto 80) para garantizar entrega ordenada y fiable.  
5. **Extensión a HTTPS** – TLS cifra el flujo HTTP, cambiando solo el puerto (443) y añadiendo la capa de seguridad.

## Como funciona
1. El cliente abre una conexión TCP al puerto 80 (o 443 para HTTPS).  
2. Envía una línea de solicitud: `METHOD SP URI SP HTTP/1.1 CRLF`.  
3. Añade los encabezados requeridos, finaliza con `CRLF`.  
4. El servidor procesa la petición, genera una línea de estado: `HTTP/1.1 SP CODE SP REASON CRLF`.  
5. Incluye encabezados de respuesta y, opcionalmente, un cuerpo.  
6. La conexión puede cerrarse o mantenerse viva (keep‑alive) para más intercambios.

## Detalles
- **Básico**: comprensión de la línea de solicitud y respuesta, y de los códigos 2xx, 4xx, 5xx.  
- **Intermedio**: manejo de encabezados críticos (Host, Content‑Length, Connection) y de métodos seguros vs idempotentes.  
- **Avanzado**: negociación de contenido (Accept, Content‑Encoding), gestión de cookies, uso de HTTP/2 multiplexado y transición a HTTPS con TLS 1.2/1.3.

## Ejemplo minimo
```bash
# Petición HTTP mínima con curl
curl -i http://example.com
```
Salida típica:
```
HTTP/1.1 200 OK
Date: Sat, 05 Nov 2026 12:00:00 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1256

<!doctype html>...
```

## Errores comunes
- Omitir el encabezado **Host** en HTTP/1.1 → el servidor responde 400 Bad Request.  
- Usar el método incorrecto (p.ej., GET para envío de datos sensibles) → vulnerabilidad o error 405.  
- No cerrar la conexión en servidores que no soportan keep‑alive → agotamiento de sockets.  

## Estado actual
**Fundamentos estables**: HTTP/1.1 sigue siendo la base para la mayoría de los servidores y dispositivos de red; los códigos de estado y métodos son invariables.  
**Práctica moderna**: la adopción de HTTP/2 y HTTP/3 mejora la latencia mediante multiplexado y UDP; HTTPS con TLS 1.3 es el estándar de seguridad para cualquier tráfico web expuesto a Internet.

## Conexiones
- **TCP**: HTTP se apoya en TCP para la entrega fiable de sus mensajes.  
- **HTTPS / TLS**: HTTPS es HTTP encapsulado en TLS, proporcionando confidencialidad e integridad.  
- **Headers / Cookies**: Los encabezados transportan información de control y las cookies permiten mantener estado entre peticiones.

## Ruta de estudio
1. **Prerequisitos**: comprensión de IP, TCP (puertos, handshake) y modelo OSI/TCP‑IP.  
2. **Fundamentos**: leer la especificación de HTTP/1.1, practicar con `curl` y `telnet`.  
3. **Intermedio**: estudiar encabezados críticos, métodos seguros, códigos de error y manejo de cookies.  
4. **Avanzado**: explorar HTTP/2 (multiplexado, server push) y HTTP/3 (QUIC), y profundizar en la configuración de TLS para HTTPS.  

## Preguntas de repaso
1. ¿Qué información lleva la línea de estado de una respuesta HTTP?  
2. ¿Cuál es la diferencia funcional entre los métodos GET y POST?  
3. ¿Por qué el encabezado Host es obligatorio en HTTP/1.1?  
4. ¿Cómo afecta la capa TLS a la operación de HTTP?  
5. ¿Qué ventaja aporta HTTP/2 respecto al modelo de conexión de HTTP/1.1?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-16-http written_at=2026-11-05T23:28:40.060650+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/01 - Internet & Web|Internet & Web]] · *Frontend*
- [[03 - Backend/02 - HTTP|HTTP]] · *Backend*
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/04 - TCP|TCP]]
- [[05 - Networking & Internet/15 - OSI - TCP-IP Model|OSI / TCP-IP Model]]
- [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]]
- [[05 - Networking & Internet/18 - Request - Response|Request / Response]]
- [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]]
- [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]]
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]]
- [[05 - Networking & Internet/22 - WebSockets|WebSockets]]

---
← [[05 - Networking & Internet/15 - OSI - TCP-IP Model|OSI / TCP-IP Model]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]] →
