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
        self.assertIn("0592-b6hQYMb-machine-only.webp", source)

    def test_day1_row_has_matching_media_and_metrics(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(
            encoding="utf-8"
        )
        card = source[source.index("<!-- 3 -->") : source.index("<!-- 4 -->")]
        self.assertIn("▶ VIDEO TÉCNICO · Remo horizontal", card)
        self.assertIn("Jl0r78dnqGU", card)
        self.assertIn("8–12 rep.", card)
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
                    "rutinas_autocontenidas/musculos_generados/upper_posterior_anatomy_v1.png",
                    "rutinas_autocontenidas/musculos_generados/lower_posterior_anatomy_v1.png",
                    "rutinas_autocontenidas/musculos_generados/lower_anterior_anatomy_v1.png",
                    "rutinas_autocontenidas/musculos_generados/upper_anterior_anatomy_v1.png",
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
