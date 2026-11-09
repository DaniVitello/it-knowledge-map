---
title: "Prototyping"
area: "UX / UI"
numero: 11
aliases: ["Prototyping"]
tags: [concepto, it/ux-ui]
---
# Prototyping

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 11 de 25**

## Qué abarca
- Prototipos low/high fidelity
- interacción

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el prototyping para materializar ideas de interacción antes de invertir en desarrollo, lo que me permite validar flujos, detectar fricciones y alinear al equipo con una visión tangible. Resuelvo el problema de la incertidumbre temprana al diseñar interfaces, ya que un prototipo muestra cómo se comportará la solución sin requerir código completo. Aparece en mi día a día cuando paso del wireframe a la prueba de usabilidad o cuando necesito comunicar decisiones de diseño a stakeholders. Después de entenderlo, puedo elegir el nivel de fidelidad adecuado, planificar pruebas y iterar rápidamente. No necesito preocuparme por prototipar cuando el alcance es meramente conceptual o cuando la solución ya está validada y se está implementando.

## Esqueleto (el 20% esencial)
1. **Fidelidad adecuada** – Selecciono low‑fidelity para explorar ideas rápidamente y high‑fidelity cuando necesito validar detalles visuales y de interacción.  
2. **Iteración rápida** – Cada versión del prototipo se prueba, se recoge feedback y se refina en ciclos cortos.  
3. **Enfoque en la interacción** – El prototipo debe reproducir los comportamientos clave (clics, transiciones, estados) que se evaluarán con usuarios.  

## Como funciona
1. Defino el objetivo de la prueba y el nivel de fidelidad necesario.  
2. Creo los artefactos iniciales (sketches o wireframes) que sirven de base.  
3. Uso una herramienta de prototyping (Figma, Axure, etc.) para añadir interactividad a los elementos.  
4. Realizo una sesión de prueba con usuarios reales o con el equipo interno.  
5. Recopilo observaciones, ajusto el flujo y repito el proceso hasta alcanzar la confianza requerida.

## Detalles
- **Básico**: papel o bocetos digitales sin interacción; sirve para validar la arquitectura de información.  
- **Intermedio**: prototipos de baja fidelidad con enlaces navegables; permite evaluar la lógica de flujo y la jerarquía visual.  
- **Avanzado**: prototipos de alta fidelidad con animaciones, micro‑interacciones y datos simulados; ideal para pruebas de usabilidad detalladas y para presentar a inversores o clientes.

## Ejemplo minimo
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Prototipo simple</title>
  <style>
    button { padding: 10px 20px; font-size: 1rem; }
  </style>
</head>
<body>
  <button id="cta">Comprar</button>
  <script>
    document.getElementById('cta').addEventListener('click', () => {
      alert('Proceso de compra iniciado');
    });
  </script>
</body>
</html>
```
Este código muestra un prototipo de alta fidelidad mínimo: un botón que simula la acción de compra mediante una alerta.

## Errores comunes
- **Demasiada fidelidad demasiado pronto** – genera gasto innecesario; evitarlo eligiendo low‑fidelity al inicio.  
- **No probar con usuarios reales** – el feedback interno no revela problemas de usabilidad; incluir siempre pruebas con usuarios.  
- **Olvidar los estados interactivos** – un prototipo estático no captura fricciones; añadir al menos hover y click.  

## Estado actual
- **Fundamentos estables**: la distinción entre low y high fidelity, la iteración basada en feedback y la necesidad de validar interacciones clave siguen siendo pilares del prototyping.  
- **Práctica moderna**: herramientas colaborativas en la nube permiten co‑edición en tiempo real y la integración de datos reales mediante APIs mock, lo que acelera la transición de prototipo a producto.

## Conexiones
- **Interaction Design**: el prototyping materializa los patrones de interacción diseñados, permitiendo su evaluación práctica.  
- **Wireframing**: los wireframes son la base estructural que se transforma en prototipos al añadir interactividad.  
- **User Testing**: los prototipos son el artefacto central en las pruebas de usabilidad, proporcionando el contexto necesario para observar comportamientos reales.

## Ruta de estudio
1. **Prerequisitos**: comprender principios básicos de UX, arquitectura de información y herramientas de diseño vectorial.  
2. **Fundamentos**: aprender a crear wireframes y a seleccionar la fidelidad adecuada según el objetivo de la prueba.  
3. **Práctica intermedia**: dominar al menos una herramienta de prototyping (p. ej., Figma) y ejecutar pruebas de usabilidad de baja fidelidad.  
4. **Avanzado**: incorporar micro‑interacciones, datos mock y pruebas A/B con prototipos de alta fidelidad; explorar integración con sistemas de gestión de feedback.  

## Preguntas de repaso
1. ¿Qué criterios utilizo para decidir entre un prototipo low‑fidelity y uno high‑fidelity?  
2. ¿Cómo se conecta el prototyping con el proceso de Interaction Design?  
3. ¿Cuál es el beneficio de incluir estados interactivos en un prototipo?  
4. ¿Qué error común implica gastar recursos en alta fidelidad demasiado pronto?  
5. ¿Qué pasos siguen a la fase de pruebas de un prototipo antes de pasar a desarrollo?

<!-- trazabilidad: run_id=run-20261106-202308-ff5d21 concept=08-ux-ui-11-prototyping written_at=2026-11-06T23:24:04.011827+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/08 - Interaction Design|Interaction Design]]
- [[08 - UX & UI/10 - Wireframing|Wireframing]]

---
← [[08 - UX & UI/10 - Wireframing|Wireframing]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]] →
