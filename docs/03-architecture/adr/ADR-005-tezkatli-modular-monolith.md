# ADR-005 — Monolito modular en Tezkatli

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Decisión

Implementar una API y workers como monolito modular con puertos/adaptadores y cola SQLite durable inicialmente.

## Consecuencias

- Menor operación que microservicios/Redis/Celery.
- Las fronteras de dominio siguen explícitas.
- Un futuro cuello de botella comprobado puede extraerse sin diseñarlo anticipadamente.
