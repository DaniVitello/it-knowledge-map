---
title: "Bash / Shell Scripting"
area: "Operating Systems / Linux"
numero: 18
aliases: ["Bash / Shell Scripting"]
tags: [concepto, it/operating-systems-linux]
---
# Bash / Shell Scripting

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 18 de 25**

## Qué abarca
- Automatización mediante scripts

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Bash/Shell scripting para automatizar tareas repetitivas del sistema, como la recolección de métricas, la rotación de logs o la orquestación de procesos al iniciar o detener servicios. Resuelvo la necesidad de ejecutar secuencias de comandos de forma fiable y reproducible, evitando errores humanos y reduciendo el tiempo de intervención manual. En mi día a día como ingeniero de sistemas Linux senior, lo empleo para crear scripts de diagnóstico que capturan información del kernel, ajustan parámetros de `sysctl` o gestionan señales a procesos críticos. Después de dominarlo, puedo diseñar pipelines de mantenimiento que se integren con `cron` o `systemd` y delegar la ejecución a usuarios sin privilegios. Cuando la tarea es puntual y sencilla, prefiero usar comandos ad‑hoc en la línea de comandos y no desarrollo un script completo.

## Esqueleto (el 20% esencial)
1. **Secuencias de comandos**: Un archivo de texto ejecutable que contiene órdenes del shell, permite reproducir una serie de pasos con un solo comando.  
2. **Variables y control de flujo**: Uso de variables, condicionales (`if`, `case`) y bucles (`for`, `while`) para adaptar la lógica a la información del sistema.  
3. **Redirección y tuberías**: Captura de salida (`>`, `>>`) y encadenamiento de comandos (`|`) para procesar datos sin crear archivos temporales.  
4. **Manejo de señales**: Trampa (`trap`) de señales del kernel (SIGINT, SIGTERM) para limpiar recursos antes de que el script termine.  
5. **Integración con el entorno Linux**: Llamadas a utilidades del CLI (e.g., `ps`, `df`, `systemctl`) y uso de rutas y permisos del filesystem.

## Como funciona
1. El intérprete `bash` lee el script línea a línea.  
2. Cada orden se ejecuta en el mismo proceso del shell o en subshells según la sintaxis (`$(…)` o `` `…` ``).  
3. Las variables se expanden antes de la ejecución, permitiendo que datos del sistema (p. ej. salida de `uname -r`) influyan en la lógica.  
4. Los bloques de control evalúan condiciones y repiten acciones, adaptándose a estados cambiantes (por ejemplo, mientras exista espacio libre en `/var`).  
5. Cuando el script recibe una señal, la rutina definida con `trap` se ejecuta, garantizando acciones de cierre como desmontar un filesystem temporal.  
6. Al finalizar, el código de salida (`exit`) comunica al llamador si la operación fue exitosa o falló.

## Detalles
- **Básico**: crear scripts con `#!/bin/bash`, usar `chmod +x` y ejecutar directamente.  
- **Intermedio**: emplear funciones para modularizar, manejar errores con `set -e` y `|| exit`.  
- **Avanzado**: usar arrays, `getopts` para parsear opciones, y `exec` para redirigir descriptor de archivo a procesos de larga duración.  
- **Optimización**: evitar forks innecesarios, usar `read -r` para procesar líneas sin interpretar backslashes y emplear `printf` en lugar de `echo` para salida controlada.  
- **Seguridad**: validar entradas, limitar `PATH` dentro del script y usar `sudo -n` cuando se requieran privilegios sin interacción.

## Ejemplo minimo
```bash
#!/bin/bash
# Muestra la carga media del sistema y termina con código 0

load=$(cat /proc/loadavg | awk '{print $1}')
echo "Carga media (1 min): $load"
exit 0
```
**Salida esperada** (en una máquina típica):
```
Carga media (1 min): 0.42
```

## Errores comunes
- Olvidar `chmod +x` y recibir “Permission denied”. → Asignar permiso de ejecución.  
- Usar `#!/bin/sh` cuando el script depende de extensiones de Bash. → Cambiar al shebang correcto.  
- No citar variables (`"$var"`), provocando expansión de globbing. → Siempre encerrar en comillas.  
- Ignorar códigos de salida y continuar con datos inválidos. → Verificar `$?` o usar `set -e`.  
- No manejar señales y dejar recursos abiertos. → Definir `trap` para SIGINT/SIGTERM.

## Estado actual
**Fundamentos estables**: la sintaxis de Bash, el modelo de procesos POSIX y la semántica de redirección son parte del estándar GNU Bash y no han cambiado significativamente en versiones recientes.  
**Práctica moderna**: la tendencia es combinar scripts Bash con herramientas como `systemd` para gestión de servicios, y con `jq` o `yq` para procesar JSON/YAML en pipelines de automatización. Además, se promueve el uso de `shellcheck` para detectar errores estáticos antes de la ejecución.

## Conexiones
- **Shell**: Bash es una implementación de shell que interpreta los comandos del Linux CLI, proporcionando el entorno donde se ejecutan los scripts.  
- **Linux CLI**: Los scripts aprovechan utilidades del CLI (p. ej. `grep`, `awk`) para inspeccionar y modificar el estado del sistema.  
- **Signals**: La capacidad de capturar y responder a señales del kernel permite que los scripts gestionen interrupciones y finalizaciones limpias, esencial para la robustez de procesos de fondo.

## Ruta de estudio
1. **Prerequisitos**: manejo básico de la línea de comandos, permisos de archivo y conceptos de procesos en Linux.  
2. **Fundamentos**: crear scripts simples, variables, control de flujo y redirección.  
3. **Intermedio**: funciones, manejo de errores, `trap` y uso de herramientas de texto (`sed`, `awk`).  
4. **Avanzado**: arrays, `getopts`, integración con `systemd` y pruebas automatizadas con `bats`.  
5. **Especialización**: optimización de rendimiento, seguridad de scripts y uso de linters como `shellcheck`.

## Preguntas de repaso
1. ¿Cómo afecta el shebang (`#!/bin/bash`) al momento de ejecutar un script?  
2. ¿Qué diferencia hay entre redirigir con `>` y con `>>` dentro de un script?  
3. ¿Cuál es la utilidad de `trap` y cómo se usa para manejar SIGTERM?  
4. ¿Por qué es importante citar variables (`"$var"`) al usarlas en comandos?  
5. ¿De qué manera puede un script Bash integrarse con `systemd` para ejecutar tareas programadas?

<!-- trazabilidad: run_id=run-20261106-225255-cea069 concept=06-operating-systems-linux-18-bash-shell-scripting written_at=2026-11-07T01:53:30.226825+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/16 - Shell|Shell]]
- [[06 - Operating Systems & Linux/17 - Linux CLI|Linux CLI]]
- [[06 - Operating Systems & Linux/19 - Signals|Signals]]

---
← [[06 - Operating Systems & Linux/17 - Linux CLI|Linux CLI]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/19 - Signals|Signals]] →
