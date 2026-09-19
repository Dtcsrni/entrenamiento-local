const CACHE_NAME = 'entrenamiento-pwa-a59e0c4bfba0';
const PRECACHE = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon.svg',
  './progress-store.js',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_2_Pierna_Gluteo_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0194-2IxROQ1-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0194-2IxROQ1-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0194-2IxROQ1-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0197-qdRxqCj.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0200-dU605di-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0200-dU605di-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0200-dU605di-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0257-X7jbxra.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0577-T0yTjgW-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0577-T0yTjgW-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0577-T0yTjgW-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0577-T0yTjgW.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0584-dRTfGZT-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0584-dRTfGZT-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0584-dRTfGZT-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0585-my33uHU.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0592-b6hQYMb-final.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0592-b6hQYMb-machine-only.webp',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0592-b6hQYMb.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0596-v3xmPAR-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0596-v3xmPAR-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0596-v3xmPAR-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0599-Zg3XY7P.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0602-myfUsKf.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0605-ykUOVze.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0739-10Z2DXU.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0743-Qa55kX1.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/0798-a8VDgLw.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1299-jHAnWmT-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1299-jHAnWmT-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1299-jHAnWmT-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1350-7I6LNUG-final.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1350-7I6LNUG.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1356-OIFMAp1.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/1512-qBcKorM.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/2141-rjtuP6X.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/2318-dNFYIU1-final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/2318-dNFYIU1-machine-only.png',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/2318-dNFYIU1-start.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/3025-butterfly-reverse-front.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/3666-rjiM4L3.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/warmup-arm-circles-filmed.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/images/warmup-shoulder-rolls-filmed.jpg',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0194-2IxROQ1.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0197-qdRxqCj.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0200-dU605di.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0257-X7jbxra.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0577-T0yTjgW.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0584-dRTfGZT.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0585-my33uHU.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0592-b6hQYMb.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0596-v3xmPAR.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0599-Zg3XY7P.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0602-myfUsKf.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0605-ykUOVze.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0739-10Z2DXU.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0743-Qa55kX1.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/0798-a8VDgLw.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/1299-jHAnWmT.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/1350-7I6LNUG.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/1356-OIFMAp1.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/1512-qBcKorM.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/2141-rjtuP6X.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/2318-dNFYIU1.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/3666-rjiM4L3.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/warmup-arm-circles-filmed.gif',
  './data/rutinas_autocontenidas/medios_publicados/ejercicios-compartido/videos/warmup-shoulder-rolls-filmed.gif',
  './data/rutinas_autocontenidas/medios_publicados/rutinas_autocontenidas/dia2_media_generated/ankle_circles_real_mymichigan.gif',
  './data/rutinas_autocontenidas/medios_publicados/rutinas_autocontenidas/dia2_media_generated/ankle_circles_real_mymichigan.jpg',
  './data/rutinas_autocontenidas/medios_publicados/rutinas_autocontenidas/dia2_media_generated/hip_thrust_machine_booty_builder_correct_form.gif',
  './data/rutinas_autocontenidas/medios_publicados/rutinas_autocontenidas/dia2_media_generated/hip_thrust_machine_booty_builder_correct_form.jpg',
  './data/rutinas_autocontenidas/medios_publicados/rutinas_autocontenidas/dia2_media_generated/hip_thrust_machine_booty_builder_correct_form_final.jpg',
  './data/rutinas_autocontenidas/medios_publicados/rutinas_autocontenidas/dia2_media_generated/hip_thrust_machine_booty_builder_correct_form_inicio.jpg',
  './data/rutinas_autocontenidas/recursos_embebidos/b963bc266356a83bea4fe9909f0516c0c3a1543c06c8a17d24ca9d674fe3c759.png'
];

const ROUTINE_URLS = [
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_2_Pierna_Gluteo_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html'
];
const LOCAL_REFERENCE = /(?:src|data-static-src|gif|thumbnail)\s*[:=]\s*[\"'](\.\.[^\"']+)[\"']/g;

async function refresh(request, cache) {
  const response = await fetch(request, { cache: 'no-store' });
  if (response.ok) await cache.put(request, response.clone());
  return response;
}

async function refreshRoutine(url, cache) {
  const response = await fetch(url, { cache: 'no-store' });
  if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
  await cache.put(url, response.clone());
  const html = await response.text();
  const base = new URL(url, self.location.href);
  const assetUrls = [...html.matchAll(LOCAL_REFERENCE)]
    .map((match) => new URL(match[1], base))
    .filter((assetUrl) => assetUrl.origin === self.location.origin)
    .map(String);
  await Promise.allSettled([...new Set(assetUrls)].map((assetUrl) => refresh(assetUrl, cache)));
}

async function refreshApplication() {
  const cache = await caches.open(CACHE_NAME);
  await Promise.allSettled(PRECACHE.map((url) => refresh(new Request(url), cache)));
  await Promise.allSettled(ROUTINE_URLS.map((url) => refreshRoutine(url, cache)));
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
      .then(() => refreshApplication())
  );
});

self.addEventListener('message', (event) => {
  if (event.data?.type === 'SYNC_APP') event.waitUntil(refreshApplication());
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    const isNavigation = request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html');
    const bypassCache = ['no-cache', 'no-store', 'reload'].includes(request.cache);

    if (!isNavigation && cached && !bypassCache) {
      event.waitUntil(refresh(request, cache).catch(() => undefined));
      return cached;
    }
    try {
      return await refresh(request, cache);
    } catch (error) {
      if (cached) return cached;
      if (isNavigation) return cache.match(new URL('./index.html', self.registration.scope));
      throw error;
    }
  })());
});
