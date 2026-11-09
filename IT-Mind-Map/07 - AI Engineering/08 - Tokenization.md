---
title: "Tokenization"
area: "AI Engineering"
numero: 8
aliases: ["Tokenization"]
tags: [concepto, it/ai-engineering]
---
# Tokenization

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 8 de 25**

## Qué abarca
- Tokens
- token budgets
- context

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la tokenización para convertir texto libre en unidades discretas que el modelo de IA pueda procesar. Resuelvo el problema de que los transformers solo operan sobre secuencias numéricas de longitud limitada, lo que permite que los prompts, documentos y respuestas entren dentro del “token budget” del modelo. Aparece en cada etapa del pipeline de un producto de IA: al pre‑procesar datos de entrenamiento, al construir prompts dinámicos y al medir el coste de inferencia. Después de entenderla, puedo estimar el consumo de contexto, diseñar prompts eficientes y diagnosticar fallos de truncamiento. No necesito preocuparme cuando trabajo exclusivamente con datos ya tokenizados o con modelos que aceptan directamente vectores pre‑embebidos.

## Esqueleto (el 20% esencial)
1. **Tokens** – unidades mínimas que el modelo consume (palabras, sub‑palabras o caracteres).  
2. **Token budgets** – límite máximo de tokens que caben en el contexto del modelo (p. ej., 8 k, 32 k).  
3. **Context** – ventana de tokens que el modelo mantiene simultáneamente para generar respuestas.  
4. **Longitud variable** – la tokenización determina cuántos tokens ocupa cada fragmento de texto, influyendo en coste y latencia.  

## Como funciona
1. El texto de entrada se pasa a un **tokenizer** que aplica reglas de segmentación (p. ej., BPE o WordPiece).  
2. Cada segmento se mapea a un **id de token** según el vocabulario del modelo.  
3. El conjunto de ids forma la **secuencia de tokens** que se inserta en la ventana de **contexto**.  
4. Durante la inferencia, el modelo verifica que la longitud total no supere el **token budget**; si la supera, se trunca o se divide en varios llamados.  
5. La salida del modelo se vuelve a des‑tokenizar para obtener texto legible.

## Detalles
- **Básico:** tokenizadores de sub‑palabras (BPE) que equilibran vocabulario pequeño y cobertura de palabras raras.  
- **Intermedio:** manejo de tokens especiales (e.g., ``<pad>``, ``<eos>``, ``<bos>``) y control de longitud mediante parámetros como `max_length` y `truncation`.  
- **Avanzado:** técnicas de *prompt engineering* que ajustan la distribución de tokens para maximizar la información útil dentro del budget, y uso de *sliding windows* para procesar documentos extensos.

## Ejemplo minimo
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
texto = "Hola, IA!"
ids = tokenizer.encode(texto, add_special_tokens=False)
print("Tokens:", tokenizer.convert_ids_to_tokens(ids))
print("IDs:", ids)
```

## Errores comunes
- **Olvidar el límite de tokens:** genera respuestas truncadas; usar `max_length` y revisar `len(ids)`.  
- **Contar caracteres en vez de tokens:** la longitud real varía; siempre medir con el tokenizer.  
- **Reusar vocabularios incompatibles:** usar un tokenizer distinto al modelo provoca errores de dimensión; asegurarse de que coincidan.

## Estado actual
- **Fundamentos estables:** los algoritmos BPE y WordPiece siguen siendo la base de la tokenización en LLMs.  
- **Práctica moderna:** los frameworks (Transformers, LangChain) exponen APIs para gestión automática de budgets y sliding windows, y se adoptan tokenizers de tipo *fast* (Rust‑based) para mayor velocidad.

## Conexiones
- **Neural Networks:** los tokens son la entrada discreta que alimenta la arquitectura de redes neuronales.  
- **Transformers:** el mecanismo de atención opera sobre la secuencia de tokens dentro del contexto.  
- **Embeddings:** cada token se proyecta a un vector de embedding antes de entrar al modelo.

## Ruta de estudio
1. **Prerequisitos:** Python, conceptos básicos de NLP y de redes neuronales.  
2. **Fundamentos:** estudiar BPE/WordPiece y experimentar con `AutoTokenizer`.  
3. **Práctica:** implementar prompts que respeten el token budget y medir latencia.  
4. **Avanzado:** explorar técnicas de sliding window y de token‑level pruning para documentos largos.  

## Preguntas de repaso
1. ¿Qué es un token y por qué el modelo no procesa texto sin tokenizar?  
2. ¿Cómo afecta el token budget al diseño de un prompt para un modelo de 8 k tokens?  
3. ¿Cuál es la diferencia entre contar caracteres y contar tokens en una solicitud de inferencia?  
4. ¿Qué consecuencias tiene usar un tokenizer que no corresponde al modelo seleccionado?  
5. ¿Cómo se puede manejar un documento que supera el límite de contexto del modelo?

<!-- trazabilidad: run_id=run-20261109-162856-297812 concept=07-ai-engineering-08-tokenization written_at=2026-11-09T19:30:23.731333+00:00 -->
<!-- ai:end -->

## Relacionados
- [[07 - AI Engineering/05 - Neural Networks|Neural Networks]]
- [[07 - AI Engineering/06 - Transformers|Transformers]]
- [[07 - AI Engineering/07 - LLMs|LLMs]]
- [[07 - AI Engineering/09 - Embeddings|Embeddings]]

---
← [[07 - AI Engineering/07 - LLMs|LLMs]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/09 - Embeddings|Embeddings]] →
