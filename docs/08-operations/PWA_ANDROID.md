# Consulta de rutinas en Android

La raíz del repositorio contiene una PWA estática (`index.html`, `manifest.webmanifest` y `sw.js`). La PWA muestra los cuatro HTML canónicos y precachea sus recursos locales publicados para que las sesiones sigan disponibles sin conexión.

## Uso en Android

1. Publicar el repositorio con un host HTTPS de archivos estáticos, por ejemplo GitHub Pages.
2. Abrir la URL publicada en Chrome para Android.
3. Pulsar `Instalar en Android` si aparece el botón, o usar el menú de Chrome → `Añadir a pantalla de inicio`.
4. Abrir la PWA instalada; el service worker descarga automáticamente la portada, las rutinas y sus medios locales.
5. En el gimnasio, abrir la PWA instalada sin conexión.

La instalación del service worker precachea la portada, las cuatro rutinas y los medios locales referenciados por ellas. No existe una preparación manual: la PWA prioriza la copia local y sincroniza cambios en segundo plano cuando hay conexión.

## Persistencia del avance

El avance de series se guarda en `IndexedDB`, separado de la caché del service worker. La portada lee esa base local para mostrar series registradas, sesiones completadas y avance por rutina. Los registros antiguos de `localStorage` se migran al primer acceso sin cambiar las claves de compatibilidad de las rutinas.

La actividad se agrupa con la hora local del dispositivo: varios guardados en el mismo minuto se consolidan; dentro de la misma hora o del mismo día actualizan el mismo contexto; al detectar otro día se conserva el historial anterior y se marca una nueva jornada de actividad. Esta clasificación evita duplicados por cada clic y permite mostrar las series de hoy sin reiniciar silenciosamente una rutina incompleta.

La base IndexedDB v3 contiene el perfil local, el progreso, las sesiones y la actividad. Al abrir una base anterior a v3, la actualización elimina sus almacenes y crea una base v3 vacía; el historial guardado en esa base se pierde. También se eliminan las claves de respaldo local anteriores. La portada informa cuando se reinicia una base existente. La portada permite editar el perfil, revisar sesiones recientes y exportar/importar respaldos JSON v3 después de validar el archivo y confirmar el reemplazo de datos.

Si `IndexedDB` no está disponible o una transacción falla por un error operativo, la aplicación usa un respaldo compacto nuevo en `localStorage` y muestra el estado de error en la portada. Los respaldos importados deben usar esquema 3. `Proteger almacenamiento` solicita al navegador persistencia adicional; no sustituye una copia externa y el usuario puede perder los datos al borrar los datos del sitio, usar navegación privada o cambiar de dispositivo. El perfil local no es una cuenta autenticada ni permite sincronización entre dispositivos.

## Actualización desde el repositorio

Cada vez que se abre la portada, `index.html` solicita una comprobación de actualización de `sw.js` sin usar la caché HTTP. El generador cambia la versión del service worker cuando cambia cualquier recurso precacheado; si hay una versión nueva y conexión, el navegador instala el worker y precarga sus recursos antes de activarlo. La activación elimina la caché anterior, toma el control de las pestañas y solicita una sola recarga controlada. Si no hay red o la comprobación falla, la última versión disponible sigue funcionando desde la caché local. No se ejecuta una sincronización paralela de todos los recursos en cada apertura.

Por tanto, el flujo de actualización es: publicar cambios en el repositorio y abrir la PWA cuando haya conexión para recibir la actualización; después puede seguir funcionando sin conexión. No es necesario borrar datos ni reinstalarla.

Antes de publicar cambios en una rutina canónica o en `medios_publicados/`, regenerar el inventario con `python scripts/build_pwa_service_worker.py`. El workflow de validación compara el resultado generado con `sw.js` y rechaza publicaciones desactualizadas.

## Estado de publicación

La PWA no necesita backend ni credenciales. El host debe servir la raíz por HTTPS para que Android permita la instalación y el almacenamiento offline. Solo se copian a `data/rutinas_autocontenidas/medios_publicados/` los archivos referenciados por las tres rutinas; el resto de `artifacts/` continúa excluido por `.gitignore`.
