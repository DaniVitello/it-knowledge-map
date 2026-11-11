"""Escritura segura del vault (Capa 3 de implementacion / Capa 5 del diseno).

Responsabilidades:
- ``SafeWriter``: la UNICA pieza que modifica el vault. Escribe de forma
  atomica (temp + ``os.replace``), hace backup antes y restaura byte a byte
  si alguna verificacion falla.
- Reemplazo del interior del bloque ``ai:start``/``ai:end`` (unicamente esa
  zona: ``find_markers``, ``count_markers``, ``replace_inside``).
- Integridad del "afuera" (todo excepto el interior del bloque):
  ``extract_outside``, ``sha256``, ``verify_outside_integrity``.
- Preservacion byte a byte del frontmatter YAML (``parse_frontmatter``,
  ``verify_frontmatter_preserved``). El writer NUNCA reescribe el frontmatter.
- Respeto de newlines del archivo original (``detect_newline``,
  ``normalize_newlines``).
- Excepciones tipadas del writer.
- Integracion con ``state.py``: transiciones
  ``validated -> written -> completed`` (y ``failed`` ante cualquier error).

Reglas de negocio (de la spec):
- Solo se modifica el interior del bloque. Todo lo demas se verifica.
- Si faltan marcadores, NO se insertan automaticamente: el concepto queda
  ``failed`` (salvo config explicita, no implementada aqui por defecto).
- Backup ANTES de escribir, en ``workdir/backups/<concept_id>/``.
- Hash SHA-256 del afuera antes y despues; verificacion releyendo desde disco.
- Escritura atomica: tmp en ``workdir/tmp`` (mismo filesystem del vault;
  el workdir vive junto al vault en el mismo arbol) + ``os.replace``.
- Frontmatter/title/area/key_ideas/connections nunca se tocan.
"""

from __future__ import annotations

import difflib
import hashlib
import os
import re
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from .models import ConceptMeta, Synthesis, WriteResult, now_iso
from .state import (
    ConceptState,
    ConceptStatus,
    InvalidTransitionError,
    load_state,
    save_state,
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

WRITER_VERSION = "1.0.0"

MARKER_START_DEFAULT = "<!-- ai:start -->"
MARKER_END_DEFAULT = "<!-- ai:end -->"

# Headings de la "voz del autor" que deben seguir presentes tras escribir.
REQUIRED_HEADINGS: tuple[str, ...] = ("Que abarca", "Relacionados")


def _cfg(config: Any, *keys: str, default: Any = None) -> Any:
    """Lee una ruta de claves de un config (mapping u objeto). Helper local."""
    cur: Any = config
    if cur is None:
        return default
    for key in keys:
        if isinstance(cur, Mapping):
            if key in cur:
                cur = cur[key]
            else:
                return default
        elif hasattr(cur, key):
            cur = getattr(cur, key)
        else:
            return default
    return cur if cur is not None else default


def now_iso_compact() -> str:
    """Timestamp compacto para nombres de archivo: 20261023T101500Z-a1b2c3."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}-{uuid.uuid4().hex[:6]}"


# ---------------------------------------------------------------------------
# Excepciones del writer
# ---------------------------------------------------------------------------


class WriterError(Exception):
    """Error base del writer."""


class VerificationError(WriterError):
    """Familia de errores de verificacion post-escritura."""


class MissingMarkersError(WriterError):
    """No hay ``ai:start`` o ``ai:end`` en una de las dos formas."""


class DuplicateMarkersError(WriterError):
    """Mas de un marcador (start o end) en la nota."""


class MarkerOrderError(WriterError):
    """Los marcadores estan en orden incorrecto (start despues de end)."""


class ConcurrentEditError(WriterError):
    """El archivo cambio entre la lectura (scan) y la escritura."""


class OutsideIntegrityError(VerificationError):
    """El hash SHA-256 del afuera difiere antes/despues de escribir."""

    def __init__(self, expected: str, actual: str) -> None:
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"Hash del afuera difiere: expected={expected} actual={actual}"
        )


class OutsideByteMismatchError(VerificationError):
    """El afuera difiere byte a byte (aunque los hashes coincidieran)."""


class FrontmatterChangedError(VerificationError):
    """El bloque ---...--- del frontmatter difiere byte a byte."""


class FrontmatterSemanticMismatchError(VerificationError):
    """El frontmatter difiere semanticamente (dict YAML distinto)."""


class InsideMismatchError(VerificationError):
    """El interior escrito no coincide con la sintesis validada."""


class MarkerCountError(VerificationError):
    """Tras escribir, los marcadores no son exactamente uno de cada."""


class HeadingsChangedError(VerificationError):
    """Un heading obligatorio desaparecio tras escribir."""


class WikilinksChangedError(VerificationError):
    """Los wikilinks del afuera cambiaron tras escribir."""


class WriteFailedError(WriterError):
    """Fallo generico de la escritura (tras intento de restore o IO)."""

    def __init__(self, path: Path, reason: Any = None) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Escritura fallida en {path}: {reason!r}")


# ---------------------------------------------------------------------------
# Newlines
# ---------------------------------------------------------------------------


def detect_newline(text: str) -> str:
    """Detecta el fin de linea dominante del archivo: ``\\r\\n`` o ``\\n``."""
    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    return "\r\n" if crlf > lf else "\n"


def normalize_newlines(text: str, target: str) -> str:
    """Unifica todo a ``\\n`` y luego convierte al estilo ``target``."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if target == "\r\n":
        text = text.replace("\n", "\r\n")
    return text


# ---------------------------------------------------------------------------
# Marcadores y bloque
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MarkerSpan:
    """Posicion del bloque ``ai:start``/``ai:end`` en la nota."""

    start_line: int      # indice de la linea del marcador start
    end_line: int        # indice de la linea del marcador end
    inside_start: int    # primera linea del interior (exclusiva del start)
    inside_end: int      # ultima linea del interior (exclusiva del end)
    raw_inside: str      # texto actual del interior (con newlines originales)


def find_markers(
    text: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> MarkerSpan | None:
    """Busca exactamente un start y un end, en ese orden. None si no valido."""
    lines = text.splitlines(keepends=True)
    starts = [i for i, ln in enumerate(lines) if marker_start in ln]
    ends = [i for i, ln in enumerate(lines) if marker_end in ln]
    if len(starts) != 1 or len(ends) != 1:
        return None
    if starts[0] >= ends[0]:
        return None
    s, e = starts[0], ends[0]
    return MarkerSpan(
        start_line=s,
        end_line=e,
        inside_start=s + 1,
        inside_end=e,
        raw_inside="".join(lines[s + 1 : e]),
    )


def count_markers(
    text: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> tuple[int, int]:
    """Cantidad de marcadores start/end en la nota (busqueda por subcadena)."""
    return (text.count(marker_start), text.count(marker_end))


def replace_inside(
    text: str,
    span: MarkerSpan,
    new_inside: str,
    newline: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> str:
    """Reemplaza SOLO el interior del bloque; los marcadores quedan verbatim.

    - El interior nuevo se normaliza al newline del archivo.
    - Si el interior queda vacio, se deja una linea vacia entre marcadores.
    """
    del marker_start, marker_end  # respetan la firma del diseno
    lines = text.splitlines(keepends=True)
    before = "".join(lines[: span.start_line + 1])   # incluye linea del start
    after = "".join(lines[span.end_line :])          # desde la linea del end
    inside = normalize_newlines(new_inside, newline) if new_inside else ""
    if inside and not inside.endswith(newline):
        inside += newline
    if not inside:
        inside = newline  # deja una linea vacia entre marcadores
    return before + inside + after


# ---------------------------------------------------------------------------
# Hash del afuera (integridad)
# ---------------------------------------------------------------------------


def sha256(text: str) -> str:
    """SHA-256 hex de un texto UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_outside(
    text: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> str:
    """TODO el texto EXCEPTO el interior del bloque (los marcadores se incluyen).

    Lanza ``MissingMarkersError`` si la nota no tiene un bloque valido.
    """
    span = find_markers(text, marker_start, marker_end)
    if span is None:
        raise MissingMarkersError(
            "extract_outside requiere un bloque ai:start/ai:end valido"
        )
    lines = text.splitlines(keepends=True)
    before = "".join(lines[: span.inside_start])  # incluye marcador start
    after = "".join(lines[span.inside_end :])     # incluye marcador end en adelante
    return before + after


def content_hash_outside(
    text: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> str | None:
    """SHA-256 del afuera; None si la nota no tiene bloque valido."""
    span = find_markers(text, marker_start, marker_end)
    if span is None:
        return None
    return sha256(extract_outside(text, marker_start, marker_end))


def content_hash_inside(
    text: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> str | None:
    """SHA-256 del interior actual del bloque; None si no hay bloque."""
    span = find_markers(text, marker_start, marker_end)
    if span is None:
        return None
    return sha256(span.raw_inside)


def verify_outside_integrity(
    original_text: str,
    written_text: str,
    outside_hash_before: str,
    marker_start: str = MARKER_START_DEFAULT,
    marker_end: str = MARKER_END_DEFAULT,
) -> str:
    """Verifica que el afuera no cambio: hash antes/despues + byte a byte.

    Devuelve el hash del afuera observado en ``written_text``.
    """
    outside_after = extract_outside(written_text, marker_start, marker_end)
    outside_hash_after = sha256(outside_after)
    if outside_hash_after != outside_hash_before:
        raise OutsideIntegrityError(
            expected=outside_hash_before, actual=outside_hash_after
        )
    # Verificacion adicional byte a byte (no solo hash).
    if extract_outside(original_text, marker_start, marker_end) != outside_after:
        raise OutsideByteMismatchError(
            "El afuera difiere byte a byte entre el original y lo escrito"
        )
    return outside_hash_after


# ---------------------------------------------------------------------------
# Frontmatter (solo verificacion; nunca se reescribe)
# ---------------------------------------------------------------------------

_FM_DELIM = re.compile(r"^---\s*$")


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    """Devuelve ``(frontmatter_dict, body_sin_frontmatter)``.

    ``(None, text)`` si no hay frontmatter. Lanza
    ``models.InvalidFrontmatterError`` si el YAML es invalido.
    """
    stripped = text.lstrip("\ufeff")
    lines = stripped.splitlines(keepends=True)
    if not lines or not _FM_DELIM.match(lines[0].rstrip("\r\n")):
        return None, text
    end_idx: int | None = None
    for i in range(1, len(lines)):
        if _FM_DELIM.match(lines[i].rstrip("\r\n")):
            end_idx = i
            break
    if end_idx is None:
        return None, text
    fm_text = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    data = yaml.safe_load(fm_text)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("El frontmatter no es un mapping YAML")
    return data, body


def extract_frontmatter_block(text: str) -> str | None:
    """Texto del bloque ---...--- inclusive, o None si no hay frontmatter."""
    stripped = text.lstrip("\ufeff")
    lines = stripped.splitlines(keepends=True)
    if not lines or not _FM_DELIM.match(lines[0].rstrip("\r\n")):
        return None
    for i in range(1, len(lines)):
        if _FM_DELIM.match(lines[i].rstrip("\r\n")):
            return "".join(lines[: i + 1])
    return None


def verify_frontmatter_preserved(original: str, written: str) -> None:
    """Frontmatter byte a byte + comparacion semantica como red de seguridad.

    Si la nota no tenia frontmatter, no se agrega ninguno y no hay nada que
    verificar (el afuera ya se verifico byte a byte).
    """
    block_before = extract_frontmatter_block(original)
    if block_before is None:
        return
    block_after = extract_frontmatter_block(written)
    if block_before != block_after:
        raise FrontmatterChangedError(
            "El frontmatter difiere byte a byte entre el original y lo escrito"
        )
    # Red de seguridad: comparacion semantica del dict YAML.
    try:
        fm_before, _ = parse_frontmatter(original)
        fm_after, _ = parse_frontmatter(written)
    except (ValueError, yaml.YAMLError):
        return  # YAML invalido ya cobijado por la comparacion byte a byte
    if fm_before != fm_after:
        raise FrontmatterSemanticMismatchError(
            "El frontmatter difiere semanticamente (dict YAML distinto)"
        )


# ---------------------------------------------------------------------------
# Defensa en profundidad: headings y wikilinks del afuera
# ---------------------------------------------------------------------------


def _accent_less(text: str) -> str:
    """Normaliza acentos simples (suficiente para los headings del vault)."""
    replacements = str.maketrans(
        "áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN"
    )
    return text.translate(replacements)


def _norm_heading(text: str) -> str:
    return _accent_less(text).casefold().strip().strip("?¿!:")


def _heading_texts(text: str) -> list[str]:
    out = []
    for ln in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.*)$", ln.rstrip("\r\n"))
        if match:
            out.append(_norm_heading(match.group(1)))
    return out


def verify_headings_preserved(
    original: str,
    written: str,
    required: Sequence[str] = REQUIRED_HEADINGS,
) -> None:
    """Verifica que los headings obligatorios del original sigan presentes."""
    original_headings = _heading_texts(original)
    written_headings = set(_heading_texts(written))
    for req in required:
        req_norm = _norm_heading(req)
        if not any(req_norm in h for h in original_headings):
            continue  # la nota original nunca lo tuvo: nada que preservar
        if not any(req_norm in h for h in written_headings):
            raise HeadingsChangedError(
                f"Heading obligatorio desaparecio tras escribir: {req!r}"
            )


_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def _wikilink_set(text: str) -> set[str]:
    links: set[str] = set()
    for group in _WIKILINK_RE.findall(text):
        target = group.split("|")[0].split("#")[0]
        target = target.strip()
        if target:
            links.add(target)
    return links


def verify_wikilinks_preserved(original: str, written: str) -> None:
    """Los wikilinks del afuera (seccion Relacionados manual) no cambian."""
    if _wikilink_set(original) != _wikilink_set(written):
        raise WikilinksChangedError(
            "Los wikilinks del afuera cambiaron tras escribir"
        )


# ---------------------------------------------------------------------------
# Render del interior
# ---------------------------------------------------------------------------


def render_inside(synthesis: Synthesis, target_newline: str = "\n", run_id: str | None = None, concept_id: str | None = None) -> str:
    """Markdown de la sintesis validada, normalizado para insertar en el bloque.

    La sintesis llega YA validada (Capa de validacion); el writer no la
    re-valida, solo la normaliza al estilo de newline del archivo destino.
    Si run_id se proporciona, se anade un pie de trazabilidad al final del bloque.
    """
    md = synthesis.markdown or ""
    out = normalize_newlines(md, target_newline).strip("\n")
    if run_id:
        from datetime import datetime, timezone
        footer = "\n\n<!-- trazabilidad: run_id=%s concept=%s written_at=%s -->" % (
            run_id, concept_id or getattr(synthesis, "concept_id", ""), datetime.now(timezone.utc).isoformat(),
        )
        out = out + footer
    return out


# ---------------------------------------------------------------------------
# SafeWriter
# ---------------------------------------------------------------------------


@dataclass
class DiffResult:
    """Resultado del modo dry-run: diff propuesto sin escribir nada."""

    path: Path
    original: str
    proposed: str
    inside_before: str
    inside_after: str
    newline: str
    outside_hash: str  # sha del afuera antes y despues (invariante del dry-run)

    def unified_diff(self, context: int = 2) -> str:
        return "\n".join(
            difflib.unified_diff(
                self.original.splitlines(),
                self.proposed.splitlines(),
                fromfile=f"{self.path} (original)",
                tofile=f"{self.path} (propuesto)",
                lineterm="",
                n=context,
            )
        )


class SafeWriter:
    """Escritura atomica + backup + verificacion. Unica pieza que toca el vault."""

    def __init__(
        self,
        config: Any = None,
        vault_root: Path | str | None = None,
        workdir: Path | str | None = None,
        run_id: str | None = None,
    ) -> None:
        self.config = config
        self.vault_root = Path(vault_root) if vault_root is not None else None
        self.run_id = run_id
        wd = (
            workdir
            or _cfg(config, "workdir", default=None)
            or Path.cwd() / "workdir"
        )
        self.workdir = Path(wd)
        self.backup_root = self.workdir / "backups"
        self.tmp_root = self.workdir / "tmp"  # mismo filesystem que el vault
        self.marker_start = str(
            _cfg(config, "markers", "start", default=MARKER_START_DEFAULT)
        )
        self.marker_end = str(
            _cfg(config, "markers", "end", default=MARKER_END_DEFAULT)
        )

    # -- API principal ------------------------------------------------------

    def write_concept(
        self,
        concept: ConceptMeta,
        synthesis: Synthesis,
        dry_run: bool = False,
    ) -> WriteResult | DiffResult:
        """Escribe la sintesis validada dentro del bloque ai:start/ai:end.

        Flujo: leer bytes -> validar marcadores -> hash del afuera antes ->
        detectar edicion concurrente -> construir texto nuevo ->
        (dry-run: devolver diff) -> backup -> escritura atomica ->
        verificacion releyendo desde disco (ante fallo: restore + error).
        """
        path = Path(concept.note_path)

        # 1. Leer nota completa en bytes y decodificar UTF-8 (BOM se preserva).
        raw_bytes = path.read_bytes()
        original_text = raw_bytes.decode("utf-8")
        newline = detect_newline(original_text)

        # 2. Validar marcadores (fallan con error tipado y preciso).
        span = find_markers(original_text, self.marker_start, self.marker_end)
        if span is None:
            self._raise_marker_error(original_text)

        # 3. Hash del afuera ANTES.
        outside_hash_before = sha256(
            extract_outside(original_text, self.marker_start, self.marker_end)
        )

        # 4. Detectar edicion concurrente (mtime/hash entre scan y ahora).
        if self.concurrent_edit_detected(
            path,
            mtime_at_read=concept.mtime_at_read,
            outside_hash_at_read=(
                concept.outside_hash_at_read or concept.content_hash_outside
            ),
        ):
            raise ConcurrentEditError(
                f"La nota {path} cambio entre la lectura y la escritura"
            )

        # 5. Construir texto nuevo SOLO dentro del bloque.
        new_inside = render_inside(synthesis, target_newline=newline, run_id=self.run_id, concept_id=concept.id)
        new_text = replace_inside(
            original_text, span, new_inside, newline,
            self.marker_start, self.marker_end,
        )
        # Pre-check en memoria antes de tocar disco.
        verify_outside_integrity(
            original_text, new_text, outside_hash_before,
            self.marker_start, self.marker_end,
        )

        # 6. Dry-run: diff propuesto, sin backup ni escritura.
        if dry_run:
            return DiffResult(
                path=path,
                original=original_text,
                proposed=new_text,
                inside_before=span.raw_inside,
                inside_after=new_inside,
                newline=newline,
                outside_hash=outside_hash_before,
            )

        # 7. Backup ANTES de escribir.
        backup_path = self.backup(path, concept.id)

        # 8. Escritura atomica (temp en mismo filesystem + os.replace).
        try:
            tmp_path = self._atomic_write(path, new_text)
        except OSError as exc:
            # El replace falló antes de tocar el destino: la nota original
            # quedó intacta (os.replace es atomico); no hace falta restore.
            raise WriteFailedError(path, reason=exc) from exc

        # 9. Verificar RELEyendo desde disco (no confiar en el buffer).
        try:
            self._verify(
                path, original_text, new_text,
                outside_hash_before, new_inside, concept,
            )
        except VerificationError as exc:
            # Restaurar backup byte a byte (preserva mtime) y fallar.
            self.restore(path, backup_path)
            tmp_path.unlink(missing_ok=True)
            raise WriteFailedError(path, reason=exc) from exc

        return WriteResult(
            path=path,
            backup_path=backup_path,
            outside_hash=outside_hash_before,
            inside_hash=sha256(new_inside),
            written_at=now_iso(),
            success=True,
        )

    # -- Backup / restore ---------------------------------------------------

    def backup(self, path: Path, concept_id: str) -> Path:
        """Copia byte a byte con mtime preservado en workdir/backups/<id>/."""
        dest_dir = self.backup_root / concept_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{path.name}.{now_iso_compact()}.bak"
        shutil.copy2(path, dest)  # copy2 preserva mtime
        return dest

    def restore(self, path: Path, backup_path: Path) -> None:
        """Restaura byte a byte desde el backup (preserva mtime)."""
        shutil.copy2(backup_path, path)

    # Alias con la firma del diseno.
    _backup = backup
    _restore = restore

    # -- Escritura atomica ---------------------------------------------------

    def _atomic_write(self, path: Path, text: str) -> Path:
        """Escribe en un tmp del workdir y hace ``os.replace`` al destino.

        Devuelve la ruta del tmp (ya renombrado por ``os.replace``; la ruta
        en si ya no existe: solo se usa para limpieza best-effort).
        """
        self.tmp_root.mkdir(parents=True, exist_ok=True)
        tmp = self.tmp_root / f"{path.name}.{uuid.uuid4().hex}.tmp"
        tmp.write_bytes(text.encode("utf-8"))  # bytes: control exacto
        os.replace(tmp, path)  # renombre atomico (mismo filesystem)
        return tmp

    # -- Deteccion de edicion concurrente ------------------------------------

    def concurrent_edit_detected(
        self,
        path: Path,
        mtime_at_read: float | None = None,
        outside_hash_at_read: str | None = None,
        mtime_epsilon: float = 0.001,
    ) -> bool:
        """True si el archivo cambio entre la lectura (scan) y ahora.

        - Si hay hash del afuera en el scan, es la referencia autoritativa:
          hash distinto (o bloque de marcadores perdido) -> edicion.
        - Si no hay hash, cae al mtime con epsilon (Obsidian toca el archivo
          a veces sin cambiar contenido; ``shutil.copy2`` preserva mtime para
          no disparar falsos positivos con los backups).
        """
        if outside_hash_at_read:
            # Bytes -> decode: sin traduccion universal de newlines.
            text = self._read_text(path)
            current = content_hash_outside(
                text, self.marker_start, self.marker_end
            )
            if current != outside_hash_at_read:
                return True
            # Hash identico: el contenido del afuera no cambio.
            return False
        if mtime_at_read is not None:
            return abs(path.stat().st_mtime - mtime_at_read) > mtime_epsilon
        return False

    # -- Lectura fiel (bytes; sin traduccion universal de newlines) ------------

    @staticmethod
    def _read_text(path: Path) -> str:
        """Lee el archivo como bytes y decodifica UTF-8.

        ``read_text`` usa newlines universales y traduce ``\\r\\n`` -> ``\\n``;
        eso invalidaria los hashes del afuera en notas CRLF. La regla de la
        capa es hashear \"lo que hay en disco\".
        """
        return path.read_bytes().decode("utf-8")

    # -- Verificacion post-escritura ------------------------------------------

    def _verify(
        self,
        path: Path,
        original_text: str,
        new_text: str,
        outside_hash_before: str,
        new_inside: str,
        concept: ConceptMeta,
    ) -> None:
        """Verifica lo escrito releyendo desde disco; lanza VerificationError."""
        del new_text, concept  # reservados para el contrato del diseno
        written = self._read_text(path)

        # a) hash del afuera antes/despues + byte a byte.
        verify_outside_integrity(
            original_text, written, outside_hash_before,
            self.marker_start, self.marker_end,
        )

        # b) marcadores siguen siendo exactamente uno de cada.
        span = find_markers(written, self.marker_start, self.marker_end)
        if span is None or count_markers(
            written, self.marker_start, self.marker_end
        ) != (1, 1):
            raise MarkerCountError(
                f"Tras escribir, los marcadores no son 1/1 en {path}"
            )

        # c) interior coincide con la sintesis validada.
        expected_inside = normalize_newlines(new_inside, "\n").strip("\n")
        actual_inside = normalize_newlines(span.raw_inside, "\n").strip("\n")
        if actual_inside != expected_inside:
            raise InsideMismatchError(
                "El interior escrito no coincide con la sintesis validada"
            )

        # d) frontmatter byte a byte (+ semantica como red de seguridad).
        verify_frontmatter_preserved(original_text, written)

        # e) defensa en profundidad: headings y wikilinks del afuera.
        verify_headings_preserved(original_text, written)
        verify_wikilinks_preserved(original_text, written)

    # -- Diagnostico de marcadores --------------------------------------------

    def _raise_marker_error(self, text: str) -> None:
        """Convierte ``find_markers -> None`` en el error tipado preciso."""
        n_start, n_end = count_markers(text, self.marker_start, self.marker_end)
        if n_start > 1 or n_end > 1:
            raise DuplicateMarkersError(
                f"Marcadores duplicados: start={n_start} end={n_end}"
            )
        if n_start >= 1 and n_end >= 1:
            raise MarkerOrderError(
                "Los marcadores estan en orden incorrecto (start tras end)"
            )
        raise MissingMarkersError(
            f"La nota no tiene el bloque: start={n_start} end={n_end}"
        )


# ---------------------------------------------------------------------------
# Integracion con state.py (Capa 2): transiciones written/completed
# ---------------------------------------------------------------------------


def record_write_result(state: ConceptState, result: WriteResult) -> None:
    """Guarda el resultado de la escritura en ``phase_data`` del estado."""
    state.phase_data["write_result"] = {
        "backup_path": str(result.backup_path) if result.backup_path else None,
        "outside_hash": result.outside_hash,
        "inside_hash": result.inside_hash,
        "written_at": result.written_at,
        "writer_version": WRITER_VERSION,
    }


def mark_written(
    state: ConceptState,
    result: WriteResult,
    workdir: Any = None,
    config: Any = None,
) -> ConceptState:
    """Transicion ``validated -> written`` (idempotente si ya esta en written).

    Persiste con ``save_state`` (atomico: temp + replace, hecho por state.py).
    """
    if state.status not in (ConceptStatus.WRITTEN, ConceptStatus.COMPLETED):
        state.transition_to(ConceptStatus.WRITTEN, checkpoint="writing")
    record_write_result(state, result)
    save_state(state, workdir=workdir, config=config)
    return state


def mark_completed(
    state: ConceptState,
    workdir: Any = None,
    config: Any = None,
) -> ConceptState:
    """Transicion ``written -> completed`` (idempotente si ya esta completed)."""
    if state.status == ConceptStatus.COMPLETED:
        return state
    state.transition_to(ConceptStatus.COMPLETED, checkpoint="writing")
    save_state(state, workdir=workdir, config=config)
    return state


def mark_writing_failed(
    state: ConceptState,
    error: BaseException,
    workdir: Any = None,
    config: Any = None,
) -> ConceptState:
    """Marca ``failed`` en fase writing (el backup ya fue restaurado por el writer)."""
    msg = f"{type(error).__name__}: {error}"
    if state.status == ConceptStatus.FAILED:
        state.error = msg
        state.checkpoint = "writing"
        save_state(state, workdir=workdir, config=config)
        return state
    try:
        state.transition_to(
            ConceptStatus.FAILED, checkpoint="writing", error=msg, clear_error=False,
        )
    except InvalidTransitionError:
        # Ej. desde needs_review no hay salida directa a failed: no se silencia.
        raise
    save_state(state, workdir=workdir, config=config)
    return state


def writing_phase(
    concept: ConceptMeta,
    synthesis: Synthesis,
    state: ConceptState | None = None,
    config: Any = None,
    workdir: Any = None,
    dry_run: bool = False,
    writer: SafeWriter | None = None,
    run_id: str | None = None,
) -> ConceptState:
    """Fase de escritura: writer + transiciones de estado (written/completed).

    - Si ``dry_run``: genera el diff sin escribir y sin cambiar el estado.
    - Si la escritura OK: ``validated -> written -> completed``, persistiendo
      en cada transicion, con ``phase_data["write_result"]``.
    - Si falla: backup ya restaurado por el writer; estado -> ``failed`` y
      el error se propaga (el orquestador decide el reintento).
    """
    concept_id = concept.id
    if state is None:
        state = (
            load_state(concept_id, workdir=workdir, config=config)
            or ConceptState(concept_id=concept_id)
        )
    # Idempotencia: un concepto completado no se re-escribe (hash del afuera).
    if state.status == ConceptStatus.COMPLETED and not dry_run:
        return state

    if writer is None:
        writer = SafeWriter(config=config, workdir=workdir, run_id=run_id)

    try:
        result = writer.write_concept(concept, synthesis, dry_run=dry_run)
    except Exception as exc:  # noqa: BLE001 - toda falla de la fase -> failed
        if not dry_run:  # en dry-run no se cambia estado
            mark_writing_failed(state, exc, workdir=workdir, config=config)
        raise

    # Dry-run devuelve diff (DiffResult) y no toca el estado.
    if dry_run or isinstance(result, DiffResult):
        return state

    state = mark_written(state, result, workdir=workdir, config=config)
    # Capa I: el paso a completed se decide en el runner tras verificar el DoD.
    # Aqui solo se marca written; mark_completed se invoca condicionalmente.
    return state


__all__ = [
    "WRITER_VERSION",
    "MARKER_START_DEFAULT",
    "MARKER_END_DEFAULT",
    "REQUIRED_HEADINGS",
    "MarkerSpan",
    "DiffResult",
    "SafeWriter",
    "find_markers",
    "count_markers",
    "replace_inside",
    "extract_outside",
    "content_hash_outside",
    "content_hash_inside",
    "sha256",
    "detect_newline",
    "normalize_newlines",
    "parse_frontmatter",
    "extract_frontmatter_block",
    "verify_frontmatter_preserved",
    "verify_headings_preserved",
    "verify_wikilinks_preserved",
    "verify_outside_integrity",
    "render_inside",
    "writing_phase",
    "mark_written",
    "mark_completed",
    "mark_writing_failed",
    "record_write_result",
    "WriterError",
    "VerificationError",
    "MissingMarkersError",
    "DuplicateMarkersError",
    "MarkerOrderError",
    "ConcurrentEditError",
    "OutsideIntegrityError",
    "OutsideByteMismatchError",
    "FrontmatterChangedError",
    "FrontmatterSemanticMismatchError",
    "InsideMismatchError",
    "MarkerCountError",
    "HeadingsChangedError",
    "WikilinksChangedError",
    "WriteFailedError",
]
