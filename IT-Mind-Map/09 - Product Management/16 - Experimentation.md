---
title: "Experimentation"
area: "Product Management"
numero: 16
aliases: ["Experimentation"]
tags: [concepto, it/product-management]
---
# Experimentation

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 16 de 25**

## Qué abarca
- Experimentos
- hipótesis
- A/B testing

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la experimentación para validar hipótesis de forma rápida y con riesgo controlado, transformando ideas vagas en decisiones basadas en datos. Resuelvo la incertidumbre que surge al priorizar funcionalidades o cambios de UI, evitando inversiones en soluciones que no generan valor. En mi día a día como product manager senior, la experimentación aparece cuando necesito decidir entre dos versiones de una pantalla, probar una nueva regla de precios o confirmar si una mejora de onboarding reduce la tasa de abandono. Después de dominarla, puedo diseñar roadmaps más seguros y comunicar resultados con evidencia cuantitativa. Cuando el producto está en fase de madurez y los cambios son marginales, la experimentación puede quedar en segundo plano y enfocarse en mantenimiento o escalado.

## Esqueleto (el 20% esencial)
1. **Hipótesis clara** – una afirmación medible que explica el impacto esperado de una variante.  
2. **Diseño de experimento** – selección del tipo (A/B test, multivariante) y definición de métricas de éxito.  
3. **Muestreo y ejecución** – lanzar la variante a un segmento representativo y recoger datos.  
4. **Análisis y decisión** – comparar resultados con criterios estadísticos y actuar según el ganador.  
5. **Iteración** – usar lo aprendido para refinar la hipótesis o generar nuevas pruebas.

## Como funciona
1. Identifico una duda concreta del producto y la convierto en una hipótesis medible.  
2. Elijo el método de experimentación (p. ej., A/B test) y determino la población de usuarios que participará.  
3. Configuro la variante (A = control, B = cambio) y establezco métricas clave (conversiones, tiempo en pantalla, churn).  
4. Lanzo el experimento, garantizando que el tráfico se distribuya aleatoriamente y que la duración sea suficiente para alcanzar significancia estadística.  
5. Al cerrar el experimento, analizo los resultados, verifico la hipótesis y tomo una decisión: adoptar, descartar o iterar.

## Detalles
- **Básico:** formular hipótesis simples (p. ej., “un botón más grande aumentará el click‑through en 5 %”).  
- **Intermedio:** diseñar experimentos multivariantes para probar combinaciones de cambios y usar herramientas de segmentación para validar efectos en sub‑poblaciones.  
- **Avanzado:** aplicar técnicas de experimentación bayesiana, ajustar el tamaño de muestra en tiempo real y combinar resultados de experimentos con modelos de atribución para decisiones de producto a nivel de roadmap.

## Ejemplo minimo
```python
# Pseudocódigo de un A/B test con Python y una librería de experimentación
import random
import pandas as pd

def assign_variant(user_id):
    return 'B' if random.random() < 0.5 else 'A'

def run_experiment(data):
    # data: DataFrame con columnas user_id, variant, conversion (0/1)
    results = data.groupby('variant')['conversion'].mean()
    lift = results['B'] - results['A']
    print(f"Lift B vs A: {lift:.2%}")

# Simulación de 1000 usuarios
users = pd.DataFrame({
    'user_id': range(1000),
    'variant': [assign_variant(i) for i in range(1000)],
    'conversion': [random.random() < (0.12 if assign_variant(i)=='B' else 0.10) for i in range(1000)]
})

run_experiment(users)
```

## Errores comunes
- **Hipótesis vaga:** evita definir métricas claras; reformula con un número concreto.  
- **Muestreo insuficiente:** no esperes a alcanzar significancia; calcula el tamaño de muestra antes de lanzar.  
- **Contaminación de grupos:** no permitas que usuarios vean ambas variantes; usa segmentación aleatoria estricta.  
- **Sobrecargar métricas:** enfócate en una o dos KPIs principales para evitar decisiones contradictorias.  
- **Ignorar resultados negativos:** documenta aprendizajes aunque la variante pierda.

## Estado actual
- **Fundamentos estables:** la formulación de hipótesis, el uso de A/B testing y la interpretación basada en significancia estadística son prácticas consolidadas.  
- **Práctica moderna:** adopción creciente de experimentación bayesiana, integración de experimentos en pipelines de CI/CD y uso de plataformas de experimentación que permiten pruebas en tiempo real y segmentación dinámica.

## Conexiones
- **Product Discovery:** la experimentación convierte ideas surgidas en la fase de descubrimiento en evidencia cuantitativa antes de comprometer recursos.  
- **MVP:** los experimentos ayudan a definir el alcance mínimo viable al validar qué funcionalidades generan el mayor impacto temprano.  
- **Data Analytics:** el análisis de resultados depende de técnicas de analítica para interpretar métricas, segmentar usuarios y estimar significancia.

## Ruta de estudio
1. **Prerequisitos:** conceptos básicos de métricas de producto, estadística descriptiva y herramientas de tracking.  
2. **Fundamentos:** leer guías de diseño de A/B tests, aprender a calcular tamaños de muestra y practicar con datasets simulados.  
3. **Intermedio:** explorar experimentación multivariante y segmentación, usar plataformas como Optimizely o Firebase A/B Testing.  
4. **Avanzado:** estudiar experimentación bayesiana, integración CI/CD y casos de uso de experimentos a escala de empresa.  
5. **Aplicación:** liderar un experimento real, presentar resultados al equipo y alimentar el roadmap con los hallazgos.

## Preguntas de repaso
1. ¿Cómo convierto una duda del producto en una hipótesis medible?  
2. ¿Qué criterios utilizo para decidir el tamaño de muestra de un A/B test?  
3. ¿Cuál es la diferencia entre un experimento A/B y uno multivariante?  
4. ¿Cómo debo actuar si el experimento muestra una diferencia no significativa?  
5. ¿De qué manera la experimentación influye en la definición de un MVP?

<!-- trazabilidad: run_id=run-20261109-163529-ca0a5b concept=09-product-management-16-experimentation written_at=2026-11-09T19:36:44.046706+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/14 - Product Discovery|Product Discovery]]
- [[09 - Product Management/15 - MVP|MVP]]

---
← [[09 - Product Management/15 - MVP|MVP]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/17 - Product Metrics|Product Metrics]] →
