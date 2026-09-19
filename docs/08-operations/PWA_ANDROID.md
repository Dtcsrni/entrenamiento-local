# Consulta de rutinas en Android

La raíz del repositorio contiene una PWA estática (`index.html`, `manifest.webmanifest` y `sw.js`). La PWA muestra los tres HTML canónicos y precachea sus recursos locales publicados para que las sesiones sigan disponibles sin conexión.

## Uso en Android

1. Publicar el repositorio con un host HTTPS de archivos estáticos, por ejemplo GitHub Pages.
2. Abrir la URL publicada en Chrome para Android.
3. Pulsar `Instalar en Android` si aparece el botón, o usar el menú de Chrome → `Añadir a pantalla de inicio`.
4. Abrir la PWA instalada; el service worker descarga automáticamente la portada, las rutinas y sus medios locales.
5. En el gimnasio, abrir la PWA instalada sin conexión.

La instalación del service worker precachea la portada, las tres rutinas y los medios locales referenciados por ellas. No existe una preparación manual: la PWA prioriza la copia local y sincroniza cambios en segundo plano cuando hay conexión.

## Persistencia del avance

El avance de series se guarda en `IndexedDB`, separado de la caché del service worker. La portada lee esa base local para mostrar series registradas, sesiones completadas y avance por rutina. Los registros antiguos de `localStorage` se migran al primer acceso sin cambiar las claves de compatibilidad de las rutinas.

La actividad se agrupa con la hora local del dispositivo: varios guardados en el mismo minuto se consolidan; dentro de la misma hora o del mismo día actualizan el mismo contexto; al detectar otro día se conserva el historial anterior y se marca una nueva jornada de actividad. Esta clasificación evita duplicados por cada clic y permite mostrar las series de hoy sin reiniciar silenciosamente una rutina incompleta.

Si `IndexedDB` no está disponible o una transacción falla, la aplicación usa un respaldo compacto en `localStorage` y muestra el estado de error en la portada. `Proteger almacenamiento` solicita al navegador persistencia adicional; no sustituye una copia externa y el usuario puede perder los datos al borrar los datos del sitio, usar navegación privada o cambiar de dispositivo. La exportación/importación aún no forma parte del contrato actual.

## Actualización desde el repositorio

Al abrir la PWA, `index.html` solicita una comprobación de actualización de `sw.js` sin usar la caché HTTP. El service worker usa una estrategia `cache-first`: entrega inmediatamente la copia local y actualiza esa copia en segundo plano cuando hay conexión; si no hay red, la última versión disponible sigue funcionando. La caché está versionada y se precarga completa antes de activar una versión nueva, evitando mezclar archivos incompatibles. Cuando cambia el service worker, activa la nueva caché inmediatamente, solicita una recarga controlada de las pestañas abiertas y elimina la anterior. En cada sincronización también actualiza los recursos precacheados.

Por tanto, el flujo de actualización es: publicar cambios en el repositorio y abrir la PWA cuando haya conexión para recibir la actualización; después puede seguir funcionando sin conexión. No es necesario borrar datos ni reinstalarla.

Antes de publicar cambios en una rutina canónica o en `medios_publicados/`, regenerar el inventario con `python scripts/build_pwa_service_worker.py`. El workflow de validación compara el resultado generado con `sw.js` y rechaza publicaciones desactualizadas.

## Estado de publicación

La PWA no necesita backend ni credenciales. El host debe servir la raíz por HTTPS para que Android permita la instalación y el almacenamiento offline. Solo se copian a `data/rutinas_autocontenidas/medios_publicados/` los archivos referenciados por las tres rutinas; el resto de `artifacts/` continúa excluido por `.gitignore`.
