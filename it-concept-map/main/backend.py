"""Shim de compatibilidad: toda la logica vive en notebook.py.

Permite importar 'backend' como antes, mientras el adaptador de NotebookLM
esta aislado en el modulo notebook (puntos 1.2 y 1.3 del diseno tecnico).
"""
from .notebook import *  # noqa: F401,F403
from . import notebook as _nb

# Re-exportar submodulos comunmente accedidos.
create_backend = _nb.create_backend
pipeline_dir = _nb.pipeline_dir
_atomic_write_json = _nb._atomic_write_json
validate_artifact_schema = _nb.validate_artifact_schema
SchemaError = _nb.SchemaError
ResearchBackend = _nb.ResearchBackend
NotebookLMBackend = _nb.NotebookLMBackend
FakeBackend = _nb.FakeBackend
FakeNotebook = _nb.FakeNotebook
ResearchResult = _nb.ResearchResult
ResearchRequest = _nb.ResearchRequest
BackendError = _nb.BackendError
BackendAuthError = _nb.BackendAuthError
BackendTimeout = _nb.BackendTimeout
BackendNetworkError = _nb.BackendNetworkError
BackendRateLimitError = _nb.BackendRateLimitError
BackendNotFoundError = _nb.BackendNotFoundError
BackendConfigError = _nb.BackendConfigError
BackendCircuitOpenError = _nb.BackendCircuitOpenError
ResearchPersistError = _nb.ResearchPersistError

# Re-exportar helpers privados usados por tests/llamadores.
for _name in ("_map_library_error", "_notebooklm_module"):
    if hasattr(_nb, _name):
        globals()[_name] = getattr(_nb, _name)
