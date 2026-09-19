"""Repara la estructura de tarjetas del HTML canónico del Día 1."""

import re
from pathlib import Path


HTML = Path(__file__).parents[1] / "data/rutinas_autocontenidas/canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html"


CARDS_4_5 = r'''<!-- 4 -->
<article class="card"><div aria-hidden="true" class="cardGlow"></div>
<div class="meta">
<div class="metaTop"><div class="num">4</div></div>
<div class="exTitle">APERTURA INVERSA EN MÁQUINA</div>
<div class="zone">HOMBRO · DELTOIDES POSTERIOR</div><div class="chipRow"><span class="infoChip chipExercise">Ejercicio 4</span><span class="infoChip">HOMBRO</span><span class="infoChip">DELTOIDES POSTERIOR</span></div>
<div class="machinePill"><span class="pillText">butterfly reverse · apoyo de pecho</span></div>
</div>
<div class="visual"><div class="phaseRow">
<div class="phaseCol"><div class="phaseLabel">Inicio</div><div class="photo techZoom"><img alt="Apertura inversa en máquina, posición inicial" class="realphoto" loading="lazy" src="../medios_publicados/ejercicios-compartido/images/0602-myfUsKf.jpg"/></div></div>
<div class="swap" aria-hidden="true">→</div>
<div class="phaseCol"><div class="phaseLabel">Final</div><div class="photo techZoom"><img alt="Apertura inversa en máquina, referencia final" class="realphoto" loading="lazy" src="../medios_publicados/ejercicios-compartido/images/3025-butterfly-reverse-front.jpg"/></div></div>
</div></div>
<div class="coach"><div class="coachHeader">Técnica clave</div><div class="exerciseQuickSummary" data-exercise-quick-summary aria-label="Resumen del ejercicio"></div><div class="metrics"><div class="metric series"><div class="metricText"><div class="metricLabel">Series</div><div class="metricVal">3 series</div></div></div><div class="metric reps"><div class="metricText"><div class="metricLabel">Repeticiones</div><div class="metricVal">12–20 rep.</div></div></div><div class="metric rest"><div class="metricText"><div class="metricLabel">Descanso</div><div class="metricVal"><strong class="timeCue">1.5 min</strong></div></div></div></div><div class="exerciseTracker" data-exercise="4" data-series-keys="e4s1 e4s2 e4s3"><div class="exerciseTrackerHead"><span>Contador de series</span><span class="exerciseTrackerMeta"><strong class="exerciseProgress">0/3</strong><span class="exerciseStatus" hidden>Completado</span></span></div><div class="exerciseSetButtons" role="group" aria-label="Contador de series de apertura inversa"><button type="button" class="completeSetButton" aria-label="Completar serie 1 de 3">Completar serie 1 de 3</button><button type="button" class="machinePendingToggle" data-pending-key="p4" aria-pressed="false">⚠ Máquina ocupada</button><div class="nextExerciseRow"><button type="button" class="nextExerciseCue" data-next="5" hidden><span class="nextArrow" aria-hidden="true">↓</span> Siguiente: 05 · Curl de bíceps en máquina</button></div></div></div></div>
<div class="techSteps"><div class="techStep setup"><div class="techStepTitle">1 · Ajuste</div><div class="techStepText">Ajusta el asiento y el apoyo para que los hombros queden cómodos y los codos alineados con el eje.</div></div><div class="techStep move"><div class="techStepTitle">2 · Ejecución</div><div class="techStepText">Abre los brazos hacia atrás en un arco controlado, sin encoger los hombros ni perder el apoyo del pecho.</div></div><div class="techStep control"><div class="techStepTitle">3 · Ritmo y respiración</div><div class="techStepText">Exhala al abrir y regresa en 2–3 s manteniendo tensión continua.</div></div><div class="techStep warning"><div class="techStepTitle">⚠ Evita</div><div class="techStepText">Impulsarte, extender de más el hombro o convertir el movimiento en un remo.</div></div></div>
</div></article>
<!-- 5 -->
<article class="card"><div aria-hidden="true" class="cardGlow"></div>
<div class="meta">
<div class="metaTop"><div class="num">5</div></div>
<div class="exTitle">CURL DE BÍCEPS EN MÁQUINA</div>
<div class="zone">BRAZO · BÍCEPS</div><div class="chipRow"><span class="infoChip chipExercise">Ejercicio 5</span><span class="infoChip">BRAZO</span><span class="infoChip">BÍCEPS</span></div>
<div class="machinePill"><span class="pillText">curl tipo preacher · brazo apoyado</span></div>
</div>
<div class="visual"><div class="phaseRow">
<div class="phaseCol"><div class="phaseLabel">Inicio</div><div class="photo techZoom"><img alt="Curl de bíceps en máquina, posición inicial" class="realphoto" loading="lazy" src="../medios_publicados/ejercicios-compartido/images/0592-b6hQYMb-start.jpg"/></div></div>
<div class="swap" aria-hidden="true">→</div>
<div class="phaseCol"><div class="phaseLabel">Final</div><div class="photo techZoom"><img alt="Curl de bíceps en máquina, posición final" class="realphoto" loading="lazy" src="../medios_publicados/ejercicios-compartido/images/0592-b6hQYMb-final.png"/></div></div>
</div></div>
<div class="coach"><div class="coachHeader">Técnica clave</div><div class="exerciseQuickSummary" data-exercise-quick-summary aria-label="Resumen del ejercicio"></div><div class="metrics"><div class="metric series"><div class="metricText"><div class="metricLabel">Series</div><div class="metricVal">3 series</div></div></div><div class="metric reps"><div class="metricText"><div class="metricLabel">Repeticiones</div><div class="metricVal">10–15 rep.</div></div></div><div class="metric rest"><div class="metricText"><div class="metricLabel">Descanso</div><div class="metricVal"><strong class="timeCue">1.5–2 min</strong></div></div></div></div><div class="exerciseTracker" data-exercise="5" data-series-keys="e5s1 e5s2 e5s3"><div class="exerciseTrackerHead"><span>Contador de series</span><span class="exerciseTrackerMeta"><strong class="exerciseProgress">0/3</strong><span class="exerciseStatus" hidden>Completado</span></span></div><div class="exerciseSetButtons" role="group" aria-label="Contador de series de curl de bíceps"><button type="button" class="completeSetButton" aria-label="Completar serie 1 de 3">Completar serie 1 de 3</button><button type="button" class="machinePendingToggle" data-pending-key="p5" aria-pressed="false">⚠ Máquina ocupada</button><div class="nextExerciseRow"><button type="button" class="nextExerciseCue" data-next="6" hidden><span class="nextArrow" aria-hidden="true">↓</span> Siguiente: 06 · Press de pecho complementario</button></div></div></div></div>
<div class="techSteps"><div class="techStep setup"><div class="techStepTitle">1 · Ajuste</div><div class="techStepText">Alinea el codo con el eje y apoya por completo la parte posterior del brazo.</div></div><div class="techStep move"><div class="techStepTitle">2 · Ejecución</div><div class="techStepText">Flexiona el codo sin despegarlo del apoyo; sube hasta una contracción cómoda.</div></div><div class="techStep control"><div class="techStepTitle">3 · Ritmo y respiración</div><div class="techStepText">Exhala al subir y desciende en 2–3 s sin perder tensión.</div></div><div class="techStep warning"><div class="techStepTitle">⚠ Evita</div><div class="techStepText">Levantar el hombro, adelantar el codo, doblar la muñeca o rebotar.</div></div></div>
</div></article>'''


def main() -> None:
    with HTML.open("r", encoding="utf-8", newline="") as handle:
        source = handle.read()
    newline = "\r\n" if "\r\n" in source else "\n"
    bad_tracker = 'data-exercise="5" data-series-keys="e5s1 e5s2 e5s3"'
    e3_tracker = 'data-exercise="3" data-series-keys="e3s1 e3s2 e3s3"'
    if bad_tracker in source and e3_tracker not in source:
        source = source.replace(bad_tracker, e3_tracker, 1)
        source = source.replace('Contador del curl de bíceps', 'Contador del remo horizontal', 1)
        source = source.replace('data-pending-key="p5"', 'data-pending-key="p3"', 1)
    elif source.count(e3_tracker) >= 2:
        second = source.find(e3_tracker, source.find(e3_tracker) + 1)
        source = source[:second] + source[second:].replace(e3_tracker, bad_tracker, 1)
    source = re.sub(
        r'(<div class="exerciseTracker" data-exercise="3" data-series-keys="e3s1 e3s2 e3s3">.*?data-next=")6(" hidden><span class="nextArrow" aria-hidden="true">↓</span> Siguiente: )06 · Press de pecho(?: complementario)?(</button>)',
        r'\g<1>4\g<2>04 · Apertura inversa en máquina\g<3>',
        source,
        count=1,
        flags=re.S,
    )
    e3_next = 'data-next="4" hidden><span class="nextArrow" aria-hidden="true">↓</span> Siguiente: 04 · Apertura inversa en máquina</button>'
    if source.count(e3_next) >= 2:
        second = source.find(e3_next, source.find(e3_next) + 1)
        source = source[:second] + source[second:].replace(e3_next, 'data-next="6" hidden><span class="nextArrow" aria-hidden="true">↓</span> Siguiente: 06 · Press de pecho complementario</button>', 1)
    source = source.replace('Siguiente: 03 · Remo horizontal</button>', 'Siguiente: 03 · Remo horizontal en máquina</button>', 1)
    source = source.replace('images/0592-b6hQYMb-start.jpg', 'images/0592-b6hQYMb.jpg', 1)
    if 'src="../../../progress-store.js"' not in source:
        source = source.replace('</head>', '<script src="../../../progress-store.js"></script>\n</head>', 1)
    legacy_save = "  const save = () => { try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) {} };"
    progress_save = """  const routineId = storageKey.match(/day\\d+/)?.[0] || 'day1';
  const plannedSeries = trackers.reduce((sum, tracker) => sum + (tracker.dataset.seriesKeys || '').trim().split(/\\s+/).filter(Boolean).length, 0);
  const publishProgress = (force = false) => {
    const hasActivity = Object.keys(state).some((key) => /^e\\d+s\\d+$/.test(key) && state[key] === true) || Boolean(state.__timing?.sessionStartedAt);
    if (!force && !hasActivity) return;
    window.TrainingProgressStore?.capture({
      routineId,
      state,
      totalExercises: trackers.length,
      totalSeries: plannedSeries
    });
  };
  const save = () => {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); }
    catch (error) { window.dispatchEvent(new CustomEvent('training-storage-error', { detail: { error } })); }
    publishProgress(true);
  };
  publishProgress();"""
    if legacy_save in source:
        source = source.replace(legacy_save, progress_save, 1)
    elif 'const publishProgress = () =>' not in source:
        raise RuntimeError("No se encontró el guardado de progreso esperado")
    marker = f"{newline}<!-- 6 -->"
    if marker not in source:
        raise RuntimeError("No se encontró el punto de inserción antes de la tarjeta 6")
    if '<div class="num">4</div>' not in source and '<div class="num">5</div>' not in source:
        source = source.replace(marker, newline + CARDS_4_5.replace("\n", newline) + marker, 1)
    elif '<div class="num">4</div>' not in source or '<div class="num">5</div>' not in source:
        raise RuntimeError("Solo existe una de las tarjetas 4 o 5; se evita alterar una tarjeta parcial")
    source = source.replace('images/0592-b6hQYMb-start.jpg', 'images/0592-b6hQYMb.jpg')
    for exercise, rest, duration in ((4, "1.5 min", "5–7 min"), (5, "1.5–2 min", "5–7 min")):
        tracker_marker = f'<div class="exerciseTracker" data-exercise="{exercise}"'
        rest_metric = f'<div class="metric rest"><div class="metricText"><div class="metricLabel">Descanso</div><div class="metricVal"><strong class="timeCue">{rest}</strong></div></div></div>'
        duration_metric = f'<div class="metric duration"><div class="metricText"><div class="metricLabel">Duración aprox.</div><div class="metricVal"><strong class="timeCue">{duration}</strong></div></div></div>'
        source = re.sub(
            rf'(<!-- {exercise} -->\s*<article class="card">.*?)(<div class="metric rest">).*?(?={re.escape(tracker_marker)})',
            rf'\g<1>{rest_metric}{duration_metric}</div></div>',
            source,
            count=1,
            flags=re.S,
        )
    with HTML.open("w", encoding="utf-8", newline="") as handle:
        handle.write(source)


if __name__ == "__main__":
    main()
