---
title: "UDP"
area: "Networking / Internet"
numero: 5
aliases: ["UDP"]
tags: [concepto, it/networking-internet]
---
# UDP

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 5 de 25**

## Qué abarca
- Comunicación rápida sin conexión

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo UDP cuando necesito enviar datos de forma rápida y sin establecer una conexión previa, como en streaming de video, juegos en tiempo real o consultas DNS. Resuelvo el problema de la latencia que introduce el handshake de TCP, permitiendo que los paquetes salgan inmediatamente y sean procesados por el receptor sin confirmaciones. En mi día a día como ingeniero de redes senior, lo empleo para diagnosticar pérdidas de paquetes, medir jitter y validar la capacidad de la red para transportar tráfico sin garantía de entrega. Después de entender UDP puedo diseñar y ajustar servicios que toleren pérdida pero requieran velocidad, y también interpretar correctamente trazas de paquetes en herramientas como tcpdump o Wireshark. No necesito preocuparme por UDP cuando la aplicación exige entrega fiable, ordenada y control de congestión; en esos casos TCP u otro protocolo con esas garantías es la elección adecuada.

## Esqueleto (el 20% esencial)
1. **Sin conexión** – UDP envía datagramas sin establecer una sesión, lo que elimina el handshake y reduce la latencia.  
2. **Entrega no garantizada** – No hay retransmisiones ni acuse de recibo; los paquetes pueden perderse o llegar fuera de orden.  
3. **Uso de puertos** – Cada datagrama lleva un número de puerto origen y destino, permitiendo que múltiples aplicaciones compartan la misma IP.  
4. **Aplicaciones en tiempo real** – Servicios que toleran pérdida pero requieren rapidez (VoIP, video, juegos).  
5. **Diagnóstico de red** – Herramientas de prueba (ping UDP, iperf) aprovechan su naturaleza sin conexión para medir pérdida y jitter.

## Como funciona
1. La aplicación crea un socket UDP y lo enlaza a un puerto local.  
2. Cuando necesita enviar datos, empaqueta la información en un datagrama y lo envía al puerto y dirección IP del destino.  
3. El kernel coloca el datagrama en la capa IP y lo transmite inmediatamente; no espera confirmación.  
4. En el receptor, el kernel entrega el datagrama al socket que escucha en el puerto indicado, sin reordenar ni retransmitir.  
5. Si el datagrama se pierde en la ruta, simplemente no llega; la aplicación decide si ignora la pérdida o implementa su propio mecanismo de corrección.

## Detalles
- **Básico**: UDP está definido en el RFC 768; su cabecera tiene 8 bytes (puerto origen, puerto destino, longitud, checksum).  
- **Intermedio**: El checksum opcional protege contra errores de bits; la mayoría de los sistemas lo calculan siempre.  
- **Avanzado**: En redes con NAT o firewalls, los puertos UDP pueden ser filtrados; se usan técnicas como “hole punching” para permitir la comunicación P2P.  
- **QoS**: Aunque UDP no controla congestión, se pueden marcar los paquetes con DSCP para priorizar tráfico sensible a la latencia.  
- **Multiplexado**: Varios procesos pueden usar diferentes puertos UDP simultáneamente sobre la misma interfaz, facilitando servicios concurrentes.

## Ejemplo minimo
```bash
# Servidor UDP que muestra lo que recibe
nc -u -l 12345
# En otra terminal, cliente que envía un mensaje
echo "hola" | nc -u 127.0.0.1 12345
```
Salida del servidor: `hola`

## Errores comunes
- **Asumir entrega fiable** – UDP no reenvía paquetes perdidos; agregar lógica de retransmisión en la aplicación cuando sea necesario.  
- **Confundir puertos con direcciones** – El puerto identifica la aplicación, no la ruta; asegurarse de que el firewall permite el puerto usado.  
- **Olvidar el checksum** – En entornos con alta interferencia, habilitar la verificación de checksum para detectar datos corruptos.

## Estado actual
- **Fundamentos estables**: La cabecera de 8 bytes y la ausencia de control de flujo son parte del estándar RFC 768 y no han cambiado.  
- **Práctica moderna**: UDP se combina con protocolos de capa superior que añaden fiabilidad (QUIC, RTP) y con técnicas de NAT traversal (STUN, TURN) para habilitar comunicaciones P2P en Internet.

## Conexiones
- **TCP** – Protocolo alternativo que garantiza entrega y orden, usado cuando la pérdida de paquetes no es aceptable.  
- **Puertos** – Campo esencial del datagrama UDP que permite a múltiples servicios coexistir en la misma dirección IP.  
- **DNS** – Servicio que utiliza consultas UDP en el puerto 53 para resolver nombres rápidamente, aprovechando la baja sobrecarga del protocolo.

## Ruta de estudio
1. **Prerequisitos**: Modelo OSI, conceptos de IP, máscara de subred y sockets.  
2. **Fundamentos**: Leer RFC 768, practicar con `nc` y `tcpdump` para observar datagramas.  
3. **Intermedio**: Implementar un cliente/servidor UDP en Python o C, añadir checksum y manejo de pérdida.  
4. **Avanzado**: Explorar protocolos basados en UDP (QUIC, RTP), NAT traversal (STUN/TURN) y configuraciones de QoS en routers.  
5. **Especialización**: Optimizar streaming de video o VoIP, medir jitter y jitter buffer, y diseñar mecanismos de corrección a nivel de aplicación.

## Preguntas de repaso
1. ¿Por qué UDP reduce la latencia respecto a TCP?  
2. ¿Qué información lleva la cabecera de un datagrama UDP?  
3. ¿Cómo se diagnostica la pérdida de paquetes en una comunicación UDP?  
4. ¿En qué casos es preferible usar TCP en lugar de UDP?  
5. ¿Qué papel juegan los puertos en la multiplexación de servicios UDP?

<!-- trazabilidad: run_id=run-20261105-201026-0a44b6 concept=05-networking-internet-05-udp written_at=2026-11-05T23:14:11.012733+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/04 - TCP|TCP]]
- [[05 - Networking & Internet/06 - Puertos|Puertos]]

---
← [[05 - Networking & Internet/04 - TCP|TCP]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/06 - Puertos|Puertos]] →
