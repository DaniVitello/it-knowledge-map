---
title: "Testing Backend"
area: "Backend"
numero: 23
aliases: ["Testing Backend"]
tags: [concepto, it/backend]
---
# Testing Backend

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 23 de 25**

## Qué abarca
- Unit
- integration
- API
- E2E

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el testing backend para validar que la lógica de negocio, las integraciones y los contratos de API de mis servicios funcionan como se espera antes de desplegarlos. Resuelvo errores que de otro modo aparecerían en producción, como cálculos incorrectos, fallos en llamadas a bases de datos o respuestas mal formateadas. Aparece en cada fase del ciclo de vida de un micro‑servicio: al desarrollar nuevas rutas, al refactorizar código existente y al actualizar dependencias. Después de entenderlo puedo automatizar la verificación de cambios, reducir el tiempo de revisión de código y confiar en la estabilidad de los despliegues. No necesito preocuparme cuando el servicio es un script ad‑hoc sin exposición externa ni lógica crítica; allí basta con pruebas manuales rápidas.

## Esqueleto (el 20% esencial)
1. **Unit tests** – verifican funciones o clases aisladas sin dependencias externas.  
2. **Integration tests** – comprueban la interacción entre componentes internos (p. ej. repositorios y servicios).  
3. **API tests** – validan los endpoints HTTP contra los contratos esperados (códigos, payloads).  
4. **End‑to‑End (E2E) tests** – ejercen el flujo completo del sistema, incluyendo bases de datos y colas externas.  

## Como funciona
1. Defino casos de prueba unitarios que inyectan *mocks* o *stubs* para evitar llamadas reales.  
2. Agrupo varios unit tests en suites de integración que arrancan una base de datos en memoria o un contenedor Docker.  
3. Utilizo un cliente HTTP (por ejemplo `requests` o `supertest`) para enviar peticiones a los endpoints y comparar la respuesta con el esquema esperado.  
4. En el pipeline CI, los tests E2E despliegan la aplicación completa en un entorno de staging y ejecutan escenarios de usuario mediante herramientas como Cypress o Playwright.  
5. El proceso se detiene al primer fallo, lo que permite corregir el problema antes de que llegue a producción.

## Detalles
- **Básico:** crear funciones de prueba con `pytest` o `unittest`, usar `assert` para validar resultados simples.  
- **Intermedio:** introducir fixtures que preparen datos de prueba, emplear `factory_boy` para generar entidades y usar bases de datos temporales (`sqlite` en memoria).  
- **Avanzado:** orquestar contenedores con `docker‑compose` para pruebas de integración que involucren Redis, RabbitMQ u otros servicios; aplicar pruebas contractuales con `pact` para asegurar compatibilidad entre micro‑servicios.  
- **E2E:** simular flujos de usuario completo, validar métricas de rendimiento y asegurar que la observabilidad (tracing, logs) se genera correctamente.

## Ejemplo minimo
```python
# test_user_service.py
import pytest
from myapp.services import calculate_discount

def test_calculate_discount():
    # caso unitario: cliente premium recibe 20% de descuento
    assert calculate_discount(price=100, is_premium=True) == 80
```

## Errores comunes
- **Mockar demasiado:** se pierden fallos reales de integración; usar mocks solo donde sea necesario.  
- **No limpiar datos:** los tests dejan datos residuales y contaminan ejecuciones posteriores; emplear fixtures con `teardown`.  
- **Ignorar pruebas de error:** solo validar casos felices; incluir escenarios de excepción y respuestas de error.  
- **Dependencias externas en unit tests:** romper el aislamiento; sustituir con stubs o usar `responses` para HTTP.  

## Estado actual
- **Fundamentos estables:** los tests unitarios e integrados con `pytest` y fixtures son prácticas consolidadas y ampliamente soportadas.  
- **Práctica moderna:** el uso de contenedores para pruebas de integración, pruebas contractuales con `pact` y pipelines CI que ejecutan suites E2E en entornos efímeros son tendencias actuales en equipos de backend senior.

## Conexiones
- **CI/CD:** los tests se ejecutan automáticamente en cada push, impidiendo que código defectuoso llegue a producción.  
- **Observability:** los fallos detectados por tests pueden correlacionarse con métricas y trazas para acelerar la depuración.  
- **Domain‑Driven Design:** los tests unitarios reflejan los *bounded contexts* y garantizan que las invariantes del dominio se mantengan.

## Ruta de estudio
1. **Prerequisitos:** Python (o lenguaje del stack), conceptos de HTTP y bases de datos.  
2. **Fundamentos:** aprender `unittest`/`pytest`, crear fixtures y usar `assert`.  
3. **Integración:** practicar con bases de datos en memoria y Docker Compose para servicios auxiliares.  
4. **API testing:** dominar `requests` o `httpx`, validar esquemas con `jsonschema`.  
5. **E2E y contract testing:** explorar Cypress/Playwright y `pact`.  
6. **Automatización:** integrar todo en pipelines GitHub Actions, GitLab CI o Jenkins.

## Preguntas de repaso
1. ¿Cuál es la diferencia principal entre un unit test y un integration test en un servicio backend?  
2. ¿Cómo ayuda un mock a mantener la velocidad y aislamiento de un unit test?  
3. ¿Qué tipo de prueba validarías para asegurar que un endpoint devuelve un 400 cuando falta un campo obligatorio?  
4. ¿Por qué es importante ejecutar pruebas E2E en un entorno de staging antes del despliegue?  
5. ¿Cómo se relaciona el testing backend con la estrategia de CI/CD de un equipo?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-23-testing-backend written_at=2026-11-05T19:56:42.724157+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/17 - Testing|Testing]] · *Software Engineering*
- [[02 - Frontend/22 - Testing|Testing]] · *Frontend*

---
← [[03 - Backend/22 - Observabilidad|Observabilidad]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/24 - Deploy & Infraestructura|Deploy & Infraestructura]] →
