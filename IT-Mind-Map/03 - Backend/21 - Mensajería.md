---
title: "Mensajería"
area: "Backend"
numero: 21
aliases: ["Mensajería"]
tags: [concepto, it/backend]
---
# Mensajería

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 21 de 25**

## Qué abarca
- Queues
- events
- brokers
- pub/sub

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la mensajería para desacoplar componentes de un servicio backend y garantizar la entrega fiable de datos entre procesos o microservicios. Resuelvo problemas de escalabilidad, tolerancia a fallos y sincronización asíncrona que aparecen cuando una API necesita delegar trabajo a workers, notificar a otros sistemas o propagar cambios de estado sin bloquear la petición original. Aparece en la arquitectura de microservicios, en pipelines de procesamiento y en integraciones con sistemas externos. Después de entenderla puedo diseñar colas de trabajo, eventos de dominio y patrones pub/sub que mejoran la resiliencia y el rendimiento de mis APIs. No necesito preocuparme por mensajería cuando la lógica es estrictamente sincrónica, el volumen de tráfico es bajo y no hay requisitos de desacoplamiento o reintentos.

## Esqueleto (el 20% esencial)
1. **Colas (queues)** – almacenan mensajes en orden FIFO para que los consumidores los procesen cuando estén listos.  
2. **Eventos (events)** – representan hechos del dominio que se publican para que cualquier suscriptor reaccione.  
3. **Brokers** – intermediarios (RabbitMQ, Kafka, SQS) que gestionan la persistencia, el enrutamiento y la entrega de mensajes.  
4. **Pub/Sub** – patrón donde los productores publican a un tema y múltiples suscriptores reciben copias independientes.  

## Como funciona
1. El productor crea un mensaje (p. ej. “orden‑creada”) y lo envía al broker.  
2. El broker persiste el mensaje en una cola o lo asigna a un tópico según la configuración.  
3. Los consumidores (workers, microservicios) se suscriben a la cola o al tópico y reciben los mensajes en orden o según particiones.  
4. Cada consumidor procesa el mensaje y, si todo sale bien, envía un ACK; de lo contrario, el broker re‑entrega según la política de reintentos.  
5. Los eventos publicados pueden disparar flujos adicionales (actualizar cachés, enviar correos, iniciar downstream services) sin que el productor conozca a los receptores.

## Detalles
- **Básico**: crear una cola simple, producir y consumir mensajes con ACK manual.  
- **Intermedio**: usar tópicos para pub/sub, configurar dead‑letter queues y políticas de reintento.  
- **Avanzado**: particionar tópicos para paralelismo, aplicar idempotencia en consumidores, integrar con transacciones distribuidas y usar esquemas de serialización (Avro, Protobuf) para compatibilidad evolutiva.

## Ejemplo minimo
```python
# productor con pika (RabbitMQ)
import pika, json

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()
ch.queue_declare(queue='tareas')

msg = {'tipo': 'email', 'destino': 'user@example.com'}
ch.basic_publish(exchange='', routing_key='tareas', body=json.dumps(msg))
conn.close()
```

```python
# consumidor
import pika, json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Procesando {data['tipo']} a {data['destino']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()
ch.basic_consume(queue='tareas', on_message_callback=callback)
ch.start_consuming()
```

## Errores comunes
- **Olvidar ACK** → el mensaje se re‑entrega indefinidamente; usar `basic_ack` al final del procesamiento.  
- **Procesar sin idempotencia** → duplicados generan efectos secundarios; diseñar consumidores idempotentes.  
- **Usar una sola cola para diferentes tipos de trabajo** → dificulta el escalado; separar por prioridad o dominio.  
- **No configurar dead‑letter** → los mensajes fallidos se pierden; habilitar DLQ para inspección.

## Estado actual
- **Fundamentos estables**: colas FIFO, ACK/NACK, dead‑letter queues y patrones pub/sub están consolidados en la mayoría de los brokers.  
- **Práctica moderna**: uso de Kafka para eventos de alta velocidad, esquemas evolutivos con Avro/Protobuf, y arquitectura basada en eventos (event‑driven) para microservicios.

## Conexiones
- **Distributed Systems** – la mensajería es la columna vertebral que permite la comunicación fiable entre nodos dispersos.  
- **Sistemas distribuidos** – los conceptos de consenso y tolerancia a particiones se implementan mediante brokers que manejan replicación y particionado.  
- **Advanced Data Architecture** – los eventos publicados forman parte de pipelines de datos en tiempo real y alimentan almacenes de eventos (event stores).

## Ruta de estudio
1. **Prerequisitos**: conocimientos de HTTP/REST, fundamentos de redes (TCP) y programación concurrente.  
2. **Fundamentos**: tutorial oficial de RabbitMQ (colas, ACK, DLQ).  
3. **Patrones**: estudiar pub/sub, work queues y fan‑out en la documentación de Kafka.  
4. **Avanzado**: leer “Designing Event‑Driven Systems” y practicar con esquemas Avro en un clúster Kafka.  
5. **Especialización**: implementar sagas y outbox pattern en microservicios, integrar con sistemas de observabilidad (tracing, metrics).

## Preguntas de repaso
1. ¿En qué situaciones un backend debería preferir una cola frente a una llamada HTTP síncrona?  
2. ¿Cómo garantiza un broker la entrega al menos una vez y qué implicaciones tiene para el consumidor?  
3. ¿Cuál es la diferencia práctica entre un tópico pub/sub y una simple cola de trabajo?  
4. ¿Qué papel juega una dead‑letter queue y cuándo deberías configurarla?  
5. ¿Cómo puedes asegurar la idempotencia de un consumidor que procesa eventos de dominio?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-21-mensajeria written_at=2026-11-05T19:54:49.085900+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/28 - Distributed Systems|Distributed Systems]] · *Software Engineering*
- [[03 - Backend/25 - Sistemas distribuidos|Sistemas distribuidos]]
- [[04 - Database & Data Analytics/25 - Advanced Data Architecture|Advanced Data Architecture]] · *Database / Data Analytics*

---
← [[03 - Backend/20 - Asincronía & Concurrencia|Asincronía & Concurrencia]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/22 - Observabilidad|Observabilidad]] →
