---
title: "HTTP Status Codes"
area: "Networking / Internet"
numero: 20
aliases: ["HTTP Status Codes"]
tags: [concepto, it/networking-internet]
---
# HTTP Status Codes

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 20 de 25**

## Qué abarca
- 2xx
- 3xx
- 4xx
- 5xx

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los códigos de estado HTTP para interpretar rápidamente el resultado de cada petición que paso por la red, ya sea desde un cliente, un balanceador o un proxy. Resuelvo problemas de conectividad como respuestas inesperadas, redirecciones infinitas o fallos del servidor, y puedo decidir si debo reenviar, corregir la solicitud o escalar el incidente. Aparecen en cada transacción de la capa de aplicación cuando diagnostico latencias, errores 4xx/5xx o bucles de redirección 3xx. Después de entenderlos, puedo automatizar alertas, diseñar políticas de reintento y optimizar la arquitectura de los servicios web. Cuando solo trabajo con tráfico de capa inferior (IP, TCP/UDP) o con protocolos sin respuesta estructurada, no necesito preocuparme por los códigos de estado.

## Esqueleto (el 20% esencial)
1. **Rangos de códigos** – 2xx éxito, 3xx redirección, 4xx error del cliente, 5xx error del servidor.  
2. **2xx** indica que la petición fue procesada correctamente y el recurso está disponible.  
3. **3xx** instruye al cliente a cambiar la URL o el método para completar la operación.  
4. **4xx** señala que la solicitud es inválida o no autorizada; el cliente debe corregirla.  
5. **5xx** muestra fallos internos del servidor; el cliente puede reintentar o escalar.

## Como funciona
1. El cliente envía una solicitud HTTP (método, URL, headers).  
2. El servidor procesa la petición y genera una respuesta que incluye un código de estado.  
3. El cliente interpreta el código según el rango: continúa (2xx), sigue la redirección (3xx), corrige la solicitud (4xx) o reintenta/avisa (5xx).  
4. Herramientas de diagnóstico (curl, wget, browsers, proxies) exponen el código en la salida, permitiendo al ingeniero decidir la acción inmediata.

## Detalles
- **Básico**: reconocer los cuatro rangos y los códigos más comunes (200, 301, 404, 500).  
- **Intermedio**: usar códigos específicos (201 Created, 302 Found, 401 Unauthorized, 503 Service Unavailable) para afinar políticas de reintento y caché.  
- **Avanzado**: combinar códigos con headers (Location, Retry-After) y cookies para orquestar flujos de autenticación, balanceo de carga y degradación gradual de servicios.

## Ejemplo minimo
```bash
$ curl -I https://example.com/nonexistent
HTTP/1.1 404 Not Found
Date: Sun, 05 Nov 2026 12:00:00 GMT
Content-Type: text/html; charset=UTF-8
```
La línea `404 Not Found` indica al ingeniero que el recurso solicitado no existe y que la causa es del cliente.

## Errores comunes
- **Interpretar 3xx como error**: 3xx son redirecciones legítimas; usar la URL indicada en el header `Location`.  
- **Ignorar 5xx temporales**: reintentar después del tiempo indicado por `Retry-After` evita falsas alarmas.  
- **Confundir 401 y 403**: 401 requiere autenticación, 403 indica que el cliente está autenticado pero no tiene permiso.

## Estado actual
Los códigos de estado son parte del estándar HTTP/1.1 y siguen siendo válidos en HTTP/2 y HTTP/3. En la práctica moderna, los balanceadores de carga y los CDNs añaden lógica basada en 2xx/3xx/4xx/5xx para dirigir tráfico, aplicar caché y generar alertas operativas.

## Conexiones
- **HTTP Methods**: el método usado (GET, POST, PUT…) determina qué códigos de estado son esperables (p. ej., 201 para POST exitoso).  
- **Headers / Cookies**: headers como `Location` o `Set-Cookie` complementan los códigos 3xx y 4xx para guiar al cliente.  
- **Internet & Web**: los códigos de estado son la señalización primaria que permite a navegadores, APIs y microservicios comunicarse sobre el estado de la conectividad a nivel de aplicación.

## Ruta de estudio
1. Prerrequisitos: modelo OSI, TCP/IP, fundamentos de HTTP (request/response).  
2. Estudiar los rangos y códigos más usados, practicando con `curl` y `wget`.  
3. Profundizar en códigos menos comunes y su interacción con headers (Location, Retry-After).  
4. Implementar scripts de monitoreo que analicen códigos 4xx/5xx y disparen alertas.  
5. Explorar casos de uso en balanceadores de carga y CDNs para aplicar lógica de redirección y degradación.

## Preguntas de repaso
1. ¿Qué rango de códigos indica que la petición fue exitosa y qué información adicional suele acompañar a un 2xx?  
2. ¿Cómo actúa un cliente frente a un código 301 y qué header es esencial para completar la redirección?  
3. ¿Cuál es la diferencia operativa entre los códigos 401 y 403?  
4. ¿Qué acción recomienda tomar un ingeniero cuando recibe repetidamente un 503 Service Unavailable?  
5. ¿De qué manera los códigos de estado influyen en la configuración de un balanceador de carga?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-20-http-status-codes written_at=2026-11-05T23:32:26.117753+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/01 - Internet & Web|Internet & Web]] · *Frontend*
- [[03 - Backend/02 - HTTP|HTTP]] · *Backend*
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[05 - Networking & Internet/18 - Request - Response|Request / Response]]
- [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]]
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]]

---
← [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]] →
