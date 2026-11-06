---
title: "Caching"
area: "Backend"
numero: 19
aliases: ["Caching"]
tags: [concepto, it/backend]
---
# Caching

> **Área:** [[03 - Backend/00 - Índice Backend|Índice Backend]] · **Concepto 19 de 25**

## Qué abarca
- Redis
- HTTP cache
- invalidación

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo el caching para reducir la latencia y la carga de los servicios que desarrollo, evitando consultas repetidas a bases de datos o a servicios externos. Resuelvo el problema de tiempos de respuesta lentos y de consumo innecesario de recursos cuando una misma información se solicita con alta frecuencia. En mi día a día como ingeniero backend senior, el caching aparece en la capa de lógica de negocio, en los endpoints de APIs y en los procesos de integración con terceros. Después de entender cómo funciona, puedo diseñar estrategias de expiración, invalidación y colocación de datos que mejoren la escalabilidad del sistema. No necesito preocuparme por caching cuando el dato es altamente volátil, la carga es mínima o la consistencia estricta es obligatoria.

## Esqueleto (el 20% esencial)
1. **Redis como store de caché en memoria** – permite lecturas ultra‑rápidas y operaciones atómicas.  
2. **HTTP cache (ETag, Cache‑Control)** – aprovecha los encabezados para que clientes y proxies reutilicen respuestas.  
3. **Invalidación** – mecanismo para retirar o actualizar entradas obsoletas y mantener la coherencia.  
4. **Política de expiración (TTL)** – define cuánto tiempo vive una entrada antes de ser descartada automáticamente.  
5. **Key design** – convención de nombres que facilita la agrupación y la purga selectiva.

## Como funciona
1. El servicio recibe una solicitud que necesita datos costosos de obtener.  
2. Se genera la clave de caché siguiendo la convención de *key design*.  
3. Se consulta Redis; si la clave existe, se devuelve el valor y se evita la operación original.  
4. Si la clave no existe, se ejecuta la lógica de negocio o la llamada externa.  
5. El resultado se almacena en Redis con un TTL adecuado y, opcionalmente, se envían encabezados HTTP Cache‑Control al cliente.  
6. Cuando el dato cambia, se dispara la *invalidación* (del key o de un conjunto de keys) para que la próxima solicitud recargue la fuente de verdad.

## Detalles
- **Básico**: conectar la aplicación a Redis, usar `GET`/`SET` y definir un TTL.  
- **Intermedio**: aplicar *Cache‑Aside* (leer‑escribir bajo demanda), usar `ETag`/`If‑None‑Match` para validar respuestas en HTTP y diseñar claves jerárquicas (`user:123:profile`).  
- **Avanzado**: implementar *Write‑Through* o *Write‑Behind* para sincronizar escritura en caché y base de datos, usar *Lua scripts* en Redis para operaciones atómicas complejas, y combinar caché de aplicación con CDN para contenido estático.

## Ejemplo minimo
```python
# Python + redis-py
import redis, json, time

r = redis.Redis(host='localhost', port=6379, db=0)

def get_user_profile(user_id):
    key = f"user:{user_id}:profile"
    cached = r.get(key)
    if cached:
        return json.loads(cached)          # 1️⃣ hit
    # 2️⃣ miss → consulta a base de datos simulada
    profile = {"id": user_id, "name": "Ana", "age": 30}
    r.setex(key, 300, json.dumps(profile)) # TTL 5 min
    return profile

print(get_user_profile(123))   # primera llamada, miss
time.sleep(1)
print(get_user_profile(123))   # segunda llamada, hit
```

## Errores comunes
- **TTL demasiado largo** → datos desactualizados; usar expiraciones adecuadas.  
- **Clave poco descriptiva** → colisiones y dificultad de purga; diseñar nombres claros.  
- **Olvidar invalidar** después de una actualización; integrar eventos de cambio con la lógica de caché.  
- **Almacenar objetos muy grandes** → consumo excesivo de memoria; serializar solo lo necesario.  
- **Confiar en caché para datos críticos de consistencia** → aplicar estrategias de escritura segura o fallback a la fuente de verdad.

## Estado actual
- **Fundamentos estables**: Redis sigue siendo la solución de caché en memoria más adoptada; los encabezados HTTP `Cache-Control`, `ETag` y `If-None-Match` son estándar para caché del lado cliente y proxy.  
- **Práctica moderna**: se combina Redis con *distributed caching* en clústeres para alta disponibilidad, se usan *client‑side caching* en GraphQL y se integran políticas de *stale‑while‑revalidate* en CDNs para equilibrar frescura y rendimiento.

## Conexiones
- **Data fetching**: el caching reduce la cantidad de lecturas a bases de datos o APIs externas, acelerando la obtención de datos.  
- **Performance**: al servir respuestas desde memoria, se disminuye la latencia y se aumenta el throughput del servicio.  
- **CDN / Load Balancing**: los encabezados de caché permiten que los CDN y los balanceadores de carga sirvan contenido estático sin tocar el backend, liberando recursos para operaciones dinámicas.

## Ruta de estudio
1. **Prerequisitos**: conocer protocolos HTTP, manejo básico de bases de datos y conceptos de redes.  
2. **Fundamentos**: instalar Redis, practicar comandos `GET/SET/EXPIRE`, y leer la especificación de encabezados HTTP de caché.  
3. **Intermedio**: implementar patrones *Cache‑Aside* y *Write‑Through* en un proyecto real, y diseñar una estrategia de claves.  
4. **Avanzado**: explorar clústeres Redis, scripting con Lua, y combinar caché de aplicación con CDN usando `stale‑while‑revalidate`.  
5. **Especialización**: estudiar casos de uso en microservicios, observabilidad de caché (metrics, tracing) y técnicas de invalidación basada en eventos.

## Preguntas de repaso
1. ¿Qué ventaja principal aporta Redis frente a una consulta directa a la base de datos?  
2. ¿Cómo se utiliza el encabezado `ETag` para validar una respuesta cacheada por el cliente?  
3. ¿Cuál es la diferencia entre *Cache‑Aside* y *Write‑Through*?  
4. ¿Qué riesgos implica un TTL demasiado amplio y cómo se pueden mitigar?  
5. ¿De qué manera un CDN puede complementar el caching implementado en el backend?

<!-- trazabilidad: run_id=run-20261105-164341-f091ab concept=03-backend-19-caching written_at=2026-11-05T19:53:03.136091+00:00 -->
<!-- ai:end -->

## Relacionados
- [[02 - Frontend/18 - Data fetching|Data fetching]] · *Frontend*
- [[02 - Frontend/23 - Performance|Performance]] · *Frontend*
- [[05 - Networking & Internet/25 - CDN - Load Balancing|CDN / Load Balancing]] · *Networking / Internet*

---
← [[03 - Backend/18 - Seguridad|Seguridad]] · [[03 - Backend/00 - Índice Backend|Índice Backend]] · [[03 - Backend/20 - Asincronía & Concurrencia|Asincronía & Concurrencia]] →
