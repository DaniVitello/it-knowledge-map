---
title: "AI System Architecture"
area: "AI Engineering"
numero: 25
aliases: ["AI System Architecture"]
tags: [concepto, it/ai-engineering]
---
# AI System Architecture

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 25 de 25**

## Qué abarca
- Diseño completo de sistemas AI en producción

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la AI System Architecture para diseñar y desplegar sistemas que combinan modelos de IA con lógica de negocio, interfaces de usuario y pipelines de datos. Resuelvo el problema de integrar componentes heterogéneos (modelos, APIs, bases de datos) de forma escalable, segura y mantenible, garantizando que el modelo siga funcionando bajo carga real. Aparece en cada proyecto donde paso de un prototipo de modelo a un producto en producción: definición de servicios, orquestación de inferencias y monitoreo de calidad. Después de entenderla, puedo planificar la infraestructura completa, elegir patrones de despliegue (microservicios, serverless) y anticipar cuellos de botella. No necesito preocuparme cuando el modelo solo se usa en experimentación local o en notebooks sin requerimientos de disponibilidad ni latencia.

## Esqueleto (el 20% esencial)
1. **Definición de componentes** – identificar modelo, API de inferencia, capa de datos y frontend.  
2. **Patrones de despliegue** – elegir entre microservicios, serverless o batch según SLA.  
3. **Orquestación y flujo** – conectar componentes mediante colas o orquestadores (Kafka, Airflow).  
4. **Monitoreo y retro‑alimentación** – instrumentar métricas de latencia, drift y errores.  
5. **Seguridad y gobernanza** – aplicar control de acceso, encriptación y registro de versiones.

## Como funciona
1. **Mapeo de requisitos**: se listan los casos de uso y se asignan a componentes (modelo → API, UI → frontend).  
2. **Selección de patrón**: según volumen y latencia, se decide si el modelo se sirve como microservicio Dockerizado o como función serverless.  
3. **Construcción del pipeline**: se crea un flujo de datos que alimenta al modelo (pre‑procesamiento → inferencia → post‑procesamiento) usando colas o DAGs.  
4. **Despliegue**: se provisiona la infraestructura (Kubernetes, Cloud Functions) y se publica la API.  
5. **Monitoreo continuo**: se recogen métricas y se disparan alertas; los resultados alimentan un ciclo de retraining.

## Detalles
- **Básico**: definir la API de inferencia (REST/GRPC) y empaquetar el modelo en un contenedor.  
- **Intermedio**: añadir una capa de orquestación (Kafka + Airflow) para procesar lotes y manejar reintentos.  
- **Avanzado**: implementar canary releases, auto‑escalado basado en métricas de latencia y drift detection con pipelines de CI/CD para modelos.

## Ejemplo minimo
```python
# fastapi_app.py
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("model.pkl")   # modelo entrenado

@app.post("/predict")
def predict(payload: dict):
    # pre‑procesamiento simple
    features = [payload["x1"], payload["x2"]]
    pred = model.predict([features])[0]
    return {"prediction": pred}
```
Ejecutar con `uvicorn fastapi_app:app --host 0.0.0.0 --port 8000`.

## Errores comunes
- **Sobredimensionar la infraestructura**: usar clústeres Kubernetes cuando una función serverless basta; evitarlo evaluando el tráfico esperado.  
- **Ignorar el versionado del modelo**: despliegues sin registrar la versión provocan inconsistencias; usar artefactos versionados (MLflow, DVC).  
- **No monitorear drift**: asumir que el modelo mantiene performance; integrar métricas de distribución de entrada.

## Estado actual
- **Fundamentos estables**: separación clara de componentes (modelo, API, datos), uso de contenedores Docker y patrones REST/GRPC.  
- **Práctica moderna**: adopción de serverless para inferencias de baja latencia, orquestación basada en eventos (Kafka, Pulsar) y pipelines de CI/CD que incluyen pruebas de regresión de modelo.

## Conexiones
- **Architecture**: AI System Architecture es una especialización de la arquitectura de software general, aplicando principios de modularidad y escalabilidad a componentes de IA.  
- **Arquitectura Frontend**: el frontend consume la API de inferencia definida en la arquitectura AI, por lo que su diseño (React, Flutter) depende de los contratos de la capa de servicio.  
- **Arquitectura de aplicaciones**: la AI System Architecture se integra dentro de la arquitectura de aplicaciones más amplia, coordinando servicios tradicionales y de IA bajo un mismo esquema de despliegue y monitoreo.

## Ruta de estudio
1. **Prerequisitos**: Python, Docker, conceptos básicos de APIs REST y fundamentos de ML (entrenamiento, evaluación).  
2. **Fundamentos**: crear una API de inferencia con FastAPI, empaquetar con Docker, desplegar en una VM.  
3. **Intermedio**: aprender Kubernetes (pods, services) y orquestadores de eventos (Kafka).  
4. **Avanzado**: profundizar en serverless (AWS Lambda, Cloud Run), CI/CD para modelos (GitHub Actions + MLflow) y técnicas de drift detection.  
5. **Especialización**: estudiar patrones de gobernanza (MLOps, DataOps) y seguridad en IA (encriptación de datos, control de acceso basado en roles).

## Preguntas de repaso
1. ¿Qué componentes clave forman una AI System Architecture y cuál es su función principal?  
2. ¿Cómo decides entre un microservicio Dockerizado y una función serverless para servir un modelo?  
3. ¿Qué papel juega la orquestación (por ejemplo, Kafka) en el flujo de inferencia?  
4. ¿Cuál es una práctica recomendada para evitar problemas de drift en producción?  
5. ¿Cómo se relaciona la AI System Architecture con la arquitectura frontend de una aplicación?

<!-- trazabilidad: run_id=run-20261106-230842-7e05a5 concept=07-ai-engineering-25-ai-system-architecture written_at=2026-11-07T02:09:44.650771+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/22 - Architecture|Architecture]] · *Software Engineering*
- [[02 - Frontend/25 - Arquitectura Frontend|Arquitectura Frontend]] · *Frontend*
- [[03 - Backend/10 - Arquitectura de aplicaciones|Arquitectura de aplicaciones]] · *Backend*

---
← [[07 - AI Engineering/24 - Fine-tuning & Adaptation|Fine-tuning & Adaptation]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]]
