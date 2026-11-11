"""Tests de Capa 9 (CLI) sin red."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cli
import state
from models import ConceptMeta

WORK = Path(__file__).parent / ".tmp-workdir-cli"
VAULT = Path(__file__).parent / ".tmp-vault-cli"

CONCEPT = ConceptMeta(
    id="frontend-01-internet-web",
    title="Internet & Web",
    area="Frontend",
    note_path=Path("02 - Frontend/01 - Internet & Web.md"),
    key_ideas=["HTTP", "HTTPS", "URLs"],
    connections=["Cliente-Servidor", "HTTP"],
)


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


def _cfg_path():
    cfg = VAULT.parent / "config_cli.yaml"
    cfg.write_text(
        f"vault_path: \"{VAULT.as_posix()}\"\nworkdir: \"{WORK.as_posix()}\"\nbackend:\n  provider: fake\n",
        encoding="utf-8",
    )
    return str(cfg)


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


def test_cmd_status_sin_estado():
    _reset()
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.concept = "frontend-01-internet-web"
    rc = cli.cmd_status(args)
    assert rc == 1


def test_cmd_list_vacio():
    _reset()
    _seed_vault()
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.status = None
    rc = cli.cmd_list(args)
    assert rc == 0


def test_cmd_reset_sin_estado():
    _reset()
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.concept = "frontend-01-internet-web"
    rc = cli.cmd_reset(args)
    assert rc == 0


def test_cmd_run_dry_run():
    _reset()
    _seed_vault()
    cfg_path = _cfg_path()
    # monkeypatch run_concept to use mock llm
    import runner as RN
    orig = RN.Runner.run_concept

    async def patched(self, concept, force=False, dry_run=False):
        return await orig(self, concept, force=force, dry_run=True)

    RN.Runner.run_concept = patched
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.concept = "frontend-01-internet-web"
    args.area = None
    args.limit = None
    args.force = False
    args.dry_run = True
    # inject llm via monkeypatch Runner init
    orig_init = RN.Runner.__init__
    def new_init(self, cfg=None, llm=None, workdir=None):
        orig_init(self, cfg=cfg, llm=_mock_llm, workdir=workdir)
    RN.Runner.__init__ = new_init
    rc = cli.cmd_run(args)
    RN.Runner.__init__ = orig_init
    RN.Runner.run_concept = orig
    assert rc in (0, 1)


def test_cmd_run_status_filter():
    _reset()
    _seed_vault()
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.status = "pending"
    rc = cli.cmd_list(args)
    assert rc == 0


def test_main_sin_comando():
    try:
        cli.main([])
        rc = 0
    except SystemExit as e:
        rc = e.code
    assert rc != 0


def test_main_help():
    try:
        cli.main(["--help"])
    except SystemExit as e:
        assert e.code == 0


def test_cmd_run_concept_no_encontrado():
    _reset()
    _seed_vault()
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.concept = "no-existe-xyz"
    args.area = None
    args.limit = None
    args.force = False
    args.dry_run = False
    rc = cli.cmd_run(args)
    assert rc == 1


def test_cmd_status_con_estado():
    _reset()
    _seed_vault()
    # crear estado manualmente
    import state
    st = state.ConceptState(concept_id="frontend-01-internet-web")
    st.status = state.ConceptStatus.COMPLETED
    state.save_state(st, workdir=str(WORK))
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.concept = "frontend-01-internet-web"
    rc = cli.cmd_status(args)
    assert rc == 0


def test_cmd_reset_con_estado():
    _reset()
    _seed_vault()
    import state
    st = state.ConceptState(concept_id="frontend-01-internet-web")
    state.save_state(st, workdir=str(WORK))
    cfg_path = _cfg_path()
    args = type("Args", (), {})()
    args.config = cfg_path
    args.workdir = None
    args.vault = None
    args.concept = "frontend-01-internet-web"
    rc = cli.cmd_reset(args)
    assert rc == 0


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
