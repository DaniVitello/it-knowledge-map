# HANDOFF — IT Knowledge Map v2

> Prompt para una sesión nueva: "Continuá IT Knowledge Map v2. Leé `ikm/HANDOFF.md` en
> `C:/Users/DGVit/Proyectos/IT Career`. Sitio vivo: https://it-knowledge-map-v2.vercel.app.
> No imprimas claves."

## Qué es
Mapa navegable de 255 conceptos de ingeniería de software. Release `2026-11-19-95e94e92`:
255 conceptos, 472 relaciones, 2295 chunks, 10 áreas. Frontend Vite+React+TS+Tailwind con
grafo 2D (canvas), grafo 3D (Three) y chat con RAG (BM25 sobre el release) + Groq.

## Dónde
- Repo: https://github.com/DaniVitello/it-knowledge-map · rama `v2/L10-frontend`.
- Laptop 1: `C:/Users/DGVit/Proyectos/IT Career` (subdir `ikm/web`). Bash = git-bash.
- Release estático: `ikm/web/public/release` (4.75 MB, 263 archivos), versionado a propósito.

## En vivo
- **Vercel (canal vigente)**: https://it-knowledge-map-v2.vercel.app — front + chat.
  - Proyecto `it-knowledge-map-v2`, id `prj_YyFaWjdhJJaSswyGioPbUuW6gQaa`,
    team `danivitello-gojirafcoms-projects` (`team_sUpemoDQYNGZgg44SWTmx1bX`, plan hobby),
    cuenta `danivitello-1613`.
  - Functions: `ikm/web/api/chat.ts`, `ikm/web/api/health.ts`, `ikm/web/vercel.json`.

## Deploy a Vercel (IMPORTANTE)
El autor del commit git (`danielgvitello@gmail.com`) NO es miembro del team hobby y el
plan Hobby no permite invitar members → Vercel bloquea con `TEAM_ACCESS_REQUIRED`.
Workaround que funciona: desplegar desde un directorio FUERA del repo git (sin `.git`):
copiar `ikm/web` a un temp (excluir `node_modules`, `dist`, `.vercel`, `.git`), crear una
junction de `node_modules`, `vercel link --project it-knowledge-map-v2 --yes` y
`vercel --prod --yes`. Requiere Vercel CLI >= 47.2.2 (instalado 66.6.0).
Si el deploy se bloquea, no reintentar en loop: avisar al usuario.

## Comandos
- Build / tests: `cd ikm/web; npm run build` · `npm test` (64 tests).
- Python: `.venv/Scripts/python.exe -m pytest ikm/tests -q`.

## Secretos
- Groq: `GROQ_API_KEYS` (4 keys) en Vercel (Production) y en Netlify. En laptop 1 también en
  el User env de Windows (`GROQ_API_KEY`, `GROQ_API_KEY_2`).
- **No imprimir claves. No commitear secretos.**

## Pendiente
1. Opcional: alinear el email del git con la cuenta Vercel para poder deployar directo.
3. UI/UX: el lote de correcciones está aplicado (commits `8e3fabf`..`0c4a204`). Queda medir
   el 3D en una PC real, pulir la sensación "entry level" y lo que Dan siga encontrando.
4. Chat: a veces responde `general`; se puede afinar el prompt P1 para más citas `documented`.

## Gotchas
- Windows: el shell es bash (git-bash); a herramientas nativas pasar rutas `C:/...`.
- Archivos del repo con CRLF.
- El harness de browser renderiza por software → el FPS del 3D no es representativo; usar
  `Page.bringToFront` antes de medir.
- La Function del chat lee `/release/chunks.json` del `host` del request (el alias de Vercel
  sirve los estáticos; la URL única del deploy cae en el SPA).
- El `.gitignore` de `ikm/web` ya ignora `.vercel/`.
