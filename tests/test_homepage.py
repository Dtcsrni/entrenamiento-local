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
        self.assertEqual(self.manifest["id"], "./")
        self.assertEqual(self.manifest["name"], "Gymratik: Rutinas y progreso")
        self.assertEqual(self.manifest["short_name"], "Gymratik")
        self.assertIn("Gymratik: Rutinas y progreso", self.html)
        self.assertIn('aria-label="Gymratik, inicio"', self.html)
        self.assertIn("background:rgba(11,16,23,.72) url('./icon.png')", self.html)
        self.assertIn('class="hero-mascot" src="./icon.png"', self.html)
        self.assertNotIn("Gymratic", self.html)
        self.assertNotIn("<title>Entrenamiento", self.html)

    def test_homepage_exposes_all_canonical_routines(self):
        routine_paths = (
            "Rutina_Dia_1_Espalda_Biceps_V1.html",
            "Rutina_Dia_2_Pierna_Gluteo_V1.html",
            "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html",
            "Rutina_Dia_4_Pierna_Equilibrio_V1.html",
        )
        for path in routine_paths:
            self.assertIn(path, self.html)

    def test_homepage_summary_matches_all_four_routines(self):
        self.assertIn("Cuatro sesiones claras", self.html)
        self.assertIn('<span class="plan-pill">4 días · 82 series</span>', self.html)
        self.assertIn('<div class="stat"><strong>4</strong><span>sesiones para rotar</span></div>', self.html)
        self.assertIn('<div class="stat"><strong>82</strong><span>series efectivas programadas</span></div>', self.html)
        self.assertIn('<span class="hero-card-label">Plan completo</span>', self.html)
        self.assertIn('<h2 id="nextSessionTitle">4 días</h2>', self.html)
        self.assertIn('href="#routines">Ver las 4 sesiones</a>', self.html)

    def test_homepage_uses_four_local_visual_references(self):
        image_paths = (
            "1350-7I6LNUG.jpg",
            "0739-10Z2DXU.jpg",
            "0577-T0yTjgW.jpg",
            "2287-V07qpXy.jpg",
        )
        for path in image_paths:
            self.assertIn(path, self.html)
        self.assertEqual(self.html.count('class="routine-card"'), 4)

    def test_pwa_icon_is_the_mascot_png_and_maskable_manifest_entry(self):
        icon = (ROOT / "icon.png").read_bytes()
        self.assertEqual(icon[:8], b"\x89PNG\r\n\x1a\n")
        self.assertNotIn(b"Gymratic", icon)
        self.assertNotIn(b"Entrenamiento Local", icon)
        self.assertEqual(self.manifest["icons"][0]["src"], "./icon.png")
        self.assertEqual(self.manifest["icons"][0]["type"], "image/png")
        self.assertEqual(self.manifest["icons"][0]["purpose"], "any maskable")
        self.assertTrue((ROOT / "icon.png").is_file())

    def test_homepage_requests_service_worker_update_and_sync(self):
        self.assertIn("updateViaCache: 'none'", self.html)
        self.assertIn("registration.update()", self.html)
        self.assertIn("type: 'SYNC_APP'", self.html)
        self.assertIn("event.data?.type === 'APP_UPDATED'", self.html)
        self.assertIn("navigator.serviceWorker.addEventListener('message'", self.html)

    def test_homepage_hides_install_button_when_app_is_already_installed(self):
        self.assertIn("display-mode: standalone", self.html)
        self.assertIn("navigator.standalone === true", self.html)
        self.assertIn("window.addEventListener('appinstalled'", self.html)
        self.assertIn("installButton.hidden = isInstalled() || !deferredInstallPrompt", self.html)
        self.assertIn("[hidden] { display:none !important; }", self.html)

    def test_homepage_shows_last_successful_update(self):
        self.assertIn('id="updateState"', self.html)
        self.assertIn("gymratik-last-update-v1", self.html)
        self.assertIn("Actualizado:", self.html)

    def test_homepage_exposes_persistent_progress_dashboard(self):
        self.assertIn('src="./progress-store.js"', self.html)
        self.assertIn('progressRecordedSeries', self.html)
        self.assertIn('progressTodaySeries', self.html)
        self.assertIn('TrainingProgressStore', self.html)
        self.assertIn('persistButton', self.html)

    def test_homepage_normalizes_partial_dashboard_data(self):
        self.assertIn('function normalizeDashboard', self.html)
        self.assertIn('fallbackRoutineProgress', self.html)
        self.assertIn('Array.isArray(source.routines)', self.html)
        self.assertIn('String(dashboard.todaySeries)', self.html)
        self.assertIn("source.temporal?.sameMinute === true", self.html)

    def test_homepage_reloads_after_service_worker_controller_change(self):
        self.assertIn("addEventListener('controllerchange'", self.html)
        self.assertIn('window.location.reload()', self.html)

    def test_homepage_is_offline_first_without_manual_preparation_prompt(self):
        self.assertNotIn('Prepáralo antes de salir', self.html)
        self.assertNotIn('Preparar sesiones', self.html)
        self.assertNotIn('cacheButton', self.html)
        self.assertNotIn('prepareOffline', self.html)

    def test_canonical_routines_use_distinct_progress_storage_keys(self):
        keys = []
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            marker = "const storageKey = '"
            start = source.index(marker) + len(marker)
            keys.append(source[start:source.index("'", start)])
        self.assertEqual(len(keys), 4)
        self.assertEqual(len(set(keys)), 4)
        self.assertIn("day1", keys[0])
        self.assertIn("day2", keys[1])
        self.assertIn("day3", keys[2])
        self.assertIn("day4", keys[3])

    def test_canonical_routines_publish_progress_to_shared_store(self):
        for path in sorted(CANONICAL.glob("Rutina_Dia_*_V1.html")):
            source = path.read_text(encoding="utf-8")
            self.assertIn('src="../../../progress-store.js"', source)
            self.assertIn('TrainingProgressStore?.capture', source)

    def test_day1_replaces_cross_day_duplicate_media_id(self):
        day1 = json.loads((ROOT / "data/rutinas_autocontenidas/evidencia/dia1_media_manifest.json").read_text(encoding="utf-8"))
        day3 = json.loads((ROOT / "data/rutinas_autocontenidas/evidencia/dia3_media_manifest.json").read_text(encoding="utf-8"))
        day1_ids = {item["dataset_id"] for item in day1["items"]}
        day3_ids = {item["repo_id"] for item in day3}
        self.assertIn("0575", day1_ids)
        self.assertNotIn("0577", day1_ids)
        self.assertIn("0577", day3_ids)
        self.assertTrue(day1_ids.isdisjoint(day3_ids))


if __name__ == "__main__":
    unittest.main()
