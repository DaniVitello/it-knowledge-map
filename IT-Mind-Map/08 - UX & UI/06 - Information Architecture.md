---
title: "Information Architecture"
area: "UX / UI"
numero: 6
aliases: ["Information Architecture"]
tags: [concepto, it/ux-ui]
---
# Information Architecture

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 6 de 25**

## Qué abarca
- Organización y jerarquía de información

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la arquitectura de información para estructurar y jerarquizar todo el contenido que aparecerá en una interfaz, de modo que los usuarios encuentren lo que buscan con el menor esfuerzo cognitivo. Resuelvo la confusión que surge cuando la información está dispersa o sin orden lógico, garantizando que cada elemento tenga su lugar dentro del flujo del producto. Aparece en cada fase del diseño de producto senior: desde la definición de la estructura del sitio o la app, pasando por la creación de wireframes, hasta la validación de prototipos con usuarios. Cuando entiendo cómo organizar la información, puedo diseñar menús, filtros y rutas de navegación que tengan sentido, y también puedo evaluar si una solución existente está bien estructurada. No necesito preocuparme de la arquitectura de información cuando el proyecto es un micro‑producto con una sola pantalla o cuando el contenido está predefinido por regulaciones que no admiten reordenamiento.

## Esqueleto (el 20% esencial)
1. **Organizar el contenido en grupos lógicos** – agrupo páginas, pantallas o módulos según su temática o función.  
2. **Definir una jerarquía clara** – establezco niveles de importancia que guían la profundidad de la navegación.  
3. **Mapear relaciones entre grupos** – creo conexiones que muestran cómo los usuarios pueden pasar de un grupo a otro.  
4. **Etiquetar de forma consistente** – utilizo nombres que los usuarios reconozcan y que reflejen la estructura.  
5. **Validar con usuarios** – comprobo que la organización propuesta sea intuitiva mediante pruebas tempranas.

## Como funciona
1. **Inventario de contenido**: recolecto todos los elementos de información del producto (páginas, funcionalidades, datos).  
2. **Agrupamiento**: aplico la idea 1 del esqueleto y formo categorías coherentes.  
3. **Jerarquización**: con la idea 2, asigno niveles (principal, secundario, terciario) y determino la profundidad de cada categoría.  
4. **Mapeo de relaciones**: siguiendo la idea 3, dibujo un sitemap o diagramas de flujo que muestren los caminos posibles.  
5. **Etiquetado**: aplico la idea 4 para nombrar cada nodo del mapa con términos familiares.  
6. **Pruebas de usabilidad**: ejecuto la idea 5, observando si los usuarios encuentran lo que buscan sin dificultad.  
7. **Iteración**: ajusto grupos, jerarquías o etiquetas según los hallazgos y repito el ciclo.

## Detalles
- **Básico**: inventario y agrupamiento. Se trata de listar todo y crear carpetas temáticas; suficiente para proyectos pequeños.  
- **Intermedio**: jerarquización y etiquetado. Introduzco niveles de profundidad y pruebo la claridad de los nombres con tarjetas de clasificación.  
- **Avanzado**: mapeo de relaciones y validación continua. Utilizo diagramas de flujo interactivos, pruebas de árbol y análisis de métricas de navegación para refinar la arquitectura en productos complejos.

## Ejemplo minimo
```json
{
  "Home": ["Dashboard", "Notificaciones"],
  "Productos": {
    "Categorías": ["Electrónica", "Ropa", "Hogar"],
    "Detalle": ["Descripción", "Precio", "Opiniones"]
  },
  "Cuenta": ["Perfil", "Pedidos", "Configuración"]
}
```
El JSON anterior muestra una arquitectura de información mínima para una tienda online: grupos principales (Home, Productos, Cuenta) y sus sub‑elementos jerárquicos.

## Errores comunes
- **Crear demasiados niveles** – genera rutas largas y confunde al usuario; mantener la profundidad mínima.  
- **Etiquetas ambiguas** – usan jerga interna; siempre validar con usuarios reales.  
- **Ignorar la retroalimentación** – no ajustar la arquitectura después de pruebas; iterar continuamente.  

## Estado actual
- **Fundamentos estables**: la necesidad de organizar y jerarquizar la información, el uso de inventarios y mapas de sitio, y la validación mediante pruebas de árbol siguen siendo prácticas consolidadas.  
- **Práctica moderna**: se complementa con herramientas de IA para sugerir agrupamientos, análisis de datos de comportamiento real (clickstream) para ajustar la jerarquía, y prototipos interactivos que permiten pruebas de navegación en tiempo real.

## Conexiones
- **Navigation**: la arquitectura de información define la estructura sobre la que se construyen los menús y los patrones de navegación.  
- **User Flows**: los flujos de usuario se dibujan sobre la jerarquía establecida, indicando los pasos que el usuario sigue entre los grupos de información.  
- **Content Strategy**: una estrategia de contenido clara depende de una arquitectura que organice y priorice la información de forma coherente.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de usabilidad, investigación de usuarios y card sorting.  
2. **Fundamentos**: aprender a crear inventarios de contenido y a agrupar información en categorías lógicas.  
3. **Herramientas**: dominar sitemaps, diagramas de flujo y pruebas de árbol (tree testing).  
4. **Avanzado**: explorar análisis de datos de navegación, IA para clustering de contenido y prototipado de arquitectura dinámica.  
5. **Especialización**: aplicar IA en IA (Information Architecture) a productos multicanal y a sistemas de gestión de contenido (CMS) complejos.

## Preguntas de repaso
1. ¿Cómo ayuda la arquitectura de información a reducir la carga cognitiva del usuario?  
2. ¿Qué pasos seguirías para crear una jerarquía clara en un nuevo producto?  
3. ¿Por qué es crítico validar las etiquetas con usuarios reales?  
4. ¿Cuál es la diferencia entre un sitemap y un user flow y cómo se complementan?  
5. ¿Qué riesgos implica una arquitectura con demasiados niveles y cómo los mitigaría?

<!-- trazabilidad: run_id=run-20261106-201753-6b4c09 concept=08-ux-ui-06-information-architecture written_at=2026-11-06T23:18:56.154265+00:00 -->
<!-- ai:end -->

## Relacionados
- [[08 - UX & UI/07 - Navigation|Navigation]]
- [[08 - UX & UI/09 - User Flows|User Flows]]

---
← [[08 - UX & UI/05 - User Journeys|User Journeys]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/07 - Navigation|Navigation]] →
