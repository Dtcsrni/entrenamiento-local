# ADR-004 — Outbox transaccional

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Decisión

Guardar cada mutación sincronizable y su evento de salida dentro de la misma transacción local. Los consumidores deben ser idempotentes.

## Consecuencias

- No hay ventana entre guardar y encolar.
- Se requieren IDs estables, ACK, reintentos y limpieza.
- La entrega es al menos una vez, no exactamente una vez.
