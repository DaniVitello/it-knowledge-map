---
title: "Subnetting / CIDR"
area: "Networking / Internet"
numero: 14
aliases: ["Subnetting / CIDR"]
tags: [concepto, it/networking-internet]
---
# Subnetting / CIDR

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 14 de 25**

## Qué abarca
- División y representación de redes

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el subnetting y CIDR para dividir una red IPv4 o IPv6 en bloques lógicos que se ajusten a la cantidad real de hosts que necesito, evitando el desperdicio de direcciones y simplificando la tabla de enrutamiento. Resuelvo problemas de colisión de direcciones, sobrecarga de rutas y limitaciones de broadcast al diseñar o depurar una infraestructura de campus, data‑center o enlace WAN. En mi día a día, aplico CIDR al planificar subredes para VLAN, al configurar DHCP scopes y al crear listas de control de acceso que dependen de prefijos de red. Después de dominarlo, puedo dimensionar redes, optimizar la agregación de rutas y diagnosticar fallas de conectividad relacionadas con máscaras incorrectas. No necesito preocuparme cuando trabajo exclusivamente con redes muy pequeñas o cuando el proveedor ya entrega subredes predefinidas y no se requiere rediseño.

## Esqueleto (el 20% esencial)
1. **División lógica de una red** – Se asigna a cada segmento un prefijo (ej. /24) que indica cuántas direcciones están disponibles.  
2. **Representación compacta** – CIDR usa notación “dirección/prefijo” en vez de máscara decimal, reduciendo la longitud de las tablas de routing.  
3. **Alineación con routing y NAT** – Los routers agrupan rutas por prefijo y los dispositivos NAT traducen entre prefijos internos y externos.  
4. **Planificación de capacidad** – El cálculo de hosts por subred permite dimensionar DHCP scopes y evitar colisiones.  

## Como funciona
1. Parto de una red base (p. ej. 192.168.0.0/16).  
2. Decido cuántos hosts necesita cada segmento y elijo el prefijo más pequeño que los contenga (p. ej. /24 para ≤254 hosts).  
3. Divido la red base en bloques contiguos que respeten el nuevo prefijo; cada bloque recibe su propia dirección de red y broadcast.  
4. Configuro los interfaces de routers, switches o servidores DHCP con la dirección y el prefijo asignado.  
5. Los routers intercambian prefijos en protocolos de routing (OSPF, BGP); la tabla de rutas muestra entradas como 192.168.1.0/24 → iface eth0.  
6. Cuando un host envía tráfico fuera de su subred, el router usa la tabla de rutas y, si corresponde, NAT para traducir la dirección interna al prefijo público.

## Detalles
- **Básico**: Entender la relación entre bits de red y número de hosts (2ⁿ‑2). Aprender a convertir máscara decimal a prefijo y viceversa.  
- **Intermedio**: Aplicar VLSM (Variable Length Subnet Mask) para mezclar subredes de diferentes tamaños dentro de la misma red base; usar herramientas como `ipcalc` o `cidrcalc`.  
- **Avanzado**: Integrar CIDR en políticas de routing dinámico (redistribución de prefijos, summarization) y en configuraciones de NAT 1:1 o PAT; planificar subredes IPv6 con prefijos /48, /64, etc., donde la regla de 2ⁿ‑2 no se aplica pero la lógica de prefijo sigue vigente.

## Ejemplo minimo
```bash
# Calcular la subred para 50 hosts dentro de 10.0.0.0/16
$ ipcalc 10.0.0.0/16 50
Network:   10.0.0.0/26
Netmask:   255.255.255.192
Broadcast: 10.0.0.63
HostMin:   10.0.0.1
HostMax:   10.0.0.62
Usable:    62
```
El comando muestra que un prefijo /26 (64 direcciones) es suficiente para 50 hosts, dejando 2 direcciones reservadas (network y broadcast).

## Errores comunes
- Usar una máscara demasiado pequeña y quedarse sin direcciones útiles; evitar calculando siempre el prefijo mínimo que cubra los hosts requeridos.  
- Olvidar que la primera y última dirección de cada subred son reservadas; validar con una herramienta antes de asignar.  
- Mezclar subredes de distinto tamaño sin respetar la alineación de bits, lo que genera rutas superpuestas; usar VLSM de forma ordenada.

## Estado actual
- **Fundamentos estables**: La notación CIDR, la regla 2ⁿ‑2 para IPv4 y la lógica de prefijo para IPv6 siguen siendo la base de cualquier diseño de red.  
- **Práctica moderna**: La mayoría de los proveedores de cloud y los equipos de routing soportan automáticamente VLSM y summarization; las configuraciones de DHCP y NAT se realizan mediante plantillas que aceptan prefijos CIDR, reduciendo errores manuales.

## Conexiones
- **IP**: El subnetting determina cómo se segmenta una dirección IP en parte de red y parte de host.  
- **Routing**: Los prefijos CIDR son la unidad mínima que los protocolos de routing intercambian y agregan.  
- **NAT**: La traducción de direcciones depende de los rangos de subred definidos por CIDR para mapear internos a externos.

## Ruta de estudio
1. **Prerequisitos**: Entender binario, máscara de subred decimal y la estructura de una dirección IPv4/IPv6.  
2. **Fundamentos**: Practicar conversiones y cálculos de hosts con `ipcalc`.  
3. **VLSM**: Diseñar escenarios con subredes de tamaños mixtos y validar con simuladores (GNS3, Cisco Packet Tracer).  
4. **Routing dinámico**: Configurar OSPF o BGP y observar cómo se anuncian los prefijos CIDR.  
5. **NAT y DHCP**: Implementar scopes basados en prefijos y reglas NAT que utilicen rangos CIDR.  
6. **IPv6**: Repetir los pasos anteriores con prefijos /48 y /64, enfocándose en la ausencia de broadcast.

## Preguntas de repaso
1. ¿Cómo determino el prefijo CIDR mínimo necesario para una subred que debe soportar 120 hosts?  
2. ¿Qué ocurre con la primera y última dirección de una subred y por qué no pueden asignarse a hosts?  
3. ¿De qué manera el uso de CIDR mejora la tabla de routing de un router OSPF?  
4. ¿Cuál es la diferencia principal entre la regla de 2ⁿ‑2 en IPv4 y la asignación de prefijos en IPv6?  
5. ¿Cómo afecta un error de máscara al proceso de NAT en una red corporativa?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-14-subnetting-cidr written_at=2026-11-05T23:27:06.111593+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/03 - IPv4 - IPv6|IPv4 / IPv6]]
- [[05 - Networking & Internet/08 - DHCP|DHCP]]
- [[05 - Networking & Internet/10 - ARP|ARP]]
- [[05 - Networking & Internet/11 - Routing|Routing]]
- [[05 - Networking & Internet/12 - Routers|Routers]]
- [[05 - Networking & Internet/13 - NAT|NAT]]

---
← [[05 - Networking & Internet/13 - NAT|NAT]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/15 - OSI - TCP-IP Model|OSI / TCP-IP Model]] →
