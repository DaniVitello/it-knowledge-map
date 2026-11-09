---
title: "Python & Programming"
area: "AI Engineering"
numero: 2
aliases: ["Python & Programming"]
tags: [concepto, it/ai-engineering]
---
# Python & Programming

> **Área:** [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · **Concepto 2 de 25**

## Qué abarca
- Python
- estructuras
- APIs
- async
- tooling

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Python como el lenguaje principal para orquestar pipelines de IA, conectar modelos a APIs y gestionar la lógica de negocio que rodea a los sistemas de inferencia. Resuelvo la necesidad de un entorno flexible que permita manipular datos, ejecutar código asíncrono y desplegar servicios de manera rápida y reproducible. Aparece en cada fase del producto de IA, desde la preparación de datos y el entrenamiento de modelos hasta la exposición de endpoints y el monitoreo de métricas. Después de dominar Python, puedo diseñar arquitecturas de backend, automatizar pruebas de modelo y escalar inferencias en la nube. No necesito preocuparme cuando el proyecto se limita a prototipos estáticos sin integración ni despliegue continuo.

## Esqueleto (el 20% esencial)
1. **Estructuras de datos** – listas, diccionarios y tensores facilitan la manipulación de entradas y salidas de modelos.  
2. **APIs y clientes HTTP** – `requests` o `httpx` permiten consumir servicios de modelo y exponer endpoints.  
3. **Programación asíncrona** – `asyncio` y `await` gestionan llamadas concurrentes a modelos sin bloquear.  
4. **Tooling de desarrollo** – entornos virtuales, linters y pruebas unitarias garantizan reproducibilidad y calidad.  
5. **Integración con librerías de IA** – `torch`, `tensorflow` y `transformers` se usan directamente desde Python.

## Como funciona
1. Defino la estructura de datos que recibirá el modelo (p. ej., dict con texto y metadatos).  
2. Creo una función que envía la petición al modelo mediante una API HTTP o llama al modelo localmente.  
3. Si la carga es alta, marco la función como `async` y utilizo `await` para lanzar múltiples inferencias en paralelo.  
4. Empaqueto la lógica en un módulo y lo pruebo con `pytest`, asegurando que los tipos y valores sean correctos.  
5. Despliego el módulo dentro de un contenedor o servidor FastAPI, donde el runtime de Python ejecuta el código bajo demanda.

## Detalles
- **Básico**: sintaxis de Python, tipos primitivos y estructuras de datos; uso de `pip` y entornos virtuales.  
- **Intermedio**: manejo de paquetes de IA, creación de clientes HTTP, introducción a `asyncio`.  
- **Avanzado**: patrones de concurrencia con `asyncio` + `httpx`, integración CI/CD con pruebas de modelo, profiling de rendimiento con `cProfile` y `py-spy`.

## Ejemplo minimo
```python
import asyncio, httpx

async def infer(text: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.ejemplo.com/v1/predict",
            json={"input": text}
        )
        return resp.json()["output"]

# Uso rápido
result = asyncio.run(infer("Hola mundo"))
print(result)
```

## Errores comunes
- Olvidar `await` en una llamada `async` → la coroutine nunca se ejecuta.  
- Usar objetos mutables como claves de diccionario → errores de hash.  
- No aislar dependencias en un entorno virtual → conflictos de versiones.  
- Ignorar manejo de excepciones en llamadas HTTP → caídas del servicio.  

## Estado actual
- **Fundamentos estables**: sintaxis de Python, estructuras de datos nativas y paquetes de IA como `torch` y `tensorflow`.  
- **Práctica moderna**: uso de `asyncio` y `httpx` para alta concurrencia, despliegue con FastAPI y contenedores Docker, pruebas automatizadas con `pytest` y cobertura de tipos mediante `mypy`.

## Conexiones
- **Programming Fundamentals**: los conceptos de variables y control de flujo son la base sobre la que se construyen los pipelines de IA.  
- **Lenguaje Backend**: Python actúa como el lenguaje de servidor que expone modelos a través de APIs REST.  
- **Runtime**: el intérprete de Python y su gestión de memoria influyen directamente en la latencia de inferencia y en la escalabilidad del servicio.

## Ruta de estudio
1. **Prerequisitos**: lógica de programación, manejo de listas/diccionarios y conceptos básicos de HTTP.  
2. **Fundamentos**: tutoriales oficiales de Python, ejercicios con `requests` y creación de funciones síncronas.  
3. **Intermedio**: introducción a `asyncio`, práctica con `httpx` y primeros experimentos con `torch` o `tensorflow`.  
4. **Avanzado**: diseño de APIs con FastAPI, pruebas unitarias y de integración, CI/CD con GitHub Actions, profiling y optimización de inferencias.  

## Preguntas de repaso
1. ¿Cómo estructuro los datos de entrada para que un modelo de IA los consuma eficientemente en Python?  
2. ¿Qué ventaja ofrece `asyncio` al llamar a un endpoint de inferencia desde un servicio de alta carga?  
3. ¿Cuál es la diferencia entre usar `requests` y `httpx` en un proyecto de IA?  
4. ¿Por qué es crítico aislar dependencias en un entorno virtual antes de desplegar un modelo?  
5. ¿Qué pasos incluye una prueba unitária típica para una función que envía una petición a un modelo?

<!-- trazabilidad: run_id=run-20261106-230027-0c76a2 concept=07-ai-engineering-02-python-programming written_at=2026-11-07T02:01:04.992631+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/01 - Programming Fundamentals|Programming Fundamentals]] · *Software Engineering*
- [[03 - Backend/04 - Lenguaje Backend|Lenguaje Backend]] · *Backend*
- [[03 - Backend/05 - Runtime|Runtime]] · *Backend*

---
← [[07 - AI Engineering/01 - AI - ML Fundamentals|AI / ML Fundamentals]] · [[07 - AI Engineering/00 - Índice AI Engineering|Índice AI Engineering]] · [[07 - AI Engineering/03 - Linear Algebra & Probability|Linear Algebra & Probability]] →
