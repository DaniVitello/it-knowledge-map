---
title: "Headers / Cookies"
area: "Networking / Internet"
numero: 21
aliases: ["Headers / Cookies"]
tags: [concepto, it/networking-internet]
---
# Headers / Cookies

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 21 de 25**

## Qué abarca
- Metadata y estado de comunicación

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los **headers** y **cookies** para transportar información de control y estado entre cliente y servidor durante una sesión HTTP/HTTPS. Resuelvo problemas de autenticación, personalización y gestión de sesiones sin necesidad de volver a negociar credenciales en cada petición. En mi día a día como ingeniero de redes senior, reviso los headers para diagnosticar errores de caché, redirecciones o problemas de TLS, y analizo cookies cuando investigo fallos de login o de balanceo de carga basado en sesión. Después de comprender cómo se estructuran y se usan, puedo diseñar políticas de seguridad (por ejemplo, `Secure` y `HttpOnly`), depurar aplicaciones web y configurar dispositivos de inspección de tráfico. Cuando la comunicación es puramente de capa de red (IP, TCP) y no involucra HTTP, no necesito preocuparme por estos elementos.

## Esqueleto (el 20% esencial)
1. **Headers** son pares *clave‑valor* que acompañan a cada request y response, indicando metadatos como tipo de contenido, caché y control de conexión.  
2. **Cookies** son pequeños fragmentos de datos que el servidor envía al cliente mediante el header `Set-Cookie` y que el cliente devuelve en cada request con el header `Cookie`.  
3. Ambos permiten **mantener estado** en un protocolo sin estado (HTTP), habilitando autenticación, preferencias y balanceo de carga.  
4. Los headers y cookies son inspeccionables con herramientas de red (tcpdump, Wireshark) y depuradores de navegador, lo que los convierte en puntos clave para el diagnóstico.  

## Como funciona
1. El cliente abre una conexión TCP (o TLS) y envía un **request** HTTP con sus headers (p. ej., `User-Agent`, `Accept`).  
2. El servidor procesa la solicitud y genera una **response** que incluye headers de control (p. ej., `Content-Type`, `Cache-Control`).  
3. Si necesita conservar información de sesión, el servidor añade un header `Set-Cookie` con atributos (dominio, ruta, expiración, `Secure`, `HttpOnly`).  
4. En cada request subsecuente, el cliente incluye el header `Cookie` con el valor recibido, permitiendo al servidor identificar la sesión y aplicar lógica de estado.  
5. Los dispositivos de red pueden leer o modificar estos headers (por ejemplo, un proxy que agrega `X-Forwarded-For` o un firewall que elimina cookies inseguras).  

## Detalles
- **Básico**: entender la sintaxis `Header-Name: value` y el ciclo `Set-Cookie` → `Cookie`.  
- **Intermedio**: manejo de atributos de cookie (`Domain`, `Path`, `SameSite`) y de headers de control de caché (`ETag`, `If-None-Match`).  
- **Avanzado**: uso de headers para seguridad (`Strict-Transport-Security`, `Content-Security-Policy`) y para balanceo de carga (`Cookie` sticky sessions). También la interacción con TLS (cifrado de headers y cookies bajo HTTPS).  

## Ejemplo minimo
```http
GET /index.html HTTP/1.1
Host: ejemplo.com
User-Agent: curl/7.68.0

HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure

<html>...</html>
```
El cliente recibe `Set-Cookie` y, en la siguiente petición, enviará `Cookie: sessionId=abc123`.

## Errores comunes
- **Olvidar atributos de seguridad** (`Secure`, `HttpOnly`) → expone la cookie a ataques de captura; evitar configurando siempre estos atributos en entornos HTTPS.  
- **Confundir header y cuerpo** → intentar colocar datos de sesión en el cuerpo de la respuesta; usar siempre `Set-Cookie` en los headers.  
- **No respetar el dominio/ruta** → la cookie se envía a servidores no deseados; definir correctamente `Domain` y `Path`.  

## Estado actual
- **Fundamentos estables**: la estructura de headers y el mecanismo `Set-Cookie`/`Cookie` están definidos en RFC 7230 y RFC 6265 y son compatibles con todos los navegadores modernos.  
- **Práctica moderna**: se recomienda usar atributos `SameSite=Lax|Strict` y `Secure` por defecto, y limitar la longitud de cookies a 4 KB para evitar problemas de rendimiento en proxies y firewalls.  

## Conexiones
- **HTTP**: los headers y cookies son parte integral del protocolo de aplicación que transporta los datos entre cliente y servidor.  
- **HTTPS / TLS**: cuando la conexión está cifrada, los headers y cookies viajan protegidos contra intercepción, pero siguen siendo visibles para los dispositivos que terminan TLS (por ejemplo, un reverse proxy).  
- **WebSockets**: la negociación inicial de un WebSocket usa una petición HTTP que incluye los mismos headers y cookies, permitiendo que la sesión establecida persista en el canal bidireccional.  

## Ruta de estudio
1. **Prerequisitos**: TCP/IP, modelo OSI, conceptos básicos de HTTP/1.1.  
2. **Fundamentos**: leer RFC 7230 (mensajes HTTP) y RFC 6265 (cookies). Practicar con `curl -v` y `Wireshark` para observar headers y cookies en tráfico real.  
3. **Seguridad**: estudiar RFC 6265bis (actualizaciones de atributos) y guías de OWASP sobre `Secure`/`HttpOnly`/`SameSite`.  
4. **Operación avanzada**: configurar balanceadores de carga con sticky sessions, inspección de headers en firewalls de próxima generación y depuración de problemas de caché con `ETag` y `If-Modified-Since`.  

## Preguntas de repaso
1. ¿Qué información de control puede transportar un header y cómo ayuda a diagnosticar problemas de caché?  
2. ¿Cómo se establece y mantiene una sesión mediante cookies en una serie de requests HTTP?  
3. ¿Qué atributos de cookie son críticos para protegerla en un entorno HTTPS y por qué?  
4. ¿De qué manera un proxy puede modificar o añadir headers y qué impacto tiene en la trazabilidad de la sesión?  
5. ¿Cómo se reutilizan los headers y cookies durante la negociación inicial de un WebSocket?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-21-headers-cookies written_at=2026-11-05T23:33:24.840869+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/01 - Internet & Web|Internet & Web]] · *Frontend*
- [[03 - Backend/02 - HTTP|HTTP]] · *Backend*
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]]
- [[05 - Networking & Internet/18 - Request - Response|Request / Response]]
- [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]]
- [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]]
- [[05 - Networking & Internet/22 - WebSockets|WebSockets]]

---
← [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/22 - WebSockets|WebSockets]] →
