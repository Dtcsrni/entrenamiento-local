# ADR-002 — Android nativo

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Decisión

Usar Kotlin, Jetpack Compose, Coroutines/Flow, Room, WorkManager y APIs nativas de Android.

## Justificación

Solo se requiere Android y existen necesidades profundas de cámara, ubicación, process lifecycle, Health Connect, rendimiento y pruebas físicas.

## Consecuencia

No se prioriza portabilidad iOS. Las versiones exactas se fijarán al crear el proyecto y se verificarán contra documentación estable.
