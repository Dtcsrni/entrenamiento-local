# Extracción del proyecto de rutinas

Fecha de revisión: 2026-09-12

## Fuentes revisadas

- Proyecto: `Proyectos Personales ERVC`
- Chats revisados: Día 1, Día 2 y Día 3.
- Repositorio clonado: `https://github.com/hasaneyldrm/exercises-dataset`
- Commit verificado: `7455efae41b330c265e7cd4b78dfa848e7ce5ebd`

## Material local incorporado

Se copiaron sin modificar los cuatro HTML que ya estaban en `D:\Downloads` a `html_fuente_local/`.

Se extrajeron de esos HTML 101 referencias `data:image` y 55 binarios únicos en `assets_embebidos_html/`:

- 16 GIF
- 45 JPEG
- 40 PNG

La relación completa está en `assets_embebidos_manifest.json`; el inventario por HTML está en `html_local_inventory.json`.

No se copiaron las cuatro imágenes ajenas de documentos académicos que estaban en `D:\Downloads`.

## Estado de las rutinas

### Día 1

El proyecto identifica la v21 reconstruida como la base mejorada: 7 ejercicios, 20 series efectivas, 6 máquinas y una estación de polea. La propia respuesta del proyecto deja `Pullover Machine` y `curl martillo` como recursos visuales pendientes de sustituir por medios exactos.

La v21 fue identificada en el proyecto, pero su descarga abre un `backend-api/estuary/content` bloqueado por Edge en este entorno. Por eso no se presenta como archivo local extraído. Las versiones locales disponibles sí se conservaron para comparación.

### Día 2

La versión local v6 coincide con el archivo final citado por el chat: 6 tarjetas, 24 imágenes embebidas y cero referencias externas según la descripción del proyecto. Se conserva el HTML y se auditará visualmente antes de reutilizarlo.

### Día 3

El chat define 7 ejercicios y 22 series efectivas: 4 + 3 + 3 + 3 + 3 + 3 + 3. La versión descrita no es completamente offline porque sus 7 GIF se cargan desde GitHub.

El proyecto afirmó correspondencia exacta con siete claves de GIF. La comprobación contra el commit clonado encontró que solo `0577-T0yTjgW` coincide literalmente. Los otros seis nombres no existen en el repositorio actual; el registro correcto por número de ejercicio usa otros `media_id`. La tabla verificable está en `dia3_media_manifest.json` y los medios corregidos están en `dia3_media_repo_verificada/`.

## Repositorio de ejercicios

El repositorio completo está en `artifacts/ejercicios-compartido/`, incluyendo `data/exercises.json`, `data/exercises.schema.json`, `images/` y `videos/`.

El dataset declara medios de Gym visual. La atribución requerida es `© Gym visual — https://gymvisual.com/`; el propio repositorio indica que su clonación no sustituye la revisión de los términos de reutilización. No se deben incrustar estos medios en una aplicación distribuible sin revisar/licenciar ese uso.

## Pendientes explícitos

1. Recuperar el binario v21 del adjunto del proyecto mediante una ruta de descarga que no sea bloqueada por Edge, o volver a adjuntarlo localmente.
2. Obtener y verificar las fotografías reales de las máquinas exactas para Día 1; los GIF genéricos del dataset no demuestran que sean máquinas Panatta ni que correspondan a la estación del gimnasio.
3. No etiquetar Día 3 como `100 % autocontenida` hasta incrustar los binarios y comprobar que no quedan URLs externas.
4. No incluir medios del repositorio en una versión pública de la aplicación sin resolver atribución y licencia.
