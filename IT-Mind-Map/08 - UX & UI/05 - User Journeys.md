---
title: "User Journeys"
area: "UX / UI"
numero: 5
aliases: ["User Journeys"]
tags: [concepto, it/ux-ui]
---
# User Journeys

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 5 de 25**

## Qué abarca
- Journey maps
- escenarios
- puntos de contacto

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los User Journeys para visualizar, paso a paso, cómo un usuario alcanza su objetivo dentro de un producto digital. Resuelvo la falta de claridad sobre los momentos críticos y los puntos de contacto que influyen en la satisfacción del usuario. Aparecen en la fase de diseño de interacción, cuando paso de la investigación a la definición de flujos, y me permiten priorizar mejoras y validar hipótesis de usabilidad. Después de entenderlos, puedo diseñar prototipos alineados con las expectativas reales y medir su efectividad; cuando el producto ya está validado y los flujos son estables, no es necesario volver a crear journeys completos.

## Esqueleto (el 20% esencial)
1. **Escenario de uso** – una situación concreta que describe la motivación del usuario y el contexto en que interactúa con el producto.  
2. **Puntos de contacto** – cada interacción (pantalla, mensaje, acción) donde el usuario toca el sistema.  
3. **Objetivo del usuario** – la meta que persigue en ese journey (ej. “comprar un boleto”).  
4. **Emociones y fricciones** – indicadores de satisfacción o problemas en cada punto de contacto.  
5. **Resultado esperado** – el estado final que valida si el journey fue exitoso.

## Como funciona
1. Parto de un **escenario de uso** identificado en la investigación de usuarios.  
2. Desgloso el escenario en una secuencia de **puntos de contacto** que el usuario encontrará.  
3. Asigno a cada punto de contacto un **objetivo del usuario** y registro sus **emociones y fricciones** observadas o anticipadas.  
4. Conecto los puntos para formar una narrativa coherente que culmina en el **resultado esperado**.  
5. Reviso el mapa con stakeholders y lo utilizo para priorizar diseños, pruebas y mejoras.

## Detalles
- **Básico:** crear un journey simple con 3‑4 pasos, centrado en un solo objetivo y sin profundizar en emociones.  
- **Intermedio:** añadir capas de contexto (dispositivo, entorno) y mapear emociones usando iconos de satisfacción/insatisfacción.  
- **Avanzado:** integrar datos de analítica (tiempos, tasas de abandono) y enlazar cada punto con criterios de éxito medibles; combinar varios journeys para identificar patrones comunes.

## Ejemplo minimo
```json
{
  "escenario": "Usuario compra una suscripción mensual",
  "objetivo": "Completar la compra",
  "puntosDeContacto": [
    { "paso": 1, "pantalla": "Home", "accion": "Click en 'Suscribirse'", "emocion": "Curiosidad" },
    { "paso": 2, "pantalla": "Planes", "accion": "Seleccionar plan", "emocion": "Confianza" },
    { "paso": 3, "pantalla": "Pago", "accion": "Ingresar datos y confirmar", "emocion": "Ansiedad" },
    { "paso": 4, "pantalla": "Confirmación", "accion": "Ver mensaje de éxito", "emocion": "Satisfacción" }
  ],
  "resultadoEsperado": "Usuario recibe acceso inmediato al contenido premium"
}
```

## Errores comunes
- **Confundir journey con flujo de tareas:** el journey incluye contexto y emociones, no solo pasos funcionales.  
- **Demasiado detalle:** saturar el mapa con información irrelevante dificulta la toma de decisiones; enfóquese en los momentos críticos.  
- **Olvidar validar con usuarios reales:** sin feedback, el journey puede basarse en suposiciones; realice pruebas de usabilidad tempranas.

## Estado actual
Los fundamentos de los User Journeys (escenarios, puntos de contacto y objetivos) son estables y ampliamente adoptados en procesos de diseño centrado en el usuario. En la práctica moderna se complementan con datos de analítica y técnicas de Service Design para crear mapas más ricos y accionables.

## Conexiones
- **User Research:** provee los escenarios y motivaciones que alimentan los journeys.  
- **Personas & User Models:** ofrecen los arquetipos que viven los journeys, asegurando que los puntos de contacto reflejen comportamientos reales.  
- **User Needs & Problems:** los journeys revelan dónde aparecen necesidades no satisfechas y oportunidades de solución.

## Ruta de estudio
1. **Prerequisitos:** comprender métodos de User Research (entrevistas, encuestas) y crear Personas.  
2. **Fundamentos:** aprender a estructurar escenarios y mapear puntos de contacto.  
3. **Práctica:** diseñar journeys para al menos tres flujos críticos de un producto real y validar con pruebas de usabilidad.  
4. **Avanzado:** integrar métricas de analítica y aplicar técnicas de Service Blueprint para conectar journeys con procesos internos.

## Preguntas de repaso
1. ¿Qué diferencia hay entre un User Journey y un simple flujo de tareas?  
2. ¿Cómo se utilizan las emociones y fricciones dentro de un journey?  
3. ¿En qué momento del proceso de diseño es más útil crear un User Journey?  
4. ¿Qué información de analítica puede enriquecer un journey avanzado?  
5. ¿Cómo se relaciona un User Journey con las Personas creadas en la fase de investigación?

<!-- trazabilidad: run_id=run-20261106-201718-f14d02 concept=08-ux-ui-05-user-journeys written_at=2026-11-06T23:17:53.043896+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/02 - User Research|User Research]]
- [[08 - UX & UI/03 - User Needs & Problems|User Needs & Problems]]
- [[08 - UX & UI/04 - Personas & User Models|Personas & User Models]]
- [[09 - Product Management/03 - User Research|User Research]] · *Product Management*
- [[09 - Product Management/05 - User Personas|User Personas]] · *Product Management*

---
← [[08 - UX & UI/04 - Personas & User Models|Personas & User Models]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/06 - Information Architecture|Information Architecture]] →
