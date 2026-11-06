---
title: "AI Infrastructure"
area: "AI Engineering"
numero: 23
aliases: ["AI Infrastructure"]
tags: [concepto, it/ai-engineering]
---
# AI Infrastructure

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 23 de 25**

## Qué abarca
- GPUs
- inference servers
- queues
- caching
- scaling

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la AI Infrastructure para provisionar y orquestar los recursos que hacen posible que un modelo de IA responda a peticiones de producción de forma fiable y rentable. Resuelvo el problema de latencia alta, cuellos de botella de cómputo y falta de escalabilidad que aparecen cuando un modelo entrenado se lleva a un entorno de usuarios reales. Aparece en cada fase del ciclo de vida del producto: desde la validación de inferencia en GPUs locales hasta el despliegue de servidores de inferencia en la nube y la gestión de colas y cachés que equilibran la carga. Después de entenderla, puedo diseñar pipelines de despliegue automatizados, dimensionar recursos y aplicar patrones de alta disponibilidad. No necesito preocuparme cuando el modelo solo se usa en pruebas unitarias o en entornos de desarrollo sin requisitos de rendimiento.

## Esqueleto (el 20% esencial)
1. **GPUs y aceleradores** – hardware especializado que reduce la latencia de inferencia.  
2. **Inference servers** – procesos o servicios que exponen el modelo mediante APIs.  
3. **Colas y caching** – mecanismos para desacoplar la llegada de peticiones y reutilizar resultados.  
4. **Escalado automático** – reglas que añaden o quitan instancias según la carga.  
5. **Monitoreo y métricas** – observabilidad para detectar degradaciones y ajustar recursos.

## Como funciona
1. Selecciono la GPU adecuada y la instalo en un nodo o contenedor.  
2. Empaqueto el modelo y lo cargo en un inference server (por ejemplo, TensorRT‑Server).  
3. Configuro una cola (RabbitMQ, SQS) que recibe las peticiones y las entrega al servidor.  
4. Activo una capa de caché (Redis) para almacenar respuestas frecuentes.  
5. Defino políticas de escalado en el orquestador (Kubernetes HPA) que monitorizan métricas de latencia y uso de GPU.  
6. El sistema monitorea continuamente y ajusta recursos para mantener SLA.

## Detalles
- **Básico**: Uso de una única GPU y un servidor de inferencia local; pruebas de latencia con `curl`.  
- **Intermedio**: Introducción de colas para manejar ráfagas de tráfico y caché para reducir llamadas repetidas.  
- **Avanzado**: Despliegue en clúster Kubernetes, autoscaling basado en métricas personalizadas, y observabilidad con Prometheus + Grafana.  

## Ejemplo minimo
```python
# inference_server.py
import torch, torchvision.models as models, flask, json

app = flask.Flask(__name__)
model = models.resnet18(pretrained=True).eval().cuda()

@app.route("/predict", methods=["POST"])
def predict():
    data = json.loads(flask.request.data)
    tensor = torch.tensor(data["input"]).float().cuda()
    with torch.no_grad():
        out = model(tensor.unsqueeze(0))
    return {"logits": out.cpu().tolist()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```
Ejecutar: `python inference_server.py` y enviar una petición `curl -X POST -d '{"input":[...]}'
http://localhost:8080/predict'`.

## Errores comunes
- **Sobredimensionar GPUs**: genera costos innecesarios; usar profiling para dimensionar correctamente.  
- **Olvidar la caché**: aumenta latencia y carga; habilitar Redis o similar.  
- **No limitar la concurrencia del servidor**: provoca OOM; establecer `max_workers`.  
- **Desactivar métricas**: dificulta la detección de cuellos de botella; integrar Prometheus desde el inicio.

## Estado actual
**Fundamentos estables**: uso de GPUs para inferencia, servidores como TensorRT‑Server o TorchServe, y patrones de cola‑caché.  
**Práctica moderna**: despliegues en Kubernetes con autoscaling basado en GPU utilization, observabilidad unificada (Prometheus, Grafana) y uso de infra‑as‑code (Terraform) para reproducibilidad.

## Conexiones
- **CI/CD**: la infraestructura se provisiona y actualiza automáticamente mediante pipelines que despliegan imágenes de contenedores con el modelo.  
- **Containers**: los inference servers se empaquetan en Docker, facilitando portabilidad y escalado en clústeres.  
- **LLMs**: los modelos de lenguaje grande requieren infraestructuras con mayor memoria GPU y estrategias de sharding, ampliando los conceptos de colas y caching.

## Ruta de estudio
1. **Prerequisitos**: Linux básico, conceptos de Docker y redes, fundamentos de deep learning (tensors, GPU).  
2. **Fundamentos**: tutorial de TensorRT‑Server o TorchServe, ejercicios de profiling con `nvidia-smi`.  
3. **Intermedio**: implementar colas con RabbitMQ, caché con Redis, y crear métricas con Prometheus.  
4. **Avanzado**: orquestar con Kubernetes, configurar HPA basado en GPU, escribir Terraform para infra‑as‑code, y explorar sharding de LLMs.  

## Preguntas de repaso
1. ¿Qué papel juegan las GPUs dentro de la AI Infrastructure y cómo afectan la latencia?  
2. ¿Cómo ayuda una capa de caching a reducir la carga del inference server?  
3. Describe el flujo de una petición desde la cola hasta la respuesta al cliente.  
4. ¿Qué riesgos implica no monitorizar métricas de uso de GPU en producción?  
5. ¿De qué manera CI/CD interactúa con los contenedores que alojan los modelos de IA?

<!-- trazabilidad: run_id=run-20261106-182207-3cb0f8 concept=07-ai-engineering-23-ai-infrastructure written_at=2026-11-06T21:22:52.024847+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/25 - CI-CD|CI/CD]] · *Software Engineering*
- [[03 - Backend/24 - Deploy & Infraestructura|Deploy & Infraestructura]] · *Backend*
- [[06 - Operating Systems & Linux/24 - Containers|Containers]] · *Operating Systems / Linux*
- [[06 - Operating Systems & Linux/25 - Virtualization & Infrastructure|Virtualization & Infrastructure]] · *Operating Systems / Linux*
- [[07 - AI Engineering/07 - LLMs|LLMs]]
- [[07 - AI Engineering/24 - Fine-tuning & Adaptation|Fine-tuning & Adaptation]]

---
← [[07 - AI Engineering/22 - Observability|Observability]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/24 - Fine-tuning & Adaptation|Fine-tuning & Adaptation]] →
