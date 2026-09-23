(() => {
  'use strict';

  const DISMISS_KEY = 'gymratik-install-invite-dismissed-v1';
  const ACCEPTED_KEY = 'gymratik-install-confirmed-v1';
  const ASSET_ROOT = new URL('.', document.currentScript?.src || window.location.href);
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
    const invite = document.createElement('dialog');
    invite.id = 'gymratikInstallInvite';
    invite.setAttribute('aria-labelledby', 'gymratikInstallTitle');
    invite.setAttribute('aria-describedby', 'gymratikInstallDescription');
    invite.innerHTML = `<section class="gymratik-install-card"><button class="gymratik-install-dismiss" type="button" aria-label="Cerrar invitación y continuar">×</button><div class="gymratik-install-art"><img src="${new URL('data/profile/mascot-install-phone.webp', ASSET_ROOT).href}" alt="La mascota de Gymratik sostiene un celular con la aplicación lista"></div><div class="gymratik-install-content"><p class="gymratik-install-kicker">Tu rutina, siempre a mano</p><h2 id="gymratikInstallTitle">Lleva Gymratik contigo</h2><p id="gymratikInstallDescription" class="gymratik-install-description">Instala la aplicación para crear tu perfil y guardar tus series y tu progreso.</p><p class="gymratik-install-help">En esta pestaña puedes consultar las rutinas. Para instalar, usa Compartir o el menú del navegador y elige «Añadir a pantalla de inicio» o «Instalar aplicación».</p><button class="gymratik-install-action" type="button" hidden>Instalar ahora</button></div></section>`;
    const style = document.createElement('style');
    style.textContent = '#gymratikInstallInvite{position:fixed;inset:0;display:grid;place-items:center;box-sizing:border-box;width:100vw;height:100dvh;max-width:none;max-height:none;margin:0;padding:20px;border:0;background:rgba(3,10,16,.82);color:#f5f8f7;font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;backdrop-filter:blur(7px)}#gymratikInstallInvite:not([open]){display:none!important}#gymratikInstallInvite::backdrop{background:rgba(3,10,16,.82)}.gymratik-install-card{position:relative;display:grid;grid-template-columns:minmax(250px,.9fr) minmax(0,1.1fr);align-items:center;gap:24px;width:min(920px,calc(100vw - 40px));min-height:500px;max-height:calc(100dvh - 40px);margin:auto;padding:clamp(24px,4vw,48px);overflow:auto;border:1px solid rgba(115,230,207,.45);border-radius:30px;background:radial-gradient(circle at 10% 15%,rgba(55,199,173,.15),transparent 40%),linear-gradient(145deg,#17313e,#0d1c28 78%);box-shadow:0 28px 90px rgba(0,0,0,.55)}.gymratik-install-art{display:grid;place-items:center;min-width:0;min-height:0}.gymratik-install-art img{display:block;width:min(100%,390px);height:min(62dvh,460px);object-fit:contain;filter:drop-shadow(0 18px 28px rgba(0,0,0,.3))}.gymratik-install-content{display:grid;align-content:center;gap:12px;min-width:0;padding:16px 4px}.gymratik-install-kicker{margin:0;color:#73e6cf;font-size:14px;font-weight:950;letter-spacing:.16em;text-transform:uppercase}.gymratik-install-content h2{margin:0;color:#f5f8f7;font-size:clamp(36px,5vw,52px);font-weight:950;line-height:1.02;letter-spacing:-.045em}.gymratik-install-description{margin:4px 0 0;color:#e5eef1;font-size:21px;font-weight:650;line-height:1.4}.gymratik-install-help{margin:0;color:#b8c9d2;font-size:17px;line-height:1.5}.gymratik-install-action{min-height:56px;margin-top:8px;padding:13px 20px;border:0;border-radius:15px;background:linear-gradient(120deg,#73e6cf,#37c7ad);color:#09231e;font:inherit;font-size:19px;font-weight:950;cursor:pointer}.gymratik-install-action:hover{filter:brightness(1.08)}.gymratik-install-dismiss{position:absolute;z-index:1;top:13px;right:13px;display:grid;place-items:center;width:46px;height:46px;border:1px solid rgba(225,241,245,.22);border-radius:50%;background:rgba(8,20,29,.7);color:#f5f8f7;font:32px/1 system-ui,sans-serif;cursor:pointer}.gymratik-install-dismiss:hover{background:rgba(255,255,255,.12)}@media(max-width:640px){#gymratikInstallInvite{padding:12px}.gymratik-install-card{grid-template-columns:1fr;gap:2px;width:min(520px,calc(100vw - 24px));min-height:0;max-height:calc(100dvh - 24px);padding:18px 22px 24px;border-radius:26px;text-align:center}.gymratik-install-art img{width:min(62vw,240px);height:min(29dvh,240px)}.gymratik-install-content{gap:10px;padding:4px 2px}.gymratik-install-kicker{font-size:12px}.gymratik-install-content h2{font-size:clamp(31px,8vw,40px)}.gymratik-install-description{font-size:18px}.gymratik-install-help{font-size:15px}.gymratik-install-action{width:100%;min-height:54px;font-size:18px}.gymratik-install-dismiss{top:8px;right:8px;width:40px;height:40px;font-size:28px}}@media(max-height:660px) and (max-width:640px){.gymratik-install-card{grid-template-columns:minmax(110px,.72fr) minmax(0,1.28fr);gap:10px;text-align:left;padding:16px}.gymratik-install-art img{width:100%;height:min(65dvh,370px)}.gymratik-install-content h2{font-size:clamp(27px,6vw,38px)}.gymratik-install-description{font-size:16px}.gymratik-install-help{font-size:14px}}';
    document.head.append(style);
    document.body.append(invite);
    invite.querySelector('.gymratik-install-dismiss').addEventListener('click', () => {
      try { window.sessionStorage.setItem(DISMISS_KEY, 'true'); } catch (_) {}
      invite.close();
    });
    invite.addEventListener('cancel', (event) => {
      event.preventDefault();
      try { window.sessionStorage.setItem(DISMISS_KEY, 'true'); } catch (_) {}
      invite.close();
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
    if (invite) {
      const shouldShow = !installed && !isDismissed();
      if (shouldShow && !invite.open) invite.showModal();
      else if (!shouldShow && invite.open) invite.close();
    }
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
