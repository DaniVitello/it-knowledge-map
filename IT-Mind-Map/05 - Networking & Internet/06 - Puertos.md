---
title: "Puertos"
area: "Networking / Internet"
numero: 6
aliases: ["Puertos"]
tags: [concepto, it/networking-internet]
---
# Puertos

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 6 de 25**

## Qué abarca
- Cómo los servicios reciben conexiones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los puertos para indicar a qué servicio o aplicación debe llegar cada paquete que entra a un host. Resuelvo el problema de distinguir múltiples flujos de datos que comparten la misma dirección IP, como cuando un servidor web y un servidor SSH operan simultáneamente. En mi día a día como ingeniero de redes senior, reviso los puertos al diagnosticar accesibilidad de servicios, al diseñar reglas de firewall o al balancear carga entre servidores. Después de comprender cómo funcionan, puedo crear filtros precisos, mapear dependencias de aplicaciones y depurar fallas de conectividad sin interferir en otros servicios. Cuando una aplicación usa exclusivamente la IP sin necesidad de distinguir flujos (por ejemplo, tráfico de broadcast), los puertos no son relevantes.

## Esqueleto (el 20% esencial)
1. **Número de puerto = punto de entrada del servicio** – Cada proceso que escucha en la red abre un puerto concreto (p. ej., 80 para HTTP).  
2. **Rango bien definido** – Puertos 0‑1023 son “well‑known”, 1024‑49151 son “registered”, y 49152‑65535 son “ephemeral”.  
3. **Asociación con protocolo** – Un puerto siempre se usa junto a TCP o UDP, lo que determina si la comunicación es orientada a conexión o no.  
4. **Visibilidad en firewalls y NAT** – Las reglas de filtrado y la traducción de direcciones operan sobre puertos para permitir o bloquear tráfico.  

## Como funciona
1. Una aplicación abre un *socket* y lo enlaza (`bind`) a un número de puerto y a una dirección IP.  
2. El kernel registra ese puerto como disponible para el protocolo indicado (TCP o UDP).  
3. Cuando llega un paquete, el encabezado IP indica la IP de destino y el encabezado de transporte lleva el número de puerto.  
4. El stack de red entrega el paquete al proceso que tiene el socket escuchando en ese puerto.  
5. En TCP, se completa el *handshake* (SYN‑SYN/ACK‑ACK) antes de que la aplicación reciba datos; en UDP, el datagrama se entrega directamente.  

## Detalles
- **Básico:** Puertos bien conocidos permiten que clientes conozcan de antemano el número esperado (p. ej., 22 para SSH).  
- **Intermedio:** Los puertos *ephemeral* son asignados dinámicamente por el cliente para respuestas entrantes; su rango se configura en `/proc/sys/net/ipv4/ip_local_port_range`.  
- **Avanzado:** En entornos con NAT, el router traduce el puerto interno a uno externo, creando una tabla de *port‑forwarding* que permite que servidores internos sean accesibles desde Internet.  
- **Seguridad:** Filtrar puertos en firewalls (iptables, nftables) permite bloquear vectores de ataque sin afectar otros servicios que comparten la misma IP.  

## Ejemplo minimo
```bash
# Servidor simple con netcat escuchando en el puerto 12345 (UDP)
nc -u -l 12345 &
# Cliente envía un mensaje al mismo puerto
echo "hola" | nc -u 127.0.0.1 12345
# Salida del servidor (mostrada en la terminal donde se ejecutó nc):
# hola
```
El servidor recibe el datagrama porque está enlazado al puerto 12345/UDP; el cliente lo dirige a ese mismo número de puerto.

## Errores comunes
- **Confundir TCP y UDP al abrir puertos** – usar el protocolo incorrecto impide la comunicación; verifique siempre el flag `-t` (TCP) o `-u` (UDP) en herramientas.  
- **Asignar puertos ya en uso** – el bind falla y la aplicación no arranca; consulte `netstat -tulpn` antes de elegir.  
- **Olvidar actualizar reglas de firewall** – abrir un puerto en la aplicación pero dejarlo bloqueado en iptables corta el tráfico; sincronice siempre ambas capas.  

## Estado actual
- **Fundamentos estables:** El modelo de puertos (0‑65535) y su asociación con TCP/UDP son parte del estándar IPv4/IPv6 y no han cambiado.  
- **Práctica moderna:** El uso de *port‑knocking* y de firewalls basados en *stateful inspection* (p. ej., nftables) permite abrir puertos sólo tras una secuencia predefinida, reduciendo la superficie de ataque. Además, la tendencia a usar *micro‑segmentación* en entornos de contenedores desplaza la gestión de puertos a nivel de *service mesh* (Istio, Linkerd).  

## Conexiones
- **TCP**: los puertos determinan a qué flujo orientado a conexión se asigna cada segmento, permitiendo multiplexar varias sesiones sobre la misma IP.  
- **UDP**: los puertos permiten que aplicaciones sin estado reciban datagramas independientes, como DNS o VoIP.  
- **Sockets**: la API de sockets expone funciones (`bind`, `listen`, `connect`) que operan directamente sobre números de puerto para establecer la comunicación.  

## Ruta de estudio
1. **Prerequisitos:** comprensión de direcciones IP, modelo OSI, y funcionamiento básico de TCP/UDP.  
2. **Fundamentos:** estudiar el proceso de *binding* de sockets y los rangos de puertos; practicar con `netcat` y `ss`.  
3. **Seguridad:** aprender reglas de iptables/nftables que filtran por puerto; experimentar con NAT y port‑forwarding en un router virtual.  
4. **Avanzado:** explorar *port‑knocking*, *SO_REUSEPORT* y la gestión de puertos en entornos de contenedores (Kubernetes Service, Ingress).  

## Preguntas de repaso
1. ¿Qué diferencia hay entre un puerto “well‑known” y uno “ephemeral” y cuándo se usa cada uno?  
2. ¿Cómo afecta el protocolo (TCP vs UDP) a la forma en que un puerto entrega datos a la aplicación?  
3. Si un firewall bloquea el puerto 443, ¿qué consecuencia tiene para el tráfico HTTPS?  
4. ¿Qué ocurre en la tabla de NAT cuando un cliente interno abre una conexión saliente a un servidor externo?  
5. ¿Cuál es la ventaja de usar *port‑knocking* antes de abrir un puerto en un firewall?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-06-puertos written_at=2026-11-05T23:20:39.165089+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/04 - TCP|TCP]]
- [[05 - Networking & Internet/05 - UDP|UDP]]
- [[06 - Operating Systems & Linux/14 - Sockets|Sockets]] · *Operating Systems / Linux*
- [[06 - Operating Systems & Linux/22 - Networking en Linux|Networking en Linux]] · *Operating Systems / Linux*

---
← [[05 - Networking & Internet/05 - UDP|UDP]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/07 - DNS|DNS]] →
