# -*- coding: utf-8 -*-
"""C6 â€” Vinculos KB <-> Journey (L1, capa 8).

Genera journey/links.json desde el campo concepts de cada registro.
No infiere vinculos.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from ikm.contracts.errors import AbortStage

from .journey import JourneyError


class LinksError(AbortStage):
    pass


def generar_links(registros: List[Any], conceptos_uids: set) -> Dict[str, List[str]]:
    """Mapea concept_uid -> list[record_uid]. Valida que cada uid exista.

    Aborta si: vinculo a un uid inexistente.
    """
    links: Dict[str, List[str]] = {}
    for reg in registros:
        uid = getattr(reg, "uid", None) or (reg.get("uid") if isinstance(reg, dict) else None)
        concepts = getattr(reg, "concept_uids", None) or (reg.get("concept_uids", []) if isinstance(reg, dict) else [])
        if not uid:
            continue
        for cuid in concepts:
            if cuid not in conceptos_uids:
                raise LinksError("invalid_concept_uid", etapa="C6",
                                 detalle={"record": uid, "uid_inexistente": cuid})
            links.setdefault(cuid, [])
            if uid not in links[cuid]:
                links[cuid].append(uid)
    return links


def guardar_links(links: Dict[str, List[str]], workdir: Path) -> Path:
    """Guarda journey/links.json de forma atomica."""
    journey_dir = workdir / "journey"
    journey_dir.mkdir(parents=True, exist_ok=True)
    dest = journey_dir / "links.json"
    import os, tempfile
    texto = json.dumps(links, ensure_ascii=False, sort_keys=True, indent=2)
    fd, tmp = tempfile.mkstemp(dir=str(journey_dir), prefix="links.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, dest)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise
    return dest
