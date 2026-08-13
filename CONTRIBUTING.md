# Contribución

Aunque el proyecto sea personal, todo cambio debe ser revisable.

## Flujo

1. Vincular el cambio con un requisito, riesgo, defecto o spike.
2. Trabajar en una rama breve `feature/*`, `fix/*`, `docs/*` o `spike/*`.
3. Hacer el cambio mínimo y actualizar pruebas/documentación.
4. Ejecutar `python scripts/validate_repository.py`.
5. Adjuntar evidencia real; no afirmar pruebas no ejecutadas.

## Definition of Done

- Criterios de aceptación satisfechos.
- Compilación, lint y pruebas aplicables aprobados.
- Errores y casos frontera cubiertos.
- Seguridad y privacidad revisadas.
- Migraciones y contratos actualizados cuando corresponda.
- Trazabilidad y ADR actualizados.
- Validación en dispositivo físico cuando dependa de cámara, batería, ubicación o reloj.
