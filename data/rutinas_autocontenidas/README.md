# Rutinas autocontenidas conservadas

Este directorio conserva los materiales locales obtenidos durante la construcción de las rutinas. Las copias de `fuentes_locales/` no fueron modificadas.

## Base seleccionada para la unificación

La plantilla canónica vigente para nuevas rutinas es la estructura visual, funcional y de navegación de esta versión del Día 1:

`canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html`

Este archivo es la fuente de verdad de la plantilla: conserva la interacción, el seguimiento, el calentamiento, la iconografía y la adaptación táctil. Los generadores de otras rutinas deben tomarlo como `TEMPLATE` sin duplicar una segunda plantilla.

La v16 y la v20 fueron descartadas por errores en la revisión visual y se eliminaron de las fuentes activas. Los inventarios de `evidencia/` conservan únicamente el registro histórico de que fueron revisadas.

## Versiones conservadas

| Día | Archivo local conservado | Estado documentado |
|---|---|---|
| Día 2 | `fuentes_locales/Rutina_Dia_2_Pierna_Gluteo_Autocontenida_v6_mejoras_integradas.html` | Versión local final citada por el chat; 24 imágenes embebidas y sin URLs externas en el inventario realizado. |
| Día 1 | `fuentes_locales/Rutina_Dia_1_Espalda_Biceps_Autocontenida_v10_HEADER_REPARADO.html` | Fuente de la base canónica seleccionada; contiene recursos externos que se revisarán durante la unificación. |
| Día 4 | `canonicas/Rutina_Dia_4_Pierna_Equilibrio_V1.html` | Salida canónica generada desde la plantilla compartida; 7 ejercicios, 20 series y medios locales con revisión de derechos pendiente. |

La versión canónica trabajada del Día 2 es `canonicas/Rutina_Dia_2_Pierna_Gluteo_V1.html`; su contenido y límites se documentan en `DIA_2_CONTENIDO_Y_MAQUETACION.md` y `evidencia/dia2_media_manifest.json`.

## Contrato de formato canónico

Los cuatro días comparten el mismo orden de pantalla: cabecera de sesión, reglas
rápidas, calentamiento visible y obligatorio, resumen, progreso de sesión,
preparación, dashboard, nota, tarjetas de ejercicios, resumen flotante y
reinicio al final. Las tarjetas viven dentro de un único `<main class="cards">`
y cada una declara `data-exercise-index="N"`; el tracker interno conserva
`data-exercise="N"` y las claves `eNs1..eNsM`.

El contenido, el número de ejercicios, la distribución de series, los medios y
las claves de progreso siguen siendo específicos de cada día. La plantilla del
Día 1 define la estructura compartida; los builders del Día 2, Día 3 y Día 4 deben
validar esta forma antes de escribir una salida canónica.

## Recursos y evidencia

- `recursos_embebidos/` contiene los 55 binarios extraídos durante la auditoría inicial de los cuatro HTML locales, identificados por su SHA-256; se conservan como evidencia, aunque v16 y v20 ya fueron eliminadas de las fuentes activas.
- `evidencia/html_local_inventory.json` registra tamaños, referencias de imágenes y URLs externas por HTML.
- `evidencia/assets_embebidos_manifest.json` relaciona cada ocurrencia con su MIME, tamaño, hash y archivo extraído.
- `evidencia/EXTRACCION_PROYECTO.md` conserva el contexto de procedencia y los pendientes conocidos.
- `evidencia/repo_verification.json`, `evidencia/dia3_media_manifest.json` y `evidencia/dia4_media_manifest.json` registran la comprobación del repositorio de ejercicios usado como referencia.

## Alcance y límites

Estas copias son un respaldo versionado de trabajo, no una certificación clínica ni una validación final de la rutina. El nombre del archivo conserva las etiquetas originales, pero el estado debe interpretarse con el inventario y la evidencia anteriores.

El repositorio de ejercicios de referencia es `https://github.com/hasaneyldrm/exercises-dataset`, commit `7455efae41b330c265e7cd4b78dfa848e7ce5ebd`. Su clon completo permanece local en `artifacts/ejercicios-compartido/` y no se duplica en este repositorio.

Los HTML canónicos son salidas de trabajo verificables, no certificaciones
clínicas ni confirmaciones del inventario físico. La procedencia y los derechos
de los medios permanecen separados de la validación estructural; los manifiestos
conservan explícitamente ese estado pendiente.
