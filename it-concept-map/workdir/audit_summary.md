# Auditoría del pipeline IT Career

- Conceptos: 255
- Runs totales (sum de run_id únicos por concepto): 615
- Duración promedio (created→updated): 81179.7s

## Estados
- completed: 255

## Eventos no estándar (errores/reintentos)
- notebook_delete_failed: 206
- phase_failed: 145
- idempotency_hash_mismatch: 118
- notebook_deleted: 61

## Fases completadas (conteo)
- research: 303
- validation: 276
- synthesis: 275
- writing: 267

## Conceptos con reintentos > 0
- Cantidad: 0

## Conceptos con failed_phase
- Cantidad: 80
  - 01-software-engineering-01-programming-fundamentals: phase=synthesizing, reason=error
  - 03-backend-10-arquitectura-de-aplicaciones: phase=synthesizing, reason=error
  - 03-backend-11-bases-de-datos: phase=researching, reason=error
  - 03-backend-12-sql: phase=synthesizing, reason=error
  - 03-backend-13-modelado-de-datos: phase=synthesizing, reason=error
  - 03-backend-14-orm-data-access: phase=synthesizing, reason=error
  - 03-backend-15-transacciones: phase=synthesizing, reason=error
  - 03-backend-16-autenticacion: phase=researching, reason=error
  - 03-backend-17-autorizacion: phase=researching, reason=error
  - 03-backend-18-seguridad: phase=synthesizing, reason=error
  - 03-backend-19-caching: phase=synthesizing, reason=error
  - 03-backend-20-asincronia-concurrencia: phase=synthesizing, reason=error
  - 03-backend-21-mensajeria: phase=synthesizing, reason=error
  - 03-backend-22-observabilidad: phase=synthesizing, reason=error
  - 03-backend-23-testing-backend: phase=synthesizing, reason=error
  - 03-backend-24-deploy-infraestructura: phase=synthesizing, reason=error
  - 03-backend-25-sistemas-distribuidos: phase=synthesizing, reason=error
  - 04-database-data-analytics-02-data-modeling: phase=researching, reason=error
  - 04-database-data-analytics-03-relational-databases: phase=researching, reason=error
  - 04-database-data-analytics-04-sql: phase=researching, reason=error
  - 04-database-data-analytics-05-filtering-aggregation: phase=researching, reason=error
  - 04-database-data-analytics-06-joins: phase=researching, reason=error
  - 04-database-data-analytics-07-keys-constraints: phase=researching, reason=error
  - 04-database-data-analytics-08-normalization: phase=researching, reason=error
  - 04-database-data-analytics-09-indexes: phase=researching, reason=error
  - 04-database-data-analytics-10-transactions: phase=researching, reason=error
  - 04-database-data-analytics-11-acid-isolation: phase=researching, reason=error
  - 05-networking-internet-06-puertos: phase=validating, reason=validation
  - 05-networking-internet-08-dhcp: phase=synthesizing, reason=error
  - 05-networking-internet-23-proxies-reverse-proxies: phase=researching, reason=interrupted
