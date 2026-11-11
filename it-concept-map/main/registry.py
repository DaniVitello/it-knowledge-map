"""Registry: carga de conceptos desde el vault (Capa 2).

Responsabilidades:
- Descubrir notas .md segun el glob/exclude configurados.
- Parsear frontmatter YAML.
- Extraer key_ideas (bullets de "Que abarca") y connections (wikilinks de "Relacionados").
- Calcular id (slug del path), hashes (outside/inside) y metadatos de lectura.
- Derivar ConceptMeta a partir de la nota + config (overrides por concepto/area).

No escribe en el vault.
"""

from __future__ import annotations

import hashlib
import os
import re
import unicodedata
from pathlib import Path
from typing import Any

import yaml

from . import areas as areas_mod
from .models import (
    ConceptMeta,
    Volatility,
    ConceptModelError,
    InvalidFrontmatterError,
    MissingRequiredFieldError,
)

MARKER_START_DEFAULT = "<!-- ai:start -->"
MARKER_END_DEFAULT = "<!-- ai:end -->"

DEFAULT_KEY_IDEA_HEADINGS = [
    "que abarca",
    "que cubre",
    "que incluye",
    "contenido",
    "key ideas",
    "ideas clave",
]

DEFAULT_CONNECTION_HEADINGS = [
    "relacionados",
    "conexiones",
    "connections",
    "relacionados y conexiones",
]

DEFAULT_EXCLUDE_GLOBS = ["**/00 - *", "**/_*", "**/README.md"]


# ---------------------------------------------------------------------------
# Helpers de config
# ---------------------------------------------------------------------------


def _cfg(config: Any, *keys: str, default: Any = None) -> Any:
    """Acceso seguro a config (dict u objeto), con fallback."""
    cur = config
    if cur is None:
        return default
    for key in keys:
        if isinstance(cur, dict):
            if key in cur:
                cur = cur[key]
            else:
                return default
        elif hasattr(cur, key):
            cur = getattr(cur, key)
        else:
            return default
    return cur if cur is not None else default


def _markers(config: Any) -> tuple[str, str]:
    start = _cfg(config, "markers", "start", default=None)
    if start is None:
        start = _cfg(config, "marker_start", default=None)
    if start is None:
        start = MARKER_START_DEFAULT
    end = _cfg(config, "markers", "end", default=None)
    if end is None:
        end = _cfg(config, "marker_end", default=None)
    if end is None:
        end = MARKER_END_DEFAULT
    return str(start), str(end)


# ---------------------------------------------------------------------------
# Normalizacion de texto
# ---------------------------------------------------------------------------


def _strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _norm_heading(text: str) -> str:
    return _strip_accents(text).strip().lower()


def slugify_path(rel_path: Path) -> str:
    """Slug del path relativo al vault root (id estable)."""
    text = str(rel_path.with_suffix(""))
    # normalizar separadores
    text = text.replace("\\", "/")
    # colapsar espacios y caracteres no alfanumericos a guion
    text = _strip_accents(text).lower()
    text = re.sub(r"[^a-z0-9/]+", "-", text)
    text = text.replace("/", "-")
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-")
    return text or "concept"


# ---------------------------------------------------------------------------
# Lectura de archivo
# ---------------------------------------------------------------------------


def detect_newline(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    return "\n"


def has_bom_bytes(raw: bytes) -> bool:
    return raw.startswith(b"\xef\xbb\xbf")


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, bool]:
    """Devuelve (frontmatter_dict, body, has_frontmatter).

    Lanza InvalidFrontmatterError si el bloque YAML es invalido.
    """
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith("---"):
        return None, text, False
    # encontrar cierre
    lines = stripped.splitlines(keepends=True)
    # primera linea debe ser --- (posiblemente con trailing)
    if not re.match(r"^---\s*$", lines[0].strip()):
        return None, text, False
    end_idx = None
    for i in range(1, len(lines)):
        if re.match(r"^---\s*$", lines[i].strip()):
            end_idx = i
            break
    if end_idx is None:
        # sin cierre valido -> no frontmatter
        return None, text, False
    fm_text = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1:])
    # preservar offset del BOM: body ya sin fm
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        raise InvalidFrontmatterError(f"YAML invalido en frontmatter: {exc}") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise InvalidFrontmatterError("El frontmatter no es un mapping YAML")
    return data, body, True


def find_markers(text: str, marker_start: str = MARKER_START_DEFAULT,
                 marker_end: str = MARKER_END_DEFAULT) -> dict[str, Any] | None:
    """Busca exactamente un start y un end, en ese orden. None si no valido."""
    lines = text.splitlines(keepends=True)
    starts = [i for i, ln in enumerate(lines) if marker_start in ln]
    ends = [i for i, ln in enumerate(lines) if marker_end in ln]
    if len(starts) != 1 or len(ends) != 1:
        return None
    if starts[0] >= ends[0]:
        return None
    s, e = starts[0], ends[0]
    inside_lines = lines[s + 1:e]
    raw_inside = "".join(inside_lines)
    return {
        "start_line": s,
        "end_line": e,
        "inside_start": s + 1,
        "inside_end": e,
        "raw_inside": raw_inside,
    }


def extract_outside(text: str, marker_start: str = MARKER_START_DEFAULT,
                    marker_end: str = MARKER_END_DEFAULT) -> str | None:
    span = find_markers(text, marker_start, marker_end)
    if span is None:
        return None
    lines = text.splitlines(keepends=True)
    outside_lines = lines[:span["start_line"] + 1] + lines[span["end_line"]:]
    return "".join(outside_lines)


def content_hash_outside(text: str, marker_start: str = MARKER_START_DEFAULT,
                        marker_end: str = MARKER_END_DEFAULT) -> str | None:
    outside = extract_outside(text, marker_start, marker_end)
    if outside is None:
        return None
    return hashlib.sha256(outside.encode("utf-8")).hexdigest()


def content_hash_inside(text: str, marker_start: str = MARKER_START_DEFAULT,
                       marker_end: str = MARKER_END_DEFAULT) -> str | None:
    span = find_markers(text, marker_start, marker_end)
    if span is None:
        return None
    return hashlib.sha256(span["raw_inside"].encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Extraccion de contenido estructurado
# ---------------------------------------------------------------------------


def _section_lines(body: str, headings: list[str]) -> list[str]:
    """Devuelve las lineas del cuerpo que pertenecen a una seccion cuyo heading
    normalizado esta en ``headings``. La seccion termina en el siguiente heading
    de nivel <= 2 (## o #)."""
    lines = body.splitlines()
    target = {_norm_heading(h) for h in headings}
    out: list[str] = []
    in_section = False
    section_level = None
    for ln in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", ln.strip())
        if m:
            level = len(m.group(1))
            title = _norm_heading(m.group(2))
            if in_section:
                if level <= (section_level or 2):
                    break
                # sub-heading dentro de la seccion: incluir
                out.append(ln)
                continue
            if title in target:
                in_section = True
                section_level = level
                continue
            continue
        if in_section:
            out.append(ln)
    return out


def extract_key_ideas(body: str, headings: list[str] | None = None) -> list[str]:
    hs = headings or DEFAULT_KEY_IDEA_HEADINGS
    lines = _section_lines(body, hs)
    ideas: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        # bullets
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            ideas.append(m.group(1).strip())
            continue
        # headings secundarios se ignoran; texto suelto no se toma como idea
    # dedup preservando orden
    seen: set[str] = set()
    out: list[str] = []
    for idea in ideas:
        key = idea.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(idea)
    return out


def _extract_wikilinks(text: str) -> list[str]:
    found = re.findall(r"\[\[([^\]]+)\]\]", text)
    out: list[str] = []
    seen: set[str] = set()
    for raw in found:
        # display title si existe
        target = raw.split("|", 1)[0].strip()
        display = raw.split("|", 1)[1].strip() if "|" in raw else target
        # elegir display title si es legible, si no el basename del target
        value = display or target
        if "/" in value and "|" not in raw:
            value = value.split("/")[-1].strip()
        # limpiar extension
        value = re.sub(r"\.md$", "", value).strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def extract_connections(body: str, headings: list[str] | None = None,
                       own_title: str | None = None) -> list[str]:
    hs = headings or DEFAULT_CONNECTION_HEADINGS
    section = _section_lines(body, hs)
    if section:
        trimmed = []
        for ln in section:
            if ln.strip().startswith("---"):
                break
            trimmed.append(ln)
        bullet_links = []
        for ln in trimmed:
            st = ln.strip()
            if __import__("re").match(r"^[-*+]\s+", st):
                bullet_links.extend(_extract_wikilinks(st))
        if bullet_links:
            links = bullet_links
        else:
            links = _extract_wikilinks("\n".join(trimmed))
    else:
        # fallback: todos los wikilinks del cuerpo excepto indices y la propia nota
        links = _extract_wikilinks(body)
        filtered: list[str] = []
        for lk in links:
            low = lk.lower()
            if low.startswith("_") or "indice" in low or "índice" in low:
                continue
            if own_title and low == own_title.lower():
                continue
            filtered.append(lk)
        links = filtered
    # filtrar indices y dedup
    filtered: list[str] = []
    seen: set[str] = set()
    for lk in links:
        low = _strip_accents(lk).lower()
        if low.startswith("_") or "indice" in low:
            continue
        if low.startswith("00 "):
            continue
        key = lk.lower()
        if key in seen:
            continue
        seen.add(key)
        filtered.append(lk)
    return filtered


# ---------------------------------------------------------------------------
# Derivacion de ConceptMeta
# ---------------------------------------------------------------------------


def _first_h1(body: str) -> str | None:
    for ln in body.splitlines():
        m = re.match(r"^#\s+(.+)$", ln.strip())
        if m:
            return m.group(1).strip()
    return None


def _title_from_filename(path: Path) -> str:
    name = path.stem
    # quitar prefijo numerico "01 - " o "01. "
    name = re.sub(r"^\d+\s*[-._]\s*", "", name)
    return name.strip() or path.stem


def _area_from_path(path: Path, vault_root: Path) -> str:
    try:
        rel = path.relative_to(vault_root)
    except ValueError:
        rel = path
    parts = rel.parts
    if len(parts) > 1:
        folder = parts[0]
        # limpiar prefijo numerico
        folder = re.sub(r"^\d+\s*[-._]\s*", "", folder).strip()
        return folder or parts[0]
    return ""


def _default_volatility(area: str, tags: list[str], config: Any) -> Volatility:
    """Volatilidad sin area yaml (areas desconocidas): config/concept overrides y tags."""
    co = _cfg(config, "concepts", area, default=None)
    if co is None:
        co = _cfg(config, "concept_overrides", area, default=None)
    if isinstance(co, dict):
        v = co.get("volatility")
        if v is not None:
            try:
                return Volatility(str(v).lower())
            except ValueError:
                pass
    # tags
    low_tags = [t.lower() for t in tags]
    if "dynamic" in low_tags:
        return Volatility.DYNAMIC
    if "stable" in low_tags:
        return Volatility.STABLE
    return Volatility.SEMI_STABLE


def read_concept(path: Path, vault_root: Path, config: Any = None) -> ConceptMeta:
    """Lee una nota del vault y deriva un ConceptMeta."""
    raw_bytes = path.read_bytes()
    bom = has_bom_bytes(raw_bytes)
    text = raw_bytes.decode("utf-8")
    if bom:
        text = text.lstrip("\ufeff")
    newline = detect_newline(text)
    m_start, m_end = _markers(config)

    # frontmatter
    fm, body, has_fm = parse_frontmatter(text)
    # si hubo BOM, has_fm ya considerado sobre stripped; text original tenia BOM removido arriba
    # recalcular con bom handling: re-parse original preserved; ok

    # titulo
    title = None
    if isinstance(fm, dict):
        title = fm.get("title")
    if not title:
        title = _first_h1(body)
    if not title:
        title = _title_from_filename(path)
    if not title:
        raise MissingRequiredFieldError(f"No se pudo derivar title para {path}")

    # area
    area = None
    if isinstance(fm, dict):
        area = fm.get("area")
    if not area:
        area = _area_from_path(path, vault_root)
    if not area:
        raise MissingRequiredFieldError(f"No se pudo derivar area para {path}")

    # tags/aliases/numero
    aliases = []
    tags = []
    numero = None
    if isinstance(fm, dict):
        aliases = fm.get("aliases") or []
        tags = fm.get("tags") or []
        numero = fm.get("numero")
    aliases = [str(a) for a in aliases]
    tags = [str(t).lstrip("#").lower() for t in tags]
    if numero is not None:
        try:
            numero = int(numero)
        except (TypeError, ValueError):
            numero = None

    # key_ideas headings configurables
    ki_headings = _cfg(config, "key_ideas_headings", default=None)
    if not isinstance(ki_headings, list):
        ki_headings = _cfg(config, "headings", "key_ideas", default=None)
    if not isinstance(ki_headings, list):
        ki_headings = DEFAULT_KEY_IDEA_HEADINGS
    conn_headings = _cfg(config, "connections_headings", default=None)
    if not isinstance(conn_headings, list):
        conn_headings = _cfg(config, "headings", "connections", default=None)
    if not isinstance(conn_headings, list):
        conn_headings = DEFAULT_CONNECTION_HEADINGS

    key_ideas = extract_key_ideas(body, ki_headings)
    connections = extract_connections(body, conn_headings, own_title=title)

    # markers / hashes
    span = find_markers(text, m_start, m_end)
    has_block = span is not None
    outside_hash = content_hash_outside(text, m_start, m_end) if has_block else None
    inside_hash = content_hash_inside(text, m_start, m_end) if has_block else None

    # concept id
    try:
        rel = path.relative_to(vault_root)
    except ValueError:
        rel = path
    concept_id = slugify_path(rel)

    # overrides — Capa D: areas/<area>.yaml es la fuente de verdad.
    # Merge: concept override > area yaml > frontmatter > defaults (areas.py).
    area_res = areas_mod.resolve_for_concept(concept_id, str(area), config=config, frontmatter=fm)
    volatility = area_res["volatility"]
    roles = area_res["professional_roles"]
    domains = area_res["preferred_domains"]
    seeds = area_res["seed_urls"]
    if not roles:
        # fallback legado SOLO para areas sin yaml (las 10 areas definidas lo tienen).
        roles = [f"{str(area).lower().replace(' ', '-')}-dev"]

    # concept_dir
    workdir = _cfg(config, "workdir", default=None)
    if workdir is None:
        workdir = _cfg(config, "workdir_path", default=None)
    concept_dir = None
    if workdir:
        concept_dir = Path(workdir) / "concepts" / concept_id

    mtime = None
    try:
        mtime = path.stat().st_mtime
    except OSError:
        mtime = None

    return ConceptMeta(
        id=concept_id,
        concept_id=concept_id,
        title=str(title),
        area=str(area),
        note_path=path.resolve(),
        path=str(path.resolve()),
        slug=concept_id,
        numero=numero,
        aliases=aliases,
        tags=tags,
        key_ideas=key_ideas,
        connections=connections,
        frontmatter=fm,
        volatility=volatility,
        professional_roles=roles,
        preferred_domains=domains,
        seed_urls=seeds,
        has_ai_block=has_block,
        content_hash_outside=outside_hash,
        content_hash_inside=inside_hash,
        content_hash_outside_ai=outside_hash,
        outside_hash_at_read=outside_hash,
        mtime_at_read=mtime,
        newline=newline,
        has_frontmatter=has_fm,
        has_bom=bom,
        concept_dir=concept_dir,
    )


def scan_vault(vault_root: Path, config: Any = None,
               glob_pattern: str = "**/*.md") -> tuple[list[ConceptMeta], list[Path]]:
    """Descubre conceptos del vault.

    Devuelve (conceptos, notas_sin_bloque). Excluye archivos segun exclude_globs.
    """
    vault_root = Path(vault_root).resolve()
    exclude_globs = _cfg(config, "exclude_globs", default=None)
    if not isinstance(exclude_globs, list):
        exclude_globs = DEFAULT_EXCLUDE_GLOBS
    include_glob = _cfg(config, "include_glob", default=None) or _cfg(config, "glob", default=None)
    if isinstance(include_glob, str):
        glob_pattern = include_glob

    candidates: list[Path] = []
    for p in vault_root.glob(glob_pattern):
        if not p.is_file():
            continue
        # exclude
        rel = p.relative_to(vault_root).as_posix()
        skip = False
        for eg in exclude_globs:
            if Path(rel).match(eg) or _glob_match(rel, eg):
                skip = True
                break
        if skip:
            continue
        candidates.append(p)

    concepts: list[ConceptMeta] = []
    without_block: list[Path] = []
    seen_ids: set[str] = set()
    for p in sorted(candidates):
        # leer para detectar bloque
        try:
            raw = p.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        m_start, m_end = _markers(config)
        span = find_markers(text, m_start, m_end)
        if span is None:
            without_block.append(p)
            continue
        try:
            concept = read_concept(p, vault_root, config)
        except (ConceptModelError, OSError, UnicodeDecodeError, ValueError):
            without_block.append(p)
            continue
        if concept.id in seen_ids:
            raise ConceptModelError(f"Colision de concept_id: {concept.id} ({p})")
        seen_ids.add(concept.id)
        concepts.append(concept)

    return concepts, without_block


def _glob_match(rel: str, pattern: str) -> bool:
    """Match simple de glob contra path relativo (soporta **)."""
    import fnmatch
    # convertir ** a * para fnmatch (aprox)
    pat = pattern.replace("**/", "*")
    return fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(Path(rel).name, pattern)


def load_concepts(vault_path: str | Path, config: Any = None) -> list[ConceptMeta]:
    """API de conveniencia: devuelve solo la lista de conceptos."""
    concepts, _ = scan_vault(Path(vault_path), config)
    return concepts