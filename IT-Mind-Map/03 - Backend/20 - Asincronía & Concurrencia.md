---
title: "Asincronía & Concurrencia"
area: "Backend"
numero: 20
aliases: ["Asincronía & Concurrencia"]
tags: [concepto, it/backend]
---
# Asincronía & Concurrencia

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 20 de 25**

## Qué abarca
- Threads
- async
- queues
- workers

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la asincronía y la concurrencia para que mis servicios y APIs respondan rápidamente aun cuando deben atender múltiples peticiones, ejecutar operaciones de I/O o procesar trabajos en segundo plano. Resuelvo el problema de los cuellos de botella que aparecen cuando un hilo queda bloqueado esperando una base de datos, un servicio externo o una operación de disco, lo que degrada la latencia y la disponibilidad del sistema. En mi día a día como ingeniero backend senior, aplico estos mecanismos al diseñar controladores HTTP que delegan tareas a colas, a workers que procesan mensajes y a rutinas async que liberan el hilo de servidor. Después de comprenderlos, puedo escalar horizontalmente, mejorar la resiliencia y reducir costos de infraestructura. No necesito preocuparme cuando el servicio es trivial, de bajo tráfico y todas sus operaciones son computacionales y rápidas.

## Esqueleto (el 20% esencial)
1. **Threads** – unidades de ejecución del sistema operativo que permiten correr código en paralelo dentro del mismo proceso.  
2. **Async / await** – sintaxis que permite escribir código no bloqueante sobre operaciones de I/O sin crear hilos explícitos.  
3. **Queues** – estructuras de mensajería que desacoplan la recepción de una petición de su procesamiento intensivo.  
4. **Workers** – procesos o contenedores que consumen mensajes de una queue y ejecutan la lógica de negocio de forma concurrente.

## Como funciona
1. El servidor recibe una petición HTTP y, si la operación implica I/O (BD, API externa), la marca como *async* y libera el thread del request.  
2. La llamada async devuelve un *Future*; el runtime registra la operación y continúa atendiendo otras peticiones.  
3. Cuando la respuesta está lista, el runtime reanuda la coroutine y envía el resultado al cliente.  
4. Si la tarea es pesada (cálculo, generación de reportes), el handler publica un mensaje en una queue.  
5. Uno o varios workers leen de la queue, procesan el mensaje en paralelo (usando threads o procesos) y actualizan el estado del dominio.  
6. Opcionalmente, el worker publica un evento de finalización que puede ser consumido por otro servicio o notificar al cliente vía WebSocket.

## Detalles
- **Básico**: entender que un thread bloquea mientras espera I/O y que async evita ese bloqueo usando un *event loop*.  
- **Intermedio**: combinar async con colas; el handler solo encola y retorna rápidamente, mientras que los workers pueden ser thread‑pools o procesos aislados.  
- **Avanzado**: orquestar múltiples workers con balanceo de carga, aplicar back‑pressure en la queue, y usar patrones como *fan‑out* o *pipeline* para procesar flujos de datos de forma altamente concurrente.

## Ejemplo minimo
```python
# Python 3.11 – servidor FastAPI con endpoint async y worker en background
from fastapi import FastAPI, BackgroundTasks
import httpx

app = FastAPI()

async def fetch_user(user_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
        return r.json()

def heavy_job(data: dict):
    # Simula trabajo intensivo
    import time, hashlib
    time.sleep(2)
    return hashlib.sha256(str(data).encode()).hexdigest()

@app.get("/users/{uid}")
async def get_user(uid: int, background: BackgroundTasks):
    user = await fetch_user(uid)          # async I/O no bloquea el thread
    background.add_task(heavy_job, user) # delega a worker en background
    return {"status": "queued", "user": user["name"]}
```

## Errores comunes
- **Crear hilos para cada petición** → agota recursos; usar async o pools en su lugar.  
- **Bloquear dentro de una coroutine** (p.ej. `time.sleep`) → vuelve a bloquear el event loop; usar `await asyncio.sleep`.  
- **Olvidar manejar excepciones en workers** → fallas silenciosas; envolver la lógica en `try/except` y registrar errores.  
- **No limitar el tamaño de la queue** → consumo ilimitado de memoria; establecer una capacidad máxima y aplicar back‑pressure.

## Estado actual
- **Fundamentos estables**: los conceptos de threads, async/await y colas son parte del modelo de ejecución de la mayoría de los runtimes modernos (JVM, .NET, Node.js, Python).  
- **Práctica moderna**: se prefiere combinar async con sistemas de mensajería distribuida (RabbitMQ, Kafka) y workers containerizados (Docker, Kubernetes) para lograr escalabilidad horizontal y resiliencia frente a fallos.

## Conexiones
- **Concurrency**: la concurrencia describe la capacidad de ejecutar varias tareas al mismo tiempo; async y threads son dos técnicas para lograrla.  
- **Caching**: usar cachés (Redis, Memcached) reduce la necesidad de I/O y, por tanto, la carga sobre los mecanismos async.  
- **Observability**: trazas y métricas (OpenTelemetry, Prometheus) son esenciales para detectar cuellos de botella en pipelines async/worker.

## Ruta de estudio
1. **Prerequisitos**: programación en al menos un lenguaje backend, conceptos de HTTP y bases de datos.  
2. **Fundamentos**: estudiar threads (synchronization, locks) y el modelo de event loop de async/await.  
3. **Práctica**: implementar un endpoint async que consuma una API externa y use una queue (RabbitMQ) con workers en Docker.  
4. **Avanzado**: explorar patrones de back‑pressure, circuit breaker y despliegue de workers en Kubernetes con autoscaling.  
5. **Especialización**: profundizar en observability de sistemas concurrentes y en arquitecturas basadas en eventos.

## Preguntas de repaso
1. ¿Por qué un handler async libera el thread del servidor mientras espera I/O?  
2. ¿Qué ventaja tiene usar una queue frente a lanzar un thread nuevo por cada petición pesada?  
3. ¿Cómo evitar que una coroutine bloquee el event loop?  
4. ¿Cuál es la diferencia práctica entre threads y workers en un entorno containerizado?  
5. ¿Qué métricas observarías para detectar que una queue está saturada?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-20-asincronia-concurrencia written_at=2026-11-05T19:53:45.199363+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/11 - Concurrency|Concurrency]] · *Software Engineering*
- [[02 - Frontend/09 - Asincronía|Asincronía]] · *Frontend*
- [[06 - Operating Systems & Linux/04 - Threads|Threads]] · *Operating Systems / Linux*

---
← [[03 - Backend/19 - Caching|Caching]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/21 - Mensajería|Mensajería]] →
