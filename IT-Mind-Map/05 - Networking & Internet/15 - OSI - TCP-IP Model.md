---
title: "OSI / TCP-IP Model"
area: "Networking / Internet"
numero: 15
aliases: ["OSI / TCP-IP Model"]
tags: [concepto, it/networking-internet]
---
# OSI / TCP-IP Model

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 15 de 25**

## Qué abarca
- Capas y responsabilidades de networking

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el modelo OSI/TCP‑IP para estructurar y diagnosticar cualquier flujo de datos que atraviesa la red. Resuelvo problemas de conectividad al identificar en qué capa se produce la falla, ya sea una dirección IP incorrecta, un puerto cerrado o una mala configuración de la aplicación. En mi día a día como ingeniero de redes senior, el modelo me guía al diseñar topologías, configurar dispositivos y analizar trazas de paquetes. Después de comprenderlo, puedo planificar segmentaciones, aplicar políticas de seguridad por capa y automatizar pruebas de enlace. Cuando la red funciona y no hay síntomas de error, no necesito profundizar en cada capa; basta con validar que los servicios críticos responden.

## Esqueleto (el 20% esencial)
1. **Capas y responsabilidades** – Cada capa del modelo tiene una función clara: física y enlace manejan la transmisión; red dirige paquetes; transporte garantiza entrega; aplicación expone servicios.  
2. **Separación de preocupaciones** – Los protocolos de una capa no dependen de los detalles internos de las capas superiores o inferiores, lo que permite modularidad.  
3. **Mapeo OSI ↔ TCP‑IP** – Las 7 capas OSI se agrupan en 4 capas TCP‑IP (Link, Internet, Transport, Application), facilitando la implementación real.  
4. **Puntos de inspección** – Herramientas como ping, traceroute y tcpdump operan en capas específicas y revelan dónde está el problema.  

## Como funciona
1. Un paquete se crea en la **capa de aplicación** (p. ej., HTTP).  
2. La **capa de transporte** (TCP) agrega puertos y controla la secuencia.  
3. La **capa de red** (IP) inserta direcciones de origen y destino.  
4. La **capa de enlace** encapsula el paquete en frames Ethernet con MACs.  
5. La **capa física** convierte los bits en señales eléctricas o ópticas para el medio.  
Al recibir el frame, cada capa inversa elimina su encabezado, devolviendo el dato original a la aplicación.

## Detalles
- **Básico**: entender qué hace cada capa y cómo se corresponde con los protocolos más usados (ARP, ICMP, TCP, UDP, HTTP).  
- **Intermedio**: usar herramientas de captura (Wireshark) para observar encabezados en cada capa y correlacionar eventos (retransmisiones TCP, TTL expirado).  
- **Avanzado**: diseñar políticas de QoS o firewall basadas en atributos de capa 3/4, y depurar problemas de NAT o MPLS que alteran la información de capa de red.

## Ejemplo minimo
```bash
# Solicita la página raíz de example.com
curl http://example.com -I
```
Salida (resumen):
```
HTTP/1.1 200 OK          ← capa Application (HTTP)
Server: ECS (nyb/1D2D)   ← información de la aplicación
```
Detrás de escena, `curl` abre un socket TCP (capa Transport), el kernel inserta una cabecera IP (capa Internet) y finalmente la tarjeta de red envía frames Ethernet (capa Link).

## Errores comunes
- **Confundir capas**: atribuir un error de “puerto cerrado” a la capa de red; evitarlo revisando primero la capa de transporte con `netstat` o `ss`.  
- **Usar OSI como estándar de implementación**: la mayoría de los equipos siguen TCP‑IP; reconocer el mapeo evita configuraciones innecesarias.  
- **Ignorar la capa física**: problemas de cableado aparecen como fallas de capa 3; validar conectividad física con `ethtool` o pruebas de señal.

## Estado actual
- **Fundamentos estables**: la separación en capas y la función de IP, TCP y HTTP siguen siendo la base de cualquier arquitectura de red.  
- **Práctica moderna**: la industria se centra en el modelo TCP‑IP de 4 capas; el modelo OSI se usa principalmente como herramienta educativa y para describir protocolos de capa 2/3 en entornos SDN y NFV.

## Conexiones
- **IP**: es el protocolo de la capa de red que lleva los paquetes entre hosts; sin IP no hay encaminamiento.  
- **TCP**: opera en la capa de transporte, proporcionando conexión fiable y control de flujo para aplicaciones como HTTP.  
- **HTTP**: reside en la capa de aplicación y depende de TCP para la entrega fiable de recursos web.

## Ruta de estudio
1. **Prerequisitos**: conocimientos de binario, direcciones IPv4/IPv6 y conceptos de sockets.  
2. **Modelo OSI/TCP‑IP**: estudiar cada capa, sus protocolos típicos y ejemplos de comandos de diagnóstico.  
3. **Herramientas de captura**: aprender Wireshark y `tcpdump` para observar encabezados reales.  
4. **Diseño avanzado**: aplicar QoS, VLANs y políticas de firewall basadas en atributos de capa 3/4.  
5. **Especialización**: explorar SDN, NFV y cómo abstraen las capas tradicionales.

## Preguntas de repaso
1. ¿Qué información añade la capa de transporte a un paquete y por qué es crucial para HTTP?  
2. ¿Cómo se relacionan las 7 capas OSI con las 4 capas del modelo TCP‑IP?  
3. ¿Qué herramienta usarías para confirmar que una dirección IP es alcanzable y en qué capa opera?  
4. Si un cliente recibe “connection refused”, ¿en qué capa probablemente está el problema?  
5. ¿Por qué el modelo OSI sigue siendo útil aunque la implementación real siga el modelo TCP‑IP?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-15-osi-tcp-ip-model written_at=2026-11-05T23:28:05.766884+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/04 - TCP|TCP]]
- [[05 - Networking & Internet/16 - HTTP|HTTP]]

---
← [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/16 - HTTP|HTTP]] →
