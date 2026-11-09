---
title: "Virtualization & Infrastructure"
area: "Operating Systems / Linux"
numero: 25
aliases: ["Virtualization & Infrastructure"]
tags: [concepto, it/operating-systems-linux]
---
# Virtualization & Infrastructure

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 25 de 25**

## Qué abarca
- VMs
- hypervisors
- cloud infrastructure

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la virtualización para aislar cargas de trabajo en máquinas virtuales (VM) o en hipervisores, lo que me permite ejecutar varios sistemas operativos sobre un mismo host Linux sin interferencias mutuas. Resuelvo problemas de consolidación de servidores, pruebas de software en entornos controlados y recuperación ante fallos, ya que cada VM puede migrarse o restaurarse independientemente. En mi día a día como ingeniero senior, la virtualización aparece al provisionar entornos de desarrollo, al diagnosticar cuellos de botella de recursos y al implementar infraestructura de nube privada. Después de dominarla, puedo diseñar arquitecturas híbridas que combinan VMs y contenedores, automatizar despliegues con CI/CD y escalar servicios bajo demanda. No necesito preocuparme cuando la carga es mínima y el hardware dedicado cubre los requisitos sin sobrecarga de gestión.

## Esqueleto (el 20% esencial)
1. **Máquinas virtuales (VM)** – unidades aisladas que ejecutan su propio kernel sobre el hardware virtualizado.  
2. **Hipervisores** – software que crea y gestiona VMs; pueden ser tipo 1 (bare‑metal) o tipo 2 (hosted).  
3. **Infraestructura de nube** – conjunto de hipervisores, redes y almacenamiento que permite escalar VMs bajo demanda.  
4. **Gestión con libvirt/virsh** – interfaz estándar para controlar hipervisores desde la línea de comandos.  
5. **Migración y snapshot** – técnicas para mover VMs entre hosts o guardar su estado sin detenerlas.

## Como funciona
1. El hipervisor accede directamente al hardware (tipo 1) o se ejecuta sobre el kernel Linux (tipo 2).  
2. Al crear una VM, el hipervisor reserva CPU, memoria y discos virtuales definidos en una descripción XML (libvirt).  
3. El kernel de la VM se carga en un entorno aislado; los dispositivos físicos se presentan como virt‑devices (e.g., virtio‑net).  
4. El administrador usa `virsh` o `virt-manager` para iniciar, detener o inspeccionar la VM.  
5. Durante la ejecución, el hipervisor traduce las peticiones de la VM a operaciones reales del host, manteniendo el aislamiento.  
6. Opcionalmente, se pueden crear snapshots o migrar la VM en vivo a otro host para balancear carga o realizar mantenimiento.

## Detalles
- **Básico**: instalación de KVM (`apt install qemu-kvm libvirt-daemon-system`) y verificación con `kvm-ok`.  
- **Intermedio**: definición de dominios XML, uso de `virsh define`, configuración de redes NAT o bridge, y creación de volúmenes con `virsh vol-create-as`.  
- **Avanzado**: configuración de SR‑IOV para pasar dispositivos PCI directamente, uso de `virsh migrate` con protocolos TLS, y automatización mediante Ansible o Terraform que interactúan con la API de libvirt.

## Ejemplo minimo
```bash
# Crear una VM de prueba con 512 MiB RAM y un disco de 5 GiB
sudo virt-install \
  --name testvm \
  --ram 512 \
  --vcpus 1 \
  --os-type linux \
  --disk path=/var/lib/libvirt/images/testvm.qcow2,size=5 \
  --import \
  --noautoconsole
```

**Salida esperada (resumida)**  
```
Domain testvm created
Starting install...
Domain testvm started
```

El comando reserva recursos, crea el archivo de disco y arranca la VM usando la imagen de sistema operativo ya preparada. Con `virsh list --all` se verifica que `testvm` aparece en estado *running*.

## Errores comunes
- **Olvidar habilitar la virtualización en BIOS** → la instalación de KVM falla; verificar con `egrep -c '(vmx|svm)' /proc/cpuinfo`.  
- **Asignar más RAM de la disponible** → la VM no arranca; usar `free -h` para comprobar la memoria libre.  
- **Usar rutas de disco inexistentes** → `virsh` devuelve “failed to open file”; crear el directorio antes de definir la VM.  
- **No configurar una red bridge** → la VM no tiene conectividad externa; crear `br0` y asociarla al dominio.  

## Estado actual
- **Fundamentos estables**: KVM como hipervisor integrado en el kernel Linux, libvirt como capa de gestión, y los comandos `virsh`/`virt-install` son ampliamente soportados en distribuciones modernas.  
- **Práctica moderna**: integración de hipervisores con plataformas de nube privada (OpenStack, oVirt), uso de APIs REST de libvirt para orquestación, y despliegues automatizados con Terraform o Ansible que generan los XML de dominio de forma declarativa.

## Conexiones
- **CI/CD** – los pipelines pueden lanzar VMs temporales para pruebas de integración, garantizando que el código se valida en un entorno idéntico al de producción.  
- **Containers** – los contenedores se ejecutan frecuentemente dentro de VMs para añadir una capa extra de aislamiento y para reutilizar hipervisores en entornos multi‑tenant.  
- **AI Infrastructure** – los entrenamientos de modelos de IA requieren GPUs que se exponen a VMs mediante passthrough, permitiendo escalar recursos de cómputo bajo demanda.

## Ruta de estudio
1. **Prerequisitos**: conocimientos sólidos de Linux (gestión de procesos, networking, permisos) y de la línea de comandos.  
2. **Fundamentos**: instalar KVM, crear y gestionar VMs con `virt-install` y `virsh`.  
3. **Redes y almacenamiento**: configurar bridges, NAT y volúmenes LVM o ZFS para discos virtuales.  
4. **Automatización**: aprender Ansible o Terraform para describir infraestructuras como código.  
5. **Escalado avanzado**: estudiar OpenStack o oVirt, y técnicas de migración en vivo y SR‑IOV.  

## Preguntas de repaso
1. ¿Qué diferencia hay entre un hipervisor tipo 1 y tipo 2 en un host Linux?  
2. ¿Cómo verifica si el CPU del servidor soporta la virtualización requerida por KVM?  
3. ¿Qué comando usaría para listar todas las VMs, incluidas las apagadas?  
4. ¿Por qué es útil crear un snapshot de una VM antes de aplicar una actualización del kernel?  
5. ¿De qué manera un pipeline de CI/CD puede beneficiarse de lanzar una VM en lugar de un contenedor?

<!-- trazabilidad: run_id=run-20261106-225912-2555a0 concept=06-operating-systems-linux-25-virtualization-infrastructure written_at=2026-11-07T02:00:25.926444+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/25 - CI-CD|CI/CD]] · *Software Engineering*
- [[03 - Backend/24 - Deploy & Infraestructura|Deploy & Infraestructura]] · *Backend*
- [[06 - Operating Systems & Linux/24 - Containers|Containers]]
- [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]] · *AI Engineering*

---
← [[06 - Operating Systems & Linux/24 - Containers|Containers]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]]
