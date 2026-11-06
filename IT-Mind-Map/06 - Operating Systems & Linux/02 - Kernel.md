---
title: "Kernel"
area: "Operating Systems / Linux"
numero: 2
aliases: ["Kernel"]
tags: [concepto, it/operating-systems-linux]
---
# Kernel

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 2 de 25**

## Qué abarca
- Núcleo que conecta software y hardware

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el kernel como la capa que traduce las peticiones de los programas en acciones sobre el hardware y gestiona recursos como CPU, memoria y dispositivos. Resuelvo problemas de aislamiento, planificación y acceso seguro a los recursos del sistema, que aparecen cada vez que configuro servicios, depuro cuelgues o ajusto el rendimiento de un servidor Linux. Después de comprender cómo funciona el kernel, puedo interpretar logs del núcleo, ajustar parámetros de `sysctl`, compilar módulos a medida o incluso personalizar una distribución mínima. Cuando sólo ejecuto aplicaciones de usuario y el hardware funciona sin incidencias, no es necesario profundizar en el kernel.

## Esqueleto (el 20% esencial)
1. **Núcleo central** – El kernel es el único código que se ejecuta en modo privilegiado y controla todo el hardware.  
2. **Abstracción de recursos** – Presenta CPU, memoria y dispositivos como objetos manejables mediante APIs estandarizadas.  
3. **Mecanismo de comunicación** – System calls son la puerta de entrada que permite a los procesos solicitar servicios al kernel.  
4. **Gestión de módulos** – El kernel puede cargar y descargar código (módulos) en tiempo de ejecución para ampliar su funcionalidad.  
5. **Política vs. mecanismo** – El kernel implementa políticas de planificación y seguridad que los administradores pueden parametrizar.

## Como funciona
1. Al arrancar, el bootloader carga la imagen del kernel en memoria y lo transfiere al modo kernel.  
2. El kernel inicializa subsistemas críticos (scheduler, memory manager, drivers).  
3. Cada proceso que necesita interactuar con el hardware ejecuta una *system call* (p. ej. `open`, `read`).  
4. El kernel valida la petición, traduce la llamada a una operación concreta sobre el hardware o un recurso interno y devuelve el resultado al proceso.  
5. Si se requiere funcionalidad adicional, el kernel carga un módulo mediante `insmod`/`modprobe`, que registra nuevas system calls o controladores.  

## Detalles
- **Básico**: El ciclo de vida de una system call (entrada, validación, ejecución, salida) y la tabla de interrupciones que enlaza eventos de hardware con manejadores del kernel.  
- **Intermedio**: Planificación de procesos (CFS en Linux), gestión de memoria (paging, cgroups) y virtualización de dispositivos mediante `udev`.  
- **Avanzado**: Compilación de un kernel personalizado, uso de `kprobes` para instrumentar código en vivo, y desarrollo de módulos que interactúan con subsistemas como netfilter o BPF.

## Ejemplo minimo
```bash
# Mostrar la versión del kernel y su configuración básica
$ uname -r
5.15.0-78-generic

# Ver el registro de arranque del kernel
$ dmesg | head -n 5
[    0.000000] Linux version 5.15.0-78-generic (buildd@lcy01-amd64-025) (gcc (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #86-Ubuntu SMP Fri Sep 15 14:30:00 UTC 2023
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-78-generic root=UUID=... ro quiet splash
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
```
*Salida*: `uname -r` muestra la versión exacta del kernel que está gestionando el hardware; `dmesg` permite inspeccionar los mensajes que el kernel emitió durante el arranque, útil para diagnosticar fallos de drivers o de inicialización.

## Errores comunes
- **Modificar parámetros del kernel sin validar** → puede provocar inestabilidad; usar `sysctl -a` para inspeccionar valores antes de cambiarlos.  
- **Cargar módulos incompatibles** → genera “invalid module format”; compilar el módulo contra la misma versión de cabecera del kernel.  
- **Confundir system call con comando de shell** → los comandos son implementaciones en espacio de usuario que usan system calls; no se pueden ejecutar directamente en el kernel.

## Estado actual
- **Fundamentos estables**: La arquitectura monolítica con módulos, la tabla de system calls y el scheduler CFS son conceptos maduros y ampliamente documentados.  
- **Práctica moderna**: Uso de eBPF para extender el kernel sin recompilar, integración de cgroups v2 para aislamiento de recursos, y despliegue de kernels “live‑patched” mediante Ksplice o KernelCare para corregir vulnerabilidades sin reinicio.

## Conexiones
- **System Calls**: Son la interfaz que permite a los procesos solicitar servicios al kernel, convirtiendo llamadas de alto nivel en acciones de bajo nivel.  
- **Operating System**: El kernel constituye el corazón del sistema operativo; sin él, no existiría la capa que coordina hardware y software.  
- **Filesystem**: El kernel implementa VFS (Virtual File System), que abstrae diferentes sistemas de archivos y permite que los procesos accedan a datos de forma uniforme.

## Ruta de estudio
1. **Prerequisitos**: Conocimientos básicos de Linux (comandos, permisos) y de arquitectura de procesos.  
2. **Fundamentos**: Lectura de “Linux Kernel Development” (capítulos de arquitectura y system calls) y práctica con `strace` para observar llamadas del kernel.  
3. **Intermedio**: Compilar un kernel genérico, usar `make menuconfig`, y cargar/unload módulos con `modprobe`.  
4. **Avanzado**: Explorar eBPF con `bcc`/`bpftrace`, experimentar con cgroups v2 y probar live‑patching.  
5. **Especialización**: Desarrollo de drivers de dispositivo o contribución a subsistemas como networking o storage.

## Preguntas de repaso
1. ¿Qué papel juega el kernel al ejecutar una system call como `open`?  
2. ¿Cómo puedes inspeccionar los mensajes que el kernel genera durante el arranque?  
3. ¿Cuál es la diferencia entre compilar un kernel completo y cargar un módulo dinámico?  
4. ¿Qué riesgos implica cambiar un parámetro de `sysctl` sin validar su impacto?  
5. ¿De qué manera eBPF permite extender la funcionalidad del kernel sin recompilarlo?

<!-- trazabilidad: run_id=run-20261105-204002-56e07b concept=06-operating-systems-linux-02-kernel written_at=2026-11-05T23:41:02.991790+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/01 - Operating System|Operating System]]
- [[06 - Operating Systems & Linux/11 - System Calls|System Calls]]

---
← [[06 - Operating Systems & Linux/01 - Operating System|Operating System]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/03 - Processes|Processes]] →
