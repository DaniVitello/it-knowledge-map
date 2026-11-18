# -*- coding: utf-8 -*-
"""Utilidades compartidas (L0.4): hashes, escritura atomica, clave de cache."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Union

PathLike = Union[str, os.PathLike]


def sha256_text(text: Union[str, bytes]) -> str:
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.sha256(text).hexdigest()


def sha256_file(path: PathLike) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def escritura_atomica(path: PathLike, data: bytes) -> None:
    """Escribe a un temporal y renombra: nunca queda un archivo a medias."""
    destino = Path(path)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(destino.parent), prefix=destino.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, destino)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def escribir_json_atomico(path: PathLike, obj: Any) -> None:
    """JSON determinista: claves ordenadas, sin marcas de tiempo."""
    texto = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)
    escritura_atomica(path, texto.encode("utf-8"))


def clave_cache(entrada: Any, version_etapa: Union[int, str], hash_config: str) -> str:
    """clave = hash(entrada) + version_etapa + hash_config.

    Si la clave no cambio, la etapa se omite (idempotencia, 6.1).
    """
    if isinstance(entrada, (dict, list)):
        crudo = json.dumps(entrada, ensure_ascii=False, sort_keys=True)
    else:
        crudo = entrada if isinstance(entrada, str) else str(entrada)
    return f"{sha256_text(crudo)}:{version_etapa}:{hash_config}"


def hash_arbol_vault(root: PathLike) -> str:
    """Hash estable de un arbol (ruta relativa + sha256 de cada archivo)."""
    root = Path(root)
    h = hashlib.sha256()
    if not root.exists():
        return sha256_text("")
    for ruta in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = ruta.relative_to(root).as_posix()
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(sha256_file(ruta).encode("ascii"))
    return h.hexdigest()
