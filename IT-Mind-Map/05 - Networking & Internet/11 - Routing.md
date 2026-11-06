---
title: "Routing"
area: "Networking / Internet"
numero: 11
aliases: ["Routing"]
tags: [concepto, it/networking-internet]
---
# Routing

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 11 de 25**

## Qué abarca
- Cómo los paquetes encuentran su destino

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el routing para que los paquetes de datos encuentren su destino a través de múltiples redes, resolviendo el problema de la conectividad entre subredes y dominios de Internet. En mi día a día como ingeniero de redes senior, configuro rutas estáticas o depuro protocolos dinámicos cuando una comunicación falla entre sitios. Al comprender cómo se decide el mejor camino, puedo diseñar topologías eficientes, diagnosticar bucles de enrutamiento y aplicar políticas de tráfico. Después de dominar el routing, paso a optimizar el uso de ancho de banda con balanceo y a integrar soluciones de alta disponibilidad. Cuando la red es una única LAN sin segmentación, el routing no es relevante y me enfoco en switching.

## Esqueleto (el 20% esencial)
1. **Tabla de rutas**: almacena los prefijos y el próximo salto que deben usarse para alcanzar cada destino.  
2. **Protocolos de enrutamiento**: intercambian información de rutas entre routers (ej. OSPF, BGP).  
3. **Selección de mejor ruta**: se basa en métricas como coste, longitud del prefijo y política.  
4. **Rutas estáticas vs dinámicas**: las estáticas se configuran manualmente; las dinámicas se aprenden automáticamente.  
5. **Impacto en NAT y subnetting**: el routing determina cómo los paquetes atraviesan zonas NAT y cómo se agrupan los prefijos con CIDR.

## Como funciona
1. Cada router mantiene su tabla de rutas, inicialmente con rutas locales y una ruta por defecto.  
2. Cuando se recibe un paquete, el router extrae la dirección IP de destino y la compara con los prefijos de la tabla.  
3. Aplica la regla de “longest prefix match” para seleccionar la entrada más específica.  
4. Si la ruta es estática, el siguiente salto está predefinido; si es dinámica, el router consulta la métrica aprendida del protocolo correspondiente.  
5. El paquete se reenvía al interfaz indicado y el proceso se repite en el siguiente hop hasta llegar al destino o a la ruta por defecto.

## Detalles
- **Básico**: configuración de rutas estáticas (`ip route`) y verificación con `show ip route`.  
- **Intermedio**: despliegue de un protocolo interior (OSPF) para que los routers intercambien automáticamente prefijos y actualicen sus métricas.  
- **Avanzado**: uso de BGP para anunciar prefijos a Internet, manipulación de atributos (local‑pref, MED) y aplicación de políticas de ruta que influyen en la selección de caminos entre proveedores.  
- En todos los niveles, la interacción con NAT implica que la tabla de rutas debe apuntar al dispositivo que realiza la traducción, y el subnetting/CIDR define la granularidad de los prefijos que aparecen en la tabla.

## Ejemplo minimo
```bash
# En un router Cisco IOS
Router(config)# ip route 10.0.0.0 255.255.255.0 192.168.1.1
Router# show ip route 10.0.0.0
S    10.0.0.0/24 [1/0] via 192.168.1.1, 00:00:12, GigabitEthernet0/1
```
La salida indica que los paquetes destinados a la subred 10.0.0.0/24 se enviarán al siguiente salto 192.168.1.1 a través de la interfaz especificada.

## Errores comunes
- **Olvidar la ruta por defecto**: sin ella, los paquetes a destinos desconocidos se descartan; añada `0.0.0.0/0` apuntando a un gateway.  
- **Confundir métricas de OSPF y BGP**: use la métrica adecuada para cada protocolo; revise los atributos antes de aplicar políticas.  
- **Superposición de prefijos**: evite que dos rutas estáticas cubran el mismo rango, ya que el “longest prefix match” puede producir resultados inesperados; planifique los subnets con CIDR.

## Estado actual
- **Fundamentos estables**: la tabla de rutas, el algoritmo de “longest prefix match” y la distinción entre rutas estáticas y dinámicas son conceptos consolidados y compatibles con cualquier router de nivel empresarial.  
- **Práctica moderna**: la adopción de BGP para interconexión entre centros de datos, el uso de Segment Routing (SR‑TE) para dirigir tráfico sin protocolos adicionales, y la integración de SD‑WAN que abstrae el routing tradicional mediante controladores centralizados.

## Conexiones
- **Routers**: son los dispositivos que ejecutan el algoritmo de routing y mantienen la tabla de rutas.  
- **NAT**: depende del routing para saber a qué interfaz debe enviar los paquetes que serán traducidos de direcciones privadas a públicas.  
- **Subnetting / CIDR**: define los prefijos que aparecen en la tabla de rutas, influyendo en la granularidad y eficiencia del enrutamiento.

## Ruta de estudio
1. **Prerequisitos**: comprensión de direcciones IP, máscara de subred y modelo OSI (capa 3).  
2. **Fundamentos**: práctica con rutas estáticas y comandos `show ip route`.  
3. **Protocolos internos**: OSPF – configuración de áreas y costos.  
4. **Protocolos externos**: BGP – establecimiento de peers, anuncio de prefijos y atributos.  
5. **Optimización**: políticas de ruta, redistribución entre OSPF y BGP, y uso de Segment Routing.  
6. **Integración**: cómo el routing interactúa con NAT y con arquitecturas SD‑WAN.

## Preguntas de repaso
1. ¿Qué criterio usa un router para elegir la entrada de la tabla de rutas cuando varios prefijos coinciden?  
2. ¿En qué situaciones prefiero una ruta estática a un protocolo dinámico?  
3. ¿Cómo afecta la longitud del prefijo (CIDR) a la selección de la mejor ruta?  
4. ¿Cuál es la diferencia principal entre la métrica de OSPF y el atributo `local‑pref` de BGP?  
5. ¿Qué papel juega el routing cuando un paquete atraviesa un dispositivo NAT?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-11-routing written_at=2026-11-05T23:24:16.130629+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/16 - Routing|Routing]] · *Frontend*
- [[03 - Backend/06 - Routing|Routing]] · *Backend*
- [[05 - Networking & Internet/12 - Routers|Routers]]
- [[05 - Networking & Internet/13 - NAT|NAT]]
- [[05 - Networking & Internet/14 - Subnetting - CIDR|Subnetting / CIDR]]

---
← [[05 - Networking & Internet/10 - ARP|ARP]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/12 - Routers|Routers]] →
