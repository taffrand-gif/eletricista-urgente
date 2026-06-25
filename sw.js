const CACHE='norte-reparos-v1';
self.addEventListener('install',e=>{self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(clients.claim())});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 e.respondWith(
 caches.open(CACHE).then(cache=>
 cache.match(e.request).then(cached=>{
 const fetched=fetch(e.request).then(res=>{
 if(res.ok)cache.put(e.request,res.clone());
 return res;
 }).catch(()=>cached);
 return cached||fetched;
 })
 )
 );
});