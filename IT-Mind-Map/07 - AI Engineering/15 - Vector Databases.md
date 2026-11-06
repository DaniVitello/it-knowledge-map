---
title: "Vector Databases"
area: "AI Engineering"
numero: 15
aliases: ["Vector Databases"]
tags: [concepto, it/ai-engineering]
---
# Vector Databases

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 15 de 25**

## Qué abarca
- Indexación
- similarity search
- retrieval

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo bases de datos vectoriales para almacenar y buscar embeddings de alta dimensión que representan textos, imágenes o cualquier dato que haya sido transformado por un modelo de IA. Resuelvo el problema de encontrar rápidamente los ítems más similares a una consulta, lo que es esencial en sistemas de recuperación aumentada (RAG), recomendación y búsqueda semántica. Aparecen en la arquitectura de productos de IA cuando necesito conectar un modelo generativo con información externa de forma eficiente. Después de entenderlas, puedo diseñar pipelines de recuperación, optimizar la latencia de búsqueda y combinar varios índices para mejorar la cobertura del contexto. No necesito preocuparme por ellas si mi aplicación solo produce respuestas sin requerir acceso a datos externos o si utilizo un motor de búsqueda tradicional basado en texto plano.

## Esqueleto (el 20% esencial)
1. **Indexación de embeddings** – los vectores se insertan en estructuras que permiten búsquedas rápidas.  
2. **Similarity search** – se calcula la distancia (p. ej., coseno) entre el query y los vectores indexados para obtener los más cercanos.  
3. **Retrieval** – los resultados se entregan al modelo de IA para enriquecer su generación o decisión.  
4. **Persistencia en NoSQL** – los metadatos y los vectores se guardan en un almacén compatible con consultas flexibles.  
5. **Escalado dinámico** – el índice se actualiza y reequilibra conforme crecen los datos.

## Como funciona
1. El modelo de IA genera un embedding a partir del input del usuario.  
2. Ese embedding se envía a la base de datos vectorial, que lo compara con los vectores indexados usando una métrica de similitud.  
3. La capa de indexación devuelve los *k* vectores más cercanos junto con sus metadatos.  
4. El componente de retrieval incorpora esos documentos al prompt del modelo (RAG) o los usa directamente en una decisión.  
5. Si se añaden nuevos datos, la base de datos actualiza su índice de forma incremental para mantener la eficiencia.

## Detalles
- **Básico:** crear un índice plano (brute‑force) y usar distancia coseno; suficiente para pocos miles de vectores.  
- **Intermedio:** emplear estructuras como HNSW o IVF para reducir la complejidad a *log N* y soportar millones de vectores.  
- **Avanzado:** combinar sharding y replicación para alta disponibilidad; usar métricas híbridas (texto + vector) y aplicar re‑ranking con modelos de IA.  

## Ejemplo minimo
```python
from sentence_transformers import SentenceTransformer
import chromadb  # cliente de una base de datos vectorial ligera

# 1. Generar embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
docs = ["¿Cómo entrenar un modelo?", "Guía de despliegue en Docker"]
embs = model.encode(docs)

# 2. Crear colección y añadir vectores
client = chromadb.Client()
collection = client.create_collection(name="knowledge")
collection.add(
    ids=["doc1", "doc2"],
    embeddings=embs.tolist(),
    documents=docs
)

# 3. Consulta
query = model.encode(["¿Cómo lanzar mi modelo?"])
results = collection.query(
    query_embeddings=query.tolist(),
    n_results=1
)
print(results['documents'][0])
```

## Errores comunes
- **Usar distancia euclídea con embeddings normalizados** – produce rankings erróneos; prefiera coseno o normalice antes.  
- **Sobrecargar el índice con inserciones masivas sin re‑indexar** – degrada la latencia; programe re‑indexado periódico.  
- **Ignorar la persistencia de metadatos** – dificulta la trazabilidad del documento recuperado; siempre almacene IDs y atributos relevantes.

## Estado actual
- **Fundamentos estables:** representación de datos mediante embeddings, métricas de similitud (coseno, dot‑product) y la necesidad de indexación para búsqueda eficiente.  
- **Práctica moderna:** uso de estructuras HNSW, IVF‑PQ y servicios gestionados (p. ej., Pinecone, Weaviate) que ofrecen escalado automático, replicación y APIs de RAG integradas.

## Conexiones
- **Embeddings** – los vectores que se indexan provienen de modelos de lenguaje o visión; la calidad del embedding determina la efectividad de la búsqueda.  
- **RAG (Retrieval‑Augmented Generation)** – la base de datos vectorial alimenta al modelo generativo con contexto relevante, mejorando precisión y factualidad.  
- **NoSQL** – muchas bases de datos vectoriales se construyen sobre almacenes NoSQL para combinar consultas estructuradas y búsqueda vectorial en una única capa.

## Ruta de estudio
1. **Prerequisitos:** Python, conceptos de embeddings y métricas de distancia; familiaridad con APIs REST.  
2. **Fundamentos:** crear un índice plano, medir similitud y evaluar precisión con conjuntos de prueba simples.  
3. **Intermedio:** aprender HNSW/IVF, experimentar con parámetros de *efecto* y *recall*.  
4. **Avanzado:** implementar sharding, replicación y pipelines RAG; explorar integraciones con plataformas de IA (LangChain, LlamaIndex).  

## Preguntas de repaso
1. ¿Qué papel juega la métrica de similitud en una base de datos vectorial?  
2. ¿Cómo se conecta una base de datos vectorial con un modelo generativo en un flujo RAG?  
3. ¿Cuál es la diferencia práctica entre un índice plano y uno basado en HNSW?  
4. ¿Por qué es importante almacenar metadatos junto a los vectores?  
5. ¿Qué consideraciones de escalado aparecen al pasar de miles a millones de vectores?

<!-- trazabilidad: run_id=run-20261106-180823-552b64 concept=07-ai-engineering-15-vector-databases written_at=2026-11-06T21:09:34.233314+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/13 - NoSQL|NoSQL]] · *Database / Data Analytics*
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]
- [[07 - AI Engineering/14 - RAG|RAG]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]

---
← [[07 - AI Engineering/14 - RAG|RAG]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/16 - Agents|Agents]] →
