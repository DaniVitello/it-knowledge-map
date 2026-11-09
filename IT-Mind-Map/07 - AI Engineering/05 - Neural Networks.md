---
title: "Neural Networks"
area: "AI Engineering"
numero: 5
aliases: ["Neural Networks"]
tags: [concepto, it/ai-engineering]
---
# Neural Networks

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 5 de 25**

## Qué abarca
- Layers
- activations
- backpropagation
- optimization

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo redes neuronales para transformar datos crudos en representaciones que permiten a los modelos de IA aprender patrones complejos y tomar decisiones automáticas. Resuelvo el problema de capturar relaciones no lineales en tareas como clasificación de imágenes, generación de texto o predicción de series temporales, y aparecen en cada componente de un producto de IA que requiere inferencia o entrenamiento. Después de entenderlas, puedo diseñar arquitecturas adecuadas, ajustar hiperparámetros y diagnosticar fallos de entrenamiento; cuando el problema es lineal o ya está resuelto por una solución pre‑entrenada, no necesito preocuparme por la arquitectura interna.

## Esqueleto (el 20% esencial)
1. **Capas (Layers)** – Conjunto de neuronas que procesan la entrada y generan una salida intermedia.  
2. **Funciones de activación (Activations)** – Introducen no linealidad para que la red pueda modelar relaciones complejas.  
3. **Propagación hacia atrás (Backpropagation)** – Algoritmo que calcula gradientes del error para actualizar pesos.  
4. **Optimización (Optimization)** – Método (p. ej., SGD, Adam) que usa los gradientes para minimizar la función de pérdida.  
5. **Arquitectura (estructura de capas)** – Organización de capas que define la capacidad y el tipo de problema que la red puede resolver.

## Como funciona
1. Se alimenta la entrada a la **capa** inicial.  
2. Cada capa aplica una **función de activación** a la combinación lineal de sus pesos y la señal recibida.  
3. La salida de una capa se convierte en la entrada de la siguiente, repitiendo el proceso hasta la capa de salida.  
4. Se calcula la **pérdida** comparando la salida con la etiqueta deseada.  
5. Con **backpropagation**, los gradientes de la pérdida se propagan inversamente a través de todas las capas.  
6. Un algoritmo de **optimización** actualiza los pesos usando esos gradientes; el ciclo se repite hasta converger.

## Detalles
- **Básico:** perceptrón simple (una capa, activación lineal o sigmoide).  
- **Intermedio:** redes profundas (varias capas ocultas) con activaciones ReLU y regularización (dropout, batch‑norm).  
- **Avanzado:** arquitecturas especializadas (CNN para visión, RNN/Transformer para secuencias) y técnicas de entrenamiento distribuido, ajuste de tasa de aprendizaje y optimizadores adaptativos.

## Ejemplo minimo
```python
import torch
import torch.nn as nn

# Red neuronal mínima: una capa oculta y salida
model = nn.Sequential(
    nn.Linear(4, 8),      # capa oculta
    nn.ReLU(),            # activación
    nn.Linear(8, 3)       # capa de salida
)

x = torch.randn(5, 4)    # batch de 5 ejemplos, 4 características
y = model(x)             # inferencia
print(y.shape)           # → torch.Size([5, 3])
```

## Errores comunes
- **Olvidar la activación** entre capas → la red se vuelve lineal; añádela siempre.  
- **Usar tasa de aprendizaje demasiado alta** → divergencia del entrenamiento; comienza con valores pequeños y ajústalos.  
- **No normalizar los datos** → gradientes inestables; aplica escalado o batch‑norm.  

## Estado actual
- **Fundamentos estables:** la teoría de capas, activaciones, backpropagation y optimizadores clásicos sigue siendo la base de cualquier arquitectura.  
- **Práctica moderna:** se prefieren arquitecturas basadas en Transformers para procesamiento de lenguaje y visión, y optimizadores como AdamW con programación de tasa de aprendizaje (cosine decay, warm‑up).  

## Conexiones
- **Embeddings** – Las capas iniciales de una red convierten tokens o píxeles en vectores densos que sirven como embeddings para modelos posteriores.  
- **Transformers** – Utilizan bloques de capas (self‑attention + feed‑forward) que son una extensión de la arquitectura de redes neuronales tradicional.  
- **Linear Algebra & Probability** – El cálculo de productos matriciales y la estimación de distribuciones bajolie la operación de capas y la propagación de gradientes.

## Ruta de estudio
1. **Prerequisitos:** álgebra lineal (matrices, vectores), cálculo de derivadas y conceptos básicos de probabilidad.  
2. **Fundamentos:** perceptrón, funciones de activación, algoritmo de backpropagation y optimizadores SGD/Adam.  
3. **Intermedio:** redes profundas, regularización, inicialización de pesos, entrenamiento con mini‑batches.  
4. **Avanzado:** arquitecturas especializadas (CNN, RNN, Transformer), entrenamiento distribuido y técnicas de ajuste fino (fine‑tuning).  

## Preguntas de repaso
1. ¿Por qué es necesaria una función de activación no lineal entre capas?  
2. ¿Cómo se calcula el gradiente de los pesos durante backpropagation?  
3. ¿Qué diferencia hay entre un optimizador SGD y Adam?  
4. ¿En qué situaciones elegirías una arquitectura Transformer sobre una red feed‑forward tradicional?  
5. ¿Cuál es el efecto de normalizar los datos de entrada antes de entrenar una red neuronal?

<!-- trazabilidad: run_id=run-20261106-230308-5b791a concept=07-ai-engineering-05-neural-networks written_at=2026-11-07T02:03:40.768234+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/01 - AI - ML Fundamentals|AI / ML Fundamentals]]
- [[07 - AI Engineering/03 - Linear Algebra & Probability|Linear Algebra & Probability]]
- [[07 - AI Engineering/04 - Machine Learning Fundamentals|Machine Learning Fundamentals]]
- [[07 - AI Engineering/06 - Transformers|Transformers]]
- [[07 - AI Engineering/07 - LLMs|LLMs]]
- [[07 - AI Engineering/08 - Tokenization|Tokenization]]
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]

---
← [[07 - AI Engineering/04 - Machine Learning Fundamentals|Machine Learning Fundamentals]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/06 - Transformers|Transformers]] →
