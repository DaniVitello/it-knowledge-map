---
title: "Containers"
area: "Operating Systems / Linux"
numero: 24
aliases: ["Containers"]
tags: [concepto, it/operating-systems-linux]
---
# Containers

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 24 de 25**

## Qué abarca
- Namespaces
- isolation
- Docker

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo containers para ejecutar aplicaciones aisladas dentro del mismo kernel de Linux, evitando conflictos de dependencias y garantizando que el entorno de ejecución sea reproducible. Resuelvo el problema de “funciona en mi máquina” al empaquetar código, librerías y configuraciones en una unidad portable que se comporta igual en desarrollo, pruebas y producción. En mi día a día como ingeniero de sistemas Linux senior, los containers aparecen al desplegar micro‑servicios, al crear entornos de CI/CD y al aislar procesos críticos para diagnóstico sin afectar al host. Después de comprender su mecanismo, puedo diseñar pipelines de despliegue automatizados, optimizar el uso de recursos y depurar problemas de forma segura. Cuando la aplicación ya corre directamente sobre el host y no necesita aislamiento ni portabilidad, no es necesario usar containers.

## Esqueleto (el 20% esencial)
1. **Namespaces**: crean vistas aisladas de recursos del kernel (PID, net, mount, etc.) para cada container.  
2. **Control Groups (cgroups)**: limitan y contabilizan CPU, memoria y I/O de los procesos dentro del container.  
3. **Imagen y runtime**: una imagen (Dockerfile) describe el filesystem y la configuración; el runtime (docker, podman) materializa el container a partir de ella.  
4. **Aislamiento de red y filesystem**: cada container tiene su propio stack de red y su propio árbol de archivos, sin interferir con el host.  

## Como funciona
1. El usuario invoca `docker run` (u otro runtime) indicando la imagen.  
2. El runtime crea un **namespace** nuevo para PID, net, mount, uts y user.  
3. Se configuran **cgroups** que asignan límites de CPU y memoria al proceso raíz del container.  
4. Se monta el **filesystem** de la imagen en un nuevo **mount namespace**, proporcionando un rootfs independiente.  
5. Se inicializa la red virtual (bridge o overlay) dentro del **network namespace** y se asigna una interfaz al container.  
6. El proceso especificado en la imagen se ejecuta como PID 1 dentro de ese entorno aislado.  

## Detalles
- **Básico**: entender que un container no es una VM; comparte el kernel y usa namespaces/cgroups para aislamiento.  
- **Intermedio**: crear imágenes eficientes con capas (Dockerfile), gestionar volúmenes para persistencia y usar redes bridge o host según necesidad.  
- **Avanzado**: orquestar múltiples containers con Kubernetes, ajustar cgroup v2 para QoS, y aplicar políticas de seguridad (seccomp, AppArmor) para reducir la superficie de ataque.  

## Ejemplo minimo
```bash
# Crear una imagen mínima que ejecuta "echo Hola"
cat > Dockerfile <<'EOF'
FROM alpine:latest
CMD ["echo","Hola"]
EOF

docker build -t hola-img .
docker run --rm hola-img
```
Salida:
```
Hola
```
El comando muestra cómo se construye una imagen y se ejecuta en un container aislado, imprimiendo “Hola” y luego desapareciendo.

## Errores comunes
- **Olvidar montar volúmenes**: los datos se pierden al destruir el container; usar `-v host_dir:/container_dir`.  
- **Ejecutar procesos como root**: aumenta el riesgo de escalada; especificar `--user` o usar imágenes sin root.  
- **No limitar recursos**: un container puede consumir toda la memoria del host; definir `--memory` y `--cpus`.  
- **Confundir PID 1 con init**: procesos zombie pueden quedar; usar un init ligero como `tini`.  

## Estado actual
- **Fundamentos estables**: namespaces y cgroups son parte del kernel Linux desde hace versiones maduras y su comportamiento es predecible.  
- **Práctica moderna**: Docker sigue siendo el runtime dominante, pero herramientas como **Podman** y **CRI-O** ganan adopción en entornos sin daemon. Las especificaciones de **OCI** (Open Container Initiative) garantizan interoperabilidad entre runtimes.  

## Conexiones
- **CI/CD**: los containers permiten ejecutar pruebas en entornos idénticos a producción dentro de pipelines automatizados.  
- **Virtualization & Infrastructure**: a diferencia de las VMs, los containers consumen menos recursos y se combinan con hipervisores para crear plataformas híbridas.  
- **AI Infrastructure**: los modelos de IA se despliegan en containers para aislar dependencias de GPU, versiones de CUDA y bibliotecas de aprendizaje profundo.  

## Ruta de estudio
1. **Prerequisitos**: manejo de la línea de comandos Linux, conceptos de procesos y permisos, y familiaridad con archivos de configuración (`/etc/fstab`, `systemd`).  
2. **Fundamentos**: estudiar namespaces (`man 7 namespaces`) y cgroups (`man 7 cgroups`).  
3. **Docker**: seguir tutorial oficial “Get Started”, crear Dockerfiles y practicar con `docker compose`.  
4. **Seguridad**: aprender seccomp, AppArmor y políticas de usuario dentro de containers.  
5. **Orquestación**: introducirse en Kubernetes (pods, deployments, services) y en herramientas de gestión de clústeres.  

## Preguntas de repaso
1. ¿Qué recursos del kernel aísla cada tipo de namespace y por qué es importante para un container?  
2. ¿Cómo limitas el consumo de memoria de un container y qué ocurre si supera ese límite?  
3. ¿Cuál es la diferencia práctica entre montar un volumen y copiar datos dentro de la imagen?  
4. ¿Por qué ejecutar procesos como root dentro de un container puede ser peligroso y cómo mitigarlo?  
5. ¿En qué situaciones preferirías usar Podman en lugar de Docker en un entorno de producción?

<!-- trazabilidad: run_id=run-20261106-225802-dfbfdc concept=06-operating-systems-linux-24-containers written_at=2026-11-07T01:59:11.143783+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/25 - CI-CD|CI/CD]] · *Software Engineering*
- [[03 - Backend/24 - Deploy & Infraestructura|Deploy & Infraestructura]] · *Backend*
- [[06 - Operating Systems & Linux/25 - Virtualization & Infrastructure|Virtualization & Infrastructure]]
- [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]] · *AI Engineering*

---
← [[06 - Operating Systems & Linux/23 - Logs & System Monitoring|Logs & System Monitoring]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/25 - Virtualization & Infrastructure|Virtualization & Infrastructure]] →
