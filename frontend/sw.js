const CACHE = 'cz-poker-v3';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.add('/')));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // API-Calls immer live holen, nie cachen
  if (url.pathname.startsWith('/auth/') ||
      url.pathname.startsWith('/sessions') ||
      url.pathname.startsWith('/tournaments') ||
      url.pathname.startsWith('/stats')) {
    e.respondWith(fetch(e.request));
    return;
  }

  // Statische Assets: Cache first, dann Netzwerk
  e.respondWith(
    caches.match(e.request).then(response => response || fetch(e.request))
  );
});
