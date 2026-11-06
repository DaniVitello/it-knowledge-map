---
title: "LLM APIs & Model Serving"
area: "AI Engineering"
numero: 12
aliases: ["LLM APIs & Model Serving"]
tags: [concepto, it/ai-engineering]
---
# LLM APIs & Model Serving

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 12 de 25**

## Qué abarca
- APIs
- SDKs
- inference
- streaming

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo LLM APIs y Model Serving para conectar mis aplicaciones con modelos de lenguaje grande sin gestionar la infraestructura del modelo. Resuelvo el problema de obtener inferencia en tiempo real y a escala, evitando la sobrecarga de entrenamiento y mantenimiento de hardware. Aparecen cada vez que necesito que un producto de IA genere texto, clasifique, o realice razonamiento bajo demanda, ya sea en un chatbot, un motor de recomendación o una herramienta de análisis de documentos. Después de entender este concepto, puedo diseñar flujos de datos que llamen a modelos externos, orquestar despliegues propios de modelos y combinar ambas estrategias. No necesito preocuparme cuando el producto solo requiere lógica estática o cuando el modelo está embebido en el mismo proceso y no requiere exposición como servicio.

## Esqueleto (el 20% esencial)
1. **API** – Punto de entrada HTTP que expone operaciones de inferencia del modelo.  
2. **SDK** – Biblioteca cliente que simplifica la construcción de peticiones y el manejo de respuestas.  
3. **Inference** – Ejecución del modelo sobre un prompt y devolución del resultado.  
4. **Streaming** – Transferencia incremental de tokens para reducir latencia percibida.  

## Como funciona
1. El desarrollador importa el SDK y configura credenciales.  
2. Construye una solicitud que incluye el prompt, parámetros de generación y, opcionalmente, la opción de streaming.  
3. El SDK envía la petición a la API REST/GRPC del modelo.  
4. El servidor de Model Serving ejecuta la inferencia y devuelve la respuesta completa o un flujo de tokens.  
5. El cliente procesa la salida y la integra en la lógica del producto (respuesta al usuario, almacenamiento, etc.).

## Detalles
- **Básico**: Uso de una API REST con JSON; envío de `prompt` y recepción de `completion`.  
- **Intermedio**: Configuración de parámetros como `temperature`, `max_tokens` y uso de SDKs que gestionan reintentos y límites de cuota.  
- **Avanzado**: Activación de streaming (Server‑Sent Events o websockets) para obtener tokens a medida que se generan; despliegue propio de Model Serving con contenedores Docker, escalado automático y balanceo de carga; integración con sistemas de autenticación y registro de métricas.

## Ejemplo minimo
```python
import openai

client = openai.OpenAI(api_key="sk-*****")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "¿Cuál es la capital de Perú?"}],
    stream=False
)

print(response.choices[0].message.content)
```

## Errores comunes
- **Olvidar el parámetro `stream`** → la respuesta llega completa y la latencia percibida aumenta; habilitar `stream=True` cuando se necesita interacción en tiempo real.  
- **Exceder el límite de tokens** → la API devuelve error; ajustar `max_tokens` o dividir el prompt.  
- **No manejar reintentos** → fallas transitorias abortan el flujo; usar la lógica de reintento del SDK.

## Estado actual
- **Fundamentos estables**: APIs RESTful con JSON, autenticación mediante tokens, límites de cuota y modelo de precios basado en tokens.  
- **Práctica moderna**: SDKs asíncronos, streaming de tokens, despliegues de Model Serving en Kubernetes o serverless, observabilidad con métricas de latencia y uso de GPU.

## Conexiones
- **API Design** – Define la estructura de los endpoints, métodos y contratos que consumen los SDKs.  
- **Model Monitoring** – Supervisa la calidad y latencia de las inferencias servidas por la API.  
- **Data Pipeline** – Alimenta los prompts y consume las respuestas dentro de flujos ETL o de procesamiento en tiempo real.

## Ruta de estudio
1. **Prerequisitos**: HTTP/HTTPS, JSON, Python, conceptos básicos de inferencia de ML.  
2. **Fundamentos**: Consumir una LLM API con un SDK, entender parámetros de generación.  
3. **Intermedio**: Implementar streaming, gestionar cuotas y errores, medir latencia.  
4. **Avanzado**: Desplegar Model Serving propio (Docker, Kubernetes), escalar con autoscaling, integrar observabilidad y alertas.  
5. **Especialización**: Optimizar costos mediante batching, usar técnicas de prompt engineering y combinar APIs externas con modelos internos.

## Preguntas de repaso
1. ¿Qué ventaja aporta el streaming frente a una respuesta completa en una LLM API?  
2. ¿Cómo se configura el número máximo de tokens que puede generar un modelo?  
3. ¿Cuál es el rol del SDK al interactuar con una API de inferencia?  
4. ¿Qué pasos seguirías para migrar de una API externa a un despliegue propio de Model Serving?  
5. ¿Qué métricas son críticas para monitorear la salud de un servicio de inferencia?

<!-- trazabilidad: run_id=run-20261106-180455-c76fa5 concept=07-ai-engineering-12-llm-apis-model-serving written_at=2026-11-06T21:06:05.712656+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/09 - API Design|API Design]] · *Software Engineering*
- [[03 - Backend/07 - APIs|APIs]] · *Backend*

---
← [[07 - AI Engineering/11 - Structured Outputs|Structured Outputs]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/13 - Tool Calling|Tool Calling]] →
