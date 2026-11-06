---
title: "Tool Calling"
area: "AI Engineering"
numero: 13
aliases: ["Tool Calling"]
tags: [concepto, it/ai-engineering]
---
# Tool Calling

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 13 de 25**

## Qué abarca
- Models que utilizan funciones
- APIs y herramientas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **Tool Calling** para que un modelo de lenguaje pueda invocar funciones, APIs o herramientas externas directamente desde la generación de texto. Resuelvo el problema de que el modelo solo produce palabras, mientras que el producto necesita ejecutar acciones concretas como consultar una base de datos, enviar un correo o generar un gráfico. Aparece en la arquitectura de cualquier sistema de IA que combine razonamiento natural con operaciones determinísticas, por ejemplo en asistentes virtuales o pipelines de análisis de datos. Después de entenderlo, puedo diseñar flujos donde el modelo decide cuándo y cómo llamar a recursos externos, lo que simplifica la integración y mejora la fiabilidad. No necesito preocuparme por Tool Calling cuando el producto solo requiere respuestas estáticas o cuando la lógica de negocio ya está codificada sin interacción dinámica con el modelo.

## Esqueleto (el 20% esencial)
1. **Definición de herramientas**: se describen funciones o APIs que el modelo puede invocar.  
2. **Prompt que expone la capacidad**: el prompt incluye instrucciones y ejemplos que enseñan al modelo a devolver una llamada estructurada.  
3. **Interpretación de la salida**: el runtime parsea la respuesta del modelo y ejecuta la herramienta correspondiente.  
4. **Ciclo de retroalimentación**: el resultado de la herramienta se vuelve a inyectar al modelo para continuar la conversación o el flujo.  

## Como funciona
1. El ingeniero registra una o más funciones (p. ej., `buscar_usuario(id)`).  
2. En el prompt se describe cada función con su nombre, parámetros y propósito.  
3. El modelo genera una respuesta que sigue el esquema estructurado (JSON) indicando la función a llamar y sus argumentos.  
4. El motor de ejecución parsea esa respuesta, invoca la función real y captura su salida.  
5. La salida se inserta en el contexto del modelo y se solicita la siguiente respuesta, completando el ciclo.

## Detalles
- **Básico**: registrar funciones simples y usar prompts con pocos ejemplos.  
- **Intermedio**: manejar tipos de datos complejos, validar argumentos y gestionar errores de llamada.  
- **Avanzado**: orquestar múltiples herramientas en un mismo turno, combinar con **Agents** que eligen la herramienta adecuada y mantener **Memory** para decisiones dependientes del historial.

## Ejemplo minimo
```python
import json

# 1. Definir la herramienta
def obtener_clima(ciudad: str) -> str:
    return f"El clima en {ciudad} es soleado."

# 2. Prompt con descripción de la herramienta
prompt = """
You can call the following function:
{
  "name": "obtener_clima",
  "description": "Devuelve el clima actual de una ciudad.",
  "parameters": {
    "type": "object",
    "properties": {
      "ciudad": {"type": "string", "description": "Nombre de la ciudad"}
    },
    "required": ["ciudad"]
  }
}
User: ¿Cuál es el clima en Madrid?
"""

# 3. Simular respuesta del modelo (en producción sería la API de LLM)
model_response = '{"name": "obtener_clima", "arguments": {"ciudad": "Madrid"}}'

# 4. Parsear y ejecutar
call = json.loads(model_response)
result = obtener_clima(**call["arguments"])
print(result)  # → El clima en Madrid es soleado.
```

## Errores comunes
- **Formato incorrecto**: devolver JSON mal formado; evitarlo validando con un parser antes de ejecutar.  
- **Argumentos faltantes**: omitir parámetros obligatorios; incluir validación de esquema en el runtime.  
- **Confusión de tipos**: pasar strings donde se esperan números; usar descripciones claras en el prompt.  

## Estado actual
- **Fundamentos estables**: la especificación de llamadas estructuradas (p. ej., JSON) y la práctica de describir funciones en el prompt son ampliamente adoptadas.  
- **Práctica moderna**: frameworks como LangChain y LlamaIndex proveen wrappers que automatizan el registro, el parsing y la gestión de errores, facilitando la integración de Tool Calling en **AI Workflows** complejos.

## Conexiones
- **Prompt Engineering**: el diseño del prompt determina si el modelo reconoce y utiliza correctamente las herramientas descritas.  
- **Agents**: los agentes deciden dinámicamente cuál herramienta llamar en función del objetivo y del estado del diálogo.  
- **Memory**: la memoria del modelo permite que decisiones de llamadas anteriores influyan en llamadas futuras, manteniendo coherencia en flujos largos.

## Ruta de estudio
1. **Prerequisitos**: familiaridad con JSON, APIs REST y conceptos básicos de LLMs.  
2. **Fundamentos**: leer la guía oficial de Tool Calling del proveedor de LLM que uses; practicar con ejemplos simples.  
3. **Integración**: experimentar con un framework (p. ej., LangChain) para registrar funciones y manejar respuestas.  
4. **Escalado**: combinar con Agents y Memory, diseñar flujos donde varias herramientas interactúan y se gestionan errores de red y tiempo de ejecución.  

## Preguntas de repaso
1. ¿Qué ventaja aporta Tool Calling frente a que el modelo solo genere texto?  
2. ¿Cómo se describe una herramienta en el prompt para que el modelo pueda llamarla?  
3. ¿Qué paso del ciclo garantiza que el resultado de la herramienta influya en la siguiente respuesta del modelo?  
4. ¿Cuál es un error típico al parsear la salida del modelo y cómo se previene?  
5. ¿De qué manera los Agents amplían la capacidad de Tool Calling en un sistema de IA?

<!-- trazabilidad: run_id=run-20261106-180605-60d0ea concept=07-ai-engineering-13-tool-calling written_at=2026-11-06T21:07:06.053816+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/10 - Prompt Engineering|Prompt Engineering]]
- [[07 - AI Engineering/11 - Structured Outputs|Structured Outputs]]
- [[07 - AI Engineering/16 - Agents|Agents]]
- [[07 - AI Engineering/17 - AI Workflows|AI Workflows]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]
- [[07 - AI Engineering/19 - Memory|Memory]]

---
← [[07 - AI Engineering/12 - LLM APIs & Model Serving|LLM APIs & Model Serving]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/14 - RAG|RAG]] →
