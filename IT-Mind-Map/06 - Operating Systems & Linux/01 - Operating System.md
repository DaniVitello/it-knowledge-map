---
title: "Operating System"
area: "Operating Systems / Linux"
numero: 1
aliases: ["Operating System"]
tags: [concepto, it/operating-systems-linux]
---
# Operating System

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 1 de 25**

## Qué abarca
- Qué hace un SO y cómo administra el hardware

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el sistema operativo como la capa que traduce las peticiones de los procesos en acciones concretas sobre el hardware, gestionando CPU, memoria, dispositivos y almacenamiento. Resuelvo la necesidad de aislar y coordinar recursos para que aplicaciones y servicios funcionen de forma estable y segura. En mi día a día como ingeniero Linux senior, el SO aparece cada vez que configuro el arranque, depuro un bloqueo de proceso o ajusto el rendimiento del disco. Después de comprender su papel, puedo diseñar políticas de scheduling, afinar el uso de swap o implementar mecanismos de aislamiento como cgroups. Cuando trabajo exclusivamente con contenedores o con un hypervisor que ya abstrae el hardware, no necesito preocuparme de los detalles internos del kernel.

## Esqueleto (el 20% esencial)
1. **Gestión de recursos** – el SO asigna CPU, memoria y dispositivos a los procesos según políticas de scheduling y asignación.  
2. **Abstracción de hardware** – expone interfaces estándar (syscalls, /dev) que ocultan la complejidad del hardware físico.  
3. **Aislamiento y protección** – usa modos de usuario/ker­nel y mecanismos de permisos para evitar interferencias entre procesos.  
4. **Servicios básicos** – provee subsistemas como el sistema de archivos, red y gestión de procesos que otras capas consumen.  

## Como funciona
1. Un proceso solicita un recurso mediante una syscall (p. ej. `read()` para leer un archivo).  
2. El kernel verifica permisos y disponibilidad; si el recurso está libre, lo asigna y actualiza sus tablas internas (task_struct, page tables).  
3. El scheduler decide qué proceso ejecuta la CPU en el siguiente tick, aplicando la política configurada (CFS, realtime).  
4. Cuando el proceso termina o libera el recurso, el kernel actualiza los contadores y notifica a los subsistemas dependientes (VFS, network stack).  

## Detalles
- **Básico**: comprensión de las syscalls principales (`fork`, `exec`, `open`, `close`) y del modelo de procesos (PID, PPID).  
- **Intermedio**: estudio del scheduler (runqueues, prioridades), gestión de memoria (paging, swap) y del VFS (inode, dentry).  
- **Avanzado**: análisis del kernel preemptible, cgroups, namespaces y de los mecanismos de seguridad (SELinux, AppArmor) que extienden el aislamiento.  

## Ejemplo minimo
```bash
# Mostrar información básica del kernel y arquitectura
uname -a
```
Salida típica:
```
Linux host01 5.15.0-78-generic #84-Ubuntu SMP Fri Sep 15 12:34:56 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```
El comando llama a la syscall `uname` que el kernel rellena con datos del subsistema de información del sistema, demostrando la capa de abstracción entre usuario y hardware.

## Errores comunes
- **Confundir permisos de archivo con aislamiento de proceso** – usar solo chmod no protege contra interferencias; combine con namespaces o cgroups.  
- **Asumir que más CPU = mejor rendimiento** – sin ajustar la política de scheduling, procesos pueden competir y generar thrashing.  
- **Ignorar la caché del kernel** – borrar indiscriminadamente `/proc/sys/vm/drop_caches` puede degradar el rendimiento; úselo solo para pruebas controladas.  

## Estado actual
- **Fundamentos estables**: el modelo de procesos, syscalls y el scheduler CFS son parte del kernel Linux desde hace varias versiones y cambian poco.  
- **Práctica moderna**: el uso de cgroups v2 y namespaces para contenedores, así como la integración de eBPF para observabilidad en tiempo real, representa la evolución reciente del manejo de recursos y aislamiento.  

## Conexiones
- **Docker** (virtualización de aplicaciones) – depende del aislamiento de procesos y de los namespaces que el SO provee.  
- **Systemd** (gestor de servicios) – orquesta unidades basándose en el modelo de procesos y en los sockets del kernel.  
- **SELinux** (seguridad) – extiende la protección de acceso del SO mediante políticas de control de acceso obligatorio.  

## Ruta de estudio
1. **Prerequisitos**: línea de comandos Linux, conceptos de procesos y permisos de archivo.  
2. **Fundamentos**: leer la sección *Process Management* del manual `man 7 syscalls` y experimentar con `strace`.  
3. **Intermedio**: estudiar el scheduler con `cat /proc/sched_debug` y probar ajustes en `/proc/sys/kernel/sched_*`.  
4. **Avanzado**: crear cgroups con `systemd-run --scope -p MemoryMax=200M bash` y explorar eBPF mediante `bpftool`.  
5. **Especialización**: profundizar en SELinux (`man selinux`) y en la integración de Systemd con unidades de tipo `socket`.  

## Preguntas de repaso
1. ¿Qué mecanismo del SO traduce una llamada `open()` en una operación sobre un dispositivo físico?  
2. ¿Cómo influye el scheduler en la latencia de un proceso de tiempo real?  
3. ¿Por qué los permisos de archivo no son suficientes para aislar procesos en un contenedor?  
4. ¿Qué ventaja ofrece cgroups v2 frente a la gestión tradicional de memoria?  
5. ¿De qué manera Systemd utiliza los sockets del kernel para iniciar servicios bajo demanda?

<!-- trazabilidad: run_id=run-20261105-140304-1cdf5c concept=06-operating-systems-linux-01-operating-system written_at=2026-11-05T17:04:01.054458+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/02 - Kernel|Kernel]]
- [[06 - Operating Systems & Linux/11 - System Calls|System Calls]]

---
[[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/02 - Kernel|Kernel]] →
