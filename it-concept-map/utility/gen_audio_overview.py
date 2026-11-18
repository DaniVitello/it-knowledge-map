r"""Genera audio overview (MP3) de cada explicacion en explicaciones/.

USO: py utility\gen_audio_overview.py [--voice es-ES-AlvaroNeural]
"""
from __future__ import annotations
import argparse, asyncio, re
from pathlib import Path

async def gen(text: str, out: Path, voice: str):
    import edge_tts
    # Limpiar markdown basico para TTS
    t = re.sub(r"```.*?```", "", text, flags=re.S)
    t = re.sub(r"`[^`]*`", "", t)
    t = re.sub(r"#+\s*", "", t)
    t = re.sub(r"\*{1,2}", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", t)
    t = re.sub(r"\n{2,}", ". ", t)
    t = t.strip()
    if not t:
        return
    communicate = edge_tts.Communicate(t, voice)
    await communicate.save(str(out))

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="es-ES-AlvaroNeural")
    ap.add_argument("--src", default=str(Path(__file__).resolve().parents[2] / "docs" / "explicaciones"))
    ap.add_argument("--out", default="C:/Users/DGVit/Proyectos/IT Career/audios")
    args = ap.parse_args()
    src = Path(args.src)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for md in sorted(src.glob("*.md")):
        mp3 = out / (md.stem + ".mp3")
        text = md.read_text(encoding="utf-8")
        print(f"Generating: {mp3.name} ...", flush=True)
        try:
            await gen(text, mp3, args.voice)
            print(f"  -> OK: {mp3}", flush=True)
        except Exception as e:
            print(f"  -> ERROR: {e}", flush=True)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
