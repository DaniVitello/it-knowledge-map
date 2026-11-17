# IT Knowledge Map

Un vault de Obsidian con 255 conceptos de ingeniería de software y un pipeline en Python que investiga, sintetiza y escribe cada nota. Las notas son las unidades de conocimiento. El producto es el mapa de relaciones entre ellas.

Arranqué para completar el vault. Terminé aprendiendo a construir el pipeline: contratos de datos, máquina de estados, escritura segura, transporte entre dos máquinas y trazabilidad. Acá están las tres cosas, juntas: el conocimiento, el código y lo que salió mal en el camino.

## Vista rápida

Cada concepto vive en `IT-Mind-Map/<área>/NN - Concepto.md`. El contenido generado queda entre marcadores, para no tocar el frontmatter ni las notas escritas a mano:

```markdown
---
title: "Programming Fundamentals"
area: "Software Engineering"
---
# Programming Fundamentals

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los fundamentos de programación para traducir requisitos del negocio
en instrucciones ejecutables por una máquina.
## Esqueleto (el 20% esencial)
1. **Variables** – espacio nombrado en memoria que almacena valores.
2. **Funciones** – bloques reutilizables que reciben parámetros y devuelven resultados.
<!-- ai:end -->
```

El pipeline solo reemplaza lo que está entre `ai:start` y `ai:end`. Si el bloque cambia a mano, el writer lo detecta y pide revisión en vez de sobrescribirlo.

## Qué hay en este repo

| Ruta | Qué contiene |
| --- | --- |
| `IT-Mind-Map/` | El vault: 10 áreas, 255 conceptos y sus índices |
| `it-concept-map/main/` | Contratos, estado, research, síntesis, validación, writer y orquestador |
| `it-concept-map/exe/` | Puntos de entrada: run_pipeline, run_area, run_missing, retry_failed, pilot |
| `it-concept-map/areas/` | Configuración de contexto por área (roles, dominios preferidos, volatilidad) |
| `it-concept-map/utility/` | Scripts de revisión y mantenimiento del vault |
| `docs/` | Especificación maestra, diseño técnico, auditoría y planes de mejora |
| `explicaciones/` | Explicación del código capa por capa |

## Cómo funciona

```mermaid
flowchart LR
    A[Nota y metadatos] --> B[Research: NotebookLM]
    B --> C[Synthesis: Groq]
    C --> D[Validation]
    D --> E[Writing: SafeWriter]
    E --> F[Verificación de hash]
    F --> G[Concepto completado]
```

Research busca fuentes con NotebookLM, que no consume tokens de LLM. Synthesis genera el contenido con Groq a partir de esas fuentes. Validation aplica checks antes de escribir. Writing reemplaza el bloque AI con escritura atómica y vuelve a leer el archivo para comprobar que nada de afuera cambió.

Hermes orquesta el flujo desde otra máquina. Para operar el proyecto usa la API HTTP de OpenCode: leer archivos, escribirlos y ejecutar comandos. Esas llamadas no invocan modelos, así que no gastan el free tier de OpenCode.

## Estado actual

Datos verificados el 16 de noviembre de 2026:

- El vault tiene 266 archivos Markdown: 255 conceptos más los índices de área y el índice maestro.
- El código está reorganizado en `main/`, `exe/` y `utility/`. Hay correcciones posteriores a la auditoría que se reconstruyen leyendo el código, no un archivo de estado público.
- Los tests todavía no corren después de esa reorganización: al ejecutar `pytest` desde la raíz aparecen 10 errores de importación porque los tests siguen importando módulos con el layout anterior. Está en la lista de pendientes.
- Los números de tests que aparecen en documentos más viejos (82, 107, 108, 116) corresponden a estados distintos del proyecto. No los tomaron como estado vigente.

## Lo que pasó en el camino

La parte aburrida de un proyecto así no es el código. Es darse cuenta de que el sistema que escribís para investigar también puede comerse la cuota que querés usar para investigar.

| Problema | Consecuencia | Cambio |
| --- | --- | --- |
| Una sesión usó la CLI/TUI de OpenCode en vez de la API HTTP | 34 sesiones, 33,3M tokens del free tier en un día; el 90% fue cache read interno | La API HTTP pasó a ser el método principal. El CLI quedó para casos puntuales |
| `concept.seed_urls and [] or []` en `research.py` | Siempre devolvía `[]`: las URLs semilla nunca llegaban a NotebookLM | `concept.seed_urls or []` |
| Asignaciones directas de `st.status` | Saltaban la máquina de estados; un concepto podía escribirse desde `FAILED` | Todas pasaron por `st.transition_to()` |
| El notebook se borraba durante research | El writer perdía las fuentes al verificar | El borrado se movió después de la escritura verificada |
| NotebookLM no expone `delete` en el backend | Quedan notebooks huérfanos y se alcanza el tope de 100 por cuenta | Limpieza manual y rotación de cuentas |
| MSYS traduce paths POSIX solo para comandos bash, no para binarios Windows | `opencode run --server` fallaba con errores de ruta | La API HTTP evita el problema por completo |
| Sesiones largas de 200+ mensajes | El resumen de compacción perdía el detalle de bugs concretos | Sesiones cortas por capa y un archivo de estado compartido como pasamanos |
| Spec y diseño muy detallados, implementación más simple | Auditoría: 8 diferencias críticas, 10 mayores y 11 bugs | Plan de mejoras y correcciones posteriores |

El hallazgo que más me sirvió: el bug de `seed_urls` no apareció en un resumen de la conversación. Apareció leyendo el archivo fuente con la API HTTP. Cuando un detalle importa, voy a la fuente.

Los informes completos están en `docs/auditoria_spec_vs_impl.md` y `docs/plan de mejoras v1.md`. La documentación operativa de las dos máquinas y la gestión de tokens quedó fuera del repo, en una carpeta local de documentación del día.

## Cómo correrlo

Necesitás un venv con las dependencias de `pyproject.toml` y credenciales de Groq y NotebookLM configuradas afuera del repo.

```powershell
cd "C:\Users\DGVit\Proyectos\IT Career\it-concept-map"
..\.venv\Scripts\python.exe exe\run_pipeline.py --area "Software Engineering" --limit 1
```

También podés pasar `--concept <id>` para un concepto puntual o `--force` para reprocesar uno ya completado. Antes de una corrida grande conviene probar con un solo concepto.

## Documentación

- [Especificación maestra](docs/explicacion%20del%20proyecto%20por%20capas%20v1.md)
- [Pseudo-código por capas](docs/explicacion%20del%20proyecto%20por%20capas%20v1%20-%20pseudo%20codigo.md)
- [Auditoría spec vs implementación](docs/auditoria_spec_vs_impl.md)
- [Plan de mejoras](docs/plan%20de%20mejoras%20v1.md)
- [Aprendizajes](docs/learnings.md)

## Uso

Proyecto personal. El vault es la fuente de verdad; el código del pipeline se puede reutilizar, pero las notas son parte de un estudio individual.
