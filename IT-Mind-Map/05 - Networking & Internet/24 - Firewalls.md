---
title: "Firewalls"
area: "Networking / Internet"
numero: 24
aliases: ["Firewalls"]
tags: [concepto, it/networking-internet]
---
# Firewalls

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 24 de 25**

## Qué abarca
- Control de tráfico de red

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo firewalls para inspeccionar y filtrar el tráfico que atraviesa los enlaces de red que administro, de modo que solo los paquetes que cumplen con las políticas de seguridad de la organización pueden entrar o salir. Resuelvo problemas de conectividad no deseada, como accesos no autorizados, ataques de denegación de servicio o fuga de datos, y garantizo que los servicios críticos estén aislados del tráfico externo. En mi día a día como ingeniero de redes senior, el firewall es la primera línea de defensa al diseñar perímetros, segmentar subredes y aplicar controles de acceso basados en IP, puertos y protocolos. Después de comprender su funcionamiento, puedo diseñar arquitecturas de zona desmilitarizada (DMZ), integrar reglas dinámicas con sistemas de detección de intrusiones y automatizar la respuesta a incidentes. Cuando la red está completamente aislada o se usan mecanismos de cifrado extremo‑a‑extremo que ya garantizan la integridad del tráfico, el foco en el firewall puede reducirse.

## Esqueleto (el 20% esencial)
1. **Política de control de tráfico** – define qué flujos están permitidos o denegados según origen, destino, puerto y protocolo.  
2. **Punto de inspección** – el firewall se sitúa en el perímetro o entre zonas para observar cada paquete que cruza.  
3. **Acción basada en reglas** – cada regla evalúa los atributos del paquete y decide permitir, bloquear o registrar.  
4. **Estado de conexión** – los firewalls stateful mantienen contexto de sesiones para permitir respuestas legítimas.  
5. **Integración con otros controles** – se combina con IDS/IPS, proxies y balanceadores para reforzar la seguridad.

## Como funciona
1. El paquete llega al interfaz del firewall (punto de inspección).  
2. El motor evalúa la tabla de reglas en orden de prioridad (política de control).  
3. Si la regla coincide, se ejecuta la acción correspondiente (permitir, bloquear, registrar).  
4. En firewalls stateful, se verifica el estado de la conexión; si es parte de una sesión establecida, se permite sin volver a inspeccionar todos los campos.  
5. El paquete se reenvía al siguiente salto o se descarta, y se genera un log si la regla lo indica.  

## Detalles
- **Básico**: reglas estáticas basadas en IP y puerto (ej. `iptables -A INPUT -s 10.0.0.0/8 -p tcp --dport 22 -j DROP`).  
- **Intermedio**: inspección de capa 7 (protocolos HTTP, DNS) y uso de zonas de seguridad para segmentar la red.  
- **Avanzado**: firewalls de próxima generación (NGFW) que combinan inspección profunda de paquetes (DPI), control de aplicaciones y correlación con inteligencia de amenazas; integración con APIs para reglas dinámicas basadas en reputación de IP.

## Ejemplo minimo
```bash
# Bloquear todo el tráfico SSH entrante desde la red 192.168.100.0/24
iptables -A INPUT -s 192.168.100.0/24 -p tcp --dport 22 -j DROP
```
Salida esperada al intentar conectar desde una máquina de esa subred:
```
ssh: connect to host 10.0.0.5 port 22: Connection timed out
```
El firewall descarta el paquete antes de que llegue al servidor.

## Errores comunes
- **Regla demasiado amplia**: bloquear rangos de IP que incluyen servicios legítimos; evitar especificando puertos y protocolos exactos.  
- **Orden de reglas incorrecto**: colocar una regla genérica antes de una específica hace que la específica nunca se evalúe; ordenar de lo más restrictivo a lo más permisivo.  
- **Olvidar estado de conexión**: en firewalls sin inspección stateful, bloquear respuestas legítimas de sesiones establecidas; habilitar seguimiento de estado cuando sea necesario.  

## Estado actual
**Fundamentos estables**: filtrado basado en IP/puerto, seguimiento de estado de conexión y registro de eventos siguen siendo la base de cualquier firewall.  
**Práctica moderna**: los NGFW incorporan inspección profunda de aplicaciones, control de usuarios mediante integración con directorios (LDAP/Active Directory) y políticas basadas en riesgo dinámico. La automatización mediante APIs y la orquestación con plataformas de seguridad (SOAR) son tendencias consolidadas en entornos empresariales.

## Conexiones
- **Security Engineering** – el diseño de políticas de firewall es una aplicación directa de los principios de ingeniería de seguridad, que buscan minimizar la superficie de ataque.  
- **HTTPS / TLS** – aunque el tráfico está cifrado, el firewall puede filtrar por puertos y, en NGFW, inspeccionar el TLS mediante terminación para aplicar políticas de contenido.  
- **CDN / Load Balancing** – los firewalls se colocan delante de los balanceadores para bloquear tráfico malicioso antes de que llegue a los servidores distribuidos por la CDN.

## Ruta de estudio
1. **Prerequisitos**: comprensión de modelos OSI, direccionamiento IP, subnetting y conceptos de routing.  
2. **Fundamentos**: aprender sintaxis de iptables/nftables, crear reglas estáticas y analizar logs.  
3. **Intermedio**: estudiar firewalls stateful, zonas de seguridad y conceptos de inspección de capa 7.  
4. **Avanzado**: explorar NGFW, integración con IDS/IPS, políticas basadas en usuarios y automatización con APIs.  
5. **Especialización**: implementar firewalls en entornos cloud (AWS Security Groups, Azure NSG) y orquestar con herramientas de gestión de seguridad (e.g., Ansible, Terraform).

## Preguntas de repaso
1. ¿Qué diferencia a un firewall stateful de uno stateless al decidir si permite un paquete?  
2. ¿Cómo afecta el orden de las reglas en una tabla de firewall a la efectividad de la política de seguridad?  
3. ¿Cuál es la ventaja de colocar un firewall delante de un balanceador de carga en una arquitectura de alta disponibilidad?  
4. ¿Qué tipo de inspección permite a un NGFW aplicar políticas a tráfico HTTPS sin romper la confidencialidad?  
5. ¿Qué pasos seguirías para diagnosticar que una regla de firewall está bloqueando inesperadamente una aplicación web?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-24-firewalls written_at=2026-11-05T23:35:41.557440+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/24 - Security Engineering|Security Engineering]] · *Software Engineering*
- [[03 - Backend/18 - Seguridad|Seguridad]] · *Backend*
- [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]]
- [[05 - Networking & Internet/23 - Proxies - Reverse Proxies|Proxies / Reverse Proxies]]
- [[05 - Networking & Internet/25 - CDN - Load Balancing|CDN / Load Balancing]]
- [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]] · *AI Engineering*

---
← [[05 - Networking & Internet/23 - Proxies - Reverse Proxies|Proxies / Reverse Proxies]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/25 - CDN - Load Balancing|CDN / Load Balancing]] →
