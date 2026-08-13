# ADR-006 — La IA produce borradores

- **Estado:** Accepted
- **Fecha:** 2026-08-12

## Decisión

Toda salida de IA será una propuesta estructurada y editable. Solo una acción explícita del usuario crea o modifica un registro confirmado.

## Consecuencias

- Se reduce el riesgo de errores silenciosos.
- Deben coexistir estados draft/confirmed y conservarse procedencia.
- La interfaz de revisión es una función central, no un fallback secundario.
