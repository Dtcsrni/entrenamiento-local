# ADR-015 — Uso exclusivo de la base local y respaldos v3

**Estado:** Parcialmente sustituida por el requisito de preservación de datos del 2026-09-24
**Fecha:** 2026-09-22

## Contexto

La aplicación usa IndexedDB con versión 3, pero el código todavía aceptaba respaldos de versiones anteriores y actualizaba automáticamente una base local antigua. El usuario solicitó operar únicamente con la versión más reciente, identificada como v3.

## Decisión

1. La versión operativa de IndexedDB es 3. Una base nueva se crea directamente con los almacenes e índices actuales.
2. El número de esquema activo sigue siendo 3, pero una actualización nunca elimina automáticamente almacenes existentes ni claves anteriores de `localStorage`. Añade los almacenes e índices requeridos que falten. La incompatibilidad de respaldos antiguos no autoriza borrar datos locales.
3. Los perfiles y respaldos usan `schemaVersion=3`. La importación exige versión 3 tanto en el respaldo como en su perfil; versiones anteriores se rechazan antes de escribir.
4. El fallback operativo nuevo de `localStorage` usa una clave v3. Si IndexedDB no está disponible o falla por una razón operativa, se usa ese fallback. Antes de mostrar el dashboard, se recuperan snapshots locales `fitlovers-day1-series-v1` a `fitlovers-day4-series-v1` cuando falta el registro central de esa rutina; los datos originales se conservan.
5. La importación solo acepta respaldos con versión 3 y perfil con `schemaVersion=3`.

## Consecuencias

- La base v3 existente y los respaldos v3 se conservan y operan con el esquema actual.
- El primer inicio con una base anterior conserva sus almacenes y el fallback; el progreso individual de las rutinas se reconcilia con el dashboard central cuando este no tiene ese registro.
- No hay conversión automática desde respaldos v1/v2. El usuario necesita una copia exportada con esquema 3 para restaurar datos en esta versión.
- Si falla la transacción de actualización, IndexedDB debe conservar su estado anterior según la atomicidad de la transacción; la PWA reporta el error y no trata una apertura fallida como una migración completada.

## Alternativas consideradas

- Eliminar automáticamente los almacenes antiguos para reiniciar. Se revoca porque una actualización de la PWA no debe borrar una sesión intermedia; se conserva la política v3 para perfiles y respaldos, separada de la retención local.
- Transformar todos los esquemas históricos. Se difiere; esta decisión solo exige preservación y recuperación de snapshots conocidos, no afirma compatibilidad semántica universal de stores desconocidos.

## Verificación

- `tests/test_progress_store_runtime.py`: bases v1/v2 actualizadas sin eliminar stores ni estado local de rutinas; respaldo anterior rechazado y respaldo v3 restaurado.
- `tests/test_progress_store.py`: contrato de versión v3 y ausencia de eliminación automática de stores.
- `python scripts/validate_repository.py`.
