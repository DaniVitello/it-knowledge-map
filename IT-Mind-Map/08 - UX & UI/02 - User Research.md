---
title: "User Research"
area: "UX / UI"
numero: 2
aliases: ["User Research"]
tags: [concepto, it/ux-ui]
---
# User Research

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 2 de 25**

## Qué abarca
- Entrevistas
- observación
- encuestas
- investigación cualitativa/cuantitativa

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la User Research para comprender quiénes son los usuarios, qué necesitan y cómo se comportan en su contexto real. Resuelvo la incertidumbre que surge al diseñar interfaces sin datos de campo, evitando suposiciones que pueden generar fricción o abandono. Aparece en la fase inicial del proceso de diseño de producto, cuando defino problemas, establezco prioridades y creo bases sólidas para las decisiones de UX. Después de dominarla, puedo traducir insights en requisitos, validar hipótesis y medir el impacto de los cambios. Cuando el producto ya está validado y los usuarios son estables, la investigación intensiva puede reducirse a pruebas de usabilidad puntuales.

## Esqueleto (el 20% esencial)
1. **Entrevistas** – conversaciones estructuradas que revelan motivaciones, frustraciones y expectativas del usuario.  
2. **Observación** – registro del comportamiento real del usuario en su entorno, detectando patrones que no se expresan verbalmente.  
3. **Encuestas** – instrumentos cuantitativos que permiten medir la prevalencia de necesidades y actitudes en grandes audiencias.  
4. **Investigación cualitativa** – análisis profundo de respuestas abiertas y narrativas para identificar temas emergentes.  
5. **Investigación cuantitativa** – uso de métricas y estadísticas para validar hipótesis y priorizar problemas.

## Como funciona
1. **Defino objetivos** alineados al proyecto (p.ej., validar una hipótesis de flujo).  
2. **Selecciono métodos** (entre entrevistas, observación y encuestas) según el tipo de insight que busco.  
3. **Recluto participantes** que representen los segmentos de usuarios relevantes.  
4. **Recolecto datos** aplicando guías de entrevista, protocolos de observación o cuestionarios estructurados.  
5. **Analizo resultados** agrupando hallazgos cualitativos y cuantitativos, extrayendo patrones y prioridades.  
6. **Comunico insights** mediante artefactos (personas, mapas de empatía, reportes) que alimentan la toma de decisiones de diseño.

## Detalles
- **Básico:** Aprender a redactar guías de entrevista y preguntas de encuesta; practicar la observación en entornos de baja complejidad.  
- **Intermedio:** Aplicar técnicas de codificación temática, crear matrices de afinidad y combinar datos cualitativos con métricas cuantitativas para priorizar problemas.  
- **Avanzado:** Ejecutar estudios longitudinales, usar herramientas de análisis estadístico (p.ej., análisis de regresión) y diseñar experimentos controlados (A/B testing) que cierren el ciclo de investigación‑diseño‑evaluación.

## Ejemplo minimo
```json
{
  "survey": {
    "title": "Satisfacción del flujo de checkout",
    "questions": [
      {"id": 1, "type": "rating", "text": "¿Qué tan fácil fue completar la compra?"},
      {"id": 2, "type": "text", "text": "¿Qué problema encontraste, si alguno?"}
    ]
  }
}
```
Este JSON representa la mínima encuesta que se puede lanzar a usuarios después de una transacción para obtener datos cuantitativos y cualitativos rápidamente.

## Errores comunes
- **Preguntar “¿Te gusta?”** en lugar de indagar sobre tareas y contextos; evita preguntas demasiado abiertas.  
- **Seleccionar una muestra no representativa**; asegura diversidad de perfiles antes de iniciar.  
- **Interpretar anecdóticos como tendencias**; valida con datos cuantitativos antes de priorizar.  
- **No cerrar el ciclo**; siempre lleva los insights a prototipos o decisiones de diseño.  

## Estado actual
**Fundamentos estables:** Las entrevistas, observación y encuestas siguen siendo pilares para obtener insights de usuarios. La combinación de métodos cualitativos y cuantitativos es una práctica consolidada.  
**Práctica moderna:** Se favorece el uso de herramientas digitales de reclutamiento y análisis automático (p.ej., análisis de sentimiento), así como la integración de datos de comportamiento en tiempo real (event tracking) para complementar la investigación tradicional.

## Conexiones
- **User Needs & Problems:** La investigación revela necesidades latentes y problemas concretos que guían la definición de requisitos.  
- **Personas & User Models:** Los insights se sintetizan en personas, proporcionando arquetipos que facilitan la comunicación dentro del equipo.  
- **User Journeys:** Los hallazgos alimentan los mapas de viaje, mostrando puntos de dolor y oportunidades a lo largo del flujo de interacción.

## Ruta de estudio
1. **Prerequisitos:** Conocer los principios básicos de UX, saber formular preguntas de investigación y manejar herramientas de captura de datos (Google Forms, miro).  
2. **Fundamentos:** Realizar entrevistas y observaciones simples; crear encuestas y analizar respuestas con hojas de cálculo.  
3. **Intermedio:** Aprender codificación temática, usar software de análisis cualitativo (Dovetail) y aplicar estadística descriptiva.  
4. **Avanzado:** Dominar estudios longitudinales, análisis de correlación, experimentación A/B y visualización de insights en dashboards interactivos.  
5. **Especialización:** Integrar investigación de usuarios con métricas de producto (KPIs) y metodologías de Design Ops.

## Preguntas de repaso
1. ¿Qué diferencia a la investigación cualitativa de la cuantitativa y cuándo se combina cada una?  
2. ¿Cómo seleccionas a los participantes para una entrevista que sea representativa del público objetivo?  
3. ¿Qué pasos sigues para transformar hallazgos de observación en una persona útil para el equipo?  
4. ¿Cuál es el riesgo de basar decisiones de diseño solo en datos anecdóticos y cómo lo mitigas?  
5. ¿En qué situaciones puedes reducir la intensidad de la User Research y enfocarte en pruebas de usabilidad puntuales?

<!-- trazabilidad: run_id=run-20261106-201433-5b426c concept=08-ux-ui-02-user-research written_at=2026-11-06T23:15:38.116098+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/03 - User Needs & Problems|User Needs & Problems]]
- [[08 - UX & UI/04 - Personas & User Models|Personas & User Models]]
- [[08 - UX & UI/05 - User Journeys|User Journeys]]
- [[09 - Product Management/03 - User Research|User Research]] · *Product Management*
- [[09 - Product Management/05 - User Personas|User Personas]] · *Product Management*

---
← [[08 - UX & UI/01 - Human-Centered Design|Human-Centered Design]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/03 - User Needs & Problems|User Needs & Problems]] →
