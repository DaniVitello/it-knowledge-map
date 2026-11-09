---
title: "Daemons / Services"
area: "Operating Systems / Linux"
numero: 20
aliases: ["Daemons / Services"]
tags: [concepto, it/operating-systems-linux]
---
# Daemons / Services

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 20 de 25**

## Qué abarca
- Procesos que funcionan como servicios

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los daemons (también llamados services) para que tareas del sistema se ejecuten de forma continua y sin intervención directa del usuario, como la gestión de redes, el registro de eventos o la sincronización de relojes. Resuelvo la necesidad de mantener procesos críticos siempre disponibles, incluso después de reinicios, y de aislar esas funciones del entorno de sesión del usuario. En mi día a día como ingeniero de sistemas Linux senior, configuro, monitorizo y depuro daemons para garantizar la estabilidad del servidor; por ejemplo, reviso `sshd` para accesos remotos o `cron` para trabajos programados. Después de comprender cómo se crean, controlan y supervisan, puedo diseñar servicios propios, automatizar despliegues y aplicar políticas de seguridad a nivel de proceso. Cuando la funcionalidad requerida es puntual y no necesita estar siempre activa, no es necesario involucrar un daemon.

## Esqueleto (el 20% esencial)
1. **Un daemon es un proceso de fondo que se inicia en el arranque y permanece activo**; no está ligado a una terminal de usuario.  
2. **Se gestiona mediante un sistema de init (systemd, SysVinit, etc.) que controla su ciclo de vida** (start, stop, restart, enable).  
3. **Provee un servicio accesible a otros procesos o a usuarios remotos** mediante sockets, archivos o APIs.  
4. **Se ejecuta con privilegios mínimos y con un entorno controlado** (umask, cwd, variables).  
5. **Los logs del daemon se canalizan a `journalctl` o a archivos específicos** para diagnóstico.

## Como funciona
1. Durante el arranque, el gestor de init lee la configuración del daemon (unit file o script).  
2. El gestor crea un proceso hijo, le asigna un *PID* y lo desacopla de la sesión (fork + setsid).  
3. Se ajusta el entorno: se cambia a `/`, se redefine `umask`, se cierran descriptors de terminal.  
4. El daemon abre los recursos que necesita (sockets, archivos) y entra en su bucle principal, esperando peticiones o ejecutando tareas programadas.  
5. El gestor de init monitoriza el proceso; si muere, puede reiniciarlo según la política definida.

## Detalles
- **Básico**: entender la diferencia entre proceso interactivo y daemon; conocer los directorios `/etc/init.d/` y `/etc/systemd/system/`.  
- **Intermedio**: crear un unit file de systemd, usar `Type=forking` o `Type=simple` según el modelo de daemon, y aplicar `Restart=on-failure`.  
- **Avanzado**: aislar el daemon con *cgroups* y *systemd sandboxing* (`ProtectSystem`, `PrivateTmp`), definir límites de recursos (`CPUQuota`, `MemoryLimit`) y usar *socket activation* para iniciar bajo demanda.

## Ejemplo minimo
```bash
# /etc/systemd/system/hellod.service
[Unit]
Description=Ejemplo de daemon que escribe en el log cada 5 segundos
After=network.target

[Service]
ExecStart=/usr/bin/bash -c 'while true; do logger "Hola desde hellod"; sleep 5; done'
Restart=always
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
```

```bash
# Recargar systemd y activar el daemon
sudo systemctl daemon-reload
sudo systemctl enable --now hellod.service

# Ver la salida en el journal
journalctl -u hellod.service -f
```

## Errores comunes
- **Olvidar habilitar el daemon** (`systemctl enable`) y solo iniciarlo, lo que provoca que no arranque tras reiniciar.  
- **Ejecutar el daemon como root sin necesidad**, aumentando la superficie de ataque; usar usuarios con privilegios limitados.  
- **No redirigir la salida estándar**, lo que genera procesos colgados esperando escritura en un terminal inexistente.  
- **Confundir `Type=forking` con `Type=simple`**, provocando que systemd no detecte el proceso hijo y lo marque como fallido.  

## Estado actual
- **Fundamentos estables**: la arquitectura de daemon (fork, setsid, cierre de fds) y la gestión mediante init siguen siendo la base de todas las distribuciones modernas.  
- **Práctica moderna**: systemd es el gestor de servicios dominante; introduce características como *socket activation*, *cgroup slicing* y políticas de sandboxing que reemplazan gran parte de los scripts SysV tradicionales.

## Conexiones
- **Filesystem**: los daemons suelen trabajar con directorios de datos persistentes (`/var/lib`, `/var/log`) y dependen de permisos de montaje para operar correctamente.  
- **Processes**: un daemon es un proceso con un ciclo de vida gestionado por el init, y su PID se usa para monitorizar y controlar su ejecución.  
- **Servidor**: muchos servidores (web, base de datos) se implementan como daemons, exponiendo servicios a través de sockets de red.

## Ruta de estudio
1. **Prerequisitos**: manejo de la línea de comandos, conceptos de procesos (PID, fork, exec) y permisos de Linux.  
2. **Fundamentos**: estudiar el modelo de init tradicional (SysV) y crear scripts en `/etc/init.d/`.  
3. **Systemd**: leer la documentación oficial de `systemd.service`, practicar con unit files, y experimentar con `systemctl` y `journalctl`.  
4. **Seguridad y aislamiento**: profundizar en opciones de sandboxing (`ProtectSystem`, `PrivateTmp`) y en el uso de *cgroups* para limitar recursos.  
5. **Desarrollo propio**: escribir un daemon en C o Bash que use *socket activation* y probar su despliegue en un entorno de pruebas.

## Preguntas de repaso
1. ¿Qué diferencia hay entre un proceso interactivo y un daemon en cuanto a su entorno de ejecución?  
2. ¿Cómo se indica a systemd que un daemon debe iniciarse automáticamente al arrancar el sistema?  
3. ¿Qué ventaja ofrece la opción `Type=notify` frente a `Type=simple` en un unit file?  
4. ¿Por qué es importante ejecutar un daemon con un usuario de privilegios limitados?  
5. ¿Cómo puedes verificar que un daemon está escribiendo sus logs en el journal de systemd?

<!-- trazabilidad: run_id=run-20261106-225431-713cc3 concept=06-operating-systems-linux-20-daemons-services written_at=2026-11-07T01:55:26.520840+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/03 - Servidor|Servidor]] · *Backend*
- [[06 - Operating Systems & Linux/03 - Processes|Processes]]

---
← [[06 - Operating Systems & Linux/19 - Signals|Signals]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/21 - Package Management|Package Management]] →
