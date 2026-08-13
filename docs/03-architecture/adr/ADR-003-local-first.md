# ADR-003 — Local-first y Room

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Decisión

Room será la fuente operativa de datos confirmados. La UI observará datos locales y toda operación crítica se confirmará localmente antes de sincronizar.

## Consecuencias

- La aplicación funciona con conectividad inestable.
- Se requieren migraciones, outbox, conflictos y recuperación.
- Tezkatli no puede alterar directamente datos confirmados.
