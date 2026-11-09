---
title: "Proxies / Reverse Proxies"
area: "Networking / Internet"
numero: 23
aliases: ["Proxies / Reverse Proxies"]
tags: [concepto, it/networking-internet]
---
# Proxies / Reverse Proxies

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 23 de 25**

## Qué abarca
- Intermediarios entre clientes y servidores

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo proxies y reverse proxies para intermediar el tráfico entre clientes y servidores, de modo que puedo ocultar la verdadera dirección del origen, aplicar políticas de acceso y balancear la carga. Resuelvo problemas de conectividad como saturación de servidores, exposición de servicios internos y filtrado de contenido no deseado. En mi día a día como ingeniero de redes senior, los configuro en la frontera de la red o delante de aplicaciones web para mejorar la disponibilidad y la seguridad. Después de entender su funcionamiento, puedo diseñar arquitecturas resilientes, integrar firewalls y CDN, y depurar fallos de capa 7. Cuando el tráfico es directo y no se requieren transformaciones ni control de acceso, no es necesario preocuparme por proxies.

## Esqueleto (el 20% esencial)
1. **Intermediario de capa 7** – recibe peticiones HTTP/HTTPS y las reenvía al servidor backend.  
2. **Ocultamiento y control** – protege la IP real del servidor y permite aplicar reglas de acceso.  
3. **Balanceo y caché** – distribuye la carga entre varios backends y almacena respuestas frecuentes.  
4. **Terminación TLS** – descifra el tráfico cifrado antes de enviarlo al servidor interno.  

## Como funciona
1. El cliente abre una conexión TCP al proxy (puede ser un puerto 80/443).  
2. El proxy recibe la solicitud HTTP y, según su configuración, decide a qué backend enviarla.  
3. Si el proxy actúa como reverse proxy, reescribe encabezados como `Host` y `X-Forwarded-For`.  
4. Opcionalmente, el proxy almacena la respuesta en caché o la entrega a un algoritmo de balanceo.  
5. La respuesta viaja de regreso al cliente, manteniendo oculta la dirección del servidor origen.

## Detalles
- **Básico:** Configuración de un proxy forward (ej. Squid) para filtrar tráfico saliente.  
- **Intermedio:** Implementación de un reverse proxy (ej. Nginx) con reglas de reescritura y terminación TLS.  
- **Avanzado:** Integración de health checks, sticky sessions y caché distribuida; uso de HTTP/2 y gRPC con proxy.

## Ejemplo minimo
```bash
# Nginx como reverse proxy simple
cat > /etc/nginx/conf.d/reverse.conf <<'EOF'
server {
    listen 80;
    location / {
        proxy_pass http://10.0.0.10:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
EOF
nginx -s reload
```
El cliente que accede a `http://proxy.example.com` recibe la respuesta del backend `10.0.0.10:8080` sin conocer su IP.

## Errores comunes
- **Olvidar reenviar encabezados críticos** – causa pérdida de información de cliente; usar `proxy_set_header` para preservarlos.  
- **Configurar TLS solo en el backend** – genera doble cifrado y latencia; terminar TLS en el proxy cuando sea posible.  
- **No validar certificados del backend** – abre vulnerabilidad de MITM; habilitar `proxy_ssl_verify` en Nginx.

## Estado actual
- **Fundamentos estables:** El modelo cliente‑proxy‑servidor y la terminación TLS siguen siendo la base de la arquitectura.  
- **Práctica moderna:** Se emplean reverse proxies como punto de entrada para microservicios, combinando balanceo de carga, observabilidad (tracing) y políticas de seguridad basadas en Zero Trust.

## Conexiones
- **Firewall:** El proxy actúa como punto de inspección donde el firewall puede aplicar reglas de capa 7 antes de que el tráfico alcance los servidores.  
- **CDN:** Un reverse proxy puede delegar contenido estático a una CDN, reduciendo la carga del backend y mejorando la latencia global.  
- **Load Balancing:** El proxy incorpora algoritmos de balanceo (round‑robin, least‑connections) para distribuir peticiones entre varios servidores.

## Ruta de estudio
1. **Prerequisitos:** TCP/IP, modelo OSI, conceptos de HTTP/HTTPS y TLS.  
2. **Fundamentos:** Configuración de un proxy forward (Squid) y de un reverse proxy básico (Nginx/HAProxy).  
3. **Intermedio:** Reescritura de encabezados, terminación TLS, caché y health checks.  
4. **Avanzado:** Integración con service mesh, observabilidad (metrics, logs), políticas Zero Trust y despliegues en contenedores/Kubernetes.

## Preguntas de repaso
1. ¿Qué ventaja aporta el ocultamiento de la IP del servidor al usar un reverse proxy?  
2. ¿Cómo se preserva la dirección original del cliente cuando el tráfico pasa por un proxy?  
3. ¿En qué situación es preferible terminar TLS en el proxy en lugar de en el backend?  
4. ¿Cuál es la diferencia funcional entre un proxy forward y un reverse proxy?  
5. ¿Qué configuración mínima necesita Nginx para actuar como reverse proxy de una aplicación en `10.0.0.10:8080`?

<!-- trazabilidad: run_id=run-20261109-162345-ef6bff concept=05-networking-internet-23-proxies-reverse-proxies written_at=2026-11-09T19:25:08.647025+00:00 -->
<!-- ai:end -->

## Relacionados
- [[05 - Networking & Internet/24 - Firewalls|Firewalls]]
- [[05 - Networking & Internet/25 - CDN - Load Balancing|CDN / Load Balancing]]

---
← [[05 - Networking & Internet/22 - WebSockets|WebSockets]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/24 - Firewalls|Firewalls]] →
