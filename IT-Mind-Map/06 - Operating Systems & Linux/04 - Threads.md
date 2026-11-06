---
title: "Threads"
area: "Operating Systems / Linux"
numero: 4
aliases: ["Threads"]
tags: [concepto, it/operating-systems-linux]
---
# Threads

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 4 de 25**

## Qué abarca
- Ejecución concurrente dentro de procesos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los threads para dividir el trabajo de un proceso en unidades de ejecución que pueden avanzar simultáneamente en distintas CPUs, lo que me permite aprovechar al máximo el hardware multicore y reducir los tiempos de respuesta de servicios críticos. Resuelvo problemas de latencia y de bloqueo al evitar que una operación lenta (por ejemplo, I/O o cálculo intensivo) detenga todo el proceso. En mi día a día como ingeniero de sistemas Linux senior, creo y depuro threads al diseñar servidores, daemons o scripts que deben atender peticiones concurrentes, y los monitorizo con herramientas como `top`, `htop` o `perf`. Después de entender su ciclo de vida y sincronización, puedo diseñar arquitecturas con pools de threads, evitar condiciones de carrera y escalar aplicaciones. Cuando una tarea es estrictamente secuencial o el proceso es muy ligero, no necesito preocuparme por threads y prefiero mantener la simplicidad con un solo flujo de ejecución.

## Esqueleto (el 20% esencial)
1. **Un thread es una vía de ejecución dentro de un proceso** y comparte memoria, descriptors y entorno con sus hermanos.  
2. **Los threads permiten concurrencia real** al ejecutarse simultáneamente en distintas CPUs bajo el scheduler del kernel.  
3. **La coordinación entre threads se hace mediante primitivas** como mutexes, condition variables y semáforos para evitar condiciones de carrera.  
4. **El kernel Linux implementa threads como tareas ligeras (task_struct)** que aparecen en `/proc` como entradas de proceso con el mismo PID de grupo.  
5. **El rendimiento y la escalabilidad dependen del scheduling** (CFS) y de la afinidad de CPU (CPU affinity).

## Como funciona
1. El proceso llama a `pthread_create` (o a la API de su lenguaje) indicando la función que ejecutará el nuevo thread.  
2. El kernel duplica el contexto de ejecución: crea una nueva estructura `task_struct`, asigna un TID y hereda el espacio de direcciones del proceso padre.  
3. El scheduler coloca el thread en la runqueue de una CPU disponible según la política de scheduling y la afinidad establecida.  
4. Mientras el thread corre, comparte variables globales con los demás threads; cualquier acceso concurrente debe protegerse con mutexes o atomics.  
5. Al terminar, el thread llama a `pthread_exit` o retorna; el proceso puede recoger su estado con `pthread_join` o dejarlo “detached”.  

## Detalles
- **Básico:** Creación y terminación con `pthread_create` / `pthread_join`. Uso de `pthread_self` para obtener el TID.  
- **Intermedio:** Sincronización con `pthread_mutex_lock`, `pthread_cond_wait`, semáforos POSIX (`sem_init`). Afinidad con `pthread_setaffinity_np`.  
- **Avanzado:** Thread‑local storage (`pthread_key_create`), manejo de señales en threads, uso de `clone` para crear threads con atributos personalizados, y técnicas de lock‑free con `std::atomic` o `futex`.  
- **Performance:** Medir uso de CPU con `perf top`, identificar contención de locks con `perf lock`, y ajustar la política de scheduling (`SCHED_RR`, `SCHED_FIFO`) cuando se necesita latencia predecible.  

## Ejemplo minimo
```c
/* hilo.c */
#include <pthread.h>
#include <stdio.h>

void *saludar(void *arg) {
    long id = (long)pthread_self();
    printf("Hola desde el thread %ld\n", id);
    return NULL;
}

int main(void) {
    pthread_t th;
    pthread_create(&th, NULL, saludar, NULL);
    pthread_join(th, NULL);
    return 0;
}
```
**Salida típica:**
```
Hola desde el thread 140735123456768
```
El programa crea un único thread que imprime su identificador y finaliza de forma controlada.

## Errores comunes
- Olvidar `pthread_join` o crear threads “detached” sin liberar recursos → fuga de TID.  
- Acceder a datos compartidos sin mutex → condiciones de carrera y resultados no determinísticos.  
- Usar variables locales del stack del hilo creador después de que el hilo haya terminado → punteros colgantes.  

## Estado actual
Los fundamentos de POSIX threads (`pthread_*`) son estables y forman parte del glibc desde hace décadas, por lo que su comportamiento es predecible en todas las distribuciones modernas de Linux. En la práctica contemporánea, muchos proyectos prefieren capas de abstracción como `std::thread` en C++17 o runtimes de alto nivel (Go, Rust) que delegan en pthreads pero añaden seguridad de tipos y manejo automático de recursos. Herramientas de diagnóstico como `perf`, `bpftrace` y `systemtap` permiten observar la actividad de threads en tiempo real y detectar contención de locks o desbalance de carga entre CPUs.

## Conexiones
- **Concurrency:** Los threads son la unidad básica que permite ejecutar varias tareas al mismo tiempo dentro de un mismo proceso.  
- **Processes:** Un proceso puede contener varios threads; la diferencia clave es que los procesos no comparten espacio de direcciones, mientras que los threads sí.  
- **CPU & Scheduling:** El scheduler del kernel asigna cada thread a una CPU, y la política de scheduling determina la prioridad y la equidad de ejecución entre ellos.  

## Ruta de estudio
1. **Prerequisitos:** Conocimientos sólidos de C, manejo de procesos (`fork`, `exec`), y conceptos de memoria virtual.  
2. **Fundamentos:** API POSIX threads (`pthread_create`, `pthread_join`, mutexes).  
3. **Sincronización:** Condiciones, semáforos, barreras y thread‑local storage.  
4. **Diagnóstico:** Uso de `top/htop`, `ps -L`, `perf`, y `strace` para observar comportamiento de threads.  
5. **Avanzado:** Afinidad de CPU, políticas de scheduling, técnicas lock‑free, y creación de threads con `clone`.  
6. **Aplicaciones:** Implementar pools de threads, servidores multihilo (ej. `nginx` worker processes/threads) y migrar a abstracciones de alto nivel (C++ `std::thread`, Rust `std::thread`).  

## Preguntas de repaso
1. ¿Qué recursos comparte un thread con los demás threads del mismo proceso y por qué es importante sincronizarlos?  
2. ¿Cómo se crea y se finaliza un thread en C usando la API POSIX?  
3. ¿Qué diferencia hay entre un thread “joinable” y uno “detached” y cuándo usar cada uno?  
4. ¿De qué manera el scheduler del kernel afecta la ejecución concurrente de varios threads?  
5. ¿Cuál es la ventaja de usar `pthread_setaffinity_np` en una aplicación multihilo intensiva en CPU?

<!-- trazabilidad: run_id=run-20261105-204002-56e07b concept=06-operating-systems-linux-04-threads written_at=2026-11-05T23:43:12.869983+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/11 - Concurrency|Concurrency]] · *Software Engineering*
- [[02 - Frontend/09 - Asincronía|Asincronía]] · *Frontend*
- [[03 - Backend/20 - Asincronía & Concurrencia|Asincronía & Concurrencia]] · *Backend*
- [[06 - Operating Systems & Linux/03 - Processes|Processes]]
- [[06 - Operating Systems & Linux/05 - CPU & Scheduling|CPU & Scheduling]]

---
← [[06 - Operating Systems & Linux/03 - Processes|Processes]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/05 - CPU & Scheduling|CPU & Scheduling]] →
