(() => {
  'use strict';

  const DISMISS_KEY = 'gymratik-install-invite-dismissed-v1';
  const ACCEPTED_KEY = 'gymratik-install-confirmed-v1';
  let deferredInstallPrompt;

  function isInstalled() {
    let acceptedThisSession = false;
    try { acceptedThisSession = window.sessionStorage.getItem(ACCEPTED_KEY) === 'true'; } catch (_) {}
    return acceptedThisSession
      || window.matchMedia?.('(display-mode: standalone)').matches === true
      || window.navigator.standalone === true;
  }

  function isDismissed() {
    try { return window.sessionStorage.getItem(DISMISS_KEY) === 'true'; } catch (_) { return false; }
  }

  function emitStateChange() {
    window.dispatchEvent(new CustomEvent('gymratik-install-state-change', { detail: { installed: isInstalled() } }));
  }

  function ensureInvite() {
    if (document.querySelector('#gymratikInstallInvite')) return document.querySelector('#gymratikInstallInvite');
    const invite = document.createElement('aside');
    invite.id = 'gymratikInstallInvite';
    invite.setAttribute('aria-labelledby', 'gymratikInstallTitle');
    invite.innerHTML = '<div class="gymratik-install-invite-copy"><strong id="gymratikInstallTitle">Instala Gymratik</strong><span>Instala la aplicación para guardar tu perfil y el avance de tus rutinas. En Compartir o en el menú del navegador, elige «Añadir a pantalla de inicio» o «Instalar aplicación».</span></div><button class="gymratik-install-action" type="button" hidden>Instalar</button><button class="gymratik-install-dismiss" type="button" aria-label="Cerrar invitación y continuar">×</button>';
    const style = document.createElement('style');
    style.textContent = '#gymratikInstallInvite{position:fixed;z-index:10000;top:max(12px,env(safe-area-inset-top));left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;width:min(720px,calc(100vw - 24px));padding:12px 48px 12px 16px;border:1px solid rgba(115,230,207,.48);border-radius:16px;background:rgba(9,25,36,.97);box-shadow:0 14px 40px rgba(0,0,0,.38);color:#f5f8f7;font:14px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif}#gymratikInstallInvite[hidden]{display:none!important}.gymratik-install-invite-copy{display:grid;gap:3px;min-width:0}.gymratik-install-invite-copy strong{color:#73e6cf;font-size:15px}.gymratik-install-action{flex:0 0 auto;min-height:38px;padding:7px 12px;border:0;border-radius:10px;background:#73e6cf;color:#09231e;font:inherit;font-weight:850;cursor:pointer}.gymratik-install-dismiss{position:absolute;top:5px;right:7px;width:32px;height:32px;border:0;border-radius:50%;background:transparent;color:#d7e4ea;font:24px/1 system-ui,sans-serif;cursor:pointer}.gymratik-install-dismiss:hover{background:rgba(255,255,255,.1)}@media(max-width:520px){#gymratikInstallInvite{align-items:flex-start;gap:8px;padding:11px 42px 11px 12px;font-size:12px}.gymratik-install-invite-copy strong{font-size:14px}.gymratik-install-action{min-height:34px;padding:6px 9px;font-size:12px}}';
    document.head.append(style);
    document.body.append(invite);
    invite.querySelector('.gymratik-install-dismiss').addEventListener('click', () => {
      try { window.sessionStorage.setItem(DISMISS_KEY, 'true'); } catch (_) {}
      invite.hidden = true;
    });
    const installButton = invite.querySelector('.gymratik-install-action');
    installButton.hidden = !deferredInstallPrompt || isInstalled() || isDismissed();
    installButton.addEventListener('click', async () => {
      if (!deferredInstallPrompt) return;
      installButton.disabled = true;
      try {
        await deferredInstallPrompt.prompt();
        const choice = await deferredInstallPrompt.userChoice;
        if (choice?.outcome === 'accepted') {
          try { window.sessionStorage.setItem(ACCEPTED_KEY, 'true'); } catch (_) {}
          syncState();
        }
      } finally {
        deferredInstallPrompt = undefined;
        installButton.hidden = true;
        installButton.disabled = false;
      }
    });
    return invite;
  }

  function syncState() {
    const installed = isInstalled();
    document.documentElement.dataset.gymratikInstalled = installed ? 'true' : 'false';
    const invite = document.querySelector('#gymratikInstallInvite');
    if (invite) invite.hidden = installed || isDismissed();
    document.querySelectorAll('.exerciseTracker').forEach((tracker) => {
      tracker.inert = !installed;
      tracker.querySelectorAll('input, button').forEach((control) => { control.disabled = !installed; });
    });
    emitStateChange();
  }

  window.GymratikInstallGate = Object.freeze({ isInstalled });
  document.documentElement.dataset.gymratikInstalled = isInstalled() ? 'true' : 'false';
  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
    const invite = document.querySelector('#gymratikInstallInvite');
    if (invite && !isInstalled() && !isDismissed()) invite.querySelector('.gymratik-install-action').hidden = false;
  });
  window.addEventListener('appinstalled', () => {
    try { window.sessionStorage.setItem(ACCEPTED_KEY, 'true'); } catch (_) {}
    syncState();
  });
  window.matchMedia?.('(display-mode: standalone)').addEventListener?.('change', syncState);
  document.addEventListener('DOMContentLoaded', () => {
    ensureInvite();
    syncState();
  }, { once: true });
})();
