---
title: "Dependencies"
area: "Project Management"
numero: 7
aliases: ["Dependencies"]
tags: [concepto, it/project-management]
---
# Dependencies

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 7 de 25**

## Qué abarca
- Relaciones entre tareas y equipos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo las **dependencies** para ordenar las actividades del proyecto de modo que cada tarea empiece sólo cuando sus predecesoras estén terminadas, evitando bloqueos y retrasos inesperados. Resuelvo el problema de coordinación entre equipos que dependen de entregas parciales, garantizando que la planificación refleje la realidad operativa. Aparecen en la fase de planificación y durante la actualización del cronograma, cuando ajusto fechas y recursos. Después de comprenderlas, puedo diseñar cronogramas más fiables, anticipar cuellos de botella y comunicar riesgos de forma clara. No necesito preocuparme por ellas cuando el proyecto es tan pequeño que todas las tareas se ejecutan en paralelo o cuando el alcance está totalmente definido y no hay interdependencias técnicas.

## Esqueleto (el 20% esencial)
1. **Identificación de predecesoras y sucesoras** – Cada tarea se enlaza con las que necesita antes de iniciar.  
2. **Tipo de dependencia** – Finish‑to‑Start (FS) es la más común; existen también Start‑to‑Start (SS), Finish‑to‑Finish (FF) y Start‑to‑Finish (SF).  
3. **Impacto en la planificación** – Las dependencias determinan la ruta crítica y la holgura disponible.  
4. **Gestión de cambios** – Modificar una dependencia implica re‑calcular fechas y recursos.  

## Como funciona
1. Al desglosar el proyecto en la **Work Breakdown Structure**, asigno un identificador a cada paquete de trabajo.  
2. En la herramienta de **Task Management**, establezco para cada tarea su predecesora(s) según el flujo de trabajo real.  
3. Selecciono el tipo de dependencia (FS, SS, etc.) que mejor refleja la interacción entre equipos.  
4. El motor de **Scheduling** calcula fechas de inicio y fin, resaltando la **ruta crítica**.  
5. Cuando surge un cambio (re‑estimación o retraso), actualizo la dependencia y el cronograma se reajusta automáticamente.

## Detalles
- **Básico**: reconocer que una tarea no puede comenzar hasta que otra finalice (FS).  
- **Intermedio**: usar SS para actividades que pueden ejecutarse en paralelo una vez iniciada la predecesora, o FF para entregas que deben concluir simultáneamente.  
- **Avanzado**: combinar varios tipos en una red compleja, aplicar **lag** (retardo) y **lead** (anticipación) para modelar tiempos de espera o solapamiento, y analizar la ruta crítica con técnicas de **Critical Path Method**.

## Ejemplo minimo
```yaml
tasks:
  - id: 1
    name: "Diseñar arquitectura"
    duration: 5d
  - id: 2
    name: "Desarrollar módulo A"
    duration: 8d
    depends_on:
      - id: 1
        type: FS   # solo empieza cuando la arquitectura está terminada
  - id: 3
    name: "Pruebas de integración"
    duration: 4d
    depends_on:
      - id: 2
        type: FS
```

## Errores comunes
- **Asumir que todas las dependencias son FS** → genera planes inflexibles; revisar si SS o FF son más adecuados.  
- **Olvidar lag/lead** → subestima tiempos de espera entre entregas; añadir márgenes explícitos.  
- **No actualizar dependencias tras cambios** → el cronograma queda desalineado; re‑evaluar siempre que se modifique una tarea.

## Estado actual
Las dependencias siguen siendo un pilar estable de la gestión de proyectos; la mayoría de las herramientas de planificación (MS Project, Jira, Primavera) implementan los cuatro tipos clásicos y permiten lag/lead. En la práctica moderna, se complementan con **visualizaciones de red** y análisis de riesgo automatizado, pero el concepto básico no ha cambiado.

## Conexiones
- **Work Breakdown Structure**: la WBS provee la lista jerárquica de entregables que luego se convierten en tareas con dependencias.  
- **Estimation**: una estimación precisa de duración es necesaria para que las dependencias produzcan un cronograma realista.  
- **Planning**: las dependencias son el esqueleto que transforma la planificación estratégica en un calendario operativo.

## Ruta de estudio
1. **Prerequisitos**: comprender la WBS y los fundamentos de estimación de duración.  
2. **Fundamentos**: estudiar los cuatro tipos de dependencia y practicar con ejemplos simples en una herramienta de scheduling.  
3. **Intermedio**: aprender a aplicar lag/lead y a identificar la ruta crítica.  
4. **Avanzado**: integrar dependencias en gestión de riesgos, usar análisis de Monte Carlo y explorar plugins de visualización de redes.  
5. **Aplicación**: crear y mantener un cronograma completo en un proyecto real, revisando y ajustando dependencias en cada fase de control.

## Preguntas de repaso
1. ¿Qué diferencia hay entre una dependencia Finish‑to‑Start y una Start‑to‑Start?  
2. ¿Cómo afecta una dependencia mal definida a la ruta crítica del proyecto?  
3. ¿En qué situaciones es útil introducir un lag entre dos tareas?  
4. ¿Qué pasos seguirías para actualizar el cronograma después de que una tarea predecesora se retrase?  
5. ¿Por qué es importante revisar las dependencias al cerrar la fase de estimación?

<!-- trazabilidad: run_id=run-20261109-171339-bda33e concept=10-project-management-07-dependencies written_at=2026-11-09T20:14:52.893306+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/05 - Work Breakdown Structure|Work Breakdown Structure]]
- [[10 - Project Management/06 - Task Management|Task Management]]
- [[10 - Project Management/08 - Estimation|Estimation]]
- [[10 - Project Management/09 - Planning|Planning]]
- [[10 - Project Management/10 - Scheduling|Scheduling]]

---
← [[10 - Project Management/06 - Task Management|Task Management]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/08 - Estimation|Estimation]] →
