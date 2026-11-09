---
title: "Usability Testing"
area: "UX / UI"
numero: 22
aliases: ["Usability Testing"]
tags: [concepto, it/ux-ui]
---
# Usability Testing

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 22 de 25**

## Qué abarca
- Tests con usuarios
- tareas
- observación
- hallazgos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el **usability testing** para validar, con usuarios reales, si una interfaz permite cumplir las tareas clave sin fricción. Resuelvo la incertidumbre de que mis decisiones de diseño funcionen en el contexto de uso, detectando problemas de navegación, comprensión y eficiencia antes de lanzar el producto. Aparece en mi flujo de trabajo cuando paso de los prototipos de alta fidelidad a la fase de validación, y me permite priorizar mejoras basadas en evidencia. Después de entenderlo, puedo diseñar pruebas estructuradas, interpretar hallazgos y traducirlos en iteraciones de diseño; cuando el producto ya está en producción y los indicadores de uso son estables, no es necesario volver a ejecutar pruebas exhaustivas a menos que se introduzcan cambios significativos.

## Esqueleto (el 20% esencial)
1. **Definir tareas representativas**: selecciono acciones que los usuarios deben realizar para alcanzar sus objetivos principales.  
2. **Reclutar usuarios reales**: elijo participantes que coincidan con el perfil del público objetivo.  
3. **Observar y registrar**: durante la prueba, capturo comportamientos, comentarios y métricas de desempeño.  
4. **Analizar hallazgos**: identifico patrones de error, tiempos de ejecución y niveles de satisfacción.  
5. **Iterar el diseño**: convierto los insights en cambios concretos y los vuelvo a validar.

## Como funciona
1. **Planificación** – a partir del mapa de flujo de usuario, determino las tareas críticas y los criterios de éxito.  
2. **Reclutamiento** – contacto a usuarios que representen los arquetipos definidos y les explico el objetivo de la prueba.  
3. **Ejecución** – los usuarios realizan cada tarea mientras yo (o un moderador) observo, toma notas y registra tiempos y errores.  
4. **Captura de datos** – utilizo grabaciones de pantalla, métricas de tiempo y cuestionarios post‑prueba para complementar la observación.  
5. **Síntesis** – agrupo los hallazgos en problemas de usabilidad, priorizándolos por impacto y frecuencia.  
6. **Iteración** – propongo soluciones de diseño, actualizo el prototipo y repito el ciclo si es necesario.

## Detalles
- **Básico**: pruebas de guerrilla con 3‑5 usuarios, tareas simples y observación directa.  
- **Intermedio**: sesiones moderadas en laboratorio, uso de métricas como *task success rate* y *time on task*, y aplicación de cuestionarios como SUS.  
- **Avanzado**: pruebas remotas con herramientas de tracking, análisis estadístico de métricas, y combinación con pruebas A/B para validar cambios específicos.

## Ejemplo minimo
```json
{
  "test_id": "UT-001",
  "tarea": "Agregar un producto al carrito",
  "pasos": [
    "Abrir la página de inicio",
    "Buscar el producto 'Camiseta azul'",
    "Seleccionar talla M",
    "Hacer clic en 'Agregar al carrito'"
  ],
  "criterio_exito": true,
  "tiempo_maximo_seg": 120
}
```

## Errores comunes
- **Seleccionar usuarios no representativos** – evita la validez de los hallazgos; verifica el perfil antes de reclutar.  
- **Demasiadas tareas en una sesión** – genera fatiga y datos ruidosos; limita a 3‑4 tareas críticas.  
- **Interpretar comentarios como métricas** – combina observación cualitativa con datos cuantitativos para decisiones equilibradas.  
- **Ignorar hallazgos menores** – pequeños problemas pueden escalar; registra y prioriza todos los incidentes.

## Estado actual
**Fundamentos estables**: la necesidad de observar usuarios reales, definir tareas y analizar errores sigue siendo la base del usability testing.  
**Práctica moderna**: se complementa con pruebas remotas, análisis de métricas de interacción (p. ej., clickstream) y la integración de resultados en sistemas de gestión de producto para seguimiento continuo.

## Conexiones
- **Usability**: el testing es la herramienta principal para medir cuán usable es una interfaz y para identificar oportunidades de mejora.  
- **UX Metrics**: los datos obtenidos (tasa de éxito, tiempo de tarea, SUS) alimentan los indicadores de experiencia de usuario que guían decisiones estratégicas.  
- **User Research**: los hallazgos del testing informan y refinan los insights obtenidos en fases de investigación cualitativa, cerrando el ciclo de descubrimiento‑validación.

## Ruta de estudio
1. **Prerequisitos**: conceptos de *user personas*, *user journeys* y principios básicos de *interaction design*.  
2. **Fundamentos**: leer guías de Nielsen sobre pruebas de usabilidad, practicar con prototipos de baja fidelidad.  
3. **Intermedio**: aprender a usar herramientas de grabación y análisis (e.g., Lookback, UserTesting), aplicar el System Usability Scale (SUS).  
4. **Avanzado**: dominar pruebas remotas, análisis estadístico de métricas, y la integración de resultados en roadmaps de producto.  
5. **Especialización**: explorar pruebas de accesibilidad y pruebas de usabilidad en entornos móviles o de realidad aumentada.

## Preguntas de repaso
1. ¿Qué criterios utilizo para seleccionar las tareas que se probarán en un usability test?  
2. ¿Cómo se combina la observación cualitativa con métricas cuantitativas durante la prueba?  
3. ¿Cuál es la diferencia entre una prueba de guerrilla y una sesión moderada en laboratorio?  
4. ¿Por qué es importante iterar el diseño después de analizar los hallazgos?  
5. ¿Cómo se relaciona el usability testing con los UX Metrics en la toma de decisiones de producto?

<!-- trazabilidad: run_id=run-20261109-163252-bb368b concept=08-ux-ui-22-usability-testing written_at=2026-11-09T19:34:06.180304+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/21 - Usability|Usability]]
- [[08 - UX & UI/23 - UX Metrics|UX Metrics]]

---
← [[08 - UX & UI/21 - Usability|Usability]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/23 - UX Metrics|UX Metrics]] →
