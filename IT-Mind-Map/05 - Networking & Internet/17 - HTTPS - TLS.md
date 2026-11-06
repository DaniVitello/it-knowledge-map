---
title: "HTTPS / TLS"
area: "Networking / Internet"
numero: 17
aliases: ["HTTPS / TLS"]
tags: [concepto, it/networking-internet]
---
# HTTPS / TLS

> **Área:** [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · **Concepto 17 de 25**

## Qué abarca
- Comunicación HTTP cifrada

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo HTTPS/TLS para proteger la comunicación HTTP entre clientes y servidores, evitando que terceros intercepten o alteren los datos. Resuelvo problemas de confidencialidad e integridad que aparecen cuando se transportan credenciales, datos personales o cualquier información sensible por Internet. En mi día a día como ingeniero de redes senior, lo empleo al validar la cadena de certificados, diagnosticar fallos de handshake y configurar dispositivos perimetrales que inspeccionan tráfico cifrado. Después de comprender cómo funciona el cifrado y la negociación de claves, puedo diseñar políticas de seguridad, depurar errores de conexión TLS y decidir cuándo delegar la terminación TLS a un load balancer o a un WAF. No necesito preocuparme cuando el tráfico es interno y no sale de un entorno controlado o cuando se usan protocolos que no requieren cifrado, como DNS interno sin DNSSEC.

## Esqueleto (el 20% esencial)
1. **Negociación de TLS (handshake)** – establece cifrado y autentica al servidor mediante certificados X.509.  
2. **Cifrado de la carga útil HTTP** – protege encabezados, cookies y cuerpo contra escuchas y manipulaciones.  
3. **Validación de la cadena de confianza** – el cliente verifica que el certificado sea emitido por una CA confiable y no esté revocado.  
4. **Terminación TLS en dispositivos perimetrales** – firewalls o load balancers pueden desencriptar para inspección y volver a cifrar.  

## Como funciona
1. El cliente envía **ClientHello** con versiones TLS soportadas y suites criptográficas.  
2. El servidor responde con **ServerHello**, elige la suite y envía su certificado (y opcionalmente cadena de CA).  
3. El cliente verifica el certificado contra su almacén de confianza; si falla, la conexión se aborta.  
4. Se genera una clave pre‑maestra (RSA, Diffie‑Hellman o ECDHE) y ambos lados derivan claves de sesión.  
5. Con esas claves, se cifran todos los mensajes HTTP posteriores; los encabezados y cookies viajan dentro del túnel TLS.  
6. Si la arquitectura incluye terminación TLS, el dispositivo perimetral realiza los pasos 1‑5 y luego re‑cifra hacia el backend.

## Detalles
- **Básico:** TLS 1.2 y 1.3 son los estándares de facto; la diferencia principal es que TLS 1.3 elimina cifrados obsoletos y reduce la latencia del handshake.  
- **Intermedio:** Configuración de **cipher suites** fuertes (por ejemplo, `TLS_AES_128_GCM_SHA256`) y desactivación de algoritmos débiles como RC4 o 3DES.  
- **Avanzado:** Uso de **OCSP stapling** para validar revocación sin consultas externas, y **TLS session resumption** (tickets o IDs) para acelerar reconexiones.  
- **Operación:** Herramientas como `openssl s_client`, `curl -v https://host` o `wireshark` permiten inspeccionar el handshake y detectar fallos de certificado o incompatibilidades de versiones.

## Ejemplo minimo
```bash
# Verificar handshake y certificado de example.com
openssl s_client -connect example.com:443 -servername example.com </dev/null
```
Salida (resumida):
```
CONNECTED(00000003)
...
Certificate chain
 0 s:/CN=example.com
   i:/C=US/O=Let's Encrypt/CN=R3
...
Verify return code: 0 (ok)
```
El cliente ha establecido TLS, validado la cadena y está listo para enviar HTTP cifrado.

## Errores comunes
- **Usar versiones TLS obsoletas (1.0/1.1).** Evitar configurándolas explícitamente en los servidores.  
- **Olvidar incluir la cadena intermedia de CA.** Corrige añadiendo el bundle de certificados.  
- **No validar revocación (OCSP/CRL).** Habilita OCSP stapling o verifica CRL periódicamente.  
- **Confundir terminación TLS con inspección profunda.** Asegúrate de que el dispositivo perimetral tenga certificados válidos para el backend.

## Estado actual
- **Fundamentos estables:** TLS 1.2 sigue siendo ampliamente soportado; la arquitectura de handshake basada en certificados X.509 es madura.  
- **Práctica moderna:** TLS 1.3 está adoptado por la mayoría de navegadores y servidores; se prefiere por su menor latencia y mayor seguridad. La terminación TLS en load balancers y WAF es una práctica estándar para inspección de tráfico cifrado.

## Conexiones
- **Security Engineering:** HTTPS/TLS es una capa esencial que implementa los principios de confidencialidad e integridad definidos en la ingeniería de seguridad.  
- **Firewalls:** Los firewalls pueden terminar TLS para aplicar políticas de filtrado y detección de amenazas dentro del tráfico cifrado.  
- **WebSockets:** Cuando se usan sobre HTTPS (`wss://`), la conexión hereda la protección TLS, garantizando que los mensajes en tiempo real también estén cifrados.

## Ruta de estudio
1. **Prerequisitos:** TCP/IP, modelo OSI, conceptos de criptografía simétrica y asimétrica, y fundamentos de HTTP/1.1.  
2. **Fundamentos TLS:** Estudiar el RFC 5246 (TLS 1.2) y RFC 8446 (TLS 1.3), enfocándose en el handshake y la derivación de claves.  
3. **Herramientas de diagnóstico:** `openssl`, `curl`, `wireshark` y `ssllabs.com` para pruebas de configuración.  
4. **Configuración segura:** Aprender a seleccionar cipher suites, habilitar OCSP stapling y desactivar versiones antiguas.  
5. **Arquitecturas avanzadas:** Terminación TLS en load balancers, uso de TLS mutuo (client‑cert authentication) y despliegue de certificados automatizados con ACME/Let’s Encrypt.  

## Preguntas de repaso
1. ¿Qué pasos del handshake TLS garantizan la autenticación del servidor?  
2. ¿Cómo afecta la elección de una cipher suite a la seguridad y latencia de la conexión?  
3. ¿Qué ventaja ofrece TLS 1.3 respecto a TLS 1.2 en entornos de alta concurrencia?  
4. ¿Por qué es importante incluir la cadena intermedia de CA en la configuración del servidor?  
5. ¿En qué casos un firewall debería terminar TLS y cuáles son los riesgos si no se gestiona correctamente?

<!-- trazabilidad: run_id=run-20261105-201924-3a3814 concept=05-networking-internet-17-https-tls written_at=2026-11-05T23:29:41.830306+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/24 - Security Engineering|Security Engineering]] · *Software Engineering*
- [[03 - Backend/18 - Seguridad|Seguridad]] · *Backend*
- [[05 - Networking & Internet/16 - HTTP|HTTP]]
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]]
- [[05 - Networking & Internet/22 - WebSockets|WebSockets]]
- [[05 - Networking & Internet/24 - Firewalls|Firewalls]]
- [[07 - AI Engineering/21 - AI Safety & Security|AI Safety & Security]] · *AI Engineering*

---
← [[05 - Networking & Internet/16 - HTTP|HTTP]] · [[05 - Networking & Internet/00 - Índice Networking - Internet|Índice Networking / Internet]] · [[05 - Networking & Internet/18 - Request - Response|Request / Response]] →
