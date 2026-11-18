# Changelog

## [Remediacion v1] - 2026-11-18

Rama `fix/v1-remediation`. Build verde: 116 tests, ruff y compileall limpios.

### Added
- CI (GitHub Actions): pytest + ruff (E9,F63,F7,F82) + compileall en push/PR.
- `config.example.yaml` (plantilla sin secretos) y `requirements-dev.txt` pineado.
- `exe/__init__.py`, `utility/__init__.py` (paquetes importables).
- LICENSE (MIT), CHANGELOG.

### Fixed
- Imports de tests migrados a `main.*`/`exe.*` (10 errores de coleccion -> 0).
- `areas.AREAS_DIR`: path roto tras migracion a `main/` (parent -> parent.parent).
- `validation`: NameError `_check_uncertainty_markers` + codigo muerto + scope de metrics.
- `research`: `SCHEMA_VERSION` sin importar; guard de `level` None.
- `writer.verify_wikilinks_preserved`: comparaba toda la nota en vez de la zona exterior.
- Hash de idempotencia canonico (`content_hash_inside`, agnostico de newlines) writer+runner.
- `_source_from_dict`: acepta URLs string (seed_urls) -> fuentes ya no vacias.
- Layout de artefactos unificado a `concepts/<id>/` (research alineado con synthesis/validation/state).
- `cli._load_concepts`: fail-fast (vault ilegible ya no devuelve [] silencioso).
- Gate DoD funcional (`from utility import dod`), antes salteado en silencio.
- Sintaxis 3.11: f-string cli, `golden_set.py` bloque __main__, escape `gen_audio_overview`.

### Changed
- `ConceptStatus` movido a `models.py` (capa base); `state` re-exporta. Ciclo de import roto.
- Scripts manuales (`test_area`, `test_nlm`) movidos de `test/` a `exe/`.
- `pyproject.toml`: paquetes main/exe/utility, entry point `main.cli:main`, config ruff.

### Security
- Secret-scan: arbol actual limpio; la HISTORIA git del repo publico contiene password del server y claves Groq (commits a6f3027, a64ef73, 85e17a6, 9c44ef9, 721aa6a). PENDIENTE (accion del usuario): rotar credenciales, purgar historia, repo privado.
