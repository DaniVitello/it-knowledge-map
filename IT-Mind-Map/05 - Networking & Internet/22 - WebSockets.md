---
title: "WebSockets"
area: "Networking / Internet"
numero: 22
aliases: ["WebSockets"]
tags: [concepto, it/networking-internet]
---
# WebSockets

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 22 de 25**

## Qué abarca
- Comunicación bidireccional persistente

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo WebSockets para mantener una comunicación bidireccional persistente entre un cliente y un servidor sin necesidad de abrir nuevas conexiones HTTP para cada mensaje. Resuelvo el problema de latencia y sobrecarga que aparecen cuando una aplicación necesita intercambiar datos en tiempo real, como chats, notificaciones o actualizaciones de estado en dashboards. En mi día a día como ingeniero de redes senior, lo empleo al diagnosticar flujos de tráfico persistente, validar la correcta negociación del handshake HTTP→WebSocket y asegurar que los firewalls y balanceadores permiten el upgrade de protocolo. Después de entender WebSockets, puedo diseñar arquitecturas que combinan HTTP para la carga inicial y WebSockets para la interacción continua, o decidir cuándo usar alternativas como HTTP/2 Server‑Sent Events. No necesito preocuparme cuando la aplicación solo envía peticiones puntuales y la latencia no es crítica.

## Esqueleto (el 20% esencial)
1. **Handshake HTTP → Upgrade** – El cliente inicia una petición HTTP con el header `Upgrade: websocket` y el servidor responde aceptando el cambio de protocolo.  
2. **Canal persistente** – Una vez aceptado, la conexión TCP subyacente permanece abierta y permite el intercambio de mensajes en ambas direcciones.  
3. **Framing de mensajes** – Cada mensaje se envuelve en un frame que indica tipo (texto, binario) y longitud, garantizando la integridad del flujo.  
4. **Cierre ordenado** – Tanto cliente como servidor pueden enviar un frame de cierre para terminar la sesión de forma limpia.  

## Como funciona
1. El cliente envía una petición HTTP GET a `ws://host:puerto/ruta` con los headers `Upgrade: websocket` y `Connection: Upgrade`.  
2. El servidor verifica que soporta WebSocket, genera una clave de aceptación (`Sec-WebSocket-Accept`) y responde con `101 Switching Protocols`.  
3. La capa TCP sigue activa; ya no se interpreta como HTTP sino como una secuencia de frames WebSocket.  
4. Cada vez que el cliente o el servidor necesita enviar datos, empaqueta la carga en un frame y lo escribe en el socket.  
5. Cuando la sesión termina, cualquiera de los extremos envía un frame de cierre (`opcode 0x8`) y cierra la conexión TCP.

## Detalles
- **Básico:** Solo se necesita una conexión TCP y los headers de handshake. No hay cifrado implícito; para seguridad se usa `wss://` (WebSocket sobre TLS).  
- **Intermedio:** Manejo de fragmentación de mensajes grandes, ping/pong para mantener viva la conexión y detectar caídas.  
- **Avanzado:** Integración con proxies inversos (NGINX, HAProxy) que deben reenviar correctamente el header `Upgrade`, uso de extensiones como permessage‑deflate para comprimir payloads y multiplexado de sub‑protocolos mediante el header `Sec-WebSocket-Protocol`.

## Ejemplo minimo
```bash
# Cliente con websocat (CLI)
websocat ws://echo.websocket.org
# Escribo "hola"
hola
# Recibo el eco del servidor
hola
```
*Salida:* El cliente envía “hola” y el servidor lo devuelve inmediatamente, demostrando el canal bidireccional persistente.

## Errores comunes
- **Olvidar el header `Upgrade`** → el servidor responde 400 y la conexión se cierra; verificar siempre el handshake.  
- **Usar HTTP en lugar de HTTPS** en entornos donde el tráfico está cifrado; cambiar a `wss://` para atravesar firewalls que inspeccionan TLS.  
- **No manejar ping/pong** → la conexión puede quedar inactiva y ser cerrada por el balanceador; implementar keep‑alive.  

## Estado actual
- **Fundamentos estables:** El protocolo definido en RFC 6455 (handshake, framing, códigos de cierre) es ampliamente soportado por navegadores y servidores.  
- **Práctica moderna:** El uso de `wss://` es la norma en producción; los balanceadores de carga actuales (NGINX, HAProxy, Envoy) incluyen soporte nativo para el upgrade de WebSocket y para la terminación TLS.  

## Conexiones
- **HTTP** – El handshake parte de una petición HTTP y depende de los mismos códigos de estado y headers.  
- **TLS** – Cuando se usa `wss://`, la capa de seguridad es idéntica a la de HTTPS, protegiendo la integridad y confidencialidad del canal.  
- **Sockets** – WebSocket reutiliza una conexión TCP (socket) tradicional, pero añade su propio framing para multiplexar mensajes.

## Ruta de estudio
1. **Prerequisitos:** TCP/IP, conceptos de sockets, fundamentos de HTTP/1.1 y TLS.  
2. **WebSocket básico:** Leer RFC 6455, practicar con herramientas CLI (websocat, wscat).  
3. **Integración con servidores:** Configurar NGINX o HAProxy para proxy inverso con `proxy_set_header Upgrade $http_upgrade;`.  
4. **Seguridad:** Implementar `wss://`, validar certificados y políticas de CORS.  
5. **Optimización:** Explorar extensiones de compresión, manejo de fragmentación y multiplexado de sub‑protocolos.  

## Preguntas de repaso
1. ¿Qué headers son obligatorios en la petición HTTP de inicio de un WebSocket?  
2. ¿Cómo se indica que una conexión WebSocket debe cerrarse de forma ordenada?  
3. ¿Por qué es necesario usar `wss://` en entornos productivos?  
4. ¿Qué papel juega el proxy inverso al manejar el upgrade de protocolo?  
5. ¿Cuál es la diferencia entre un frame de tipo “text” y uno de tipo “binary”?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-22-websockets written_at=2026-11-05T23:33:58.972985+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]]
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]]
- [[06 - Operating Systems & Linux/14 - Sockets|Sockets]] · *Operating Systems / Linux*

---
← [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/23 - Proxies - Reverse Proxies|Proxies / Reverse Proxies]] →
