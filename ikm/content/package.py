# -*- coding: utf-8 -*-
"""C9 — Empaquetado (L1, capa 11).

Escribe los archivos del release de forma atomica, genera manifest.json
con hashes REALES de los bytes en disco y el release_id. No publica.

Fail-closed: si un archivo falta o su hash no coincide, aborta.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import sha256_file, escribir_json_atomico, escritura_atomica
from ikm.content.release_files import serializar_json


class PackageError(AbortStage):
    pass


class HashMismatchError(PackageError):
    pass


def calcular_release_id(archivos: List[Dict[str, Any]]) -> str:
    """release_id = fecha UTC + prefijo del hash de contenido (sin fecha)."""
    contenido_hash = _hash_contenido_release(archivos)
    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"{fecha}-{contenido_hash[:8]}"


def _hash_contenido_release(archivos: List[Dict[str, Any]]) -> str:
    """Hash del contenido del release (orden estable por path, sin fecha)."""
    h = hashlib.sha256()
    for a in sorted(archivos, key=lambda x: x["path"]):
        h.update(a["path"].encode("utf-8"))
        h.update(b"\0")
        h.update(a["sha256"].encode("ascii"))
    return h.hexdigest()


def listar_archivos_release(release_dir: Path) -> List[Dict[str, str]]:
    """Lista todos los archivos del release con su sha256 real en disco."""
    archivos: List[Dict[str, str]] = []
    if not release_dir.exists():
        return archivos
    for p in sorted(release_dir.rglob("*")):
        if p.is_file():
            rel = p.relative_to(release_dir).as_posix()
            archivos.append({"path": rel, "sha256": sha256_file(p)})
    return archivos


def escribir_archivos_release(release_dir: Path,
                              payloads: Dict[str, Any]) -> List[Dict[str, str]]:
    """Escribe cada payload JSON de forma atomica y devuelve path+sha256 real.

    Los paths pueden ser anidados (concepts/<uid>.json). El directorio se
    crea si no existe; cada archivo se escribe tmp+rename (nunca a medias).
    """
    release_dir = Path(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    archivos: List[Dict[str, str]] = []
    for rel in sorted(payloads):
        destino = release_dir / rel
        escritura_atomica(destino, serializar_json(payloads[rel]))
        archivos.append({"path": rel, "sha256": sha256_file(destino)})
    return archivos


def empaquetar(workdir: Path, conceptos: int, areas: int, relaciones: int,
               journey_records: int, evidencias: int, chunks: int,
               archivos: List[Dict[str, str]],
               release_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Genera el manifest con counts, files (path + sha256) y release_id.

    Si `release_dir` se provee, verifica contra disco que cada archivo
    exista y su hash coincida (fail-closed). Aborta ante entradas invalidas.
    """
    for a in archivos:
        if not a.get("path") or not a.get("sha256") or len(a["sha256"]) != 64:
            raise HashMismatchError("invalid_file_entry", etapa="C9",
                                    detalle={"archivo": a})
    if release_dir is not None:
        release_dir = Path(release_dir)
        for a in archivos:
            p = release_dir / a["path"]
            if not p.is_file():
                raise HashMismatchError("missing_release_file", etapa="C9",
                                        detalle={"archivo": a["path"]})
            real = sha256_file(p)
            if real != a["sha256"]:
                raise HashMismatchError("hash_mismatch", etapa="C9",
                                        detalle={"archivo": a["path"],
                                                 "esperado": a["sha256"],
                                                 "real": real})

    manifest = {
        "schema_version": 1,
        "release_id": calcular_release_id(archivos),
        "pipeline_version": "0.1.0",
        "vault_hash": "",  # se llena desde el runner
        "counts": {
            "concepts": conceptos,
            "areas": areas,
            "relations": relaciones,
            "journey_records": journey_records,
            "evidence": evidencias,
            "chunks": chunks,
        },
        "files": sorted(archivos, key=lambda x: x["path"]),
    }
    return manifest


def guardar_manifest(workdir: Path, manifest: Dict[str, Any]) -> Path:
    """Guarda manifest.json de forma atomica y actualiza latest.json."""
    release_dir = workdir / "releases" / manifest["release_id"]
    release_dir.mkdir(parents=True, exist_ok=True)
    dest = release_dir / "manifest.json"
    escribir_json_atomico(dest, manifest)
    latest = workdir / "releases" / "latest.json"
    escribir_json_atomico(latest, {"release_id": manifest["release_id"]})
    return dest