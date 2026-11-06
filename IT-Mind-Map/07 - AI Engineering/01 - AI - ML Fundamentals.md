---
title: "AI / ML Fundamentals"
area: "AI Engineering"
numero: 1
aliases: ["AI / ML Fundamentals"]
tags: [concepto, it/ai-engineering]
---
# AI / ML Fundamentals

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 1 de 25**

## Qué abarca
- Modelos
- entrenamiento
- inferencia
- datos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los fundamentos de AI/ML para transformar datos en modelos que resuelvan tareas específicas dentro de un producto de IA, como clasificación de imágenes o generación de texto. Resuelvo el problema de cómo pasar de datos crudos a predicciones fiables, lo que permite que el sistema tome decisiones automáticas o asista a usuarios. En mi día a día como AI engineer senior, estos conceptos aparecen en la fase de diseño del pipeline, en la selección de arquitectura y en la planificación de entrenamiento e inferencia. Después de comprenderlos, puedo diseñar, entrenar y desplegar modelos con criterios de calidad y coste. No necesito preocuparme cuando el producto ya usa un modelo pre‑entrenado con una API estable y la única tarea es su integración.

## Esqueleto (el 20% esencial)
1. **Datos** – La calidad y el formato de los datos determinan la capacidad del modelo para aprender.  
2. **Entrenamiento** – Proceso iterativo que ajusta los parámetros del modelo usando un algoritmo de optimización.  
3. **Modelo** – Representación matemática (red neuronal, árbol, etc.) que captura patrones del dominio.  
4. **Inferencia** – Uso del modelo entrenado para generar predicciones sobre datos nuevos.  

## Como funciona
1. **Recolección y curación de datos**: se extraen, limpian y etiquetan los ejemplos que alimentarán el entrenamiento.  
2. **Definición del modelo**: se elige una arquitectura adecuada (p. ej., transformer para texto) y se inicializan sus pesos.  
3. **Entrenamiento**: el algoritmo de optimización (SGD, Adam) procesa lotes de datos, calcula el loss y actualiza los pesos hasta que el loss converge o se alcanza el número de epochs deseado.  
4. **Validación**: se evalúa el modelo en un conjunto de datos no visto para detectar over‑fitting y ajustar hiperparámetros.  
5. **Despliegue e inferencia**: el modelo se serializa y se expone mediante una API; cada solicitud de inferencia pasa datos de entrada, el modelo genera la salida y se devuelve al cliente.

## Detalles
- **Básico**: entender la diferencia entre features y labels, y cómo dividir datos en train/validation/test.  
- **Intermedio**: aplicar técnicas de regularización (dropout, weight decay) y usar callbacks para early stopping.  
- **Avanzado**: gestionar entrenamiento distribuido, mezclar precisión (mixed‑precision) y aplicar fine‑tuning de modelos pre‑entrenados para reducir coste computacional.

## Ejemplo minimo
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)               # entrenamiento
pred = model.predict(X_test)               # inferencia
print("Accuracy:", accuracy_score(y_test, pred))
```

## Errores comunes
- **Datos desbalanceados** → usar técnicas de re‑muestreo o pesos de clase.  
- **Leakage entre train y test** → separar estrictamente los conjuntos antes de cualquier pre‑procesamiento.  
- **Sobre‑entrenamiento** → aplicar early stopping o regularización.  
- **Olvidar escalar features** → normalizar antes de entrenar modelos sensibles a la escala.

## Estado actual
- **Fundamentos estables**: la teoría del gradient descent, la división train/val/test y la necesidad de validación cruzada siguen siendo pilares.  
- **Práctica moderna**: uso de modelos pre‑entrenados (BERT, CLIP), entrenamiento distribuido con PyTorch Lightning o DeepSpeed, y despliegue mediante contenedores ligeros (Docker, ONNX Runtime) son tendencias predominantes.

## Conexiones
- **CI/CD** – Automatiza la re‑entrenamiento y el despliegue de modelos cada vez que llegan nuevos datos.  
- **Data Versioning (DVC)** – Rastrea cambios en los datasets y permite reproducir entrenamientos anteriores.  
- **Observability** – Monitorea métricas de inferencia (latencia, drift) para detectar degradación del modelo en producción.

## Ruta de estudio
1. **Prerequisitos**: Python, estadística básica, álgebra lineal y manejo de pandas/numpy.  
2. **Fundamentos**: cursos introductorios de ML (supervised learning, evaluación de modelos).  
3. **Especialización**: profundizar en deep learning (PyTorch/TensorFlow), técnicas de regularización y optimización avanzada.  
4. **Ingeniería de IA**: aprender sobre pipelines (MLflow, Kubeflow), despliegue (FastAPI, Docker) y monitorización (Prometheus, Grafana).  
5. **Avanzado**: entrenamiento distribuido, fine‑tuning de grandes modelos y gestión de datos a escala.

## Preguntas de repaso
1. ¿Por qué la calidad de los datos impacta directamente en la capacidad predictiva del modelo?  
2. ¿Qué papel juega la función de loss durante el entrenamiento?  
3. ¿Cómo detectas y mitigás el over‑fitting en un modelo de IA?  
4. ¿Cuál es la diferencia práctica entre entrenamiento y inferencia en un pipeline productivo?  
5. ¿De qué manera CI/CD puede mejorar la fiabilidad de los modelos desplegados?

<!-- trazabilidad: run_id=run-20261105-140443-ee37b4 concept=07-ai-engineering-01-ai-ml-fundamentals written_at=2026-11-05T17:06:08.174465+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/21 - Statistics|Statistics]] · *Database / Data Analytics*
- [[07 - AI Engineering/03 - Linear Algebra & Probability|Linear Algebra & Probability]]
- [[07 - AI Engineering/04 - Machine Learning Fundamentals|Machine Learning Fundamentals]]
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]

---
[[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/02 - Python & Programming|Python & Programming]] →
