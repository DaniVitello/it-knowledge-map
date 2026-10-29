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
- Usar los fundamentos de programación para traducir requisitos de negocio en código que compile, se ejecute y sea mantenible.  
- Resuelve el problema de *cómo* expresar lógica de negocio de forma estructurada y verificable, evitando errores de cálculo y comportamiento inesperado.  
- Aparece en el día a día de un ingeniero senior al diseñar algoritmos, escribir APIs, depurar fallas y revisar pull‑requests.  
- Después de dominarlo puedes estructurar sistemas complejos, automatizar pruebas y estimar esfuerzos con mayor precisión.  
- No necesitas preocuparte por él cuando trabajas exclusivamente con herramientas de bajo código o cuando delegas la lógica a servicios externos ya probados.  

## Esqueleto (el 20% esencial)
1. **Variables** – contenedores nombrados que almacenan datos temporales durante la ejecución.  
2. **Tipos** – definen la forma y operaciones válidas sobre los datos (int, string, bool, etc.).  
3. **Funciones** – unidades reutilizables que encapsulan una secuencia de instrucciones y devuelven un valor.  
4. **Control flow** – estructuras (if/else, loops, try/catch) que dirigen la ejecución según condiciones.  
5. **Abstracción** – ocultar detalles internos mediante interfaces o funciones para reducir complejidad.  

## Como funciona
1. **Declarar variables** con un tipo apropiado para representar el estado que necesita el algoritmo.  
2. **Aplicar control flow** para decidir qué bloques de código ejecutar según el valor de esas variables.  
3. **Invocar funciones** que operen sobre los datos, devolviendo resultados que pueden asignarse a nuevas variables.  
4. **Utilizar abstracción** para agrupar funciones relacionadas bajo una interfaz o módulo, facilitando pruebas unitarias y cambios futuros.  
5. El **runtime** del lenguaje (p. ej., Python) gestiona la asignación de memoria y la ejecución paso a paso de estas instrucciones.  

## Detalles
- **Básico**: declaración de variables simples, tipos primitivos y estructuras de control lineales.  
- **Intermedio**: funciones con parámetros y valores de retorno, manejo de excepciones, uso de tipos compuestos (listas, dicts).  
- **Avanzado**: closures, decoradores, programación orientada a objetos para crear abstracciones más potentes, y optimizaciones de control flow (tail‑recursion, async/await).  

## Ejemplo minimo
```python
# Variables y tipos
contador: int = 0
mensaje: str = "Hola"

# Función simple
def saludar(nombre: str) -> str:
    return f"{mensaje}, {nombre}!"

# Control flow
if contador < 5:
    print(saludar("Mundo"))
else:
    print("Límite alcanzado")
```
*?? verificar* que el tipo de anotación `int` y `str` sea compatible con la versión de Python usada en el proyecto.

## Errores comunes
- **Olvidar inicializar variables** → genera `NameError`; inicialízalas antes de usarlas.  
- **Confundir tipos** (p. ej., sumar `int` y `str`) → lanza `TypeError`; usa conversiones explícitas.  
- **Control flow incompleto** (falta `else`) → lógica inesperada; cubre todos los casos relevantes.  
- **Funciones con efectos secundarios ocultos** → dificultan pruebas; mantén funciones puras cuando sea posible.  

## Estado actual
- **Fundamentos estables**: variables, tipos, funciones, control flow y abstracción son pilares de cualquier lenguaje de backend y runtime modernos (sin verificar).  
- **Práctica moderna**: uso de tipado estático opcional (p. ej., `mypy` en Python), patrones de abstracción como inyección de dependencias y programación funcional ligera (sin verificar).  

## Conexiones
- **Lenguaje Backend** – los fundamentos son la base sobre la que se construyen servicios backend (API, microservicios).  
- **Runtime** – el motor de ejecución interpreta las variables, tipos y control flow en tiempo de ejecución.  
- **Python & Programming** – Python es un ejemplo concreto donde estos conceptos se aplican con sintaxis clara; la mayoría de los principios son transferibles a otros lenguajes.  

## Ruta de estudio
1. **Prerequisitos**: lógica básica, familiaridad con la línea de comandos y un editor de código.  
2. **Fundamentos**: tutoriales de variables, tipos y control flow en el lenguaje elegido.  
3. **Funciones y abstracción**: ejercicios de refactorización y creación de módulos.  
4. **Práctica avanzada**: patrones de diseño, pruebas unitarias y tipado estático.  
5. **Especialización**: aplicar los fundamentos a un framework backend (Django, FastAPI, etc.).  

## Preguntas de repaso
1. ¿Cómo ayuda una variable bien tipada a prevenir errores en producción?  
2. ¿Qué diferencia hay entre una función pura y una con efectos secundarios, y por qué importa en pruebas?  
3. Describe un caso donde un `if/else` mal estructurado puede generar un bug difícil de detectar.  
4. ¿De qué manera la abstracción facilita la integración de un nuevo runtime o lenguaje backend?  
5. Cuando trabajas con un servicio externo ya probado, ¿puedes ignorar los fundamentos de programación en tu código?  
<!-- ai:end -->

## Relacionados
- [[03 - Backend/04 - Lenguaje Backend|Lenguaje Backend]] · *Backend*
- [[03 - Backend/05 - Runtime|Runtime]] · *Backend*
- [[07 - AI Engineering/02 - Python & Programming|Python & Programming]] · *AI Engineering*

---
[[01 - Software Engineering/00 - Índice Software Engineering|Índice Software Engineering]] · [[01 - Software Engineering/02 - Data Structures|Data Structures]] →
