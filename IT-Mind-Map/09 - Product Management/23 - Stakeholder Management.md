---
title: "Stakeholder Management"
area: "Product Management"
numero: 23
aliases: ["Stakeholder Management"]
tags: [concepto, it/product-management]
---
# Stakeholder Management

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 23 de 25**

## Qué abarca
- Usuarios
- negocio
- ingeniería
- diseño
- dirección

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Stakeholder Management para alinear a todos los grupos que influyen o se ven afectados por el producto – usuarios, negocio, ingeniería, diseño y dirección – y así tomar decisiones basadas en sus necesidades reales. Resuelvo el problema de la fragmentación de expectativas que genera retrasos, cambios de alcance y falta de foco. Aparece en cada fase del ciclo de vida del producto: al definir la visión, al priorizar el backlog y al validar hipótesis. Después de entenderlo, puedo diseñar canales de comunicación, mapear influencias y negociar compromisos que mantengan el ritmo de entrega. No necesito preocuparme cuando el producto está en modo “maintenance” con requisitos estables y sin cambios estratégicos.

## Esqueleto (el 20% esencial)
1. **Identificación de stakeholders** – reconocer a usuarios, negocio, ingeniería, diseño y dirección que tienen interés o poder de decisión.  
2. **Mapeo de intereses y poder** – clasificar cada stakeholder según su nivel de influencia y sus objetivos críticos.  
3. **Comunicación estructurada** – definir canales, frecuencia y formato de interacción para cada grupo.  
4. **Gestión de expectativas** – acordar entregables, métricas y criterios de éxito que satisfagan a todos.  
5. **Revisión y ajuste continuo** – actualizar el mapa y los planes de comunicación a medida que cambian prioridades.

## Como funciona
1. **Recolectar datos**: entrevistas, surveys y reuniones para listar a todos los stakeholders.  
2. **Clasificar**: usar una matriz de poder‑interés (alto/alto, alto/bajo, bajo/alto, bajo/bajo).  
3. **Diseñar canales**: por ejemplo, demos quincenales para dirección, newsletters mensuales para usuarios, stand‑ups diarios con ingeniería.  
4. **Alinear prioridades**: traducir los objetivos de negocio y de usuarios en historias de usuario y criterios de aceptación.  
5. **Monitorear**: revisar métricas de satisfacción y ajustar el mapa cada sprint o trimestre.

## Detalles
- **Básico**: crear una lista simple de stakeholders y asignar un responsable de contacto.  
- **Intermedio**: aplicar la matriz de poder‑interés, definir RACI (Responsible, Accountable, Consulted, Informed) y establecer un calendario de comunicaciones.  
- **Avanzado**: integrar herramientas de gestión (Jira, Confluence) con dashboards de stakeholder health, usar técnicas de negociación basada en valor y ejecutar workshops de co‑creación para validar roadmaps.

## Ejemplo minimo
```json
{
  "stakeholders": [
    {"grupo":"Usuarios","interes":"Funcionalidad","poder":"Bajo"},
    {"grupo":"Negocio","interes":"Ingresos","poder":"Alto"},
    {"grupo":"Ingeniería","interes":"Escalabilidad","poder":"Alto"},
    {"grupo":"Diseño","interes":"Usabilidad","poder":"Medio"},
    {"grupo":"Dirección","interes":"Visión estratégica","poder":"Alto"}
  ]
}
```
Este JSON representa un mapa rápido que permite decidir que la próxima demo se enfoque en métricas de ingresos (Negocio) y usabilidad (Diseño), mientras que la arquitectura se revisa en el sprint planning con Ingeniería.

## Errores comunes
- **Ignorar a los usuarios finales** → se generan funcionalidades que no resuelven su problema; evitar involucrándolos desde la fase de descubrimiento.  
- **Sobrecargar a la dirección con detalle técnico** → provoca pérdida de foco estratégico; usar resúmenes ejecutivos.  
- **No actualizar el mapa** → decisiones basadas en información obsoleta; programar revisiones periódicas.

## Estado actual
- **Fundamentos estables**: identificación de stakeholders, matriz de poder‑interés y comunicación estructurada siguen siendo prácticas consolidadas.  
- **Práctica moderna**: integración de métricas de salud de stakeholders en dashboards de producto, uso de herramientas de colaboración en tiempo real (Miro, FigJam) para workshops y adopción de enfoques de Design Thinking para co‑creación.

## Conexiones
- **Technical Leadership**: colabora definiendo prioridades técnicas que deben ser comunicadas a los stakeholders de negocio y usuarios.  
- **Roadmapping**: el mapa de stakeholders alimenta la construcción de roadmaps alineados con expectativas y restricciones.  
- **Data‑Driven Decision Making**: los indicadores de satisfacción y uso de los stakeholders proveen datos que guían la priorización del backlog.

## Ruta de estudio
1. **Prerequisitos**: conceptos básicos de gestión de productos, metodologías ágiles y técnicas de entrevista.  
2. **Fundamentos**: leer sobre la matriz de poder‑interés y RACI; practicar con casos reales de tu organización.  
3. **Intermedio**: aprender a crear dashboards de stakeholder health en herramientas como Tableau o PowerBI.  
4. **Avanzado**: dominar workshops de co‑creación, negociación basada en valor y la integración de stakeholder metrics en OKR.

## Preguntas de repaso
1. ¿Cómo identificas a los stakeholders críticos en un proyecto de producto digital?  
2. ¿Qué diferencia hay entre poder y interés y cómo influye en la forma de comunicarte con cada grupo?  
3. ¿Cuál es el propósito de establecer un RACI dentro del Stakeholder Management?  
4. ¿Cómo utilizas los indicadores de salud de stakeholders para ajustar el roadmap?  
5. ¿Qué error frecuente genera desalineación entre ingeniería y negocio y cómo lo evitas?

<!-- trazabilidad: run_id=run-20261109-170441-0d3403 concept=09-product-management-23-stakeholder-management written_at=2026-11-09T20:06:27.764077+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/29 - Technical Leadership|Technical Leadership]] · *Software Engineering*
- [[10 - Project Management/21 - Stakeholder Management|Stakeholder Management]] · *Project Management*

---
← [[09 - Product Management/22 - Product Lifecycle|Product Lifecycle]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/24 - Go-to-Market|Go-to-Market]] →
