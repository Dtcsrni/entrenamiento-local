# Registro de riesgos

Escala: probabilidad e impacto de 1 a 5. Exposición = probabilidad × impacto.

| ID | Riesgo | P | I | Exposición | Tratamiento | Evidencia requerida | Estado |
|---|---|---:|---:|---:|---|---|---|
| RISK-001 | Amazfit Active no soporta el flujo requerido | 4 | 5 | 20 | PoC; mantener reloj opcional | Prueba en dispositivo | Abierto |
| RISK-002 | Una foto no permite estimar masa aceptablemente | 5 | 5 | 25 | Peso, multivista, profundidad, rangos y edición | Golden set pesado | Abierto |
| RISK-003 | Tezkatli no está disponible desde el gimnasio | 3 | 5 | 15 | Tailscale, outbox y fallback local | Prueba fuera de LAN | Abierto |
| RISK-004 | Pérdida o duplicación de series | 3 | 5 | 15 | Room transaccional, IDs e idempotencia | Process death/fault injection | Abierto |
| RISK-005 | Saturación de VRAM o RAM | 4 | 4 | 16 | Worker único, límites y selección de modelo | Benchmark reproducible | Abierto |
| RISK-006 | Catálogo nutricional incorrecto | 4 | 4 | 16 | Procedencia, calidad y validación | Casos de catálogo | Abierto |
| RISK-007 | Falsos positivos de llegada al gimnasio | 3 | 3 | 9 | Fusión, histéresis y confirmación | Prueba de campo | Abierto |
| RISK-008 | Consumo excesivo de batería | 3 | 4 | 12 | Trabajo diferido y sensores de baja energía | Perfil de batería | Abierto |
| RISK-009 | IA modifica información confirmada | 2 | 5 | 10 | Contrato de borrador y autorización humana | Pruebas de autorización | Mitigado por diseño |
| RISK-010 | Datos sensibles aparecen en Git o logs | 3 | 5 | 15 | Clasificación, ignore y escaneo | Auditoría de secretos | Abierto |
| RISK-011 | Crecimiento descontrolado del alcance | 4 | 4 | 16 | P0/P1/P2, gates y fuera de alcance | Revisión por milestone | Abierto |
| RISK-012 | Modelo nuevo degrada precisión | 4 | 4 | 16 | Registro, golden set y promoción manual | Comparativa de regresión | Abierto |
| RISK-013 | Duplicación de datos de Health Connect | 3 | 3 | 9 | Conservar origen y política de deduplicación | Prueba multi-origen | Abierto |
| RISK-014 | Respaldo no restaurable | 2 | 5 | 10 | Simulacro periódico | Restauración limpia | Abierto |

## Revisión

Cada riesgo debe revisarse al concluir un spike, milestone o cambio arquitectónico. Un riesgo no se cierra por implementar una mitigación; se cierra cuando existe evidencia suficiente o desaparece la exposición.
