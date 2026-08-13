# ADR-001 — Monorepo

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Contexto

Android, contratos, backend, Zepp y evaluación de IA evolucionarán conjuntamente y pertenecen a un único producto personal.

## Decisión

Mantener todos los componentes y documentación en un monorepo, excluyendo datos personales y artefactos pesados.

## Consecuencias

- Cambios de contrato pueden ser atómicos.
- CI y trazabilidad se centralizan.
- Será necesario evitar acoplamiento accidental entre runtimes.
