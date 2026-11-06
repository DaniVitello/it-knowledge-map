---
title: "Data Visualization"
area: "Database / Data Analytics"
numero: 23
aliases: ["Data Visualization"]
tags: [concepto, it/database-data-analytics]
---
# Data Visualization

> **Área:** [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · **Concepto 23 de 25**

## Qué abarca
- Charts
- dashboards
- visual encoding

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la visualización de datos para transformar resultados de consultas y análisis en representaciones gráficas que facilitan la detección de patrones, tendencias y anomalías. Resuelvo el problema de comunicar información compleja a equipos técnicos y de negocio sin que tengan que interpretar tablas extensas. En mi día a día como ingeniero de datos y analista senior, la visualización aparece al crear dashboards de monitoreo de pipelines, al presentar métricas de calidad de datos y al apoyar decisiones basadas en KPIs. Después de dominarla, puedo diseñar informes interactivos, automatizar la generación de gráficos y combinar visualizaciones con alertas. No necesito preocuparme cuando el consumo es exclusivamente programático (por ejemplo, una API que entrega JSON) y la audiencia no requiere interpretación visual.

## Esqueleto (el 20% esencial)
1. **Charts** – Selección del tipo de gráfico (barras, líneas, dispersión) que mejor representa la distribución o evolución de los datos.  
2. **Dashboards** – Agrupación de varios charts en una vista única para monitorear métricas clave en tiempo real.  
3. **Visual encoding** – Mapeo de atributos (color, tamaño, posición) a variables del dataset para transmitir información de forma intuitiva.  
4. **Interactividad** – Herramientas como filtros y tooltips que permiten al usuario explorar los datos sin volver a ejecutar consultas.  
5. **Consistencia** – Uso de paletas y escalas coherentes para evitar confusión y mantener la jerarquía visual.

## Como funciona
1. **Definir la pregunta** que se quiere responder (p. ej., “¿Cuál es el churn mensual por segmento?”).  
2. **Extraer los datos** mediante una consulta SQL o un proceso ETL que entregue un dataset estructurado.  
3. **Elegir el chart** cuyo visual encoding represente mejor la variable objetivo (tiempo → eje X, churn → eje Y, segmento → color).  
4. **Configurar el dashboard**, colocando el chart junto a otros indicadores relacionados (tasa de retención, NPS).  
5. **Agregar interactividad** (filtros por región, tooltips con valores exactos) para que el analista pueda profundizar sin volver a la base.  
6. **Publicar o compartir** el dashboard, permitiendo que stakeholders tomen decisiones basadas en la visualización.

## Detalles
- **Básico:** Uso de bibliotecas como Matplotlib o Seaborn para crear gráficos estáticos a partir de DataFrames.  
- **Intermedio:** Implementación de dashboards con Plotly Dash o Power BI, donde se conectan consultas parametrizadas y se habilitan filtros.  
- **Avanzado:** Integración de visualizaciones en tiempo real mediante streaming de datos (Kafka → Spark Structured Streaming → Grafana) y aplicación de técnicas de visual encoding perceptualmente óptimas (escala logarítmica, codificación de color divergente).

## Ejemplo minimo
```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Consulta simulada
df = pd.read_sql(
    "SELECT month, churn_rate FROM churn_monthly WHERE year = 2023",
    con=engine
)

# 2. Chart simple
plt.figure(figsize=(6,4))
plt.plot(df['month'], df['churn_rate'], marker='o', color='steelblue')
plt.title('Churn mensual 2023')
plt.xlabel('Mes')
plt.ylabel('Tasa de churn (%)')
plt.grid(True)
plt.show()
```

## Errores comunes
- **Elegir un chart inadecuado** (p. ej., usar pastel para comparar valores similares). *Evitarlo analizando la naturaleza de la variable antes de graficar.*  
- **Sobrecargar el dashboard** con demasiados gráficos. *Mantener la jerarquía visual y limitar a métricas clave.*  
- **Ignorar la escala** (eje truncado que distorsiona tendencias). *Usar límites y marcas que reflejen la distribución real.*  

## Estado actual
- **Fundamentos estables:** Los principios de visual encoding y la necesidad de elegir el tipo de chart adecuado siguen siendo válidos.  
- **Práctica moderna:** Herramientas de visual analytics como Tableau, Power BI y soluciones open‑source (Superset, Metabase) dominan la creación de dashboards interactivos; la integración con pipelines de datos en tiempo real está en expansión.

## Conexiones
- **Data Analysis** – La visualización es la capa final que comunica los hallazgos obtenidos durante el análisis de datos.  
- **BI & Reporting** – Los dashboards de visualización son componentes centrales de las soluciones de Business Intelligence para la toma de decisiones.  
- **Visual Hierarchy** – La organización de colores, tamaños y posiciones en un gráfico sigue los principios de jerarquía visual para guiar la atención del usuario.

## Ruta de estudio
1. **Prerequisitos:** SQL básico, manipulación de datos con pandas, conceptos de estadística descriptiva.  
2. **Fundamentos:** Aprender Matplotlib/Seaborn, entender tipos de charts y sus usos.  
3. **Intermedio:** Construir dashboards con Plotly Dash o Power BI, practicar filtros y tooltips.  
4. **Avanzado:** Integrar visualizaciones en pipelines de streaming, aplicar principios de percepción visual y optimizar rendimiento de renderizado.  

## Preguntas de repaso
1. ¿Qué tipo de chart elegirías para comparar la distribución de valores entre varios segmentos y por qué?  
2. ¿Cómo afecta la elección de una escala logarítmica al interpretar tendencias de crecimiento rápido?  
3. ¿Cuál es la ventaja de usar filtros interactivos en un dashboard frente a ejecutar consultas separadas?  
4. Describe un caso donde un pastel sería una visualización inadecuada.  
5. ¿Qué pasos seguirías para conectar una consulta SQL a un gráfico en tiempo real dentro de un dashboard?

<!-- trazabilidad: run_id=run-20261105-194852-06b315 concept=04-database-data-analytics-23-data-visualization written_at=2026-11-05T23:07:17.264647+00:00 -->
<!-- ai:end -->

## Relacionados
- [[04 - Database & Data Analytics/20 - Data Analysis|Data Analysis]]
- [[04 - Database & Data Analytics/21 - Statistics|Statistics]]
- [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]]
- [[04 - Database & Data Analytics/24 - BI & Reporting|BI & Reporting]]
- [[08 - UX & UI/12 - Visual Hierarchy|Visual Hierarchy]] · *UX / UI*

---
← [[04 - Database & Data Analytics/22 - Analytics Metrics|Analytics Metrics]] · [[04 - Database & Data Analytics/00 - Índice Database - Data Analytics|Índice Database / Data Analytics]] · [[04 - Database & Data Analytics/24 - BI & Reporting|BI & Reporting]] →
