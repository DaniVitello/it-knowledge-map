---
title: "Logs & System Monitoring"
area: "Operating Systems / Linux"
numero: 23
aliases: ["Logs & System Monitoring"]
tags: [concepto, it/operating-systems-linux]
---
# Logs & System Monitoring

> **Área:** [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · **Concepto 23 de 25**

## Qué abarca
- Procesos
- CPU
- RAM
- disco
- logs

## Mis notas
<!-- ai:start -->
## Objetivo
Utilizo los logs y el monitoreo del sistema para obtener una visión en tiempo real del comportamiento de procesos, CPU, RAM y discos en los servidores Linux que administro. Con esta información detecto cuellos de botella, fallos de servicios y eventos de seguridad antes de que impacten a los usuarios. Cuando entiendo cómo se generan, almacenan y consultan los logs, y cómo se configuran métricas de monitoreo, puedo diagnosticar problemas de rendimiento, planificar capacidad y automatizar alertas. No necesito preocuparme por logs y monitoreo cuando el sistema está en modo de desarrollo aislado y no hay requisitos de disponibilidad ni de auditoría.

## Esqueleto (el 20% esencial)
1. **Recolección de logs** – los componentes del kernel y los daemons escriben eventos en archivos bajo `/var/log` o en el journal de `systemd`.  
2. **Métricas de recursos** – el kernel expone contadores de CPU, memoria y I/O que herramientas como `top`, `vmstat` o `collectd` convierten en métricas.  
3. **Visualización y alerta** – sistemas como `Grafana` o `Nagios` consumen esas métricas y logs para generar dashboards y disparar notificaciones.  
4. **Retención y rotación** – `logrotate` y la configuración del journal controlan cuánto tiempo se conserva la información.  

## Como funciona
1. Cada proceso escribe mensajes de estado en su descriptor de salida o mediante `syslog`.  
2. `systemd-journald` o `rsyslog` capturan esos mensajes y los almacenan en un archivo binario o texto.  
3. Los contadores del kernel (expuestos en `/proc` y `/sys`) son leídos periódicamente por un agente de monitoreo.  
4. El agente envía los datos a un backend (por ejemplo, InfluxDB).  
5. Un visualizador consulta el backend y muestra gráficos; si una métrica supera un umbral, se genera una alerta por correo o webhook.  

## Detalles
- **Básico**: leer logs con `journalctl -u nginx` o `tail -f /var/log/auth.log`; observar uso de CPU con `top`.  
- **Intermedio**: configurar `logrotate` para dividir archivos por tamaño y fecha; instalar `collectd` y definir plugins para CPU, RAM y disco.  
- **Avanzado**: habilitar el modo persistente del journal (`Storage=persistent`), crear reglas de filtrado en `systemd-journald`, integrar agentes como `Telegraf` con etiquetas personalizadas y definir alertas complejas en `Prometheus Alertmanager`.  

## Ejemplo minimo
```bash
# Ver los últimos 10 eventos del kernel relacionados con el disco
journalctl -k -n 10

# Monitorear uso de CPU cada 2 segundos y detener después de 5 lecturas
mpstat 2 5
```
La salida de `journalctl` muestra timestamps, nivel de severidad y mensaje del kernel; `mpstat` muestra %usr, %sys, %idle, etc., permitiendo detectar picos de carga.

## Errores comunes
- **Ignorar la rotación**: los archivos crecen sin límite y agotan disco; configure `logrotate` o limite el tamaño del journal.  
- **Monitorear solo CPU**: omitir RAM e I/O lleva a diagnósticos incompletos; incluya métricas de disco y memoria.  
- **Alertas demasiado sensibles**: generar notificaciones por cada pequeño pico produce ruido; ajuste umbrales y períodos de evaluación.  

## Estado actual
- **Fundamentos estables**: `systemd-journald`, `rsyslog`, `logrotate`, y los contadores expuestos en `/proc` son componentes maduros y ampliamente usados.  
- **Práctica moderna**: la tendencia es centralizar logs en soluciones como ELK (Elasticsearch‑Logstash‑Kibana) o Loki, y combinar métricas con Prometheus + Grafana para observabilidad completa.  

## Conexiones
- **Observability**: logs y métricas son los pilares que permiten observar el estado interno del sistema sin intervención directa.  
- **Alerting**: las métricas recolectadas alimentan reglas de alerta que notifican incidentes en tiempo real.  
- **Performance tuning**: los datos de monitoreo guían la afinación de parámetros del kernel y de los servicios para mejorar el rendimiento.  

## Ruta de estudio
1. **Prerequisitos**: manejo de la línea de comandos, conceptos de procesos y permisos en Linux.  
2. **Fundamentos**: estudiar `systemd-journald`, `rsyslog` y `logrotate`; practicar con `journalctl` y `tail`.  
3. **Métricas**: aprender a usar `top`, `htop`, `vmstat`, `iostat` y a leer `/proc/*`.  
4. **Agentes**: instalar y configurar `collectd` o `Telegraf`; enviar datos a InfluxDB o Prometheus.  
5. **Visualización**: crear dashboards simples en Grafana; definir alertas en Alertmanager.  
6. **Avanzado**: implementar un stack ELK o Loki, usar filtros avanzados en el journal y automatizar respuestas con scripts.  

## Preguntas de repaso
1. ¿Qué ventaja tiene usar `systemd-journald` frente a archivos de texto tradicionales?  
2. ¿Cómo se configura la rotación automática de logs para evitar que el disco se llene?  
3. ¿Qué métricas del kernel son críticas para detectar un problema de I/O en disco?  
4. ¿Cuál es el flujo típico desde la generación de un log hasta la emisión de una alerta?  
5. ¿Por qué es importante combinar logs y métricas en una estrategia de observabilidad?

<!-- trazabilidad: run_id=run-20261106-225649-4f677c concept=06-operating-systems-linux-23-logs-system-monitoring written_at=2026-11-07T01:58:01.063076+00:00 -->
<!-- ai:end -->

## Relacionados
- [[01 - Software Engineering/26 - Observability|Observability]] · *Software Engineering*
- [[03 - Backend/22 - Observabilidad|Observabilidad]] · *Backend*
- [[07 - AI Engineering/22 - Observability|Observability]] · *AI Engineering*

---
← [[06 - Operating Systems & Linux/22 - Networking en Linux|Networking en Linux]] · [[06 - Operating Systems & Linux/00 - Índice Operating Systems - Linux|Índice Operating Systems / Linux]] · [[06 - Operating Systems & Linux/24 - Containers|Containers]] →
