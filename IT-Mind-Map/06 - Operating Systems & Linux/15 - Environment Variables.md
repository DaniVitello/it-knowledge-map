---
title: "Environment Variables"
area: "Operating Systems / Linux"
numero: 15
aliases: ["Environment Variables"]
tags: [concepto, it/operating-systems-linux]
---
# Environment Variables

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 15 de 25**

## Qué abarca
- Configuración del entorno de ejecución

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo variables de entorno para parametrizar el comportamiento de procesos y herramientas sin tocar su código fuente. Resuelvo la necesidad de adaptar rutas, opciones de depuración o credenciales a distintas máquinas o usuarios, lo que simplifica la administración y el diagnóstico de un sistema Linux. Aparecen cada vez que configuro el shell de un usuario, preparo scripts de inicio o depuro servicios con `systemd`. Después de comprenderlas, puedo crear entornos reproducibles, aislar configuraciones por proyecto y evitar errores de “hard‑coding”. No necesito preocuparme por ellas cuando ejecuto comandos aislados que no dependen de configuración externa.

## Esqueleto (el 20% esencial)
1. **Alcance del proceso** – Cada proceso hereda del padre el conjunto de variables que describen su entorno de ejecución.  
2. **Persistencia en el shell** – El shell almacena variables en su tabla interna y las exporta para que los procesos hijos las vean.  
3. **Uso en configuración** – Herramientas como `make`, `gcc` o gestores de paquetes leen variables para decidir rutas, flags y credenciales.  
4. **Sobrescritura temporal** – Se pueden redefinir en una sola línea de comando o dentro de un script sin afectar el entorno global.  

## Como funciona
1. El usuario define o modifica una variable en el shell (`export VAR=valor`).  
2. El shell actualiza su tabla interna y marca la variable como exportable.  
3. Al lanzar un nuevo proceso, el kernel copia la tabla de variables exportadas al bloque de memoria del proceso hijo.  
4. El proceso lee la variable mediante la llamada de sistema `getenv()` o mediante la expansión del shell (`$VAR`).  
5. Si el proceso modifica la variable, el cambio queda limitado a su propio espacio; el padre y los demás procesos no se ven afectados.  

## Detalles
- **Básico**: Creación (`VAR=valor`), exportación (`export VAR`) y visualización (`printenv`, `env`).  
- **Intermedio**: Uso de variables especiales (`PATH`, `LD_LIBRARY_PATH`, `HOME`) y su influencia en la búsqueda de ejecutables y bibliotecas.  
- **Avanzado**: Manipulación en scripts de inicio (`/etc/profile`, `~/.bashrc`), uso de `env -i` para iniciar procesos con un entorno vacío, y combinación con `systemd` mediante `Environment=` y `EnvironmentFile=`.  

## Ejemplo minimo
```bash
# Definir y exportar una variable
export APP_MODE=debug

# Ejecutar un comando que la usa
python3 -c 'import os; print("Modo:", os.getenv("APP_MODE"))'
```
Salida:
```
Modo: debug
```

## Errores comunes
- Olvidar `export` y pensar que la variable está disponible para procesos hijos. *Evitarlo exportando explícitamente.*  
- Sobrescribir `PATH` sin incluir el valor anterior, rompiendo la búsqueda de comandos. *Usar `PATH=$PATH:/nuevo/directorio`.*  
- Usar comillas simples alrededor de `$VAR`, impidiendo la expansión. *Preferir comillas dobles o sin comillas.*  

## Estado actual
**Fundamentos estables**: La herencia de variables mediante `export`, la tabla de entorno del proceso y las llamadas `getenv()`/`setenv()` son parte del POSIX desde hace décadas.  
**Práctica moderna**: Herramientas como `direnv` y `dotenv` gestionan variables por proyecto; `systemd` permite declarar entornos en unidades; los contenedores (Docker, Podman) usan `ENV` en Dockerfiles para reproducir entornos aislados.  

## Conexiones
- **Shell**: Es el intérprete que crea, exporta y expande variables de entorno, sirviendo de puente entre el usuario y los procesos.  
- **Package Management**: Gestores como `apt` o `dnf` leen variables como `DEBIAN_FRONTEND` para decidir si operar en modo interactivo o silencioso.  
- **Systemd**: Permite definir variables de entorno en unidades mediante `Environment=` y cargar archivos con `EnvironmentFile=`, integrando la configuración del entorno con el control de servicios.  

## Ruta de estudio
1. **Prerequisitos**: Conocer el funcionamiento básico del shell (bash, zsh) y la estructura de procesos en Linux.  
2. **Fundamentos**: Practicar creación, exportación y lectura de variables; explorar `printenv`, `env` y `set`.  
3. **Intermedio**: Modificar archivos de inicio (`/etc/profile`, `~/.bashrc`), usar `env -i` y entender variables especiales (`PATH`, `LD_LIBRARY_PATH`).  
4. **Avanzado**: Integrar variables en unidades `systemd`, usar `direnv` para entornos por proyecto y aplicar `dotenv` en contenedores.  

## Preguntas de repaso
1. ¿Qué diferencia hay entre definir una variable y exportarla en el shell?  
2. ¿Cómo afecta la variable `PATH` al comportamiento del comando `which`?  
3. ¿Qué ocurre con una variable de entorno cuando un proceso hijo la modifica?  
4. ¿Cuál es la forma correcta de iniciar un proceso con un entorno completamente vacío?  
5. ¿Cómo puedes declarar una variable de entorno para un servicio gestionado por `systemd`?

<!-- trazabilidad: run_id=run-20261106-224944-8bee5c concept=06-operating-systems-linux-15-environment-variables written_at=2026-11-07T01:50:55.814060+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/16 - Shell|Shell]]
- [[06 - Operating Systems & Linux/21 - Package Management|Package Management]]

---
← [[06 - Operating Systems & Linux/14 - Sockets|Sockets]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/16 - Shell|Shell]] →
