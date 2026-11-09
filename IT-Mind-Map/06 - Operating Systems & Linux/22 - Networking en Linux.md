---
title: "Networking en Linux"
area: "Operating Systems / Linux"
numero: 22
aliases: ["Networking en Linux"]
tags: [concepto, it/operating-systems-linux]
---
# Networking en Linux

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 22 de 25**

## Qué abarca
- Interfaces
- puertos
- rutas
- sockets

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el networking en Linux para que los procesos del sistema puedan intercambiar datos con otros equipos o con componentes locales mediante la pila TCP/IP. Resuelvo problemas de conectividad, aislamiento de tráfico y diagnóstico de fallos de comunicación que aparecen al configurar servidores, contenedores o al depurar servicios de red. Aparece en la rutina diaria de un ingeniero de sistemas Linux senior cuando se asignan direcciones IP, se crean interfaces virtuales, se inspeccionan puertos abiertos o se trazan rutas. Después de entenderlo puedo diseñar arquitecturas de red seguras, automatizar la puesta en marcha de servicios y usar herramientas de diagnóstico con confianza. No necesito preocuparme cuando la aplicación se ejecuta completamente dentro de un único host sin requerir comunicación externa.

## Esqueleto (el 20% esencial)
1. **Interfaces de red** – puntos de conexión lógicos o físicos que exponen direcciones IP al kernel.  
2. **Puertos y sockets** – endpoints de transporte que permiten a los procesos escuchar o iniciar conexiones.  
3. **Tabla de rutas** – conjunto de reglas que decide por cuál interfaz se envía cada paquete.  
4. **Herramientas de diagnóstico** – `ip`, `ss`, `netstat`, `tcpdump` y `ping` para inspeccionar y validar la configuración.

## Como funciona
1. El kernel crea una **interfaz** (p. ej. `eth0`, `lo`, `tun0`) y le asigna una dirección IP mediante `ip addr add`.  
2. Cada proceso abre un **socket** y lo enlaza a un **puerto** (ej. 80/tcp) con `bind()`.  
3. Cuando el proceso envía datos, el stack TCP/IP consulta la **tabla de rutas** para elegir la interfaz de salida.  
4. El paquete se encapsula y se entrega a la capa de enlace; la NIC lo transmite por la red física o virtual.  
5. En la recepción, la NIC entrega el paquete al kernel, que lo dirige al **socket** correspondiente según puerto y dirección destino.

## Detalles
- **Básico**: `ip link` muestra interfaces; `ip addr` muestra direcciones; `ss -tln` lista sockets escuchando.  
- **Intermedio**: Configuración de VLANs o bridges con `ip link add` y `brctl`; manipulación de la tabla de rutas con `ip route add|del`.  
- **Avanzado**: Uso de namespaces para aislar pilas de red; creación de sockets raw para captura de paquetes; ajuste de parámetros TCP en `/proc/sys/net/ipv4/`.  

## Ejemplo minimo
```bash
# Crear una interfaz loopback adicional y asignarle IP
sudo ip link add name lo:1 type dummy
sudo ip addr add 10.0.0.1/32 dev lo:1
sudo ip link set lo:1 up

# Ver que la interfaz está activa
ip -brief addr show lo:1
```
Salida esperada:
```
lo:1               UNKNOWN        10.0.0.1/32
```
El comando muestra que la interfaz dummy está operativa y lista para usar en pruebas de conectividad local.

## Errores comunes
- Olvidar activar la interfaz (`ip link set up`) y obtener “Destination Host Unreachable”.  
- Asignar una máscara de red incorrecta y generar colisiones de rutas.  
- Usar puertos reservados sin privilegios root, lo que provoca “Permission denied”.  
- No actualizar la tabla de rutas después de cambiar la IP, provocando tráfico que nunca sale.

## Estado actual
Los fundamentos de interfaces, puertos, sockets y rutas son estables y forman parte del kernel Linux desde hace décadas. La práctica moderna incorpora herramientas como `ip` (reemplazo de `ifconfig`) y `ss` (reemplazo de `netstat`), y se apoya en namespaces y containers para aislar entornos de red sin modificar la configuración global del host.

## Conexiones
- **TCP**: protocolo de transporte que utiliza los puertos y sockets para garantizar entrega fiable.  
- **Puertos**: número lógico que identifica la aplicación dentro de un host y permite multiplexar varias conexiones sobre la misma interfaz.  
- **Sockets**: API del kernel que abstrae la comunicación de red y sirve de puente entre procesos y la pila TCP/IP.

## Ruta de estudio
1. Prerrequisitos: conceptos de procesos, permisos de usuario y manejo básico de la línea de comandos.  
2. Fundamentos: `ip` y `ss` para inspeccionar interfaces y sockets.  
3. Intermedio: configuración de rutas estáticas y dinámicas con `ip route` y `dhclient`.  
4. Avanzado: namespaces (`ip netns`), bridges (`brctl`/`ip link`) y captura de paquetes con `tcpdump`.  
5. Especialización: tuning de TCP en `/proc/sys/net/ipv4/` y uso de eBPF para filtrado de tráfico.

## Preguntas de repaso
1. ¿Qué comando muestra la lista de sockets escuchando en puertos TCP?  
2. ¿Cómo se agrega una ruta estática para que todo el tráfico a 192.168.10.0/24 salga por `eth1`?  
3. ¿Cuál es la diferencia práctica entre una interfaz física y una dummy?  
4. ¿Qué ocurre si intentas enlazar un socket a un puerto < 1024 sin ser root?  
5. ¿Cómo puedes aislar la pila de red de un proceso usando namespaces?

<!-- trazabilidad: run_id=run-20261106-225606-4bcf74 concept=06-operating-systems-linux-22-networking-en-linux written_at=2026-11-07T01:56:48.216537+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/04 - TCP|TCP]] · *Networking / Internet*
- [[05 - Networking & Internet/06 - Puertos|Puertos]] · *Networking / Internet*
- [[06 - Operating Systems & Linux/14 - Sockets|Sockets]]

---
← [[06 - Operating Systems & Linux/21 - Package Management|Package Management]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/23 - Logs & System Monitoring|Logs & System Monitoring]] →
