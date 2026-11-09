---
title: "Risk Management"
area: "Project Management"
numero: 13
aliases: ["Risk Management"]
tags: [concepto, it/project-management]
---
# Risk Management

> **Área:** [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · **Concepto 13 de 25**

## Qué abarca
- Identificación y mitigación de riesgos

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el Risk Management para anticipar y controlar los eventos que pueden desviar a un proyecto de sus objetivos de tiempo, costo o calidad. Resuelvo la incertidumbre al identificar, evaluar y planificar respuestas a los riesgos antes de que se materialicen, lo que permite tomar decisiones informadas y proteger la inversión. Aparece en cada fase del proyecto, desde la planificación inicial hasta el cierre, y es esencial cuando el proyecto tiene alta complejidad, dependencias externas o recursos limitados. Después de comprenderlo, puedo diseñar un registro de riesgos, asignar propietarios y monitorear la efectividad de las mitigaciones; también puedo integrar esas prácticas con la gestión de issues y cambios. No necesito preocuparme de forma exhaustiva cuando el proyecto es trivial, de corto plazo y con pocos factores de incertidumbre.

## Esqueleto (el 20% esencial)
1. **Identificación de riesgos** – Detectar eventos potenciales que puedan afectar los objetivos del proyecto.  
2. **Evaluación y priorización** – Analizar la probabilidad e impacto de cada riesgo para ordenar su atención.  
3. **Planificación de respuestas** – Definir acciones de mitigación, transferencia, aceptación o explotación.  
4. **Monitoreo y control** – Revisar continuamente los riesgos y la efectividad de las respuestas.  
5. **Comunicación** – Mantener informados a los stakeholders sobre el estado de los riesgos y decisiones asociadas.

## Como funciona
1. Durante la planificación, el equipo realiza una sesión de *risk identification* (brainstorming, check‑lists, lecciones aprendidas) y registra cada riesgo en un *risk register*.  
2. Cada riesgo se evalúa asignando una probabilidad (p) y un impacto (i); el producto p × i genera un *risk score* que permite priorizar.  
3. Para los riesgos con mayor score se diseñan planes de respuesta: mitigación (reducir p o i), transferencia (seguro, contrato), aceptación (monitorizar) o explotación (si es una oportunidad).  
4. El *risk owner* se encarga de ejecutar la respuesta y de actualizar el registro en cada *risk review* (reuniones de control).  
5. Los cambios en el registro se comunican a los stakeholders y se alinean con los procesos de Issue Management y Change Management.

## Detalles
- **Básico**: crear un registro simple (ID, descripción, probabilidad, impacto, propietario).  
- **Intermedio**: aplicar matrices de riesgo (probabilidad vs impacto) y definir criterios de escalamiento; integrar la revisión de riesgos en los *status meetings*.  
- **Avanzado**: usar técnicas cuantitativas (Monte Carlo, análisis de sensibilidad), automatizar alertas en herramientas de PM, y vincular riesgos a indicadores de desempeño (KPIs) para decisiones estratégicas.

## Ejemplo minimo
```json
{
  "riskId": "R-001",
  "description": "Retraso en la entrega del proveedor de API",
  "probability": 0.4,
  "impact": "Alto",
  "score": 0.4 * 3,   // 3 = factor de impacto alto
  "owner": "Ana Gómez",
  "response": "Mitigación: solicitar plan de contingencia y definir alternativa interna",
  "status": "Abierto"
}
```

## Errores comunes
- **Confundir riesgo con issue** – Un riesgo es potencial; un issue ya ocurrió. Evitar mezclar ambos en el mismo registro.  
- **Subestimar la probabilidad** – Asumir que “es poco probable” sin datos lleva a planes insuficientes; usar datos históricos o expertos.  
- **No actualizar el registro** – Dejar riesgos estáticos impide detectar cambios; programar revisiones periódicas.  
- **Asignar respuestas sin propietario** – Cada riesgo necesita un responsable claro para ejecutar la mitigación.  

## Estado actual
- **Fundamentos estables**: identificación, evaluación (probabilidad/impacto), planificación de respuestas y monitoreo continuo siguen siendo la base aceptada en guías como PMBOK y PRINCE2.  
- **Práctica moderna**: integración de risk registers con herramientas de gestión ágil (Jira, Azure DevOps), uso de análisis cuantitativo y visualizaciones de heat‑maps, y alineación de riesgos con OKR y métricas de negocio.

## Conexiones
- **Issue Management** – Cuando un riesgo se materializa, pasa a ser un issue que debe ser gestionado bajo el proceso de resolución de incidentes.  
- **Change Management** – Las respuestas a riesgos a menudo implican cambios en alcance, cronograma o recursos, por lo que deben ser canalizados por el proceso de gestión de cambios.  
- **Stakeholder Management** – La comunicación de riesgos y sus respuestas influye en la percepción y el compromiso de los stakeholders, afectando la toma de decisiones.

## Ruta de estudio
1. **Pre‑requisitos**: conceptos básicos de planificación de proyectos, cronograma (WBS) y gestión de stakeholders.  
2. **Fundamentos**: leer la sección de Risk Management en la guía PMBOK, practicar con plantillas de risk register.  
3. **Intermedio**: aprender a construir matrices de riesgo y a conducir *risk workshops*.  
4. **Avanzado**: estudiar técnicas cuantitativas (Monte Carlo) y explorar integraciones con herramientas de PM (plugins de riesgo).  
5. **Especialización**: aplicar risk management en entornos ágiles (Scrum, SAFe) y en proyectos de transformación digital.

## Preguntas de repaso
1. ¿Cuál es la diferencia esencial entre un riesgo y un issue dentro de un proyecto?  
2. ¿Cómo se determina la prioridad de un riesgo usando probabilidad e impacto?  
3. ¿Qué papel juega el *risk owner* en la fase de monitoreo y control?  
4. ¿Por qué es importante alinear la gestión de riesgos con Change Management?  
5. ¿Qué ventaja aporta el análisis cuantitativo de riesgos frente a una simple matriz cualitativa?

<!-- trazabilidad: run_id=run-20261109-173245-ab953b concept=10-project-management-13-risk-management written_at=2026-11-09T20:33:57.462515+00:00 -->
<!-- ai:end -->

## Relacionados
- [[10 - Project Management/14 - Issue Management|Issue Management]]
- [[10 - Project Management/15 - Change Management|Change Management]]

---
← [[10 - Project Management/12 - Resource Management|Resource Management]] · [[10 - Project Management/00 - Índice Project Management|Índice Project Management]] · [[10 - Project Management/14 - Issue Management|Issue Management]] →
