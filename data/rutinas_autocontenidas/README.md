# Rutinas autocontenidas conservadas

Este directorio conserva los materiales locales obtenidos durante la construcción de las rutinas. Las copias de `fuentes_locales/` no fueron modificadas.

## Base seleccionada para la unificación

La base canónica de trabajo para el Día 1 es la estructura visual y de navegación de la antigua v10, renumerada ahora como v1:

`canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html`

La v16 y la v20 fueron descartadas por errores en la revisión visual y se eliminaron de las fuentes activas. Los inventarios de `evidencia/` conservan únicamente el registro histórico de que fueron revisadas.

## Versiones conservadas

| Día | Archivo local conservado | Estado documentado |
|---|---|---|
| Día 2 | `fuentes_locales/Rutina_Dia_2_Pierna_Gluteo_Autocontenida_v6_mejoras_integradas.html` | Versión local final citada por el chat; 24 imágenes embebidas y sin URLs externas en el inventario realizado. |
| Día 1 | `fuentes_locales/Rutina_Dia_1_Espalda_Biceps_Autocontenida_v10_HEADER_REPARADO.html` | Fuente de la base canónica seleccionada; contiene recursos externos que se revisarán durante la unificación. |

## Recursos y evidencia

- `recursos_embebidos/` contiene los 55 binarios extraídos durante la auditoría inicial de los cuatro HTML locales, identificados por su SHA-256; se conservan como evidencia, aunque v16 y v20 ya fueron eliminadas de las fuentes activas.
- `evidencia/html_local_inventory.json` registra tamaños, referencias de imágenes y URLs externas por HTML.
- `evidencia/assets_embebidos_manifest.json` relaciona cada ocurrencia con su MIME, tamaño, hash y archivo extraído.
- `evidencia/EXTRACCION_PROYECTO.md` conserva el contexto de procedencia y los pendientes conocidos.
- `evidencia/repo_verification.json` y `evidencia/dia3_media_manifest.json` registran la comprobación del repositorio de ejercicios usado como referencia.

## Alcance y límites

Estas copias son un respaldo versionado de trabajo, no una certificación clínica ni una validación final de la rutina. El nombre del archivo conserva las etiquetas originales, pero el estado debe interpretarse con el inventario y la evidencia anteriores.

El repositorio de ejercicios de referencia es `https://github.com/hasaneyldrm/exercises-dataset`, commit `7455efae41b330c265e7cd4b78dfa848e7ce5ebd`. Su clon completo permanece local en `artifacts/ejercicios-compartido/` y no se duplica en este repositorio. El dataset declara medios de Gym visual; cualquier redistribución de esos medios requiere revisar sus términos y conservar la atribución correspondiente.

El Día 3 sigue pendiente: no debe tratarse como HTML terminado ni como 100 % autocontenido.
