# Consulta de rutinas en Android

La raíz del repositorio contiene una PWA estática (`index.html`, `manifest.webmanifest` y `sw.js`). La PWA muestra los cuatro HTML canónicos y precachea sus recursos locales publicados para que las sesiones sigan disponibles sin conexión.

## Uso en Android

1. Publicar el repositorio con un host HTTPS de archivos estáticos, por ejemplo GitHub Pages.
2. Abrir la URL publicada en Chrome para Android.
3. Pulsar `Instalar en Android` si aparece el botón, o usar el menú de Chrome → `Añadir a pantalla de inicio`.
4. Abrir la PWA instalada; el service worker descarga automáticamente la portada, las rutinas y sus medios locales.
5. En el gimnasio, abrir la PWA instalada sin conexión.

En una pestaña del navegador se puede consultar el plan y sus rutinas. La página muestra una invitación descartable para instalar Gymratik; el perfil, el historial y el registro de series solo se habilitan cuando la aplicación se abre en modo instalado.

La primera preparación del service worker guarda la portada, las cuatro rutinas canónicas y sus imágenes estáticas esenciales; los videos/GIF son opcionales. El splash mantiene separados el estado local y la preparación de recursos y muestra conteos de descargas. No hay sincronización de perfil, series o historial: esos datos permanecen en el almacenamiento local del dispositivo.

En `Mi perfil` → `Datos móviles para actualizaciones` el usuario puede elegir `Preguntar cada vez` (predeterminado), `Permitir siempre` o `Solo Wi‑Fi`. La autorización de una pregunta dura solo la apertura actual y aparece como controles accesibles dentro del splash, sin bloquearlo con un diálogo nativo del navegador. Se muestra el tamaño local estimado del paquete con desglose de aplicación e imágenes, expresado en KiB/MiB; la transferencia real puede variar. El usuario también puede continuar sin descargar; la versión disponible se abre y el estado de actualización queda pendiente. El navegador no siempre informa si la conexión es celular o Wi‑Fi; si no puede identificar Wi‑Fi, la opción `Solo Wi‑Fi` pospone la actualización. Durante la descarga se reportan recursos completados, no bytes de red.

## Persistencia del avance

El avance de series se guarda en `IndexedDB`, separado de la caché del service worker. La portada lee esa base local para mostrar series registradas, sesiones completadas y avance por rutina. Los registros antiguos de `localStorage` se migran al primer acceso sin cambiar las claves de compatibilidad de las rutinas.

La actividad se agrupa con la hora local del dispositivo: varios guardados en el mismo minuto se consolidan; dentro de la misma hora o del mismo día actualizan el mismo contexto; al detectar otro día se conserva el historial anterior y se marca una nueva jornada de actividad. Esta clasificación evita duplicados por cada clic y permite mostrar las series de hoy sin reiniciar silenciosamente una rutina incompleta.

La base IndexedDB v3 contiene el perfil local, el progreso, las sesiones y la actividad. Al abrir una base anterior a v3, la actualización elimina sus almacenes y crea una base v3 vacía; el historial guardado en esa base se pierde. También se eliminan las claves de respaldo local anteriores. La portada informa cuando se reinicia una base existente. En modo instalado, la portada permite editar el perfil, revisar sesiones recientes y exportar/importar respaldos JSON v3 después de validar el archivo y confirmar el reemplazo de datos.

Si `IndexedDB` no está disponible o una transacción falla por un error operativo, la aplicación usa un respaldo compacto nuevo en `localStorage` y muestra el estado de error en la portada. Los respaldos importados deben usar esquema 3. `Proteger almacenamiento` solicita al navegador persistencia adicional; no sustituye una copia externa y el usuario puede perder los datos al borrar los datos del sitio, usar navegación privada o cambiar de dispositivo. El perfil local no es una cuenta autenticada ni permite sincronización entre dispositivos.

## Actualización desde el repositorio

Al abrir la portada, la inicialización local y la comprobación/preparación estática ocurren en paralelo. La comprobación de versión y la descarga tienen presupuestos independientes de 20 s; el inicio local no tiene un timeout fijo. Al vencer uno, la última versión completa sigue disponible y el estado pendiente queda visible en la portada. Una actualización descargada después de abrir se mantiene en espera y se activa en una apertura posterior, sin reemplazar un worker que pueda servir una sesión abierta. Si la primera instalación no consigue una versión offline completa, el splash permanece visible y reintenta al recuperar conexión y cada 30 s.

Cada versión nueva se descarga a una caché separada y recibe una marca solo al completar el inventario. Solo una instalación completa puede tomar control (primera instalación) o quedar esperando activación; si una descarga falla, se elimina su caché parcial y la versión previa se conserva. La instalación exitosa limpia las cachés anteriores al activar. Ante error de cuota se intenta una vez más después de eliminar cachés obsoletas/incompletas propias de Gymratik; se conserva la versión anterior completa y nunca se alteran otras cachés.

Por tanto, el flujo de actualización es: publicar cambios y abrir la PWA con red y permiso según la preferencia elegida; el nuevo worker queda preparado y se aplica al volver a abrir la portada. Después la app puede funcionar sin conexión. No es necesario borrar datos ni reinstalarla.

Antes de publicar cambios en una rutina canónica o en `medios_publicados/`, regenerar el inventario con `python scripts/build_pwa_service_worker.py`. El workflow de validación compara el resultado generado con `sw.js` y rechaza publicaciones desactualizadas.

## Estado de publicación

La PWA no necesita backend ni credenciales. El host debe servir la raíz por HTTPS para que Android permita la instalación y el almacenamiento offline. Solo se copian a `data/rutinas_autocontenidas/medios_publicados/` los archivos referenciados por las tres rutinas; el resto de `artifacts/` continúa excluido por `.gitignore`.
