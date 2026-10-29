"""Adaptador real de NotebookLM (re-export de backend.py).

Mantiene la interfaz ResearchBackend contra notebooklm-py async.
El codigo vive en backend.py (NotebookLMBackend) para un unico punto de verdad.
"""

from backend import (
    NotebookLMBackend,
    _map_library_error,
    _notebooklm_module,
)

__all__ = ["NotebookLMBackend", "_map_library_error", "_notebooklm_module"]
