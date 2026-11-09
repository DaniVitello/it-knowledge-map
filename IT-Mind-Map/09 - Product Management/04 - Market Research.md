---
title: "Market Research"
area: "Product Management"
numero: 4
aliases: ["Market Research"]
tags: [concepto, it/product-management]
---
# Market Research

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 4 de 25**

## Qué abarca
- Mercado
- competidores
- alternativas

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Market Research para entender el contexto del mercado en el que mi producto compite, identificar oportunidades y riesgos antes de invertir en desarrollo. Resuelvo la incertidumbre sobre quiénes son los clientes potenciales, qué alternativas existen y cómo se posicionan los competidores, lo que me permite priorizar funcionalidades y definir una propuesta de valor clara. Aparece en la fase de descubrimiento y en los checkpoints de validación de hipótesis, cuando debo decidir si seguir adelante con una idea o pivotar. Después de dominarlo, puedo diseñar estrategias de entrada al mercado, fijar precios y planificar roadmaps con mayor confianza. No necesito preocuparme por Market Research cuando el producto ya está consolidado y la estrategia de crecimiento se basa en métricas de uso interno y optimización de la experiencia existente.

## Esqueleto (el 20% esencial)
1. **Entender el mercado** – Analizo el tamaño, crecimiento y segmentación para saber cuántos usuarios potenciales existen.  
2. **Mapear competidores y alternativas** – Identifico quiénes ya resuelven el problema y qué propuestas ofrecen.  
3. **Detectar brechas de valor** – Cruzo la información del mercado y la competencia para encontrar necesidades no satisfechas.  
4. **Validar hipótesis con datos** – Uso fuentes externas (informes, bases públicas) para confirmar o refutar supuestos iniciales.  
5. **Priorizar oportunidades** – Convierto los hallazgos en criterios de priorización que alimentan el backlog.

## Como funciona
1. Defino la pregunta de negocio (p. ej., “¿Existe un segmento de usuarios que necesite una solución de gestión de tiempo offline?”).  
2. Recolecto datos de fuentes secundarias: informes de industria, bases de datos públicas y análisis de competidores.  
3. Segmento el mercado según criterios relevantes (tamaño de empresa, perfil demográfico, comportamiento).  
4. Construyo un mapa competitivo que muestra fortalezas y debilidades de cada alternativa.  
5. Identifico brechas donde mi propuesta puede aportar mayor valor y asigno un puntaje de oportunidad.  
6. Presento los resultados al equipo de producto y utilizo el puntaje para decidir qué hipótesis pasar a pruebas de usuario.

## Detalles
- **Básico:** foco en datos cuantitativos de mercado (tamaño, CAGR) y listado de competidores principales.  
- **Intermedio:** incorporación de análisis cualitativo (reviews, estudios de caso) y creación de “buyer personas” basadas en la segmentación.  
- **Avanzado:** uso de modelos de “total addressable market” (TAM), “serviceable obtainable market” (SOM) y análisis de “blue‑ocean” para diseñar estrategias de diferenciación y pricing.

## Ejemplo minimo
```python
# Estimación rápida de TAM usando datos públicos de población y adopción esperada
poblacion_total = 50_000_000          # usuarios potenciales en el país
tasa_adopcion = 0.07                  # 7 % estimado de adopción en el primer año
tam = poblacion_total * tasa_adopcion
print(f"TAM estimado: {tam:,} usuarios")
```

## Errores comunes
- **Confundir tamaño de mercado con demanda real.** Evitarlo validando la intención de compra con encuestas o pruebas piloto.  
- **Depender solo de fuentes secundarias sin triangulación.** Complementar con entrevistas a expertos o usuarios.  
- **Ignorar la evolución del mercado.** Actualizar el research periódicamente para capturar cambios de tendencia.

## Estado actual
- **Fundamentos estables:** la práctica de segmentar mercado, mapear competidores y calcular TAM sigue siendo la base aceptada en product management.  
- **Práctica moderna:** se complementa con herramientas de scraping automatizado, análisis de datos en tiempo real y dashboards de inteligencia competitiva que permiten iterar el research de forma continua.

## Conexiones
- **Product Thinking** – El Market Research alimenta la mentalidad de construir productos que resuelvan problemas reales del mercado, no solo ideas internas.  
- **Problem Discovery** – Provee la evidencia externa necesaria para validar que el problema identificado por los usuarios es suficientemente amplio y no está ya cubierto.  
- **User Research** – Los hallazgos de mercado guían los objetivos y la muestra de los estudios de usuarios, asegurando que se investiguen los segmentos más relevantes.

## Ruta de estudio
1. **Prerequisitos:** conceptos básicos de segmentación de clientes y métricas de mercado (TAM, SAM, SOM).  
2. **Fundamentos:** leer guías de investigación de mercado para product managers, practicar con fuentes públicas (e.g., Statista, informes gubernamentales).  
3. **Intermedio:** aprender a usar herramientas de análisis competitivo (SimilarWeb, Crunchbase) y a crear mapas de posicionamiento.  
4. **Avanzado:** dominar técnicas de modelado financiero de mercado y automatizar la recolección de datos con APIs.  
5. **Después:** aplicar los insights a la definición de roadmap, pricing y estrategias de go‑to‑market; profundizar en User Research para validar hipótesis surgidas del market research.

## Preguntas de repaso
1. ¿Qué información del mercado me permite decidir si una idea merece pasar a la fase de prototipo?  
2. ¿Cómo se diferencia un análisis de competidores de un estudio de usuarios?  
3. ¿Qué métricas utilizo para estimar el TAM y por qué son importantes?  
4. ¿Cuál es el riesgo de basar una decisión de producto únicamente en fuentes secundarias?  
5. ¿De qué manera el Market Research influye en la priorización del backlog?

<!-- trazabilidad: run_id=run-20261106-204543-b1e774 concept=09-product-management-04-market-research written_at=2026-11-06T23:46:20.528294+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/01 - Product Thinking|Product Thinking]]
- [[09 - Product Management/02 - Problem Discovery|Problem Discovery]]
- [[09 - Product Management/03 - User Research|User Research]]

---
← [[09 - Product Management/03 - User Research|User Research]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/05 - User Personas|User Personas]] →
