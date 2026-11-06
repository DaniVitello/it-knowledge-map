---
title: "CDN / Load Balancing"
area: "Networking / Internet"
numero: 25
aliases: ["CDN / Load Balancing"]
tags: [concepto, it/networking-internet]
---
# CDN / Load Balancing

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 25 de 25**

## Qué abarca
- Distribución y escalamiento del tráfico

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo CDN y load balancing para distribuir el tráfico de usuarios hacia los servidores que entregan contenido estático o dinámico, reduciendo la latencia y evitando cuellos de botella. Resuelvo problemas de congestión y fallos de disponibilidad al repartir peticiones entre múltiples puntos de presencia y servidores backend. En mi día a día como ingeniero de redes senior, los configuro en los edge routers o en los servicios de nube para que la entrega de video, imágenes o APIs sea constante aunque aumente la carga. Después de entender cómo funcionan, puedo diseñar arquitecturas resilientes, dimensionar capacidad y diagnosticar por qué una petición no llega al origen. Cuando la aplicación es monolítica y el tráfico es bajo, no es necesario preocuparse por CDN o balanceadores.

## Esqueleto (el 20% esencial)
1. **Distribución geográfica del tráfico** – los CDN replican contenido en nodos cercanos al usuario para minimizar la distancia de red.  
2. **Escalamiento horizontal** – los load balancers reparten solicitudes entre varios servidores idénticos, aumentando la capacidad total.  
3. **Mejora de la disponibilidad** – si un nodo o servidor falla, el tráfico se redirige automáticamente a los restantes.  
4. **Caché en el edge** – los CDN almacenan respuestas y sirven versiones en caché, reduciendo la carga del origen.  
5. **Visibilidad y métricas** – ambos componentes generan logs que permiten detectar cuellos de botella y planificar capacidad.

## Como funciona
1. El cliente resuelve el DNS del dominio; el registro apunta a la red de distribución del CDN.  
2. El resolver devuelve la IP del nodo edge más cercano según la latencia y la política de geolocalización.  
3. El nodo edge verifica su caché; si el objeto está almacenado, lo entrega inmediatamente.  
4. Si la caché está vacía, el nodo solicita el contenido al origen a través de un reverse proxy o load balancer.  
5. El load balancer selecciona un servidor backend siguiendo una estrategia (round‑robin, least‑connections, etc.) y envía la petición.  
6. La respuesta vuelve al nodo edge, se almacena en caché y se entrega al cliente, mientras se registran métricas de tiempo y éxito.

## Detalles
- **Básico:** Configuración de un registro CNAME que delega el dominio al proveedor de CDN y activación de un balanceador de capa 4 (TCP) con algoritmo round‑robin.  
- **Intermedio:** Uso de políticas de caché (TTL, cache‑control) y balanceo de capa 7 (HTTP) que permite enrutar por ruta, encabezado o peso. Se añaden health‑checks para detectar servidores enfermos.  
- **Avanzado:** Implementación de Anycast para que el mismo bloque IP sea anunciado desde múltiples puntos, integración con WAF (Web Application Firewall) y uso de algoritmos de carga predictiva basados en telemetría en tiempo real.

## Ejemplo minimo
```nginx
# reverse proxy + load balancing simple
upstream app_servers {
    server 10.0.1.10;
    server 10.0.1.11;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
    }
}
```
Este bloque de configuración de Nginx actúa como un reverse proxy que reparte las peticiones HTTP entre dos servidores backend.

## Errores comunes
- **Cache demasiado agresiva:** sirve contenido obsolejo; ajustar TTL y usar encabezados `Cache-Control`.  
- **Health‑check mal configurado:** el balanceador sigue enviando tráfico a servidores caídos; validar respuestas HTTP 200.  
- **Sobrecarga de DNS:** usar TTL bajo en registros CNAME puede generar consultas excesivas; equilibrar con TTL razonable.  
- **Ignorar la afinidad de sesión:** aplicaciones stateful pueden romperse; habilitar sticky sessions o externalizar el estado.  

## Estado actual
- **Fundamentos estables:** los principios de distribución geográfica, caché en edge y algoritmos de balanceo (round‑robin, least‑connections) son ampliamente soportados por proveedores como Cloudflare, Akamai y AWS.  
- **Práctica moderna:** el uso de Anycast, integración con observabilidad basada en OpenTelemetry y la adopción de políticas de seguridad Zero‑Trust (WAF, DDoS mitigation) están en expansión y varían según el proveedor.

## Conexiones
- **Reliability:** CDN y load balancing aumentan la fiabilidad al eliminar puntos únicos de falla.  
- **Reverse Proxies:** el balanceador actúa como un reverse proxy que oculta la topología interna y permite aplicar reglas de enrutamiento.  
- **Caching:** la caché en el edge reduce la carga del origen y mejora la latencia percibida por el usuario.

## Ruta de estudio
1. **Prerequisitos:** TCP/IP, DNS, conceptos de HTTP y conceptos básicos de virtualización de red.  
2. **Fundamentos:** estudiar modelos de CDN (edge nodes, PoPs) y tipos de balanceadores (L4 vs L7). Practicar con Nginx o HAProxy.  
3. **Intermedio:** configurar health‑checks, políticas de caché y TLS termination en un CDN comercial.  
4. **Avanzado:** implementar Anycast con BGP, integrar WAF y observar métricas con Prometheus + Grafana.  
5. **Especialización:** explorar algoritmos de carga predictiva y arquitecturas serverless que dependen de CDN para la entrega de funciones.

## Preguntas de repaso
1. ¿Cómo decide el DNS cuál nodo edge del CDN debe atender a un cliente?  
2. ¿Qué diferencia hay entre un balanceador de capa 4 y uno de capa 7?  
3. ¿Cuál es el riesgo de usar un TTL muy bajo en los registros CNAME de un CDN?  
4. ¿Cómo afecta la configuración de `Cache-Control` a la frescura del contenido servido por el CDN?  
5. ¿Qué mecanismo permite que un balanceador deje de enviar tráfico a un servidor que falló?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-25-cdn-load-balancing written_at=2026-11-05T23:36:50.109060+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/27 - Reliability|Reliability]] · *Software Engineering*
- [[01 - Software Engineering/28 - Distributed Systems|Distributed Systems]] · *Software Engineering*
- [[02 - Frontend/18 - Data fetching|Data fetching]] · *Frontend*
- [[02 - Frontend/23 - Performance|Performance]] · *Frontend*
- [[02 - Frontend/24 - Rendering moderno|Rendering moderno]] · *Frontend*
- [[03 - Backend/19 - Caching|Caching]] · *Backend*
- [[03 - Backend/25 - Sistemas distribuidos|Sistemas distribuidos]] · *Backend*
- [[05 - Networking & Internet/23 - Proxies - Reverse Proxies|Proxies / Reverse Proxies]]
- [[05 - Networking & Internet/24 - Firewalls|Firewalls]]

---
← [[05 - Networking & Internet/24 - Firewalls|Firewalls]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]]
