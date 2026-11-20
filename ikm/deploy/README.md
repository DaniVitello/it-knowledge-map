---
title: IT Knowledge Map API
emoji: "🐴"
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 8000
pinned: false
---
# IT Knowledge Map — API de chat

Backend FastAPI del chat sobre el release estatico (255 conceptos / 472 relaciones).
LLM: Groq `openai/gpt-oss-120b`. Chat abierto con rate-limit por IP. Google auth OIDC como base.

## Secrets del Space (Settings -> Variables and secrets)
- `GROQ_API_KEYS`: keys de Groq coma-separadas (las de la sintesis).
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`: OAuth de Google (opcional, para login).
- `IKM_SESSION_SECRET`: secreto aleatorio de sesiones.
- `IKM_CORS_ORIGINS`: origenes permitidos, incluir `https://it-knowledge-map-v2.netlify.app`.
- `IKM_FRONTEND_URL`: URL del frontend para el redirect post-login.
- `GOOGLE_REDIRECT_URI`: `https://<space>.hf.space/api/auth/google/callback`.

## Armado y push
`py prepare.py` arma `ikm/` (subset contracts+api) y `release/` desde el proyecto.
Luego subir este directorio a un Space Docker de Hugging Face.
