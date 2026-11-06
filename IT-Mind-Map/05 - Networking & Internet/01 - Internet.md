---
title: "Internet"
area: "Networking / Internet"
numero: 1
aliases: ["Internet"]
tags: [concepto, it/networking-internet]
---
# Internet

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 1 de 25**

## Qué abarca
- Red de redes y modelo cliente-servidor

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Internet como la infraestructura que interconecta todas las redes locales y de proveedores, permitiendo que mis clientes y servidores se comuniquen sin importar su ubicación física. Resuelvo problemas de conectividad cuando una aplicación no alcanza un recurso externo, rastreando si el fallo está dentro de mi dominio o en la ruta global. Aparece en mi día a día al diseñar topologías WAN, configurar rutas estáticas o protocolos de enrutamiento dinámico, y al validar la disponibilidad de servicios en la nube. Después de entender cómo funciona, puedo planificar redundancia, optimizar el tráfico y diagnosticar fallos de capa 3 y 4. No necesito preocuparme cuando la comunicación es estrictamente intra‑LAN y no depende de recursos fuera de mi red.

## Esqueleto (el 20% esencial)
1. **Red de redes**: Internet es la interconexión de miles de redes autónomas mediante protocolos comunes.  
2. **Modelo cliente‑servidor**: Los dispositivos actúan como clientes que solicitan servicios a servidores ubicados en cualquier punto de la red global.  
3. **Dirección IP y enrutamiento**: Cada extremo posee una dirección IP única que permite a los routers decidir el camino óptimo.  
4. **Protocolos de capa de transporte**: TCP y UDP garantizan la entrega fiable o la transmisión sin conexión según la aplicación.  
5. **Sistema de nombres de dominio (DNS)**: Traduce nombres legibles por humanos a direcciones IP para que los clientes encuentren servidores.

## Como funciona
1. Un cliente genera una solicitud a un nombre de dominio (ej. `www.ejemplo.com`).  
2. El resolver local consulta DNS y obtiene la dirección IP del servidor.  
3. El paquete IP se encapsula con TCP/UDP y se envía al router de borde.  
4. Cada router consulta su tabla de enrutamiento y reenvía el paquete hacia el siguiente salto, siguiendo el mejor camino basado en la métrica (costo, latencia, políticas).  
5. Al llegar al router del servidor, el paquete se entrega al proceso que escucha en el puerto indicado.  
6. El servidor responde siguiendo el mismo proceso inverso, completando la sesión cliente‑servidor.

## Detalles
- **Básico**: Comprender direcciones IPv4/IPv6, máscara de subred y la tabla de enrutamiento estática.  
- **Intermedio**: Configurar protocolos dinámicos (OSPF, BGP) que permiten que la red de redes se adapte automáticamente a cambios de topología.  
- **Avanzado**: Implementar políticas de tráfico (QoS, ACL) y mecanismos de resiliencia (BGP multipath, Anycast) para optimizar la entrega de servicios críticos.

## Ejemplo minimo
```bash
# Resolución DNS y ping a un host público
$ nslookup www.google.com
Server:  192.168.1.1
Address: 192.168.1.1#53

Non-authoritative answer:
Name:    www.google.com
Addresses: 142.250.72.196

# Verificar conectividad IP
$ ping -c 2 142.250.72.196
PING 142.250.72.196 (142.250.72.196): 56 data bytes
64 bytes from 142.250.72.196: icmp_seq=0 ttl=115 time=12.3 ms
64 bytes from 142.250.72.196: icmp_seq=1 ttl=115 time=12.1 ms
```
El comando `nslookup` muestra cómo el cliente traduce un nombre a IP mediante DNS; `ping` confirma que la ruta IP está operativa.

## Errores comunes
- **Confundir DNS con routing**: DNS solo traduce nombres; el enrutamiento decide el camino. Verificar ambas capas por separado.  
- **Usar máscara de subred incorrecta**: provoca que paquetes se envíen a la puerta de enlace equivocada. Revisar siempre la máscara antes de aplicar rutas estáticas.  
- **Ignorar MTU**: paquetes demasiado grandes pueden fragmentarse o ser descartados, generando pérdida de conectividad. Ajustar MTU o habilitar Path MTU Discovery.

## Estado actual
- **Fundamentos estables**: El modelo cliente‑servidor, la pila TCP/IP y el uso de direcciones IP siguen siendo la base de Internet.  
- **Práctica moderna**: La adopción de IPv6, BGP con comunidades extendidas y el uso de DNSSEC para autenticación de nombres son tendencias actuales que complementan los fundamentos clásicos.

## Conexiones
- **BGP**: Protocolo de enrutamiento que permite a los proveedores de Internet intercambiar rutas y mantener la “red de redes”.  
- **DNSSEC**: Extensión de DNS que protege la integridad de la resolución de nombres, importante para la seguridad de la capa de aplicación.  
- **SD-WAN**: Tecnologías que utilizan la infraestructura de Internet para crear enlaces WAN virtuales con gestión centralizada, aprovechando la ubiquidad de la red global.

## Ruta de estudio
1. **Prerequisitos**: Conceptos de direccionamiento IP, máscara de subred y tabla de rutas estáticas.  
2. **Fundamentos**: DNS, modelo cliente‑servidor, TCP/UDP, y pruebas básicas con `ping`/`traceroute`.  
3. **Enrutamiento dinámico**: OSPF para interior y BGP para exterior; práctica con laboratorios de simulación.  
4. **Seguridad y resiliencia**: DNSSEC, filtros ACL, y configuraciones de BGP con comunidades y Anycast.  
5. **Tecnologías emergentes**: IPv6, SD-WAN y automatización mediante APIs (por ejemplo, NETCONF/YANG).

## Preguntas de repaso
1. ¿Cómo determina un router el siguiente salto para un paquete que viaja por Internet?  
2. ¿Qué papel juega DNS en el modelo cliente‑servidor y por qué no es parte del enrutamiento?  
3. ¿Cuál es la diferencia práctica entre usar una ruta estática y un protocolo dinámico como OSPF?  
4. ¿En qué situaciones un problema de conectividad se debe investigar en la capa de transporte (TCP/UDP) en lugar de la capa de red?  
5. ¿Qué ventaja aporta DNSSEC frente a una resolución DNS tradicional?

<!-- trazabilidad: run_id=run-20261105-141644-9d1ecd concept=05-networking-internet-01-internet written_at=2026-11-05T17:17:51.194370+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/01 - Internet & Web|Internet & Web]] · *Frontend*
- [[03 - Backend/01 - Cliente-Servidor|Cliente-Servidor]] · *Backend*
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/07 - DNS|DNS]]

---
[[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/02 - IP|IP]] →
