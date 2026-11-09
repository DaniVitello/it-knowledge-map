---
title: "System Calls"
area: "Operating Systems / Linux"
numero: 11
aliases: ["System Calls"]
tags: [concepto, it/operating-systems-linux]
---
# System Calls

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 11 de 25**

## Qué abarca
- Interfaz entre programas y kernel

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo las system calls para que un programa de espacio de usuario pueda solicitar al kernel que realice operaciones críticas como crear procesos, leer o escribir en archivos, o asignar memoria. Resuelvo el problema de la separación entre código de aplicación y recursos protegidos del sistema operativo, evitando que el programa acceda directamente al hardware o a estructuras internas del kernel. En mi día a día como ingeniero Linux senior, las system calls aparecen cada vez que depuro fallos de I/O, analizo consumo de recursos o implemento herramientas que necesitan interactuar con el núcleo. Después de comprenderlas, puedo diseñar scripts y binarios que usen la API del kernel de forma segura, o crear wrappers en C/Python que expongan funcionalidades avanzadas. Cuando utilizo únicamente comandos de alto nivel (por ejemplo `ls` o `systemd`), no necesito preocuparme por las system calls subyacentes.

## Esqueleto (el 20% esencial)
1. **Interfaz de usuario‑kernel**: la única vía oficial para que un proceso solicite servicios del kernel.  
2. **Número de llamada y argumentos**: cada system call está identificada por un número y recibe parámetros en registros o en la pila.  
3. **Cambio de modo**: al invocar una system call el CPU pasa de modo usuario a modo kernel, ejecutando código privilegiado.  
4. **Resultado y errno**: el kernel devuelve un valor (éxito o descriptor) y, en caso de error, establece `errno`.  
5. **Mecanismo de retorno**: la ejecución vuelve al proceso en modo usuario con el control del flujo.

## Como funciona
1. El proceso prepara los argumentos y coloca el número de la system call en el registro `rax` (x86‑64).  
2. Ejecuta la instrucción `syscall` (o `int 0x80` en arquitecturas antiguas).  
3. El CPU cambia a modo kernel y el scheduler dirige la interrupción al handler correspondiente dentro del kernel.  
4. El handler valida los argumentos, accede a recursos protegidos y ejecuta la operación solicitada (p. ej., abrir un archivo).  
5. Al terminar, el kernel escribe el valor de retorno en `rax` y, si hubo error, coloca el código en `errno`.  
6. El CPU vuelve a modo usuario y el proceso continúa con la siguiente instrucción, leyendo el resultado.

## Detalles
- **Básico**: conocer las system calls más usadas (`read`, `write`, `open`, `close`, `fork`, `execve`).  
- **Intermedio**: entender la tabla de system calls del kernel (`/proc/kallsyms` o `syscall_64.tbl`) y cómo se mapean a funciones internas (`do_sys_open`, `sys_clone`).  
- **Avanzado**: manipular la tabla mediante módulos de kernel, interceptar llamadas con `ptrace` o `seccomp`, y crear nuevas system calls mediante `syscall_register`.  
- **Seguridad**: `errno` permite a la aplicación reaccionar a fallos como permisos insuficientes o recursos agotados; el kernel verifica siempre los punteros de usuario para evitar vulnerabilidades.  
- **Rendimiento**: cada cambio de modo implica overhead; por eso se usan técnicas como `vDSO` para operaciones de tiempo sin entrar al kernel.

## Ejemplo minimo
```c
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>

int main(void) {
    const char *msg = "Hola\n";
    /* syscall número 1 = write en x86‑64 */
    long ret = syscall(SYS_write, STDOUT_FILENO, msg, 5);
    printf("write returned %ld\n", ret);
    return 0;
}
```
Salida típica:
```
Hola
write returned 5
```
El programa llama directamente a la system call `write` mediante `syscall(2)` y muestra el número de bytes escritos.

## Errores comunes
- Pasar punteros no validados → kernel devuelve `EFAULT`.  
- Usar número de llamada incorrecto para la arquitectura → `ENOSYS`.  
- Olvidar cerrar descriptors → fuga de recursos; usar `close` siempre que sea posible.  
- Ignorar `errno` → la aplicación puede continuar con datos corruptos.  

## Estado actual
- **Fundamentos estables**: la tabla de system calls y la convención de número/registro son parte del ABI de Linux y cambian solo entre versiones mayores del kernel.  
- **Práctica moderna**: se favorece el uso de bibliotecas de alto nivel (`glibc`) que envuelven las system calls y gestionan `errno` automáticamente; sin embargo, herramientas de diagnóstico (strace, perf) y contenedores de seguridad (`seccomp`) siguen interactuando directamente con la lista de llamadas del kernel.

## Conexiones
- **Filesystem**: `open`, `read` y `write` son system calls que permiten al proceso acceder al árbol de directorios gestionado por el VFS.  
- **Process Management**: `fork`, `execve` y `waitpid` son llamadas que crean y controlan la vida de los procesos, vinculándose al scheduler del kernel.  
- **Security**: `ptrace` y `seccomp` utilizan system calls para inspeccionar o filtrar otras llamadas, integrándose con el subsistema de control de acceso del kernel.

## Ruta de estudio
1. **Prerequisitos**: conocimientos de arquitectura de CPU (modos usuario/kernel), manejo de punteros en C y conceptos de procesos en Linux.  
2. **Fundamentos**: leer `man 2 syscall`, experimentar con `strace` para observar llamadas reales.  
3. **Intermedio**: explorar `/usr/include/asm/unistd.h` y la tabla `syscall_64.tbl` del kernel; escribir programas que usen `syscall(2)` directamente.  
4. **Avanzado**: estudiar `ptrace(2)`, `seccomp(2)` y la creación de módulos que añadan nuevas system calls; analizar el código fuente del kernel en `kernel/sys.c`.  

## Preguntas de repaso
1. ¿Qué ocurre en el CPU cuando un proceso ejecuta la instrucción `syscall`?  
2. ¿Cómo se comunica el kernel con el proceso cuando una system call falla?  
3. ¿Por qué es importante cerrar los descriptors de archivo después de usarlos?  
4. ¿Qué ventaja ofrece `vDSO` respecto a una system call tradicional?  
5. ¿Cómo podrías interceptar una system call específica para auditoría de seguridad?

<!-- trazabilidad: run_id=run-20261109-162701-efcae7 concept=06-operating-systems-linux-11-system-calls written_at=2026-11-09T19:27:44.289418+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/01 - Operating System|Operating System]]
- [[06 - Operating Systems & Linux/02 - Kernel|Kernel]]

---
← [[06 - Operating Systems & Linux/10 - Users & Groups|Users & Groups]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/12 - I-O|I/O]] →
