# -*- coding: utf-8 -*-
"""C0 — Inventario y clasificacion (capa L1).

Entrada: rutas del vault y del material crudo del Journey; publish.config.
Salida: inventory.json. Todo elemento nace `private`. Los escaneos producen
SENALES, nunca decisiones. No parsea contenido ni decide publicacion.

Aborta: configuracion invalida; archivo ilegible; hash que cambia durante la corrida.
Reporta: cobertura por origen; senales halladas; elementos sin clasificar.
"""
from __future__ import annotations

import os
import re
from collections import Counter
from pathlib import Path
from typing import List

from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import hash_arbol_vault, sha256_bytes, sha256_text

from .publish_config import PublishConfig
from .schemas import Inventory, InventoryItem, InventorySummary, ScanSignal

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(\+?\d[\d\s().-]{7,}\d)(?!\d)")
ABS_PATH_RE = re.compile(r"(?<![\w])/(?:home|Users|root|var|etc|opt|mnt)/[^\s\)\]\}]+")
WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\(?:Users|Windows|Program Files)[^\s\)\]\}]*")
URL_RE = re.compile(r"https?://[^\s\)\]\}>\"']+")
PRIVATE_URL_RE = re.compile(r"(localhost|127\.0\.0\.1|192\.168\.|10\.|172\.(?:1[6-9]|2\d|3[01])\.)")


def _senales_de_texto(texto: str, config: PublishConfig) -> List[ScanSignal]:
    """Escaneos que producen senales, no decisiones."""
    out: List[ScanSignal] = []
    for patron in config.scan_patterns:
        for m in re.finditer(patron, texto):
            out.append(ScanSignal(kind="secret_pattern", excerpt=texto[max(0, m.start() - 20):m.end() + 20]))
    for m in EMAIL_RE.finditer(texto):
        out.append(ScanSignal(kind="email", excerpt=m.group(0)))
    for m in PHONE_RE.finditer(texto):
        out.append(ScanSignal(kind="phone", excerpt=m.group(0)))
    for m in ABS_PATH_RE.finditer(texto):
        out.append(ScanSignal(kind="absolute_path", excerpt=m.group(0)))
    for m in WINDOWS_PATH_RE.finditer(texto):
        out.append(ScanSignal(kind="system_path", excerpt=m.group(0)))
    for m in URL_RE.finditer(texto):
        url = m.group(0).rstrip(".,);")
        if PRIVATE_URL_RE.search(url):
            out.append(ScanSignal(kind="private_url", excerpt=url))
    return out


def _tipo_de(ruta: Path) -> str:
    if ruta.suffix.lower() in (".md", ".markdown"):
        return "markdown"
    if ruta.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"):
        return "image"
    return "otro"


def _iter_archivos(raices: List[str], config: PublishConfig) -> List[Path]:
    vistos = set()
    out: List[Path] = []
    for raiz in raices:
        base = Path(raiz)
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(base).as_posix()
            if any(Path(rel).match(pat) for pat in config.exclude):
                continue
            # include: si no coincide con ninguno, se excluye
            if config.include and not any(Path(rel).match(pat) for pat in config.include):
                continue
            clave = str(p.resolve())
            if clave in vistos:
                continue
            vistos.add(clave)
            out.append(p)
    return sorted(out, key=lambda p: str(p))


def C0_inventario(config: PublishConfig) -> Inventory:
    """Inventaria y clasifica. Todo nace private. Solo lectura."""
    if not config.vault_root:
        raise AbortStage("invalid_config", etapa="C0", detalle={"motivo": "vault_root vacio"})

    raices = [config.vault_root] + list(config.journey_raw_roots)
    hash_antes = hash_arbol_vault(config.vault_root)
    archivos = _iter_archivos(raices, config)

    items: List[InventoryItem] = []
    for p in archivos:
        try:
            crudo = p.read_bytes()
        except OSError as exc:
            raise AbortStage("unreadable_file", etapa="C0",
                             detalle={"archivo": str(p), "motivo": str(exc)}) from exc
        tipo = _tipo_de(p)
        signals: List[ScanSignal] = []
        if tipo == "markdown":
            try:
                signals = _senales_de_texto(crudo.decode("utf-8", errors="replace"), config)
            except Exception:
                signals = []
        items.append(InventoryItem(
            id_temporal=sha256_text(str(p))[:16],
            hash_de_ruta=sha256_text(str(p.relative_to(Path(config.vault_root).parent))
                                     if str(p).startswith(config.vault_root) else str(p)),
            tipo=tipo,
            sha256=sha256_bytes(crudo),
            clasificacion="private",
            signals=signals,
        ))

    hash_despues = hash_arbol_vault(config.vault_root)
    if hash_despues != hash_antes:
        raise AbortStage("vault_modified", etapa="C0",
                         detalle={"hash_antes": hash_antes, "hash_despues": hash_despues})

    por_tipo = Counter(i.tipo for i in items)
    por_clasif = Counter(i.clasificacion for i in items)
    por_origen = Counter()
    for p in archivos:
        base = Path(config.vault_root)
        try:
            rel = p.relative_to(base)
            por_origen[rel.parts[0] if len(rel.parts) > 1 else "(raiz)"] += 1
        except ValueError:
            por_origen["(journey)"] += 1

    summary = InventorySummary(
        total=len(items),
        por_tipo=dict(sorted(por_tipo.items())),
        por_clasificacion=dict(sorted(por_clasif.items())),
        con_senales=sum(1 for i in items if i.signals),
        por_origen=dict(sorted(por_origen.items())),
    )
    return Inventory(items=items, summary=summary, vault_hash=hash_antes)
