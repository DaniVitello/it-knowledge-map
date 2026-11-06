---
title: "DNS"
area: "Networking / Internet"
numero: 7
aliases: ["DNS"]
tags: [concepto, it/networking-internet]
---
# DNS

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 7 de 25**

## Qué abarca
- Traducción de dominios → IP

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo DNS para traducir los nombres de dominio que escribo en el navegador a direcciones IP que las máquinas de la red pueden enrutar. Resuelvo el problema de que los usuarios recuerden nombres legibles en vez de largas secuencias numéricas, y lo aplico cada vez que configuro o depuro la conectividad de clientes y servidores. Después de entender DNS puedo diseñar zonas, delegar sub‑dominios y diagnosticar fallos de resolución que impiden el acceso a servicios. No necesito preocuparme cuando la comunicación se realiza exclusivamente entre direcciones IP estáticas dentro de una red aislada.

## Esqueleto (el 20% esencial)
1. **Resolución de nombres** – Un cliente envía una consulta DNS y recibe la IP correspondiente.  
2. **Jerarquía de servidores** – La petición recorre una cadena de servidores autoritativos y cachés.  
3. **Zonas y registros** – Cada zona contiene registros (A, AAAA, CNAME, MX, etc.) que describen recursos.  
4. **Caché y TTL** – Los resolvers guardan respuestas temporales para acelerar consultas posteriores.  

## Como funciona
1. El host genera una consulta DNS (por ejemplo, `example.com`).  
2. El resolver local verifica su caché; si la entrada está fresca, devuelve la IP.  
3. Si no está en caché, el resolver envía la consulta al **root server**.  
4. El root server indica el **TLD server** (.com).  
5. El TLD server responde con la dirección del **authoritative server** de `example.com`.  
6. El servidor autoritativo devuelve el registro A (IPv4) o AAAA (IPv6) con la IP solicitada.  
7. El resolver almacena la respuesta según el TTL y la entrega al cliente.

## Detalles
- **Básico**: Entender los tipos de registros (A, AAAA, CNAME) y el flujo de consulta descrito en el esqueleto.  
- **Intermedio**: Configurar zonas, delegar sub‑dominios y ajustar TTL para balancear frescura y carga.  
- **Avanzado**: Implementar DNSSEC para firmar respuestas, usar servidores de resolución recursiva internos y aplicar políticas de split‑horizon para entornos híbridos.

## Ejemplo minimo
```bash
$ nslookup example.com 8.8.8.8
Server:  8.8.8.8
Address: 8.8.8.8#53

Non-authoritative answer:
Name:    example.com
Address: 93.184.216.34
```
La salida muestra la IP que el resolver de Google (8.8.8.8) devolvió para `example.com`.

## Errores comunes
- **Olvidar actualizar la zona** después de cambiar la IP de un servidor → la resolución sigue apuntando a la dirección antigua.  
- **TTL demasiado bajo** genera tráfico innecesario a los servidores autoritativos.  
- **Confundir registros CNAME con A** provoca bucles de resolución o respuestas inesperadas.  

## Estado actual
- **Fundamentos estables**: El modelo jerárquico de root → TLD → autoritativo y los tipos de registro básicos siguen sin cambios.  
- **Práctica moderna**: DNSSEC se está adoptando para evitar envenenamiento; los resolvers recursivos incorporan filtrado de malware y políticas de privacidad (p. ej., DNS over HTTPS).  

## Conexiones
- **IP** – DNS traduce nombres a direcciones IP, permitiendo que los protocolos de capa de red operen.  
- **HTTP** – Los navegadores usan DNS antes de iniciar una conexión HTTP/HTTPS a un servidor web.  
- **CDN** – Las redes de distribución de contenido utilizan respuestas DNS geográficas para dirigir al cliente al nodo más cercano.  

## Ruta de estudio
1. **Prerequisitos**: comprensión de direcciones IP, modelo cliente‑servidor y conceptos básicos de TCP/UDP.  
2. **Fundamentos**: tipos de registros DNS, flujo de consulta y configuración de zonas en BIND o PowerDNS.  
3. **Intermedio**: delegación de sub‑dominios, ajuste de TTL y uso de herramientas de diagnóstico (`dig`, `nslookup`).  
4. **Avanzado**: implementación de DNSSEC, despliegue de resolvers recursivos internos, integración con DNS over TLS/HTTPS y políticas de split‑horizon.  

## Preguntas de repaso
1. ¿Qué papel juega el servidor raíz en una consulta DNS?  
2. ¿Cuál es la diferencia funcional entre un registro A y un registro CNAME?  
3. ¿Cómo afecta el valor de TTL al tráfico generado hacia los servidores autoritativos?  
4. ¿Qué mecanismo se utiliza para proteger la integridad de las respuestas DNS en entornos modernos?  
5. En un escenario de split‑horizon, ¿por qué se necesita más de un servidor autoritativo?

<!-- trazabilidad: run_id=run-20261105-201026-0a44b6 concept=05-networking-internet-07-dns written_at=2026-11-05T23:16:25.360500+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/01 - Internet|Internet]]
- [[05 - Networking & Internet/02 - IP|IP]]

---
← [[05 - Networking & Internet/06 - Puertos|Puertos]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/08 - DHCP|DHCP]] →
