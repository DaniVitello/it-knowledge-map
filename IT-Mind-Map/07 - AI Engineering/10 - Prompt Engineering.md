---
title: "Prompt Engineering"
area: "AI Engineering"
numero: 10
aliases: ["Prompt Engineering"]
tags: [concepto, it/ai-engineering]
---
# Prompt Engineering

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 10 de 25**

## Qué abarca
- Instructions
- context
- few-shot
- structured prompts

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Prompt Engineering para traducir la intención del usuario o del producto en instrucciones que un modelo de lenguaje pueda ejecutar de forma fiable. Resuelvo la ambigüedad y la variabilidad del input, garantizando que el modelo genere respuestas alineadas con los requisitos de la aplicación, como generación de texto, clasificación o extracción de datos. Aparece en cada fase del ciclo de vida de un producto de IA: diseño de la interacción, pruebas de calidad y despliegue continuo. Después de dominarlo, puedo diseñar flujos de conversación, crear plantillas reutilizables y combinar prompts con herramientas externas. No es necesario preocuparse por Prompt Engineering cuando el modelo se usa como un componente interno sin interacción directa con usuarios o cuando la salida es simplemente la probabilidad de una clase.

## Esqueleto (el 20% esencial)
1. **Instrucciones claras** – especifican la tarea y el formato esperado.  
2. **Contexto relevante** – provee información previa que el modelo necesita para responder adecuadamente.  
3. **Few‑shot examples** – demuestran el patrón deseado mediante ejemplos dentro del prompt.  
4. **Structured prompts** – usan marcadores o JSON para guiar la salida estructurada.  

## Como funciona
1. Defino la tarea y redacto una instrucción concisa.  
2. Inserto contexto (p. ej., historial de conversación o datos de dominio).  
3. Añado uno o dos ejemplos (few‑shot) que ilustran la respuesta ideal.  
4. Formateo el prompt con una plantilla estructurada que indique el tipo de salida (texto libre, lista, JSON).  
5. Envío el prompt al modelo; el modelo genera la respuesta siguiendo los patrones aprendidos.  

## Detalles
- **Básico:** Solo instrucción y contexto mínimo; útil para consultas simples.  
- **Intermedio:** Incorporación de few‑shot para enseñar el estilo de respuesta; mejora la consistencia.  
- **Avanzado:** Uso de structured prompts y técnicas de “chain‑of‑thought” para tareas complejas, combinando con tool calling o memory para mantener coherencia a lo largo de interacciones largas.  

## Ejemplo minimo
```python
import openai

prompt = """Instrucción: Resume el siguiente texto en una frase.
Texto: "Los modelos de lenguaje grande pueden generar texto coherente y útil en múltiples dominios."
Respuesta:"""

response = openai.Completion.create(
    model="gpt-4o-mini",
    prompt=prompt,
    max_tokens=30
)

print(response.choices[0].text.strip())
```

## Errores comunes
- **Prompt demasiado vago:** genera respuestas impredecibles; usar instrucciones específicas.  
- **Olvidar el contexto necesario:** el modelo carece de información clave; incluir datos relevantes.  
- **Ejemplos inconsistentes:** confunden al modelo; mantener estilo y formato uniformes.  

## Estado actual
Los fundamentos de Prompt Engineering (instrucciones, contexto, few‑shot y prompts estructurados) son estables y se aplican en la mayoría de los productos de IA. La práctica moderna incorpora técnicas de *chain‑of‑thought*, *tool calling* y gestión de *memory* para mejorar la fiabilidad en flujos de trabajo complejos.  

## Conexiones
- **Structured Outputs:** los prompts estructurados dictan el formato de la respuesta, facilitando la parsificación automática.  
- **Tool Calling:** un prompt bien diseñado puede invocar funciones externas, ampliando la capacidad del modelo más allá del texto.  
- **Memory:** al incluir historial relevante en el prompt, se mantiene la coherencia en conversaciones prolongadas.  

## Ruta de estudio
1. **Prerequisitos:** comprensión básica de modelos de lenguaje y API de OpenAI/Anthropic.  
2. **Fundamentos:** practicar con instrucciones simples y contexto directo.  
3. **Few‑shot:** crear plantillas con ejemplos y medir su impacto.  
4. **Prompts estructurados:** aprender a usar JSON o XML dentro del prompt.  
5. **Avanzado:** explorar chain‑of‑thought, tool calling y gestión de memory; integrar con pipelines de CI/CD para pruebas automatizadas.  

## Preguntas de repaso
1. ¿Qué elementos debe contener una instrucción para que sea eficaz en Prompt Engineering?  
2. ¿Cómo ayuda el few‑shot a mejorar la consistencia de la salida del modelo?  
3. ¿En qué situaciones es preferible usar un prompt estructurado en lugar de texto libre?  
4. ¿Cuál es la relación entre Prompt Engineering y Tool Calling?  
5. ¿Qué estrategia usarías para evitar que un modelo olvide información importante en una conversación larga?

<!-- trazabilidad: run_id=run-20261109-163143-fdd935 concept=07-ai-engineering-10-prompt-engineering written_at=2026-11-09T19:32:50.804264+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/11 - Structured Outputs|Structured Outputs]]
- [[07 - AI Engineering/13 - Tool Calling|Tool Calling]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]
- [[07 - AI Engineering/19 - Memory|Memory]]

---
← [[07 - AI Engineering/09 - Embeddings|Embeddings]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/11 - Structured Outputs|Structured Outputs]] →
