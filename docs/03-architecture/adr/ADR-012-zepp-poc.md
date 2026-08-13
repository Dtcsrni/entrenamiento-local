# ADR-012 — Integración Zepp condicionada por PoC

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Contexto

La documentación pública de Workout Extension enumera dispositivos compatibles y no confirma Amazfit Active.

## Decisión

Diseñar el reloj como adaptador opcional. Validar primero Device App, almacenamiento, mensajería y Side Service en hardware real. No depender de Workout Extension ni BLE no documentado.

## Consecuencias

El MVP de entrenamiento funciona completamente sin reloj.
