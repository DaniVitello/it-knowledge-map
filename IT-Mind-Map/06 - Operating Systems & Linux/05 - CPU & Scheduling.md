---
title: "CPU & Scheduling"
area: "Operating Systems / Linux"
numero: 5
aliases: ["CPU & Scheduling"]
tags: [concepto, it/operating-systems-linux]
---
# CPU & Scheduling

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 5 de 25**

## Qué abarca
- Cómo el SO distribuye tiempo de CPU

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la planificación de CPU para decidir qué proceso o hilo recibe tiempo de ejecución en cada instante del kernel. Resuelvo la competencia por recursos cuando varios procesos están listos y evito que el sistema se quede bloqueado o que una carga crítica se vea retrasada. Aparece cada vez que administro la carga de trabajo de servidores, ajusto la respuesta de aplicaciones en tiempo real o diagnostico cuellos de botella de rendimiento. Después de entender cómo funciona el scheduler, puedo afinar prioridades con `nice`, aislar cargas con cgroups o elegir políticas de planificación adecuadas. No necesito preocuparme cuando el sistema está bajo carga ligera y todas las tareas son de baja prioridad.

## Esqueleto (el 20% esencial)
1. **Política de planificación** – el kernel elige entre *CFS* (Completely Fair Scheduler) y políticas de tiempo real (*SCHED_FIFO*, *SCHED_RR*) según la naturaleza de la carga.  
2. **Prioridad y peso** – cada tarea tiene una prioridad (tiempo real) o un peso (CFS) que determina su cuota de tiempo de CPU.  
3. **Quantum y re‑programación** – el scheduler asigna un quantum de tiempo; al agotarse, la tarea vuelve a la cola y se selecciona la siguiente.  
4. **Afinidad de CPU** – se puede restringir una tarea a un subconjunto de núcleos para mejorar la localidad de caché.  
5. **Balanceo de carga** – el kernel redistribuye tareas entre CPUs para evitar desequilibrios.

## Como funciona
1. Cuando una tarea pasa a estado *RUNNABLE*, el scheduler la inserta en la cola correspondiente a su política.  
2. En cada tick de timer, el scheduler revisa la cola de mayor prioridad disponible.  
3. Selecciona la tarea con mayor peso (CFS) o la primera en la cola de tiempo real (FIFO/RR).  
4. Asigna el quantum; al terminar o ser preemptada, la tarea vuelve a la cola y el scheduler elige la siguiente.  
5. Si la afinidad está definida, el scheduler solo considera los CPUs permitidos; de lo contrario, el balanceador de carga puede mover la tarea a otro núcleo.

## Detalles
- **Básico**: entender la diferencia entre políticas *CFS* y *RT*; usar `nice` y `renice` para modificar el peso.  
- **Intermedio**: manipular la afinidad con `taskset` o `sched_setaffinity`; observar métricas en `/proc/sched_debug`.  
- **Avanzado**: crear cgroups con control de CPU (`cpu.shares`, `cpu.rt_runtime_us`); ajustar parámetros del kernel como `sched_latency_ns` o `sched_min_granularity_ns` para perfilar cargas específicas.

## Ejemplo minimo
```bash
# Ejecutar una carga CPU intensiva con prioridad baja
nice -n 19 bash -c 'while :; do :; done' &
# Ejecutar una carga de tiempo real con prioridad alta
sudo chrt -f 1 bash -c 'while :; do :; done' &
# Mostrar prioridades y afinidad
ps -eo pid,comm,pri,rtprio,psr | grep -E 'bash'
```
Salida (ejemplo):
```
 1234 bash          39     0   0
 1235 bash          20     1   0
```
El primer proceso tiene `nice` 19 (peso bajo) y se ejecuta en CPU 0; el segundo usa política FIFO con prioridad 1 y también está en CPU 0, pero preemptará al primero cuando necesite CPU.

## Errores comunes
- **Usar `nice` para procesos de tiempo real** – `nice` solo afecta CFS; para latencias críticas se necesita `chrt` o cgroups.  
- **Ignorar afinidad** – asignar muchas tareas a un solo núcleo genera contención de caché; usar `taskset` o el balanceador del kernel.  
- **Modificar parámetros del scheduler sin medir** – cambios como `sched_latency_ns` pueden degradar el rendimiento global; siempre validar con `perf` o `top`.

## Estado actual
- **Fundamentos estables**: el algoritmo CFS y las políticas *SCHED_FIFO*/*SCHED_RR* son parte del kernel Linux desde la versión 2.6 y se mantienen sin cambios estructurales.  
- **Práctica moderna**: el uso de cgroups v2 para control fino de CPU, la exposición de métricas en `/proc/sched_debug` y la integración con systemd‑slice para aislar servicios son habituales en distribuciones actuales.

## Conexiones
- **Concurrency** – la planificación permite que múltiples hilos progresen simultáneamente, gestionando la concurrencia a nivel de CPU.  
- **Processes** – cada proceso contiene una o más tareas que el scheduler coloca en colas según su estado y prioridad.  
- **Threads** – los hilos comparten el mismo espacio de direcciones pero son programados individualmente, por lo que la política de scheduling afecta directamente su rendimiento.

## Ruta de estudio
1. **Prerequisitos**: conceptos de procesos, estados de proceso, y uso básico de la línea de comandos.  
2. **Fundamentos**: leer la documentación de `man sched`, experimentar con `nice`, `renice` y `chrt`.  
3. **Intermedio**: profundizar en `/proc/sched_debug`, probar `taskset` y crear cgroups con `systemd-run --scope`.  
4. **Avanzado**: ajustar parámetros del kernel (`/sys/kernel/debug/sched/`), usar `perf sched` para análisis de latencia y estudiar casos de uso de tiempo real en sistemas embebidos.

## Preguntas de repaso
1. ¿Qué diferencia hay entre una política CFS y una política de tiempo real en Linux?  
2. ¿Cómo afecta el valor de `nice` al peso de una tarea en el scheduler?  
3. ¿Qué comando permite fijar la afinidad de una tarea a un núcleo específico?  
4. ¿Por qué es importante usar cgroups para controlar el uso de CPU en entornos con múltiples servicios?  
5. ¿Qué ocurre cuando el quantum de una tarea se agota y el scheduler la vuelve a colocar en la cola?

<!-- trazabilidad: run_id=run-20261105-204002-56e07b concept=06-operating-systems-linux-05-cpu-scheduling written_at=2026-11-05T23:44:15.674507+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/11 - Concurrency|Concurrency]] · *Software Engineering*
- [[06 - Operating Systems & Linux/03 - Processes|Processes]]
- [[06 - Operating Systems & Linux/04 - Threads|Threads]]

---
← [[06 - Operating Systems & Linux/04 - Threads|Threads]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/06 - Memory Management|Memory Management]] →
