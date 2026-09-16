# Consulta de rutinas en Android

La raíz del repositorio contiene una PWA estática (`index.html`, `manifest.webmanifest` y `sw.js`). La PWA muestra los tres HTML canónicos y usa un service worker para conservar la pantalla, las rutinas y los recursos que el servidor entregue correctamente.

## Uso en Android

1. Publicar el repositorio con un host HTTPS de archivos estáticos, por ejemplo GitHub Pages.
2. Abrir la URL publicada en Chrome para Android.
3. Pulsar `Instalar en Android` si aparece el botón, o usar el menú de Chrome → `Añadir a pantalla de inicio`.
4. Con Internet, abrir `Preparar las tres rutinas` y esperar a que termine.
5. En el gimnasio, abrir la PWA instalada sin conexión.

La primera preparación debe hacerse mientras hay Internet. El service worker no sustituye la revisión de procedencia de los medios. Los recursos referenciados por los tres HTML canónicos se publican por autorización expresa del propietario para este uso personal; esta autorización no debe interpretarse como una licencia general para reutilizar los medios fuera de este proyecto.

## Estado de publicación

La PWA no necesita backend ni credenciales. El host debe servir la raíz por HTTPS para que Android permita la instalación y el almacenamiento offline. Solo se copian a `data/rutinas_autocontenidas/medios_publicados/` los archivos referenciados por las tres rutinas; el resto de `artifacts/` continúa excluido por `.gitignore`.
