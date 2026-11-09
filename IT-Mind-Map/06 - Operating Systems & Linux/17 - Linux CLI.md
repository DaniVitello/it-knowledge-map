---
title: "Linux CLI"
area: "Operating Systems / Linux"
numero: 17
aliases: ["Linux CLI"]
tags: [concepto, it/operating-systems-linux]
---
# Linux CLI

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 17 de 25**

## Qué abarca
- Comandos
- pipes
- redirecciones

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la Linux CLI para interactuar directamente con el kernel y los subsistemas del sistema operativo, ejecutando comandos que inspeccionan procesos, gestionan archivos y configuran servicios. Resuelvo problemas de diagnóstico como procesos colgados, uso excesivo de disco o fallos de permisos sin necesidad de interfaces gráficas. En mi día a día como ingeniero de sistemas Linux senior la CLI aparece al revisar logs, ajustar parámetros del kernel o automatizar tareas repetitivas. Después de dominarla puedo escribir scripts, encadenar herramientas con pipes y redirigir flujos de datos para crear soluciones rápidas. Sólo cuando todo está automatizado y monitorizado a nivel de API dejo de preocuparme por la línea de comandos.

## Esqueleto (el 20% esencial)
1. **Comandos** – unidades básicas que solicitan al kernel o a utilidades del usuario una acción concreta (p.ej., `ps`, `ls`).  
2. **Pipes (`|`)** – conectan la salida estándar de un comando con la entrada estándar de otro, permitiendo procesamiento en cadena.  
3. **Redirecciones (`>`, `>>`, `<`)** – envían la salida o la entrada a archivos o dispositivos, controlando dónde se almacena o lee la información.  
4. **Shell** – intérprete que interpreta los comandos y gestiona la ejecución, proporcionando variables y expansión.  
5. **Señales** – mecanismos de interrupción que permiten controlar procesos desde la CLI (p.ej., `SIGTERM` con `kill`).

## Como funciona
1. El usuario escribe un comando en el *shell*; el intérprete lo tokeniza y busca el ejecutable en `$PATH`.  
2. El kernel crea un proceso hijo que ejecuta el binario, heredando los descriptores de archivo estándar (stdin, stdout, stderr).  
3. Si se incluye un pipe, el *shell* crea un par de descriptores conectados; la salida del primer proceso se redirige al descriptor de lectura del segundo.  
4. Con redirecciones, el *shell* abre o crea archivos y reasigna los descriptores antes de lanzar el proceso.  
5. Durante la ejecución, el proceso puede recibir señales (p.ej., `SIGINT`) que el *shell* o el usuario envían para modificar su comportamiento o terminarlo.

## Detalles
- **Básico**: uso de comandos simples (`ls`, `cat`) y redirecciones (`> file`).  
- **Intermedio**: combinación de varios comandos con pipes (`ps aux | grep httpd`) y uso de redirecciones de error (`2>`).  
- **Avanzado**: manipulación de descriptores de archivo con `exec`, control de señales (`trap` en scripts) y uso de subshells para aislar entornos (`(cd /tmp && touch tmpfile)`).  
- **Optimización**: emplear `xargs` para evitar la sobrecarga de forks, y `stdbuf` para ajustar buffers en pipelines largas.

## Ejemplo minimo
```bash
# Lista los procesos que usan más CPU y guarda el resultado en un archivo
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 5 > top_cpu.txt
```
*Salida*: `top_cpu.txt` contiene las cinco líneas con mayor consumo de CPU.

## Errores comunes
- Olvidar cerrar comillas o paréntesis, lo que genera errores de sintaxis; revisar con `set -x` antes de ejecutar.  
- Usar `>` en lugar de `>>` y sobrescribir datos importantes; siempre confirmar el modo de redirección.  
- Conectar pipes sin considerar que algunos comandos no leen de stdin (p.ej., `grep -q`); usar `cat` o `tee` cuando sea necesario.  
- Enviar señales al PID equivocado; verificar con `ps -p PID` antes de usar `kill`.

## Estado actual
- **Fundamentos estables**: los comandos POSIX, la semántica de pipes y redirecciones, y el modelo de señales son parte del estándar Unix y se mantienen sin cambios.  
- **Práctica moderna**: el uso intensivo de herramientas como `jq` para procesar JSON, `fd` como sustituto rápido de `find`, y la integración de shells como `zsh` o `fish` para mejoras de usabilidad, aunque la lógica subyacente sigue siendo la misma.

## Conexiones
- **Shell** – el intérprete que ejecuta la CLI; sin él los comandos no podrían ser interpretados ni encadenados.  
- **Bash / Shell Scripting** – extiende la CLI con estructuras de control y funciones, permitiendo automatizar secuencias de comandos.  
- **Signals** – permiten a la CLI interrumpir o controlar procesos en ejecución, esencial para la gestión de servicios y depuración.

## Ruta de estudio
1. **Prerequisitos**: conocimientos básicos de Linux (filesystem, permisos, procesos).  
2. **Fundamentos**: dominar los comandos esenciales, pipes y redirecciones; practicar con ejercicios de filtrado y búsqueda.  
3. **Scripting**: aprender Bash, variables, bucles y funciones; crear scripts que combinen múltiples comandos.  
4. **Gestión de procesos**: estudiar señales, `kill`, `nohup` y `systemd` para controlar servicios desde la CLI.  
5. **Optimización**: explorar `xargs`, `parallel`, y herramientas de procesamiento de datos como `awk` y `jq`.  
6. **Especialización**: integrar la CLI con herramientas de monitoreo (e.g., `htop`, `iostat`) y automatización (Ansible, Terraform).

## Preguntas de repaso
1. ¿Qué ocurre a nivel del kernel cuando ejecutas un comando con redirección `>`?  
2. ¿Cómo conectarías dos comandos para que la salida del primero sea la entrada del segundo?  
3. ¿Cuál es la diferencia entre `>` y `>>` y cuándo usarías cada una?  
4. ¿Qué señal envías con `kill -9 PID` y qué efecto tiene en el proceso?  
5. ¿De qué manera un script Bash puede capturar y manejar una señal como `SIGINT`?

<!-- trazabilidad: run_id=run-20261106-225158-2c2396 concept=06-operating-systems-linux-17-linux-cli written_at=2026-11-07T01:52:54.098971+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/16 - Shell|Shell]]
- [[06 - Operating Systems & Linux/18 - Bash - Shell Scripting|Bash / Shell Scripting]]
- [[06 - Operating Systems & Linux/19 - Signals|Signals]]

---
← [[06 - Operating Systems & Linux/16 - Shell|Shell]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/18 - Bash - Shell Scripting|Bash / Shell Scripting]] →
