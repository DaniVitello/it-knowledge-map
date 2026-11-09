---
title: "Shell"
area: "Operating Systems / Linux"
numero: 16
aliases: ["Shell"]
tags: [concepto, it/operating-systems-linux]
---
# Shell

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 16 de 25**

## Qué abarca
- Interfaz para interactuar con el sistema

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el shell como la puerta de enlace directa al kernel de Linux: me permite lanzar procesos, inspeccionar el estado del sistema y encadenar herramientas para diagnosticar y automatizar tareas. Resuelvo la necesidad de interactuar con el sistema sin escribir código C, accediendo a archivos de `/proc`, gestionando servicios o inspeccionando variables de entorno. Aparece en mi día a día al depurar un servicio que no arranca, al inspeccionar el consumo de CPU con `top` o al crear scripts que despliegan paquetes. Después de dominar el shell puedo escribir scripts de mantenimiento, integrar comandos en pipelines y personalizar mi entorno de trabajo; cuando solo ejecuto una única orden puntual, no necesito profundizar más.

## Esqueleto (el 20% esencial)
1. **Interfaz de línea de comandos (CLI)**: punto de entrada textual para enviar órdenes al kernel.  
2. **Interpretación y ejecución de comandos**: el shell parsea la línea, busca el ejecutable y crea un proceso.  
3. **Gestión del entorno**: variables de entorno y expansión de comodines influyen en la ejecución.  
4. **Control de flujo y scripting**: estructuras (`if`, `for`, `while`) permiten automatizar secuencias de comandos.  
5. **Manejo de señales**: el shell recibe y propaga señales (SIGINT, SIGTERM) a los procesos hijos.

## Como funciona
1. El usuario escribe una línea en la CLI del shell.  
2. El shell tokeniza la línea, expandiendo variables y comodines.  
3. Busca cada comando en los directorios listados en `$PATH`.  
4. Lanza un proceso mediante `fork()` y `execve()`.  
5. Si el comando se ejecuta en segundo plano (`&`), el shell no espera; de lo contrario, espera su terminación y captura su código de salida.  
6. Las señales enviadas al shell (p. ej. `Ctrl‑C`) se propagan a los procesos hijos según la política del shell.  
7. En scripts, el flujo de control dirige la ejecución de múltiples órdenes de forma condicional o iterativa.

## Detalles
- **Básico**: uso de comandos simples, redirección (`>`, `>>`, `<`) y pipelines (`|`).  
- **Intermedio**: definición y exportación de variables, sustitución de comandos ``$(cmd)`` y manejo de trabajos (`jobs`, `bg`, `fg`).  
- **Avanzado**: funciones de shell, trap de señales, expansión de arrays, y uso de `eval` para generar código dinámico. Cada nivel aprovecha las ideas del esqueleto: la CLI sigue siendo la base, mientras que la gestión del entorno y el control de flujo permiten construir herramientas de diagnóstico complejas.

## Ejemplo minimo
```bash
# Lista los procesos que usan más CPU y guarda el resultado en un archivo
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 5 > top5.txt
```
*Salida esperada*: `top5.txt` contiene las cinco líneas con mayor consumo de CPU, útil para identificar rápidamente procesos problemáticos.

## Errores comunes
- Olvidar exportar una variable (`export VAR=value`) y esperar que esté disponible en procesos hijos.  
- Usar `=` sin espacios al asignar en scripts, provocando errores de sintaxis.  
- Ejecutar un comando en primer plano y luego presionar `Ctrl‑C`, terminando también procesos que deberían seguir corriendo; usar `nohup` o `&` cuando sea necesario.

## Estado actual
Los shells tradicionales (Bash, Zsh, Fish) siguen siendo la base estable para la interacción diaria con Linux. En la práctica moderna, Bash es el intérprete por defecto en la mayoría de distribuciones, mientras que Zsh gana popularidad por sus mejoras de completado y plugins. Las extensiones de scripting (por ejemplo, `bash` 4+ con arrays asociativos) amplían la capacidad de automatización sin romper la compatibilidad con scripts heredados.

## Conexiones
- **Environment Variables**: el shell es el punto donde se crean, exportan y consumen variables que afectan a todos los procesos del sistema.  
- **Linux CLI**: el shell constituye la capa de interpretación que convierte la línea de comandos en acciones del kernel.  
- **Package Management**: los gestores de paquetes (`apt`, `dnf`, `pacman`) se invocan habitualmente desde el shell, y sus scripts de post‑instalación se ejecutan en este entorno.

## Ruta de estudio
1. **Prerequisitos**: comprensión de procesos Unix (`fork`, `exec`), sistema de archivos y permisos.  
2. **Fundamentos**: práctica intensiva con comandos básicos, redirección y pipelines.  
3. **Scripting**: crear scripts que usen variables, condicionales y bucles; estudiar `set -e` y `trap`.  
4. **Avanzado**: profundizar en manejo de señales, funciones de shell y personalización del prompt.  
5. **Especialización**: explorar shells alternativos (Zsh, Fish) y su ecosistema de plugins para mejorar la productividad.

## Preguntas de repaso
1. ¿Qué pasos sigue el shell para ejecutar una orden escrita en la línea de comandos?  
2. ¿Cómo afecta la variable `$PATH` a la búsqueda de un ejecutable?  
3. ¿Cuál es la diferencia entre redirigir la salida con `>` y con `>>`?  
4. ¿Cómo puedes hacer que una variable esté disponible para los procesos hijos?  
5. ¿Qué comando usarías para enviar una señal `SIGTERM` a todos los procesos iniciados por un script?

<!-- trazabilidad: run_id=run-20261106-225057-fc3b6d concept=06-operating-systems-linux-16-shell written_at=2026-11-07T01:51:56.545048+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/15 - Environment Variables|Environment Variables]]
- [[06 - Operating Systems & Linux/17 - Linux CLI|Linux CLI]]
- [[06 - Operating Systems & Linux/18 - Bash - Shell Scripting|Bash / Shell Scripting]]
- [[06 - Operating Systems & Linux/19 - Signals|Signals]]
- [[06 - Operating Systems & Linux/21 - Package Management|Package Management]]

---
← [[06 - Operating Systems & Linux/15 - Environment Variables|Environment Variables]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/17 - Linux CLI|Linux CLI]] →
