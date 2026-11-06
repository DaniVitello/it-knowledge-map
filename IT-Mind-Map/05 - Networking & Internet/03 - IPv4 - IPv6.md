---
title: "IPv4 / IPv6"
area: "Networking / Internet"
numero: 3
aliases: ["IPv4 / IPv6"]
tags: [concepto, it/networking-internet]
---
# IPv4 / IPv6

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 3 de 25**

## Qué abarca
- Versiones del protocolo IP

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo IPv4 e IPv6 para direccionar y encaminar paquetes dentro de cualquier red que administro. Resuelvo el problema de identificar de forma única cada host y de permitir que los routers sepan a dónde enviar el tráfico. Aparecen en todas las tareas de diagnóstico y operación: asignación de direcciones, configuración de interfaces, análisis de rutas y resolución de problemas de conectividad. Después de entender cómo funcionan, puedo planificar subredes, migrar a IPv6 y depurar fallos de capa 3 con herramientas como ping o traceroute. Cuando la red está completamente configurada y los hosts usan direcciones estáticas o DHCP sin conflicto, ya no necesito preocuparme por el protocolo en sí.

## Esqueleto (el 20% esencial)
1. **Versiones del protocolo IP** – IPv4 usa direcciones de 32 bits, IPv6 de 128 bits, lo que define el espacio de direcciones disponible.  
2. **Encapsulamiento y routing** – Cada paquete lleva una cabecera IP que indica origen, destino y TTL; los routers usan esa información para reenviar el tráfico.  
3. **Asignación de direcciones** – DHCP entrega direcciones IPv4 o IPv6 a los hosts; la ausencia de DHCP obliga a usar configuraciones estáticas.  
4. **Resolución de capa 2** – ARP traduce direcciones IPv4 a MAC; en IPv6 se usa Neighbor Discovery (ND) con mensajes ICMPv6.  

## Como funciona
1. Un host solicita una dirección mediante DHCP (IPv4) o DHCPv6 (IPv6).  
2. El servidor DHCP responde con una dirección y parámetros de red (máscara, gateway, DNS).  
3. El host construye la cabecera IP del paquete, inserta la dirección de destino y calcula el checksum.  
4. Antes de enviarlo, el host resuelve la dirección MAC del gateway: usa ARP para IPv4 o ND para IPv6.  
5. El router recibe el paquete, decrementa el TTL y busca la mejor ruta en su tabla de routing basada en la dirección de destino.  
6. El proceso se repite en cada salto hasta que el paquete llega al destino o se agota el TTL.

## Detalles
- **Básico**: comprensión de la notación decimal punteada (IPv4) y hexadecimal con dos puntos (IPv6).  
- **Intermedio**: configuración de DHCP scopes, reservas y opciones; uso de `ip -6 route` para inspeccionar rutas IPv6.  
- **Avanzado**: planificación de subredes con CIDR, despliegue de Dual Stack, túneles (6to4, Teredo) y políticas de seguridad basadas en direcciones IP.

## Ejemplo minimo
```bash
# Ping a una dirección IPv4
ping -c 1 8.8.8.8

# Ping a una dirección IPv6
ping6 -c 1 2001:4860:4860::8888
```
Salida típica muestra `1 packets transmitted, 1 received`, confirmando que la capa IP está operativa.

## Errores comunes
- Confundir la máscara de subred con la dirección de red; evitarlo revisando siempre la notación CIDR.  
- Usar una dirección IPv6 sin habilitar ND; corregir activando el daemon `radvd` o configurando DHCPv6.  
- Asignar la misma dirección IPv4 a varios hosts; prevenirlo con reservas DHCP o auditorías de ARP.

## Estado actual
**Fundamentos estables**: IPv4 sigue siendo la columna vertebral de Internet; la estructura de cabecera y el algoritmo de routing no han cambiado. IPv6, con su cabecera simplificada y espacio de direcciones ampliado, está estandarizado y soportado por todos los sistemas operativos modernos.  
**Práctica moderna**: la mayoría de los data centers despliegan Dual Stack y utilizan DHCPv6 + SLAAC para asignar direcciones automáticamente. Las políticas de seguridad ahora incluyen filtros basados en prefijos IPv6 y la desactivación de ARP en entornos IPv6 puro.

## Conexiones
- **IP**: la capa de red que encapsula los datos y define cómo se enrutan los paquetes.  
- **DHCP**: provee la asignación dinámica de direcciones IPv4 e IPv6, facilitando la gestión de grandes redes.  
- **ARP**: traduce direcciones IPv4 a MAC; su equivalente en IPv6 es Neighbor Discovery, que cumple la misma función en la capa de enlace.

## Ruta de estudio
1. **Prerequisitos**: comprensión de modelos OSI, direccionamiento MAC y conceptos básicos de routing.  
2. **Fundamentos**: estudiar la estructura de la cabecera IPv4 e IPv6, notación CIDR y funcionamiento de DHCP/ARP.  
3. **Práctica**: configurar interfaces en Linux/Windows, crear scopes DHCP y validar con `ping` y `traceroute`.  
4. **Avanzado**: diseñar una red Dual Stack, implementar túneles 6to4 y aplicar listas de control de acceso (ACL) por prefijo IPv6.  

## Preguntas de repaso
1. ¿Qué diferencia principal hay entre la longitud de la dirección IPv4 y la IPv6?  
2. ¿Cómo resuelve un host IPv4 la dirección MAC del gateway antes de enviar un paquete?  
3. ¿Qué rol juega DHCPv6 en una red Dual Stack?  
4. Si un paquete IPv6 llega a un router con TTL (hop limit) = 1, ¿qué ocurre?  
5. ¿Por qué es importante planificar subredes con CIDR antes de asignar direcciones estáticas?

<!-- trazabilidad: run_id=run-20261105-201026-0a44b6 concept=05-networking-internet-03-ipv4-ipv6 written_at=2026-11-05T23:12:37.897703+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/08 - DHCP|DHCP]]
- [[05 - Networking & Internet/10 - ARP|ARP]]
- [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]]

---
← [[05 - Networking & Internet/02 - IP|IP]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/04 - TCP|TCP]] →
