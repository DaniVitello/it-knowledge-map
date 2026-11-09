---
title: "Embeddings"
area: "AI Engineering"
numero: 9
aliases: ["Embeddings"]
tags: [concepto, it/ai-engineering]
---
# Embeddings

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 9 de 25**

## Qué abarca
- Representaciones vectoriales y semantic similarity

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo embeddings para convertir texto, imágenes o cualquier dato estructurado en vectores numéricos de dimensión fija que capturan su significado semántico. Resuelvo el problema de comparar y buscar similitud entre piezas de información sin depender de coincidencias exactas de palabras. En mi día a día como AI engineer senior, los embeddings aparecen al diseñar sistemas de recuperación aumentada (RAG), motores de recomendación o al indexar documentos en una vector database. Después de entenderlos, puedo crear pipelines de búsqueda semántica, mejorar la contextualización de prompts y evaluar la coherencia de respuestas generadas. Cuando el producto solo necesita reglas estáticas o coincidencias exactas, no es necesario preocuparse por embeddings.

## Esqueleto (el 20% esencial)
1. **Representación vectorial** – Cada elemento de entrada se mapea a un vector denso que preserva relaciones semánticas.  
2. **Similaridad semántica** – La distancia (p. ej., coseno) entre vectores indica cuán similares son los conceptos subyacentes.  
3. **Generación mediante modelos** – Redes neuronales como Transformers entrenadas en tareas de lenguaje producen los embeddings.  
4. **Indexación y búsqueda** – Los vectores se almacenan en estructuras especializadas (vector databases) para consultas rápidas.  
5. **Uso en RAG** – Los embeddings alimentan la recuperación de contexto relevante antes de generar respuestas con LLMs.

## Como funciona
1. **Tokenización** del texto de entrada para obtener tokens compatibles con el modelo.  
2. **Paso por el modelo Transformer** que, en una capa intermedia, genera una representación densa para cada token.  
3. **Pooling** (p. ej., media o CLS) para obtener un único vector que resume todo el documento.  
4. **Normalización** opcional del vector para que la métrica de similitud sea consistente.  
5. **Almacenamiento** del vector en una vector database junto con metadatos.  
6. **Consulta**: se calcula el embedding de la pregunta, se busca el vector más cercano y se recupera el contenido asociado para alimentar al LLM.

## Detalles
- **Básico**: usar un modelo pre‑entrenado (e.g., `sentence‑transformers/all‑MiniLM-L6-v2`) para obtener embeddings de oraciones.  
- **Intermedio**: ajustar (fine‑tune) el modelo con datos propios para que los vectores reflejen dominio específico.  
- **Avanzado**: combinar múltiples capas de embeddings (texto + imágenes) y aplicar técnicas de reducción de dimensionalidad (PCA, UMAP) antes de indexar; usar índices HNSW o IVF para escalabilidad.

## Ejemplo minimo
```python
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
sentences = ["Inteligencia artificial", "Machine learning", "Cocina italiana"]
embs = model.encode(sentences, normalize_embeddings=True)

# Similaridad coseno entre la primera y la segunda frase
sim = util.cos_sim(embs[0], embs[1])
print(f"Similaridad: {sim.item():.3f}")
```

## Errores comunes
- **Usar embeddings sin normalizar** → la métrica de distancia puede estar sesgada; normaliza siempre.  
- **Comparar vectores de diferentes dimensiones** → asegura que todos provengan del mismo modelo.  
- **Ignorar el dominio** → embeddings genéricos pueden no capturar jerga técnica; considera fine‑tuning.  

## Estado actual
- **Fundamentos estables**: la idea de representar datos como vectores y medir similitud con coseno es ampliamente aceptada.  
- **Práctica moderna**: los modelos basados en Transformers (BERT, RoBERTa, CLIP) generan embeddings de alta calidad; las vector databases como Pinecone, Milvus o Weaviate son la infraestructura de referencia para consultas a gran escala.  

## Conexiones
- **NoSQL** – Las vector databases suelen ofrecer APIs compatibles con sistemas NoSQL para almacenar pares (vector, metadato).  
- **Transformers** – Los embeddings son la salida de capas intermedias de modelos Transformer entrenados en tareas de lenguaje.  
- **RAG (Retrieval‑Augmented Generation)** – Los embeddings alimentan la fase de recuperación que precede a la generación de texto por un LLM.

## Ruta de estudio
1. **Prerequisitos**: Python, conceptos básicos de redes neuronales y tokenización.  
2. **Fundamentos**: leer la documentación de `sentence‑transformers` y experimentar con embeddings de texto.  
3. **Indexación**: aprender a usar Milvus o Pinecone para almacenar y consultar vectores.  
4. **Fine‑tuning**: seguir tutoriales de ajuste de BERT para tareas de similitud de pares.  
5. **Integración RAG**: combinar la recuperación basada en embeddings con un LLM (e.g., OpenAI GPT) para construir un sistema de respuesta contextual.  

## Preguntas de repaso
1. ¿Qué propiedad de los embeddings permite comparar conceptos que no comparten palabras exactas?  
2. ¿Por qué es importante normalizar los vectores antes de calcular la similitud coseno?  
3. ¿Cómo afecta el tipo de pooling (media vs. CLS) al vector final de un documento?  
4. ¿Qué ventajas ofrece una vector database frente a una tabla SQL tradicional para búsquedas semánticas?  
5. ¿En qué situaciones un AI engineer debería evitar usar embeddings y optar por coincidencias exactas?

<!-- trazabilidad: run_id=run-20261109-163025-5aded4 concept=07-ai-engineering-09-embeddings written_at=2026-11-09T19:31:41.587145+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]] · *Database / Data Analytics*
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]
- [[07 - AI Engineering/06 - Transformers|Transformers]]
- [[07 - AI Engineering/07 - LLMs|LLMs]]
- [[07 - AI Engineering/08 - Tokenization|Tokenization]]
- [[07 - AI Engineering/14 - RAG|RAG]]
- [[07 - AI Engineering/15 - Vector Databases|Vector Databases]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]

---
← [[07 - AI Engineering/08 - Tokenization|Tokenization]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/10 - Prompt Engineering|Prompt Engineering]] →
