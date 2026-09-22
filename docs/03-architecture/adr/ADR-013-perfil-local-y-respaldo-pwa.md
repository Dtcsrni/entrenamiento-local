# ADR-013 — Perfil local, historial y respaldo de la PWA

**Estado:** Superseded por ADR-015
**Fecha:** 2026-09-21

## Contexto

La PWA estática necesita conservar un perfil básico y permitir administrar el historial de entrenamiento sin depender de Internet. La implementación previa guardaba progreso resumido en IndexedDB v2 y tenía un respaldo limitado en `localStorage`, sin perfil ni exportación/importación.

## Decisión

1. El perfil local será el propietario lógico de los registros y usará el identificador estable `local-default`.
2. La decisión histórica permitía migrar IndexedDB v2 a v3 añadiendo los almacenes `profiles` y `meta`, además del índice `profileId` en los almacenes existentes. Esta política fue reemplazada por ADR-015.
3. Los registros antiguos se asociarán al perfil local durante la migración; no se eliminarán ni se cambiarán las claves legacy de compatibilidad.
4. La portada permitirá editar fecha de nacimiento, sexo, altura, objetivo y unidades; estos datos no se enviarán a ningún servicio.
5. El historial conservará las sesiones resumidas existentes y sus estados (`active`, `completed`, `abandoned` o `edited`).
6. La exportación e importación usarán el formato versionado `gymratik-backup` y validarán el contenido antes de reemplazar datos. La importación requiere confirmación explícita.
7. No se implementará autenticación falsa con `localStorage`. Una cuenta multi-dispositivo, cookies seguras y passkeys requieren un backend posterior.

## Consecuencias

- La funcionalidad básica permanece offline y compatible con la PWA instalada.
- El usuario puede recuperar el perfil y el historial mediante un archivo JSON.
- El navegador o el sistema operativo todavía pueden borrar el almacenamiento local; el respaldo exportado es responsabilidad del usuario.
- El perfil local no equivale a una cuenta autenticada ni protege contra un dispositivo comprometido o XSS.
- La futura sincronización podrá reutilizar `profileId`, revisiones y una outbox sin rehacer la UI.

## Alternativas descartadas

- `localStorage` como base principal: no ofrece transacciones ni es adecuado para datos estructurados.
- Login local basado en una contraseña almacenada en el navegador: no proporciona identidad verificable.
- Backend inmediato: ampliaría el alcance de la PWA estática y exigiría definir identidad, recuperación, hosting y política de sincronización.

## Verificación

- Migración y contratos: `tests/test_progress_store.py`, `tests/test_progress_store_runtime.py`.
- UI y controles: `tests/test_homepage.py`.
- Validación global: `python scripts/validate_repository.py` y `python -m unittest discover -s tests -p "test_*.py"`.
