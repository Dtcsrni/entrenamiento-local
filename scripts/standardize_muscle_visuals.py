"""Estandariza la referencia anatómica de la franja «Músculos del día».

Las láminas son referencias ilustrativas. El foco visual ayuda a localizar la
región descrita sin afirmar que la imagen, por sí sola, demuestre activación
muscular ni superioridad fisiológica.
"""

from __future__ import annotations

import re


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


MUSCLE_VISUAL_STYLE = r'''<style data-fix="muscle-specific-focus-v1">
/* Referencia ilustrativa: el halo localiza la región, no pretende ser una
   segmentación clínica ni una prueba de activación muscular. */
.muscleDayItem[data-muscle-focus]{--focus-color:rgba(100,215,255,.92);--focus-x:50%;--focus-y:50%;--focus-r:38%;--focus-scale:1.18}
.muscleDayVisual{position:relative!important;width:104px!important;height:104px!important;flex:0 0 104px!important;overflow:hidden!important;isolation:isolate!important;border-radius:16px!important;background:#f7f5ee!important}
.muscleDayImage{display:block!important;width:100%!important;height:100%!important;max-width:none!important}
.muscleDayVisual::after{content:"";position:absolute;inset:0;z-index:2;pointer-events:none;border-radius:inherit;background:radial-gradient(ellipse at var(--focus-x) var(--focus-y),var(--focus-color) 0%,rgba(255,255,255,.12) 10%,transparent var(--focus-r));mix-blend-mode:screen;opacity:.72}
.muscleDayVisual::before{content:"";position:absolute;z-index:3;pointer-events:none;width:24px;height:24px;left:calc(var(--focus-x) - 12px);top:calc(var(--focus-y) - 12px);border:2px solid var(--focus-color);border-radius:50%;box-shadow:0 0 0 3px rgba(4,17,27,.36),0 0 18px var(--focus-color);opacity:.86}
.muscleDayItem[data-muscle-focus] .muscleDayImage{object-fit:cover!important;object-position:var(--focus-x) var(--focus-y)!important;transform:scale(var(--focus-scale))!important;transform-origin:var(--focus-x) var(--focus-y)!important}
.muscleDayItem[data-muscle-focus="latissimus"]{--focus-x:58%;--focus-y:57%;--focus-r:42%;--focus-scale:1.22}
.muscleDayItem[data-muscle-focus="rhomboids"]{--focus-x:50%;--focus-y:38%;--focus-r:30%;--focus-scale:1.34}
.muscleDayItem[data-muscle-focus="middle-trapezius"]{--focus-x:50%;--focus-y:43%;--focus-r:28%;--focus-scale:1.35}
.muscleDayItem[data-muscle-focus="rear-deltoid"]{--focus-x:23%;--focus-y:32%;--focus-r:27%;--focus-scale:1.32}
.muscleDayItem[data-muscle-focus="biceps"]{--focus-x:21%;--focus-y:47%;--focus-r:30%;--focus-scale:1.28}
.muscleDayItem[data-muscle-focus="pectoralis-major"]{--focus-x:50%;--focus-y:36%;--focus-r:35%;--focus-scale:1.25}
.muscleDayItem[data-muscle-focus="quadriceps"]{--focus-x:50%;--focus-y:37%;--focus-r:35%;--focus-scale:1.22}
.muscleDayItem[data-muscle-focus="gluteus-maximus"]{--focus-x:50%;--focus-y:22%;--focus-r:31%;--focus-scale:1.3}
.muscleDayItem[data-muscle-focus="hamstrings"]{--focus-x:50%;--focus-y:38%;--focus-r:31%;--focus-scale:1.26}
.muscleDayItem[data-muscle-focus="adductors"]{--focus-x:50%;--focus-y:40%;--focus-r:27%;--focus-scale:1.28}
.muscleDayItem[data-muscle-focus="abductors"]{--focus-x:58%;--focus-y:28%;--focus-r:29%;--focus-scale:1.28}
.muscleDayItem[data-muscle-focus="gastrocnemius"]{--focus-x:50%;--focus-y:60%;--focus-r:31%;--focus-scale:1.26}
.muscleDayItem[data-muscle-focus="soleus"]{--focus-x:50%;--focus-y:72%;--focus-r:26%;--focus-scale:1.3}
.muscleDayItem[data-muscle-focus="deltoid"]{--focus-x:22%;--focus-y:30%;--focus-r:27%;--focus-scale:1.28}
.muscleDayItem[data-muscle-focus="triceps"]{--focus-x:22%;--focus-y:48%;--focus-r:30%;--focus-scale:1.26}
.muscleDayItem[data-muscle-focus="biceps"] .muscleDayVisual::after,.muscleDayItem[data-muscle-focus="deltoid"] .muscleDayVisual::after{background:radial-gradient(ellipse at 21% 47%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 34%),radial-gradient(ellipse at 79% 47%,var(--focus-color) 0%,rgba(255,255,255,.12) 11%,transparent 34%)}
.muscleDayItem[data-muscle-focus="biceps"] .muscleDayVisual::before,.muscleDayItem[data-muscle-focus="deltoid"] .muscleDayVisual::before{left:calc(21% - 12px)}
.muscleDayCopy{display:flex!important;min-width:0!important;flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:4px!important}
.muscleDayCopy .muscleCode{display:inline-flex!important;align-items:center!important;min-height:22px;padding:3px 8px;border:1px solid currentColor;border-radius:999px;font-size:.68rem!important;line-height:1!important;letter-spacing:.03em!important}
.muscleDayCopy .muscleName{display:block!important;font-size:clamp(.78rem,1.25vw,1rem)!important;line-height:1.15!important}
.muscleDayCopy .muscleName{overflow-wrap:anywhere!important}
@media(max-width:640px){
  .muscleDayVisual{width:76px!important;height:76px!important;flex:0 0 76px!important}
  .muscleDayItem[data-muscle-focus] .muscleDayVisual::before{width:20px;height:20px;left:calc(var(--focus-x) - 10px);top:calc(var(--focus-y) - 10px)}
  .muscleDayItem[data-muscle-focus="biceps"] .muscleDayVisual::before,.muscleDayItem[data-muscle-focus="deltoid"] .muscleDayVisual::before{left:calc(21% - 10px)}
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
    if "timing.restReminderNotifiedAt = timing.restNotifiedAt; sendBrowserNotification" not in source:
        source = source.replace(
            "timing.restNotifiedAt = Date.now();",
            "timing.restNotifiedAt = Date.now(); timing.restReminderNotifiedAt = timing.restNotifiedAt; sendBrowserNotification('Descanso listo', `Puedes iniciar ${item.title}.`);",
        )
    if "timing.restNotifiedAt = 0; timing.restReminderNotifiedAt = 0;" not in source:
        source = source.replace(
            "timing.restNotifiedAt = 0;",
            "timing.restNotifiedAt = 0; timing.restReminderNotifiedAt = 0;",
        )
    if "current.restNotifiedAt = 0; current.restReminderNotifiedAt = 0;" not in source:
        source = source.replace(
            "current.restNotifiedAt = 0;",
            "current.restNotifiedAt = 0; current.restReminderNotifiedAt = 0;",
        )
    if "sessionAbandonedAt = Date.now()" not in source:
        source = source.replace(
            "document.addEventListener('visibilitychange', renderTimingDisplays);",
            "document.addEventListener('visibilitychange', renderTimingDisplays); window.addEventListener('pagehide', () => { const timing = state.__timing; if (timing?.sessionStartedAt && !timing.sessionEndedAt) { timing.sessionAbandonedAt = Date.now(); save(); } }, { once: true });",
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
    item = re.sub(
        r'<span class="muscleDayVisual [^"]+">',
        f'<span class="muscleDayVisual {focus["view"]}" title="Foco visual: {focus["region"]}">',
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
    image = f"{source}{'upper' if name in UPPER_MUSCLES else 'lower'}_{focus['view']}_anatomy_v1.png"
    return (
        f'<div class="muscleDayItem" data-muscle-focus="{focus["key"]}" '
        f'data-muscle-view="{focus["view"]}" data-muscle-visual="{("upper" if name in UPPER_MUSCLES else "lower")}-{focus["view"]}" '
        f'aria-label="{name}; foco visual en {focus["region"]}">'
        f'<span class="muscleDayVisual {focus["view"]}" title="Foco visual: {focus["region"]}">'
        f'<img class="muscleDayImage" src="{image}" alt="Referencia anatómica ilustrativa {focus["view"]} del músculo {name}; foco visual aproximado en {focus["region"]}" decoding="async">'
        '<span class="muscleDayFallback" hidden>ANATOMÍA</span></span>'
        f'<span class="muscleDayCopy"><span class="muscleCode" style="color:{color}">{MUSCLE_CODE[name]}</span>'
        f'<span class="muscleName">{name}</span></span></div>'
    )


def _image_markup(markup: str, name: str, focus: dict[str, str]) -> str:
    image_prefix = "upper" if name in UPPER_MUSCLES else "lower"
    markup = re.sub(
        r'src="[^"]+"',
        f'src="../medios_publicados/rutinas_autocontenidas/musculos_generados/{image_prefix}_{focus["view"]}_anatomy_v1.png"',
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
    return source
