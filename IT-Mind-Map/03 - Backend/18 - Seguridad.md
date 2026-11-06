---
title: "Seguridad"
area: "Backend"
numero: 18
aliases: ["Seguridad"]
tags: [concepto, it/backend]
---
# Seguridad

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 18 de 25**

## Qué abarca
- CORS
- CSRF
- XSS
- injection
- secrets

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo la seguridad para proteger los servicios y APIs que desarrollo contra accesos no autorizados, manipulación de datos y ataques que comprometan la disponibilidad o confidencialidad. Resuelvo problemas como peticiones maliciosas desde navegadores, inyección de código en bases de datos o exposición accidental de credenciales. Aparece en cada endpoint que expongo, en la configuración del servidor y en el manejo de secretos. Después de entender estos mecanismos puedo diseñar defensas por capas, auditar vulnerabilidades y aplicar buenas prácticas sin que el código se vuelva un punto débil. No necesito preocuparme cuando el servicio está aislado detrás de un firewall interno y no expone datos sensibles a usuarios externos.

## Esqueleto (el 20% esencial)
1. **CORS** – controla qué orígenes pueden consumir la API desde el navegador.  
2. **CSRF** – previene que un sitio externo envíe peticiones autenticadas en nombre del usuario.  
3. **XSS & Inyección** – evitan que datos enviados por el cliente se ejecuten como código o alteren consultas.  
4. **Gestión de secrets** – protege claves, tokens y contraseñas dentro del entorno de ejecución.  

## Como funciona
1. Al iniciar la aplicación, configuro middleware que añade encabezados `Access‑Control‑Allow‑Origin` según la política CORS.  
2. Para cada petición con sesión activa, verifico un token anti‑CSRF (por ejemplo, un header `X‑CSRF‑Token`) que el cliente debe enviar.  
3. Los datos de entrada se sanitizan o parametrizan antes de usarlos en plantillas HTML o consultas SQL, bloqueando XSS e inyección.  
4. Los secrets se cargan desde un vault o variables de entorno y nunca se codifican en el código fuente; el runtime los inyecta de forma segura.  

## Detalles
- **Básico**: habilitar CORS con una lista blanca de dominios; usar encabezados `SameSite` en cookies; almacenar passwords con hash bcrypt.  
- **Intermedio**: implementar tokens CSRF rotativos; usar ORM o consultas preparadas para evitar inyección; rotar secrets periódicamente.  
- **Avanzado**: aplicar políticas de Content Security Policy (CSP) contra XSS persistente; usar secret management tools (HashiCorp Vault, AWS Secrets Manager); integrar pruebas de seguridad automatizadas (SAST, DAST) en CI/CD.  

## Ejemplo minimo
```js
// Node.js + Express
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config(); // carga secrets desde .env

const app = express();

app.use(cors({ origin: ['https://mi-frontend.com'] })); // CORS
app.use(helmet()); // protege contra XSS, clickjacking, etc.
app.use(express.json());

// Middleware CSRF simple (token en header)
app.use((req, res, next) => {
  const token = req.headers['x-csrf-token'];
  if (req.method !== 'GET' && token !== process.env.CSRF_TOKEN) {
    return res.status(403).send('CSRF token inválido');
  }
  next();
});

app.get('/secret', (req, res) => {
  // secret nunca está hardcodeado
  res.send({ apiKey: process.env.API_KEY });
});

app.listen(3000);
```

## Errores comunes
- **Permitir cualquier origen en CORS** → expone la API a scripts maliciosos; usar lista blanca.  
- **Almacenar secrets en el repositorio** → fuga de credenciales; usar vault o variables de entorno.  
- **Confiar en la sanitización manual** → omisiones comunes; preferir consultas parametrizadas y librerías de escape.  
- **Olvidar validar el token CSRF en métodos no GET** → vulnerabilidad de sesión; aplicar middleware global.  

## Estado actual
- **Fundamentos estables**: CORS, encabezados de seguridad (`X‑Content‑Type‑Options`, `X‑Frame‑Options`), hashing de contraseñas, uso de variables de entorno para secrets.  
- **Práctica moderna**: políticas CSP dinámicas, gestión de secrets con herramientas de vault, rotación automática de tokens CSRF, integración de pruebas de seguridad en pipelines CI/CD, adopción de Zero‑Trust networking en microservicios.  

## Conexiones
- **Autenticación**: la seguridad de la API depende de que los mecanismos de autenticación (JWT, OAuth) entreguen identidades verificables antes de aplicar CORS y CSRF.  
- **HTTPS / TLS**: cifra el tráfico entre cliente y servidor, garantizando que los tokens CSRF y los secrets no sean interceptados.  
- **Security Engineering**: provee el marco metodológico para diseñar, evaluar y mejorar las defensas descritas (defensa en profundidad, threat modeling).  

## Ruta de estudio
1. **Prerequisitos**: HTTP, conceptos de API REST, manejo de entornos en Node/Java/Python.  
2. **Fundamentos**: leer la especificación CORS, entender SameSite cookies, practicar hashing con bcrypt.  
3. **Intermedio**: implementar CSRF con tokens sincronizados, usar ORM con consultas preparadas, configurar Helmet o middleware equivalente.  
4. **Avanzado**: estudiar CSP, integrar un secret manager (Vault, AWS Secrets Manager), automatizar escaneos SAST/DAST en CI.  
5. **Especialización**: profundizar en Zero‑Trust, micro‑segmentación de red y auditorías de cumplimiento (PCI‑DSS, GDPR).  

## Preguntas de repaso
1. ¿Cómo limita CORS los orígenes que pueden consumir una API y por qué es importante en backend?  
2. ¿Qué diferencia hay entre un ataque XSS y una inyección SQL, y cómo se mitigan en el código?  
3. ¿Cuál es el propósito de un token CSRF y en qué momento debe validarse?  
4. ¿Por qué los secrets nunca deben estar hardcodeados y cuál es una práctica segura para gestionarlos?  
5. ¿Qué ventajas aporta la integración de pruebas de seguridad automatizadas en el pipeline CI/CD?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-18-seguridad written_at=2026-11-05T19:51:57.334508+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/24 - Security Engineering|Security Engineering]] · *Software Engineering*
- [[03 - Backend/16 - Autenticación|Autenticación]]
- [[03 - Backend/17 - Autorización|Autorización]]
- [[05 - Networking & Internet/17 - HTTPS - TLS|HTTPS / TLS]] · *Networking / Internet*
- [[05 - Networking & Internet/24 - Firewalls|Firewalls]] · *Networking / Internet*
- [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]] · *AI Engineering*

---
← [[03 - Backend/17 - Autorización|Autorización]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/19 - Caching|Caching]] →
