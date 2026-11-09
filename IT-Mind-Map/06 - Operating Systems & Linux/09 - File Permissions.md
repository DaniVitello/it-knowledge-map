---
title: "File Permissions"
area: "Operating Systems / Linux"
numero: 9
aliases: ["File Permissions"]
tags: [concepto, it/operating-systems-linux]
---
# File Permissions

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 9 de 25**

## Qué abarca
- Users
- groups
- read/write/execute

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los permisos de archivo para controlar quién puede leer, modificar o ejecutar cada recurso del sistema. Resuelvo problemas de seguridad y de integridad, evitando que usuarios no autorizados alteren configuraciones críticas o accedan a datos sensibles. En mi día a día como ingeniero de sistemas Linux senior, reviso y ajusto los bits de permiso al crear servicios, al depurar scripts de arranque y al auditar directorios compartidos. Después de comprender cómo se representan y aplican los permisos, puedo diseñar políticas de acceso coherentes, automatizar su aplicación con herramientas como `chmod` y `setfacl`, y diagnosticar fallos de “permiso denegado”. Cuando un archivo pertenece a un proceso del kernel o a un usuario del sistema que nunca será accedido por otros, no es necesario preocuparse por sus permisos.

## Esqueleto (el 20% esencial)
1. **Usuarios y grupos** – Cada proceso se ejecuta con la identidad de un UID y pertenece a uno o varios GID, y los permisos se evalúan contra esas identidades.  
2. **Bits de permiso (r, w, x)** – Tres bits por categoría (owner, group, others) indican lectura, escritura y ejecución.  
3. **Orden de evaluación** – El kernel comprueba primero los permisos del propietario, luego los del grupo y, por último, los de “otros”.  
4. **Modificación con `chmod`** – Cambia los bits de permiso de forma explícita o simbólica.  
5. **Herencia y ACLs** – Las listas de control de acceso pueden complementar o sobrescribir los bits tradicionales.

## Como funciona
1. Cuando un proceso intenta abrir un archivo, el kernel extrae su UID y GID.  
2. Busca los bits de permiso del archivo y los compara con la categoría correspondiente (owner, group, others).  
3. Si el bit requerido (r, w o x) está activo, la operación se permite; de lo contrario, el kernel devuelve `EACCES`.  
4. El administrador usa `chmod` (p.ej. `chmod u+rwx,g+rx,o-r file`) para ajustar los bits y volver a habilitar la operación.  
5. Si existen ACLs, el kernel evalúa esas entradas antes de aplicar la regla “others”.

## Detalles
- **Básico**: Entender que `r` permite leer datos, `w` permite modificar el contenido y `x` permite ejecutar o entrar en directorios.  
- **Intermedio**: Manipular permisos simbólicos (`u`, `g`, `o`, `a`) y octales (e.g., `chmod 750 script.sh`). Aprender el efecto de `setuid` y `setgid` en archivos ejecutables.  
- **Avanzado**: Utilizar ACLs con `setfacl`/`getfacl` para otorgar permisos finos a usuarios específicos, y combinar con máscaras (`mask`) para limitar el alcance de las ACLs. También, comprender cómo los bits de sticky (`t`) protegen la eliminación de archivos en directorios compartidos.

## Ejemplo minimo
```bash
# Crear archivo y asignar permisos 640
echo "texto" > demo.txt
chmod 640 demo.txt
ls -l demo.txt
```
Salida:
```
-rw-r----- 1 usuario grupo 6 nov  9 12:34 demo.txt
```
El propietario puede leer y escribir, el grupo solo leer, y otros no tienen acceso.

## Errores comunes
- **Confundir `x` en archivos con `x` en directorios** – En directorios, `x` permite entrar; sin él, no se pueden listar ni acceder a los contenidos.  
- **Usar `chmod 777` como solución rápida** – Otorga acceso total a todos los usuarios, exponiendo el sistema a riesgos.  
- **Olvidar actualizar ACLs después de cambiar los bits tradicionales** – Las ACL pueden quedar desincronizadas y seguir denegando acceso esperado.  
- **No considerar el umask al crear archivos** – El umask define los bits que se restan automáticamente; ignorarlo genera permisos inesperados.  

## Estado actual
**Fundamentos estables**: El modelo de tres categorías (owner, group, others) y los bits `rwx` siguen siendo la base del control de acceso en Linux desde sus primeras versiones. `chmod`, `chown` y `ls -l` son comandos consolidados y compatibles en todas las distribuciones modernas.  

**Práctica moderna**: El uso de ACLs (`setfacl`, `getfacl`) se ha extendido para entornos multi‑usuario y contenedores, ofreciendo permisos granulares sin romper el modelo tradicional. Además, herramientas de gestión de configuración como Ansible o Chef incluyen módulos específicos para asegurar permisos de forma declarativa.

## Conexiones
- **File Systems** – Los permisos se almacenan en los inodos del sistema de archivos, por lo que el tipo de FS (ext4, XFS, Btrfs) determina la disponibilidad de ACLs.  
- **Users & Groups** – La asignación de UID y GID define a qué categoría pertenece cada proceso, influyendo directamente en la evaluación de permisos.  
- **Systemd** – Los servicios pueden especificar `User=` y `Group=` en sus unidades, y el daemon verifica los permisos del binario antes de iniciar el proceso.

## Ruta de estudio
1. **Prerequisitos**: Familiarizarse con la estructura de directorios Linux, conceptos de UID/GID y el comando `ls -l`.  
2. **Fundamentos**: Practicar `chmod`, `chown` y `umask` en un entorno de pruebas; leer la página man de `chmod`.  
3. **Intermedio**: Explorar permisos simbólicos vs octales, y experimentar con `setuid`/`setgid`.  
4. **Avanzado**: Aprender ACLs con `setfacl`/`getfacl`, estudiar la máscara (`mask`) y su interacción con los bits tradicionales.  
5. **Especialización**: Integrar control de permisos en scripts de despliegue (Ansible, Bash) y revisar políticas de seguridad en entornos de contenedores (Docker, Kubernetes).

## Preguntas de repaso
1. ¿Qué combinación de bits permite que el propietario lea y escriba, el grupo solo lea y nadie más acceda?  
2. ¿Cómo afecta el umask a los permisos de un archivo creado con `touch`?  
3. ¿Cuál es la diferencia práctica entre el bit `x` en un archivo y en un directorio?  
4. ¿En qué caso usarías una ACL en lugar de los permisos tradicionales?  
5. ¿Qué comando muestra la máscara (`mask`) de una ACL y por qué es importante?

<!-- trazabilidad: run_id=run-20261109-162603-f52dc2 concept=06-operating-systems-linux-09-file-permissions written_at=2026-11-09T19:26:59.554421+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/08 - File Systems|File Systems]]
- [[06 - Operating Systems & Linux/10 - Users & Groups|Users & Groups]]

---
← [[06 - Operating Systems & Linux/08 - File Systems|File Systems]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/10 - Users & Groups|Users & Groups]] →
