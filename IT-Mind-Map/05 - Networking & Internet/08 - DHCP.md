---
title: "DHCP"
area: "Networking / Internet"
numero: 8
aliases: ["DHCP"]
tags: [concepto, it/networking-internet]
---
# DHCP

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 8 de 25**

## Qué abarca
- Asignación automática de configuración de red

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo DHCP para que los dispositivos que conecto a la red reciban automáticamente una dirección IP, máscara de subred, puerta de enlace y servidores DNS sin necesidad de configurarlos a mano. Resuelvo el problema de la asignación manual y los conflictos de direcciones que aparecen cuando se añaden o quitan equipos frecuentemente, como en oficinas, centros de datos o entornos de pruebas. En mi día a día como ingeniero de redes senior, DHCP es la herramienta que me permite escalar la infraestructura y mantener la consistencia de la configuración mientras gestiono miles de hosts. Después de entender cómo funciona, puedo diseñar políticas de reservas, segmentar subredes mediante scopes y depurar fallas de conectividad relacionadas con la falta de lease. Cuando la red es estática y el número de dispositivos es muy reducido, no necesito preocuparme por DHCP.

## Esqueleto (el 20% esencial)
1. **Asignación automática de parámetros de red** – DHCP entrega IP, máscara, gateway y DNS en tiempo de arranque.  
2. **Proceso de descubrimiento y concesión** – Cliente envía DHCPDISCOVER, servidor responde con DHCPOFFER y finaliza con DHCPACK.  
3. **Scopes y reservas** – Un scope define el rango de direcciones disponible; las reservas garantizan la misma IP a un MAC específico.  
4. **Renovación de lease** – El cliente renueva su lease antes de que expire para mantener la misma configuración.  

## Como funciona
1. El cliente DHCP (por ejemplo, una laptop) se conecta a la red sin IP y envía un broadcast **DHCPDISCOVER**.  
2. Todos los servidores DHCP escuchan el broadcast y, si tienen direcciones libres en su scope, responden con **DHCPOFFER** que incluye una IP propuesta y otros parámetros.  
3. El cliente elige una oferta y envía **DHCPREQUEST** indicando la dirección aceptada.  
4. El servidor confirma con **DHCPACK**, momento en el que el cliente configura su interfaz con la IP, máscara, gateway y DNS recibidos.  
5. Antes de que el lease expire, el cliente envía **DHCPREQUEST** al servidor para renovar; el servidor responde con **DHCPACK** o **DHCPNAK** si la renovación falla.

## Detalles
- **Básico**: El intercambio de mensajes se realiza sobre UDP (puertos 67/68) y utiliza broadcast mientras el cliente no tiene IP.  
- **Intermedio**: Los scopes pueden dividirse por VLAN o por rango de direcciones, y se pueden aplicar opciones DHCP (por ejemplo, opción 6 para DNS). Las reservas se configuran vinculando una MAC a una IP dentro del scope.  
- **Avanzado**: En entornos IPv6 se usa DHCPv6, que opera sobre UDP/546‑547 y permite asignar prefijos y parámetros de capa de enlace. También se pueden implementar failover entre servidores DHCP para alta disponibilidad y usar filtros de relay (DHCP relay) para extender el servicio a subredes remotas.

## Ejemplo minimo
```bash
# En una máquina cliente Linux sin IP configurada
sudo dhclient -v                 # solicita una dirección vía DHCP (modo verboso)

# Salida típica (resumida)
Listening on LPF/eth0/00:11:22:33:44:55
Sending on   LPF/eth0/00:11:22:33:44:55
DHCPDISCOVER on eth0 to 255.255.255.255 port 67 interval 3
DHCPOFFER of 192.168.1.45 from 192.168.1.1
DHCPREQUEST for 192.168.1.45 on eth0 to 255.255.255.255 port 67
DHCPACK of 192.168.1.45 from 192.168.1.1
bound to 192.168.1.45 -- renewal in 3600 seconds.
```

## Errores comunes
- **Olvidar habilitar el relay**: los clientes en subredes distintas no reciben ofertas; se soluciona configurando un DHCP relay en el router.  
- **Rangos de scope que se solapan**: genera conflictos de IP; evitar solapamientos revisando la planificación de subredes.  
- **Lease demasiado corto**: provoca renovaciones frecuentes y carga innecesaria; ajustar el tiempo de lease según la estabilidad de la red.  

## Estado actual
- **Fundamentos estables**: El modelo cliente‑servidor basado en UDP, los mensajes DISCOVER/OFFER/REQUEST/ACK y la gestión de leases siguen definidos por RFC 2131 (IPv4) y RFC 3315 (IPv6).  
- **Práctica moderna**: Los servidores DHCP integrados en plataformas como ISC dhcpd, Microsoft DHCP y soluciones en la nube (AWS VPC DHCP Options) añaden funcionalidades de alta disponibilidad, integración con DNS dinámico y políticas basadas en etiquetas. En entornos de contenedores, se emplean servidores DHCP ligeros (dnsmasq) o se delega la asignación a orquestadores (Kubernetes CNI).  

## Conexiones
- **IP** – DHCP asigna direcciones IP a los hosts, evitando la configuración manual y los conflictos.  
- **ARP** – Una vez que el cliente tiene su IP, usa ARP para descubrir la MAC de la puerta de enlace y de otros hosts en la misma subred.  
- **Subnetting / CIDR** – Los scopes de DHCP se definen en base a bloques CIDR; la máscara de subred entregada por DHCP determina el rango de direcciones válidas para el host.  

## Ruta de estudio
1. **Prerequisitos**: comprensión de direcciones IP, máscaras, broadcast y del protocolo ARP.  
2. **Fundamentos DHCP**: estudiar el flujo de mensajes (DISCOVER, OFFER, REQUEST, ACK) y la configuración de scopes en un servidor básico (ISC dhcpd).  
3. **Avanzado**: implementar reservas, DHCP relay y failover; explorar DHCPv6 y opciones avanzadas (PXE, DNS).  
4. **Integración**: combinar DHCP con DNS dinámico (DDNS) y con herramientas de orquestación (Kubernetes CNI, Docker).  
5. **Seguridad y monitoreo**: aprender a usar filtros DHCP, VLANs aisladas y logs de lease para detectar anomalías.  

## Preguntas de repaso
1. ¿Qué mensajes intercambia un cliente DHCP antes de obtener una dirección IP?  
2. ¿Cómo afecta la longitud del lease a la carga del servidor y a la estabilidad de la red?  
3. ¿En qué situación es necesario configurar un DHCP relay y por qué?  
4. ¿Cuál es la diferencia principal entre DHCP para IPv4 y DHCPv6?  
5. ¿Cómo se relaciona una reserva DHCP con la dirección MAC de un dispositivo?

<!-- trazabilidad: run_id=run-20261106-224132-c99f9a concept=05-networking-internet-08-dhcp written_at=2026-11-07T01:42:18.124658+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/03 - IPv4 - IPv6|IPv4 / IPv6]]
- [[05 - Networking & Internet/10 - ARP|ARP]]
- [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]]

---
← [[05 - Networking & Internet/07 - DNS|DNS]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/09 - MAC - Ethernet|MAC / Ethernet]] →
