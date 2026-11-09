---
title: "Funnels"
area: "Product Management"
numero: 18
aliases: ["Funnels"]
tags: [concepto, it/product-management]
---
# Funnels

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 18 de 25**

## Qué abarca
- Acquisition → activation → conversion → retention

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los funnels para visualizar y medir cómo los usuarios avanzan desde el primer contacto con el producto hasta que se convierten en clientes recurrentes. Resuelvo la falta de claridad sobre dónde se pierden usuarios y qué acciones pueden revertir esas pérdidas, lo que me permite priorizar mejoras con impacto directo en ingresos. Aparecen en cada fase del ciclo de vida del producto: adquisición, activación, conversión y retención. Después de entender el funnel, puedo diseñar experimentos, asignar recursos y comunicar resultados con datos concretos. No necesito preocuparme por el funnel cuando el producto está en fase de ideación sin usuarios reales o cuando la métrica clave no depende del comportamiento secuencial del usuario.

## Esqueleto (el 20% esencial)
1. **Adquisición** – captar usuarios a través de canales de marketing o referencias.  
2. **Activación** – lograr que el usuario realice la primera acción de valor (p. ej. crear una cuenta).  
3. **Conversión** – transformar la activación en una acción de negocio (pago, suscripción).  
4. **Retención** – mantener al usuario activo y recurrente después de la conversión.  
5. **Iteración** – usar los datos del funnel para identificar cuellos de botella y lanzar mejoras.

## Como funciona
1. Defino los eventos clave que representan cada etapa del funnel.  
2. Configuro la captura de esos eventos en la herramienta de product analytics.  
3. Genero un reporte que muestra el número de usuarios en cada etapa y el porcentaje que avanza al siguiente paso.  
4. Analizo dónde se produce la mayor caída (drop‑off) y formulo hipótesis de mejora.  
5. Priorizo experimentos, los ejecuto, y vuelvo a medir el funnel para validar el impacto.

## Detalles
- **Básico:** identificar eventos, crear un embudo simple y observar tasas de paso.  
- **Intermedio:** segmentar el funnel por origen de tráfico o cohortes para detectar variaciones.  
- **Avanzado:** combinar el funnel con modelos de atribución y pruebas A/B multivariantes, y automatizar alertas cuando una tasa cae bajo umbrales predefinidos.

## Ejemplo minimo
```python
# Calcular tasas de un funnel simple
adquisicion = 1000
activacion = 400
conversion = 150
retencion = 80

def tasa(paso, total):
    return round(paso / total * 100, 1)

print("Tasa de activación:", tasa(activacion, adquisicion), "%")
print("Tasa de conversión:", tasa(conversion, activacion), "%")
print("Tasa de retención:", tasa(retencion, conversion), "%")
```

## Errores comunes
- **Medir eventos equivocados:** elegir métricas que no reflejan valor real; evitarlo alineando cada evento con una acción de negocio.  
- **Ignorar segmentación:** analizar el funnel global oculta problemas específicos de canales; segmentar siempre que sea posible.  
- **No cerrar el bucle:** lanzar mejoras sin volver a medir; siempre re‑evaluar el funnel después de cada cambio.

## Estado actual
**Fundamentos estables:** la estructura de adquisición → activación → conversión → retención sigue siendo la base aceptada para diagnosticar el comportamiento del usuario.  
**Práctica moderna:** se complementa con cohort analysis, análisis de cohortes de retención y dashboards en tiempo real que integran datos de product analytics y experimentación continua.

## Conexiones
- **Product Metrics:** el funnel traduce métricas abstractas (p. ej. CAC, LTV) en pasos observables que facilitan su seguimiento.  
- **Retention:** la última etapa del funnel se solapa con métricas de retención, permitiendo comparar la salud a corto y largo plazo.  
- **Product Analytics:** sin una herramienta de analytics no se pueden capturar los eventos que alimentan el funnel; la integración es esencial para la medición.

## Ruta de estudio
1. **Prerequisitos:** conceptos de eventos, tracking y métricas básicas (p. ej. usuarios activos).  
2. **Fundamentos:** crear un funnel en una herramienta de analytics, interpretar tasas y detectar drop‑offs.  
3. **Intermedio:** segmentar funnels por canal y cohortes, introducir pruebas A/B.  
4. **Avanzado:** combinar funnels con modelos de atribución, automatizar alertas y usar dashboards de monitoring en tiempo real.  
5. **Especialización:** aplicar funnels a productos SaaS, marketplaces o apps móviles, adaptando etapas según el modelo de negocio.

## Preguntas de repaso
1. ¿Qué problema de producto resuelve la visualización de un funnel?  
2. ¿Cómo se determina cuál es la etapa que necesita mayor atención?  
3. ¿Por qué es importante segmentar el funnel por origen de tráfico?  
4. ¿Qué diferencia hay entre una métrica de retención y la etapa de retención en el funnel?  
5. ¿Cuál es el paso siguiente después de identificar un drop‑off significativo en el funnel?

<!-- trazabilidad: run_id=run-20261106-210034-307741 concept=09-product-management-18-funnels written_at=2026-11-07T00:01:50.972604+00:00 -->
<!-- ai:end -->

## Relacionados
- [[09 - Product Management/17 - Product Metrics|Product Metrics]]
- [[09 - Product Management/19 - Retention|Retention]]
- [[09 - Product Management/20 - Product Analytics|Product Analytics]]

---
← [[09 - Product Management/17 - Product Metrics|Product Metrics]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/19 - Retention|Retention]] →
