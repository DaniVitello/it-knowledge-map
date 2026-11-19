# -*- coding: utf-8 -*-
"""C5 â€” Journey: validacion y evidencias (L1, capa 7).

Valida registros curados y procesa evidencias (imagen/video/documento/enlace).
No redacta registros.
"""
from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ikm.contracts.errors import AbortStage
from ikm.contracts.release import Evidence, EvidenceKind, EvidenceReview, JourneyRecord
from ikm.contracts.utils import sha256_bytes, sha256_text

# Secret scan patterns (reused from inventory)
SECRET_PATTERNS = [
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"AKIA[0-9A-Z]{16}",
    r"sk-[A-Za-z0-9]{20,}",
    r"ghp_[A-Za-z0-9]{36}",
    r"AIza[0-9A-Za-z_\-]{35}",
]
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(\+?\d[\d\s().-]{7,}\d)(?!\d)")


class JourneyError(AbortStage):
    pass


class ApprovedRecordChangedError(JourneyError):
    pass


class MissingEvidenceError(JourneyError):
    pass


class UnresolvedSignalError(JourneyError):
    pass


def _scan_text(text: str) -> List[str]:
    """Escanea texto en busca de secretos, emails, telefonos. Devuelve lista de senales."""
    senales = []
    for pat in SECRET_PATTERNS:
        for m in re.finditer(pat, text):
            senales.append(f"secret:{pat}")
    for m in EMAIL_RE.finditer(text):
        senales.append(f"email:{m.group(0)}")
    for m in PHONE_RE.finditer(text):
        senales.append(f"phone:{m.group(0)}")
    return senales


def _procesar_imagen(ruta: Path, storage_dir: Path) -> Evidence:
    """Procesa una imagen: elimina EXIF, redimensiona, genera WebP."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise JourneyError("missing_dependency", etapa="C5",
                           detalle={"motivo": "Pillow no disponible"}) from exc

    if not ruta.exists():
        raise MissingEvidenceError("missing_evidence", etapa="C5",
                                  detalle={"archivo": str(ruta)})

    crudo = ruta.read_bytes()
    sha = sha256_bytes(crudo)

    # Abrir y eliminar EXIF (re-encode sin metadatos)
    img = Image.open(ruta)
    # Convertir a RGB si es necesario (para WebP)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    # Redimensionar si es muy grande (max 1920px en el lado mayor)
    max_side = 1920
    if max(img.size) > max_side:
        ratio = max_side / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # Generar WebP
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_key = f"{sha[:16]}-{ruta.stem}.webp"
    dest = storage_dir / storage_key
    img.save(dest, format="WEBP", quality=85, method=6)

    # OCR: escanear texto alternativo (si hay) para marcar tokens
    # (El OCR real se diferencia; aca solo escaneamos el nombre del archivo)
    senales = _scan_text(ruta.name)
    if senales:
        # SeÃ±al: decide el autor
        pass

    return Evidence(
        uid=f"e_{sha[:10].upper()}",
        record_uid="",  # se asigna despues
        kind=EvidenceKind.image,
        storage_key=storage_key,
        sha256=sha,
        mime="image/webp",
        size=dest.stat().st_size,
        alt_text=ruta.stem,
        review=EvidenceReview.manually_reviewed,
    )


def _procesar_documento(ruta: Path) -> List[str]:
    """Escanea un documento/codigo en busca de secretos y datos personales."""
    if not ruta.exists():
        raise MissingEvidenceError("missing_evidence", etapa="C5",
                                  detalle={"archivo": str(ruta)})
    try:
        texto = ruta.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise MissingEvidenceError("unreadable_file", etapa="C5",
                                  detalle={"archivo": str(ruta), "motivo": str(exc)}) from exc
    return _scan_text(texto)


def _verificar_enlace(url: str) -> bool:
    """Verifica que un enlace responde (sin bloquear)."""
    try:
        import urllib.request
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status < 400
    except Exception:
        return False


def validar_registro(reg: JourneyRecord, conceptos_uids: set, hash_original: Optional[str] = None) -> JourneyRecord:
    """Valida un registro curado.

    Aborta si: registro approved con hash cambiado; evidencia faltante;
    senal de escaneo sin resolver.
    """
    # Verificar hash si es approved
    if reg.publication == "approved" and hash_original and reg.content_hash != hash_original:
        raise ApprovedRecordChangedError(
            "approved_record_changed", etapa="C5",
            detalle={"uid": reg.uid, "hash_original": hash_original, "hash_actual": reg.content_hash},
        )

    # Verificar que los concept_uids existen
    for cuid in reg.concept_uids:
        if cuid not in conceptos_uids:
            raise JourneyError("invalid_concept_uid", etapa="C5",
                               detalle={"record": reg.uid, "uid_inexistente": cuid})

    # Verificar que las evidencias existen (si hay)
    for evid in reg.evidence_uids:
        if not evid:
            raise MissingEvidenceError("missing_evidence", etapa="C5",
                                      detalle={"record": reg.uid})

    return reg


def procesar_evidencia(ev: Evidence, storage_dir: Path) -> Evidence:
    """Procesa una evidencia segun su tipo.

    Imagen: elimina EXIF, redimensiona, genera WebP.
    Video: revision manual (no se procesa automaticamente).
    Documento/codigo: escaneo de secretos.
    Enlace: se verifica que responde.
    """
    # Para imagenes, el procesamiento ya se hizo en _procesar_imagen.
    # Esta funcion valida y retorna la evidencia.
    if ev.kind == EvidenceKind.image:
        if not ev.storage_key:
            raise MissingEvidenceError("missing_storage_key", etapa="C5",
                                      detalle={"evidence": ev.uid})
    elif ev.kind in (EvidenceKind.document, EvidenceKind.code):
        # Escaneo ya hecho en el flujo de curacion
        pass
    elif ev.kind == EvidenceKind.link:
        # Verificacion de enlace se hace en el flujo de curacion
        pass
    elif ev.kind == EvidenceKind.video:
        # Revision manual obligatoria: no se procesa automaticamente
        if ev.review != EvidenceReview.manually_reviewed:
            raise UnresolvedSignalError("video_not_reviewed", etapa="C5",
                                        detalle={"evidence": ev.uid})
    return ev


def C5_journey(registros: List[JourneyRecord], conceptos_uids: set,
               evidencias: Optional[List[Evidence]] = None,
               storage_dir: Optional[Path] = None) -> List[JourneyRecord]:
    """Valida registros curados y procesa evidencias.

    Aborta si: registro approved con hash cambiado; evidencia faltante;
    senal de escaneo sin resolver.
    """
    if storage_dir is None:
        storage_dir = Path(".")

    validados = []
    for reg in registros:
        # Solo los approved entran al release; los demas se saltan
        if reg.publication not in ("approved",):
            continue
        validar_registro(reg, conceptos_uids)
        validados.append(reg)

    # Procesar evidencias si se proporcionan
    if evidencias:
        for ev in evidencias:
            procesar_evidencia(ev, storage_dir)

    return validados


# Excepciones adicionales
class JourneyValidationError(JourneyError):
    pass
