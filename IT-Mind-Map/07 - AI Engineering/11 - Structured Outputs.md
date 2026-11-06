---
title: "Structured Outputs"
area: "AI Engineering"
numero: 11
aliases: ["Structured Outputs"]
tags: [concepto, it/ai-engineering]
---
# Structured Outputs

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 11 de 25**

## Qué abarca
- JSON schemas
- constrained generation
- typed outputs

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo **Structured Outputs** para obligar a un modelo de IA a devolver datos en un formato predefinido, como JSON que sigue un esquema concreto. Resuelvo el problema de respuestas impredecibles o mal formateadas que dificultan la integración automática en pipelines de producción. Aparecen cada vez que el producto necesita consumir la salida del modelo en componentes posteriores, por ejemplo en validación de datos, generación de tickets o actualización de bases de datos. Después de entender este concepto, puedo diseñar prompts que garanticen tipado seguro y reducir la lógica de parsing en el código de la aplicación. No necesito preocuparme cuando la salida se usa solo para visualización humana o cuando el modelo ya entrega el formato requerido sin ambigüedad.

## Esqueleto (el 20% esencial)
1. **JSON Schema**: define la estructura, tipos y restricciones que la salida debe cumplir.  
2. **Constrained Generation**: el modelo genera texto que respeta el esquema, evitando valores fuera de rango o campos faltantes.  
3. **Typed Outputs**: la salida se interpreta directamente como objetos tipados en el lenguaje de programación, eliminando parsing manual.  

## Como funciona
1. Se escribe un **JSON Schema** que describa los campos esperados (tipo, enum, rango).  
2. El esquema se incluye en el prompt mediante la instrucción “devuelve un JSON que cumpla este esquema”.  
3. El modelo realiza **Constrained Generation**, guiado por el esquema, y produce un texto que se valida contra él.  
4. La respuesta se parsea automáticamente a **Typed Outputs**, por ejemplo a un `dataclass` en Python, listo para usar en el resto del sistema.  

## Detalles
- **Básico**: crear un esquema simple (string, number) y añadirlo al prompt.  
- **Intermedio**: usar validaciones avanzadas (enum, patrones regex) y manejar errores de validación con re‑prompting.  
- **Avanzado**: combinar varios esquemas mediante `oneOf`/`anyOf`, integrar con **Tool Calling** para que el modelo invoque funciones que devuelvan datos estructurados, y aplicar **Memory** para mantener consistencia entre llamadas sucesivas.  

## Ejemplo minimo
```python
import openai
import json
from pydantic import BaseModel

class Producto(BaseModel):
    id: int
    nombre: str
    precio: float

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "nombre": {"type": "string"},
        "precio": {"type": "number"}
    },
    "required": ["id", "nombre", "precio"]
}

prompt = f"""Devuelve un JSON que cumpla este esquema:
{json.dumps(schema, indent=2)}"""

resp = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

data = json.loads(resp.choices[0].message.content)
producto = Producto(**data)
print(producto)
```

## Errores comunes
- **Olvidar validar** la salida contra el esquema → se generan excepciones al parsear.  
- **Esquema demasiado rígido** (p.ej. campos obligatorios innecesarios) → el modelo falla al cumplirlo.  
- **No usar temperature=0** en entornos críticos → aumenta la variabilidad y rompe la estructura.  

## Estado actual
- **Fundamentos estables**: JSON Schema y la práctica de incluirlo en prompts son ampliamente soportados por los principales proveedores de LLM.  
- **Práctica moderna**: los frameworks de IA (LangChain, LlamaIndex) ofrecen wrappers que automatizan la validación y el mapeo a tipos, y la integración con **Tool Calling** permite que el modelo delegue la generación estructurada a funciones externas cuando la complejidad supera la capacidad de generación directa.  

## Conexiones
- **Prompt Engineering**: la redacción del prompt que incluye el esquema es una técnica clave de ingeniería de prompts.  
- **Tool Calling**: cuando la generación estructurada es insuficiente, el modelo puede invocar una herramienta que devuelve datos ya validados.  
- **Memory**: mantener el esquema y los resultados anteriores en la memoria del agente permite respuestas coherentes a lo largo de una conversación.  

## Ruta de estudio
1. **Prerequisitos**: manejo básico de prompts, familiaridad con JSON y tipos de datos en Python.  
2. **Fundamentos**: aprender a escribir JSON Schemas y a incluirlos en prompts.  
3. **Práctica**: implementar validación automática con `pydantic` o `dataclasses`.  
4. **Avanzado**: explorar `oneOf`/`anyOf`, combinar con Tool Calling y gestionar estado con Memory.  
5. **Especialización**: contribuir a librerías como LangChain que abstraen Structured Outputs para flujos de trabajo complejos.  

## Preguntas de repaso
1. ¿Qué ventaja aporta un JSON Schema al diseñar la salida de un modelo de IA?  
2. ¿Cómo afecta la temperatura del modelo a la fiabilidad de los Structured Outputs?  
3. ¿Qué ocurre si la respuesta del modelo no pasa la validación contra el esquema?  
4. ¿De qué manera se relaciona Structured Outputs con Tool Calling?  
5. ¿Cuál es el beneficio de mapear la salida a un tipo tipado como un `dataclass` o `pydantic` model?

<!-- trazabilidad: run_id=run-20261106-180347-8a31fe concept=07-ai-engineering-11-structured-outputs written_at=2026-11-06T21:04:55.508861+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/10 - Prompt Engineering|Prompt Engineering]]
- [[07 - AI Engineering/13 - Tool Calling|Tool Calling]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]
- [[07 - AI Engineering/19 - Memory|Memory]]

---
← [[07 - AI Engineering/10 - Prompt Engineering|Prompt Engineering]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/12 - LLM APIs & Model Serving|LLM APIs & Model Serving]] →
