---
title: "Linear Algebra & Probability"
area: "AI Engineering"
numero: 3
aliases: ["Linear Algebra & Probability"]
tags: [concepto, it/ai-engineering]
---
# Linear Algebra & Probability

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 3 de 25**

## Qué abarca
- Vectores
- matrices
- distribuciones
- probabilidad

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo álgebra lineal y probabilidad para transformar datos crudos en representaciones numéricas que los modelos de IA pueden procesar y para cuantificar la incertidumbre de sus predicciones. Resuelvo problemas de escalado, combinación y evaluación de características en pipelines de entrenamiento y despliegue, y aparezco en cada capa donde se manipulan tensores, se calculan pérdidas o se interpreta la salida de un modelo. Después de dominar estos conceptos puedo diseñar embeddings, optimizar funciones de coste y validar la fiabilidad de un sistema mediante métricas probabilísticas. No necesito preocuparme cuando trabajo exclusivamente con APIs de alto nivel que abstraen los cálculos numéricos.

## Esqueleto (el 20% esencial)
1. **Vectores y matrices** – estructuras básicas para representar datos y parámetros de modelos.  
2. **Operaciones lineales** – producto punto, multiplicación de matrices y descomposición SVD, que habilitan transformaciones y optimizaciones.  
3. **Distribuciones de probabilidad** – describen la variabilidad de los datos y de las predicciones (p. ej., normal, Bernoulli).  
4. **Cálculo de probabilidades conjuntas y marginales** – permite combinar fuentes de información y estimar incertidumbre.  
5. **Gradientes y derivadas** – conectan álgebra lineal con probabilidad para entrenar modelos mediante descenso de gradiente.

## Como funciona
1. **Ingesta de datos** → se convierten en vectores o matrices (features × ejemplos).  
2. **Pre‑procesamiento** → se aplican transformaciones lineales (normalización, proyección).  
3. **Modelado** → los parámetros del modelo son matrices; la inferencia usa productos matriciales.  
4. **Cálculo de pérdida** → se modela como una función probabilística (p. ej., entropía cruzada).  
5. **Optimización** → se calculan gradientes (derivadas de funciones lineales) y se actualizan los pesos.  
6. **Evaluación** → se estima la probabilidad de clases o intervalos de confianza a partir de la distribución resultante.

## Detalles
- **Básico**: manejo de vectores, operaciones de suma y producto escalar; conceptos de media y varianza.  
- **Intermedio**: multiplicación de matrices, factorización QR, distribución normal multivariada, cálculo de log‑likelihood.  
- **Avanzado**: descomposición SVD para reducción de dimensionalidad, estimación de densidad kernel, back‑propagation con Jacobianos y Hessianos.

## Ejemplo minimo
```python
import numpy as np
from scipy.stats import norm

# 1. Vector de características
x = np.array([2.0, -1.0])

# 2. Peso (matriz 2x1) y sesgo
W = np.array([[0.5], [-0.3]])
b = 0.1

# 3. Operación lineal (logits)
logit = x @ W + b          # producto punto + sesgo

# 4. Probabilidad con distribución normal
prob = norm.cdf(logit)     # función de distribución acumulada
print(f"logit={logit.item():.3f}, prob={prob.item():.3f}")
```

## Errores comunes
- **Confundir dimensión de vectores** → validar shapes antes de multiplicar.  
- **Usar distribución incorrecta** → elegir la que refleje la naturaleza del dato (p. ej., binaria vs continua).  
- **Olvidar escalar datos** → puede provocar gradientes explosivos; normalizar siempre que sea posible.  

## Estado actual
- **Fundamentos estables**: la teoría de espacios vectoriales, la regla de la cadena y las distribuciones clásicas (normal, Bernoulli) son pilares consolidados.  
- **Práctica moderna**: bibliotecas como PyTorch y TensorFlow implementan operaciones lineales en GPU y ofrecen capas probabilísticas (e.g., `torch.distributions`) que integran directamente la estimación de incertidumbre en los modelos.

## Conexiones
- **AI / ML Fundamentals** – los conceptos de vectores y probabilidades son la base de cualquier algoritmo de aprendizaje automático.  
- **Machine Learning Fundamentals** – la optimización de funciones de coste combina álgebra lineal (gradientes) y probabilidad (likelihood).  
- **Neural Networks** – las capas lineales (fully‑connected) y las funciones de activación probabilísticas dependen directamente de estos conceptos.

## Ruta de estudio
1. **Prerequisitos**: cálculo diferencial, programación en Python, nociones básicas de estadística.  
2. **Fundamentos**: estudiar vectores, matrices y operaciones básicas con NumPy; repasar distribuciones discretas y continuas.  
3. **Intermedio**: practicar SVD y PCA; implementar log‑likelihood y entropía cruzada a mano.  
4. **Avanzado**: profundizar en back‑propagation con Jacobianos, explorar técnicas de inferencia bayesiana y modelos de mezcla.  
5. **Aplicación**: integrar capas lineales y distribuciones en un modelo PyTorch/TensorFlow y evaluar incertidumbre en producción.

## Preguntas de repaso
1. ¿Cómo convierto una tabla de datos en una matriz de características adecuada para un modelo de IA?  
2. ¿Qué operación lineal se usa para calcular los logits en una red neuronal densa?  
3. ¿Por qué la distribución normal es frecuente al modelar errores de predicción?  
4. ¿Cuál es la diferencia entre probabilidad marginal y conjunta en el contexto de un modelo de clasificación?  
5. ¿Cómo afecta la falta de normalización de los datos al cálculo de gradientes durante el entrenamiento?

<!-- trazabilidad: run_id=run-20261106-230106-b5f4be concept=07-ai-engineering-03-linear-algebra-probability written_at=2026-11-07T02:02:09.826042+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/01 - AI - ML Fundamentals|AI / ML Fundamentals]]
- [[07 - AI Engineering/04 - Machine Learning Fundamentals|Machine Learning Fundamentals]]
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]

---
← [[07 - AI Engineering/02 - Python & Programming|Python & Programming]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/04 - Machine Learning Fundamentals|Machine Learning Fundamentals]] →
