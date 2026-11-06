---
title: "Fine-tuning & Adaptation"
area: "AI Engineering"
numero: 24
aliases: ["Fine-tuning & Adaptation"]
tags: [concepto, it/ai-engineering]
---
# Fine-tuning & Adaptation

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 24 de 25**

## Qué abarca
- Fine-tuning
- LoRA
- distillation
- model adaptation

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el fine‑tuning y la adaptación de modelos para transformar un modelo preentrenado genérico en un componente que responde a los requisitos específicos de mi producto de IA, como dominio de negocio, restricciones de latencia o criterios de fiabilidad. Resuelvo el problema de que un modelo grande y costoso no entrega el rendimiento deseado en datos reales del cliente, y lo aplico cuando necesito mejorar precisión, reducir sesgo o adaptar el comportamiento sin entrenar desde cero. Después de comprender estas técnicas puedo diseñar pipelines de entrenamiento, seleccionar la estrategia (full‑parameter fine‑tuning, LoRA, distillation) y automatizar la puesta en producción. No me preocupo por fine‑tuning cuando el modelo ya cumple los SLAs o cuando el coste de adaptación supera el beneficio esperado.

## Esqueleto (el 20% esencial)
1. **Fine‑tuning completo** – ajuste de todos los pesos del modelo con datos del dominio.  
2. **LoRA (Low‑Rank Adaptation)** – agrega matrices de bajo rango que se entrenan mientras el modelo base permanece congelado.  
3. **Distillation** – transfiere conocimiento de un modelo grande (teacher) a uno más pequeño (student) para eficiencia.  
4. **Model adaptation** – combina técnicas (prompt tuning, adapters) para cambios rápidos sin re‑entrenar todo el modelo.

## Como funciona
1. Selecciono un modelo preentrenado (p. ej. `bert-base-uncased`).  
2. Preparo un dataset representativo del dominio y lo divido en train/val.  
3. Elijo la estrategia:  
   - *Full fine‑tuning*: habilito gradientes para todos los parámetros.  
   - *LoRA*: inserto capas LoRA en las capas de atención y entreno solo sus pesos.  
   - *Distillation*: entreno un modelo pequeño usando logits del teacher como objetivo.  
4. Configuro el optimizador, la tasa de aprendizaje y ejecuto el ciclo de entrenamiento, monitorizando métricas en el set de validación.  
5. Exporto el modelo adaptado y lo despliego en la infraestructura de inferencia.

## Detalles
- **Básico**: carga del modelo, tokenizador y dataset; entrenamiento con `Trainer`.  
- **Intermedio**: integración de LoRA mediante la librería `peft`; ajuste de hiper‑parámetros específicos de adaptación (rango bajo, alfa).  
- **Avanzado**: pipeline de distillation que combina pérdida de cross‑entropy y KL‑divergence; uso de técnicas de regularización (weight decay, early stopping) para evitar sobre‑ajuste; empaquetado con ONNX o TensorRT para inferencia optimizada.

## Ejemplo minimo
```python
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
train = load_dataset("imdb", split="train[:1%]")
val   = load_dataset("imdb", split="test[:1%]")

args = TrainingArguments(
    output_dir="./tmp",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    evaluation_strategy="epoch",
    learning_rate=5e-5,
)

trainer = Trainer(model=model, args=args, train_dataset=train, eval_dataset=val)
trainer.train()
```

## Errores comunes
- **Sobre‑ajuste** al entrenar con pocos datos; mitigarlo con early stopping o congelar capas superiores.  
- **Olvidar ajustar el tokenizador** al cambiar de modelo; mantener consistencia entre tokenizador y pesos.  
- **Usar tasas de aprendizaje demasiado altas** en LoRA, lo que desestabiliza la base; iniciar con valores 1‑2 órdenes de magnitud menores que en full fine‑tuning.

## Estado actual
- **Fundamentos estables**: el fine‑tuning completo sigue siendo la referencia para adaptar modelos a dominios con datos abundantes.  
- **Práctica moderna**: LoRA y otras técnicas de adaptación de bajo costo son la norma en entornos de producción donde la latencia y el coste de GPU son críticos. La distillation se emplea para crear versiones ligeras que cumplen requisitos de edge‑computing.

## Conexiones
- **LLMs** – los mismos principios de fine‑tuning y LoRA se aplican a grandes modelos de lenguaje para personalizar respuestas.  
- **AI Infrastructure** – la orquestación de pipelines de adaptación depende de plataformas de entrenamiento distribuido y de gestión de artefactos.  
- **MLOps** – la monitorización de métricas post‑despliegue y la automatización de re‑entrenamiento forman parte del ciclo de vida del modelo adaptado.

## Ruta de estudio
1. **Prerequisitos**: Python, PyTorch, conceptos de redes neuronales y transformers.  
2. **Fundamentos**: tutorial oficial de HuggingFace sobre fine‑tuning de clasificación de texto.  
3. **LoRA**: leer la publicación original de “LoRA: Low‑Rank Adaptation of Large Language Models” y practicar con la librería `peft`.  
4. **Distillation**: estudiar “DistilBERT” y experimentar con `torch.nn.KLDivLoss`.  
5. **MLOps**: integrar los pipelines en CI/CD usando MLflow o DVC para versionado y despliegue.

## Preguntas de repaso
1. ¿En qué situaciones prefiero LoRA a un fine‑tuning completo?  
2. ¿Cómo afecta la tasa de aprendizaje al entrenar adaptadores de bajo rango?  
3. ¿Qué ventaja aporta la distillation respecto a la simple reducción de parámetros?  
4. ¿Cuál es el rol del tokenizador al cambiar de modelo base?  
5. ¿Cómo se monitoriza la degradación de rendimiento de un modelo adaptado en producción?

<!-- trazabilidad: run_id=run-20261106-182252-4820ad concept=07-ai-engineering-24-fine-tuning-adaptation written_at=2026-11-06T21:23:55.476209+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/07 - LLMs|LLMs]]
- [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]]

---
← [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/25 - AI System Architecture|AI System Architecture]] →
