---
title: "Memory Management"
area: "Operating Systems / Linux"
numero: 6
aliases: ["Memory Management"]
tags: [concepto, it/operating-systems-linux]
---
# Memory Management

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 6 de 25**

## Qué abarca
- RAM
- memoria virtual
- páginas

## Mis notas
<!-- ai:start -->
## Objetivo  
Utilizo la gestión de memoria para que el kernel asigne, libere y proteja la RAM que necesita cada proceso, evitando colisiones y agotamiento del recurso. Resuelvo problemas de sobre‑uso de memoria, fragmentación y aislamiento entre procesos, que aparecen cada vez que un servicio se vuelve inestable o el sistema se queda sin “free” memory. Con este conocimiento puedo diagnosticar cuellos de botella con `top`, `free` o `/proc/*/smaps`, ajustar parámetros como `vm.overcommit_memory` y diseñar aplicaciones que usen la memoria de forma eficiente. Cuando el sistema está bajo carga ligera y los procesos usan poca RAM, no es necesario profundizar en los detalles de paginación ni de swapping.

## Esqueleto (el 20% esencial)  
1. **RAM física** – espacio de hardware donde se guardan los datos en tiempo real.  
2. **Memoria virtual** – espacio de direcciones lógicas que el kernel mapea a la RAM o a swap.  
3. **Páginas** – unidades de 4 KB (por defecto) que el kernel mueve entre RAM y swap.  
4. **Page tables** – estructuras que traducen direcciones virtuales a físicas.  
5. **Swapping** – mecanismo que desplaza páginas inactivas a disco para liberar RAM.

## Como funciona  
1. Cuando un proceso solicita memoria (`malloc`, `mmap`), el kernel reserva páginas en su espacio de direcciones virtuales.  
2. La tabla de páginas del proceso se actualiza con una entrada “no presente”.  
3. Al primer acceso, se produce un *page fault*; el kernel asigna una página física libre o la recupera de swap.  
4. La página se marca como “present” y el proceso continúa ejecutándose.  
5. Si la RAM se agota, el kernel elige páginas poco usadas (algoritmo LRU) y las escribe a swap, liberando espacio para nuevas asignaciones.

## Detalles  
- **Básico:** `free`, `top` y `/proc/meminfo` muestran la cantidad de RAM libre, usada y en swap.  
- **Intermedio:** `/proc/<pid>/smaps` desglosa el uso por segmento (heap, stack, mmap). Las *page tables* pueden inspeccionarse con `pagemap` (requiere privilegios).  
- **Avanzado:** Ajustes de `vm.swappiness` y `vm.overcommit_memory` controlan cuándo el kernel recurre a swap y cuánta memoria virtual puede reservar sin respaldo físico. Herramientas como `perf` o `trace-cmd` permiten rastrear *page faults* y tiempos de swapping.

## Ejemplo minimo  
```c
/* mm_demo.c */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    size_t sz = 10 * 1024 * 1024;          // 10 MiB
    char *buf = malloc(sz);
    if (!buf) { perror("malloc"); return 1; }

    /* tocar cada página para forzar su asignación */
    for (size_t i = 0; i < sz; i += 4096)
        buf[i] = 0xAA;

    printf("Dirección base: %p\n", (void*)buf);
    sleep(30);   // permite inspeccionar con `pmap <pid>`
    free(buf);
    return 0;
}
```
Compilación y ejecución:  
```bash
$ gcc -O0 -g mm_demo.c -o mm_demo
$ ./mm_demo &
[1] 12345
Dirección base: 0x55c3e2b5c260
$ pmap -x 12345
```
`pmap` muestra que el proceso tiene una región de 10 MiB marcada como **private** y **rw‑**; esas páginas fueron creadas bajo demanda por el *page fault* del bucle.

## Errores comunes  
- **Asumir que `malloc` siempre reserva RAM física** – solo reserva espacio virtual; la RAM se asigna al primer acceso. Evitarlo verificando el consumo real con `pmap` o `smaps`.  
- **Desactivar swap indiscriminadamente** – puede provocar OOM (out‑of‑memory) y caída del sistema; ajustar `swappiness` es más seguro.  
- **Ignorar límites de `ulimit -v`** – procesos pueden ser terminados por el kernel si superan el límite de memoria virtual.

## Estado actual  
- **Fundamentos estables:** modelo de paginación de 4 KB, uso de `/proc` para inspección, algoritmo LRU aproximado para swapping.  
- **Práctica moderna:** uso de *cgroups* para limitar memoria por contenedor, *zswap* y *zram* como compresión de swap en RAM, y *memfd_create* para archivos anónimos de alta velocidad. Estas extensiones están disponibles en kernels ≥ 4.14 y se configuran mediante sysctl o archivos bajo `/sys/fs/cgroup`.

## Conexiones  
- **Processes** – cada proceso posee su propio espacio de direcciones virtuales gestionado por la memoria del kernel.  
- **Stack & Heap** – son regiones dentro del espacio virtual que crecen bajo demanda mediante paginación.  
- **Filesystem** – el swap es un archivo o partición del sistema de archivos que actúa como extensión de la RAM cuando la memoria física se agota.

## Ruta de estudio  
1. **Prerequisitos:** comprensión de procesos Linux, uso de `/proc`, y comandos `top`, `free`.  
2. **Fundamentos:** leer la sección *Memory Management* del *Linux Kernel Documentation*; experimentar con `malloc` y `pmap`.  
3. **Intermedio:** estudiar `/proc/<pid>/smaps`, ajustar `vm.swappiness` y `vm.overcommit_memory`.  
4. **Avanzado:** explorar cgroups v2 (`memory.max`), habilitar *zswap* y *zram*, y usar `perf trace` para analizar *page faults*.  
5. **Especialización:** profundizar en algoritmos de reemplazo de página y en la arquitectura del *page table* (p4d, pud, pmd, pte) en arquitecturas x86_64.

## Preguntas de repaso  
1. ¿Qué ocurre en el kernel cuando un proceso accede a una página virtual que aún no está presente en RAM?  
2. ¿Cómo puedes verificar cuánta memoria física está realmente ocupada por el heap de un proceso?  
3. ¿Qué parámetro controla la propensión del kernel a usar swap antes de liberar RAM?  
4. ¿Cuál es la diferencia práctica entre limitar la RAM con `ulimit -v` y con un cgroup `memory.max`?  
5. ¿En qué situaciones es recomendable habilitar *zswap* en lugar de aumentar la capacidad de swap tradicional?

<!-- trazabilidad: run_id=run-20261109-161214-f64042 concept=06-operating-systems-linux-06-memory-management written_at=2026-11-09T19:12:14.449156+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/03 - Processes|Processes]]
- [[06 - Operating Systems & Linux/07 - Stack & Heap|Stack & Heap]]

---
← [[06 - Operating Systems & Linux/05 - CPU & Scheduling|CPU & Scheduling]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/07 - Stack & Heap|Stack & Heap]] →
