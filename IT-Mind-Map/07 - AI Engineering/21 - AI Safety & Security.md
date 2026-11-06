---
title: "AI Safety & Security"
area: "AI Engineering"
numero: 21
aliases: ["AI Safety & Security"]
tags: [concepto, it/ai-engineering]
---
# AI Safety & Security

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 21 de 25**

## Qué abarca
- Prompt injection
- data leakage
- abuse
- permissions

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo AI Safety & Security para garantizar que los sistemas de IA que despliego sean confiables, no filtren datos sensibles y no puedan ser manipulados por usuarios malintencionados. Resuelvo problemas como la inyección de prompts que alteran el comportamiento del modelo, la filtración inadvertida de información de entrenamiento y el uso indebido de la API. Aparece en cada fase del ciclo de vida del producto: diseño, integración, pruebas y monitoreo. Después de entenderlo, puedo diseñar controles de acceso, validar salidas y establecer observabilidad que detecte abusos. No necesito preocuparme cuando el modelo se usa internamente sin exposición a usuarios externos y sin datos sensibles.

## Esqueleto (el 20% esencial)
1. **Prompt injection** – los usuarios pueden insertar instrucciones que desvían el modelo de su propósito original.  
2. **Data leakage** – el modelo puede reproducir información confidencial presente en los datos de entrenamiento.  
3. **Abuse** – actores externos pueden explotar la IA para generar contenido dañino o automatizar ataques.  
4. **Permissions** – la gestión de quién puede invocar el modelo y con qué parámetros es clave para limitar riesgos.  

## Como funciona
1. **Diseño de la superficie de ataque**: se identifican puntos donde el prompt llega al modelo (API, UI).  
2. **Validación de entrada**: se aplican filtros y sanitización para bloquear patrones de inyección.  
3. **Control de salida**: se usan heurísticas y modelos de detección para impedir que se devuelvan datos sensibles.  
4. **Gestión de permisos**: se asignan roles y tokens con scopes limitados que definen qué prompts pueden enviarse.  
5. **Monitoreo y respuesta**: logs de requests se analizan en tiempo real para detectar abuso y activar bloqueos.

## Detalles
- **Básico**: aplicar listas blancas de palabras y limitar la longitud del prompt.  
- **Intermedio**: integrar un modelo secundario de detección de contenido tóxico y usar técnicas de differential privacy para reducir leakage.  
- **Avanzado**: implementar sandboxing de ejecución, auditorías de datos de entrenamiento y políticas de zero‑trust en la cadena de suministro de modelos.

## Ejemplo minimo
```python
import openai

def safe_completion(prompt, api_key):
    # 1. Sanitizar prompt
    forbidden = ["system:", "reset", "ignore"]
    if any(tok in prompt.lower() for tok in forbidden):
        raise ValueError("Prompt contiene comandos prohibidos")
    # 2. Llamada segura
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key,
        max_tokens=200,
        temperature=0.0,
    )
    # 3. Filtrar salida sensible (ejemplo simple)
    if "password" in response.choices[0].message.content.lower():
        raise ValueError("Posible fuga de datos")
    return response.choices[0].message.content

print(safe_completion("¿Cuál es la capital de Francia?", "sk-..."))
```

## Errores comunes
- **Filtrar solo palabras clave**: no captura variaciones; usar expresiones regulares o modelos de detección.  
- **Confiar únicamente en logs**: sin alertas en tiempo real se pierde la ventana de mitigación; implementar detección automática.  
- **Asignar permisos demasiado amplios**: aplicar el principio de menor privilegio desde el inicio.

## Estado actual
Los fundamentos de AI Safety & Security (filtrado de prompts, control de salida y gestión de permisos) son prácticas estables y ampliamente adoptadas en la industria. La práctica moderna incorpora técnicas de **differential privacy**, **red teaming** de modelos y **observability** basada en trazas de inferencia para detectar abuso en tiempo real.

## Conexiones
- **Security Engineering**: provee metodologías de threat modeling que se adaptan a los vectores de ataque de IA.  
- **HTTPS / TLS**: asegura la confidencialidad e integridad de los datos en tránsito entre cliente y servicio de IA.  
- **Observability**: permite rastrear métricas de uso y anomalías que indican posibles inyecciones o abusos.

## Ruta de estudio
1. **Prerequisitos**: conceptos de redes (TLS), control de acceso (OAuth scopes) y fundamentos de ML.  
2. **Fundamentos**: estudiar prompt sanitization, técnicas de redacción segura y políticas de permisos.  
3. **Intermedio**: aprender differential privacy y modelos de detección de contenido.  
4. **Avanzado**: practicar red teaming de LLMs, implementar sandboxing y diseñar pipelines de observabilidad con tracing.

## Preguntas de repaso
1. ¿Qué es una inyección de prompt y cómo afecta la confiabilidad del modelo?  
2. ¿De qué manera el control de permisos reduce el riesgo de abuso en una API de IA?  
3. ¿Cuál es la diferencia entre filtrado estático de palabras y un modelo de detección de contenido?  
4. ¿Cómo ayuda la observabilidad a identificar intentos de data leakage en tiempo real?  
5. ¿Qué técnicas de privacidad diferencial pueden aplicarse para mitigar la fuga de datos?

<!-- trazabilidad: run_id=run-20261106-181723-daf11c concept=07-ai-engineering-21-ai-safety-security written_at=2026-11-06T21:18:40.066216+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/24 - Security Engineering|Security Engineering]] · *Software Engineering*
- [[03 - Backend/18 - Seguridad|Seguridad]] · *Backend*
- [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]] · *Networking / Internet*
- [[05 - Networking & Internet/24 - Firewalls|Firewalls]] · *Networking / Internet*
- [[07 - AI Engineering/20 - Evaluation|Evaluation]]
- [[07 - AI Engineering/22 - Observability|Observability]]

---
← [[07 - AI Engineering/20 - Evaluation|Evaluation]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/22 - Observability|Observability]] →
