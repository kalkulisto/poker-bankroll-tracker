const CACHE = 'cz-poker-v1';
const ASSETS = ['/', '/static/manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // API-Calls immer live holen
  if (e.request.url.includes('/auth/') || e.request.url.includes('/sessions') ||
      e.request.url.includes('/tournaments') || e.request.url.includes('/stats')) {
    return;
  }
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
