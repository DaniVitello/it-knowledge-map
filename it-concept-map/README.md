# IT Career Concept Map

Proyecto base para el pipeline de enriquecimiento de conceptos IT almacenados en
un vault de Obsidian. Implementacion por capas (1-10): registry + contratos,
state + persistencia, writer, backend, investigacion, sintesis, validacion,
orquestador, CLI, piloto + calibracion.

## Estructura

```
it-concept-map/
├── models.py              # Contratos de datos (dataclasses con schema_version)
├── registry.py            # Carga de conceptos desde el vault
├── state.py               # State machine + persistencia (estado.json / sqlite)
├── writer.py              # Capa 3: escritura segura del vault (SafeWriter)
├── backend.py             # Capa 4: interfaz ResearchBackend + FakeBackend + run_research_phase
├── notebooklm_backend.py  # Capa 4: adaptador real (re-export de backend)
├── research.py            # Capa 5: ResearchPhase (orquesta investigacion)
├── synthesis.py           # Capa 6: SynthesisPhase (genera study guide con LLM)
├── validation.py          # Capa 7: ValidationPhase (valida sintesis)
├── runner.py              # Capa 8: Runner (orquesta pipeline completo)
├── cli.py                 # Capa 9: CLI (run, status, list, reset, dry-run)
├── pilot.py               # Capa 10: PilotRunner (piloto + calibracion)
├── config.yaml            # Configuracion base
├── pyproject.toml         # Metadatos del proyecto
├── README.md
├── scripts/
│   └── smoke_notebooklm.py  # Smoke test con cuenta real
└── tests/
    ├── test_areas.py      # 25 tests
    ├── test_backend.py    # 15 tests
    ├── test_research.py   # 12 tests
    ├── test_synthesis.py  # 11 tests
    ├── test_validation.py # 12 tests
    ├── test_runner.py     # 11 tests
    ├── test_cli.py        # 12 tests
    └── test_pilot.py      # 9 tests
```

## Estado

TODAS LAS CAPAS COMPLETADAS (1-10). Proyecto listo para piloto con cuenta real.
Total tests: 107 (25+15+12+11+12+11+12+9).
```