# Modelo de amenazas

## Activos

- Historial de salud y rendimiento.
- Alimentación y suplementos.
- Fotografías y metadatos.
- Ubicación y horarios.
- Tokens, claves y respaldos.
- Modelos, prompts y datos de evaluación.

## Límites de confianza

1. Usuario ↔ Android.
2. Android ↔ sistema operativo/Health Connect.
3. Android ↔ red privada ↔ Tezkatli.
4. Amazfit ↔ Zepp App/Side Service.
5. Side Service ↔ Tezkatli.
6. Tezkatli ↔ catálogos/modelos importados.

## Amenazas STRIDE y mitigaciones

| Categoría | Ejemplo | Control inicial |
|---|---|---|
| Spoofing | cliente falso accede a Tezkatli | identidad VPN + token de app |
| Tampering | evento o respaldo modificado | TLS, hashes, validación y revisiones |
| Repudiation | corrección sin procedencia | auditoría selectiva y timestamps |
| Information disclosure | fotos en logs/backups | minimización, cifrado y retención |
| Denial of service | imagen agota RAM/VRAM | límites y cola con concurrencia acotada |
| Elevation of privilege | texto visual induce herramientas | LLM sin herramientas y salida esquemática |

## Validación de archivos

- Tamaño máximo de solicitud y píxeles.
- MIME verificado por contenido.
- Decodificación aislada y límites de memoria.
- Nombres generados internamente.
- Sin rutas proporcionadas por cliente.
- EXIF eliminado salvo necesidad explícita.
- TTL de temporales.

## Seguridad móvil

- Permisos mínimos y solicitados en contexto.
- Android Keystore para claves.
- Network Security Config restrictiva.
- Componentes no exportados salvo necesidad.
- Intents y deep links validados.
- Datos sensibles fuera de notificaciones y screenshots cuando se decida.
- Verificación guiada por OWASP MASVS.

## Cadena de suministro

- Dependencias fijadas mediante lockfiles/catálogos.
- Procedencia y licencia de modelos/datasets.
- Hashes de pesos.
- SBOM para releases.
- Escaneo de secretos y vulnerabilidades.
- Actualizaciones revisadas, no automáticas a producción.

## Privacidad

- Procesamiento local por defecto.
- Consentimiento separado para Health Connect y ubicación.
- Retención configurable.
- Exportación y eliminación.
- Telemetría local sin contenido personal.
- No reutilizar datos personales para otros fines.

## Pendientes

- DFD detallado al existir endpoints.
- Análisis MASVS del APK release.
- Prueba de exposición de Tezkatli.
- Decisión final de cifrado de base local.
