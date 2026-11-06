---
title: "Programming Fundamentals"
area: "Software Engineering"
numero: 1
aliases: ["Programming Fundamentals"]
tags: [concepto, it/software-engineering]
---
# Programming Fundamentals

> **Área:** [[01 - Software Engineering/00 - Índice Software Engineering|Índice Software Engineering]] · **Concepto 1 de 30**

## Qué abarca
- Variables
- funciones
- tipos
- control flow
- abstracción

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los fundamentos de programación para traducir requisitos del negocio en instrucciones ejecutables por una máquina. Resuelvo el problema de cómo estructurar datos, encapsular lógica y controlar el flujo de ejecución de manera predecible y mantenible. En mi día a día como ingeniero senior, estos conceptos aparecen al diseñar módulos, escribir APIs y depurar comportamientos inesperados. Cuando los domino, puedo crear componentes reutilizables, aplicar pruebas automatizadas y colaborar eficazmente con equipos multidisciplinarios. No necesito preocuparme de los fundamentos cuando trabajo exclusivamente con herramientas de bajo código o cuando delego la lógica a servicios externos que ya los encapsulan.

## Esqueleto (el 20% esencial)
1. **Variables** – espacio nombrado en memoria que almacena valores y permite su reutilización.  
2. **Funciones** – bloques de código reutilizables que reciben parámetros y devuelven resultados.  
3. **Tipos** – clasificación de valores (números, texto, booleanos, estructuras) que define operaciones válidas.  
4. **Control flow** – estructuras (condicionales, bucles) que determinan el orden de ejecución.  
5. **Abstracción** – ocultar detalles internos mediante interfaces o módulos para simplificar la interacción.

## Como funciona
1. Declaro una **variable** con un **tipo** adecuado para representar el dato que necesito.  
2. Encapsulo la lógica que opera sobre esas variables dentro de una **función**, definiendo sus parámetros y valor de retorno.  
3. Utilizo **control flow** (if/else, for, while) dentro de la función para decidir qué caminos seguir según los valores de las variables.  
4. Expongo la función mediante una **abstracción** (por ejemplo, una API o una clase) de modo que otros componentes la consuman sin conocer su implementación interna.  
5. En tiempo de ejecución, el motor del lenguaje evalúa el **control flow**, manipula las **variables** y devuelve resultados a quien llamó la **función**.

## Detalles
- **Básico**: declaración de variables simples, tipos primitivos y uso de `if`/`else`.  
- **Intermedio**: funciones con parámetros, retorno de valores compuestos (objetos, arrays) y bucles `for`/`while`.  
- **Avanzado**: funciones de orden superior, closures, manejo de errores, y diseño de interfaces que abstraen múltiples funciones y tipos.

## Ejemplo minimo
```python
# Variables y tipos
contador: int = 0

# Función con control flow
def incrementar(limite: int) -> int:
    while contador < limite:
        contador += 1
    return contador

print(incrementar(5))  # 5
```

## Errores comunes
- **Olvidar inicializar una variable** → genera errores de referencia; siempre asignar un valor inicial.  
- **Confundir tipos** (por ejemplo, sumar string y número) → usar conversiones explícitas.  
- **No devolver valor en una función** → la llamada recibe `None`; asegurar `return`.  
- **Anidar excesivo el control flow** → dificulta la lectura; refactorizar en funciones auxiliares.  

## Estado actual
- **Fundamentos estables**: la existencia de variables, tipos, funciones, y estructuras de control es constante en todos los lenguajes de propósito general.  
- **Práctica moderna**: se promueve la **abstracción** mediante programación funcional (lambdas, map/reduce) y orientada a objetos (interfaces, inyección de dependencias) para mejorar la testabilidad y la escalabilidad del código.

## Conexiones
- **Testing** – los fundamentos permiten escribir pruebas unitarias que verifican el comportamiento de funciones aisladas.  
- **Design Patterns** – la abstracción es la base de patrones como Strategy o Factory, que estructuran la creación y uso de objetos.  
- **Version Control** – al modularizar código con funciones y tipos, los cambios se pueden rastrear y fusionar de forma más segura.

## Ruta de estudio
1. **Prerequisitos**: lógica básica, familiaridad con al menos un lenguaje de programación.  
2. **Fundamentos**: practicar declaración de variables, tipos y control flow mediante ejercicios cortos.  
3. **Funciones y abstracción**: crear módulos reutilizables, introducir pruebas unitarias.  
4. **Profundización**: estudiar closures, programación funcional y patrones de diseño que extienden la abstracción.  
5. **Aplicación**: integrar los conceptos en un proyecto real, usando control de versiones y CI/CD.

## Preguntas de repaso
1. ¿Cómo afecta la elección del tipo de una variable al comportamiento del control flow?  
2. ¿Por qué es importante que una función siempre tenga un valor de retorno explícito?  
3. ¿Qué ventaja aporta la abstracción al trabajar con equipos multidisciplinarios?  
4. ¿Cómo puedes transformar un bucle `while` en una expresión funcional equivalente?  
5. ¿En qué situaciones podrías decidir ignorar la creación de una función adicional?

<!-- trazabilidad: run_id=run-20261105-135242-889677 concept=01-software-engineering-01-programming-fundamentals written_at=2026-11-05T16:53:49.142202+00:00 -->
<!-- ai:end -->

## Relacionados
- [[03 - Backend/04 - Lenguaje Backend|Lenguaje Backend]] · *Backend*
- [[03 - Backend/05 - Runtime|Runtime]] · *Backend*
- [[07 - AI Engineering/02 - Python & Programming|Python & Programming]] · *AI Engineering*

---
[[01 - Software Engineering/00 - Índice Software Engineering|Índice Software Engineering]] · [[01 - Software Engineering/02 - Data Structures|Data Structures]] →
