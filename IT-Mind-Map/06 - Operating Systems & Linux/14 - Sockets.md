---
title: "Sockets"
area: "Operating Systems / Linux"
numero: 14
aliases: ["Sockets"]
tags: [concepto, it/operating-systems-linux]
---
# Sockets

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 14 de 25**

## Qué abarca
- Comunicación entre procesos/red

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo sockets para establecer canales de comunicación entre procesos, ya sea dentro del mismo host o a través de la red, lo que me permite intercambiar datos de forma estructurada y fiable. Resuelvo el problema de cómo un proceso cliente solicita un servicio a un proceso servidor sin depender de archivos temporales ni de mecanismos de señalización limitados. En mi día a día como ingeniero de sistemas Linux senior, los sockets aparecen al depurar servicios de red, al crear herramientas de monitoreo o al conectar contenedores. Después de comprender su uso, puedo diseñar servidores multihilo, implementar clientes ligeros y diagnosticar cuellos de botella de red. Cuando la interacción se limita a llamadas locales muy simples, puedo prescindir de sockets y usar pipes o shared memory.

## Esqueleto (el 20% esencial)
1. **Creación de un endpoint** – Un proceso abre un socket y lo asocia a un puerto o a un archivo de dominio Unix.  
2. **Establecimiento de la conexión** – El cliente solicita conectar al endpoint del servidor mediante `connect()` o `accept()`.  
3. **Intercambio de datos** – Se usan `read()/write()` o `send()/recv()` para transferir bytes.  
4. **Cierre ordenado** – `close()` libera el descriptor y notifica al peer.  

## Como funciona
1. El proceso llama a `socket()` indicando familia (AF_INET o AF_UNIX) y tipo (SOCK_STREAM para TCP).  
2. El servidor ejecuta `bind()` para reservar un puerto y `listen()` para aceptar peticiones.  
3. Cada cliente ejecuta `connect()`; el kernel realiza el handshake TCP (SYN‑SYN/ACK‑ACK) y crea una tabla de sockets vinculada al proceso.  
4. Cuando el servidor llama a `accept()`, el kernel devuelve un nuevo descriptor que representa la conexión establecida.  
5. Ambos extremos usan `send()`/`recv()` (o `write()`/`read()`) para mover datos; el kernel gestiona buffers y notifica disponibilidad mediante `select()`/`poll()`.  
6. Al terminar, cualquiera de los procesos llama a `close()`, lo que envía FIN y libera recursos.

## Detalles
- **Básico**: sockets de dominio Unix (`AF_UNIX`) para comunicación local sin sobrecarga de red.  
- **Intermedio**: sockets IPv4 (`AF_INET`) con `SOCK_STREAM` (TCP) garantizan entrega ordenada y control de congestión; se pueden ajustar opciones con `setsockopt()` (p. ej., `SO_REUSEADDR`).  
- **Avanzado**: sockets no bloqueantes (`O_NONBLOCK`) y multiplexación (`epoll`, `poll`) permiten servidores de alta concurrencia; `SOCK_DGRAM` (UDP) sirve para mensajes sin conexión; `SOCK_SEQPACKET` combina características de stream y datagrama.  
- **Seguridad**: `iptables`/`nftables` filtran puertos; `SELinux` controla acceso a sockets de dominio Unix.  
- **Diagnóstico**: `netstat -tulnp`, `ss -ltnp` y `lsof -i` revelan sockets abiertos y procesos asociados.

## Ejemplo minimo
```bash
# Servidor simple (TCP, puerto 12345)
#!/usr/bin/env bash
exec 3<>/dev/tcp/0.0.0.0/12345   # abre socket y asocia descriptor 3
echo "Hola cliente" >&3
cat <&3                         # espera y muestra lo que envíe el cliente
exec 3<&- 3>&-                   # cierra el socket
```

```bash
# Cliente que se conecta al servidor anterior
#!/usr/bin/env bash
exec 3<>/dev/tcp/127.0.0.1/12345
read -r line <&3
echo "Servidor dice: $line"
echo "Respuesta del cliente" >&3
exec 3<&- 3>&-
```
Al ejecutar primero el servidor y luego el cliente, la salida del cliente será:  
`Servidor dice: Hola cliente`

## Errores comunes
- Olvidar `bind()` antes de `listen()`: el servidor no reserva puerto y falla al aceptar.  
- Usar `read()` en un socket bloqueante sin verificar retorno: puede quedar colgado si el peer cierra.  
- No establecer `SO_REUSEADDR` al reiniciar rápidamente un servidor: el puerto queda en TIME_WAIT.  
- Confundir descriptor de archivo con descriptor de socket; siempre cerrar ambos con `close()`.  

## Estado actual
Los conceptos básicos de sockets (creación, bind, listen, accept, connect, send/recv, close) son estables y forman parte del API POSIX desde hace décadas. En la práctica moderna, la mayoría de los servicios de alto rendimiento usan `epoll` (Linux) o `io_uring` para I/O asíncrono, y emplean bibliotecas como **libevent** o **Boost.Asio** que abstraen la complejidad del multiplexado. Los contenedores y microservicios suelen exponer puertos mediante **Docker** y orquestadores (Kubernetes) que gestionan la asignación de sockets a nivel de host.

## Conexiones
- **TCP**: protocolo de transporte que garantiza entrega ordenada y confiable; los sockets tipo `SOCK_STREAM` se basan en él.  
- **Signals**: pueden interrumpir operaciones de I/O bloqueante; `SIGPIPE` se genera si se escribe en un socket cerrado.  
- **Processes IPC**: los sockets de dominio Unix son una forma de IPC que compite y complementa a pipes, shared memory y message queues.

## Ruta de estudio
1. **Prerequisitos**: manejo de procesos (`fork`, `exec`), conceptos de red (IP, puertos) y permisos de archivo.  
2. **Fundamentos**: practicar con `socket()`, `bind()`, `listen()`, `accept()`, `connect()` en scripts Bash y programas C simples.  
3. **Multiplexado**: aprender `select()` y `poll()`, luego `epoll` para escalabilidad.  
4. **Opciones avanzadas**: `setsockopt()` (SO_REUSEADDR, TCP_NODELAY), sockets no bloqueantes y `io_uring`.  
5. **Seguridad y diagnóstico**: usar `ss`, `netstat`, `lsof`, y configurar firewall/NFTables.  
6. **Integración**: explorar bibliotecas de alto nivel (libevent, Boost.Asio) y contenedores Docker que exponen puertos.

## Preguntas de repaso
1. ¿Qué pasos realiza el kernel para transformar una llamada `connect()` en una conexión TCP establecida?  
2. ¿En qué situaciones prefiero un socket de dominio Unix frente a un socket TCP?  
3. ¿Cómo evita `SO_REUSEADDR` que el puerto quede bloqueado después de un reinicio rápido del servidor?  
4. ¿Qué ocurre si un proceso escribe en un socket cuyo peer ya ha cerrado la conexión y no se maneja `SIGPIPE`?  
5. ¿Cuál es la ventaja principal de usar `epoll` en lugar de `select()` en un servidor con miles de conexiones concurrentes?

<!-- trazabilidad: run_id=run-20261109-162745-97e6a8 concept=06-operating-systems-linux-14-sockets written_at=2026-11-09T19:28:54.826264+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/04 - TCP|TCP]] · *Networking / Internet*
- [[05 - Networking & Internet/06 - Puertos|Puertos]] · *Networking / Internet*
- [[05 - Networking & Internet/22 - WebSockets|WebSockets]] · *Networking / Internet*
- [[06 - Operating Systems & Linux/13 - Processes IPC|Processes IPC]]
- [[06 - Operating Systems & Linux/19 - Signals|Signals]]
- [[06 - Operating Systems & Linux/22 - Networking en Linux|Networking en Linux]]

---
← [[06 - Operating Systems & Linux/13 - Processes IPC|Processes IPC]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/15 - Environment Variables|Environment Variables]] →
