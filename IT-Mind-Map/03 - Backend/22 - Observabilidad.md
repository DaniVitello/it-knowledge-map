---
title: "Observabilidad"
area: "Backend"
numero: 22
aliases: ["Observabilidad"]
tags: [concepto, it/backend]
---
# Observabilidad

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 22 de 25**

## Qué abarca
- Logs
- metrics
- traces
- monitoring

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la observabilidad para saber, en tiempo real, qué está pasando dentro de mis servicios y APIs y para detectar rápidamente fallas o degradaciones de rendimiento. Resuelvo el problema de operar sistemas distribuidos sin “cajas negras”, obteniendo visibilidad suficiente para diagnosticar errores, medir SLAs y planificar mejoras. Aparece en mi día a día cuando despliego nuevos microservicios, cuando investigo incidentes o cuando optimizo la latencia de una cadena de llamadas. Después de entenderla, puedo diseñar pipelines de logs, métricas y trazas que alimenten dashboards y alertas, y decidir cuándo delegar la responsabilidad a un equipo de SRE. No necesito preocuparme de la observabilidad cuando trabajo con scripts aislados o pruebas unitarias que no involucran interacción externa.

## Esqueleto (el 20% esencial)
1. **Logs estructurados** – registros de eventos que describen acciones y errores en formato legible por máquinas.  
2. **Métricas** – valores numéricos (counters, gauges, histograms) que cuantifican comportamiento del sistema.  
3. **Trazas distribuidas** – seguimiento de una petición a través de múltiples servicios, mostrando latencias y puntos de fallo.  
4. **Monitoring** – proceso de recopilar, visualizar y alertar sobre logs, métricas y trazas.  
5. **Correlación** – unión de los tres pilares para obtener una visión completa del estado del backend.

## Como funciona
1. Cada servicio escribe **logs** estructurados en stdout o en un agente de recolección.  
2. Un exporter expone **métricas** (p. ej., Prometheus) que el servidor de monitoreo raspa periódicamente.  
3. Un tracer (OpenTelemetry) inserta IDs de correlación en los encabezados HTTP y genera **spans** que se envían a un backend de trazas.  
4. El sistema de **monitoring** agrupa logs, métricas y trazas en dashboards y define reglas de alerta.  
5. Cuando ocurre un incidente, el ingeniero busca la alerta, revisa la métrica afectada, inspecciona los logs y sigue la traza para localizar el origen.

## Detalles
- **Básico**: habilitar logs JSON y exportar contadores simples (requests_total, error_total).  
- **Intermedio**: añadir histogramas de latencia, etiquetas de contexto (service, endpoint) y configurar un collector de OpenTelemetry.  
- **Avanzado**: implementar sampling inteligente de trazas, crear alertas basadas en anomalías estadísticas y usar dashboards unificados (Grafana) que correlacionen los tres tipos de datos.

## Ejemplo minimo
```python
# app.py – FastAPI con logs, métricas y trazas mínimas
from fastapi import FastAPI, Request
import logging, time
from prometheus_client import Counter, Histogram, start_http_server
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("app")

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Latency per endpoint", ["endpoint"])

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor().instrument_app(app)

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    logger.info(f'{{"method":"{request.method}","path":"{request.url.path}","status":{response.status_code},"latency_ms":{latency*1000:.2f}}}')
    return response

@app.get("/ping")
def ping():
    return {"msg": "pong"}

if __name__ == "__main__":
    start_http_server(8000)   # expone métricas en /metrics
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

## Errores comunes
- **Logs sin estructura** – dificultan búsquedas; usar JSON o logfmt.  
- **Métricas sin etiquetas** – impiden filtrar por servicio o versión; etiquetar siempre.  
- **Trazas sin propagación de contexto** – pierden la cadena de llamadas; asegurar que los headers (`traceparent`) se reenvíen.  
- **Alertas demasiado ruidosas** – generan fatiga; calibrar umbrales y usar agregaciones.  
- **No versionar la configuración** – cambios inesperados; mantener la configuración en control de versiones.

## Estado actual
- **Fundamentos estables**: logs estructurados, métricas basadas en Prometheus, trazas con OpenTelemetry.  
- **Práctica moderna**: observabilidad como código (IaC), sampling adaptativo de trazas, alertas basadas en aprendizaje automático y dashboards unificados que correlacionan los tres pilares.

## Conexiones
- **Logs & System Monitoring** – los logs alimentan los sistemas de monitoreo para generar alertas y dashboards.  
- **Tracing & Distributed Systems** – las trazas revelan la topología de llamadas entre microservicios, esencial para depurar latencias.  
- **Metrics & Autoscaling** – las métricas de carga y latencia se usan como triggers para escalar automáticamente los pods o instancias.

## Ruta de estudio
1. **Prerequisitos**: manejo de Linux, conceptos de HTTP y REST, familiaridad con contenedores.  
2. **Fundamentos**: leer la guía oficial de OpenTelemetry, tutorial de Prometheus y práctica de logs JSON.  
3. **Intermedio**: implementar un collector (Grafana Agent) y crear alertas en Alertmanager.  
4. **Avanzado**: explorar sampling dinámico, integrar observabilidad como código con Terraform y aplicar detección de anomalías con herramientas como Prometheus Rule Engine o Grafana ML.

## Preguntas de repaso
1. ¿Qué información clave debe contener un log estructurado para ser útil en un incidente?  
2. ¿Cómo se diferencia un counter de un histogram en la definición de métricas?  
3. ¿Qué papel juega el encabezado `traceparent` en la propagación de trazas?  
4. ¿Por qué una alerta basada solo en logs suele generar más ruido que una basada en métricas?  
5. ¿Cuál es la ventaja de usar sampling adaptativo en trazas distribuidas?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-22-observabilidad written_at=2026-11-05T19:55:31.033911+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/26 - Observability|Observability]] · *Software Engineering*
- [[06 - Operating Systems & Linux/23 - Logs & System Monitoring|Logs & System Monitoring]] · *Operating Systems / Linux*
- [[07 - AI Engineering/22 - Observability|Observability]] · *AI Engineering*

---
← [[03 - Backend/21 - Mensajería|Mensajería]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/23 - Testing Backend|Testing Backend]] →
