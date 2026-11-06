---
title: "Routers"
area: "Networking / Internet"
numero: 12
aliases: ["Routers"]
tags: [concepto, it/networking-internet]
---
# Routers

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 12 de 25**

## Qué abarca
- Dispositivos que interconectan redes

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo routers para conectar dos o más redes distintas y permitir que el tráfico encuentre su camino entre ellas. Resuelvo el problema de que dispositivos en subredes diferentes no pueden comunicarse directamente, ya sea dentro de una empresa, entre sucursales o hacia Internet. En mi día a día como ingeniero de redes senior, configuro routers para establecer rutas, aplicar NAT y segmentar la topología con CIDR. Después de entender cómo funciona un router, puedo diseñar arquitecturas de red escalables, diagnosticar fallos de encaminamiento y optimizar el uso del ancho de banda. No necesito preocuparme por routers cuando todo el tráfico se mantiene dentro de una única LAN sin necesidad de salida a otras redes.

## Esqueleto (el 20% esencial)
1. **Interconexión de redes** – el router recibe paquetes en una interfaz y los envía a otra según la tabla de rutas.  
2. **Encaminamiento (routing)** – decide el mejor camino usando protocolos como OSPF o BGP.  
3. **Traducción de direcciones (NAT)** – permite que múltiples hosts internos compartan una IP pública.  
4. **Segmentación con Subnetting/CIDR** – define rangos de direcciones que el router reconoce como locales o remotas.

## Como funciona
1. Un paquete llega a una de las interfaces del router.  
2. El router inspecciona la dirección IP de destino y la compara con su tabla de rutas.  
3. Si la ruta indica una interfaz local, el paquete se entrega directamente; si indica una red remota, el router lo reenvía por la interfaz correspondiente.  
4. Cuando la salida es a Internet, el router aplica NAT, sustituyendo la IP origen privada por la IP pública configurada.  
5. El proceso se repite en cada salto hasta que el paquete alcanza su destino final.

## Detalles
- **Básico:** Configuración estática de rutas (e.g., `ip route 10.0.0.0/24 192.168.1.1`).  
- **Intermedio:** Implementación de protocolos dinámicos (OSPF, EIGRP) que actualizan la tabla de rutas automáticamente.  
- **Avanzado:** Uso de BGP para intercambio de rutas entre proveedores, políticas de ruta, y NAT de sobrecarga (PAT) para cientos de hosts.

## Ejemplo minimo
```bash
# Configuración mínima en un router Cisco IOS
interface Gig0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown

interface Gig0/1
 ip address 10.0.0.1 255.255.255.0
 no shutdown

ip route 0.0.0.0 0.0.0.0 192.168.1.254   # ruta por defecto hacia Internet
```
Este fragmento crea dos interfaces, asigna subredes y define una ruta por defecto que enviará todo el tráfico no local al ISP.

## Errores comunes
- **Olvidar la ruta por defecto** → el tráfico fuera de las subredes locales se pierde; verifique siempre `ip route 0.0.0.0`.  
- **Superposición de subredes** → causa bucles de encaminamiento; mantenga rangos CIDR únicos.  
- **NAT mal configurado** → hosts internos no pueden acceder a Internet; revise la lista de acceso que define qué tráfico se traduce.

## Estado actual
Los principios de encaminamiento y NAT son estables y se encuentran en todas las plataformas de routing. En la práctica moderna, los routers virtuales (vRouter) y los servicios de routing en la nube (AWS Transit Gateway, Azure Virtual WAN) complementan a los dispositivos físicos, ofreciendo escalabilidad y automatización mediante APIs.

## Conexiones
- **Firewall:** ambos inspeccionan y pueden modificar paquetes; el firewall suele colocarse después del router para aplicar políticas de seguridad.  
- **Load Balancer:** distribuye tráfico entrante que el router ha dirigido a un pool de servidores, mejorando disponibilidad.  
- **SD-WAN:** utiliza routers como nodos de borde para crear enlaces de red sobre Internet, aplicando políticas de ruta basadas en la calidad del enlace.

## Ruta de estudio
1. Prerrequisitos: modelo OSI, direcciones IP, máscara de subred y conceptos básicos de TCP/IP.  
2. Fundamentos: configuración estática de rutas y NAT en routers de línea de comandos.  
3. Intermedio: protocolos dinámicos (OSPF, EIGRP) y conceptos de métricas.  
4. Avanzado: BGP, políticas de ruta, NAT de sobrecarga y arquitectura de routers virtuales en entornos cloud.  
5. Laboratorio: montar una topología con al menos tres routers, implementar OSPF interno y BGP externo, y validar la conectividad con `ping` y `traceroute`.

## Preguntas de repaso
1. ¿Qué papel cumple la tabla de rutas en la decisión de envío de un paquete?  
2. ¿Cómo se diferencia una ruta estática de una aprendida por OSPF?  
3. ¿Qué problema resuelve NAT y por qué es esencial para la conectividad a Internet?  
4. ¿Cuál es la consecuencia de superponer subredes en la configuración de un router?  
5. ¿En qué situaciones elegirías un router virtual en la nube en lugar de un dispositivo físico?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-12-routers written_at=2026-11-05T23:24:57.279259+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/11 - Routing|Routing]]
- [[05 - Networking & Internet/13 - NAT|NAT]]
- [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]]

---
← [[05 - Networking & Internet/11 - Routing|Routing]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/13 - NAT|NAT]] →
