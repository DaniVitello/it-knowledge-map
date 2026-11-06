---
title: "Sistemas distribuidos"
area: "Backend"
numero: 25
aliases: ["Sistemas distribuidos"]
tags: [concepto, it/backend]
---
# Sistemas distribuidos

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 25 de 25**

## Qué abarca
- Load balancing
- scaling
- replication
- consistency

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo sistemas distribuidos para diseñar y operar servicios backend que deben atender miles de peticiones por segundo sin perder disponibilidad. Resuelvo el problema de que una única máquina no puede escalar ni tolerar fallos, distribuyendo la lógica de negocio, los datos y la carga entre varios nodos. Aparecen en cada API que necesita alta concurrencia, replicación de datos o tolerancia a fallos, y me permiten añadir capacidad o reemplazar instancias sin interrumpir el servicio. Después de entenderlos, puedo planificar arquitecturas que escalen horizontalmente, aplicar patrones de replicación y elegir estrategias de consistencia adecuadas. No necesito preocuparme cuando el servicio es monolítico, de bajo tráfico y no requiere alta disponibilidad.

## Esqueleto (el 20% esencial)
1. **Load balancing** – distribuye las peticiones entrantes entre varias instancias para evitar cuellos de botella.  
2. **Scaling** – añade o quita nodos (horizontal) para ajustar la capacidad al nivel de demanda.  
3. **Replication** – copia datos o estado en varios nodos para mejorar disponibilidad y latencia de lectura.  
4. **Consistency** – define cómo se sincronizan esas copias y qué garantías de lectura/escritura se ofrecen.  

## Como funciona
1. El cliente envía una solicitud al punto de entrada (por ejemplo, un DNS o un reverse proxy).  
2. El balanceador de carga selecciona una instancia saludable según la política configurada (round‑robin, least‑connections, etc.).  
3. La instancia procesa la lógica de negocio; si necesita datos, accede a un cluster replicado.  
4. El mecanismo de replicación asegura que la escritura se propague a los seguidores según el modelo de consistencia elegido (strong, eventual, etc.).  
5. Si la carga aumenta, el orquestador lanza nuevas réplicas y el balanceador actualiza su pool automáticamente.

## Detalles
- **Básico**: configuración de un reverse proxy (NGINX, HAProxy) como balanceador y despliegue de varias copias del mismo contenedor.  
- **Intermedio**: uso de orquestadores (Kubernetes) para auto‑escalar pods y definir políticas de replicación (StatefulSet, ReplicaSet).  
- **Avanzado**: implementación de protocolos de consenso (Raft, Paxos) para strong consistency, y de sharding + quorum reads/writes para escalar bases de datos distribuidas.

## Ejemplo minimo
```yaml
# docker‑compose.yml – 2 instancias detrás de un balanceador simple
version: "3.8"
services:
  api:
    image: my/backend:latest
    deploy:
      replicas: 2
  lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```
```nginx
# nginx.conf – round‑robin entre los contenedores api
events {}
http {
    upstream backend {
        server api:8080;
        server api:8080;
    }
    server {
        listen 80;
        location / { proxy_pass http://backend; }
    }
}
```

## Errores comunes
- **Sobrecargar el balanceador**: usar una única instancia sin alta disponibilidad; evitarlo desplegando al menos dos balanceadores en modo activo‑pasivo.  
- **Ignorar la latencia de replicación**: asumir que los datos están instantáneamente consistentes; elegir el nivel de consistencia acorde al caso de uso.  
- **Escalar sin monitorear**: añadir nodos sin métricas de uso; usar alertas de CPU/memoria y de latencia de respuesta.

## Estado actual
- **Fundamentos estables**: el patrón de separación entre cliente → balanceador → instancias y la replicación de datos con modelos de consistencia son pilares consolidados.  
- **Práctica moderna**: los orquestadores (Kubernetes) gestionan automáticamente el balanceo y el auto‑escalado; los sistemas de consenso como etcd o Consul proporcionan strong consistency para configuraciones críticas.

## Conexiones
- **Reliability** – la replicación y el balanceo aumentan la tolerancia a fallos, garantizando que el servicio siga operativo pese a caídas de nodos.  
- **Mensajería** – los sistemas distribuidos a menudo usan colas (Kafka, RabbitMQ) para desacoplar componentes y manejar picos de carga.  
- **CDN / Load Balancing** – los CDN actúan como balanceadores de nivel de red, reduciendo la latencia al servir contenido estático cercano al cliente.

## Ruta de estudio
1. **Prerequisitos**: redes TCP/IP, conceptos de HTTP, contenedores Docker.  
2. **Fundamentos**: configurar NGINX/HAProxy como balanceador; desplegar múltiples instancias de una API.  
3. **Orquestación**: aprender Kubernetes (Deployments, Services, HPA).  
4. **Consistencia**: estudiar CAP theorem, modelos de consistencia (strong vs eventual) y protocolos de consenso (Raft).  
5. **Especialización**: implementar sharding, usar bases de datos distribuidas (Cassandra, CockroachDB) y explorar service mesh (Istio) para control de tráfico avanzado.

## Preguntas de repaso
1. ¿Cómo ayuda el load balancing a evitar cuellos de botella en una API backend?  
2. ¿Qué diferencia hay entre escalar horizontalmente y verticalmente, y cuándo elegir cada uno?  
3. ¿En qué situaciones es preferible una consistencia eventual frente a una fuerte?  
4. ¿Qué papel juega un orquestador como Kubernetes en la replicación automática de servicios?  
5. ¿Cómo se relaciona la replicación de datos con la mejora de la reliability del sistema?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-25-sistemas-distribuidos written_at=2026-11-05T19:58:31.155668+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/27 - Reliability|Reliability]] · *Software Engineering*
- [[01 - Software Engineering/28 - Distributed Systems|Distributed Systems]] · *Software Engineering*
- [[03 - Backend/21 - Mensajería|Mensajería]]
- [[04 - Database & Data Analytics/25 - Advanced Data Architecture|Advanced Data Architecture]] · *Database / Data Analytics*
- [[05 - Networking & Internet/25 - CDN - Load Balancing|CDN / Load Balancing]] · *Networking / Internet*

---
← [[03 - Backend/24 - Deploy & Infraestructura|Deploy & Infraestructura]] · [[03 - Backend/00 - Índice Backend|Índice Backend]]
