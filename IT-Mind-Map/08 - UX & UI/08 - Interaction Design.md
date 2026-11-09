---
title: "Interaction Design"
area: "UX / UI"
numero: 8
aliases: ["Interaction Design"]
tags: [concepto, it/ux-ui]
---
# Interaction Design

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 8 de 25**

## Qué abarca
- Cómo el usuario interactúa con el producto

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Interaction Design para estructurar y guiar la forma en que los usuarios realizan acciones dentro de un producto digital. Resuelvo la ambigüedad de “¿cómo debería tocar, deslizar o escribir el usuario para conseguir su objetivo?” y, por tanto, mejoro la eficiencia, la satisfacción y la reducción de errores. En mi día a día como diseñador de producto senior, lo aplico al crear flujos de tareas, definir patrones de interacción y validar que cada elemento de la interfaz responde de manera predecible. Después de comprenderlo, puedo diseñar interacciones coherentes, evaluar prototipos y comunicar requisitos claros a desarrollo. No necesito enfocarme en Interaction Design cuando el proyecto se limita a contenido estático sin acciones del usuario.

## Esqueleto (el 20% esencial)
1. **Entender la intención del usuario** – identificar la meta que persigue en cada paso del flujo.  
2. **Definir los patrones de interacción** – seleccionar gestos, clicks o teclas que mejor sirvan a esa intención.  
3. **Mapear la secuencia de acciones** – ordenar los pasos de forma lógica y minimizar la carga cognitiva.  
4. **Prototipar y testear** – crear representaciones interactivas y validar con usuarios reales.  
5. **Iterar con feedback** – ajustar los patrones según los hallazgos de usabilidad.

## Como funciona
1. **Investigación de intención**: a través de entrevistas o análisis de tareas, descubro qué quiere lograr el usuario.  
2. **Selección de patrones**: elijo entre botones, deslizamientos, arrastrar‑y‑soltar, etc., basándome en la intención y en las limitaciones del dispositivo.  
3. **Diseño del flujo**: dibujo wireframes que conectan cada acción en una secuencia clara, asegurando que no haya pasos innecesarios.  
4. **Construcción del prototipo**: paso de wireframes a un prototipo interactivo que permite al usuario ejecutar el flujo.  
5. **Pruebas de usabilidad**: observo si los usuarios completan la tarea sin fricción y recojo datos de error y tiempo.  
6. **Iteración**: refino los patrones y el orden de los pasos hasta alcanzar una interacción fluida.

## Detalles
- **Básico**: reconocer la necesidad de una interacción y asignar un control UI simple (p.ej., botón “Enviar”).  
- **Intermedio**: combinar varios controles en un flujo coherente, aplicar principios de affordance y feedback visual.  
- **Avanzado**: diseñar interacciones adaptativas que cambian según contexto (modo oscuro, accesibilidad, dispositivos) y sincronizar con animaciones micro‑interactivas para reforzar la respuesta del sistema.

## Ejemplo minimo
```html
<!-- Botón que envía un formulario al pulsar Enter o clic -->
<form id="login">
  <input type="text" placeholder="Usuario" required>
  <input type="password" placeholder="Contraseña" required>
  <button type="submit">Entrar</button>
</form>

<script>
document.getElementById('login').addEventListener('submit', function(e){
  e.preventDefault();               // evita recarga
  // lógica de autenticación
  alert('Acceso concedido');
});
</script>
```
Este fragmento muestra la interacción esencial: el usuario escribe datos y activa la acción mediante clic o tecla Enter, recibiendo feedback inmediato.

## Errores comunes
- **Sobrecargar la interfaz con demasiados gestos** – simplificar a los patrones más intuitivos.  
- **Ignorar el feedback visual** – siempre proveer una respuesta clara (cambio de color, animación).  
- **Diseñar sin pruebas de usabilidad** – validar con usuarios reales antes de cerrar el diseño.

## Estado actual
Los fundamentos de Interaction Design (intención, patrones, flujo) siguen siendo estables y se aplican en la mayoría de los productos digitales. La práctica moderna incorpora micro‑interacciones, diseño responsivo y accesibilidad como requisitos estándar, y se apoya en herramientas de prototipado rápido que permiten iterar en ciclos de días.

## Conexiones
- **Wireframing**: sirve como plano estático donde se definen los puntos de interacción antes de añadir dinamismo.  
- **Prototyping**: transforma los wireframes en experiencias interactivas que permiten probar los patrones de Interaction Design.  
- **Usability Testing**: evalúa si las interacciones diseñadas cumplen con las expectativas y metas del usuario.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de UX research, arquitectura de información y principios de usabilidad.  
2. **Fundamentos**: estudiar patrones de interacción comunes (botones, formularios, gestos) y principios de affordance.  
3. **Herramientas**: aprender a usar Figma o Adobe XD para crear wireframes y prototipos interactivos.  
4. **Práctica**: diseñar flujos de tareas simples, testear con usuarios y documentar hallazgos.  
5. **Especialización**: explorar micro‑interacciones, diseño para accesibilidad y adaptación a dispositivos emergentes.

## Preguntas de repaso
1. ¿Cómo identifico la intención del usuario antes de definir un patrón de interacción?  
2. ¿Qué diferencia hay entre un wireframe y un prototipo en el contexto de Interaction Design?  
3. ¿Por qué es crítico incluir feedback visual en cada interacción?  
4. ¿Cuál es el riesgo de introducir demasiados gestos diferentes en una misma pantalla?  
5. ¿Cómo integraría pruebas de usabilidad en el ciclo de iteración de Interaction Design?

<!-- trazabilidad: run_id=run-20261106-201958-b16a4c concept=08-ux-ui-08-interaction-design written_at=2026-11-06T23:21:01.354559+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/10 - Wireframing|Wireframing]]
- [[08 - UX & UI/11 - Prototyping|Prototyping]]

---
← [[08 - UX & UI/07 - Navigation|Navigation]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/09 - User Flows|User Flows]] →
