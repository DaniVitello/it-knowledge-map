---
title: "MAC / Ethernet"
area: "Networking / Internet"
numero: 9
aliases: ["MAC / Ethernet"]
tags: [concepto, it/networking-internet]
---
# MAC / Ethernet

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 9 de 25**

## Qué abarca
- Comunicación dentro de una red local

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la dirección MAC y el marco Ethernet para identificar de forma única cada interfaz de red dentro de una LAN y para encaminar los paquetes en el nivel de enlace. Resuelvo problemas de conectividad local cuando un host no puede comunicarse con otro a pesar de estar en la misma subred, ya que la causa suele estar en la asignación o reconocimiento de direcciones MAC. En mi día a día como ingeniero de redes senior, reviso tablas ARP, inspecciono tramas con tcpdump y configuro filtros basados en MAC para aislar fallas. Después de comprender cómo se forman y procesan los marcos Ethernet, puedo diseñar políticas de seguridad por dirección MAC, depurar bucles de capa 2 y validar la correcta operación de protocolos como DHCP y ARP. Cuando el tráfico ya está en la capa IP y la red está segmentada por routers, la MAC deja de ser relevante y no necesito preocuparme por ella.

## Esqueleto (el 20% esencial)
1. **Dirección MAC única** – Cada NIC tiene una MAC de 48 bits que la identifica en la LAN.  
2. **Marco Ethernet** – La MAC envuelve los datos en un encabezado/trailer que permite la entrega fiable dentro del segmento.  
3. **Resolución de MAC** – ARP traduce una IP a la MAC correspondiente; DHCP entrega la MAC al servidor para asignar una IP.  
4. **Filtrado y seguridad** – Los switches usan la MAC para aprender puertos y aplicar listas de control (ACL) de capa 2.  

## Como funciona
1. Un host genera un paquete IP y lo entrega a la capa 2.  
2. La NIC encapsula el paquete en un marco Ethernet, insertando su propia MAC como **source** y la MAC del destino como **destination**.  
3. Si la MAC de destino es desconocida, el host envía una petición ARP broadcast; el propietario de la IP responde con su MAC.  
4. El switch recibe el marco, aprende la MAC‑source en el puerto de entrada y reenvía el marco solo por los puertos que tienen la MAC‑destino en su tabla de encaminamiento.  
5. Cuando el host recibe un marco con su MAC‑destino, extrae el payload IP y lo pasa a la capa 3.  

## Detalles
- **Básico**: Formato del encabezado Ethernet (preamble, destination MAC, source MAC, EtherType, CRC).  
- **Intermedio**: Operación de switches de aprendizaje, manejo de broadcast ARP y de tráfico DHCP (DISCOVER/REQUEST).  
- **Avanzado**: VLAN tagging (802.1Q) que añade un campo de identificación de VLAN manteniendo la MAC; protocolos de prevención de bucles como STP que dependen de la tabla MAC; filtrado dinámico con 802.1X y listas de control basadas en MAC.  

## Ejemplo minimo
```bash
# Captura de un solo marco Ethernet y muestra direcciones MAC
sudo tcpdump -i eth0 -e -c 1
```
Salida típica:
```
12:34:56.789012 eth0 00:1a:2b:3c:4d:5e > ff:ff:ff:ff:ff:ff, ethertype ARP, length 42: Request who-has 192.168.1.10 tell 192.168.1.5, length 28
```
*Explicación*: `00:1a:2b:3c:4d:5e` es la MAC de origen (mi NIC), `ff:ff:ff:ff:ff:ff` es broadcast porque aún no conozco la MAC del destino; el EtherType indica ARP, que es el mecanismo de resolución de MAC que sigue.  

## Errores comunes
- **Confundir MAC con IP** – La MAC nunca cambia con la topología de capa 3; usarla para rutear fuera de la LAN no funciona.  
- **Ignorar tablas ARP obsoletas** – No limpiar entradas ARP stale puede provocar que se envíen tramas a una MAC que ya no pertenece al host esperado.  
- **Filtrar MAC incorrectamente** – Bloquear la MAC de un servidor crítico corta la conectividad sin que el problema sea evidente en la capa 3.  

## Estado actual
- **Fundamentos estables**: El formato de 48 bits, el proceso de ARP y el aprendizaje de MAC en switches siguen definidos por IEEE 802.3 y son ampliamente compatibles.  
- **Práctica moderna**: El uso de VLANs (802.1Q) y de autenticación 802.1X ha extendido la gestión de MAC más allá del simple aprendizaje, permitiendo segmentación y control de acceso a nivel de enlace. Los switches de capa 2/3 actuales integran tablas MAC con políticas de seguridad dinámicas y exportan eventos a sistemas de monitoreo.  

## Conexiones
- **DHCP**: El servidor DHCP registra la MAC del cliente para asignarle siempre la misma dirección IP mediante reservas.  
- **ARP**: Es el protocolo que traduce la IP que necesita el host a la MAC que debe aparecer en el encabezado Ethernet.  
- **VLAN**: Añade un identificador de VLAN al marco Ethernet manteniendo la MAC, lo que permite segmentar la LAN sin cambiar las direcciones físicas.  

## Ruta de estudio
1. **Prerequisitos**: Modelo OSI, conceptos de IP y subredes, funcionamiento básico de switches.  
2. **Fundamentos**: Estudiar el formato del marco Ethernet y la tabla de direcciones MAC; practicar con `arp -a` y `tcpdump`.  
3. **Intermedio**: Configurar un servidor DHCP y observar cómo registra MAC; implementar filtros MAC en un switch.  
4. **Avanzado**: Implementar VLANs 802.1Q, habilitar 802.1X para control de acceso por MAC y usar STP para evitar bucles mientras se mantiene la coherencia de la tabla MAC.  

## Preguntas de repaso
1. ¿Qué información lleva el encabezado de un marco Ethernet y por qué es esencial para la entrega dentro de una LAN?  
2. ¿Cómo se resuelve la MAC de un host cuando solo se conoce su dirección IP?  
3. ¿Qué papel juega la tabla MAC de un switch al recibir un marco broadcast?  
4. ¿Por qué bloquear una dirección MAC en un switch puede ser más efectivo que bloquear una IP en ciertos escenarios?  
5. ¿Cómo interactúan DHCP y ARP con la dirección MAC durante el proceso de asignación y comunicación inicial?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-09-mac-ethernet written_at=2026-11-05T23:22:00.239042+00:00 -->
<!-- ai:end -->

---
← [[05 - Networking & Internet/08 - DHCP|DHCP]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/10 - ARP|ARP]] →
