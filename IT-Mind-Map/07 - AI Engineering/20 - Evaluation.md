---
title: "Evaluation"
area: "AI Engineering"
numero: 20
aliases: ["Evaluation"]
tags: [concepto, it/ai-engineering]
---
# Evaluation

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 20 de 25**

## Qué abarca
- Accuracy
- relevance
- groundedness
- task-specific evals

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la evaluación para medir si un modelo de IA cumple con los requisitos de precisión, relevancia y groundedness en el contexto del producto que estoy construyendo. Resuelvo el problema de saber si el modelo entrega respuestas correctas y útiles antes de lanzarlo a producción, lo que evita retrocesos costosos y problemas de confianza del usuario. Aparece en cada fase del ciclo de vida: durante el desarrollo de prompts, la integración de modelos y el monitoreo post‑despliegue. Después de entenderla, puedo diseñar pipelines de testing automatizados, comparar versiones de modelos y establecer umbrales de aceptación. No necesito preocuparme cuando el modelo solo se usa en pruebas internas sin impacto en usuarios finales ni decisiones críticas.

## Esqueleto (el 20% esencial)
1. **Accuracy** – mide la coincidencia entre la salida del modelo y la respuesta esperada.  
2. **Relevance** – evalúa si la respuesta es útil para la tarea del usuario.  
3. **Groundedness** – verifica que la información provenga de fuentes verificables o del contexto dado.  
4. **Task‑specific evals** – métricas diseñadas para el dominio concreto (p. ej., F1 para extracción de entidades).  

## Como funciona
1. Defino los criterios de éxito (accuracy, relevance, groundedness) según la tarea.  
2. Construyo un conjunto de datos de referencia con respuestas esperadas y fuentes de verdad.  
3. Ejecuto el modelo sobre ese conjunto y recojo sus salidas.  
4. Aplico métricas genéricas (exact match, BLEU) y métricas específicas del dominio.  
5. Analizo los resultados para decidir si el modelo pasa el umbral o necesita ajuste.  

## Detalles
- **Básico:** usar métricas de precisión y recall sobre un dataset estático.  
- **Intermedio:** añadir evaluación de relevance mediante puntuaciones de similitud semántica y validar groundedness con verificadores de hechos.  
- **Avanzado:** diseñar evaluaciones de ciclo completo que incluyan usuarios reales, pruebas A/B y monitoreo continuo de métricas en producción.  

## Ejemplo minimo
```python
from sklearn.metrics import accuracy_score

# respuestas esperadas
gold = ["Paris", "Tokyo", "Berlin"]
# salida del modelo
pred = ["Paris", "Osaka", "Berlin"]

acc = accuracy_score(gold, pred)
print(f"Accuracy: {acc:.2f}")
```

## Errores comunes
- **Confiar solo en accuracy:** ignora relevancia y groundedness; combinar métricas evita este sesgo.  
- **Usar datos de prueba que no reflejan el dominio real:** validar con datos representativos del entorno productivo.  

## Estado actual
- **Fundamentos estables:** precisión, recall y métricas de similitud siguen siendo la base para cualquier evaluación de modelo.  
- **Práctica moderna:** integración de evaluaciones de groundedness y relevance en pipelines CI/CD, y uso de observabilidad para detectar degradación de métricas en tiempo real.  

## Conexiones
- **AI Safety & Security:** la evaluación de groundedness ayuda a detectar respuestas no verificables que pueden generar riesgos de desinformación.  
- **Observability:** métricas de evaluación se exponen como indicadores que permiten monitorear la salud del modelo en producción.  
- **Prompt Engineering:** los resultados de la evaluación guían la iteración de prompts para mejorar relevance y accuracy.  

## Ruta de estudio
1. **Prerequisitos:** estadística básica, conceptos de clasificación y métricas (precision, recall).  
2. **Fundamentos:** práctica con datasets de referencia y cálculo de accuracy y F1.  
3. **Intermedio:** aprender técnicas de evaluación semántica (cosine similarity, embeddings) y herramientas de fact‑checking.  
4. **Avanzado:** implementar pipelines CI/CD con pruebas de evaluación, integrar observabilidad y diseñar pruebas de usuario.  

## Preguntas de repaso
1. ¿Cómo se diferencia accuracy de relevance en la evaluación de un modelo de IA?  
2. ¿Qué papel juega groundedness al validar respuestas generativas?  
3. ¿Por qué una métrica task‑specific es necesaria aunque exista accuracy?  
4. ¿Cómo se puede automatizar la evaluación de groundedness en un pipeline CI/CD?  
5. ¿Qué relación existe entre la evaluación y la observabilidad en sistemas de IA en producción?

<!-- trazabilidad: run_id=run-20261106-181618-229ba5 concept=07-ai-engineering-20-evaluation written_at=2026-11-06T21:17:23.756843+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]]
- [[07 - AI Engineering/22 - Observability|Observability]]

---
← [[07 - AI Engineering/19 - Memory|Memory]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]] →
