---
title: "Autenticación"
area: "Backend"
numero: 16
aliases: ["Autenticación"]
tags: [concepto, it/backend]
---
# Autenticación

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 16 de 25**

## Qué abarca
- Sessions
- cookies
- JWT
- OAuth

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la autenticación para verificar que quien llama a un endpoint es quien dice ser, evitando que usuarios no autorizados accedan a recursos sensibles. Resuelvo el problema de identificar de forma confiable a clientes y servicios en un entorno distribuido, lo que es esencial al diseñar APIs REST, micro‑servicios o websockets. Aparece en cada punto de entrada del backend: login, middleware de protección y llamadas entre servicios. Después de entenderla puedo elegir el mecanismo (session, cookie, JWT, OAuth) que mejor se adapte a los requisitos de seguridad y escalabilidad de mi proyecto. No necesito preocuparme cuando el servicio es interno y confío en la red de la infraestructura, o cuando delego la autenticación completa a un gateway externo.

## Esqueleto (el 20% esencial)
1. **Session + Cookie** – El servidor crea una sesión y envía su identificador en una cookie; el cliente la devuelve en cada petición.  
2. **JWT (JSON Web Token)** – Token autocontenido firmado que el cliente incluye en el encabezado `Authorization`.  
3. **OAuth 2.0** – Protocolo de delegación que permite a terceros obtener tokens de acceso en nombre del usuario.  
4. **Almacenamiento de credenciales** – Bases de datos o directorios (ej. LDAP) donde se verifica la identidad del usuario.  
5. **Middleware de verificación** – Código que intercepta la petición, extrae el dato de autenticación y lo valida antes de ejecutar la lógica de negocio.

## Como funciona
1. El cliente envía sus credenciales (usuario/clave, código de autorización o token).  
2. El backend valida esas credenciales contra el **almacenamiento de credenciales**.  
3. Si la validación es exitosa, el servidor genera un **session ID** (para cookies) o un **JWT** firmado, o redirige al cliente a un **provider OAuth**.  
4. El dato de autenticación se devuelve al cliente: cookie `Set-Cookie`, token en el cuerpo o redirección con código.  
5. En cada petición posterior, el **middleware de verificación** extrae la cookie, el JWT o el token OAuth del encabezado `Authorization`.  
6. El middleware verifica la firma (JWT) o consulta el store de sesiones; si es válido, asocia la petición a un usuario y permite que la lógica de negocio continúe.

## Detalles
- **Básico**: Session + Cookie. Ideal para aplicaciones monolíticas donde el backend mantiene estado.  
- **Intermedio**: JWT. Permite stateless scaling; el token lleva claims (roles, expiración) y se verifica sin acceso a base de datos.  
- **Avanzado**: OAuth 2.0 + OpenID Connect. Usa *authorization code flow* para delegar la autenticación a un IdP (Identity Provider) y obtener tokens de acceso y refresh.  
- **Refresh Tokens**: En flujos OAuth, el refresh token permite renovar el JWT sin volver a pedir credenciales al usuario.  
- **Rotación de claves**: Para JWT, se recomienda rotar la clave de firma y mantener un *key set* para validar tokens antiguos.  
- **Seguridad de cookies**: `HttpOnly`, `Secure` y `SameSite=Strict` reducen ataques de XSS y CSRF.

## Ejemplo minimo
```python
# FastAPI + JWT (minimal)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt, datetime

app = FastAPI()
SECRET = "supersecretkey"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def crear_token(usuario: str):
    payload = {
        "sub": usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido")

@app.post("/login")
def login(username: str, password: str):
    # aquí iría la verificación contra DB
    if username == "admin" and password == "admin":
        return {"access_token": crear_token(username), "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Credenciales incorrectas")

@app.get("/protected")
def protegido(usuario: str = Depends(validar_token)):
    return {"msg": f"Hola {usuario}, acceso concedido"}
```

## Errores comunes
- **Almacenar contraseñas en texto plano** – Usa hashing con bcrypt o Argon2.  
- **No establecer `HttpOnly` y `Secure` en cookies** – Los navegadores pueden exponerlas a scripts maliciosos.  
- **Ignorar la expiración del JWT** – Verifica siempre el claim `exp`.  
- **Usar el mismo secreto para firma y cifrado** – Mantén claves separadas y rotálas periódicamente.  
- **Confiar en el cliente para validar roles** – La autorización siempre se verifica en el backend.

## Estado actual
**Fundamentos estables**:  
- Session + Cookie sigue siendo la forma más simple y probada para autenticación en aplicaciones con estado.  
- JWT es ampliamente adoptado para arquitecturas sin estado y micro‑servicios.  

**Práctica moderna**:  
- OAuth 2.0 con OpenID Connect es el estándar de facto para delegar autenticación a IdPs externos (Google, Auth0, Keycloak).  
- Uso de *refresh tokens* rotativos y *token binding* para mitigar robo de tokens.  
- Implementaciones de *Zero Trust* que combinan autenticación fuerte (MFA) con autorización basada en atributos.

## Conexiones
- **Security Engineering**: La autenticación es una capa fundamental dentro del diseño de sistemas seguros, influenciando la arquitectura de defensa en profundidad.  
- **Autorización**: Después de identificar al usuario, la autorización decide qué recursos puede acceder; ambas deben estar alineadas.  
- **Seguridad en Frontend**: El frontend debe manejar correctamente los tokens (almacenamiento, envío en encabezados) para no comprometer la autenticación establecida por el backend.

## Ruta de estudio
1. **Prerequisitos**: HTTP, conceptos de estado vs stateless, criptografía básica (hash, firma).  
2. **Fundamentos**: Implementar sesiones con cookies en Express o Django; comprender el flujo de login tradicional.  
3. **JWT**: Estudiar la estructura (header, payload, signature), algoritmos HS256/RS256, y practicar generación/validación en al menos dos lenguajes.  
4. **OAuth 2.0**: Aprender los cuatro grant types (authorization code, client credentials, password, refresh token) y probar con un IdP como Keycloak.  
5. **Avanzado**: Rotación de claves, token binding, integración de MFA, y patrones de Zero Trust.  
6. **Práctica**: Construir una API protegida con FastAPI (JWT) y un gateway que use OAuth 2.0; medir rendimiento y seguridad con pruebas de penetración.

## Preguntas de repaso
1. ¿Qué información lleva un JWT y por qué es importante validar su firma y expiración?  
2. ¿En qué casos preferirías una sesión basada en cookie frente a un JWT?  
3. Describe el flujo básico de autorización en OAuth 2.0 con el *authorization code grant*.  
4. ¿Cómo protege la bandera `HttpOnly` a una cookie de sesión?  
5. ¿Cuál es la diferencia entre autenticación y autorización y cómo se relacionan en un backend de micro‑servicios?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-16-autenticacion written_at=2026-11-05T19:49:59.675697+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/24 - Security Engineering|Security Engineering]] · *Software Engineering*
- [[02 - Frontend/19 - Autenticación en Frontend|Autenticación en Frontend]] · *Frontend*
- [[03 - Backend/17 - Autorización|Autorización]]
- [[03 - Backend/18 - Seguridad|Seguridad]]

---
← [[03 - Backend/15 - Transacciones|Transacciones]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/17 - Autorización|Autorización]] →
