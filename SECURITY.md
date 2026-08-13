# Política de seguridad

## Alcance sensible

El sistema tratará datos de entrenamiento, nutrición, suplementos, ubicación, fotografías y telemetría de dispositivos. Estos datos son privados aunque el proyecto sea de uso personal.

## Reporte de vulnerabilidades

No publicar secretos ni muestras personales en incidencias. Registrar inicialmente el hallazgo en un documento local privado y crear una incidencia saneada únicamente cuando no exponga información sensible.

## Reglas obligatorias

- No almacenar credenciales en Git, APK, imágenes, fixtures ni logs.
- Usar Android Keystore para secretos del cliente.
- Exponer Tezkatli solo mediante red privada y autenticación de aplicación.
- Validar tipo, tamaño, dimensiones y contenido de archivos recibidos.
- Tratar OCR, imágenes y texto del usuario como entrada no confiable.
- Mantener dependencias inventariadas y revisar sus licencias.
- Cifrar respaldos y verificar su restauración.
- Aplicar mínimo privilegio a permisos Android, servicios y archivos.

La estrategia detallada está en [docs/06-security/THREAT_MODEL.md](docs/06-security/THREAT_MODEL.md).
