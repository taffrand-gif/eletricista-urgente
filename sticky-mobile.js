/* StickyCallBar - Atlas - 2026-06-25
   Barre sticky mobile pour eletricista-urgente.pt
   - Téléphone cliquable (tel:)
   - WhatsApp cliquable
   - Masqué sur desktop (md:hidden)
   - 64px height, fond blanc, ombre subtile
*/
(function() {
  'use strict';
  var isMobile = window.matchMedia('(max-width: 767px)').matches;
  if (!isMobile) return;
  if (sessionStorage.getItem('stickybar_shown_eu')) return;
  sessionStorage.setItem('stickybar_shown_eu', '1');
  var PHONE = '+351932321892';
  var PHONE_DISPLAY = '932 321 892';
  var WHATSAPP = 'https://wa.me/351932321892?text=Olá%2C%20preciso%20de%20eletricista%20urgente';
  var COLOR_PRIMARY = '#FF6B35';
  var bar = document.createElement('div');
  bar.setAttribute('role', 'navigation');
  bar.setAttribute('aria-label', 'Contacto urgente');
  bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;height:64px;background:#fff;box-shadow:0 -2px 8px rgba(0,0,0,0.12);display:flex;z-index:9999;padding:8px;gap:8px;border-top:1px solid #e5e7eb';
  var phoneBtn = document.createElement('a');
  phoneBtn.href = 'tel:' + PHONE;
  phoneBtn.setAttribute('aria-label', 'Ligar ' + PHONE_DISPLAY);
  phoneBtn.style.cssText = 'flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:' + COLOR_PRIMARY + ';color:white;text-decoration:none;border-radius:8px;font-weight:700;font-size:16px;min-height:48px;font-family:-apple-system,BlinkMacSystemFont,sans-serif';
  phoneBtn.innerHTML = '📞 Ligar';
  var waBtn = document.createElement('a');
  waBtn.href = WHATSAPP;
  waBtn.setAttribute('aria-label', 'WhatsApp');
  waBtn.target = '_blank';
  waBtn.rel = 'noopener noreferrer';
  waBtn.style.cssText = 'flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:#25D366;color:white;text-decoration:none;border-radius:8px;font-weight:700;font-size:16px;min-height:48px;font-family:-apple-system,BlinkMacSystemFont,sans-serif';
  waBtn.innerHTML = '💬 WhatsApp';
  bar.appendChild(phoneBtn);
  bar.appendChild(waBtn);
  document.body.appendChild(bar);
  document.body.style.paddingBottom = '72px';
})();
