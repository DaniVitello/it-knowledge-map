---
title: "RAG"
area: "AI Engineering"
numero: 14
aliases: ["RAG"]
tags: [concepto, it/ai-engineering]
---
# RAG

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 14 de 25**

## Qué abarca
- Retrieval-Augmented Generation

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Retrieval‑Augmented Generation (RAG) cuando necesito que un modelo de lenguaje produzca respuestas precisas y actualizadas sin entrenar el modelo con todo el conocimiento disponible. Resuelvo el problema de “alucinaciones” y de información desactualizada al combinar la generación de texto con una búsqueda en una base de datos de vectores que contiene documentos relevantes. En mi día a día como AI engineer senior, RAG aparece en sistemas de asistencia al cliente, buscadores internos y chatbots que deben citar fuentes. Después de entender RAG, puedo diseñar pipelines que integren embeddings, vector stores y prompts de contexto, y decidir cuándo delegar la recuperación a un motor externo en lugar de depender únicamente del modelo. No necesito preocuparme por RAG cuando el dominio es estático, pequeño o cuando la latencia de búsqueda supera los requisitos del producto.

## Esqueleto (el 20% esencial)
1. **Generación guiada por recuperación** – el modelo genera texto usando como contexto los documentos recuperados.  
2. **Embeddings** – transforman textos en vectores para que la búsqueda sea semántica.  
3. **Vector Database** – almacena los embeddings y permite consultas de similitud rápida.  
4. **Prompt / Context Engineering** – combina la información recuperada con instrucciones al modelo.  
5. **Ciclo de retro‑alimentación** – la calidad de la recuperación influye directamente en la calidad de la generación.

## Como funciona
1. **Indexado**: se crean embeddings de los documentos y se insertan en una vector database.  
2. **Consulta**: el usuario envía una pregunta; se genera su embedding.  
3. **Recuperación**: la base de vectores devuelve los *k* documentos más similares.  
4. **Construcción del prompt**: los documentos recuperados se concatenan con instrucciones (system prompt) que guían al LLM.  
5. **Generación**: el LLM produce la respuesta, ahora anclada a la información recuperada.  
6. **Post‑procesado** (opcional): se añaden referencias o se verifica la factualidad.

## Detalles
- **Básico**: usar una única capa de recuperación (top‑k) y un prompt simple.  
- **Intermedio**: aplicar re‑ranking con modelos cross‑encoders, ajustar *k* dinámicamente y usar técnicas de chunking para documentos extensos.  
- **Avanzado**: incorporar feedback del usuario para actualizar embeddings, emplear hybrid search (texto + vector) y orquestar múltiples LLMs especializados según el tipo de documento recuperado.

## Ejemplo minimo
```python
from sentence_transformers import SentenceTransformer
from chromadb import Client
from openai import OpenAI

# 1. Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
docs = ["La capital de Francia es París.", "Python es un lenguaje de programación."]
embs = model.encode(docs)

# 2. Vector store (Chromadb)
client = Client()
collection = client.create_collection(name="knowledge")
collection.add(ids=["d1","d2"], embeddings=embs.tolist(), documents=docs)

# 3. Consulta
query = "¿Cuál es la capital de Francia?"
q_emb = model.encode([query])[0]
results = collection.query(query_embeddings=[q_emb], n_results=1)

# 4. Prompt con contexto
context = results['documents'][0][0]
prompt = f"Contexto: {context}\nPregunta: {query}\nResponde citando el contexto."

# 5. Generación (OpenAI)
client = OpenAI()
answer = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt}]
)
print(answer.choices[0].message.content)
```

## Errores comunes
- **Usar embeddings genéricos** que no capturan la terminología del dominio → entrenar o fine‑tune un encoder especializado.  
- **Seleccionar *k* demasiado bajo** y perder información relevante → probar varios valores y validar la cobertura.  
- **Sobrecargar el prompt** con documentos completos → chunkear y resumir antes de incluirlos.  
- **Olvidar actualizar la base de vectores** cuando el corpus cambia → programar pipelines de re‑indexado periódico.

## Estado actual
- **Fundamentos estables**: la combinación de embeddings, búsqueda de similitud y generación de texto es ampliamente adoptada en productos de IA.  
- **Práctica moderna**: uso de modelos de embeddings de última generación (e.g., Mistral‑Embed), bases de datos híbridas (e.g., Pinecone, Qdrant) y técnicas de *retrieval‑augmented generation* con LLMs de gran escala (GPT‑4, Claude). La comunidad también explora RAG con *multimodal retrieval* (imágenes + texto) y *self‑query retrievers* que generan sus propias consultas.

## Conexiones
- **Embeddings**: convierten texto en vectores que la vector database puede comparar; la calidad del embedding determina la pertinencia de la recuperación.  
- **Vector Databases**: almacenan y sirven los embeddings; su arquitectura (ANN, disk‑based) impacta la latencia y escalabilidad del pipeline RAG.  
- **Context Engineering**: define cómo se inserta la información recuperada en el prompt; una buena ingeniería de contexto evita que el LLM ignore o contradiga los documentos.

## Ruta de estudio
1. **Prerequisitos**: Python, fundamentos de NLP, uso básico de APIs de LLM.  
2. **Embeddings**: estudiar SentenceTransformers, Mistral‑Embed y técnicas de fine‑tuning.  
3. **Vector Stores**: experimentar con Chroma, Pinecone o Qdrant; comprender índices ANN y métricas de distancia.  
4. **Prompt Design**: aprender patrones de *system* y *user* prompts, manejo de longitud y referencias.  
5. **RAG avanzado**: explorar re‑ranking, hybrid search y retro‑alimentación de usuario.  
6. **Implementación en producción**: CI/CD para pipelines de re‑indexado, monitorización de latencia y calidad de respuesta.

## Preguntas de repaso
1. ¿Qué papel juegan los embeddings dentro del ciclo RAG?  
2. ¿Cómo afecta la elección del parámetro *k* a la precisión y latencia de la respuesta?  
3. ¿Por qué es importante el *context engineering* al combinar documentos recuperados con un LLM?  
4. ¿Qué diferencia hay entre una búsqueda puramente textual y una búsqueda basada en vectores en RAG?  
5. ¿Cuál es una estrategia eficaz para mantener actualizada una vector database en un entorno productivo?

<!-- trazabilidad: run_id=run-20261106-180706-98b501 concept=07-ai-engineering-14-rag written_at=2026-11-06T21:08:22.991858+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]
- [[07 - AI Engineering/15 - Vector Databases|Vector Databases]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]

---
← [[07 - AI Engineering/13 - Tool Calling|Tool Calling]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/15 - Vector Databases|Vector Databases]] →
