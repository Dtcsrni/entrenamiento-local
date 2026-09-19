# Consulta de rutinas en Android

La raíz del repositorio contiene una PWA estática (`index.html`, `manifest.webmanifest` y `sw.js`). La PWA muestra los tres HTML canónicos y precachea sus recursos locales publicados para que las sesiones sigan disponibles sin conexión.

## Uso en Android

1. Publicar el repositorio con un host HTTPS de archivos estáticos, por ejemplo GitHub Pages.
2. Abrir la URL publicada en Chrome para Android.
3. Pulsar `Instalar en Android` si aparece el botón, o usar el menú de Chrome → `Añadir a pantalla de inicio`.
4. Con Internet, abrir `Preparar sesiones` y esperar a que termine la primera sincronización.
5. En el gimnasio, abrir la PWA instalada sin conexión.

La instalación del service worker precachea la portada, las tres rutinas y los medios locales referenciados por ellas. La acción `Preparar sesiones` permite forzar una sincronización completa cuando haya conexión.

## Persistencia del avance

El avance de series se guarda en `IndexedDB`, separado de la caché del service worker. La portada lee esa base local para mostrar series registradas, sesiones completadas y avance por rutina. Los registros antiguos de `localStorage` se migran al primer acceso sin cambiar las claves de compatibilidad de las rutinas.

La actividad se agrupa con la hora local del dispositivo: varios guardados en el mismo minuto se consolidan; dentro de la misma hora o del mismo día actualizan el mismo contexto; al detectar otro día se conserva el historial anterior y se marca una nueva jornada de actividad. Esta clasificación evita duplicados por cada clic y permite mostrar las series de hoy sin reiniciar silenciosamente una rutina incompleta.

Si `IndexedDB` no está disponible o una transacción falla, la aplicación usa un respaldo compacto en `localStorage` y muestra el estado de error en la portada. `Proteger almacenamiento` solicita al navegador persistencia adicional; no sustituye una copia externa y el usuario puede perder los datos al borrar los datos del sitio, usar navegación privada o cambiar de dispositivo. La exportación/importación aún no forma parte del contrato actual.

## Actualización desde el repositorio

Al abrir la PWA con conexión, `index.html` solicita una comprobación de actualización de `sw.js` sin usar la caché HTTP. El service worker usa navegación `network-first`: obtiene la versión publicada más reciente y la guarda; si no hay red, sirve la última versión disponible en caché. Cuando cambia el service worker, activa la nueva caché inmediatamente y elimina la anterior. En cada sincronización también actualiza los recursos precacheados.

Por tanto, el flujo de actualización es: publicar cambios en el repositorio, abrir la PWA una vez con conexión y volver a usarla sin conexión. No es necesario borrar datos ni reinstalarla.

Antes de publicar cambios en una rutina canónica o en `medios_publicados/`, regenerar el inventario con `python scripts/build_pwa_service_worker.py`. El workflow de validación compara el resultado generado con `sw.js` y rechaza publicaciones desactualizadas.

## Estado de publicación

La PWA no necesita backend ni credenciales. El host debe servir la raíz por HTTPS para que Android permita la instalación y el almacenamiento offline. Solo se copian a `data/rutinas_autocontenidas/medios_publicados/` los archivos referenciados por las tres rutinas; el resto de `artifacts/` continúa excluido por `.gitignore`.
