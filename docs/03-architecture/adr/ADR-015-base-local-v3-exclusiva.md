# ADR-015 — Uso exclusivo de la base local y respaldos v3

**Estado:** Accepted
**Fecha:** 2026-09-22

## Contexto

La aplicación usa IndexedDB con versión 3, pero el código todavía aceptaba respaldos de versiones anteriores y actualizaba automáticamente una base local antigua. El usuario solicitó operar únicamente con la versión más reciente, identificada como v3.

## Decisión

1. La versión operativa de IndexedDB es 3. Una base nueva se crea directamente con los almacenes e índices actuales.
2. Si IndexedDB ya existe con una versión menor que 3, la transacción de actualización elimina sus almacenes y crea el esquema v3 vacío. Al completar la apertura, se elimina la clave de fallback v1. Se conservan las claves `fitlovers-day1-series-v1` a `fitlovers-day4-series-v1`: las rutinas canónicas aún las usan para guardar y restaurar el progreso individual de series.
3. Los perfiles y respaldos usan `schemaVersion=3`. La importación exige versión 3 tanto en el respaldo como en su perfil; versiones anteriores se rechazan antes de escribir.
4. El fallback operativo de `localStorage` usa una clave v3. Si IndexedDB no está disponible o falla por una razón operativa, se usa ese fallback; no se lee ni migra información de claves previas.
5. La importación solo acepta respaldos con versión 3 y perfil con `schemaVersion=3`.

## Consecuencias

- La base v3 existente y los respaldos v3 se conservan y operan con el esquema actual.
- El primer inicio con una base anterior elimina los datos del historial y el fallback v1, y empieza un historial vacío en v3; la portada lo comunica. El progreso individual de las cuatro rutinas permanece disponible para su restauración local.
- No hay conversión automática desde respaldos v1/v2. El usuario necesita una copia exportada con esquema 3 para restaurar datos en esta versión.
- Si falla la transacción de actualización, IndexedDB debe conservar su estado anterior según la atomicidad de la transacción; la PWA reporta el error y no trata una apertura fallida como una migración completada.

## Alternativas consideradas

- Migrar bases anteriores a v3 para preservar historial. Se descartó a petición del usuario para reiniciar con v3 únicamente.
- Mantener accesibles bases anteriores. Se descartó para evitar operar con múltiples esquemas y formatos locales.

## Verificación

- `tests/test_progress_store_runtime.py`: bases v1/v2 reiniciadas a esquema v3 vacío, respaldo anterior rechazado y respaldo v3 restaurado.
- `tests/test_progress_store.py`: contrato de versión v3 y ausencia de importación de esquemas anteriores.
- `python scripts/validate_repository.py`.
