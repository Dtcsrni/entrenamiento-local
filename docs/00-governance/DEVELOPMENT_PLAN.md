# Plan de desarrollo y ciclo de vida

## Modelo

Se adopta un ciclo iterativo basado en cortes verticales. Cada incremento debe producir una capacidad observable de extremo a extremo y evidencia verificable.

## Etapas y gates

### M0 — Definición

**Entregables:** visión, glosario, requisitos P0, casos de uso, riesgos, wireframes y trazabilidad.

**Gate:** todos los requisitos P0 tienen criterio de aceptación y los términos críticos están definidos.

### M1 — Viabilidad técnica

| Spike | Pregunta | Evidencia de salida |
|---|---|---|
| SPIKE-001 | ¿Puede Amazfit Active ejecutar, persistir y reenviar eventos? | Demostración en reloj real |
| SPIKE-002 | ¿Puede el teléfono alcanzar Tezkatli desde el gimnasio de forma privada? | Medición de conexión y reconexión |
| SPIKE-003 | ¿Qué pipeline cabe y rinde en Tezkatli? | VRAM, RAM, latencia y fallos |
| SPIKE-004 | ¿Qué error se obtiene en porciones personales? | Dataset pesado y reporte |
| SPIKE-005 | ¿Room/outbox sobrevive a process death? | Prueba automatizada |
| SPIKE-006 | ¿La detección de gimnasio es útil sin agotar batería? | Falsos positivos y consumo |

**Gate:** cada riesgo técnico queda viable, condicionado, sustituido o descartado.

### M2 — Arquitectura ejecutable

- Android instalable.
- API privada con health check.
- Base de datos y migración inicial.
- Contratos compartidos.
- CI y validación documental.
- Respaldo/restauración mínimo.

### M3 — MVP de entrenamiento

- Rutinas manuales.
- Sesión y fases.
- Registro de series.
- Descanso, corrección y valores previos.
- Historial y métricas básicas.
- Operación totalmente offline.

### M4 — Nutrición y suplementos deterministas

- Catálogo y búsqueda.
- Texto y código de barras.
- OCR de etiqueta.
- Recetas y comidas habituales.
- Suplementos, dosis, horarios e inventario.

### M5 — IA alimentaria

- Trabajos asíncronos.
- Pipeline visual.
- Borradores editables.
- Incertidumbre y procedencia.
- Golden set personal y fallback.

### M6 — Recomendación y analítica

- Inventario verificado del gimnasio.
- Motor de restricciones y puntuación.
- Progresión explicable.
- Peso tendencial y balance energético.

### M7 — Integraciones

- Health Connect.
- Detección contextual del gimnasio.
- Zepp Device App y Side Service si SPIKE-001 es viable.

### M8 — Endurecimiento

- Seguridad, privacidad, rendimiento, batería y recuperación.
- Release candidate reproducible.

### M9 — Operación personal

- Despliegue, monitoreo, respaldos, actualización y mantenimiento.

## Gestión del trabajo

- Backlog por capacidades, no por capas técnicas.
- Ramas breves y `main` siempre construible.
- ADR para decisiones significativas.
- Revisión de riesgos al cerrar cada milestone.
- No asignar fechas hasta medir la velocidad de M0 y M1.

## Definition of Ready

- Necesidad y valor identificados.
- Criterios de aceptación observables.
- Dependencias y riesgos conocidos.
- Tamaño apto para un incremento.
- Incertidumbre técnica resuelta o spike definido.

## Definition of Done

- Implementación y pruebas aplicables aprobadas.
- Manejo de fallos y límites cubierto.
- Documentación y trazabilidad actualizadas.
- Seguridad y privacidad revisadas.
- Validación física cuando depende de hardware.
- Evidencia conservada sin datos personales.
