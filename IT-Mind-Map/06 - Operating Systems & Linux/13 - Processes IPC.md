---
title: "Processes IPC"
area: "Operating Systems / Linux"
numero: 13
aliases: ["Processes IPC"]
tags: [concepto, it/operating-systems-linux]
---
# Processes IPC

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 13 de 25**

## Qué abarca
- Comunicación entre procesos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la comunicación entre procesos (IPC) para que dos o más procesos en un mismo host Linux intercambien datos o señales de control sin necesidad de recurrir a archivos temporales. Resuelvo la falta de coordinación que aparece cuando, por ejemplo, un proceso productor genera datos y otro consumidor debe procesarlos en tiempo real. En mi día a día de ingeniero de sistemas, IPC aparece al diseñar demonios, scripts de automatización o al depurar servicios que se comunican mediante tuberías, sockets o señales. Después de entender IPC puedo estructurar aplicaciones más eficientes, aislar fallos y aplicar patrones como “pipeline” o “client‑server”. Cuando los procesos son independientes y no comparten estado, no necesito preocuparme por IPC.

## Esqueleto (el 20% esencial)
1. **Canales de datos**: tuberías (`pipe`), sockets (`socketpair`, `AF_UNIX`) y memoria compartida permiten pasar bytes entre procesos.  
2. **Sincronización**: señales (`SIGUSR1`, `SIGTERM`) y semáforos coordinan el momento de la lectura/escritura.  
3. **Identificación**: cada proceso tiene un PID; los descriptores de archivo y los nombres de socket sirven para localizar al interlocutor.  
4. **Seguridad**: permisos de archivo y namespaces limitan quién puede crear o usar un canal IPC.  

## Como funciona
1. Un proceso crea un canal IPC (p. ej., `pipe()` o `socketpair()`).  
2. El kernel asigna descriptores de archivo y los asocia a los procesos involucrados.  
3. El proceso escritor escribe bytes en su descriptor; el kernel copia los datos al buffer interno del canal.  
4. El proceso lector lee del descriptor correspondiente; si el buffer está vacío, el kernel lo bloquea o devuelve `EAGAIN` según el modo.  
5. Opcionalmente, el escritor envía una señal (`kill(pid, SIGUSR1)`) para notificar que hay datos disponibles, evitando esperas activas.  

## Detalles
- **Básico**: `pipe()` crea un canal unidireccional; útil para conectar la salida de un comando con la entrada de otro (`ls | grep`).  
- **Intermedio**: `socketpair(AF_UNIX, SOCK_STREAM, 0)` genera un par de sockets bidireccional en el espacio de nombres de Unix, permite comunicación full‑duplex y es la base de muchos demonios.  
- **Avanzado**: memoria compartida (`shm_open`, `mmap`) elimina copias de datos, pero requiere semáforos o mutexes para evitar condiciones de carrera; se usa en bases de datos en memoria o servidores de alto rendimiento.  

## Ejemplo minimo
```bash
#!/usr/bin/env bash
# demo de pipe entre dos procesos
exec 3< <(echo "hola IPC")   # proceso subshell escribe en pipe y lo conecta al fd 3
read -r mensaje <&3         # proceso principal lee del fd 3
echo "Recibido: $mensaje"
```
**Salida**  
```
Recibido: hola IPC
```
El script muestra cómo un proceso hijo escribe en una tubería y el padre la consume sin crear archivos temporales.

## Errores comunes
- Olvidar cerrar el descriptor de escritura en el lector, provocando bloqueos indefinidos; cerrar siempre los descriptores que no se usan.  
- Usar señales para pasar datos grandes; las señales solo transportan un número entero, no payload.  
- Compartir memoria sin sincronización; emplear semáforos o mutexes para proteger la zona crítica.  

## Estado actual
- **Fundamentos estables**: `pipe()`, `socketpair()`, señales POSIX y semáforos System V siguen siendo la base de IPC en Linux.  
- **Práctica moderna**: `eventfd` y `signalfd` permiten tratar eventos y señales como descriptores de archivo, integrándose con `select/poll/epoll`. Las APIs de `memfd_create` y `cgroup` facilitan la creación de áreas de memoria compartida aisladas por contenedores.  

## Conexiones
- **Sockets**: proporcionan un canal de comunicación similar a `pipe` pero con soporte para comunicación bidireccional y uso en redes locales.  
- **Signals**: sirven como mecanismo de notificación ligera para indicar que un proceso debe leer o escribir en un canal IPC.  
- **Shared Memory**: permite compartir grandes volúmenes de datos sin copiar, complementando a los canales basados en bytes cuando el rendimiento es crítico.  

## Ruta de estudio
1. **Prerequisitos**: manejo de procesos (`fork`, `exec`), conceptos de descriptor de archivo y permisos de Unix.  
2. **Fundamentos**: practicar `pipe()`, `socketpair()` y señales con scripts Bash y pequeños programas en C.  
3. **Intermedio**: explorar `select`/`poll` para multiplexar varios canales, y `eventfd` para integrar señales en bucles de I/O.  
4. **Avanzado**: implementar memoria compartida con `shm_open` + `mmap`, usar semáforos POSIX y probar `memfd_create` dentro de contenedores.  
5. **Especialización**: leer la documentación del kernel (`Documentation/filesystems/pipe.txt`) y seguir tutoriales de IPC en proyectos de código abierto (por ejemplo, systemd).  

## Preguntas de repaso
1. ¿Qué diferencia hay entre una tubería (`pipe`) y un `socketpair` en cuanto a dirección y uso?  
2. ¿Cómo se evita que un proceso lector se bloquee indefinidamente cuando la escritura termina?  
3. ¿Por qué una señal no es adecuada para transferir datos arbitrariamente grandes?  
4. ¿Qué ventaja ofrece `eventfd` respecto a una señal tradicional en un bucle `select`?  
5. ¿Cuál es el rol de los semáforos cuando se utiliza memoria compartida entre procesos?

<!-- trazabilidad: run_id=run-20261106-224845-2ed0bb concept=06-operating-systems-linux-13-processes-ipc written_at=2026-11-07T01:49:22.332024+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/14 - Sockets|Sockets]]
- [[06 - Operating Systems & Linux/19 - Signals|Signals]]

---
← [[06 - Operating Systems & Linux/12 - I-O|I/O]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/14 - Sockets|Sockets]] →
