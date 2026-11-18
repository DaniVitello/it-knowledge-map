"""Recovery: restaurar .md del vault desde backups (tras migracion fallida).

USO: py utility\recover_from_backup.py --vault "IT-Mind-Map" --workdir "it-concept-map/workdir" [--dry-run|--apply]
"""
from __future__ import annotations
import argparse, os, glob
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--workdir", default="workdir")
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    vault = Path(args.vault)
    workdir = Path(args.workdir)
    backup_root = workdir / "backups"
    restored = 0
    for backup_dir in sorted(backup_root.iterdir()):
        if not backup_dir.is_dir():
            continue
        baks = sorted(backup_dir.glob("*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not baks:
            continue
        bak = baks[0]
        # bak name: "25 - Arquitectura Frontend.md.20261112T...bak"
        # strip the timestamp suffix to get original filename
        name = bak.name
        # remove everything after the last ".md"
        idx = name.find(".md")
        if idx == -1:
            continue
        orig_name = name[:idx+3]
        # find the .md in vault
        matches = list(vault.rglob(orig_name))
        if not matches:
            print(f"NOT FOUND: {orig_name}")
            continue
        target = matches[0]
        restored += 1
        if args.apply:
            import shutil
            shutil.copy2(bak, target)
            print(f"RESTORED: {target}")
        else:
            print(f"WOULD RESTORE: {target} <- {bak.name}")
    print(f"\nTotal: {restored} archivos")

if __name__ == "__main__":
    main()
