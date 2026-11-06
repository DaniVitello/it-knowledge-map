---
title: "AI Workflows"
area: "AI Engineering"
numero: 17
aliases: ["AI Workflows"]
tags: [concepto, it/ai-engineering]
---
# AI Workflows

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 17 de 25**

## Qué abarca
- Pipelines
- orchestration
- routing
- parallelization

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo AI Workflows para encadenar de forma fiable los distintos componentes de un producto de IA—desde la ingestión y transformación de datos, pasando por la invocación de modelos y la post‑procesación, hasta la exposición de resultados al usuario. Resuelvo la complejidad de coordinar tareas que dependen de recursos externos, requieren paralelismo o deben reaccionar a eventos en tiempo real, evitando cuellos de botella y errores de sincronización. Aparecen en la arquitectura de cualquier sistema que combine modelos de lenguaje, visión o recomendación con pipelines de datos y lógica de negocio. Después de entenderlos, puedo diseñar sistemas escalables, depurar fallos de orquestación y añadir nuevas etapas sin romper el flujo existente. No necesito preocuparme cuando el producto es un prototipo monolítico que ejecuta una única inferencia aislada.

## Esqueleto (el 20% esencial)
1. **Pipelines** – Secuencias lineales de etapas que transforman datos y generan salidas intermedias.  
2. **Orchestration** – Motor que programa, monitoriza y recupera la ejecución de pipelines.  
3. **Routing** – Decisión dinámica que dirige la entrada a diferentes pipelines según contexto o tipo de solicitud.  
4. **Parallelization** – Ejecución simultánea de etapas independientes para reducir latencia.  

## Como funciona
1. El **router** inspecciona la solicitud y elige el pipeline adecuado.  
2. El **orchestrator** instancia el pipeline y lanza cada etapa en orden, aplicando **parallelization** cuando las etapas no comparten dependencias.  
3. Cada **pipeline** consume datos de la etapa previa, ejecuta transformaciones (p. ej. tokenización, extracción de características) y pasa el resultado a la siguiente.  
4. Al finalizar, el orchestrator recopila los resultados, maneja errores y devuelve la respuesta al cliente.

## Detalles
- **Básico**: Definir pipelines estáticos con herramientas como Apache Airflow o Prefect; cada tarea es una función Python.  
- **Intermedio**: Introducir routing mediante reglas de negocio (p. ej. modelo de clasificación que decide si usar un LLM o un modelo de visión).  
- **Avanzado**: Implementar parallelization a nivel de GPU/CPU con Ray o Dask, y usar orquestadores serverless (AWS Step Functions, Google Cloud Workflows) para escalar bajo demanda.

## Ejemplo minimo
```python
from prefect import flow, task

@task
def preprocess(text):
    return text.lower().strip()

@task
def infer(prompt):
    # llamada ficticia a un modelo LLM
    return f"Respuesta a: {prompt}"

@flow
def simple_workflow(raw):
    clean = preprocess(raw)
    return infer(clean)

print(simple_workflow("  Hola Mundo! "))
```

## Errores comunes
- **Olvidar manejo de errores**: el workflow se detiene sin recuperación; usar `try/except` o políticas de retry.  
- **Rutas estáticas en contextos dinámicos**: el router no adapta la lógica a nuevos tipos de entrada; mantener reglas actualizables.  
- **Sobrecargar la paralelización**: lanzar más tareas de las que la infraestructura soporta, provocando throttling; dimensionar recursos adecuadamente.

## Estado actual
Los fundamentos de pipelines y orquestación son estables y están soportados por frameworks como Airflow, Prefect y Luigi. En la práctica moderna, la tendencia es combinar estos conceptos con arquitecturas serverless y sistemas de paralelización distribuida (Ray, Dask) para lograr escalabilidad bajo demanda y latencias bajas.

## Conexiones
- **ETL / ELT**: los pipelines de AI Workflows reutilizan los mismos patrones de extracción‑transformación‑carga para preparar datos antes de la inferencia.  
- **Tool Calling**: el routing puede invocar herramientas externas (APIs, bases de datos) como pasos dentro del workflow.  
- **Agents**: los agentes autónomos pueden generar dinámicamente nuevos pipelines en respuesta a cambios del entorno o a resultados de inferencia.

## Ruta de estudio
1. **Prerequisitos**: Python, conceptos de APIs REST y fundamentos de procesamiento de datos.  
2. **Fundamentos**: aprender a crear pipelines con Prefect o Airflow; practicar manejo de errores y logging.  
3. **Orquestación avanzada**: estudiar Step Functions o Cloud Workflows, y técnicas de retry y timeout.  
4. **Paralelización**: dominar Ray o Dask para distribuir tareas; experimentar con GPU‑accelerated inference.  
5. **Integración**: combinar routing, tool calling y agentes para construir sistemas adaptativos.

## Preguntas de repaso
1. ¿Qué papel juega el router dentro de un AI Workflow y cómo afecta al diseño del pipeline?  
2. ¿Cómo se diferencia la orquestación de un simple script secuencial?  
3. ¿En qué situaciones es ventajoso aplicar parallelization y qué riesgos implica?  
4. ¿Cuál es la relación entre AI Workflows y los procesos ETL tradicionales?  
5. ¿Qué mecanismos de retry y manejo de errores son recomendables en un workflow productivo?

<!-- trazabilidad: run_id=run-20261106-181255-9428b3 concept=07-ai-engineering-17-ai-workflows written_at=2026-11-06T21:14:05.738344+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/16 - ETL - ELT|ETL / ELT]] · *Database / Data Analytics*
- [[04 - Database & Data Analytics/17 - Data Pipelines|Data Pipelines]] · *Database / Data Analytics*
- [[07 - AI Engineering/13 - Tool Calling|Tool Calling]]
- [[07 - AI Engineering/16 - Agents|Agents]]
- [[07 - AI Engineering/19 - Memory|Memory]]

---
← [[07 - AI Engineering/16 - Agents|Agents]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/18 - Context Engineering|Context Engineering]] →
