---
title: "Context Engineering"
area: "AI Engineering"
numero: 18
aliases: ["Context Engineering"]
tags: [concepto, it/ai-engineering]
---
# Context Engineering

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 18 de 25**

## Qué abarca
- Qué información recibe el modelo y cuándo

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **Context Engineering** para decidir qué información le entrego al modelo de IA y en qué momento, de modo que el modelo pueda generar respuestas relevantes y coherentes sin sobrecargarlo con datos innecesarios. Resuelvo el problema de que los modelos, al recibir demasiado contexto o un contexto equivocado, pierden precisión o aumentan costos de inferencia. Aparece en cada fase donde el modelo interactúa con datos externos: al construir prompts, al recuperar documentos de una base vectorial o al mantener memoria de conversación. Después de entenderlo, puedo diseñar pipelines que entreguen justo el fragmento de contexto necesario, optimizando latencia y coste. No necesito preocuparme cuando el modelo opera en modo “zero‑shot” con preguntas totalmente autocontenidas.

## Esqueleto (el 20% esencial)
1. **Qué información recibe el modelo** – Seleccionar datos relevantes (documentos, historial, variables) antes de la inferencia.  
2. **Cuándo se entrega** – Inyectar el contexto en el momento exacto del prompt o mediante llamadas a herramientas.  
3. **Formato del contexto** – Representar la información de forma que el modelo la entienda (texto plano, JSON estructurado, embeddings).  
4. **Control de longitud** – Mantener el contexto dentro del límite de tokens para evitar truncamiento.  

## Como funciona
1. **Identificación del requerimiento**: el ingeniero define la tarea (p. ej., respuesta a preguntas sobre políticas).  
2. **Selección de fuentes**: se eligen documentos o estados de conversación pertinentes usando embeddings o búsquedas en una vector database.  
3. **Construcción del prompt**: el contexto seleccionado se inserta en el prompt siguiendo una plantilla que delimita claramente la información y la pregunta.  
4. **Invocación del modelo**: el LLM procesa el prompt con el contexto incluido y genera la salida.  
5. **Post‑procesado opcional**: se pueden extraer datos estructurados o actualizar la memoria del sistema para la siguiente interacción.  

## Detalles
- **Básico**: usar una plantilla simple `Context: {texto}` + `Question: {pregunta}`.  
- **Intermedio**: aplicar técnicas de *retrieval* (RAG) para obtener los fragmentos más similares mediante embeddings y limitar su longitud con heurísticas de recorte.  
- **Avanzado**: combinar *tool calling* para obtener datos en tiempo real, usar *structured outputs* (JSON) y gestionar *memory* a largo plazo mediante bases de datos de vectores que almacenan historial codificado.  

## Ejemplo minimo
```python
import openai

def ask_with_context(question, context):
    prompt = f"""Context:
{context}

Question: {question}
Answer:"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()

# Uso
doc = "La política de devoluciones permite reembolsos dentro de 30 días."
print(ask_with_context("¿Cuántos días tengo para devolver un producto?", doc))
```

## Errores comunes
- **Sobrecargar el prompt** con texto irrelevante → reduce precisión y aumenta coste. *Evitar*: filtrar antes de inyectar.  
- **Olvidar el límite de tokens** → respuestas truncadas. *Evitar*: medir la longitud y recortar inteligentemente.  
- **Formato inconsistente** entre contexto y pregunta → confusión del modelo. *Evitar*: usar plantillas claras y delimitadores.  

## Estado actual
- **Fundamentos estables**: la práctica de inyectar contexto mediante prompts estructurados es ampliamente adoptada y documentada.  
- **Práctica moderna**: la integración de *retrieval* (RAG) con embeddings y el uso de *tool calling* para obtener contexto dinámico están en expansión, impulsados por APIs de vectores y frameworks como LangChain.  

## Conexiones
- **Embeddings**: permiten buscar los fragmentos de texto más relevantes que forman el contexto entregado al modelo.  
- **Prompt Engineering**: define la plantilla que combina contexto y pregunta, garantizando que el modelo interprete correctamente la información.  
- **RAG (Retrieval‑Augmented Generation)**: utiliza una base de datos vectorial para extraer contexto en tiempo real, alimentando el proceso de Context Engineering.  

## Ruta de estudio
1. **Prerequisitos**: comprensión de prompts, límites de tokens y APIs de LLM.  
2. **Fundamentos**: practicar con plantillas simples y medir longitud de contexto.  
3. **Recuperación**: aprender a generar y consultar embeddings en una vector database.  
4. **Integración avanzada**: explorar tool calling y structured outputs para contextos dinámicos.  
5. **Optimización**: experimentar con técnicas de recorte y evaluación de coste/precisión.  

## Preguntas de repaso
1. ¿Cuál es la diferencia entre seleccionar información relevante y simplemente pasar todo el historial al modelo?  
2. ¿Cómo influye el límite de tokens en la estrategia de Context Engineering?  
3. ¿De qué manera los embeddings facilitan la selección del contexto?  
4. ¿Qué ventaja aporta combinar Context Engineering con tool calling en una aplicación de IA?  
5. Describe un caso donde usar RAG mejora la calidad de la respuesta frente a un prompt estático.

<!-- trazabilidad: run_id=run-20261106-181405-f43055 concept=07-ai-engineering-18-context-engineering written_at=2026-11-06T21:15:04.501407+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]
- [[07 - AI Engineering/10 - Prompt Engineering|Prompt Engineering]]
- [[07 - AI Engineering/11 - Structured Outputs|Structured Outputs]]
- [[07 - AI Engineering/13 - Tool Calling|Tool Calling]]
- [[07 - AI Engineering/14 - RAG|RAG]]
- [[07 - AI Engineering/15 - Vector Databases|Vector Databases]]
- [[07 - AI Engineering/19 - Memory|Memory]]

---
← [[07 - AI Engineering/17 - AI Workflows|AI Workflows]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/19 - Memory|Memory]] →
