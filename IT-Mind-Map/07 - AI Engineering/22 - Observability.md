---
title: "Observability"
area: "AI Engineering"
numero: 22
aliases: ["Observability"]
tags: [concepto, it/ai-engineering]
---
# Observability

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 22 de 25**

## Qué abarca
- Traces
- latency
- token usage
- failures
- monitoring

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la observabilidad para saber en tiempo real cómo se comporta mi pipeline de IA: desde la latencia de las llamadas a modelo, el consumo de tokens, hasta los fallos inesperados. Resuelvo el problema de no poder diagnosticar degradaciones de calidad o cuellos de botella que afectan la experiencia del usuario y la fiabilidad del producto. Aparece en cada fase del ciclo de vida del modelo, especialmente en la integración y el despliegue continuo. Después de entenderla, puedo diseñar alertas automáticas, optimizar costos y garantizar que los SLAs se cumplan. No necesito preocuparme cuando el sistema es estático, de bajo tráfico y no está sujeto a requisitos de disponibilidad o seguridad críticos.

## Esqueleto (el 20% esencial)
1. **Traces** – Capturan el flujo de una petición a través de los componentes del stack de IA.  
2. **Latency** – Mide el tiempo que tarda cada llamada al modelo y a los servicios auxiliares.  
3. **Token usage** – Registra cuántos tokens se consumen por petición, útil para control de costos.  
4. **Failures** – Detecta errores de inferencia, time‑outs y excepciones de infraestructura.  
5. **Monitoring** – Agrupa métricas y logs en dashboards y sistemas de alertas.

## Como funciona
1. Al recibir una solicitud, el middleware inserta un **trace id** y lo propaga a todos los micro‑servicios.  
2. Cada componente registra su **latencia** y **token usage** en un collector (por ejemplo, Prometheus).  
3. Si ocurre una excepción, se genera un evento de **failure** con contexto del trace.  
4. Los datos se envían a un sistema de **monitoring** que correlaciona métricas y permite crear alertas basadas en umbrales definidos.  
5. Los dashboards muestran la salud del pipeline y facilitan la investigación de incidentes.

## Detalles
- **Básico**: habilitar logs estructurados y generar un trace id único por petición.  
- **Intermedio**: instrumentar latencia y token usage con métricas de tipo counter/gauge; configurar alertas de alta latencia y consumo excesivo.  
- **Avanzado**: integrar tracing distribuido (OpenTelemetry), crear paneles de correlación entre métricas de modelo y métricas de infraestructura, y aplicar políticas de auto‑remediación.

## Ejemplo minimo
```python
import openai, time, uuid
from prometheus_client import Counter, Histogram, start_http_server

# Métricas
REQ_LATENCY = Histogram('llm_latency_seconds', 'Latency of LLM calls')
TOKENS_USED = Counter('llm_tokens_total', 'Total tokens consumed')
FAILURES = Counter('llm_failures_total', 'Number of failed LLM calls')

start_http_server(8000)   # exposa métricas en /metrics

def call_llm(prompt: str):
    trace_id = str(uuid.uuid4())
    start = time.time()
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            request_id=trace_id   # pseudo‑campo para trazas
        )
        TOKENS_USED.inc(resp['usage']['total_tokens'])
        return resp['choices'][0]['message']['content']
    except Exception:
        FAILURES.inc()
        raise
    finally:
        REQ_LATENCY.observe(time.time() - start)

print(call_llm("¿Cuál es la capital de Francia?"))
```

## Errores comunes
- **Olvidar propagar el trace id** → los logs no se pueden correlacionar; evitar pasando el id en cabeceras de cada llamada.  
- **Métricas sin etiquetas** → dificultan filtrar por modelo o versión; siempre etiquetar con `model`, `version`.  
- **Alertas demasiado sensibles** → generan ruido; calibrar umbrales con datos históricos.

## Estado actual
- **Fundamentos estables**: generación de logs estructurados, recolección de métricas de latencia y consumo de tokens, y alertas basadas en umbrales simples.  
- **Práctica moderna**: adopción de OpenTelemetry para tracing distribuido, dashboards unificados (Grafana + Loki), y políticas de auto‑escalado basadas en métricas de observabilidad.

## Conexiones
- **Logs & System Monitoring**: los logs estructurados alimentan los sistemas de monitoring que visualizan latencia y fallos.  
- **Evaluation**: los datos de token usage y latencia informan métricas de rendimiento usadas en la evaluación continua del modelo.  
- **AI Safety & Security**: la detección temprana de fallas y anomalías mediante observabilidad ayuda a prevenir comportamientos inseguros o sesgados.

## Ruta de estudio
1. **Prerequisitos**: conceptos de APIs REST, métricas Prometheus, y logging estructurado.  
2. **Fundamentos**: implementar tracing básico y métricas de latencia/token usage.  
3. **Intermedio**: configurar alertas y dashboards; integrar OpenTelemetry.  
4. **Avanzado**: diseñar pipelines de auto‑remediación y correlacionar observabilidad con métricas de evaluación y seguridad.  
5. **Especialización**: estudios de caso de observabilidad en LLMs a gran escala y patrones de resiliencia.

## Preguntas de repaso
1. ¿Qué información clave captura un trace y por qué es esencial en un pipeline de IA?  
2. ¿Cómo se relaciona la métrica de token usage con el control de costos del producto?  
3. ¿Qué pasos sigue el sistema cuando una llamada al modelo falla?  
4. ¿Cuál es la ventaja de usar OpenTelemetry frente a logs manuales?  
5. ¿Cómo puedes evitar que las alertas de alta latencia generen ruido en el equipo?

<!-- trazabilidad: run_id=run-20261106-181840-405d11 concept=07-ai-engineering-22-observability written_at=2026-11-06T21:19:48.566893+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/26 - Observability|Observability]] · *Software Engineering*
- [[03 - Backend/22 - Observabilidad|Observabilidad]] · *Backend*
- [[06 - Operating Systems & Linux/23 - Logs & System Monitoring|Logs & System Monitoring]] · *Operating Systems / Linux*
- [[07 - AI Engineering/20 - Evaluation|Evaluation]]
- [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]]

---
← [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]] →
