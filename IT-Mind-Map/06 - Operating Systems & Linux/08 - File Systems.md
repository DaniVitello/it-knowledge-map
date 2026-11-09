---
title: "File Systems"
area: "Operating Systems / Linux"
numero: 8
aliases: ["File Systems"]
tags: [concepto, it/operating-systems-linux]
---
# File Systems

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 8 de 25**

## Qué abarca
- Archivos
- directorios
- bloques
- metadata

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los sistemas de archivos para organizar los datos que el kernel almacena en discos, SSD o memoria volátil, de modo que pueda leer, escribir y borrar información de forma estructurada. Resuelvo el problema de localizar rápidamente cualquier bloque de datos mediante nombres de archivo y directorios, evitando la gestión manual de sectores físicos. En mi día a día como ingeniero Linux senior, lo empleo al crear particiones, montar volúmenes, diagnosticar fragmentación o corrupción de metadatos y al aplicar políticas de retención. Después de comprender cómo se estructuran los bloques, los inodos y la metadata, puedo diseñar estrategias de backup, optimizar el rendimiento I/O y elegir el tipo de FS adecuado para cada carga de trabajo. Sólo cuando trabajo con dispositivos de bloque virtuales o sistemas temporales (por ejemplo, `tmpfs`) no necesito preocuparme por los detalles internos del FS.

## Esqueleto (el 20% esencial)
1. **Archivos y directorios** – Nodos que el usuario manipula mediante rutas legibles.  
2. **Bloques** – Unidades físicas de almacenamiento donde el FS guarda el contenido de los archivos.  
3. **Metadata (inodos)** – Información estructural (tamaño, timestamps, punteros a bloques, permisos).  
4. **Asignación y recuperación** – Algoritmos que asignan bloques libres y reconstruyen la estructura tras fallos.  

## Como funciona
1. El usuario invoca una operación (p. ej., `open("/home/user/file.txt")`).  
2. El VFS traduce la ruta en un inodo mediante la metadata del directorio.  
3. El inodo contiene punteros a los bloques que contienen los datos del archivo.  
4. El kernel solicita esos bloques al controlador del dispositivo y los lee/escribe.  
5. Tras la operación, el VFS actualiza timestamps y contadores en la metadata.  

## Detalles
- **Básico:** Cada archivo tiene un inodo único; los directorios son archivos especiales que listan pares nombre‑inodo.  
- **Intermedio:** Los sistemas modernos usan bloques de 4 KB y estructuras de árbol (extent) para reducir la fragmentación.  
- **Avanzado:** Funciones como journaling (ext4, XFS) registran cambios antes de aplicarlos, permitiendo recuperación rápida tras cortes de energía; sistemas copy‑on‑write (btrfs, ZFS) gestionan versiones y snapshots.  

## Ejemplo minimo
```bash
# Crear un directorio y un archivo
mkdir -p /tmp/mi_dir
touch /tmp/mi_dir/archivo.txt
# Ver metadata del archivo
ls -li /tmp/mi_dir/archivo.txt
```
Salida típica:
```
1234567 -rw-r--r-- 1 usuario usuarios 0 nov  7 12:34 /tmp/mi_dir/archivo.txt
```
El número `1234567` es el inodo, evidencia de la metadata que el FS mantiene.

## Errores comunes
- **Olvidar montar** el dispositivo antes de acceder a sus archivos → “No such file or directory”.  
- **Confundir permisos con ownership**; aplicar `chmod` sin revisar `chown` genera accesos inesperados.  
- **Ignorar el límite de bloques**; crear archivos muy grandes en un FS con bloques de 1 KB provoca fragmentación excesiva.  

## Estado actual
- **Fundamentos estables:** Inodos, bloques de 4 KB, jerarquía de directorios y journaling son conceptos presentes desde ext2/ext3.  
- **Práctica moderna:** Ext4 es el FS predeterminado en la mayoría de distribuciones; btrfs y XFS se usan para cargas que requieren snapshots o alta concurrencia; overlayfs permite combinar capas de FS en contenedores.  

## Conexiones
- **File Permissions** – La metadata del inodo incluye los bits de permiso que determinan quién puede leer o escribir un archivo.  
- **Users & Groups** – Los campos UID y GID del inodo enlazan el archivo con usuarios y grupos del sistema, controlando el acceso.  
- **Kernel VFS (Virtual File System)** – Actúa como capa de abstracción que permite al kernel manejar diferentes tipos de FS mediante una interfaz común.  

## Ruta de estudio
1. **Prerequisitos:** manejo de la línea de comandos, conceptos de bloques y dispositivos de bloque (`lsblk`, `fdisk`).  
2. **Fundamentos:** estudiar la estructura de inodos y directorios con `stat` y `debugfs`.  
3. **FS modernos:** comparar ext4, XFS y btrfs mediante pruebas de rendimiento (`fio`) y análisis de logs (`dmesg`).  
4. **Diagnóstico:** aprender a usar `fsck`, `tune2fs` y `btrfs check` para detectar y reparar metadata corrupta.  
5. **Avanzado:** implementar snapshots y subvolúmenes con btrfs, y explorar overlayfs en entornos de contenedores.  

## Preguntas de repaso
1. ¿Qué información contiene un inodo y por qué es esencial para localizar los bloques de un archivo?  
2. ¿Cómo afecta el tamaño de bloque a la fragmentación y al rendimiento de I/O?  
3. ¿Qué diferencia hay entre permisos (`chmod`) y ownership (`chown`) en la metadata de un archivo?  
4. ¿Cuál es el papel del journaling y en qué situaciones puede evitar una pérdida de datos?  
5. ¿Cómo montar temporalmente un dispositivo y verificar que su FS está saludable antes de usarlo?

<!-- trazabilidad: run_id=run-20261106-224430-ceacfa concept=06-operating-systems-linux-08-file-systems written_at=2026-11-07T01:45:21.340590+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/09 - File Permissions|File Permissions]]
- [[06 - Operating Systems & Linux/10 - Users & Groups|Users & Groups]]

---
← [[06 - Operating Systems & Linux/07 - Stack & Heap|Stack & Heap]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/09 - File Permissions|File Permissions]] →
