/* StickyCallBar - Atlas - 2026-06-25
   Barre sticky mobile pour eletricista-urgente.pt
   - Téléphone cliquable (tel:)
   - WhatsApp cliquable
   - Masqué sur desktop (md:hidden)
   - 64px height, fond blanc, ombre subtile
   - Pas declaim agressif, prix transparent
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
  bar.style.cssText = [
    'position: fixed',
    'bottom: 0',
    'left: 0',
    'right: 0',
    'height: 64px',
    'background: #ffffff',
    'box-shadow: 0 -2px 8px rgba(0,0,0,0.12)',
    'display: flex',
    'z-index: 9999',
    'padding: 8px',
    'gap: 8px',
    'border-top: 1px solid #e5e7eb'
  ].join(';');
  
  var phoneBtn = document.createElement('a');
  phoneBtn.href = 'tel:' + PHONE;
  phoneBtn.setAttribute('aria-label', 'Ligar ' + PHONE_DISPLAY);
  phoneBtn.style.cssText = [
    'flex: 1',
    'display: flex',
    'align-items: center',
    'justify-content: center',
    'gap: 6px',
    'background: ' + COLOR_PRIMARY,
    'color: white',
    'text-decoration: none',
    'border-radius: 8px',
    'font-weight: 700',
    'font-size: 16px',
    'min-height: 48px',
    'font-family: -apple-system, BlinkMacSystemFont, sans-serif'
  ].join(';');
  phoneBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/></svg> Ligar';
  
  var waBtn = document.createElement('a');
  waBtn.href = WHATSAPP;
  waBtn.setAttribute('aria-label', 'Contactar via WhatsApp');
  waBtn.target = '_blank';
  waBtn.rel = 'noopener noreferrer';
  waBtn.style.cssText = [
    'flex: 1',
    'display: flex',
    'align-items: center',
    'justify-content: center',
    'gap: 6px',
    'background: #25D366',
    'color: white',
    'text-decoration: none',
    'border-radius: 8px',
    'font-weight: 700',
    'font-size: 16px',
    'min-height: 48px',
    'font-family: -apple-system, BlinkMacSystemFont, sans-serif'
  ].join(';');
  waBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-1-.3-.1-.5-.1-.7.1-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1s-1.2-.4-2.3-1.4c-.8-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.2-.6-.4z"/><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3.1 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.5 0-3-.4-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3C4 14.8 3.5 13.4 3.5 12c0-4.7 3.8-8.5 8.5-8.5s8.5 3.8 8.5 8.5-3.8 8.5-8.5 8.5z"/></svg> WhatsApp';
  
  bar.appendChild(phoneBtn);
  bar.appendChild(waBtn);
  document.body.appendChild(bar);
  
  document.body.style.paddingBottom = '72px';
})();
