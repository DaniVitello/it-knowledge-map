---
title: "Processes"
area: "Operating Systems / Linux"
numero: 3
aliases: ["Processes"]
tags: [concepto, it/operating-systems-linux]
---
# Processes

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 3 de 25**

## Qué abarca
- Programas ejecutándose y su ciclo de vida

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los procesos para ejecutar cualquier programa dentro de un sistema Linux, ya sea un script, un daemon o una aplicación interactiva. Resuelvo la necesidad de aislar recursos de CPU, memoria y dispositivos entre tareas concurrentes, lo que permite que el kernel planifique y controle su ejecución sin interferencias. En mi día a día como ingeniero de sistemas senior, administro procesos mediante herramientas como `ps`, `top`, `systemctl` y depuro fallas con `strace` o `gdb`. Al comprender su ciclo de vida (creación, ejecución, terminación) puedo diseñar servicios robustos, optimizar el uso de recursos y diagnosticar cuellos de botella. Después de dominar los procesos, puedo pasar a orquestar contenedores, gestionar clusters o implementar servidores de alta disponibilidad. Cuando una tarea es trivial y se ejecuta en modo batch sin requerir control fino, no es necesario profundizar en su gestión detallada.

## Esqueleto (el 20% esencial)
1. **Creación y fork** – Un proceso nace mediante la llamada `fork()`, copiando el contexto del padre.  
2. **Ciclo de vida** – Transiciones entre estados: running, sleeping, stopped y zombie.  
3. **Planificación (scheduling)** – El scheduler asigna tiempo de CPU según políticas (CFS, realtime).  
4. **Separación de memoria** – Cada proceso tiene su propio espacio de direcciones, con stack y heap aislados.  
5. **Comunicación y control** – Señales, pipes y sockets permiten interacción entre procesos.

## Como funciona
1. Un programa solicitado por el usuario o por otro proceso invoca `fork()`.  
2. El kernel duplica la tabla de procesos, creando un **PID** único y una copia del espacio de direcciones.  
3. El proceso hijo puede ejecutar `execve()` para cargar un nuevo binario, cambiando su imagen de memoria.  
4. El scheduler coloca al proceso en la cola de runnable; cuando le corresponde, el CPU ejecuta sus instrucciones.  
5. Durante la ejecución, el proceso puede bloquearse (sleep) esperando I/O, recibir señales o terminar, pasando a estado zombie hasta que el padre lo recoja con `wait()`.

## Detalles
- **Básico**: `fork()` + `exec()` forman la base de cualquier lanzamiento de programa.  
- **Intermedio**: manejo de señales (`SIGTERM`, `SIGKILL`) y estados de espera (`waitpid()`) para evitar zombies.  
- **Avanzado**: afinación del scheduler mediante `nice`, `renice` o políticas de tiempo real; uso de cgroups para limitar CPU y memoria; depuración con `ptrace` y `strace`.

## Ejemplo minimo
```bash
#!/bin/bash
# Lanzar un proceso en segundo plano y mostrar su PID
sleep 30 &
pid=$!
echo "Proceso sleep lanzado con PID $pid"
ps -p $pid -o pid,stat,cmd
```
**Salida esperada**
```
 PID STAT CMD
12345 S    sleep 30
```
El proceso está en estado `S` (sleeping) esperando que expire el temporizador.

## Errores comunes
- **Olvidar `wait()`**: genera procesos zombie; usar `wait` o `waitpid` para recolectarlos.  
- **Confundir `fork()` y `exec()`**: lanzar `exec` sin `fork` reemplaza el proceso actual.  
- **Asignar señales a PID equivocado**: verificar el PID con `ps` antes de enviar `kill`.  
- **Ignorar límites de recursos**: sin cgroups, un proceso puede consumir toda la CPU o memoria.

## Estado actual
- **Fundamentos estables**: el modelo de procesos POSIX, las llamadas `fork`, `exec`, `wait`, y el scheduler CFS son parte del kernel Linux desde hace décadas.  
- **Práctica moderna**: uso de cgroups v2 para aislamiento de recursos, systemd como gestor de servicios que abstrae gran parte del ciclo de vida, y contenedores (Docker, podman) que encapsulan procesos en namespaces.

## Conexiones
- **Threads** – Los hilos comparten el mismo espacio de direcciones dentro de un proceso, ofreciendo concurrencia más ligera que crear procesos separados.  
- **Memory Management** – El kernel asigna páginas de memoria a cada proceso; la separación evita que un proceso corrompa la memoria de otro.  
- **Daemons / Services** – Los servicios del sistema son procesos que se inician en segundo plano y se gestionan mediante `systemd`, aprovechando el control de estado y reinicio automático.

## Ruta de estudio
1. **Prerequisitos**: conceptos de Linux shell, permisos de usuario y fundamentos de sistemas de archivos.  
2. **Fundamentos**: estudiar las llamadas `fork`, `exec`, `wait` y el modelo de estados de proceso (man 2 fork, man 7 signal).  
3. **Herramientas**: practicar con `ps`, `top`, `htop`, `strace` y `gdb` para inspeccionar procesos en tiempo real.  
4. **Aislamiento**: aprender cgroups y namespaces (man 7 cgroups, man 7 namespaces).  
5. **Orquestación**: explorar systemd unit files y conceptos de contenedores (Dockerfile básico).  
6. **Especialización**: profundizar en políticas de scheduling realtime y tuning de `nice`/`renice`.

## Preguntas de repaso
1. ¿Qué diferencia hay entre el estado *running* y *sleeping* de un proceso?  
2. ¿Por qué es necesario llamar a `wait()` después de un `fork()`?  
3. ¿Cómo afecta la llamada `nice` al comportamiento del scheduler?  
4. ¿En qué se diferencia un hilo de un proceso respecto a la memoria?  
5. ¿Qué herramienta usarías para limitar el consumo de CPU de un proceso sin modificar su código?

<!-- trazabilidad: run_id=run-20261106-173129-f8ea4e concept=06-operating-systems-linux-03-processes written_at=2026-11-06T20:32:13.940301+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/11 - Concurrency|Concurrency]] · *Software Engineering*
- [[03 - Backend/03 - Servidor|Servidor]] · *Backend*
- [[06 - Operating Systems & Linux/04 - Threads|Threads]]
- [[06 - Operating Systems & Linux/05 - CPU & Scheduling|CPU & Scheduling]]
- [[06 - Operating Systems & Linux/06 - Memory Management|Memory Management]]
- [[06 - Operating Systems & Linux/07 - Stack & Heap|Stack & Heap]]
- [[06 - Operating Systems & Linux/20 - Daemons - Services|Daemons / Services]]

---
← [[06 - Operating Systems & Linux/02 - Kernel|Kernel]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/04 - Threads|Threads]] →
