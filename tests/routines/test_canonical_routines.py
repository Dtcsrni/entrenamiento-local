from __future__ import annotations

import sys
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_canonical_routines import validate_path  # noqa: E402


CANONICAL = ROOT / "data" / "rutinas_autocontenidas" / "canonicas"


class CanonicalRoutineValidationTests(unittest.TestCase):
    def test_day2_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_2_Pierna_Gluteo_V1.html"), []
        )

    def test_day1_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html"), []
        )

    def test_day1_corruption_is_detected(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(
            encoding="utf-8"
        )
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            path = Path(directory) / "Rutina_Dia_1_Espalda_Biceps_V1.html"
            path.write_text(source.replace('data-exercise="3"', 'data-exercise="5"', 1), encoding="utf-8")
            errors = validate_path(path)
        self.assertTrue(any("secuencia contigua" in error for error in errors))

    def test_day3_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html"), []
        )

    def test_day4_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_4_Pierna_Equilibrio_V1.html"), []
        )

    def test_day3_current_exercise_cue_is_detected(self) -> None:
        source = (CANONICAL / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html").read_text(
            encoding="utf-8"
        )
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            path = Path(directory) / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html"
            path.write_text(source.replace('data-next="2"', 'data-next="1"', 1), encoding="utf-8")
            errors = validate_path(path)
        self.assertTrue(any("apunta a 1; se esperaba 2" in error for error in errors))

    def test_day3_does_not_keep_day1_media_repairs(self) -> None:
        source = (CANONICAL / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("machineOnlyCurl", source)
        self.assertNotIn("finalAssets", source)
        self.assertNotIn(
            "confirma directamente la identidad de la máquina del gimnasio", source
        )

    def test_canonical_routines_do_not_embed_license_or_attribution_metadata(self) -> None:
        forbidden_markers = (
            '"license":',
            'portraitLicense',
            'portraitCredit',
            'portraitSource',
            'authorContextSource',
            'CANDIDATE_PENDING_LICENSE_REVIEW',
            'sourceUrl:',
            'mediaStatus',
            'motivationSource',
            'gifAttribution',
        )
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            for marker in forbidden_markers:
                with self.subTest(path=path.name, marker=marker):
                    self.assertNotIn(marker, source)

    def test_canonical_routines_show_full_motivational_phrases(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            match = re.search(r"\.sessionCompletionCopy p\{([^}]*)\}", source)
            self.assertIsNotNone(match, path.name)
            rules = match.group(1)
            self.assertIn("display:block", rules, path.name)
            self.assertIn("overflow:visible", rules, path.name)
            self.assertIn("overflow-wrap:anywhere", rules, path.name)
            self.assertNotIn("-webkit-line-clamp", rules, path.name)

    def test_day1_has_machine_only_reference_and_two_phases_per_exercise(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            len(re.findall(r'<div[^>]*class="[^"]*machineRefBox[^"]*"', source)),
            6,
        )
        self.assertEqual(source.count('<div class="phaseLabel">Inicio'), 6)
        self.assertEqual(source.count('<div class="phaseLabel">Final'), 6)
        self.assertIn("3025-butterfly-reverse-front.jpg", source)
        self.assertIn("0592-b6hQYMb-machine-only.jpg", source)

    def test_day1_row_has_matching_media_and_metrics(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(
            encoding="utf-8"
        )
        card = source[source.index("<!-- 3 -->") : source.index("<!-- 4 -->")]
        self.assertIn("▶ VIDEO TÉCNICO · Remo horizontal", card)
        self.assertIn("Jl0r78dnqGU", card)
        self.assertIn("8–12 repeticiones", card)
        self.assertIn("2–2.5 min", card)
        self.assertIn("7–9 min", card)

    def test_all_routines_have_explicit_rest_transition_and_alert_contract(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            self.assertIn("startSeriesButton", source)
            self.assertIn("restPhase", source)
            self.assertIn("restNotifiedAt", source)
            self.assertIn("restReminderNotifiedAt", source)
            self.assertIn("sessionAbandonedAt", source)
            self.assertIn("sendBrowserNotification", source)
            self.assertIn("navigator.vibrate", source)
            self.assertIn("timing.timingVersion = 5", source)

    def test_series_flow_uses_one_button_and_enforces_minimum_rest(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("className = 'startSeriesButton'", source)
                self.assertIn(
                    "const startSeriesButton = item.tracker.querySelector('.completeSetButton');",
                    source,
                )
                self.assertIn("Completar serie ${nextIndex + 1}", source)
                self.assertIn("Iniciar serie ${nextIndex + 1}", source)
                self.assertIn("Descanso · ${formatElapsed(restRemaining)}", source)
                self.assertIn("mantén 5 s para continuar", source)
                self.assertNotIn("startExerciseButton", source)
                self.assertNotIn("item.startButton", source)
                self.assertIn("beginSeries(item, Date.now())", source)
                self.assertIn("}, 5000);", source)
                self.assertIn(
                    "resting && restRemaining > 0",
                    source,
                )
                self.assertIn(
                    "Date.now() - timing.restStartedAt < getRestRecommendation(item).minMs",
                    source,
                )
                self.assertNotRegex(source, r"\bseriesPreparing\b")

    def test_repetition_selector_uses_exercise_range_plus_four_without_defaulting(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            control = source[
                source.index("const repsTitle"):source.index("const loadLabel")
            ]
            reps_logic = source[
                source.index("const renderPerformanceReps"):source.index(
                    "item.performanceLoad.addEventListener"
                )
            ]
            with self.subTest(path=path.name):
                self.assertIn("repsInput.min = String(item.repMinimum)", source)
                self.assertIn("repsInput.max = String(item.repMaximum + 4)", source)
                self.assertIn("repsInput.dataset.selected = 'false'", source)
                self.assertIn("item.performanceReps.dataset.selected === 'true'", source)
                self.assertIn("reps <= item.repMaximum + 4", source)
                self.assertIn("performanceRepsNudge", control)
                self.assertIn("Elige entre ${item.repMinimum} y ${item.repMaximum + 4}", control)
                self.assertIn("aria-live', 'polite", control)
                self.assertIn("Math.min(item.repMaximum + 4", reps_logic)
                self.assertIn("Math.max(item.repMinimum", reps_logic)
                self.assertIn("savePerformanceDraft()", reps_logic)
                self.assertIn("data-enhancement=\"interaction-feedback-v1\"", source)
                self.assertIn("button:not(:disabled):active", source)
                self.assertNotIn("Number(item.performanceReps.value) > 0 ?", source)

    def test_all_routines_use_persistent_fifteen_second_preparation_before_timing(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertEqual(source.count("const PREPARATION_MS = 15000;"), 1)
                self.assertIn("warmup.phase = 'preparing'", source)
                self.assertIn("warmup.preparationEndsAt = warmupPreparationEndsAt", source)
                self.assertIn("timing.preparationEndsAt = endsAt", source)
                self.assertIn("getWarmupTiming().phase === 'preparing' && getWarmupTiming().preparationEndsAt", source)
                self.assertIn("Omitir ejercicio · mantén 10 s", source)
                self.assertIn("setTimeout(() => { skipHoldTimer = 0", source)
                self.assertIn("loadOutput.addEventListener('click'", source)
                self.assertIn("performanceLoadDirect", source)
                self.assertIn("--hold-progress", source)
                self.assertIn("root.sessionStartedAt = timestamp", source)
                self.assertIn("startSeriesPreparation(item);", source)
                self.assertIn(
                    "const startTiming = (item, timestamp = Date.now(), startSeries = false)",
                    source,
                )
                self.assertIn("startTiming(item, timestamp, true)", source)
                self.assertIn("clearPreparationTimers();", source)
                self.assertEqual(
                    source.count("sendBrowserNotification('Descanso listo'"), 1
                )
                self.assertNotIn(
                    "const preparing = isSeriesPreparing(item); if (preparing) "
                    "{ renderPreparationDisplay(item); if (item.restDisplay) item.restDisplay.hidden = true; return; } "
                    "const preparing = isSeriesPreparing(item);",
                    source,
                )

    def test_all_routines_expose_direct_decimal_load_entry_and_hold_feedback(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("loadOutput.addEventListener('click'", source)
                self.assertIn("editor.step = '0.1'", source)
                self.assertIn("entered <= Number(loadInput.max)", source)
                self.assertIn("item.performanceLoadExact = Math.round(entered * 10) / 10", source)
                self.assertIn("load: String(item.performanceLoadExact || 0)", source)
                self.assertIn("queueMicrotask(() => finish(true))", source)
                self.assertIn("startSeriesButton.style.setProperty('--hold-progress', '100%')", source)
                self.assertIn("--hold-progress", source)
                self.assertIn("}, 10000);", source)
                self.assertIn("state.__skippedExercises[key] = true", source)
                self.assertIn("row.skipped ? '↷ Omitido'", source)

    def test_editable_load_value_persists_decimal_independently_of_slider_step(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(encoding="utf-8")
        self.assertIn("item.performanceLoadExact = Math.round(entered * 10) / 10", source)
        self.assertIn("load: String(item.performanceLoadExact || 0)", source)
        self.assertIn("const loadValue = Number(item.performanceLoadExact)", source)
        self.assertIn("editor.addEventListener('blur', () => queueMicrotask(() => finish(true))", source)

    def test_all_routines_share_the_canonical_page_layout_contract(self) -> None:
        expected_cards = {"Rutina_Dia_1_Espalda_Biceps_V1.html": 6, "Rutina_Dia_2_Pierna_Gluteo_V1.html": 6, "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html": 7, "Rutina_Dia_4_Pierna_Equilibrio_V1.html": 7}
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertEqual(source.count('<main class="cards">'), 1)
                self.assertEqual(source.count('<footer class="sessionFooter"'), 1)
                self.assertNotIn('<footer class="footer">', source)
                card_indexes = [int(value) for value in re.findall(r'<article class="card" data-exercise-index="(\d+)">', source)]
                self.assertEqual(card_indexes, list(range(1, expected_cards[path.name] + 1)))

    def test_routine_navigation_targets_every_exercise_card_in_the_document(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("main.cards > article.card", source)
                self.assertGreaterEqual(
                    source.count("article.card[data-exercise-index]"), 4
                )
                self.assertIn("summaryExercise", source)
                self.assertIn("nextExerciseCue", source)

    def test_all_routines_expose_accessible_segmented_warmup_and_series_progress(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertEqual(source.count('data-enhancement="segmented-progress-bars-v1"'), 1)
                self.assertIn("warmupProgressSegments", source)
                self.assertIn("Progreso del calentamiento", source)
                self.assertIn("aria-valuemax', '2'", source)
                self.assertIn("seriesProgressSegments", source)
                self.assertIn("Series completadas", source)
                self.assertIn("seriesProgress.setAttribute('aria-valuenow', String(done))", source)
                self.assertIn("segment.classList.toggle('is-complete'", source)
                self.assertIn("warmupProgress.dataset.state = warmupState", source)
                self.assertIn("seriesProgress.dataset.state = seriesState", source)
                self.assertIn("'empty'", source)
                self.assertIn("'filling'", source)
                self.assertIn("'full'", source)
                self.assertIn("@keyframes progressSweep", source)
                self.assertIn("@keyframes progressPulse", source)
                self.assertIn("@keyframes progressFinish", source)
                self.assertIn("prefers-reduced-motion:reduce", source)

    def test_load_slider_can_be_saved_when_completing_a_series(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("item.performanceLoadOutput = loadOutput", source)
                self.assertIn("item.performanceLoadOutput.textContent = loadUnit", source)
                self.assertNotIn("loadOutput.textContent = loadUnit", source)

    def test_motivation_button_has_multiple_offline_fallback_phrases(self) -> None:
        fallback_phrases = (
            "La constancia convierte cada entrenamiento en progreso.",
            "Una serie bien hecha también cuenta.",
            "El avance se construye repetición a repetición.",
        )
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("if (!motivationalQuotes.length) motivationalQuotes.push(", source)
                for phrase in fallback_phrases:
                    self.assertIn(phrase, source)

    def test_all_routines_expose_access_to_homepage(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                match = re.search(
                    r'<a class="routine-home-link" href="([^"]+)"[^>]*>', source
                )
                self.assertIsNotNone(match)
                self.assertEqual((path.parent / match.group(1)).resolve(), ROOT / "index.html")
                self.assertIn('aria-label="Volver a la portada"', source)
                self.assertIn('>← Portada</a>', source)

    def test_all_routines_use_the_shared_liquid_glass_redesign(self) -> None:
        stylesheet = ROOT / "routine-liquid-glass-v13.css"
        self.assertTrue(stylesheet.is_file())
        css = stylesheet.read_text(encoding="utf-8")
        for marker in ("backdrop-filter:blur(18px)", "#ffd166", "prefers-reduced-motion:reduce"):
            self.assertIn(marker, css)
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertIn('href="../../../routine-liquid-glass-v13.css"', source)
                self.assertIn('grid-template-areas:"intro meta" "details details"', css)

    def test_all_routines_share_the_canonical_exercise_card_contract(self) -> None:
        required_markers = (
            r'class="machineRefBox(?:\s|\")',
            r'class="muscleRefBox(?:\s|\")',
            r'class="phaseRow(?:\s|\")',
            r'data-exercise-quick-summary',
            r'class="exerciseTracker(?:\s|\")',
            r'class="techSteps(?:\s|\")',
        )
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            cards = re.findall(
                r'<article class="card" data-exercise-index="\d+">.*?</article>',
                source,
                re.S,
            )
            with self.subTest(path=path.name):
                self.assertTrue(cards)
                self.assertIn('data-enhancement="canonical-card-contract-v1"', source)
                for card in cards:
                    for marker in required_markers:
                        self.assertEqual(len(re.findall(marker, card)), 1, marker)

    def test_all_routines_share_the_realistic_muscle_day_media_contract(self) -> None:
        expected_images = {
            "Rutina_Dia_1_Espalda_Biceps_V1.html": 6,
            "Rutina_Dia_2_Pierna_Gluteo_V1.html": 6,
            "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html": 3,
            "Rutina_Dia_4_Pierna_Equilibrio_V1.html": 6,
        }
        asset_root = ROOT / "data" / "rutinas_autocontenidas" / "medios_publicados"
        manifest = ROOT / "data" / "rutinas_autocontenidas" / "evidencia" / "muscle_day_visuals_manifest.json"
        self.assertTrue(manifest.is_file())
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            items = re.findall(r'<div class="muscleDayItem"[^>]*>', source)
            images = re.findall(
                r'<img class="muscleDayImage"[^>]+src="([^"]+)"[^>]+alt="([^"]+)"',
                source,
            )
            with self.subTest(path=path.name):
                self.assertEqual(len(items), expected_images[path.name])
                self.assertEqual(len(images), expected_images[path.name])
                self.assertIn('muscle-day-realistic-media-v1', source)
                self.assertIn('muscle-day-image-fallback-v1', source)
                for reference, alt in images:
                    self.assertTrue(alt.startswith("Referencia anatómica ilustrativa"))
                    self.assertTrue((path.parent / reference).is_file(), reference)
                self.assertTrue(all((asset_root / name).is_file() for name in (
                    "rutinas_autocontenidas/musculos_generados/upper_posterior_anatomy_v1.webp",
                    "rutinas_autocontenidas/musculos_generados/lower_posterior_anatomy_v1.webp",
                    "rutinas_autocontenidas/musculos_generados/lower_anterior_anatomy_v1.webp",
                    "rutinas_autocontenidas/musculos_generados/upper_anterior_anatomy_v1.webp",
                )))

    def test_all_routines_keep_specific_muscle_focus_and_valid_document_structure(self) -> None:
        expected = {
            "Rutina_Dia_1_Espalda_Biceps_V1.html": {
                "Dorsal ancho": ("latissimus", "posterior", "upper-posterior"),
                "Romboides": ("rhomboids", "posterior", "upper-posterior"),
                "Trapecio medio": ("middle-trapezius", "posterior", "upper-posterior"),
                "Deltoides posterior": ("rear-deltoid", "posterior", "upper-posterior"),
                "Bíceps braquial": ("biceps", "anterior", "upper-anterior"),
                "Pectoral mayor": ("pectoralis-major", "anterior", "upper-anterior"),
            },
            "Rutina_Dia_2_Pierna_Gluteo_V1.html": {
                "Cuádriceps": ("quadriceps", "anterior", "lower-anterior"),
                "Glúteo mayor": ("gluteus-maximus", "posterior", "lower-posterior"),
                "Isquiosurales": ("hamstrings", "posterior", "lower-posterior"),
                "Aductores": ("adductors", "anterior", "lower-anterior"),
                "Gastrocnemio": ("gastrocnemius", "posterior", "lower-posterior"),
                "Sóleo": ("soleus", "posterior", "lower-posterior"),
            },
            "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html": {
                "Pectoral mayor": ("pectoralis-major", "anterior", "upper-anterior"),
                "Deltoides": ("deltoid", "anterior", "upper-anterior"),
                "Tríceps": ("triceps", "posterior", "upper-posterior"),
            },
            "Rutina_Dia_4_Pierna_Equilibrio_V1.html": {
                "Cuádriceps": ("quadriceps", "anterior", "lower-anterior"),
                "Glúteo mayor": ("gluteus-maximus", "posterior", "lower-posterior"),
                "Isquiosurales": ("hamstrings", "posterior", "lower-posterior"),
                "Abductores": ("abductors", "posterior", "lower-posterior"),
                "Aductores": ("adductors", "anterior", "lower-anterior"),
                "Gastrocnemio": ("gastrocnemius", "posterior", "lower-posterior"),
            },
        }
        item_pattern = re.compile(
            r'<div class="muscleDayItem"[^>]*data-muscle-focus="([^"]+)"'
            r'[^>]*data-muscle-view="([^"]+)"[^>]*data-muscle-visual="([^"]+)"'
            r'[^>]*>.*?<span class="muscleName">([^<]+)</span>',
            re.S,
        )
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            observed = {
                name: (focus, view, visual)
                for focus, view, visual, name in item_pattern.findall(source)
            }
            with self.subTest(path=path.name):
                self.assertIn("</head>", source)
                self.assertIn("<body>", source)
                self.assertIn('<header class="hero">', source)
                self.assertIn('data-fix="muscle-specific-focus-v1"', source)
                self.assertEqual(observed, expected[path.name])
                if path.name == "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html":
                    self.assertIn(
                        'data-muscle-focus="triceps" data-muscle-view="posterior" '
                        'data-muscle-visual="upper-posterior"',
                        source,
                    )

    def test_all_routines_keep_explicit_anatomical_focus_markers(self) -> None:
        bilateral = {
            "Dorsal ancho",
            "Romboides",
            "Trapecio medio",
            "Deltoides posterior",
            "Bíceps braquial",
            "Pectoral mayor",
            "Cuádriceps",
            "Glúteo mayor",
            "Isquiosurales",
            "Aductores",
            "Abductores",
            "Gastrocnemio",
            "Sóleo",
            "Deltoides",
            "Tríceps",
        }
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            items = re.findall(r'<div class="muscleDayItem"[^>]*>.*?</div>', source, flags=re.S)
            for item in items:
                name_match = re.search(r'<span class="muscleName">([^<]+)</span>', item)
                self.assertIsNotNone(name_match, f"Tarjeta sin nombre: {path.name}")
                name = name_match.group(1)
                marker_count = len(re.findall(r'class="muscleFocusMarker"', item))
                with self.subTest(path=path.name, muscle=name):
                    self.assertEqual(marker_count, 2 if name in bilateral else 1)
                    self.assertIn('data-enhancement="muscle-marker-precision-v2"', source)
                    self.assertIn('data-enhancement="mobile-first-muscle-grid-v1"', source)
                    self.assertIn("--marker-x:", item)
                    self.assertIn("--marker-y:", item)

    def test_all_routines_keep_phase_media_readable_on_dark_ui(self) -> None:
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn('data-fix="phase-media-clarity-v5"', source)
                self.assertIn("article.card .phaseRow .photo img.realphoto{", source)
                self.assertIn("background:transparent!important;", source)
                self.assertIn("mix-blend-mode:normal!important;", source)
                self.assertIn('data-fix="day1-rowing-phase-pair-v1"', source)
                self.assertIn("1350-7I6LNUG.jpg", source)
                self.assertIn("1350-7I6LNUG-final.png", source)
                if path.name == "Rutina_Dia_1_Espalda_Biceps_V1.html":
                    self.assertIn(
                        "panatta-super-high-row-unilateral-start.webp",
                        source,
                    )
                    self.assertIn(
                        "panatta-super-high-row-unilateral-final.webp",
                        source,
                    )
                self.assertIn('data-enhancement="warmup-motion-zoom-v2"', source)
                self.assertIn("object-fit:cover!important;", source)


if __name__ == "__main__":
    unittest.main()
