---
title: "States & Feedback"
area: "UX / UI"
numero: 18
aliases: ["States & Feedback"]
tags: [concepto, it/ux-ui]
---
# States & Feedback

> **Área:** [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · **Concepto 18 de 25**

## Qué abarca
- Loading
- empty
- success
- error
- disabled
- hover

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los estados y feedback para comunicarle al usuario qué está ocurriendo con la interfaz en cada momento de su interacción. Resuelvo la incertidumbre que genera la ausencia de información visual, como saber si una acción está en proceso, si no hay datos disponibles o si ocurrió un error. Aparecen en cada pantalla donde el producto depende de datos externos o de acciones del usuario: formularios, listados, botones de envío, etc. Después de entenderlos, puedo diseñar transiciones claras, elegir los indicadores adecuados y validar que el feedback sea percibido y comprendido. No necesito preocuparme cuando la interacción es puramente estática y no depende de procesos asíncronos ni de cambios de estado.

## Esqueleto (el 20% esencial)
1. **Loading** – indica que el sistema está procesando una solicitud o recuperando datos.  
2. **Empty** – comunica que no hay contenido disponible para mostrar.  
3. **Success** – confirma que la acción del usuario se completó correctamente.  
4. **Error** – avisa que ocurrió un problema y, a menudo, sugiere una solución.  
5. **Disabled / Hover** – controla la disponibilidad del control y brinda pistas visuales al pasar el cursor.

## Como funciona
1. El diseñador define los estados necesarios según el flujo de datos del producto.  
2. Durante el desarrollo, cada componente expone propiedades que activan esos estados (p. ej., `isLoading`, `hasError`).  
3. Cuando la condición cambia, la UI actualiza su apariencia: muestra un spinner, un mensaje vacío, un check verde, un banner rojo o cambia el estilo del botón.  
4. El feedback se muestra de forma inmediata y persistente hasta que la condición se resuelve, garantizando que el usuario siempre sepa el estado actual.  
5. Opcionalmente, se añaden micro‑animaciones para suavizar la transición entre estados.

## Detalles
- **Básico:** asignar colores y textos claros a cada estado (p. ej., azul para loading, rojo para error).  
- **Intermedio:** usar animaciones sutiles (spinner, fade‑in) y mensajes contextuales que indiquen el siguiente paso.  
- **Avanzado:** sincronizar estados con accesibilidad (ARIA live regions), personalizar feedback según el perfil del usuario y aplicar patrones de “optimistic UI” para anticipar resultados.

## Ejemplo minimo
```html
<button id="saveBtn" disabled>
  <span class="label">Guardar</span>
  <span class="spinner" hidden>⏳</span>
</button>

<script>
const btn = document.getElementById('saveBtn');
function startSaving() {
  btn.disabled = true;
  btn.querySelector('.spinner').hidden = false;
  // simulación de petición
  setTimeout(() => {
    btn.disabled = false;
    btn.querySelector('.spinner').hidden = true;
    btn.querySelector('.label').textContent = 'Guardado';
  }, 1500);
}
btn.addEventListener('click', startSaving);
</script>
```

## Errores comunes
- Usar el mismo color para *loading* y *error* → confunde al usuario; elegir paletas contrastantes.  
- Ocultar el feedback demasiado rápido → el usuario no percibe la confirmación; mantenerlo visible al menos 1 s.  
- No comunicar estados deshabilitados → parece que el control está roto; aplicar estilos visuales claros.

## Estado actual
**Fundamentos estables:** los estados básicos (loading, empty, success, error, disabled, hover) y sus convenciones de color y texto son ampliamente aceptados en guías de estilo.  
**Práctica moderna:** la integración automática de estados mediante frameworks declarativos (React, Vue) y el uso de ARIA live regions para que los lectores de pantalla anuncien cambios en tiempo real.

## Conexiones
- **Data fetching** – los estados de loading y error dependen directamente del ciclo de petición de datos.  
- **Accessibility** – los feedback visuales deben complementarse con atributos ARIA para usuarios con discapacidades.  
- **Interaction design** – los estados hover y disabled forman parte de los patrones de interacción que guían la conducta del usuario.

## Ruta de estudio
1. **Prerequisitos:** conceptos de usabilidad, principios de diseño visual y fundamentos de HTML/CSS.  
2. **Fundamental:** estudiar patrones de feedback en guías de estilo (Material Design, Human Interface Guidelines).  
3. **Intermedio:** practicar con componentes reactivos en un framework (React hooks para manejo de estados).  
4. **Avanzado:** profundizar en accesibilidad (ARIA live regions) y en técnicas de optimistic UI.  
5. **Aplicación:** crear un caso de estudio completo que incluya todos los estados en un flujo de datos real.

## Preguntas de repaso
1. ¿Qué problema de usabilidad resuelve el estado *loading* y cómo se debe presentar visualmente?  
2. ¿En qué situaciones es apropiado usar un estado *empty* y qué mensaje debe acompañarlo?  
3. ¿Cómo se diferencia el feedback de *success* de un simple cambio de color en un botón?  
4. ¿Qué consideraciones de accesibilidad deben aplicarse al mostrar un mensaje de *error*?  
5. ¿Por qué es importante mantener visible el feedback durante al menos un segundo después de la acción?

<!-- trazabilidad: run_id=run-20261106-202905-4c53c1 concept=08-ux-ui-18-states-feedback written_at=2026-11-06T23:30:10.091263+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/18 - Data fetching|Data fetching]] · *Frontend*

---
← [[08 - UX & UI/17 - UI Components|UI Components]] · [[08 - UX & UI/00 - Índice UX - UI|Índice UX / UI]] · [[08 - UX & UI/19 - Responsive Design|Responsive Design]] →
