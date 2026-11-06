---
title: "Memory"
area: "AI Engineering"
numero: 19
aliases: ["Memory"]
tags: [concepto, it/ai-engineering]
---
# Memory

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 19 de 25**

## Qué abarca
- Conversation state
- long-term memory
- retrieval

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la **Memory** para que un agente de IA mantenga información relevante entre interacciones, evitando que el modelo tenga que recomponer todo el contexto en cada llamada. Resuelvo la pérdida de coherencia en conversaciones largas y la incapacidad de reutilizar conocimientos adquiridos previamente, lo que mejora la fiabilidad y la experiencia del usuario. Aparece cada vez que diseño un chatbot, un asistente personal o un flujo de trabajo que requiere recordar preferencias, historial de acciones o resultados de inferencias anteriores. Después de entenderla, puedo diseñar sistemas que combinen memoria a corto plazo (estado de la conversación) y a largo plazo (persistencia en bases de datos) y decidir cuándo delegar la recuperación a un motor de búsqueda externo. No necesito preocuparme por Memory cuando el producto solo procesa consultas aisladas sin dependencia temporal.

## Esqueleto (el 20% esencial)
1. **Conversation state** – guarda el contexto inmediato de la interacción para que el modelo genere respuestas coherentes.  
2. **Long‑term memory** – persiste información más allá de la sesión actual, permitiendo reutilizar aprendizajes y datos de usuario.  
3. **Retrieval** – mecanismo que busca en la memoria (caché, base de datos, vector store) la información más relevante para la petición actual.  
4. **Update policy** – regla que decide cuándo y cómo se añaden o modifican entradas en la memoria.  
5. **Expiration** – criterio que elimina datos obsoletos para evitar ruido y sobrecarga.

## Como funciona
1. Al iniciar la conversación, el agente crea un **conversation state** vacío.  
2. Cada mensaje del usuario se añade al estado y, si corresponde, se actualiza la **long‑term memory** mediante la **update policy**.  
3. Cuando el modelo necesita contexto, se ejecuta **retrieval**: se consultan tanto el estado actual como la memoria persistente usando claves o embeddings.  
4. Los resultados recuperados se inyectan en el prompt (prompt engineering) y el modelo genera la respuesta.  
5. Periodicamente, el sistema aplica **expiration** para limpiar entradas viejas.

## Detalles
- **Básico**: usar una lista en memoria RAM para el conversation state; actualizarla después de cada turno.  
- **Intermedio**: integrar un vector store (p. ej., FAISS) para la long‑term memory y emplear embeddings de los mensajes para una recuperación semántica.  
- **Avanzado**: definir políticas de actualización basadas en importancia (p. ej., puntuación de relevancia) y combinar múltiples fuentes de memoria (caché, base de datos relacional, knowledge graph).  
- **Seguridad**: aplicar encriptación y control de acceso a la long‑term memory cuando se almacena información sensible.  
- **Escalabilidad**: shardear el vector store y usar índices invertidos para búsquedas rápidas en grandes volúmenes de datos.

## Ejemplo minimo
```python
from collections import deque

# 1. Conversation state (FIFO de 3 turnos)
state = deque(maxlen=3)

def add_to_state(user_msg, assistant_msg):
    state.append({"role": "user", "content": user_msg})
    state.append({"role": "assistant", "content": assistant_msg})

def build_prompt(new_msg):
    # 2. Inyectar estado en el prompt
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in state])
    prompt += f"\nuser: {new_msg}"
    return prompt

# Simulación
add_to_state("Hola", "¡Hola! ¿En qué puedo ayudar?")
print(build_prompt("¿Cuál es mi última compra?"))
```

## Errores comunes
- **Sobrecargar la memoria** con información irrelevante → usar políticas de expiración y filtrado.  
- **Olvidar actualizar la long‑term memory** después de eventos críticos → incluir hooks de actualización en cada acción importante.  
- **Confundir estado de conversación con memoria persistente** → mantener separadas las estructuras de datos y sus ciclos de vida.

## Estado actual
- **Fundamentos estables**: uso de colas para conversation state y bases de datos vectoriales para recuperación semántica.  
- **Práctica moderna**: integración de Retrieval‑Augmented Generation (RAG) con LLMs, políticas de actualización basadas en atención y métricas de relevancia, y despliegues de memoria distribuida en infraestructuras cloud.

## Conexiones
- **Prompt Engineering** – la memoria provee los fragmentos que se insertan en el prompt para guiar al modelo.  
- **Tool Calling** – la información recuperada puede decidir qué herramienta externa invocar (p. ej., buscar en una API).  
- **AI Workflows** – la gestión de memoria es un paso clave dentro de pipelines que incluyen pre‑procesado, inferencia y post‑procesado.

## Ruta de estudio
1. **Prerequisitos**: Python, conceptos de LLMs, fundamentos de bases de datos y embeddings.  
2. **Fundamental**: implementar conversation state con estructuras de datos simples; experimentar con prompts que incluyan historial.  
3. **Intermedio**: aprender a usar FAISS o Elastic Vector para long‑term memory; practicar retrieval con embeddings.  
4. **Avanzado**: diseñar políticas de actualización y expiración; combinar RAG con tool calling; escalar la memoria en entornos distribuidos.  
5. **Especialización**: seguridad de datos en memoria, optimización de latencia y costos, y evaluación de impacto en métricas de fiabilidad del producto.

## Preguntas de repaso
1. ¿Cómo diferencia la **conversation state** de la **long‑term memory** en un agente de IA?  
2. ¿Qué papel juega la **retrieval** al generar una respuesta con contexto?  
3. ¿Cuándo deberías aplicar una **policy de expiración** y cuál es su beneficio?  
4. ¿De qué manera la **Memory** influye en la **Tool Calling** dentro de un workflow?  
5. ¿Qué ventajas aporta usar un vector store frente a una lista en RAM para la memoria a largo plazo?

<!-- trazabilidad: run_id=run-20261106-181504-d0713a concept=07-ai-engineering-19-memory written_at=2026-11-06T21:16:18.503914+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/10 - Prompt Engineering|Prompt Engineering]]
- [[07 - AI Engineering/11 - Structured Outputs|Structured Outputs]]
- [[07 - AI Engineering/13 - Tool Calling|Tool Calling]]
- [[07 - AI Engineering/16 - Agents|Agents]]
- [[07 - AI Engineering/17 - AI Workflows|AI Workflows]]
- [[07 - AI Engineering/18 - Context Engineering|Context Engineering]]

---
← [[07 - AI Engineering/18 - Context Engineering|Context Engineering]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/20 - Evaluation|Evaluation]] →
