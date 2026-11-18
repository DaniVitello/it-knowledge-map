# -*- coding: utf-8 -*-
"""C1 — Parseo de la Knowledge Base (capa L1).

Entrada: notas de la lista de inclusion. Salida: parsed/concepts/*.json
(frontmatter, zonas, secciones, WikiLinks con posicion y oracion, marcas de
verificacion, fuentes). No resuelve links ni asigna identidades (C2/C3).

Aborta: frontmatter invalido; titulo no resoluble.
Reporta: secciones del contrato ausentes; marcas de verificacion.
No hace: decidir publicacion, resolver destinos, tocar el vault.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

from ikm.contracts.errors import AbortStage
from ikm.contracts.utils import sha256_text

from .publish_config import SECCIONES_CONTRATO, PublishConfig
from .schemas import ConceptSections, ParsedConcept, SourceRef, VerificationMark, WikiLink, Zone, ZoneKind

AI_START = re.compile(r"<!--\s*ai:start\s*-->", re.I)
AI_END = re.compile(r"<!--\s*ai:end\s*-->", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
CODE_BLOCK = re.compile(r"```.*?```", re.S | re.I)
URL_RE = re.compile(r"https?://[^\s\)\]\}>\"']+")
SIN_VERIFICAR = re.compile(r"\(?\s*s[íi]n\s+verificar\s*\)?", re.I)
VERIFICAR = re.compile(r"⚠️?\s*\(?\s*verificar\s*\)?", re.I)

HEADING_TO_ZONE = {
    "qué abarca": ZoneKind.que_abarca,
    "que abarca": ZoneKind.que_abarca,
    "mis notas": ZoneKind.mis_notas,
    "relacionados": ZoneKind.relacionados,
}

# Prioridad al decidir a que zona pertenece un offset (la mas especifica gana).
PRIORIDAD = {
    ZoneKind.relacionados: 0,
    ZoneKind.que_abarca: 1,
    ZoneKind.bloque_ai: 2,
    ZoneKind.mis_notas: 3,
    ZoneKind.otro: 4,
    ZoneKind.navegacion: 5,
    ZoneKind.pie: 6,
    ZoneKind.titulo: 7,
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def _canon_seccion(titulo: str) -> Optional[str]:
    """Mapea variantes reales ('Esqueleto (el 20% esencial)') a la seccion canonica."""
    n = _norm(re.sub(r"\s*\(.*?\)\s*", "", titulo))
    for canon, variantes in SECCIONES_CONTRATO.items():
        for v in variantes:
            if n == _norm(v) or n.startswith(_norm(v)):
                return canon
    return None


def _extraer_frontmatter(texto: str) -> Tuple[Dict, str, int]:
    """Devuelve (frontmatter, cuerpo, offset del cuerpo)."""
    if not texto.startswith("---"):
        return {}, texto, 0
    fin = texto.find("\n---", 3)
    if fin == -1:
        return {}, texto, 0
    bloque = texto[3:fin].strip("\n")
    try:
        datos = yaml.safe_load(bloque) or {}
    except yaml.YAMLError as exc:
        raise AbortStage("invalid_frontmatter", etapa="C1",
                         detalle={"motivo": str(exc)}) from exc
    if not isinstance(datos, dict):
        raise AbortStage("invalid_frontmatter", etapa="C1",
                         detalle={"motivo": "frontmatter no es un mapa"})
    cuerpo = texto[fin + 4:]
    return datos, cuerpo, fin + 4


def _titulo(frontmatter: Dict, cuerpo: str) -> str:
    t = str(frontmatter.get("title") or "").strip()
    if t:
        return t
    m = re.search(r"^#\s+(.+?)\s*$", cuerpo, re.M)
    if m:
        return m.group(1).strip()
    return ""


def _zonas_de(cuerpo: str, config: PublishConfig) -> List[Zone]:
    """Clasifica la nota en zonas. Fuente de verdad para C3 (que links cuentan).

    El bloque AI es una zona unica y publicable; los encabezados `##` que caen
    dentro de el NO generan zonas propias (se resuelven por seccion en el link).
    """
    zonas: List[Zone] = []

    bloque_start = bloque_end = None
    m_start = AI_START.search(cuerpo)
    if m_start:
        m_end = AI_END.search(cuerpo, m_start.end())
        bloque_end = m_end.start() if m_end else len(cuerpo)
        bloque_start = m_start.start()
        zonas.append(Zone(kind=ZoneKind.bloque_ai, name="ai", start=bloque_start, end=bloque_end,
                          publicable=config.zona_es_publicable("bloque_ai"),
                          text=cuerpo[m_start.end():bloque_end]))

    h1 = re.search(r"^#\s+(.+?)\s*$", cuerpo, re.M)
    if h1:
        zonas.append(Zone(kind=ZoneKind.titulo, name=h1.group(1), start=h1.start(), end=h1.end(),
                          publicable=False, text=h1.group(1)))

    bq = re.search(r"^>\s*\*\*[ÁA]rea:\*\*.*$", cuerpo, re.M)
    if bq:
        zonas.append(Zone(kind=ZoneKind.navegacion, name="area", start=bq.start(), end=bq.end(),
                          publicable=config.zona_es_publicable("navegacion"), text=bq.group(0)))

    heads = list(H2.finditer(cuerpo))
    for i, m in enumerate(heads):
        start = m.start()
        if bloque_start is not None and bloque_start <= start < bloque_end:
            continue
        fin = len(cuerpo)
        for j in range(i + 1, len(heads)):
            hs = heads[j].start()
            if bloque_start is not None and bloque_start <= hs < bloque_end:
                continue
            fin = hs
            break
        if bloque_start is not None and start < bloque_start < fin:
            fin = bloque_start
        if _norm(m.group(1)) == "relacionados":
            pie = re.search(r"^---\s*$", cuerpo[start:fin], re.M)
            if pie:
                fin = start + pie.start()
        kind = HEADING_TO_ZONE.get(_norm(m.group(1)), ZoneKind.otro)
        publicable = config.zona_es_publicable(kind.value) if kind != ZoneKind.otro else False
        zonas.append(Zone(kind=kind, name=m.group(1), start=start, end=fin,
                          publicable=publicable, text=cuerpo[start:fin]))

    pie = re.search(r"^(?:←\s*)?\[\[.*→\s*$", cuerpo, re.M)
    if pie:
        zonas.append(Zone(kind=ZoneKind.pie, name="prevnext", start=pie.start(), end=pie.end(),
                          publicable=False, text=pie.group(0)))

    return zonas


def _zona_de_offset(zonas: List[Zone], offset: int) -> Optional[Zone]:
    candidatas = [z for z in zonas if z.start <= offset < z.end]
    if not candidatas:
        return None
    return min(candidatas, key=lambda z: PRIORIDAD.get(z.kind, 99))


def _seccion_de(cuerpo: str, offset: int) -> str:
    """Nombre del `##` que contiene el offset (seccion semantica del link/marca)."""
    mejor = ""
    for m in H2.finditer(cuerpo):
        if m.end() <= offset:
            mejor = m.group(1)
        else:
            break
    return mejor


def _oracion_de(texto: str, offset: int) -> str:
    """La oracion (o linea) que contiene el offset."""
    linea_ini = texto.rfind("\n", 0, offset) + 1
    linea_fin = texto.find("\n", offset)
    if linea_fin == -1:
        linea_fin = len(texto)
    linea = texto[linea_ini:linea_fin].strip()
    if len(linea) <= 200:
        return linea
    pos = offset - linea_ini
    inicios = [x for x in (linea.rfind(". ", 0, pos), linea.rfind("! ", 0, pos),
                           linea.rfind("? ", 0, pos)) if x != -1]
    ini = (max(inicios) + 1) if inicios else 0
    fines = [x for x in (linea.find(". ", pos), linea.find("! ", pos), linea.find("? ", pos)) if x != -1]
    fin = (min(fines) + 1) if fines else len(linea)
    return linea[ini:fin].strip()[:400]


def _wikilinks_de(texto: str, zonas: List[Zone], config: PublishConfig) -> List[WikiLink]:
    """Solo zonas publicables; ignora bloques de codigo."""
    out: List[WikiLink] = []
    codigo = [(m.start(), m.end()) for m in CODE_BLOCK.finditer(texto)]
    for m in WIKILINK.finditer(texto):
        if any(a <= m.start() < b for a, b in codigo):
            continue
        zona = _zona_de_offset(zonas, m.start())
        if zona is None or not zona.publicable:
            continue
        interno = m.group(1)
        destino, alias = interno, None
        if "|" in interno:
            destino, alias = interno.split("|", 1)
        heading = None
        if "#" in destino:
            destino, heading = destino.split("#", 1)
        out.append(WikiLink(
            destino_textual=destino.strip(),
            alias=alias.strip() if alias else None,
            heading=heading.strip() if heading else None,
            seccion=_seccion_de(texto, m.start()) or zona.name or zona.kind.value,
            oracion=_oracion_de(texto, m.start()),
            offset=m.start(),
            zona=zona.kind.value,
        ))
    return out


def _marcas_de(cuerpo: str, zonas: List[Zone], config: PublishConfig) -> List[VerificationMark]:
    """Registra 'sin verificar' y '⚠️ verificar' por seccion. Nunca los stripea."""
    out: List[VerificationMark] = []
    for m in SIN_VERIFICAR.finditer(cuerpo):
        zona = _zona_de_offset(zonas, m.start())
        seccion = _seccion_de(cuerpo, m.start()) or (zona.name if zona else "") or "desconocida"
        out.append(VerificationMark(section=seccion, kind="sin_verificar"))
    for m in VERIFICAR.finditer(cuerpo):
        zona = _zona_de_offset(zonas, m.start())
        seccion = _seccion_de(cuerpo, m.start()) or (zona.name if zona else "") or "desconocida"
        out.append(VerificationMark(section=seccion, kind="verificar"))
    return out


def _fuentes_de(cuerpo: str) -> List[SourceRef]:
    """Cosecha URLs de la nota. No exige una fuente web por claim (decision de encuadre)."""
    vistos = set()
    out: List[SourceRef] = []
    for m in URL_RE.finditer(cuerpo):
        url = m.group(0).rstrip(".,);")
        if url in vistos:
            continue
        vistos.add(url)
        out.append(SourceRef(url=url))
    return out


def _secciones_de(bloque_ai: str) -> Tuple[ConceptSections, List[str]]:
    """Extrae las 10 secciones del contrato del bloque AI. Reporta ausentes."""
    secciones = list(H2.finditer(bloque_ai))
    por_canon: Dict[str, str] = {}
    for i, m in enumerate(secciones):
        canon = _canon_seccion(m.group(1))
        if not canon or canon in por_canon:
            continue
        inicio = m.end()
        fin = secciones[i + 1].start() if i + 1 < len(secciones) else len(bloque_ai)
        por_canon[canon] = bloque_ai[inicio:fin].strip()
    data = {k: v for k, v in por_canon.items() if v}
    ausentes = [c for c in SECCIONES_CONTRATO if c not in por_canon or not por_canon[c]]
    return ConceptSections(**data), ausentes


def C1_parseo_nota(ruta: Path, config: PublishConfig, id_temporal: str) -> ParsedConcept:
    try:
        crudo = ruta.read_bytes()
    except OSError as exc:
        raise AbortStage("unreadable_file", etapa="C1",
                         detalle={"archivo": str(ruta), "motivo": str(exc)}) from exc
    texto = crudo.decode("utf-8", errors="replace")

    if not texto.startswith("---"):
        raise AbortStage("invalid_frontmatter", etapa="C1", detalle={"archivo": str(ruta)})
    frontmatter, cuerpo, _ = _extraer_frontmatter(texto)
    titulo = _titulo(frontmatter, cuerpo)
    if not titulo:
        raise AbortStage("unresolvable_title", etapa="C1", detalle={"archivo": str(ruta)})

    zonas = _zonas_de(cuerpo, config)
    bloque = next((z for z in zonas if z.kind == ZoneKind.bloque_ai), None)
    sections, ausentes = _secciones_de(bloque.text) if bloque else (ConceptSections(), list(SECCIONES_CONTRATO))

    return ParsedConcept(
        note_id=id_temporal,
        titulo=titulo,
        frontmatter=frontmatter,
        zones=zonas,
        sections=sections,
        sections_missing=ausentes,
        wikilinks=_wikilinks_de(cuerpo, zonas, config),
        marks=_marcas_de(cuerpo, zonas, config),
        sources=_fuentes_de(cuerpo),
        content_hash=sha256_text(texto),
    )


def C1_parseo(notas: List[Tuple[Path, str]], config: PublishConfig) -> List[ParsedConcept]:
    """Parsea cada nota de la lista de inclusion. No resuelve links ni asigna uids."""
    return [C1_parseo_nota(ruta, config, id_temporal) for ruta, id_temporal in notas]
