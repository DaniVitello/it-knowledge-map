# -*- coding: utf-8 -*-
"""Carga y validacion del release en el backend (L2, capa 13)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import sha256_file


class ReleaseError(Exception):
    """Error base del release loader."""
    pass


class ReleaseNotFoundError(ReleaseError):
    pass


class ReleaseHashMismatchError(ReleaseError):
    pass


class ReleaseSchemaError(ReleaseError):
    pass


class Release:
    """Release cargado en memoria."""

    def __init__(self, release_id: str, manifest: Dict[str, Any],
                 base_path: Path):
        self.release_id = release_id
        self.manifest = manifest
        self.base_path = base_path
        self._cache: Dict[str, Any] = {}

    def get_file_path(self, relative_path: str) -> Path:
        return self.base_path / relative_path

    def load_json(self, relative_path: str) -> Any:
        if relative_path in self._cache:
            return self._cache[relative_path]
        p = self.base_path / relative_path
        if not p.exists():
            raise ReleaseNotFoundError(f"archivo no encontrado: {relative_path}")
        data = json.loads(p.read_text(encoding="utf-8"))
        self._cache[relative_path] = data
        return data

    def invalidate_cache(self) -> None:
        self._cache.clear()


def cargar_release(release_id: str, release_path: Path) -> Release:
    """Carga manifest.json, valida hashes, verifica schema_version soportado.

    Aborta si: manifest no existe, hash no coincide, schema_version no soportado.
    """
    release_path = Path(release_path)
    if not release_path.exists():
        raise ReleaseNotFoundError(f"release no encontrado: {release_path}")

    manifest_path = release_path / "manifest.json"
    if not manifest_path.exists():
        raise ReleaseNotFoundError(f"manifest.json no encontrado en {release_path}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ReleaseSchemaError(f"manifest invalido: {exc}") from exc

    # Validar schema_version
    schema_version = manifest.get("schema_version")
    if schema_version not in (1, "1", "2.0.0", 2):
        raise ReleaseSchemaError(f"schema_version no soportado: {schema_version}")

    # Validar release_id
    if manifest.get("release_id") != release_id and release_id:
        # Permitir si el release_id del manifest es el que se pide
        if manifest.get("release_id") != release_id:
            raise ReleaseSchemaError(
                f"release_id no coincide: manifest={manifest.get('release_id')}, pedido={release_id}"
            )

    # Validar hashes de archivos
    files = manifest.get("files", [])
    for f in files:
        path = f.get("path")
        expected_hash = f.get("sha256")
        if not path or not expected_hash:
            raise ReleaseSchemaError(f"entrada de archivo invalida: {f}")
        full_path = release_path / path
        if not full_path.exists():
            raise ReleaseNotFoundError(f"archivo faltante en release: {path}")
        actual_hash = sha256_file(full_path)
        if actual_hash != expected_hash:
            raise ReleaseHashMismatchError(
                f"hash no coincide para {path}: esperado={expected_hash}, actual={actual_hash}"
            )

    release = Release(
        release_id=manifest.get("release_id", release_id),
        manifest=manifest,
        base_path=release_path,
    )
    return release


def validar_compatibilidad(frontend_release_id: str, backend_release_id: str) -> bool:
    """El backend soporta la actual y la anterior (schema_version)."""
    # Simplificado: si ambos tienen el mismo release_id, son compatibles
    if frontend_release_id == backend_release_id:
        return True
    # Si difieren, el backend informa su release_id y el frontend ofrece recargar
    return False


def listar_releases(releases_dir: Path) -> List[str]:
    """Lista los release_id disponibles en el directorio de releases."""
    releases_dir = Path(releases_dir)
    if not releases_dir.exists():
        return []
    result = []
    for d in releases_dir.iterdir():
        if d.is_dir() and (d / "manifest.json").exists():
            result.append(d.name)
    return sorted(result)


class ReleaseLoaderError(ReleaseError):
    pass
