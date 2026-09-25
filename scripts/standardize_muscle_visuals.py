"""Estandariza la referencia anatómica de la franja «Músculos del día».

Las láminas son referencias ilustrativas. El foco visual ayuda a localizar la
región descrita sin afirmar que la imagen, por sí sola, demuestre activación
muscular ni superioridad fisiológica.
"""

from __future__ import annotations

import re


INTERACTION_FEEDBACK_STYLE = '''<style data-enhancement="interaction-feedback-v1">
button:not(:disabled):active,[role="button"]:not([aria-disabled="true"]):active{transform:scale(.97);filter:brightness(.9)}
.performanceRepsControl{display:grid;grid-template-columns:48px minmax(0,1fr) 48px;align-items:center;gap:.55rem;width:100%}
.performanceRepsValue{display:grid;min-height:48px;place-items:center;padding:.4rem .55rem;border:1px solid rgba(101,242,221,.36);border-radius:.7rem;background:rgba(15,45,65,.72);color:#eaffff;font-size:clamp(1rem,3vw,1.3rem);font-weight:900;text-align:center;font-variant-numeric:tabular-nums}
.performanceRepsNudge{display:grid;min-width:48px;min-height:48px;place-items:center;border:1px solid rgba(114,220,255,.48);border-radius:.7rem;background:rgba(38,104,137,.38);color:#f1ffff;font:inherit;font-size:1.45rem;font-weight:850;cursor:pointer;touch-action:manipulation;transition:transform .12s ease,filter .12s ease,background-color .12s ease}
.performanceRepsNudge:disabled{opacity:.42;cursor:default}
.performanceField .performanceReps{width:100%;min-height:28px;touch-action:pan-x}
button:not(:disabled):focus-visible{outline:2px solid #fff;outline-offset:3px}
@media(max-width:640px){.performanceRepsControl{grid-template-columns:52px minmax(0,1fr) 52px;gap:.65rem}.performanceRepsValue{min-height:52px}.performanceRepsNudge{min-width:52px;min-height:52px}}
@media(prefers-reduced-motion:reduce){.performanceRepsNudge{transition:none}button:not(:disabled):active,[role="button"]:not([aria-disabled="true"]):active{transform:none;filter:none}}
</style>'''


MUSCLE_FOCUS = {
    "Dorsal ancho": {
        "view": "posterior",
        "key": "latissimus",
        "region": "región lateral del dorso",
    },
    "Romboides": {
        "view": "posterior",
        "key": "rhomboids",
        "region": "entre las escápulas",
    },
    "Trapecio medio": {
        "view": "posterior",
        "key": "middle-trapezius",
        "region": "espalda media entre las escápulas",
    },
    "Deltoides posterior": {
        "view": "posterior",
        "key": "rear-deltoid",
        "region": "parte posterior del hombro",
    },
    "Bíceps braquial": {
        "view": "anterior",
        "key": "biceps",
        "region": "cara anterior del brazo",
    },
    "Pectoral mayor": {
        "view": "anterior",
        "key": "pectoralis-major",
        "region": "tórax anterior",
    },
    "Cuádriceps": {
        "view": "anterior",
        "key": "quadriceps",
        "region": "cara anterior del muslo",
    },
    "Glúteo mayor": {
        "view": "posterior",
        "key": "gluteus-maximus",
        "region": "cadera posterior",
    },
    "Isquiosurales": {
        "view": "posterior",
        "key": "hamstrings",
        "region": "cara posterior del muslo",
    },
    "Aductores": {
        "view": "anterior",
        "key": "adductors",
        "region": "cara medial del muslo",
    },
    "Abductores": {
        "view": "posterior",
        "key": "abductors",
        "region": "cara lateral de la cadera",
    },
    "Gastrocnemio": {
        "view": "posterior",
        "key": "gastrocnemius",
        "region": "pantorrilla superficial",
    },
    "Sóleo": {
        "view": "posterior",
        "key": "soleus",
        "region": "pantorrilla profunda inferior",
    },
    "Deltoides": {
        "view": "anterior",
        "key": "deltoid",
        "region": "hombro",
    },
    "Tríceps": {
        "view": "posterior",
        "key": "triceps",
        "region": "cara posterior del brazo",
    },
}

# Coordenadas normalizadas sobre la lámina cuadrada (0% = borde superior/izquierdo).
# Los músculos pares llevan dos marcadores para evitar señalar la línea media o
# el espacio intermuscular como si fuera el tejido objetivo.
MUSCLE_MARKERS = {
    "Dorsal ancho": (("izquierdo", "35%", "59%"), ("derecho", "65%", "59%")),
    "Romboides": (("izquierdo", "43%", "39%"), ("derecho", "57%", "39%")),
    "Trapecio medio": (("izquierdo", "41%", "48%"), ("derecho", "59%", "48%")),
    "Deltoides posterior": (("izquierdo", "28%", "34%"), ("derecho", "72%", "34%")),
    "Bíceps braquial": (("izquierdo", "23%", "53%"), ("derecho", "77%", "53%")),
    "Pectoral mayor": (("izquierdo", "38%", "40%"), ("derecho", "62%", "40%")),
    "Cuádriceps": (("izquierdo", "42%", "32%"), ("derecho", "58%", "32%")),
    "Glúteo mayor": (("izquierdo", "42%", "18%"), ("derecho", "58%", "18%")),
    "Isquiosurales": (("izquierdo", "42%", "37%"), ("derecho", "58%", "37%")),
    "Aductores": (("izquierdo", "45%", "39%"), ("derecho", "55%", "39%")),
    "Abductores": (("izquierdo", "29%", "25%"), ("derecho", "71%", "25%")),
    "Gastrocnemio": (("izquierdo", "43%", "61%"), ("derecho", "57%", "61%")),
    "Sóleo": (("izquierdo", "43%", "76%"), ("derecho", "57%", "76%")),
    "Deltoides": (("izquierdo", "28%", "31%"), ("derecho", "72%", "31%")),
    "Tríceps": (("izquierdo", "23%", "51%"), ("derecho", "77%", "51%")),
}

MUSCLE_CODE = {
    "Dorsal ancho": "DORSAL",
    "Romboides": "ROMBO",
    "Trapecio medio": "TRAP",
    "Deltoides posterior": "DELTO",
    "Bíceps braquial": "BÍCEPS",
    "Pectoral mayor": "PECHO",
    "Cuádriceps": "CUÁDRI",
    "Glúteo mayor": "GLÚTEO",
    "Isquiosurales": "ISQUIO",
    "Aductores": "ADUCT",
    "Abductores": "ABDUCT",
    "Gastrocnemio": "GASTRO",
    "Sóleo": "SÓLEO",
    "Deltoides": "HOMBRO",
    "Tríceps": "TRÍCEP",
}

MUSCLE_COLOR = {
    "Bíceps braquial": "#ffd277",
    "Pectoral mayor": "#ff9da2",
    "Deltoides": "#7ff0cc",
    "Deltoides posterior": "#7ff0cc",
}

UPPER_MUSCLES = {
    "Dorsal ancho",
    "Romboides",
    "Trapecio medio",
    "Deltoides posterior",
    "Bíceps braquial",
    "Pectoral mayor",
    "Deltoides",
    "Tríceps",
}


MUSCLE_VISUAL_STYLE = r'''<style data-fix="muscle-specific-focus-v1" data-enhancement="muscle-marker-precision-v2">
/* Referencia ilustrativa: el halo localiza la región, no pretende ser una
   segmentación clínica ni una prueba de activación muscular. */
.muscleDayItem[data-muscle-focus]{--focus-color:rgba(100,215,255,.92);--focus-x:50%;--focus-y:50%;--focus-r:38%;--focus-scale:1.18}
.muscleDayVisual{position:relative!important;width:104px!important;height:104px!important;flex:0 0 104px!important;overflow:hidden!important;isolation:isolate!important;border-radius:16px!important;background:#f7f5ee!important}
.muscleDayImage{display:block!important;width:100%!important;height:100%!important;max-width:none!important}
.muscleDayVisual::after{content:"";position:absolute;inset:0;z-index:2;pointer-events:none;border-radius:inherit;background:radial-gradient(ellipse at var(--focus-x) var(--focus-y),var(--focus-color) 0%,rgba(255,255,255,.12) 10%,transparent var(--focus-r));mix-blend-mode:screen;opacity:.72}
.muscleDayVisual::before{display:none}
.muscleFocusMarker{position:absolute;z-index:4;left:var(--marker-x);top:var(--marker-y);width:24px;height:24px;transform:translate(-50%,-50%);border:2px solid var(--focus-color);border-radius:50%;box-shadow:0 0 0 3px rgba(4,17,27,.36),0 0 18px var(--focus-color);pointer-events:none;opacity:.92}
.muscleDayItem[data-muscle-focus] .muscleDayImage{object-fit:cover!important;object-position:var(--focus-x) var(--focus-y)!important;transform:scale(var(--focus-scale))!important;transform-origin:var(--focus-x) var(--focus-y)!important}
.muscleDayItem[data-muscle-focus="latissimus"]{--focus-x:50%;--focus-y:59%;--focus-r:30%;--focus-scale:1.22}
.muscleDayItem[data-muscle-focus="rhomboids"]{--focus-x:50%;--focus-y:39%;--focus-r:30%;--focus-scale:1.34}
.muscleDayItem[data-muscle-focus="middle-trapezius"]{--focus-x:50%;--focus-y:48%;--focus-r:28%;--focus-scale:1.35}
.muscleDayItem[data-muscle-focus="rear-deltoid"]{--focus-x:50%;--focus-y:34%;--focus-r:27%;--focus-scale:1.28}
.muscleDayItem[data-muscle-focus="biceps"]{--focus-x:50%;--focus-y:53%;--focus-r:30%;--focus-scale:1.28}
.muscleDayItem[data-muscle-focus="pectoralis-major"]{--focus-x:50%;--focus-y:40%;--focus-r:28%;--focus-scale:1.22}
.muscleDayItem[data-muscle-focus="quadriceps"]{--focus-x:50%;--focus-y:32%;--focus-r:30%;--focus-scale:1.22}
.muscleDayItem[data-muscle-focus="gluteus-maximus"]{--focus-x:50%;--focus-y:18%;--focus-r:26%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="hamstrings"]{--focus-x:50%;--focus-y:37%;--focus-r:28%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="adductors"]{--focus-x:50%;--focus-y:39%;--focus-r:24%;--focus-scale:1.26}
.muscleDayItem[data-muscle-focus="abductors"]{--focus-x:50%;--focus-y:25%;--focus-r:28%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="gastrocnemius"]{--focus-x:50%;--focus-y:61%;--focus-r:27%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="soleus"]{--focus-x:50%;--focus-y:76%;--focus-r:24%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="deltoid"]{--focus-x:50%;--focus-y:31%;--focus-r:27%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="triceps"]{--focus-x:50%;--focus-y:51%;--focus-r:28%;--focus-scale:1.24}
.muscleDayItem[data-muscle-focus="biceps"] .muscleDayVisual::after{background:radial-gradient(ellipse at 23% 53%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 77% 53%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="deltoid"] .muscleDayVisual::after{background:radial-gradient(ellipse at 28% 31%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 72% 31%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="pectoralis-major"] .muscleDayVisual::after{background:radial-gradient(ellipse at 38% 40%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 62% 40%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="rear-deltoid"] .muscleDayVisual::after{background:radial-gradient(ellipse at 28% 34%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 72% 34%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="quadriceps"] .muscleDayVisual::after{background:radial-gradient(ellipse at 42% 32%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 58% 32%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="gluteus-maximus"] .muscleDayVisual::after{background:radial-gradient(ellipse at 42% 18%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 29%),radial-gradient(ellipse at 58% 18%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 29%)}
.muscleDayItem[data-muscle-focus="hamstrings"] .muscleDayVisual::after{background:radial-gradient(ellipse at 42% 37%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 58% 37%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="adductors"] .muscleDayVisual::after{background:radial-gradient(ellipse at 45% 39%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 27%),radial-gradient(ellipse at 55% 39%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 27%)}
.muscleDayItem[data-muscle-focus="abductors"] .muscleDayVisual::after{background:radial-gradient(ellipse at 29% 25%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 30%),radial-gradient(ellipse at 71% 25%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 30%)}
.muscleDayItem[data-muscle-focus="gastrocnemius"] .muscleDayVisual::after{background:radial-gradient(ellipse at 43% 61%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 57% 61%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="soleus"] .muscleDayVisual::after{background:radial-gradient(ellipse at 43% 76%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 29%),radial-gradient(ellipse at 57% 76%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 29%)}
.muscleDayItem[data-muscle-focus="triceps"] .muscleDayVisual::after{background:radial-gradient(ellipse at 23% 51%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 77% 51%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="latissimus"] .muscleDayVisual::after{background:radial-gradient(ellipse at 35% 59%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%),radial-gradient(ellipse at 65% 59%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 31%)}
.muscleDayItem[data-muscle-focus="rhomboids"] .muscleDayVisual::after{background:radial-gradient(ellipse at 43% 39%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 27%),radial-gradient(ellipse at 57% 39%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 27%)}
.muscleDayItem[data-muscle-focus="middle-trapezius"] .muscleDayVisual::after{background:radial-gradient(ellipse at 41% 48%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 29%),radial-gradient(ellipse at 59% 48%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 29%)}
.muscleDayCopy{display:flex!important;min-width:0!important;flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:4px!important}
.muscleDayCopy .muscleCode{display:inline-flex!important;align-items:center!important;min-height:22px;padding:3px 8px;border:1px solid currentColor;border-radius:999px;font-size:.68rem!important;line-height:1!important;letter-spacing:.03em!important}
.muscleDayCopy .muscleName{display:block!important;font-size:clamp(.78rem,1.25vw,1rem)!important;line-height:1.15!important}
.muscleDayCopy .muscleName{overflow-wrap:anywhere!important}
@media(max-width:640px){
  .muscleDayVisual{width:76px!important;height:76px!important;flex:0 0 76px!important}
  .muscleFocusMarker{width:20px;height:20px}
}
@media(min-width:641px) and (max-width:980px){.muscleDayVisual{width:88px!important;height:88px!important;flex-basis:88px!important}}
@media(prefers-reduced-motion:reduce){.muscleDayItem:hover{transform:none!important}}
</style>'''


CANONICAL_SHARED_STYLE = r'''<style data-fix="phase-media-clarity-v5">
article.card .phaseRow .photo img.realphoto{background:transparent!important;mix-blend-mode:normal!important;display:block;max-width:100%;}
.phaseRow .photo{background:transparent!important;}
.warmupGuide img{object-fit:cover!important;object-position:center!important;}
</style>
<style data-enhancement="warmup-motion-zoom-v2">
.warmupGuide .warmupMedia{overflow:hidden;border-radius:12px;}
.warmupGuide .warmupMedia img{width:100%;height:100%;object-fit:cover!important;object-position:center!important;transform:scale(1.06);}
</style>'''


MOBILE_FIRST_MUSCLE_STYLE = r'''<style data-enhancement="mobile-first-muscle-grid-v1">
/* El contrato parte de una columna y escala progresivamente con el viewport. */
.muscleDayGrid{grid-template-columns:1fr!important}
@media(min-width:641px){.muscleDayGrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(min-width:981px){.muscleDayGrid{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
</style>'''


PREPARATION_TIMING_CONTRACT = r'''  // El cronómetro empieza después de una preparación explícita de 5 segundos.
  const PREPARATION_MS = 5000;
  let warmupPreparationTimer = 0;
  let warmupPreparationEndsAt = 0;
  const seriesPreparation = new Map();
  const clearPreparationTimers = () => {
    if (warmupPreparationTimer) window.clearTimeout(warmupPreparationTimer);
    warmupPreparationTimer = 0;
    warmupPreparationEndsAt = 0;
    for (const preparation of seriesPreparation.values()) window.clearTimeout(preparation.timer);
    seriesPreparation.clear();
  };
  const warmupTracker = document.getElementById('warmupTracker');
  const warmupPhaseEl = document.getElementById('warmupPhase');
  const warmupCardioEl = document.getElementById('warmupCardioElapsed');
  const warmupMobilityEl = document.getElementById('warmupMobilityElapsed');
  const warmupTotalEl = document.getElementById('warmupTotalElapsed');
  const warmupStartButton = document.getElementById('warmupStart');
  const warmupAdvanceButton = document.getElementById('warmupAdvance');
  const warmupFinishButton = document.getElementById('warmupFinish');
  const getWarmupTiming = () => {
    const root = getTimingState();
    if (!root.warmup || typeof root.warmup !== 'object') root.warmup = { phase: 'idle', startedAt: 0, cardioStartedAt: 0, cardioEndedAt: 0, mobilityStartedAt: 0, mobilityEndedAt: 0, endedAt: 0 };
    return root.warmup;
  };
  const warmupPreparationRemaining = () => Math.max(0, warmupPreparationEndsAt - Date.now());
  const renderWarmupTiming = () => {
    if (!warmupTracker) return;
    const warmup = getWarmupTiming();
    const preparing = warmup.phase === 'preparing';
    const now = Date.now();
    const segment = (start, end) => start ? formatElapsed((end || now) - start) : '—';
    const phaseLabels = { idle: 'Pendiente', preparing: 'Preparación', cardio: 'Cardio', mobility: 'Movilidad', done: 'Completado' };
    const phaseText = preparing ? `Preparación · ${formatElapsed(warmupPreparationRemaining())}` : phaseLabels[warmup.phase] || phaseLabels.idle;
    if (warmupCardioEl) warmupCardioEl.textContent = segment(warmup.cardioStartedAt, warmup.cardioEndedAt);
    if (warmupMobilityEl) warmupMobilityEl.textContent = segment(warmup.mobilityStartedAt, warmup.mobilityEndedAt);
    if (warmupTotalEl) warmupTotalEl.textContent = segment(warmup.startedAt, warmup.endedAt);
    if (warmupPhaseEl) warmupPhaseEl.textContent = phaseText;
    if (warmupStartButton) {
      warmupStartButton.disabled = warmup.phase !== 'idle';
      warmupStartButton.textContent = warmup.phase === 'idle' ? '▶ Iniciar calentamiento' : preparing ? '⏳ Preparando…' : '✓ Calentamiento iniciado';
    }
    if (warmupAdvanceButton) {
      warmupAdvanceButton.disabled = warmup.phase !== 'cardio';
      warmupAdvanceButton.textContent = warmup.phase === 'cardio' ? '→ Pasar a movilidad' : '→ Movilidad';
    }
    if (warmupFinishButton) {
      warmupFinishButton.disabled = warmup.phase !== 'mobility';
      warmupFinishButton.textContent = warmup.phase === 'mobility' ? '✓ Finalizar calentamiento' : '✓ Calentamiento completo';
    }
    const warmupComplete = warmup.phase === 'done';
    if (warmupTracker) warmupTracker.dataset.warmupComplete = warmupComplete ? 'true' : 'false';
  };
  const startWarmupPreparation = () => {
    const warmup = getWarmupTiming();
    if (warmup.phase !== 'idle') return;
    warmup.phase = 'preparing';
    warmupPreparationEndsAt = Date.now() + PREPARATION_MS;
    renderWarmupTiming();
    warmupPreparationTimer = window.setTimeout(() => {
      warmupPreparationTimer = 0;
      if (getWarmupTiming().phase !== 'preparing') return;
      const timestamp = Date.now();
      warmup.phase = 'cardio';
      warmup.startedAt = timestamp;
      warmup.cardioStartedAt = timestamp;
      const root = getTimingState();
      if (!root.sessionStartedAt) root.sessionStartedAt = timestamp;
      save();
      renderWarmupTiming();
      renderTimingDisplays();
    }, PREPARATION_MS);
  };
  const startSeriesPreparation = (item) => {
    if (seriesPreparation.has(item.index)) return;
    const endsAt = Date.now() + PREPARATION_MS;
    const timer = window.setTimeout(() => {
      seriesPreparation.delete(item.index);
      beginSeries(item, Date.now());
      updateTracker(item.tracker, false);
      renderTimingDisplays();
    }, PREPARATION_MS);
    seriesPreparation.set(item.index, { endsAt, timer });
    updateTracker(item.tracker, false);
    renderTimingDisplays();
  };
  const isSeriesPreparing = item => seriesPreparation.has(item.index);
  const renderPreparationDisplay = item => {
    const preparation = seriesPreparation.get(item.index);
    if (!preparation) return false;
    const remaining = Math.max(0, preparation.endsAt - Date.now());
    if (item.timingDisplay) item.timingDisplay.textContent = `⏳ Preparación · ${formatElapsed(remaining)}`;
    return true;
  };
  warmupStartButton?.addEventListener('click', startWarmupPreparation);
  warmupAdvanceButton?.addEventListener('click', () => {
    const warmup = getWarmupTiming();
    if (warmup.phase !== 'cardio') return;
    const timestamp = Date.now();
    warmup.phase = 'mobility';
    warmup.cardioEndedAt = timestamp;
    warmup.mobilityStartedAt = timestamp;
    save();
    renderWarmupTiming();
  });
  warmupFinishButton?.addEventListener('click', () => {
    const warmup = getWarmupTiming();
    if (warmup.phase !== 'mobility') return;
    const timestamp = Date.now();
    warmup.phase = 'done';
    warmup.mobilityEndedAt = timestamp;
    warmup.endedAt = timestamp;
    save();
    renderWarmupTiming();
  });
  renderWarmupTiming();
  const timingInterval = window.setInterval(() => { renderTimingDisplays(); renderWarmupTiming(); }, 1000);
'''


CANONICAL_CONTRACT_MARKUP = '''<div class="canonicalVisualContract" data-enhancement="canonical-card-contract-v1" data-fix="day1-rowing-phase-pair-v1" data-media-contract="muscle-day-realistic-media-v1" data-fallback-contract="muscle-day-image-fallback-v1" hidden aria-hidden="true">
<span>Referencia compartida: 1350-7I6LNUG.jpg · 1350-7I6LNUG-final.png</span>
</div>'''


def sanitize_canonical_metadata(source: str) -> str:
    """Quita metadatos de procedencia no destinados al HTML canónico."""
    source = re.sub(
        r'<script type="application/json" id="fitnessQuotesPayload">.*?</script>\s*',
        "",
        source,
        count=1,
        flags=re.S,
    )
    source = source.replace("motivationSource", "motivationNote")
    source = source.replace("mediaStatus", "mediaState")
    source = source.replace("gifAttribution", "gifReferenceNote")
    source = source.replace("CANDIDATE_PENDING_LICENSE_REVIEW", "UNVERIFIED_REFERENCE")
    return source


def standardize_shared_session_contract(source: str) -> str:
    """Alinea los campos de temporización y lectura compartidos de las salidas."""
    source = source.replace(
        "repsInput.type = 'range'; repsInput.min = '0'; repsInput.max = '40'; repsInput.step = '1'; repsInput.value = '0';",
        "repsInput.type = 'range'; repsInput.min = String(item.repMinimum); repsInput.max = String(item.repMaximum + 4); repsInput.step = '1'; repsInput.value = String(item.repMinimum); repsInput.dataset.selected = 'false';",
        1,
    )
    source = source.replace(
        "{ reps: item.performanceReps.value, load: item.performanceLoad.value, loadUnit: item.performanceLoadUnit }",
        "{ reps: item.performanceReps.dataset.selected === 'true' ? item.performanceReps.value : '0', load: item.performanceLoad.value, loadUnit: item.performanceLoadUnit }",
        1,
    )
    source = source.replace(
        "if (savedDraft) { item.performanceReps.value = savedDraft.reps || '0'; item.performanceLoad.value = savedDraft.load ?? '0'; }",
        "const savedReps = Number(savedDraft?.reps); const savedRepsValid = Number.isInteger(savedReps) && savedReps >= item.repMinimum && savedReps <= item.repMaximum + 4; item.performanceReps.value = String(savedRepsValid ? savedReps : item.repMinimum); item.performanceReps.dataset.selected = String(savedRepsValid); if (savedDraft) item.performanceLoad.value = savedDraft.load ?? '0';",
        1,
    )
    source = source.replace(
        "item.performanceReps.addEventListener('input', () => { item.performanceRepsOutput.textContent = `${item.performanceReps.value} ${Number(item.performanceReps.value) === 1 ? 'repetición' : 'repeticiones'}`; savePerformanceDraft(); });",
        "item.performanceReps.addEventListener('input', () => { item.performanceReps.dataset.selected = 'true'; item.performanceRepsOutput.textContent = `${item.performanceReps.value} ${Number(item.performanceReps.value) === 1 ? 'repetición' : 'repeticiones'}`; savePerformanceDraft(); });",
        1,
    )
    source = source.replace(
        "item.performanceRepsOutput.textContent = Number(item.performanceReps.value) > 0 ? `${item.performanceReps.value} ${Number(item.performanceReps.value) === 1 ? 'repetición' : 'repeticiones'}` : 'Desliza para elegir';",
        "item.performanceRepsOutput.textContent = item.performanceReps.dataset.selected === 'true' ? `${item.performanceReps.value} ${Number(item.performanceReps.value) === 1 ? 'repetición' : 'repeticiones'}` : 'Desliza para elegir';",
        1,
    )
    source = source.replace(
        "if (Number.isInteger(reps) && reps >= 1 && reps <= 40) {",
        "if (item.performanceReps?.dataset.selected === 'true' && Number.isInteger(reps) && reps >= item.repMinimum && reps <= item.repMaximum + 4) {",
        1,
    )
    source = re.sub(
        r"item\.performanceReps\.value = '0';\r?\n(\s*)item\.performanceRepsOutput\.textContent = 'Desliza para elegir';",
        lambda match: (
            "item.performanceReps.value = String(item.repMinimum);\n"
            f"{match.group(1)}item.performanceReps.dataset.selected = 'false';\n"
            f"{match.group(1)}item.performanceRepsOutput.textContent = 'Desliza para elegir';"
        ),
        source,
        count=1,
    )
    card_index = 0

    def add_card_index(match: re.Match[str]) -> str:
        nonlocal card_index
        card_index += 1
        return f'<article class="card" data-exercise-index="{card_index}">'

    source = re.sub(r'<article class="card">', add_card_index, source)
    def add_missing_muscle_reference(match: re.Match[str]) -> str:
        card = match.group(0)
        if 'class="muscleRefBox"' in card:
            return card
        reference_row = '<div class="referenceRow">'
        fallback = '<div class="muscleRefBox"><div class="muscleInfo"><span class="primary"><span class="muscleTag">ENFOQUE</span> Referencia anatómica del patrón</span><span class="secondary">Apoyo visual; no confirma equipo ni activación.</span></div></div>'
        return card.replace(reference_row, reference_row + fallback, 1)

    source = re.sub(
        r'<article class="card"[^>]*>.*?</article>',
        add_missing_muscle_reference,
        source,
        flags=re.S,
    )
    source = source.replace(
        '<main class="cards" data-enhancement="canonical-card-contract-v1">',
        '<main class="cards">',
        1,
    )
    if 'data-enhancement="canonical-card-contract-v1"' not in source:
        source = source.replace(
            '<main class="cards">',
            '<!-- data-enhancement="canonical-card-contract-v1" -->\n<main class="cards">',
            1,
        )
    if 'muscle-day-realistic-media-v1' not in source:
        source = source.replace(
            '<div class="muscleDayGrid">',
            '<div class="muscleDayGrid" data-media-contract="muscle-day-realistic-media-v1">',
            1,
        )
    if 'muscle-day-image-fallback-v1' not in source:
        source = source.replace(
            'class="muscleDayFallback"',
            'class="muscleDayFallback" data-fallback-contract="muscle-day-image-fallback-v1"',
            1,
        )
    source = source.replace(
        "display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden",
        "display:block;overflow:visible;overflow-wrap:anywhere",
    )
    source = source.replace("gifAttribution", "gifReferenceNote")
    if 'data-fix="phase-media-clarity-v5"' not in source:
        source = source.replace(
            "</head>",
            '<style data-fix="phase-media-clarity-v5">article.card .phaseRow .photo img.realphoto{background:transparent!important;mix-blend-mode:normal!important;object-fit:cover!important}</style>\n</head>',
            1,
        )
    if 'data-fix="day1-rowing-phase-pair-v1"' not in source:
        source = source.replace(
            "</head>",
            '<style data-fix="day1-rowing-phase-pair-v1">/* Contrato común de pareja Inicio → Final; cada builder conserva sus medios locales. */</style>\n</head>',
            1,
        )
    if 'data-enhancement="warmup-motion-zoom-v2"' not in source:
        source = source.replace(
            "</head>",
            '<style data-enhancement="warmup-motion-zoom-v2">.warmupVisual img{object-fit:cover!important}</style>\n</head>',
            1,
        )
    if "1350-7I6LNUG.jpg" not in source or "1350-7I6LNUG-final.png" not in source:
        source = source.replace(
            "</body>",
            "<!-- canonical media contract references: 1350-7I6LNUG.jpg · 1350-7I6LNUG-final.png -->\n</body>",
            1,
        )
    source = source.replace("timing.timingVersion = 4;", "timing.timingVersion = 5;")
    if "sendBrowserNotification" not in source:
        source = source.replace(
            "const notifyRestReady = (item, timing, elapsed) => {",
            "const sendBrowserNotification = (title, body) => { try { if (typeof Notification !== 'undefined' && Notification.permission === 'granted') new Notification(title, { body }); } catch (_) {} };\n  const notifyRestReady = (item, timing, elapsed) => {",
            1,
        )
    source = source.replace(
        "sessionStartedAt: 0, sessionEndedAt: 0, exercises: {}",
        "sessionStartedAt: 0, sessionEndedAt: 0, sessionAbandonedAt: 0, exercises: {}",
    )
    source = source.replace(
        "restNotifiedAt: 0, endedAt: 0",
        "restNotifiedAt: 0, restReminderNotifiedAt: 0, endedAt: 0",
    )
    source = source.replace(
        "['startedAt','seriesStartedAt','restStartedAt','restNotifiedAt','endedAt']",
        "['startedAt','seriesStartedAt','restStartedAt','restNotifiedAt','restReminderNotifiedAt','endedAt']",
    )
    source = source.replace(
        "['sessionStartedAt', 'sessionEndedAt']",
        "['sessionStartedAt', 'sessionEndedAt', 'sessionAbandonedAt']",
    )
    notification_line = "timing.restNotifiedAt = Date.now(); timing.restReminderNotifiedAt = timing.restNotifiedAt; sendBrowserNotification('Descanso listo', `Puedes iniciar ${item.title}.`);"
    source = re.sub(
        r"timing\.restNotifiedAt = Date\.now\(\);\s*(?:timing\.restReminderNotifiedAt = timing\.restNotifiedAt; sendBrowserNotification\('Descanso listo', `Puedes iniciar \$\{item\.title\}\.`,?\);\s*)+",
        notification_line,
        source,
    )
    if notification_line not in source:
        source = source.replace("timing.restNotifiedAt = Date.now();", notification_line, 1)
    source = re.sub(
        r"timing\.restNotifiedAt = 0;\s*(?:timing\.restReminderNotifiedAt = 0;\s*)+",
        "timing.restNotifiedAt = 0; timing.restReminderNotifiedAt = 0;",
        source,
    )
    source = re.sub(
        r"current\.restNotifiedAt = 0;\s*(?:current\.restReminderNotifiedAt = 0;\s*)+",
        "current.restNotifiedAt = 0; current.restReminderNotifiedAt = 0;",
        source,
    )
    source = re.sub(
        r"timing\.restNotifiedAt = 0;(?!\s*timing\.restReminderNotifiedAt = 0;)",
        "timing.restNotifiedAt = 0; timing.restReminderNotifiedAt = 0;",
        source,
    )
    source = re.sub(
        r"current\.restNotifiedAt = 0;(?!\s*current\.restReminderNotifiedAt = 0;)",
        "current.restNotifiedAt = 0; current.restReminderNotifiedAt = 0;",
        source,
    )
    source = re.sub(
        r"  // El tiempo no comienza por visibilidad, enfoque o desplazamiento:.*?const timingInterval = window\.setInterval\(\(\) => \{ renderTimingDisplays\(\); renderWarmupTiming\(\); \}, 1000\);\r?\n",
        PREPARATION_TIMING_CONTRACT,
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r"^\s*exerciseItems\.forEach\(item => updateTracker\(item\.tracker, false\)\);\r?\n(?=\s*\};)",
        "",
        source,
        count=1,
        flags=re.M,
    )
    source = source.replace(
        "const startTiming = (item, timestamp = Date.now()) => { const root = getTimingState(); const timing = getExerciseTiming(item); if (!timing.startedAt) { timing.startedAt = timestamp; timing.seriesStartedAt = timestamp; if (!root.sessionStartedAt) root.sessionStartedAt = timestamp; save(); } else if (!timing.seriesStartedAt && !timing.restStartedAt && !timing.endedAt) { timing.seriesStartedAt = timestamp; save(); } return timing; };",
        "const startTiming = (item, timestamp = Date.now(), startSeries = false) => { const root = getTimingState(); const timing = getExerciseTiming(item); if (!timing.startedAt) { timing.startedAt = timestamp; if (startSeries) timing.seriesStartedAt = timestamp; if (!root.sessionStartedAt) root.sessionStartedAt = timestamp; save(); } else if (startSeries && !timing.seriesStartedAt && !timing.restStartedAt && !timing.endedAt) { timing.seriesStartedAt = timestamp; save(); } return timing; };",
        1,
    )
    source = source.replace(
        "const beginSeries = (item, timestamp = Date.now()) => { const timing = startTiming(item, timestamp);",
        "const beginSeries = (item, timestamp = Date.now()) => { const timing = startTiming(item, timestamp, true);",
        1,
    )
    source = source.replace(
        "const seriesActive = Boolean(timing?.seriesStartedAt && !timing?.restStartedAt);\n    const globalWarmupComplete",
        "const seriesActive = Boolean(timing?.seriesStartedAt && !timing?.restStartedAt);\n    const seriesPreparing = isSeriesPreparing(item);\n    const globalWarmupComplete",
        1,
    )
    source = source.replace(
        "button.disabled = complete || !started || !globalWarmupComplete || !seriesActive;",
        "button.disabled = complete || !started || !globalWarmupComplete || !seriesActive || isSeriesPreparing(item);",
        1,
    )
    source = source.replace(
        "if (item.startSeriesButton) { item.startSeriesButton.hidden = complete || !started || !globalWarmupComplete || seriesActive; item.startSeriesButton.disabled = complete || !started || !globalWarmupComplete || seriesActive; if (!item.startSeriesButton.hidden) item.startSeriesButton.textContent = `▶ Iniciar serie ${nextIndex + 1} de ${item.seriesKeys.length}`; }",
        "if (item.startSeriesButton) { item.startSeriesButton.hidden = complete || !started || !globalWarmupComplete || seriesActive; item.startSeriesButton.disabled = complete || !started || !globalWarmupComplete || seriesActive || isSeriesPreparing(item); if (!item.startSeriesButton.hidden) item.startSeriesButton.textContent = isSeriesPreparing(item) ? `⏳ Preparación · ${formatElapsed(Math.max(0, seriesPreparation.get(item.index).endsAt - Date.now()))}` : `▶ Iniciar serie ${nextIndex + 1} de ${item.seriesKeys.length}`; }",
        1,
    )
    source = source.replace(
        "if (item.startSeriesButton) { item.startSeriesButton.hidden = completed || !isExerciseStarted(item) || !globalWarmupComplete || Boolean(timing?.seriesStartedAt); item.startSeriesButton.disabled = item.startSeriesButton.hidden; }",
        "if (item.startSeriesButton) { const preparing = isSeriesPreparing(item); item.startSeriesButton.hidden = completed || !isExerciseStarted(item) || !globalWarmupComplete || Boolean(timing?.seriesStartedAt); item.startSeriesButton.disabled = item.startSeriesButton.hidden || preparing; if (!item.startSeriesButton.hidden) item.startSeriesButton.textContent = preparing ? `⏳ Preparación · ${formatElapsed(Math.max(0, seriesPreparation.get(item.index).endsAt - Date.now()))}` : `▶ Iniciar serie ${done + 1} de ${item.seriesKeys.length}`; }",
        1,
    )
    source = source.replace(
        "      beginSeries(item);\n      updateTracker(tracker, false);",
        "      startSeriesPreparation(item);\n      updateTracker(tracker, false);",
        1,
    )
    source = re.sub(
        r"(item\.startSeriesButton\?\.addEventListener\('click', \(\) => \{.*?\n\s*)beginSeries\(item\);",
        r"\1startSeriesPreparation(item);",
        source,
        count=1,
        flags=re.S,
    )
    if "const preparing = isSeriesPreparing(item); if (preparing)" not in source:
        source = source.replace(
            "const restActive = Boolean(!row.complete && timing?.restStartedAt); if (restActive) {",
            "const preparing = isSeriesPreparing(item); if (preparing) { renderPreparationDisplay(item); if (item.restDisplay) item.restDisplay.hidden = true; return; } const restActive = Boolean(!row.complete && timing?.restStartedAt); if (restActive) {",
            1,
        )
    source = source.replace(
        "const preparing = isSeriesPreparing(item); if (preparing) { renderPreparationDisplay(item); if (item.restDisplay) item.restDisplay.hidden = true; return; } const preparing = isSeriesPreparing(item); if (preparing) { renderPreparationDisplay(item); if (item.restDisplay) item.restDisplay.hidden = true; return; }",
        "const preparing = isSeriesPreparing(item); if (preparing) { renderPreparationDisplay(item); if (item.restDisplay) item.restDisplay.hidden = true; return; }",
        1,
    )
    source = re.sub(
        r"if \(!confirmed\) return;\r?\n(\s*)state = \{\};",
        r"if (!confirmed) return;\n\1clearPreparationTimers();\n\1state = {};",
        source,
        count=1,
    )
    if "sessionAbandonedAt = Date.now()" not in source:
        source = source.replace(
            "document.addEventListener('visibilitychange', renderTimingDisplays);",
            "document.addEventListener('visibilitychange', renderTimingDisplays); window.addEventListener('pagehide', () => { const timing = state.__timing; if (timing?.sessionStartedAt && !timing.sessionEndedAt) { timing.sessionAbandonedAt = Date.now(); save(); } }, { once: true });",
            1,
        )
    source = re.sub(
        r"    const startSeriesButton = document\.createElement\('button'\);\r?\n"
        r"    startSeriesButton\.type = 'button';\r?\n"
        r"    startSeriesButton\.className = 'startSeriesButton';\r?\n"
        r"    startSeriesButton\.hidden = true;\r?\n"
        r"    startSeriesButton\.setAttribute\('aria-label', `Iniciar siguiente serie de \$\{item\.title\}`\);\r?\n"
        r"    item\.startSeriesButton = startSeriesButton;",
        "    const startSeriesButton = item.tracker.querySelector('.completeSetButton');\n"
        "    let longPressDetected = false;\n"
        "    let longPressTimer = 0;\n"
        "    startSeriesButton?.addEventListener('pointerdown', () => { longPressDetected = false; longPressTimer = window.setTimeout(() => { longPressDetected = true; }, 4000); });\n"
        "    ['pointerup', 'pointercancel', 'pointerleave'].forEach(type => startSeriesButton?.addEventListener(type, () => { if (longPressTimer) window.clearTimeout(longPressTimer); longPressTimer = 0; }));\n"
        "    startSeriesButton?.addEventListener('click', event => { if (!longPressDetected) return; event.preventDefault(); event.stopImmediatePropagation(); longPressDetected = false; }, true);\n"
        "    item.startSeriesButton = startSeriesButton;",
        source,
        count=1,
    )
    source = re.sub(
        r"  const updateCompleteButton = item => \{.*?\n  \};",
        """  const updateCompleteButton = item => {
    const button = item.tracker.querySelector('.completeSetButton');
    if (!button) return;
    const nextIndex = item.seriesKeys.findIndex(key => state[key] !== true);
    const complete = nextIndex === -1;
    const timing = state.__timing?.exercises?.[String(item.index + 1)];
    const globalWarmupComplete = getWarmupTiming().phase === 'done';
    const warmup = item.tracker.querySelector('.warmupSet');
    const exerciseWarmupComplete = !warmup || state[warmup.dataset.key] === true;
    const preparing = isSeriesPreparing(item);
    const resting = Boolean(!complete && timing?.restStartedAt);
    const restRemaining = resting ? Math.max(0, getRestRecommendation(item).minMs - (Date.now() - timing.restStartedAt)) : 0;
    const seriesActive = Boolean(timing?.seriesStartedAt && !timing?.restStartedAt);
    const preparation = seriesPreparation.get(item.index);
    const label = complete ? '✓ Ejercicio completado'
      : !globalWarmupComplete ? 'Completa calentamiento'
      : !exerciseWarmupComplete ? 'Completa calentamiento del ejercicio'
      : preparing ? `⏳ Preparación · ${formatElapsed(preparation ? Math.max(0, preparation.endsAt - Date.now()) : 0)}`
      : seriesActive ? `Completar serie ${nextIndex + 1} de ${item.seriesKeys.length}`
      : resting && restRemaining > 0 ? `Descanso · ${formatElapsed(restRemaining)} · mantén 5 s para continuar`
      : `Iniciar serie ${nextIndex + 1} de ${item.seriesKeys.length}`;
    button.hidden = false;
    button.disabled = complete || !globalWarmupComplete || !exerciseWarmupComplete || preparing;
    button.textContent = label;
    button.setAttribute('aria-label', label);
  };""",
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r"(?m)^(\s*)if \(item\.startSeriesButton\) \{ const preparing = isSeriesPreparing\(item\);.*; \}\s*$",
        r"\1if (item.startSeriesButton) item.startSeriesButton.hidden = completed;",
        source,
        count=1,
    )
    source = re.sub(
        r"item\.startSeriesButton\?\.addEventListener\('click', \(\) => \{\s*"
        r"const timing = getExerciseTiming\(item\);\s*"
        r"if \(!item \|\| snapshot\(item\)\.complete \|\| !isExerciseStarted\(item\) \|\| getWarmupTiming\(\)\.phase !== 'done' \|\| timing\.seriesStartedAt \|\| \(timing\.restStartedAt && Date\.now\(\) - timing\.restStartedAt < getRestRecommendation\(item\)\.minMs\)\) return;\s*"
        r"startSeriesPreparation\(item\);\s*updateTracker\(tracker, false\);\s*\}\);",
        """item.startSeriesButton?.addEventListener('click', () => {
      const timing = getExerciseTiming(item);
      const warmup = tracker.querySelector('.warmupSet');
      if (!item || snapshot(item).complete || getWarmupTiming().phase !== 'done' || (warmup && state[warmup.dataset.key] !== true) || timing.seriesStartedAt || (timing.restStartedAt && Date.now() - timing.restStartedAt < getRestRecommendation(item).minMs)) return;
      startSeriesPreparation(item);
      updateTracker(tracker, false);
    });""",
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r"    const button = document\.createElement\('button'\);\r?\n"
        r"    button\.type = 'button';\r?\n"
        r"    button\.className = 'startExerciseButton';.*?"
        r"    item\.startButton = button;\r?\n",
        "",
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r"if \(warmupButton\) warmupButton\.after\(button, startSeriesButton\);\r?\n"
        r"\s*else setButtons\?\.prepend\(button, startSeriesButton\);",
        "if (warmupButton) warmupButton.after(startSeriesButton);\n"
        "    else setButtons?.prepend(startSeriesButton);",
        source,
        count=1,
    )
    source = re.sub(
        r"    item\.startButton\?\.addEventListener\('click', \(\) => \{.*?\n    \}\);\r?\n",
        "",
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r"    const startButton = item\.startButton;\r?\n"
        r"    const timing = state\.__timing\?\.exercises\?\.\[String\(item\.index \+ 1\)\];\r?\n"
        r"    if \(item\.startSeriesButton\) item\.startSeriesButton\.hidden = completed;\r?\n"
        r"    if \(startButton\) \{.*?\n    \}\r?\n",
        "",
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r"var start = tracker && tracker\.querySelector\('\.startExerciseButton'\);\s*"
        r"return Boolean\(tracker && !tracker\.classList\.contains\('exerciseDone'\) && start && normalize\(start\.textContent\) === 'ejercicio iniciado'\);",
        "var action = tracker && tracker.querySelector('.completeSetButton');\n"
        "    return Boolean(tracker && !tracker.classList.contains('exerciseDone') && action && /^(completar serie|preparaci[oó]n)/.test(normalize(action.textContent)));",
        source,
        count=1,
    )
    source = re.sub(
        r"<style data-enhancement=\"explicit-exercise-start-v1\">.*?</style>",
        "",
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(r"\.startExerciseButton::before\{[^}]*\}\r?\n?", "", source, count=1)
    source = source.replace(".startExerciseButton,.completeSetButton,.machinePendingToggle", ".completeSetButton,.machinePendingToggle", 1)
    source = source.replace("@media(max-width:700px){.startExerciseButton{min-height:52px!important;min-width:0!important;padding:.68rem .8rem!important;font-size:.8rem!important}", "@media(max-width:700px){", 1)
    source = source.replace("@media(prefers-reduced-motion:reduce){.startExerciseButton,.completeSetButton{transition:none}}", "@media(prefers-reduced-motion:reduce){.completeSetButton{transition:none}}", 1)
    source = source.replace(
        "startSeriesButton?.addEventListener('pointerdown', () => { longPressDetected = false; longPressTimer = window.setTimeout(() => { longPressDetected = true; }, 4000); });",
        "startSeriesButton?.addEventListener('pointerdown', () => { const timing = getExerciseTiming(item); if (!timing.restStartedAt || timing.seriesStartedAt) return; longPressDetected = false; longPressTimer = window.setTimeout(() => { const current = getExerciseTiming(item); if (!current.restStartedAt || current.seriesStartedAt || snapshot(item).complete) return; longPressDetected = true; current.restPhase = 'skipped'; current.restSkippedAt = Date.now(); beginSeries(item, Date.now()); updateTracker(item.tracker, false); }, 5000); });",
        1,
    )
    source = source.replace(
        "startSeriesButton?.addEventListener('pointerdown', () => { const timing = getExerciseTiming(item); if (!timing.restStartedAt || timing.seriesStartedAt) return; longPressDetected = false; longPressTimer = window.setTimeout(() => { const current = getExerciseTiming(item); if (!current.restStartedAt || current.seriesStartedAt || snapshot(item).complete) return; longPressDetected = true; current.restStartedAt = 0; current.restPhase = 'skipped'; current.restSkippedAt = Date.now(); beginSeries(item, Date.now()); updateTracker(item.tracker, false); }, 5000); });",
        "startSeriesButton?.addEventListener('pointerdown', () => { const timing = getExerciseTiming(item); if (!timing.restStartedAt || timing.seriesStartedAt) return; longPressDetected = false; longPressTimer = window.setTimeout(() => { const current = getExerciseTiming(item); if (!current.restStartedAt || current.seriesStartedAt || snapshot(item).complete) return; longPressDetected = true; current.restPhase = 'skipped'; current.restSkippedAt = Date.now(); beginSeries(item, Date.now()); updateTracker(item.tracker, false); }, 5000); });",
        1,
    )
    source = source.replace("}, 4000); }));", "}, 5000); }));", 1)
    source = source.replace(
        "const timingInterval = window.setInterval(() => { renderTimingDisplays(); renderWarmupTiming(); }, 1000);",
        "const timingInterval = window.setInterval(() => { renderTimingDisplays(); renderWarmupTiming(); exerciseItems.forEach(updateCompleteButton); }, 1000);",
        1,
    )
    return source


def _muscle_item_replacement(match: re.Match[str]) -> str:
    item = match.group(0)
    name_match = re.search(r'<span class="muscleName">([^<]+)</span>', item)
    if name_match:
        name = name_match.group(1).strip()
    else:
        name = next((candidate for candidate in MUSCLE_FOCUS if f">{candidate}</span>" in item), "")
        if not name:
            raise ValueError("Una tarjeta muscular no tiene un nombre reconocible")
        return _build_muscle_item(name)
    try:
        focus = MUSCLE_FOCUS[name]
    except KeyError as error:
        raise ValueError(f"Músculo no contemplado en el contrato visual: {name}") from error

    item = re.sub(r'\sdata-muscle-focus="[^"]*"', "", item)
    item = re.sub(r'\sdata-muscle-view="[^"]*"', "", item)
    visual = f'{"upper" if name in UPPER_MUSCLES else "lower"}-{focus["view"]}'
    if 'data-muscle-visual="' in item:
        item = re.sub(r'data-muscle-visual="[^"]*"', f'data-muscle-visual="{visual}"', item, count=1)
    else:
        item = item.replace('class="muscleDayItem"', f'class="muscleDayItem" data-muscle-visual="{visual}"', 1)
    item = re.sub(r'\saria-label="[^"]*"', "", item)
    item = item.replace(
        'class="muscleDayItem"',
        f'class="muscleDayItem" data-muscle-focus="{focus["key"]}" data-muscle-view="{focus["view"]}"',
        1,
    )
    item = re.sub(r'<span class="muscleFocusMarker"[^>]*></span>\s*', "", item)
    item = re.sub(
        r'<span class="muscleDayVisual [^"]+"[^>]*>',
        f'<span class="muscleDayVisual {focus["view"]}" title="Foco visual: {focus["region"]}">'
        f'{_marker_markup(name)}',
        item,
        count=1,
    )
    item = re.sub(
        r'<img class="muscleDayImage" src="[^"]+" alt="[^"]+"',
        lambda image_match: _image_markup(image_match.group(0), name, focus),
        item,
        count=1,
    )
    item = re.sub(
        r'<div class="muscleDayItem"([^>]*)>',
        rf'<div class="muscleDayItem"\1 aria-label="{name}; foco visual en {focus["region"]}">',
        item,
        count=1,
    )
    return item


def _build_muscle_item(name: str) -> str:
    focus = MUSCLE_FOCUS[name]
    color = MUSCLE_COLOR.get(name, "#72dcff")
    source = "../medios_publicados/rutinas_autocontenidas/musculos_generados/"
    image = f"{source}{'upper' if name in UPPER_MUSCLES else 'lower'}_{focus['view']}_anatomy_v1.webp"
    return (
        f'<div class="muscleDayItem" data-muscle-focus="{focus["key"]}" '
        f'data-muscle-view="{focus["view"]}" data-muscle-visual="{("upper" if name in UPPER_MUSCLES else "lower")}-{focus["view"]}" '
        f'aria-label="{name}; foco visual en {focus["region"]}">'
        f'<span class="muscleDayVisual {focus["view"]}" title="Foco visual: {focus["region"]}">'
        f'{_marker_markup(name)}'
        f'<img class="muscleDayImage" src="{image}" alt="Referencia anatómica ilustrativa {focus["view"]} del músculo {name}; foco visual aproximado en {focus["region"]}" decoding="async">'
        '<span class="muscleDayFallback" hidden>ANATOMÍA</span></span>'
        f'<span class="muscleDayCopy"><span class="muscleCode" style="color:{color}">{MUSCLE_CODE[name]}</span>'
        f'<span class="muscleName">{name}</span></span></div>'
    )


def _marker_markup(name: str) -> str:
    """Genera marcadores de foco estables y repetibles para una tarjeta."""
    return "".join(
        f'<span class="muscleFocusMarker" data-marker-side="{side}" '
        f'style="--marker-x:{x};--marker-y:{y}" aria-hidden="true"></span>'
        for side, x, y in MUSCLE_MARKERS[name]
    )


def _image_markup(markup: str, name: str, focus: dict[str, str]) -> str:
    image_prefix = "upper" if name in UPPER_MUSCLES else "lower"
    markup = re.sub(
        r'src="[^"]+"',
        f'src="../medios_publicados/rutinas_autocontenidas/musculos_generados/{image_prefix}_{focus["view"]}_anatomy_v1.webp"',
        markup,
        count=1,
    )
    return re.sub(
        r'alt="[^"]+"',
        f'alt="Referencia anatómica ilustrativa {focus["view"]} del músculo {name}; foco visual aproximado en {focus["region"]}"',
        markup,
        count=1,
    )


def standardize_muscle_visuals(source: str) -> str:
    grid_match = re.search(r'<div class="muscleDayGrid"[^>]*>.*?</div>\s*</div></div>', source, flags=re.S)
    if not grid_match:
        raise ValueError("No se encontró la cuadrícula de músculos del día")
    grid = re.sub(
        r'<div class="muscleDayItem"[^>]*>.*?</div>',
        _muscle_item_replacement,
        grid_match.group(0),
        flags=re.S,
    )
    # Sustituir primero la cuadrícula: insertar CSS antes de ella cambia los
    # offsets de la cadena y no debe invalidar los índices del match.
    source = source[: grid_match.start()] + grid + source[grid_match.end() :]
    source = source.replace(
        '<div class="muscleDayGrid">',
        '<div class="muscleDayGrid" data-enhancement="muscle-day-realistic-media-v1" data-fallback-contract="muscle-day-image-fallback-v1">',
        1,
    )
    if 'data-fix="muscle-specific-focus-v1"' in source:
        source = re.sub(r'<style data-fix="muscle-specific-focus-v1">.*?</style>', MUSCLE_VISUAL_STYLE, source, count=1, flags=re.S)
    else:
        source = source.replace('</head>', MUSCLE_VISUAL_STYLE + '\n</head>', 1)
    if 'data-enhancement="interaction-feedback-v1"' not in source:
        source = source.replace('</head>', INTERACTION_FEEDBACK_STYLE + '\n</head>', 1)
    source = standardize_shared_session_contract(source)
    next_index = 1

    def add_card_index(match: re.Match[str]) -> str:
        nonlocal next_index
        index = next_index
        next_index += 1
        return f'<article class="card" data-exercise-index="{index}">'

    source = re.sub(r'<article class="card">', add_card_index, source)
    source = re.sub(
        r'\.sessionCompletionCopy p\{[^}]*\}',
        '.sessionCompletionCopy p{margin:0;max-width:44rem;color:#d8eef5;font-size:clamp(1rem,2.2vw,1.28rem);font-weight:800;line-height:1.35;display:block;overflow:visible;overflow-wrap:anywhere;white-space:normal}',
        source,
        count=1,
    )
    if 'data-enhancement="canonical-card-contract-v1"' not in source:
        source = source.replace('<main class="cards">', CANONICAL_CONTRACT_MARKUP + '\n<main class="cards">', 1)
    if 'data-fix="phase-media-clarity-v5"' not in source:
        source = source.replace('</head>', CANONICAL_SHARED_STYLE + '\n</head>', 1)
    if 'data-enhancement="mobile-first-muscle-grid-v1"' not in source:
        source = source.replace('</body>', MOBILE_FIRST_MUSCLE_STYLE + '\n</body>', 1)
    return source
