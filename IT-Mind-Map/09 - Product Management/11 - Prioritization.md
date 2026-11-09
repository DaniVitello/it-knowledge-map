---
title: "Prioritization"
area: "Product Management"
numero: 11
aliases: ["Prioritization"]
tags: [concepto, it/product-management]
---
# Prioritization

> **Área:** [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · **Concepto 11 de 25**

## Qué abarca
- Decidir qué hacer y qué no hacer

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la priorización para decidir qué funcionalidades, mejoras o experimentos deben entrar al backlog y en qué orden, resolviendo la escasez de recursos y la necesidad de generar valor rápidamente. Resuelvo la incertidumbre de “qué hacer primero” al alinear decisiones con los objetivos de negocio, la retroalimentación de usuarios y los datos de rendimiento. Aparece en cada ciclo de planificación, desde la definición de la hoja de ruta hasta la selección de hipótesis para pruebas A/B. Después de entenderla, puedo estructurar debates de equipo, justificar inversiones y medir el impacto de nuestras elecciones. No necesito preocuparme cuando el producto está en fase de mantenimiento sin cambios críticos o cuando los recursos son ilimitados y el riesgo es nulo.

## Esqueleto (el 20% esencial)
1. **Valor vs. Esfuerzo** – Evalúo el impacto potencial de una iniciativa contra el costo de implementarla.  
2. **Alineación con objetivos** – Priorizo lo que impulsa los OKR o métricas clave del producto.  
3. **Datos y evidencia** – Uso métricas de uso, feedback y resultados de experimentos para sustentar la decisión.  
4. **Visibilidad del trade‑off** – Comunico claramente qué se gana y qué se sacrifica al elegir una opción.  
5. **Iteración continua** – Reviso y ajusto la prioridad a medida que aparecen nuevos datos o cambios de contexto.

## Como funciona
1. Reúno una lista de iniciativas pendientes.  
2. Asigno a cada una una estimación de esfuerzo (p. ej., story points) y un puntaje de valor basado en objetivos y datos.  
3. Aplico una matriz simple (Valor × Esfuerzo) o un modelo de scoring para ordenar la lista.  
4. Presento el ranking al equipo, discutiendo los trade‑offs y obteniendo consenso.  
5. Inserto los ítems más altos en el próximo sprint o hoja de ruta, dejando los de bajo puntaje para revisión futura.

## Detalles
- **Básico:** Uso una tabla de dos columnas (Valor, Esfuerzo) y ordeno manualmente.  
- **Intermedio:** Implemento un modelo de scoring que pondera criterios como ingresos potenciales, retención y coste técnico; utilizo herramientas como Airtable o Excel para automatizar el cálculo.  
- **Avanzado:** Integro datos en tiempo real mediante dashboards de analytics, aplico algoritmos de optimización (p. ej., knapsack) y sincronizo la priorización con sistemas de gestión de backlog (Jira, Azure DevOps) para actualizaciones automáticas.

## Ejemplo minimo
```javascript
// Scoring simple: valor (1‑10) * pesoObjetivo + -esfuerzo (1‑5) * pesoCosto
const iniciativas = [
  { nombre: "Login social", valor: 8, esfuerzo: 3 },
  { nombre: "Nuevo reporte PDF", valor: 5, esfuerzo: 2 },
  { nombre: "Refactor UI", valor: 4, esfuerzo: 5 }
];
const pesoValor = 1.0, pesoEsfuerzo = 0.5;
iniciativas.forEach(i => i.score = i.valor * pesoValor - i.esfuerzo * pesoEsfuerzo);
iniciativas.sort((a,b) => b.score - a.score);
console.log(iniciativas);
```

## Errores comunes
- **Sobre‑valorizar ideas sin datos** – evitarlo solicitando evidencia antes de asignar puntaje alto.  
- **Ignorar el costo de oportunidad** – considerar siempre qué se deja de hacer al elegir una iniciativa.  
- **Priorizar solo por facilidad** – equilibrar siempre con el impacto esperado.  
- **Fijarse en una única métrica** – combinar ingresos, retención y satisfacción para una visión completa.  
- **No revisar la lista** – programar revisiones periódicas para ajustar prioridades según nueva información.

## Estado actual
**Fundamentos estables:** la lógica de comparar valor contra esfuerzo y la necesidad de alineación con objetivos siguen siendo la base de cualquier proceso de priorización.  
**Práctica moderna:** se favorecen métodos basados en datos (scoring automático, dashboards en tiempo real) y la integración con herramientas de gestión de backlog que permiten re‑priorizar dinámicamente según métricas de uso y resultados de experimentos.

## Conexiones
- **Roadmapping** – la priorización determina qué ítems aparecen en la hoja de ruta y cuándo.  
- **Experimentación** – los resultados de pruebas A/B alimentan los puntajes de valor en la priorización.  
- **Gestión de stakeholders** – la visibilidad de los trade‑offs facilita la negociación y el alineamiento con partes interesadas.

## Ruta de estudio
1. **Prerequisitos:** comprensión de OKR, métricas de producto (DAU, churn, LTV) y estimación de esfuerzo (story points).  
2. **Fundamentos:** practicar la matriz Valor‑Esfuerzo con casos reales y aprender a argumentar trade‑offs.  
3. **Intermedio:** dominar modelos de scoring y usar herramientas de hoja de cálculo para automatizar cálculos.  
4. **Avanzado:** integrar APIs de analytics, aplicar algoritmos de optimización y conectar el proceso con sistemas de gestión de backlog.  
5. **Especialización:** explorar frameworks como RICE, WSJF y técnicas de portfolio management.

## Preguntas de repaso
1. ¿Cómo relaciono el valor de una iniciativa con los OKR del producto?  
2. ¿Qué datos necesito antes de asignar un puntaje de valor a una hipótesis?  
3. ¿Cuál es la diferencia entre una matriz Valor‑Esfuerzo y un modelo de scoring ponderado?  
4. ¿Cómo evito que la priorización se quede estática cuando aparecen nuevos insights?  
5. ¿De qué manera la priorización impacta la construcción del roadmap y la gestión de stakeholders?

<!-- trazabilidad: run_id=run-20261106-205150-8d0ef4 concept=09-product-management-11-prioritization written_at=2026-11-06T23:52:49.206358+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/11 - Prioritization|Prioritization]] · *Project Management*

---
← [[09 - Product Management/10 - Product Roadmap|Product Roadmap]] · [[09 - Product Management/00 - Índice Product Management|Índice Product Management]] · [[09 - Product Management/12 - Requirements|Requirements]] →
