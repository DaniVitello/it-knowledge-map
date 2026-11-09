---
title: "Stack & Heap"
area: "Operating Systems / Linux"
numero: 7
aliases: ["Stack & Heap"]
tags: [concepto, it/operating-systems-linux]
---
# Stack & Heap

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 7 de 25**

## Qué abarca
- Organización de memoria de los procesos

## Mis notas
<!-- ai:start -->
## Objetivo  
Utilizo el stack y el heap para organizar la memoria de cada proceso que administro en Linux. Resuelvo problemas de asignación dinámica y de gestión de variables locales, evitando desbordamientos y fugas que pueden colapsar servicios críticos. Aparecen cada vez que compilo o depuro aplicaciones, cuando analizo core dumps o reviso el consumo de RAM con `pmap` o `smem`. Después de comprender su funcionamiento, puedo optimizar el uso de memoria, detectar errores de acceso y diseñar programas que escalen sin agotar recursos. Cuando trabajo solo con scripts o binarios que no manejan memoria explícita, no necesito preocuparme por estos detalles.

## Esqueleto (el 20% esencial)  
1. **Stack**: zona de memoria de crecimiento descendente donde se guardan variables locales y marcos de pila de funciones.  
2. **Heap**: zona de crecimiento ascendente usada por la asignación dinámica (`malloc`, `new`).  
3. **Límites físicos**: el kernel define un límite superior para el stack y un límite inferior para el heap dentro del espacio de direcciones del proceso.  
4. **Colisión**: si stack y heap se expanden demasiado pueden encontrarse, provocando fallos de segmentación.  

## Como funciona  
1. Al crear un proceso, el kernel reserva un espacio de direcciones virtuales y fija el punto de partida del stack (por ejemplo, `0x7ff…`).  
2. Cada llamada a función empuja un *frame* al stack; al retornar, el frame se desapila.  
3. Cuando el programa solicita memoria con `malloc`, el runtime pide al kernel más páginas para el heap mediante `brk` o `mmap`.  
4. El heap crece hacia direcciones más altas mientras el stack crece hacia direcciones más bajas; el kernel vigila que no se crucen.  
5. Si la aplicación supera los límites, el kernel genera `SIGSEGV` y el proceso termina.

## Detalles  
- **Básico**: el stack está limitado por `ulimit -s`; el heap está limitado por la disponibilidad de RAM y por `ulimit -v`.  
- **Intermedio**: el uso de `mprotect` permite marcar páginas del stack como no ejecutables (protección *NX*) y el heap puede fragmentarse; herramientas como `valgrind` detectan fugas.  
- **Avanzado**: técnicas de *stack canaries* y *address space layout randomization* (ASLR) refuerzan la seguridad; el heap puede gestionarse con allocadores alternativos (`jemalloc`, `tcmalloc`) para reducir fragmentación y mejorar rendimiento en servidores de alta carga.

## Ejemplo minimo  
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int stack_var = 42;
    int *heap_var = malloc(sizeof(int));
    *heap_var = 99;

    printf("Dirección stack_var : %p\n", (void *)&stack_var);
    printf("Dirección heap_var  : %p\n", (void *)heap_var);

    free(heap_var);
    return 0;
}
```
Salida típica (las direcciones varían por ASLR):  
```
Dirección stack_var : 0x7ffd5c3a1abc
Dirección heap_var  : 0x602010
```

## Errores comunes  
- **Desbordar el stack** con recursión infinita → usar recursión limitada o convertir a iteración.  
- **Olvidar liberar** memoria del heap → usar `valgrind --leak-check=full` o patrones RAII.  
- **Confundir punteros** entre stack y heap → revisar la procedencia del puntero antes de liberarlo.  

## Estado actual  
- **Fundamentos estables**: la arquitectura de stack/heap y los syscalls `brk`/`mmap` no han cambiado desde hace décadas en Linux.  
- **Práctica moderna**: la mayoría de distribuciones habilitan ASLR por defecto; los allocadores de alto rendimiento (`jemalloc`, `tcmalloc`) son recomendados para aplicaciones de servidor que manejan gran cantidad de objetos dinámicos.  

## Conexiones  
- **Processes**: cada proceso posee su propio espacio de direcciones con stack y heap independientes.  
- **Memory Management**: el kernel administra la asignación de páginas al stack y al heap mediante su subsistema de gestión de memoria.  
- **Security**: mecanismos como ASLR y stack canaries dependen de la separación y protección del stack y el heap.  

## Ruta de estudio  
1. Prerrequisitos: comprensión de direcciones virtuales, syscalls `brk` y `mmap`, y uso de `ulimit`.  
2. Estudio básico: leer la sección *Memory Layout* del manual de `proc(5)` y experimentar con `pmap`.  
3. Intermedio: practicar con `valgrind` y `gdb` para observar el crecimiento del stack y del heap en tiempo real.  
4. Avanzado: comparar allocadores (`glibc malloc` vs `jemalloc`) y habilitar opciones de seguridad (`execstack -s`, `gcc -fstack-protector`).  

## Preguntas de repaso  
1. ¿Qué diferencia hay entre la dirección de una variable local y la de una variable obtenida con `malloc`?  
2. ¿Cómo impide el kernel que el stack y el heap se colisionen?  
3. ¿Qué comando permite visualizar el límite máximo de stack para un proceso?  
4. ¿Cuál es el efecto de habilitar ASLR sobre las direcciones mostradas en el ejemplo mínimo?  
5. ¿Por qué un allocador alternativo como `jemalloc` puede mejorar el rendimiento de una aplicación de servidor?

<!-- trazabilidad: run_id=run-20261106-224333-7af9e2 concept=06-operating-systems-linux-07-stack-heap written_at=2026-11-07T01:44:29.114288+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/03 - Processes|Processes]]
- [[06 - Operating Systems & Linux/06 - Memory Management|Memory Management]]

---
← [[06 - Operating Systems & Linux/06 - Memory Management|Memory Management]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/08 - File Systems|File Systems]] →
