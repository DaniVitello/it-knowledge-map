# Aprendizajes e ideas de mejora

## 2026-10-22 — Automatización de conceptos Frontend con NotebookLM

### Error: UnicodeDecodeError en subprocess (Windows)

**Síntoma:** al automatizar la creación de notebooks y research con
`notebooklm-py`, el script lanzó `UnicodeDecodeError: 'charmap' codec can't
decode byte 0x90` dentro de `_readerthread` de `subprocess`.

**Causa:** `subprocess.run(..., text=True)` usa el encoding por defecto del
sistema. En Windows ese default es `cp1252`, pero la CLI de NotebookLM
imprime UTF-8 (tildes, "árbol", emojis, etc.). cp1252 no puede decodificar
esos bytes.

**Responsabilidad:** nuestra (el wrapper), no del servicio ni del response.

**Fix:** pasar explícitamente el encoding al subprocess:

```python
subprocess.run(
    CLI + args,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",   # o "backslashreplace" para depurar
    timeout=timeout,
)
```

**Idea de mejora:** centralizar la invocación del CLI en una única función
helper con estos parámetros, para no repetir el bug en otros scripts. También
considerar usar la API Python de `notebooklm` directamente (en vez de la CLI)
para evitar parsing de stdout y problemas de encoding.

### Contexto
- Script: `automate_frontend_concepts.py`
- CLI invocada: `py -m notebooklm` (notebooklm-py v0.8.4)
- Conceptos procesados: Frontend 02–06 (HTML, CSS, Layout, DOM, JavaScript)
