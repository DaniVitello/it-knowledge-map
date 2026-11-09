---
title: "Machine Learning Fundamentals"
area: "AI Engineering"
numero: 4
aliases: ["Machine Learning Fundamentals"]
tags: [concepto, it/ai-engineering]
---
# Machine Learning Fundamentals

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 4 de 25**

## Qué abarca
- Features
- labels
- training
- validation
- generalization

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los fundamentos de Machine Learning para transformar datos crudos en modelos que predigan o clasifiquen de forma fiable. Resuelvo el problema de cómo enseñar a una máquina a reconocer patrones sin programarlos explícitamente, lo que es esencial al diseñar pipelines de IA que integren modelos entrenados, validen su desempeño y garanticen su generalización. Aparecen en cada fase del desarrollo de un producto de IA: recolección de datos, construcción de features, entrenamiento, validación y despliegue. Después de comprender estos conceptos puedo diseñar experimentos controlados, seleccionar algoritmos adecuados y diagnosticar fallos de sobre‑ajuste. No necesito preocuparme cuando el modelo ya está entrenado y solo se consume como servicio.

## Esqueleto (el 20% esencial)
1. **Features** – Representaciones numéricas que capturan la información relevante del dominio.  
2. **Labels** – Valores objetivo que el modelo debe aprender a predecir.  
3. **Training** – Proceso de ajustar los parámetros del modelo usando un conjunto de pares feature‑label.  
4. **Validation** – Evaluación del modelo en datos no vistos para estimar su capacidad de generalizar.  
5. **Generalization** – Habilidad del modelo para mantener buen desempeño en datos reales fuera del conjunto de entrenamiento.

## Como funciona
1. **Recolección y etiquetado**: se obtienen datos y se asignan labels.  
2. **Ingeniería de features**: se transforman los datos crudos en vectores numéricos.  
3. **División del dataset**: se separa en *training set* y *validation set*.  
4. **Entrenamiento**: el algoritmo minimiza una función de pérdida sobre el training set, ajustando sus pesos.  
5. **Validación**: se calcula la métrica de desempeño (p. ej. accuracy, RMSE) sobre el validation set; si el desempeño difiere mucho del entrenamiento, se detecta sobre‑ajuste.  
6. **Iteración**: se ajustan features, hiperparámetros o el algoritmo hasta lograr una buena generalización.

## Detalles
- **Básico**: selección de features simples (escala, codificación one‑hot) y uso de algoritmos lineales (regresión logística, SVM).  
- **Intermedio**: normalización, manejo de desbalance de clases, validación cruzada y búsqueda de hiperparámetros (grid/random search).  
- **Avanzado**: pipelines de preprocesamiento, técnicas de regularización (L1/L2, dropout), ensembles y aprendizaje profundo que extienden los mismos principios de training/validation a redes neuronales.

## Ejemplo minimo
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Datos sintéticos (features) y etiquetas (labels)
X = np.array([[0, 1], [1, 1], [2, 0], [3, 1]])
y = np.array([0, 0, 1, 1])

# 2. División entrenamiento / validación
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.5, random_state=42)

# 3. Entrenamiento
model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Validación
pred = model.predict(X_val)
print("Accuracy:", accuracy_score(y_val, pred))
```

## Errores comunes
- **Usar features con alta colinealidad** → genera inestabilidad; aplicar reducción de dimensionalidad o regularización.  
- **Entrenar y validar con el mismo conjunto** → sobre‑ajuste invisible; siempre separar datos.  
- **Ignorar el escalado de features** → algoritmos sensibles a la magnitud fallan; normalizar antes de entrenar.  

## Estado actual
Los fundamentos (features, labels, training, validation, generalization) siguen siendo la base estable de cualquier proyecto de IA. En la práctica moderna se complementan con herramientas de automatización de pipelines (por ejemplo, *MLflow* o *Kubeflow*) y con técnicas de regularización y validación cruzada avanzadas que mejoran la robustez del modelo.

## Conexiones
- **Statistics**: provee la teoría de estimación y pruebas que sustentan la validación y la medición de generalización.  
- **Linear Algebra & Probability**: forman el lenguaje matemático para representar features y modelar incertidumbre en los algoritmos.  
- **Neural Networks**: extienden los principios de training y validation a arquitecturas profundas, manteniendo la necesidad de buenas features y datos etiquetados.

## Ruta de estudio
1. **Prerequisitos**: álgebra lineal básica, conceptos de probabilidad y estadística descriptiva.  
2. **Fundamentos**: aprender a crear y preprocesar features, entender etiquetas y dividir datos.  
3. **Algoritmos clásicos**: regresión lineal/logística, árboles de decisión, SVM.  
4. **Validación**: técnicas de hold‑out, k‑fold cross‑validation y métricas de desempeño.  
5. **Avanzado**: regularización, pipelines automatizados, integración con frameworks de deep learning.  

## Preguntas de repaso
1. ¿Qué papel juegan las features en la capacidad de generalización de un modelo?  
2. ¿Por qué es crítico separar training y validation sets antes de entrenar?  
3. ¿Cómo ayuda la regularización a mitigar el sobre‑ajuste?  
4. ¿Qué diferencia hay entre una métrica de precisión y una de recall en un problema de clasificación?  
5. ¿En qué situaciones podrías prescindir de una fase de ingeniería de features?

<!-- trazabilidad: run_id=run-20261106-230211-e9ef8f concept=07-ai-engineering-04-machine-learning-fundamentals written_at=2026-11-07T02:03:06.652172+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/21 - Statistics|Statistics]] · *Database / Data Analytics*
- [[07 - AI Engineering/01 - AI - ML Fundamentals|AI / ML Fundamentals]]
- [[07 - AI Engineering/03 - Linear Algebra & Probability|Linear Algebra & Probability]]
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]

---
← [[07 - AI Engineering/03 - Linear Algebra & Probability|Linear Algebra & Probability]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/05 - Neural Networks|Neural Networks]] →
