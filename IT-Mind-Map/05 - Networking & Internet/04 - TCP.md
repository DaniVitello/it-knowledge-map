---
title: "TCP"
area: "Networking / Internet"
numero: 4
aliases: ["TCP"]
tags: [concepto, it/networking-internet]
---
# TCP

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 4 de 25**

## Qué abarca
- Comunicación confiable orientada a conexión

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo TCP para transportar datos entre dos hosts con garantía de entrega íntegra y ordenada. Resuelvo problemas de pérdida, duplicación o reordenamiento de paquetes que aparecen en enlaces IP sin fiabilidad. En mi día a día como ingeniero de redes senior, empleo TCP al diagnosticar flujos de aplicaciones críticas, validar la capacidad de los firewalls o ajustar los parámetros de congestión. Cuando entiendo el establecimiento, la gestión de ventanas y el cierre de una conexión TCP, puedo interpretar trazas de `tcpdump`, diseñar políticas de QoS y depurar fallos de conectividad. No necesito preocuparme por TCP cuando la comunicación es unidireccional, de baja latencia y tolerante a pérdidas, casos en los que suele usarse UDP.

## Esqueleto (el 20% esencial)
1. **Conexión orientada** – TCP crea un circuito lógico mediante el handshake de tres pasos antes de intercambiar datos.  
2. **Fiabilidad** – Cada segmento lleva número de secuencia y acuse de recibo; los paquetes perdidos se retransmiten.  
3. **Control de flujo y congestión** – La ventana deslizante y los algoritmos de congestión evitan saturar al receptor y la red.  
4. **Cierre ordenado** – El proceso de “four‑way handshake” libera recursos de forma segura.  

## Como funciona
1. **Handshake (SYN, SYN‑ACK, ACK)**: el cliente envía un segmento SYN, el servidor responde con SYN‑ACK y el cliente finaliza con ACK, estableciendo los números de secuencia iniciales.  
2. **Transferencia**: los datos se fragmentan en segmentos; cada uno lleva número de secuencia y el receptor envía ACK con el número del siguiente byte esperado.  
3. **Retransmisión**: si el ACK no llega dentro del timeout, el emisor vuelve a enviar el segmento.  
4. **Ventana deslizante**: el receptor indica cuántos bytes puede aceptar, limitando la velocidad del emisor.  
5. **Cierre**: el initiador envía FIN, el otro responde con ACK y luego envía su propio FIN, que se confirma con un último ACK.

## Detalles
- **Básico**: handshake, numeración de bytes y ACK.  
- **Intermedio**: ventana de congestión (slow start, congestion avoidance), retransmisión por timeout y fast retransmit.  
- **Avanzado**: opciones TCP (MSS, SACK, timestamp), tuning de buffers en Linux (`/proc/sys/net/ipv4/tcp_*`), y algoritmos de control de congestión modernos (CUBIC, BBR).

## Ejemplo minimo
```bash
# Servidor TCP escuchando en el puerto 12345
nc -l 12345 &
# Cliente que abre la conexión y envía una línea
echo "hola" | nc localhost 12345
```
Salida del cliente: `hola`. El servidor muestra la misma cadena y la conexión se cierra automáticamente tras el intercambio, demostrando el handshake implícito y la entrega fiable de un solo segmento.

## Errores comunes
- **Olvidar cerrar el socket** → puertos quedan en estado TIME_WAIT; usar `nc -z` para pruebas rápidas.  
- **Confundir puertos UDP con TCP** → verifica con `netstat -tln` que el servicio está escuchando en TCP.  
- **Desactivar la retransmisión** en pruebas de laboratorio → elimina la fiabilidad y genera falsos negativos; mantén los valores por defecto del kernel.  

## Estado actual
**Fundamentos estables**: el modelo de tres‑way handshake, numeración de secuencia, ACK y el algoritmo de control de congestión básico siguen siendo la base de todas las implementaciones TCP.  
**Práctica moderna**: los sistemas Linux usan CUBIC como algoritmo predeterminado y exponen parámetros tunables (`tcp_congestion_control`, `tcp_rmem`, `tcp_wmem`). Además, la adopción de TCP Fast Open y de extensiones como SACK mejora la latencia y la eficiencia en entornos de alta velocidad.

## Conexiones
- **IP**: TCP se encapsula dentro de paquetes IP, por lo que la dirección de origen/destino y el encaminamiento dependen de la capa de red.  
- **Sockets**: la API de sockets expone funciones (`socket()`, `connect()`, `listen()`, `accept()`) que permiten a aplicaciones crear y gestionar conexiones TCP.  
- **HTTP**: la mayoría de las peticiones web utilizan TCP como transporte, de modo que la disponibilidad de un servidor HTTP depende directamente del correcto funcionamiento de TCP.

## Ruta de estudio
1. **Prerequisitos**: comprensión de la capa IP, direcciones IPv4/IPv6 y uso básico de la línea de comandos en Linux.  
2. **Fundamentos**: estudiar el handshake, numeración de bytes y ACK con `tcpdump` y `wireshark`.  
3. **Control de flujo y congestión**: experimentar con `sysctl -w net.ipv4.tcp_congestion_control=cubic` y observar su efecto en pruebas de carga (`iperf`).  
4. **Opciones avanzadas**: leer la documentación de `man 7 tcp` para SACK, MSS y TCP Fast Open; probar configuraciones en entornos de alta latencia.  
5. **Especialización**: integrar TCP con balanceadores de carga, inspección profunda de paquetes (DPI) y TLS para seguridad de capa de transporte.

## Preguntas de repaso
1. ¿Qué información intercambia el three‑way handshake y por qué es esencial para la fiabilidad?  
2. ¿Cómo determina el emisor cuántos bytes puede enviar antes de recibir un ACK?  
3. ¿Qué ocurre cuando un segmento se pierde y el timeout expira?  
4. ¿Cuál es la diferencia práctica entre los algoritmos de congestión CUBIC y BBR?  
5. ¿Cómo se verifica con `netstat` que un servicio está escuchando en TCP y no en UDP?

<!-- trazabilidad: run_id=run-20261105-201026-0a44b6 concept=05-networking-internet-04-tcp written_at=2026-11-05T23:13:14.555446+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/02 - IP|IP]]
- [[05 - Networking & Internet/05 - UDP|UDP]]
- [[05 - Networking & Internet/06 - Puertos|Puertos]]
- [[05 - Networking & Internet/15 - OSI - TCP-IP Model|OSI / TCP-IP Model]]
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[06 - Operating Systems & Linux/14 - Sockets|Sockets]] · *Operating Systems / Linux*
- [[06 - Operating Systems & Linux/22 - Networking en Linux|Networking en Linux]] · *Operating Systems / Linux*

---
← [[05 - Networking & Internet/03 - IPv4 - IPv6|IPv4 / IPv6]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/05 - UDP|UDP]] →
