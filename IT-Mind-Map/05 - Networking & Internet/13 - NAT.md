---
title: "NAT"
area: "Networking / Internet"
numero: 13
aliases: ["NAT"]
tags: [concepto, it/networking-internet]
---
# NAT

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 13 de 25**

## Qué abarca
- Traducción entre direcciones privadas y públicas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo NAT para que los dispositivos de una red interna con direcciones privadas puedan comunicarse con Internet usando una única dirección pública, lo que resuelve el agotamiento de IPv4 y protege la topología interna. En mi día a día de ingeniero de redes senior, lo aplico al diseñar la frontera entre la LAN y el ISP, al diagnosticar fallas de conectividad que aparecen cuando los hosts internos no pueden salir a la red externa, y al validar que los servicios publicados (por ejemplo, un servidor web) sean accesibles desde fuera. Después de comprender NAT, puedo planificar la asignación de direcciones, configurar firewalls y balanceadores que dependan de la traducción de puertos, y depurar problemas de “address not reachable”. Cuando la red está totalmente IPv6 o se usa un proxy transparente, NAT deja de ser relevante.

## Esqueleto (el 20% esencial)
1. **Traducción de direcciones**: NAT reemplaza la IP privada de origen por la IP pública del router al salir del tráfico.  
2. **Tipos de NAT**: *Source NAT* (SNAT) para salida, *Destination NAT* (DNAT) para entrada, y *Port Address Translation* (PAT) que reutiliza puertos.  
3. **Relación con routing**: El router sigue tomando decisiones de encaminamiento antes de aplicar la traducción.  
4. **Impacto en subnetting/CIDR**: NAT permite usar subredes privadas (por ejemplo, 10.0.0.0/8) sin colisiones con la red pública.

## Como funciona
1. Un host interno envía un paquete con su IP privada y puerto origen.  
2. El router recibe el paquete, consulta su tabla de rutas y determina que el siguiente salto es el ISP.  
3. Antes de reenviarlo, el módulo NAT sustituye la IP de origen por la IP pública del router y, si es PAT, asigna un puerto de salida único, guardando la asociación en su tabla de traducción.  
4. El paquete sale hacia Internet; la respuesta llega a la IP pública y puerto asignado.  
5. El router revierte la traducción usando la tabla, restaurando la IP y puerto originales y entrega el paquete al host interno.

## Detalles
- **Básico**: Configuración de SNAT/PAT en routers domésticos o firewalls; tabla de traducción temporal.  
- **Intermedio**: DNAT para publicar servidores internos, uso de ACLs para limitar qué tráfico se traduce, y manejo de colisiones de puertos.  
- **Avanzado**: NAT64 para IPv6‑IPv4 interop, NAT en entornos de alta disponibilidad (VRRP/HSRP) donde la tabla debe sincronizarse, y optimizaciones de rendimiento con hardware de ASIC.

## Ejemplo minimo
```bash
# Configuración rápida de NAT en Linux (iptables)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```
Salida esperada: la regla se añade sin mensaje; a partir de ahora, cualquier paquete que salga por *eth0* tendrá la IP de *eth0* como origen. Con `iptables -t nat -L -n -v` se ve el contador de bytes/paquetes que atraviesan la regla, confirmando que la traducción está activa.

## Errores comunes
- **Olvidar habilitar el reenvío de IP** (`net.ipv4.ip_forward=1`); sin él, los paquetes nunca salen del host.  
- **Confundir SNAT y DNAT**; aplicar la regla equivocada impide el acceso externo al servidor.  
- **Colisión de puertos en PAT**; usar rangos de puertos restringidos en la ACL evita sobrescrituras inesperadas.  

## Estado actual
- **Fundamentos estables**: La lógica de sustitución de direcciones y la tabla de traducción son parte del estándar IPv4 desde hace décadas y siguen sin cambios.  
- **Práctica moderna**: En entornos cloud se prefiere *NAT Gateway* gestionado, y en IPv6 se recurre a NAT64/DNS64 solo cuando es estrictamente necesario. Los firewalls de próxima generación integran NAT con inspección profunda de paquetes y políticas basadas en aplicaciones.

## Conexiones
- **Routing**: NAT se ejecuta después de que el router decide el mejor camino, por lo que depende de la tabla de rutas para saber cuándo aplicar la traducción.  
- **Routers**: Los dispositivos que hacen NAT son típicamente routers de borde; su capacidad de procesamiento afecta la latencia de la traducción.  
- **Subnetting / CIDR**: NAT permite que múltiples subredes privadas compartan una única dirección pública, simplificando la planificación de bloques CIDR internos.

## Ruta de estudio
1. **Prerequisitos**: IPv4 addressing, conceptos de routing y tablas de encaminamiento, fundamentos de firewalls.  
2. **Fundamentos**: Configuración de SNAT/PAT en Linux y Cisco IOS, análisis de tablas de traducción.  
3. **Intermedio**: DNAT para servidores internos, NAT en entornos con alta disponibilidad, uso de ACLs con NAT.  
4. **Avanzado**: NAT64/DNS64, integración con SD‑WAN, optimizaciones de hardware y monitoreo de rendimiento.  
5. **Especialización**: Implementación de NAT en plataformas cloud (AWS NAT Gateway, Azure NAT) y en contenedores/Kubernetes (kube‑proxy, CNI plugins).

## Preguntas de repaso
1. ¿Qué diferencia hay entre SNAT y DNAT y cuándo se usa cada uno?  
2. ¿Cómo afecta la tabla de rutas al momento de aplicar NAT en un paquete?  
3. ¿Qué paso falta si después de crear una regla MASQUERADE el tráfico sigue sin salir?  
4. ¿En qué situaciones un ingeniero de redes optaría por NAT64 en lugar de una solución IPv6 pura?  
5. ¿Cómo se evita la colisión de puertos cuando se usa PAT en un entorno con muchos hosts simultáneos?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-13-nat written_at=2026-11-05T23:26:03.905924+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/11 - Routing|Routing]]
- [[05 - Networking & Internet/12 - Routers|Routers]]
- [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]]

---
← [[05 - Networking & Internet/12 - Routers|Routers]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]] →
