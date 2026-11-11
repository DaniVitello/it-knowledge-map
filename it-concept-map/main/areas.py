"""Capa D - Contexto por area: cargador de areas/<area>.yaml.

Hace que areas.json ( rol senior, orientacion, ejemplo/estilo, modo, fuentes
preferidas) sea la fuente de verdad para el contexto por area, con la
estructura del diseno 7.1 (auditoria D18):

    areas/<area>.yaml con: context_framing, context_questions,
    professional_roles, style_example, response_mode, preferred_domains,
    seed_urls, default_volatility + volatility_overrides.

Merge de prioridad al resolver por concepto (igual criterio que el registry):

    override por concepto > areas/<area>.yaml > frontmatter > defaults.

En adelante los prompts (sintesis, y despues investigacion/validacion)
inyectan este contexto por area en lugar de "Sos un experto en {area}".
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .models import Volatility

SCHEMA_VERSION = "1.0.0"

# Directorio por defecto: it-concept-map/areas/ (junto al modulo).
AREAS_DIR = Path(__file__).resolve().parent / "areas"

# Areas definidas (10, desde areas.json). Usado por los tests de cobertura.
EXPECTED_AREAS = sorted([
    "Software Engineering",
    "Frontend",
    "Backend",
    "Database / Data Analytics",
    "Networking / Internet",
    "Operating Systems / Linux",
    "AI Engineering",
    "UX / UI",
    "Product Management",
    "Project Management",
])


class AreaConfigError(Exception):
    """Error leyendo areas/<area>.yaml (estructura invalida)."""


def slugify_area(text: str) -> str:
    """Slug de nombre de area: "Database & Data Analytics" -> database-data-analytics.

    Normaliza &, / y otros separadores a guion, sin acentos y en minuscula:
    variantes del mismo nombre ("Database / Data Analytics" vs
    "Database & Data Analytics") colapsan al mismo slug.
    """
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


@dataclass
class AreaContext:
    """Contexto profesional de un area (areas/<area>.yaml)."""

    name: str
    context_framing: str = ""
    context_questions: list[str] = field(default_factory=list)
    professional_roles: list[str] = field(default_factory=list)
    style_example: str = ""
    response_mode: str = ""
    preferred_domains: list[str] = field(default_factory=list)
    seed_urls: list[str] = field(default_factory=list)
    default_volatility: Volatility = Volatility.SEMI_STABLE
    volatility_overrides: dict[str, str] = field(default_factory=dict)
    path: Path | None = None

    schema_version: str = SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------


def load_area_yaml(path: Path) -> AreaContext:
    """Lee un archivo areas/<area>.yaml y devuelve el AreaContext validado."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise AreaConfigError(f"No se pudo leer {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise AreaConfigError(f"YAML invalido en {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise AreaConfigError(f"{path} no es un mapping YAML")
    name = data.get("area")
    if not name or not str(name).strip():
        raise AreaConfigError(f"{path} no define 'area'")
    roles = data.get("professional_roles") or []
    if not isinstance(roles, list):
        raise AreaConfigError(f"{path}: professional_roles debe ser una lista")
    domains = data.get("preferred_domains") or []
    if not isinstance(domains, list):
        raise AreaConfigError(f"{path}: preferred_domains debe ser una lista")
    seeds = data.get("seed_urls") or []
    if not isinstance(seeds, list):
        raise AreaConfigError(f"{path}: seed_urls debe ser una lista")
    questions = data.get("context_questions") or []
    if not isinstance(questions, list):
        raise AreaConfigError(f"{path}: context_questions debe ser una lista")
    overrides = data.get("volatility_overrides") or {}
    if not isinstance(overrides, dict):
        raise AreaConfigError(f"{path}: volatility_overrides debe ser un mapping")
    try:
        volatility = Volatility(str(data.get("default_volatility", "semi_stable")).lower())
    except ValueError as exc:
        raise AreaConfigError(
            f"{path}: default_volatility invalido: {data.get('default_volatility')}"
        ) from exc
    return AreaContext(
        name=str(name).strip(),
        context_framing=str(data.get("context_framing") or "").strip(),
        context_questions=[str(q).strip() for q in questions if str(q).strip()],
        professional_roles=[str(r).strip() for r in roles if str(r).strip()],
        style_example=str(data.get("style_example") or "").strip(),
        response_mode=str(data.get("response_mode") or "").strip().lower(),
        preferred_domains=[str(d).strip() for d in domains if str(d).strip()],
        seed_urls=[str(s).strip() for s in seeds if str(s).strip()],
        default_volatility=volatility,
        volatility_overrides={str(k): str(v) for k, v in overrides.items()},
        path=path,
    )


def load_areas(areas_dir: Path | str | None = None) -> dict[str, AreaContext]:
    """Carga todos los areas/*.yaml indexados por nombre (ci) y por slug."""
    directory = Path(areas_dir) if areas_dir else AREAS_DIR
    areas: dict[str, AreaContext] = {}
    if not directory.is_dir():
        return areas
    for path in sorted(directory.glob("*.yaml")):
        ctx = load_area_yaml(path)
        areas[ctx.name.lower()] = ctx
        areas[slugify_area(ctx.name)] = ctx
    return areas


def load_area(area: str, areas_dir: Path | str | None = None) -> AreaContext | None:
    """Devuelve el AreaContext de un area por nombre/slug, o None si no existe."""
    if not area:
        return None
    areas = load_areas(areas_dir)
    for key in (str(area).strip().lower(), slugify_area(area)):
        ctx = areas.get(key)
        if ctx is not None:
            return ctx
    return None


# ---------------------------------------------------------------------------
# Resolucion por concepto (merge de prioridad)
# ---------------------------------------------------------------------------


def _concept_override(config: Any, concept_id: str) -> dict | None:
    """Override por concepto desde config.yaml (concepts/cli / concept_overrides/)."""
    if not isinstance(config, dict):
        return None
    co = config.get("concepts") or config.get("concept_overrides") or {}
    if isinstance(co, dict):
        entry = co.get(concept_id)
        if isinstance(entry, dict):
            return entry
    return None


def _first_list(*lists: Any) -> list[str]:
    """Primera lista no vacia de las pasadas (prioridad de izq a der)."""
    for value in lists:
        if isinstance(value, list) and value:
            return [str(v).strip() for v in value if str(v).strip()]
    return []


def _resolve_volatility(concept_id: str, area_ctx: AreaContext | None,
                        config: Any, frontmatter: dict | None) -> Volatility:
    """Volatilidad: concept override > area volatility_overrides > default_volatility > tags."""
    co = _concept_override(config, concept_id)
    if co is not None and co.get("volatility") is not None:
        try:
            return Volatility(str(co["volatility"]).lower())
        except ValueError:
            pass
    if area_ctx is not None:
        ov = area_ctx.volatility_overrides.get(concept_id)
        if ov is None:
            # permitir override por slug tambien
            ov = area_ctx.volatility_overrides.get(slugify_area(concept_id))
        if ov is not None:
            try:
                return Volatility(str(ov).lower())
            except ValueError:
                pass
        return area_ctx.default_volatility
    # fallback sin area yaml: tags del frontmatter
    tags = (frontmatter or {}).get("tags") or []
    low_tags = [str(t).lstrip("#").lower() for t in tags]
    if "dynamic" in low_tags:
        return Volatility.DYNAMIC
    if "stable" in low_tags:
        return Volatility.STABLE
    return Volatility.SEMI_STABLE


def resolve_for_concept(concept_id: str, area: str, config: Any = None,
                        frontmatter: dict | None = None,
                        areas_dir: Path | str | None = None) -> dict:
    """Resuelve el contexto de area para un concepto con merge de prioridad:

        override por concepto > areas/<area>.yaml > frontmatter > defaults.

    Devuelve un dict con: volatility, professional_roles, preferred_domains,
    seed_urls, context_framing, context_questions, style_example,
    response_mode, area_yaml (o None) y expected_domains_yaml (true si los
    dominios vienen del yaml del area).
    """
    area_ctx = load_area(area, areas_dir=areas_dir)
    co = _concept_override(config, concept_id) or {}
    fm = frontmatter or {}

    roles = _first_list(co.get("professional_roles"), co.get("roles"),
                        area_ctx.professional_roles if area_ctx else None,
                        fm.get("professional_roles"), fm.get("roles"))
    domains = _first_list(co.get("preferred_domains"),
                          area_ctx.preferred_domains if area_ctx else None,
                          fm.get("preferred_domains"))
    seeds = _first_list(co.get("seed_urls"),
                        area_ctx.seed_urls if area_ctx else None,
                        fm.get("seed_urls"))
    # defaults globales de config (strategy) se agregan al final sin duplicar.
    if isinstance(config, dict):
        strategy = config.get("strategy") or {}
        if isinstance(strategy, dict):
            for key, target in (("preferred_domains", domains), ("seed_urls", seeds)):
                global_val = strategy.get(key)
                if isinstance(global_val, list):
                    for item in global_val:
                        item_s = str(item).strip()
                        if item_s and item_s not in target:
                            target.append(item_s)

    return {
        "area": str(area),
        "area_yaml": area_ctx,
        "volatility": _resolve_volatility(concept_id, area_ctx, config, fm),
        "professional_roles": roles,
        "preferred_domains": domains,
        "seed_urls": seeds,
        "context_framing": (co.get("context_framing")
                            or (area_ctx.context_framing if area_ctx else "")
                            or str(fm.get("context_framing") or "")),
        "context_questions": (co.get("context_questions")
                              or (area_ctx.context_questions if area_ctx else [])
                              or list(fm.get("context_questions") or [])),
        "style_example": (co.get("style_example")
                          or (area_ctx.style_example if area_ctx else "")
                          or str(fm.get("style_example") or "")),
        "response_mode": (co.get("response_mode")
                          or (area_ctx.response_mode if area_ctx else "")
                          or str(fm.get("response_mode") or "")).lower(),
    }
