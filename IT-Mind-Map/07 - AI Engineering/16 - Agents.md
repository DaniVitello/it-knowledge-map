---
title: "Agents"
area: "AI Engineering"
numero: 16
aliases: ["Agents"]
tags: [concepto, it/ai-engineering]
---
# Agents

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 16 de 25**

## Qué abarca
- Planning
- tools
- loops
- state
- autonomous workflows

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **agents** para orquestar decisiones autónomas dentro de un producto de IA, delegando tareas a herramientas externas y manteniendo contexto entre interacciones. Resuelvo el problema de coordinar múltiples pasos de razonamiento y ejecución sin intervención humana constante, lo que permite crear flujos de trabajo que se adaptan a datos cambiantes y a objetivos de negocio. Aparecen en sistemas de asistencia conversacional, pipelines de análisis de datos y plataformas de automatización donde se necesita que el modelo planifique, invoque herramientas y recuerde información relevante. Después de entenderlos, puedo diseñar arquitecturas que integren planificación, bucles de retroalimentación y memoria, y decidir cuándo delegar a un agente o cuándo una llamada directa al modelo es suficiente. No necesito preocuparme por agents cuando la tarea es una única inferencia sin dependencias externas.

## Esqueleto (el 20% esencial)
1. **Planning** – el agente genera un plan de alto nivel antes de ejecutar cualquier acción.  
2. **Tools** – el agente selecciona y llama a herramientas (APIs, funciones) para cumplir cada paso del plan.  
3. **Loops** – se repite el ciclo *observe‑plan‑act* hasta alcanzar el objetivo o un criterio de parada.  
4. **State** – el agente mantiene estado interno (variables, resultados parciales) entre iteraciones.  
5. **Autonomous workflows** – combina los elementos anteriores para crear flujos de trabajo que operan sin supervisión humana continua.

## Como funciona
1. **Entrada**: el usuario o sistema envía una solicitud al agente.  
2. **Observación**: el agente analiza la solicitud y su estado actual.  
3. **Planificación**: genera un plan estructurado (lista de acciones) usando el modelo de lenguaje.  
4. **Selección de herramienta**: para cada acción, decide qué herramienta es necesaria y construye la llamada.  
5. **Ejecución**: invoca la herramienta, recibe la respuesta y actualiza su estado.  
6. **Retroalimentación**: evalúa si el objetivo está alcanzado; si no, vuelve al paso 3 (loop).  
7. **Salida**: devuelve al usuario el resultado final o el estado actualizado.

## Detalles
- **Básico**: agentes que solo planifican una única acción y llaman a una herramienta (p. ej., buscar información).  
- **Intermedio**: bucles simples donde el agente repite planificación y ejecución hasta cumplir una condición de parada (p. ej., rellenar un formulario paso a paso).  
- **Avanzado**: agentes con memoria persistente, capacidad de razonamiento condicional y manejo de errores, integrando varios tipos de herramientas y adaptando el plan en tiempo real (p. ej., asistente de soporte que combina búsqueda de documentación, ejecución de scripts y actualización de tickets).  

## Ejemplo minimo
```python
from openai import OpenAI
client = OpenAI()

def simple_agent(query):
    # 1. Prompt que incluye planificación y llamada a herramienta
    prompt = f"""You are an autonomous agent.
Plan the steps to answer the user and call the tool when needed.

User query: {query}
Tool: get_current_weather(city) -> returns temperature.

Provide the final answer."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content

print(simple_agent("¿Cuál es la temperatura actual en Buenos Aires?"))
```
Este fragmento muestra un agente que planifica una única llamada a la herramienta `get_current_weather` y devuelve la respuesta al usuario.

## Errores comunes
- **Olvidar actualizar el estado** → el agente pierde contexto; evitar guardando resultados en una estructura explícita después de cada llamada.  
- **Planificar sin validar la disponibilidad de la herramienta** → genera errores de ejecución; comprobar primero la lista de herramientas soportadas.  
- **Crear bucles sin criterio de parada** → riesgo de loops infinitos; definir siempre una condición de terminación clara.  

## Estado actual
- **Fundamentos estables**: la arquitectura *plan‑execute‑observe* y el uso de *tool calling* están consolidados en frameworks como LangChain y LlamaIndex.  
- **Práctica moderna**: se están explorando agentes con memoria a largo plazo (vector stores) y bucles de retroalimentación adaptativa que ajustan el plan en función de métricas de confianza y coste.

## Conexiones
- **Tool Calling**: los agents delegan acciones concretas a herramientas externas mediante llamadas estructuradas, lo que extiende sus capacidades más allá del modelo de lenguaje.  
- **AI Workflows**: un agente es un nodo inteligente dentro de un workflow mayor, capaz de decidir dinámicamente el siguiente paso del proceso.  
- **Memory**: la memoria permite que el agente recuerde información de interacciones previas, mejorando la coherencia y reduciendo la necesidad de repetir datos al usuario.

## Ruta de estudio
1. **Prerequisitos**: comprensión de prompts, APIs REST y conceptos básicos de programación orientada a eventos.  
2. **Fundamentos**: estudiar el patrón *plan‑execute‑observe* y practicar con ejemplos de tool calling.  
3. **Intermedio**: implementar bucles de retroalimentación y gestionar estado interno con estructuras de datos simples.  
4. **Avanzado**: integrar vectores de memoria, manejar errores de herramienta y optimizar criterios de parada; explorar frameworks de agentes (LangChain, CrewAI).  

## Preguntas de repaso
1. ¿Qué papel juega la planificación dentro de un agente y por qué es esencial?  
2. ¿Cómo se decide qué herramienta debe invocarse en cada paso del ciclo del agente?  
3. Describe un caso donde un bucle sin criterio de parada cause problemas operacionales.  
4. ¿En qué situaciones es preferible usar un agente en lugar de una simple llamada directa al modelo?  
5. ¿Cómo contribuye la memoria a la efectividad de un agente en flujos de trabajo autónomos?

<!-- trazabilidad: run_id=run-20261106-180934-910d21 concept=07-ai-engineering-16-agents written_at=2026-11-06T21:10:39.936207+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/13 - Tool Calling|Tool Calling]]
- [[07 - AI Engineering/17 - AI Workflows|AI Workflows]]
- [[07 - AI Engineering/19 - Memory|Memory]]

---
← [[07 - AI Engineering/15 - Vector Databases|Vector Databases]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/17 - AI Workflows|AI Workflows]] →
