---
title: "Transformers"
area: "AI Engineering"
numero: 6
aliases: ["Transformers"]
tags: [concepto, it/ai-engineering]
---
# Transformers

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 6 de 25**

## Qué abarca
- Attention
- tokens
- embeddings
- architecture

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Transformers para construir componentes de IA que procesen texto, código o cualquier secuencia de tokens de forma eficiente y con capacidad de generalizar. Resuelvo el problema de capturar dependencias a largo plazo sin recurrir a arquitecturas recurrentes, lo que permite que los modelos respondan rápidamente a consultas de usuarios y mantengan coherencia en diálogos extensos. En mi día a día como AI engineer senior, los Transformers aparecen en la fase de integración de modelos de lenguaje grande (LLM), en la generación de embeddings y en la adaptación de prompts a tareas específicas. Después de entender su arquitectura, puedo diseñar pipelines de inferencia, ajustar hiper‑parámetros y combinar varios modelos en un mismo producto. Cuando el problema es puramente tabular o de visión sin texto, no es necesario preocuparme por Transformers.

## Esqueleto (el 20% esencial)
1. **Self‑Attention** – permite que cada token pese la información de todos los demás tokens en la misma secuencia.  
2. **Tokens y Embeddings** – el texto se divide en tokens y cada token se proyecta a un vector denso que alimenta la atención.  
3. **Arquitectura en capas** – bloques repetidos de atención multi‑cabeza + feed‑forward forman la profundidad del modelo.  
4. **Positional Encoding** – agrega información de posición porque la atención es invariantes al orden.  

## Como funciona
1. **Tokenización**: el input se corta en tokens y se convierten en índices del vocabulario.  
2. **Embedding**: cada índice se transforma en un vector mediante una tabla de embeddings.  
3. **Positional Encoding**: al vector de embedding se suma un vector que indica su posición en la secuencia.  
4. **Self‑Attention**: en cada capa, los vectores generan *queries*, *keys* y *values*; el producto escalar entre queries y keys produce pesos que se aplican a los values.  
5. **Multi‑Head**: se repite el proceso en varios subespacios paralelos y sus resultados se concatenan.  
6. **Feed‑Forward**: la salida de la atención pasa por una red neuronal densa y se normaliza.  
7. **Stacking**: los pasos 4‑6 se repiten N veces; la salida final se proyecta a la tarea (clasificación, generación, etc.).  

## Detalles
- **Básico**: comprender que la atención sustituye a la recurrencia y que cada capa es idéntica en estructura.  
- **Intermedio**: ajustar el número de cabezas, la dimensión de los embeddings y la profundidad para equilibrar capacidad y coste computacional.  
- **Avanzado**: aplicar técnicas como *Layer Normalization* pre‑norm, *Dropout* en atención, *Sparse Attention* para secuencias largas y *Fine‑Tuning* con *LoRA* o *Adapter* para especializar modelos sin re‑entrenar todo el peso.  

## Ejemplo minimo
```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

sentence = "Los Transformers cambian la IA."
inputs = tokenizer(sentence, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# embeddings de la primera token [CLS]
cls_embedding = outputs.last_hidden_state[:, 0, :]
print(cls_embedding.shape)   # (1, 768)
```

## Errores comunes
- **Olvidar Positional Encoding**: la atención pierde orden; usar embeddings sin posición genera resultados incoherentes.  
- **Confundir tokens con palabras**: asumir que cada palabra es un token lleva a errores de longitud y OOV.  
- **Sobredimensionar el modelo**: usar una arquitectura demasiado grande para el dataset provoca overfitting y consumo innecesario.  

## Estado actual
- **Fundamentos estables**: la arquitectura de capas de self‑attention, embeddings y positional encoding se mantiene desde el artículo original y es la base de la mayoría de los modelos.  
- **Práctica moderna**: se emplean variantes como *Transformer‑XL* para dependencias más largas, *Sparse Transformers* para eficiencia, y técnicas de ajuste ligero (LoRA, Adapters) que permiten personalizar LLMs sin re‑entrenar todo el modelo.  

## Conexiones
- **Neural Networks**: los Transformers son una familia de redes neuronales que sustituyen la recurrencia por atención paralela.  
- **LLMs**: los grandes modelos de lenguaje (GPT, LLaMA) están construidos sobre arquitecturas Transformer, heredando sus mecanismos de atención y embeddings.  
- **Tokenization**: el proceso de dividir texto en tokens es el punto de entrada que permite a los Transformers trabajar con datos discretos.  

## Ruta de estudio
1. **Prerequisitos**: álgebra lineal, cálculo de gradientes y conceptos básicos de redes neuronales (feed‑forward, backpropagation).  
2. **Fundamentos**: estudiar el mecanismo de self‑attention y la arquitectura de capas; practicar con modelos pre‑entrenados en HuggingFace.  
3. **Especialización**: explorar variantes (Transformer‑XL, Sparse Attention) y técnicas de ajuste ligero (LoRA, Adapters).  
4. **Aplicación**: diseñar pipelines de inferencia, integrar prompts dinámicos y medir métricas de latencia y fiabilidad en producción.  

## Preguntas de repaso
1. ¿Qué papel juega el mecanismo de self‑attention dentro de un bloque Transformer?  
2. ¿Por qué es necesario añadir Positional Encoding a los embeddings?  
3. ¿Cómo afecta el número de cabezas de atención al comportamiento del modelo?  
4. ¿Cuál es la diferencia entre fine‑tuning completo y ajuste ligero (LoRA/Adapters) en un LLM?  
5. ¿En qué situaciones elegirías una arquitectura Sparse Transformer en lugar de la estándar?

<!-- trazabilidad: run_id=run-20261106-230342-d13f79 concept=07-ai-engineering-06-transformers written_at=2026-11-07T02:04:38.846802+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]
- [[07 - AI Engineering/07 - LLMs|LLMs]]
- [[07 - AI Engineering/08 - Tokenization|Tokenization]]
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]

---
← [[07 - AI Engineering/05 - Neural Networks|Neural Networks]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/07 - LLMs|LLMs]] →
