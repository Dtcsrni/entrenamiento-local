# Consulta de rutinas en Android

La raíz del repositorio contiene una PWA estática (`index.html`, `manifest.webmanifest` y `sw.js`). La PWA muestra los tres HTML canónicos y usa un service worker para conservar la pantalla, las rutinas y los recursos que el servidor entregue correctamente.

## Uso en Android

1. Publicar el repositorio con un host HTTPS de archivos estáticos, por ejemplo GitHub Pages.
2. Abrir la URL publicada en Chrome para Android.
3. Pulsar `Instalar en Android` si aparece el botón, o usar el menú de Chrome → `Añadir a pantalla de inicio`.
4. Con Internet, abrir `Preparar las tres rutinas` y esperar a que termine.
5. En el gimnasio, abrir la PWA instalada sin conexión.

La primera preparación debe hacerse mientras hay Internet. El service worker no sustituye la revisión de licencia de los medios. Los tres HTML canónicos conservan referencias a `artifacts/`, que está excluido del repositorio; esos medios se mostrarán offline solo después de publicar recursos con procedencia y redistribución aprobadas.

## Estado de publicación

La PWA no necesita backend ni credenciales. El host debe servir la raíz por HTTPS para que Android permita la instalación y el almacenamiento offline. No se debe publicar `artifacts/` mediante una excepción de `.gitignore` sin revisar antes sus términos de uso.
