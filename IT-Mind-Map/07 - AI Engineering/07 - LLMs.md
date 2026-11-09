---
title: "LLMs"
area: "AI Engineering"
numero: 7
aliases: ["LLMs"]
tags: [concepto, it/ai-engineering]
---
# LLMs

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 7 de 25**

## Qué abarca
- Pretraining
- inference
- context windows
- capabilities

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo LLMs (Large Language Models) para dotar a mis productos de IA de capacidad de comprensión y generación de texto natural a gran escala. Resuelvo el problema de traducir consultas de usuarios, generar respuestas coherentes o sintetizar información sin escribir reglas específicas para cada caso. Aparecen en la capa de servicio de cualquier aplicación que requiera interacción en lenguaje, como chatbots, asistentes de código o sistemas de resumen automático. Después de entender cómo entrenan, inferencian y manejan contextos, puedo diseñar pipelines que integren prompts, ajustar el modelo a dominios concretos y monitorizar su fiabilidad. No necesito preocuparme por LLMs cuando la tarea es estrictamente numérica o cuando la latencia requerida es tan baja que un modelo pequeño o reglas heurísticas son más apropiados.

## Esqueleto (el 20% esencial)
1. **Pretraining** – el modelo aprende patrones de lenguaje a partir de enormes corpora sin supervisión directa.  
2. **Inference** – durante la ejecución, el modelo recibe tokens y devuelve probabilidades para el siguiente token.  
3. **Context windows** – el modelo solo “ve” una ventana limitada de tokens; su tamaño determina cuánta información previa puede usar.  
4. **Capabilities** – la combinación de arquitectura y datos determina tareas como completado, traducción o razonamiento.  

## Como funciona
1. Se selecciona un modelo pre‑entrenado (p. ej., GPT‑Neo).  
2. En inference, el prompt del usuario se tokeniza y se inserta en la **context window**.  
3. Cada paso de generación consulta la **Neural Network** (un Transformer) para obtener la distribución del siguiente token.  
4. El token con mayor probabilidad se decodifica y se agrega al contexto, repitiéndose hasta alcanzar la longitud deseada o un token de parada.  

## Detalles
- **Básico**: entender que el pretraining provee conocimientos generales y que la inference depende de la probabilidad de tokens.  
- **Intermedio**: gestionar la longitud de la **context window** para evitar truncamiento de información relevante; usar técnicas de *prompt engineering* para guiar las **capabilities**.  
- **Avanzado**: combinar varios LLMs, aplicar *retrieval‑augmented generation* (RAG) y ajustar (fine‑tune) el modelo con datos del dominio para mejorar precisión y reducir sesgos.  

## Ejemplo minimo
```python
from transformers import pipeline

# Carga un modelo pequeño y listo para inference
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

prompt = "¿Cuál es la diferencia entre IA supervisada y no supervisada?"
result = generator(prompt, max_new_tokens=50, do_sample=False)

print(result[0]["generated_text"])
```

## Errores comunes
- **Olvidar la longitud de la context window** → el modelo pierde información importante; evitar truncando prompts críticos.  
- **Usar temperatura alta sin control** → respuestas incoherentes; fijar `temperature` bajo para tareas determinísticas.  
- **No validar salida** → generar contenido no fiable; implementar filtros y métricas de calidad.  

## Estado actual
- **Fundamentos estables**: pretraining con grandes corpora, arquitectura Transformer y tokenización sub‑palabra siguen siendo la base.  
- **Práctica moderna**: uso de modelos de 6‑30 B parámetros en producción, integración con AI Infrastructure (servicios de inferencia escalables) y pipelines de fine‑tuning adaptados a dominios específicos.  

## Conexiones
- **Neural Networks**: los LLMs son una clase de redes neuronales profundas cuya arquitectura principal es el Transformer.  
- **Tokenization**: el proceso de dividir texto en sub‑palabras es esencial para que el modelo pueda mapear palabras a vectores de entrada.  
- **AI Infrastructure**: despliegue de LLMs requiere orquestación de GPUs/TPUs, balanceo de carga y monitorización de latencia.  

## Ruta de estudio
1. **Prerequisitos**: Python, fundamentos de Machine Learning, conceptos de redes neuronales y embeddings.  
2. **Fundamentos**: estudiar la arquitectura Transformer y la tokenización BPE.  
3. **Práctica**: experimentar con pipelines de HuggingFace, ajustar prompts y medir uso de la context window.  
4. **Especialización**: aprender técnicas de fine‑tuning, RAG y despliegue en plataformas de AI Infrastructure (Kubernetes, SageMaker, etc.).  

## Preguntas de repaso
1. ¿Qué papel juega el pretraining en la capacidad de un LLM para responder preguntas fuera de dominio?  
2. ¿Cómo afecta el tamaño de la context window al rendimiento de un modelo en una conversación larga?  
3. ¿Por qué la tokenización es un paso crítico antes de la inference?  
4. ¿Qué diferencia hay entre ajustar (fine‑tune) un LLM y simplemente diseñar un mejor prompt?  
5. ¿En qué situaciones preferirías usar un modelo pequeño en lugar de un LLM de varios miles de millones de parámetros?

<!-- trazabilidad: run_id=run-20261106-230440-6168aa concept=07-ai-engineering-07-llms written_at=2026-11-07T02:05:38.971144+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]
- [[07 - AI Engineering/06 - Transformers|Transformers]]
- [[07 - AI Engineering/08 - Tokenization|Tokenization]]
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]
- [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]]
- [[07 - AI Engineering/24 - Fine-tuning & Adaptation|Fine-tuning & Adaptation]]

---
← [[07 - AI Engineering/06 - Transformers|Transformers]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/08 - Tokenization|Tokenization]] →
