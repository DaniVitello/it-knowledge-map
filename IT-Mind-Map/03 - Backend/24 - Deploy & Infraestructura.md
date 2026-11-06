---
title: "Deploy & Infraestructura"
area: "Backend"
numero: 24
aliases: ["Deploy & Infraestructura"]
tags: [concepto, it/backend]
---
# Deploy & Infraestructura

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 24 de 25**

## Qué abarca
- Linux
- Docker
- CI/CD
- cloud

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo Deploy & Infraestructura para pasar código escrito en mi máquina local a un entorno donde pueda ser consumido por otras aplicaciones, garantizando que el servicio esté disponible, escalable y seguro. Resuelvo el problema de reproducir exactamente la misma configuración y dependencias en producción, evitando “funciona en mi máquina”. Aparece cada vez que entrego una API o micro‑servicio: preparo la imagen, la envío a la nube y configuro el pipeline que la actualiza automáticamente. Después de entenderlo puedo orquestar despliegues sin interrupciones, aplicar rollback y monitorizar la salud del servicio. No necesito preocuparme cuando el proyecto es un script puntual que nunca será reutilizado ni expuesto a usuarios externos.

## Esqueleto (el 20% esencial)
1. **Linux** – base del entorno de ejecución; todas las imágenes de contenedor se construyen sobre un kernel Linux.  
2. **Docker** – empaqueta la aplicación y sus dependencias en una imagen portable.  
3. **CI/CD** – automatiza la construcción, pruebas y despliegue de la imagen en cada commit.  
4. **Cloud** – provee la infraestructura (VM, Kubernetes, serverless) donde se ejecutan los contenedores.  

## Como funciona
1. Escribo el código y lo guardo en un repositorio Git.  
2. El pipeline de CI (por ejemplo GitHub Actions) detecta el push, ejecuta pruebas y construye una **imagen Docker** usando un `Dockerfile` sobre **Linux**.  
3. La imagen se publica en un registro (Docker Hub, ECR).  
4. El pipeline de CD extrae la imagen y la despliega en la **cloud** mediante un servicio de orquestación (ECS, GKE, etc.).  
5. La infraestructura provisionada mantiene el contenedor en ejecución, aplica escalado y monitoriza su salud.

## Detalles
- **Básico**: crear un `Dockerfile` sencillo, usar `docker build` y `docker run` en una máquina Linux local.  
- **Intermedio**: integrar pruebas unitarias en el pipeline CI, versionar imágenes con tags semánticos y usar variables de entorno para configuración.  
- **Avanzado**: desplegar con Kubernetes, gestionar secretos con herramientas como Vault, aplicar blue‑green o canary deployments y usar infraestructura como código (Terraform) para provisionar la **cloud**.

## Ejemplo minimo
```bash
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["python", "main.py"]
```
```bash
# Construir y ejecutar localmente
docker build -t mi-api:dev .
docker run -p 8000:8000 mi-api:dev
```

## Errores comunes
- **Olvidar .dockerignore** → la imagen incluye archivos innecesarios; evita copiando solo lo necesario.  
- **Hardcodear rutas o credenciales** → rompe en otros entornos; usa variables de entorno o secret managers.  
- **No versionar la imagen** → no se puede reproducir un despliegue anterior; etiqueta con versiones.  

## Estado actual
- **Fundamentos estables**: Linux como SO subyacente, Docker para contenedorización y los principios de CI/CD (build‑test‑deploy).  
- **Práctica moderna**: uso de Kubernetes o servicios serverless en la **cloud**, pipelines declarativos (GitHub Actions, GitLab CI) y gestión de infraestructura con Terraform o Pulumi.  

## Conexiones
- **CI/CD**: el pipeline automatiza la construcción y despliegue de la imagen Docker.  
- **Containers**: Docker es la tecnología que permite empaquetar la aplicación para que la infraestructura la ejecute sin variaciones.  
- **Virtualization & Infrastructure**: la capa de virtualización (VM o Kubernetes) provee los recursos donde los contenedores se ejecutan, conectando la lógica de negocio con la hardware subyacente.  

## Ruta de estudio
1. **Prerequisitos**: línea de comandos Linux, Git y fundamentos de redes.  
2. **Docker**: crear Dockerfiles, usar `docker compose` y publicar en un registro.  
3. **CI/CD**: diseñar pipelines con GitHub Actions o GitLab CI, incluir pruebas automatizadas.  
4. **Cloud**: familiarizarse con al menos un proveedor (AWS, GCP, Azure), lanzar una VM y desplegar contenedores con ECS, GKE o Cloud Run.  
5. **Orquestación**: aprender conceptos de Kubernetes (pods, deployments, services) y patrones de despliegue (blue‑green, canary).  

## Preguntas de repaso
1. ¿Por qué es importante que la imagen Docker se construya sobre una base Linux en entornos de backend?  
2. ¿Qué pasos automatiza un pipeline CI/CD al publicar una API?  
3. ¿Cómo evita el archivo `.dockerignore*` que la imagen sea innecesariamente grande?  
4. ¿Cuál es la diferencia entre desplegar un contenedor en una VM y en un clúster Kubernetes?  
5. ¿Qué estrategia de despliegue usarías para introducir una nueva versión sin interrumpir a los usuarios?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-24-deploy-infraestructura written_at=2026-11-05T19:57:19.658313+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/25 - CI-CD|CI/CD]] · *Software Engineering*
- [[06 - Operating Systems & Linux/24 - Containers|Containers]] · *Operating Systems / Linux*
- [[06 - Operating Systems & Linux/25 - Virtualization & Infrastructure|Virtualization & Infrastructure]] · *Operating Systems / Linux*
- [[07 - AI Engineering/23 - AI Infrastructure|AI Infrastructure]] · *AI Engineering*

---
← [[03 - Backend/23 - Testing Backend|Testing Backend]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/25 - Sistemas distribuidos|Sistemas distribuidos]] →
