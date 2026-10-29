"""Tests de Capa 10 (piloto) sin red."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pilot as P
import state
from models import ConceptMeta

WORK = Path(__file__).parent / ".tmp-workdir-pilot"
VAULT = Path(__file__).parent / ".tmp-vault-pilot"

CONCEPTS = [
    ConceptMeta(
        id="frontend-01-internet-web",
        title="Internet & Web",
        area="Frontend",
        note_path=Path("02 - Frontend/01 - Internet & Web.md"),
        key_ideas=["HTTP", "HTTPS", "URLs"],
        connections=["Cliente-Servidor", "HTTP"],
    ),
]


def _reset():
    if WORK.exists():
        shutil.rmtree(WORK)
    if VAULT.exists():
        shutil.rmtree(VAULT)


def _seed_vault():
    note = VAULT / "02 - Frontend" / "01 - Internet & Web.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\ntitle: \"Internet & Web\"\narea: \"Frontend\"\n---\n"
        "# Internet & Web\n\n## Mis notas\n<!-- ai:start -->\n- \n<!-- ai:end -->\n",
        encoding="utf-8",
    )


def _cfg():
    return {"workdir": str(WORK), "vault_path": str(VAULT), "backend": {"provider": "fake"}, "pacing": {"pause_between_concepts_s": 0}}


MOCK_MD = """## Objetivo
Para que sirve HTTP en el desarrollo web moderno.

## Esqueleto (el 20% esencial)
1. Request/response.
2. Metodos y status codes.

## Como funciona
El cliente envia un request al servidor.

## Detalles
HTTP/1.1, HTTP/2, HTTP/3 con QUIC.

## Ejemplo minimo
GET / HTTP/1.1 con headers basicos.

## Errores comunes
Olvidar headers o status codes.

## Estado actual
HTTP/3 vigente y recomendado.

## Conexiones
HTTP complementa HTTPS en seguridad.

## Ruta de estudio
Antes: redes. Despues: APIs REST.

## Preguntas de repaso
1. Que es HTTP?
2. Como funciona?
3. Ejemplo?
"""


def _mock_llm(prompt):
    return MOCK_MD


# ---------------------------------------------------------------------------


def test_pilot_report_persistido():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    report = asyncio.run(runner.run_pilot())
    assert (Path(WORK) / "pilot_report.json").is_file()
    assert report.total == 1


def test_pilot_success_rate():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    report = asyncio.run(runner.run_pilot())
    assert report.completed == 1
    assert report.success_rate == 1.0


def test_pilot_metrics():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    report = asyncio.run(runner.run_pilot())
    assert len(report.metrics) == 1
    m = report.metrics[0]
    assert m.status == "completed"
    assert m.synthesis_chars > 0


def test_pilot_generate_summary():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    report = asyncio.run(runner.run_pilot())
    summary = runner.generate_summary(report)
    assert "Reporte de piloto" in summary
    assert "Tasa de exito" in summary


def test_pilot_to_dict():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    report = asyncio.run(runner.run_pilot())
    d = report.to_dict()
    assert "total" in d
    assert "metrics" in d
    assert "calibration" in d


def test_pilot_calibration():
    _reset()
    _seed_vault()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    report = asyncio.run(runner.run_pilot())
    assert "suggested_pacing_s" in report.calibration
    assert "suggested_timeout_s" in report.calibration


def test_pilot_empty_concepts():
    _reset()
    cfg = _cfg()
    runner = P.PilotRunner(cfg=cfg, llm=_mock_llm, workdir=str(WORK), concepts=[])
    report = asyncio.run(runner.run_pilot())
    assert report.total == 0
    assert report.success_rate == 0.0


def test_run_pilot_funcion():
    _reset()
    _seed_vault()
    cfg = _cfg()
    report = asyncio.run(P.run_pilot(CONCEPTS, cfg=cfg, llm=_mock_llm, workdir=str(WORK)))
    assert report.total == 1
    assert report.completed == 1


def test_pilot_protocolo():
    runner = P.PilotRunner(cfg={"workdir": str(WORK)}, llm=_mock_llm, workdir=str(WORK), concepts=CONCEPTS)
    assert runner is not None
    assert hasattr(runner, "run_pilot")
    assert hasattr(runner, "generate_summary")


if __name__ == "__main__":
    _reset()
    fallos = 0
    for name, fn in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        try:
            fn()
            print(f"OK   {name}")
        except AssertionError as exc:
            fallos += 1
            print(f"FAIL {name}: {exc}")
        except Exception as exc:
            fallos += 1
            print(f"ERR  {name}: {type(exc).__name__}: {exc}")
    _reset()
    print("TODOS OK" if fallos == 0 else f"{fallos} fallos")
    raise SystemExit(1 if fallos else 0)
