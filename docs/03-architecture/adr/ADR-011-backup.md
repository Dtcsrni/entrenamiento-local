# ADR-011 — Respaldo verificable

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Decisión

Diseñar exportación versionada y cifrada, con checksum y restauración a ubicación temporal antes de sustitución atómica.

## Consecuencias

Una copia no se declara respaldo válido hasta completar una restauración de prueba.
