import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
INDEX = ROOT / "index.html"
CANONICAL = ROOT / "data" / "rutinas_autocontenidas" / "canonicas"


class HomepageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))

    def test_public_brand_does_not_include_local(self):
        self.assertNotIn("Entrenamiento Local", self.html)
        self.assertEqual(self.manifest["name"], "Entrenamiento")

    def test_homepage_exposes_all_canonical_routines(self):
        routine_paths = (
            "Rutina_Dia_1_Espalda_Biceps_V1.html",
            "Rutina_Dia_2_Pierna_Gluteo_V1.html",
            "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html",
        )
        for path in routine_paths:
            self.assertIn(path, self.html)

    def test_homepage_uses_three_local_visual_references(self):
        image_paths = (
            "1350-7I6LNUG.jpg",
            "0739-10Z2DXU.jpg",
            "0577-T0yTjgW.jpg",
        )
        for path in image_paths:
            self.assertIn(path, self.html)
        self.assertEqual(self.html.count('class="routine-card"'), 3)

    def test_pwa_icon_has_the_new_mark_and_maskable_manifest_entry(self):
        icon = (ROOT / "icon.svg").read_text(encoding="utf-8")
        self.assertIn('id="title"', icon)
        self.assertIn('id="desc"', icon)
        self.assertIn('id="mark"', icon)
        self.assertNotIn("Entrenamiento Local", icon)
        self.assertEqual(self.manifest["icons"][0]["purpose"], "any maskable")

    def test_homepage_requests_service_worker_update_and_sync(self):
        self.assertIn("updateViaCache: 'none'", self.html)
        self.assertIn("registration.update()", self.html)
        self.assertIn("type: 'SYNC_APP'", self.html)

    def test_homepage_exposes_persistent_progress_dashboard(self):
        self.assertIn('src="./progress-store.js"', self.html)
        self.assertIn('progressRecordedSeries', self.html)
        self.assertIn('TrainingProgressStore', self.html)
        self.assertIn('persistButton', self.html)

    def test_canonical_routines_use_distinct_progress_storage_keys(self):
        keys = []
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            marker = "const storageKey = '"
            start = source.index(marker) + len(marker)
            keys.append(source[start:source.index("'", start)])
        self.assertEqual(len(keys), 3)
        self.assertEqual(len(set(keys)), 3)
        self.assertIn("day1", keys[0])
        self.assertIn("day2", keys[1])
        self.assertIn("day3", keys[2])

    def test_canonical_routines_publish_progress_to_shared_store(self):
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            self.assertIn('src="../../../progress-store.js"', source)
            self.assertIn('TrainingProgressStore?.capture', source)


if __name__ == "__main__":
    unittest.main()
