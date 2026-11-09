---
title: "Signals"
area: "Operating Systems / Linux"
numero: 19
aliases: ["Signals"]
tags: [concepto, it/operating-systems-linux]
---
# Signals

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 19 de 25**

## Qué abarca
- Comunicación/control de procesos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo señales para comunicar eventos asíncronos entre procesos o dentro del mismo proceso en Linux. Resuelvo la necesidad de interrumpir una tarea, solicitar su terminación o notificarle que debe ejecutar una rutina de limpieza sin que el proceso tenga que estar constantemente revisando una condición. Aparecen cada vez que administro demonios, scripts de arranque o depuro procesos colgados: envío `SIGTERM` para cerrar un servicio, capturo `SIGINT` en un script interactivo o manejo `SIGCHLD` para reaprovechar recursos de hijos. Después de entenderlas, puedo diseñar manejadores seguros, usar `kill` y `trap` para orquestar flujos y evitar fugas de recursos. Cuando el proceso no necesita reaccionar a interrupciones externas, no es necesario preocuparse por ellas.

## Esqueleto (el 20% esencial)
1. **Envió y recepción** – Un proceso genera una señal con `kill` o el kernel la envía por eventos internos; otro proceso la recibe según su ID o grupo.  
2. **Manejador (handler)** – Si el proceso registra una función con `signal` o `sigaction`, esa rutina se ejecuta al llegar la señal.  
3. **Acciones por defecto** – Cada señal tiene una conducta predefinida (terminar, ignorar, detener) que se aplica si no hay manejador.  
4. **Bloqueo y máscara** – Un proceso puede bloquear señales temporalmente con `sigprocmask` para evitar interrupciones críticas.  

## Como funciona
1. El kernel identifica la señal y el destinatario (PID, PGID o proceso actual).  
2. Busca si el proceso tiene un manejador instalado; si lo tiene, suspende la ejecución corriente y salta a esa rutina.  
3. Si no hay manejador, ejecuta la acción por defecto (p. ej., terminar).  
4. Tras el handler, el proceso retoma su flujo normal, salvo que la señal haya terminado el proceso.  
5. Opcionalmente, el proceso puede haber bloqueado la señal; en ese caso la señal queda pendiente hasta que se desbloquee.

## Detalles
- **Básico**: usar `kill -SIGTERM <pid>` y registrar un handler con `signal(SIGTERM, handler)`.  
- **Intermedio**: `sigaction` permite especificar máscara de señales bloqueadas durante el handler y reinicio de llamadas del sistema.  
- **Avanzado**: manipular la cola de señales con `sigqueue` para enviar datos, y usar `rt_sigaction` para señales en tiempo real con orden de entrega garantizado.  
- **Seguridad**: los handlers deben ser async‑signal‑safe; solo pueden llamar a funciones listadas por POSIX.  
- **Sincronización**: combinar señales con `sigsuspend` o `signalfd` para integrar en bucles de `select`/`poll`.

## Ejemplo minimo
```bash
#!/usr/bin/env bash
# Captura SIGINT (Ctrl‑C) y muestra un mensaje antes de salir
trap 'echo "Interrupción recibida, limpiando..."; exit 0' SIGINT

echo "Ejecutando, presiona Ctrl‑C para probar"
while :; do
    sleep 1
done
```
Al pulsar **Ctrl‑C**, el script muestra el mensaje y finaliza limpiamente en lugar de abortar abruptamente.

## Errores comunes
- Registrar un handler que llama a funciones no async‑signal‑safe → puede corromper el proceso; use solo `write`, `_exit`, etc.  
- Olvidar bloquear señales críticas durante el handler → re‑entrada inesperada; incluya la máscara adecuada en `sigaction`.  
- Confundir `kill -9` (SIGKILL) con señales manejables; SIGKILL no puede ser atrapada ni ignorada.  

## Estado actual
**Fundamentos estables**: el modelo de señales POSIX, `kill`, `signal`, `sigaction`, y las acciones por defecto son parte del kernel Linux desde hace décadas y no cambian.  
**Práctica moderna**: se prefiere `sigaction` sobre `signal` por su comportamiento consistente; `signalfd` y `timerfd` permiten integrar señales en bucles de E/S sin usar `trap`; las señales en tiempo real (`SIGRTMIN…`) se usan en aplicaciones de alta frecuencia donde el orden de entrega importa.

## Conexiones
- **Processes IPC** – Las señales son un mecanismo de IPC de bajo nivel que complementa pipes y sockets para notificaciones rápidas.  
- **Shell** – El intérprete de comandos traduce eventos del teclado (Ctrl‑C, Ctrl‑Z) en señales (`SIGINT`, `SIGTSTP`) que controla los procesos lanzados.  
- **Linux CLI** – Herramientas como `kill`, `pkill` y `killall` exponen la funcionalidad de envío de señales al usuario desde la línea de comandos.

## Ruta de estudio
1. **Prerequisitos**: comprensión de procesos, PID, y conceptos básicos de Unix/Linux.  
2. **Fundamentos**: leer la página man de `signal(7)` y practicar con `kill` y `trap`.  
3. **Intermedio**: implementar handlers en C usando `sigaction`, experimentar con máscaras y `sigsuspend`.  
4. **Avanzado**: explorar señales en tiempo real con `sigqueue`, usar `signalfd` en programas basados en `select`/`epoll`, y estudiar async‑signal‑safe API.  
5. **Especialización**: integrar señales en demonios systemd, depurar con `strace -e signal`, y revisar casos de uso en contenedores y entornos de alta disponibilidad.

## Preguntas de repaso
1. ¿Qué ocurre cuando un proceso recibe una señal para la que no ha registrado un handler?  
2. ¿Cuál es la diferencia práctica entre `signal` y `sigaction` al instalar un manejador?  
3. ¿Cómo se bloquea temporalmente una señal y por qué es útil hacerlo dentro de un handler?  
4. ¿Qué limitaciones tiene un handler respecto a las funciones que puede llamar?  
5. ¿En qué situaciones preferirías usar `signalfd` en lugar de `trap` o `sigaction`?

<!-- trazabilidad: run_id=run-20261106-225331-389846 concept=06-operating-systems-linux-19-signals written_at=2026-11-07T01:54:30.104359+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/13 - Processes IPC|Processes IPC]]
- [[06 - Operating Systems & Linux/14 - Sockets|Sockets]]
- [[06 - Operating Systems & Linux/16 - Shell|Shell]]
- [[06 - Operating Systems & Linux/17 - Linux CLI|Linux CLI]]
- [[06 - Operating Systems & Linux/18 - Bash - Shell Scripting|Bash / Shell Scripting]]

---
← [[06 - Operating Systems & Linux/18 - Bash - Shell Scripting|Bash / Shell Scripting]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/20 - Daemons - Services|Daemons / Services]] →
