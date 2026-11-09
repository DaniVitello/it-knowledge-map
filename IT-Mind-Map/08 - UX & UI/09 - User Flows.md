---
title: "User Flows"
area: "UX / UI"
numero: 9
aliases: ["User Flows"]
tags: [concepto, it/ux-ui]
---
# User Flows

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 9 de 25**

## Qué abarca
- Caminos necesarios para completar tareas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los **User Flows** para visualizar, planificar y validar el recorrido que debe seguir un usuario para completar una tarea dentro de un producto digital. Resuelvo la ambigüedad que surge al diseñar interacciones complejas, asegurando que cada paso necesario esté presente y sea coherente con los objetivos del negocio y las expectativas del usuario. Aparecen en mi día a día cuando defino la arquitectura de interacción de una nueva funcionalidad o cuando evalúo la usabilidad de una pantalla existente. Después de comprenderlos, puedo crear prototipos más enfocados, priorizar mejoras y comunicar de forma clara el comportamiento esperado a desarrolladores y stakeholders. Cuando la tarea es trivial o la interfaz ya está validada mediante pruebas de usabilidad, no es necesario dedicar tiempo a elaborar un User Flow detallado.

## Esqueleto (el 20% esencial)
1. **Identificar la meta del usuario**: definir claramente qué quiere lograr al iniciar la interacción.  
2. **Desglosar la tarea en pasos obligatorios**: enumerar cada acción que el usuario debe ejecutar para alcanzar la meta.  
3. **Mapear decisiones y ramificaciones**: señalar los puntos donde el usuario puede elegir entre alternativas que alteran el flujo.  
4. **Asignar resultados esperados a cada paso**: describir el estado de la interfaz o la información que el usuario recibe después de cada acción.  
5. **Validar la completitud del flujo**: comprobar que no falten pasos críticos y que el recorrido sea lógico y sin bloqueos.

## Como funciona
1. **Recolecto la necesidad** a través de investigación (entrevistas, análisis de tareas).  
2. **Defino la meta** del usuario y la escribo como una frase de objetivo.  
3. **Listo los pasos** que el usuario debe seguir, ordenándolos cronológicamente.  
4. **Inserto puntos de decisión** donde el usuario elige entre opciones (p. ej., “¿Guardar o descartar?”).  
5. **Asigno resultados** (cambios de pantalla, mensajes) a cada paso y decisión.  
6. **Reviso el flujo** con el equipo y lo ajusto según feedback antes de pasar a prototipado.

## Detalles
- **Básico**: crear un diagrama lineal que muestre la secuencia de pantallas y acciones principales.  
- **Intermedio**: añadir ramificaciones, condiciones de error y estados alternativos (p. ej., usuarios sin permisos).  
- **Avanzado**: integrar métricas de éxito (tiempo, tasa de abandono), conectar el flujo con la arquitectura de información y documentar reglas de negocio que influyen en decisiones.

## Ejemplo minimo
```json
{
  "meta": "Publicar una foto",
  "pasos": [
    {"accion": "Abrir cámara", "resultado": "Vista de captura"},
    {"accion": "Tomar foto", "resultado": "Vista de previsualización"},
    {"accion": "Confirmar", "resultado": "Pantalla de edición"},
    {"accion": "Compartir", "resultado": "Foto publicada"}
  ]
}
```

## Errores comunes
- **Olvidar pasos de validación** (p. ej., confirmación de datos) → revisar checklist de requisitos antes de cerrar el flujo.  
- **Crear ramificaciones excesivas** que confunden al usuario → limitar decisiones a las realmente necesarias.  
- **No alinear el flujo con la arquitectura de información** → validar que cada pantalla pertenece a la estructura de navegación prevista.  

## Estado actual
- **Fundamentos estables**: los User Flows siguen siendo una herramienta esencial para estructurar tareas y comunicar requisitos de interacción.  
- **Práctica moderna**: se combinan con herramientas de prototipado rápido y pruebas de usabilidad temprana; además, se integran en sistemas de diseño que permiten generar flujos a partir de componentes reutilizables.

## Conexiones
- **Information Architecture**: el User Flow depende de la organización de contenidos para garantizar que cada paso tenga una ubicación lógica dentro del sitio o la app.  
- **Navigation**: los flujos determinan los patrones de navegación (p. ej., breadcrumb, menú lateral) que el usuario seguirá para avanzar.  
- **Usability Testing**: los flujos sirven como guías de escenario durante pruebas de usabilidad, facilitando la observación de puntos de fricción.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de UX research, principios de diseño centrado en el usuario y nociones de arquitectura de información.  
2. **Fundamentos**: leer guías de creación de User Flows, practicar con casos simples (registro, compra).  
3. **Intermedio**: aprender a mapear decisiones complejas y a incorporar métricas de éxito.  
4. **Avanzado**: integrar flujos en sistemas de diseño, usar herramientas de prototipado colaborativo y validar con pruebas de usabilidad.  
5. **Especialización**: explorar flujos para experiencias multicanal (web, móvil, voz) y automatizar su documentación.

## Preguntas de repaso
1. ¿Cuál es el primer paso para iniciar la creación de un User Flow?  
2. ¿Cómo se diferencia una decisión de una acción dentro del flujo?  
3. ¿Qué riesgo implica añadir demasiadas ramificaciones en un User Flow?  
4. ¿De qué manera los User Flows se relacionan con la Information Architecture?  
5. ¿Qué información adicional se suele añadir a un User Flow avanzado para medir su efectividad?

<!-- trazabilidad: run_id=run-20261106-202101-989e29 concept=08-ux-ui-09-user-flows written_at=2026-11-06T23:22:06.180563+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/06 - Information Architecture|Information Architecture]]
- [[08 - UX & UI/07 - Navigation|Navigation]]

---
← [[08 - UX & UI/08 - Interaction Design|Interaction Design]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/10 - Wireframing|Wireframing]] →
