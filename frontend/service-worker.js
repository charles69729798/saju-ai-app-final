const CACHE_NAME = 'saju-ai-v1.3';
const STATIC_ASSETS = [
    '/',
    '/manifest.json',
    '/icons/icon-192x192.png',
    '/icons/icon-512x512.png'
];

// 설치 시 정적 자산 캐싱
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('[SW] 정적 자산 캐싱 중...');
            return cache.addAll(STATIC_ASSETS);
        })
    );
    self.skipWaiting();
});

// 활성화 시 이전 캐시 정리
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            )
        )
    );
    self.clients.claim();
});

// 메인 페이지(/)는 네트워크 우선, 정적 파일은 캐시 우선 전략
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // API 요청은 네트워크 우선
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request)
                .catch(() => new Response(
                    JSON.stringify({ status: 'error', message: '오프라인 상태입니다. 인터넷 연결을 확인해주세요.' }),
                    { headers: { 'Content-Type': 'application/json' } }
                ))
        );
        return;
    }

    // 메인 페이지는 네트워크 우선 (업데이트 즉시 반영)
    if (url.pathname === '/' || url.pathname === '/index.html') {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // 기타 정적 파일은 캐시 우선
    event.respondWith(
        caches.match(event.request).then(cached => {
            if (cached) return cached;
            return fetch(event.request).then(response => {
                if (response.ok) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return response;
            });
        }).catch(() => {
            if (event.request.destination === 'document') {
                return caches.match('/');
            }
        })
    );
});
