# IT Knowledge Map

Vault de Obsidian con ~255 conceptos de carrera IT, organizados en 10 áreas temáticas. Cada concepto incluye definición, fuentes verificadas, y cross-links contextuales.

## Objetivo

Tener en un solo lugar todos los conceptos de la carrera IT a los que se quiera acceder, con información verificada y estructurada, conectados entre sí por contexto.

## Áreas

1. Software Engineering
2. Frontend
3. Backend
4. Database / Data Analytics
5. Networking / Internet
6. Operating Systems / Linux
7. AI Engineering
8. UX / UI
9. Product Management
10. Project Management

## Estructura

```
IT Career/
├── it-concept-map/     # Pipeline de relleno automatizado
│   ├── models.py       # Contratos y tipos
│   ├── registry.py     # Registro de conceptos
│   ├── state.py        # Persistencia y estado
│   ├── research.py     # Fase de research (NotebookLM)
│   ├── synthesis.py    # Fase de síntesis (LLM)
│   ├── validation.py   # Validación determinista
│   ├── writer.py       # Escritura segura al vault
│   ├── runner.py       # Orquestador
│   ├── cli.py          # Interfaz de línea de comandos
│   └── pilot.py        # Runner de pilot
├── docs/               # Documentación del proyecto
├── explicaciones/      # Explicaciones por capa
└── *.md                # Conceptos del vault (255 archivos)
```

## Pipeline

El pipeline rellena automáticamente los 255 conceptos del vault:

1. **Research** — busca fuentes verificadas via NotebookLM (zero tokens)
2. **Synthesis** — genera contenido estructurado con LLM (Groq)
3. **Validation** — checks deterministas de calidad
4. **Writing** — escribe al vault con integridad de hash

### Uso

```bash
cd it-concept-map
.venv\Scripts\activate
python run_pipeline.py --area "Software Engineering"
```

### Tests

```bash
pytest  # 116 tests pasando
```

## Tech Stack

| Componente | Tecnología |
|-----------|-----------|
| Vault | Obsidian (Markdown) |
| Research | NotebookLM (via notebooklm-py) |
| Synthesis LLM | Groq (gpt-oss-120b) |
| Orquestación | Hermes Agent ,OpenCode and Python (determinista) |
| Persistencia | JSON + SQLite |

## Licencia

Uso personal.
