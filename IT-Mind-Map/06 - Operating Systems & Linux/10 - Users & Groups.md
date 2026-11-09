---
title: "Users & Groups"
area: "Operating Systems / Linux"
numero: 10
aliases: ["Users & Groups"]
tags: [concepto, it/operating-systems-linux]
---
# Users & Groups

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 10 de 25**

## Qué abarca
- Identidad y separación de privilegios

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo usuarios y grupos para identificar a cada proceso y a cada archivo dentro del sistema, de modo que pueda asignar y controlar quién puede leer, escribir o ejecutar recursos críticos. Resuelvo el problema de la colisión de privilegios y la exposición accidental de datos al separar la autoridad de cada actor del sistema. En mi día a día como ingeniero Linux senior, los usuarios y grupos aparecen cada vez que creo cuentas de servicio, configuro permisos de directorios compartidos o depuro accesos denegados en logs de `auth.log`. Después de entender este mecanismo, puedo diseñar políticas de seguridad basadas en roles, automatizar la creación de cuentas y auditar el cumplimiento de normas. No necesito preocuparme cuando trabajo exclusivamente con procesos sin interacción humana y con recursos que ya están aislados mediante contenedores o máquinas virtuales.

## Esqueleto (el 20% esencial)
1. **Identidad única** – Cada proceso se ejecuta bajo un UID (User ID) y pertenece a uno o varios GID (Group ID).  
2. **Separación de privilegios** – Los permisos de archivo (`rwx`) se evalúan primero contra el propietario, luego contra el grupo y finalmente contra el resto del mundo.  
3. **Roles mediante grupos** – Agrupar usuarios permite conceder el mismo conjunto de permisos a varios actores sin duplicar configuraciones.  
4. **Persistencia en el kernel** – La tabla de usuarios y grupos (`/etc/passwd`, `/etc/group`) es consultada por el kernel en cada llamada de sistema que requiera autorización.  

## Como funciona
1. Al iniciar sesión, `login` o `sshd` verifica el nombre contra `/etc/passwd` y asigna el UID correspondiente al proceso de la sesión.  
2. El proceso hereda el GID primario del usuario y los GID suplementarios definidos en `/etc/group`.  
3. Cuando el proceso intenta abrir un archivo, el kernel compara el UID/GID del proceso con el propietario y el grupo del inode del archivo.  
4. Según la coincidencia, el kernel aplica los bits de permiso `rwx` del propietario, del grupo o de “otros” y decide permitir o denegar la operación.  

## Detalles
- **Básico**: Creación de usuarios con `useradd`, asignación de contraseñas con `passwd`, y visualización con `id`.  
- **Intermedio**: Uso de grupos secundarios (`usermod -aG`) para otorgar accesos temporales, y configuración de `setgid` en directorios para heredar el GID.  
- **Avanzado**: Manipulación directa de `/etc/shadow` para políticas de expiración, uso de `sudo` con `User_Alias` y `Runas_Alias` para delegar privilegios, y empleo de ACLs (`setfacl`) cuando los bits tradicionales son insuficientes.  

## Ejemplo minimo
```bash
# Crear usuario y grupo
sudo groupadd devops
sudo useradd -m -g devops alice

# Ver identidad del proceso de alice
su - alice -c 'id'
# salida:
# uid=1001(alice) gid=1001(devops) groups=1001(devops)

# Crear archivo y asignar permisos
touch proyecto.txt
chmod 640 proyecto.txt      # rw- r-- ---
chown alice:devops proyecto.txt

# Intentar lectura como otro usuario
sudo -u bob cat proyecto.txt   # falla: Permission denied
```

## Errores comunes
- **Olvidar añadir al usuario al grupo secundario** → el usuario no hereda los permisos esperados; usar `usermod -aG`.  
- **Confundir UID y GID al cambiar propietario** → usar `chown user:group` en vez de `chown user group`.  
- **Asignar permisos 777 por comodidad** → expone datos; aplicar el principio de menor privilegio.  

## Estado actual
Los conceptos de UID/GID y permisos POSIX son fundamentos estables del kernel Linux. En la práctica moderna, se complementan con `sudo` para delegar privilegios de forma granular y con ACLs (`setfacl`) para casos donde los tres niveles tradicionales (`owner`, `group`, `others`) resultan insuficientes. Herramientas como `systemd` también gestionan usuarios y grupos de servicio mediante unidades `User=` y `Group=`.

## Conexiones
- **File Permissions** – Los bits `rwx` que evalúa el kernel dependen directamente del UID/GID del proceso.  
- **File Systems** – Cada inode almacena UID, GID y los bits de permiso; el sistema de archivos los expone al kernel.  
- **sudo** – Permite a usuarios no privilegiados ejecutar comandos con UID 0 u otro UID, basándose en reglas que referencian nombres de usuarios y grupos.  

## Ruta de estudio
1. **Prerequisitos**: Familiarizarse con la línea de comandos, conceptos de procesos y el árbol de directorios Linux.  
2. **Fundamentos**: Leer `/etc/passwd` y `/etc/group`, practicar `useradd`, `groupadd`, `id`, `chmod`, `chown`.  
3. **Intermedio**: Configurar `sudoers` (visualmente con `visudo`), crear grupos secundarios y probar `setgid` en directorios.  
4. **Avanzado**: Implementar ACLs (`setfacl`, `getfacl`), explorar `systemd`‑user units y automatizar la gestión de cuentas con scripts o herramientas como `ansible`.  

## Preguntas de repaso
1. ¿Qué verifica el kernel primero al decidir si un proceso puede leer un archivo?  
2. ¿Cómo añado un usuario existente a un grupo sin perder su grupo primario?  
3. ¿Qué diferencia hay entre los permisos mostrados por `chmod 750` y `chmod 750` aplicado a un directorio?  
4. ¿En qué situación usarías una ACL en lugar de los permisos tradicionales?  
5. ¿Cuál es el efecto de establecer el bit `setgid` en un directorio?

<!-- trazabilidad: run_id=run-20261106-224541-eade0d concept=06-operating-systems-linux-10-users-groups written_at=2026-11-07T01:46:43.076535+00:00 -->
<!-- ai:end -->

## Relacionados
- [[06 - Operating Systems & Linux/08 - File Systems|File Systems]]
- [[06 - Operating Systems & Linux/09 - File Permissions|File Permissions]]

---
← [[06 - Operating Systems & Linux/09 - File Permissions|File Permissions]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/11 - System Calls|System Calls]] →
