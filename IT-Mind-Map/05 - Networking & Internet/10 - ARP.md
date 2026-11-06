---
title: "ARP"
area: "Networking / Internet"
numero: 10
aliases: ["ARP"]
tags: [concepto, it/networking-internet]
---
# ARP

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 10 de 25**

## Qué abarca
- Resolución IP → MAC en IPv4

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo ARP para traducir la dirección IP de un host IPv4 a la dirección MAC que necesita la capa de enlace para enviarle un paquete dentro de la misma red local. Resuelvo el problema de “¿a qué hardware debo dirigir este frame?” que aparece cada vez que una máquina necesita comunicarse con otra en su segmento sin conocer su dirección física. En mi día a día como ingeniero de redes senior, ARP está presente al diagnosticar fallas de conectividad local, al validar tablas de encaminamiento y al diseñar políticas de seguridad basadas en direcciones MAC. Después de entender ARP puedo interpretar la salida de `arp -a`, detectar conflictos de direcciones y configurar filtros MAC. Cuando trabajo exclusivamente con enlaces punto a punto o con IPv6, donde se usa Neighbor Discovery, ya no necesito preocuparme por ARP.

## Esqueleto (el 20% esencial)
1. **Solicitud ARP**: un host broadcasta una petición preguntando “¿Quién tiene esta IP?”.
2. **Respuesta ARP**: el propietario de la IP responde con su dirección MAC en un mensaje unicast.
3. **Cache ARP**: el solicitante guarda la pareja IP‑MAC para evitar nuevas solicitudes.
4. **Timeout y refresco**: las entradas caducan y se vuelven a solicitar cuando expiran.
5. **Uso en diagnóstico**: `arp -a` muestra la tabla y permite validar la resolución.

## Como funciona
1. El host A necesita enviar un paquete a la IP 192.168.1.20 y no tiene la MAC en su cache.  
2. Construye un **ARP request** con la IP objetivo y la envía a la dirección MAC de broadcast `ff:ff:ff:ff:ff:ff`.  
3. Todos los hosts del segmento reciben la petición; solo el host B cuya IP coincide responde.  
4. B envía un **ARP reply** unicast a A, incluyendo su MAC (p. ej. `00:1a:2b:3c:4d:5e`).  
5. A actualiza su tabla ARP y encapsula el paquete original en un frame Ethernet dirigido a la MAC de B.  
6. Si la respuesta no llega, A re‑intenta hasta que el timeout expire; la entrada se elimina después de un período de inactividad.

## Detalles
- **Básico**: ARP opera solo en IPv4; el mensaje tiene 28 bytes y se transporta en una trama Ethernet sin encapsulación adicional.  
- **Intermedio**: Las tablas ARP pueden ser estáticas (configuradas manualmente) o dinámicas; los switches pueden inspeccionar ARP para prevenir ataques de spoofing.  
- **Avanzado**: En entornos virtualizados, los hypervisores implementan “proxy ARP” para representar máquinas detrás de un router. En redes SDN, el controlador puede inyectar respuestas ARP para optimizar rutas.  

## Ejemplo minimo
```bash
# En la máquina que necesita la MAC
$ ping -c 1 192.168.1.20   # genera una solicitud ARP implícita
PING 192.168.1.20 (192.168.1.20) 56(84) bytes of data.

--- 192.168.1.20 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms

# Ver la tabla ARP resultante
$ arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
192.168.1.20            ether   00:1a:2b:3c:4d:5e   C                     eth0
```
La salida muestra que la IP 192.168.1.20 quedó asociada a la MAC 00:1a:2b:3c:4d:5e.

## Errores comunes
- **Confundir ARP con DNS**: ARP resuelve IP→MAC, DNS resuelve nombres→IP. Evitar usar el comando `nslookup` para problemas de capa 2.  
- **Ignorar la caché**: asumir que la tabla está vacía y volver a generar tráfico innecesario; limpiar con `arp -d` solo cuando sea necesario.  
- **No considerar proxy ARP**: en redes con routers que responden por subredes remotas, la ausencia de respuesta directa no siempre indica fallo.  

## Estado actual
- **Fundamentos estables**: ARP sigue definido en RFC 826 y su comportamiento básico (broadcast request, unicast reply, caché con timeout) es idéntico a la implementación de la mayoría de los sistemas operativos modernos.  
- **Práctica moderna**: se complementa con mecanismos de seguridad como Dynamic ARP Inspection (DAI) en switches Cisco, y con soluciones de detección de ARP spoofing en entornos de nube. Los controladores SDN pueden sobrescribir respuestas ARP para dirigir tráfico sin cambiar la topología física.

## Conexiones
- **IP**: ARP traduce la dirección IP de nivel 3 a la dirección MAC necesaria para la capa 2.  
- **DHCP**: al asignar una IP, DHCP permite que el nuevo host participe en ARP para anunciar su MAC.  
- **Subnetting / CIDR**: la necesidad de enviar una solicitud ARP depende de que la IP destino pertenezca a la misma subred definida por la máscara CIDR.

## Ruta de estudio
1. **Prerequisitos**: comprender el modelo OSI, direcciones IPv4 y funcionamiento de Ethernet.  
2. **Fundamentos**: leer RFC 826 (ARP) y practicar con `arp -a`, `arp -d`.  
3. **Seguridad**: estudiar Dynamic ARP Inspection y técnicas de mitigación de ARP spoofing.  
4. **Entornos avanzados**: explorar proxy ARP en routers, ARP en redes virtualizadas y su gestión desde controladores SDN.  
5. **Especialización**: implementar scripts de monitoreo de la tabla ARP y diseñar políticas de filtrado MAC basadas en la información obtenida.

## Preguntas de repaso
1. ¿Qué información contiene una solicitud ARP y a qué dirección MAC se envía?  
2. ¿Cómo afecta el timeout de la caché ARP a la generación de tráfico de red?  
3. ¿Cuál es la diferencia principal entre una tabla ARP estática y una dinámica?  
4. ¿En qué situaciones un switch con Dynamic ARP Inspection bloquearía una respuesta ARP?  
5. ¿Por qué un host IPv6 no utiliza ARP y qué protocolo lo reemplaza?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-10-arp written_at=2026-11-05T23:23:08.474369+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/03 - IPv4 - IPv6|IPv4 / IPv6]]
- [[05 - Networking & Internet/08 - DHCP|DHCP]]
- [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]]

---
← [[05 - Networking & Internet/09 - MAC - Ethernet|MAC / Ethernet]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/11 - Routing|Routing]] →
