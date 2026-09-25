import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.build_pwa_service_worker import build_precache, fingerprint_content, render


ROOT = Path(__file__).parents[1]
SW = ROOT / "sw.js"
GENERATOR = ROOT / "scripts" / "build_pwa_service_worker.py"


class ServiceWorkerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service_worker = SW.read_text(encoding="utf-8")
        cls.generator = GENERATOR.read_text(encoding="utf-8")

    def test_local_resources_are_cache_first_with_offline_fallback(self):
        for source in (self.service_worker, self.generator):
            self.assertIn("progress-store.js", source)
            self.assertIn("if (cached && !bypassCache) return cached", source)
            self.assertIn("if (cached) return cached", source)

    def test_profile_mascots_are_part_of_the_offline_precache(self):
        for asset in ("mouse-female-effort.webp", "mouse-male-effort.webp", "mascot-install-phone.webp"):
            self.assertIn(f"data/profile/{asset}", self.service_worker)
            self.assertIn(f"data/profile/{asset}", self.generator)

    def test_worker_fingerprint_normalizes_text_line_endings_only(self):
        with TemporaryDirectory() as temp_dir:
            text_asset = Path(temp_dir) / "routine.css"
            binary_asset = Path(temp_dir) / "image.png"
            text_asset.write_bytes(b"a\r\nb\rc")
            binary_asset.write_bytes(b"a\r\nb\rc")

            self.assertEqual(fingerprint_content(text_asset), b"a\nb\nc")
            self.assertEqual(fingerprint_content(binary_asset), b"a\r\nb\rc")

    def test_generated_worker_cache_fingerprint_matches_current_precache(self):
        generated = render(build_precache())
        generated_name = re.search(r"const CACHE_NAME = '([^']+)';", generated)
        checked_in_name = re.search(r"const CACHE_NAME = '([^']+)';", self.service_worker)

        self.assertIsNotNone(generated_name)
        self.assertIsNotNone(checked_in_name)
        self.assertEqual(
            checked_in_name.group(1),
            generated_name.group(1),
            "sw.js está obsoleto: ejecuta python scripts/build_pwa_service_worker.py",
        )

    def test_shared_routine_stylesheet_is_part_of_the_offline_precache(self):
        for source in (self.service_worker, self.generator):
            self.assertIn("routine-liquid-glass-v13.css", source)

    def test_worker_reports_incremental_download_and_defers_updates(self):
        for source in (self.service_worker, self.generator):
            with self.subTest(source=source[:40]):
                self.assertIn("PRECACHE_PROGRESS", source)
                self.assertIn("for (const path of PRECACHE)", source)
                self.assertIn("self.skipWaiting()", source)
                self.assertIn("ACTIVATE_UPDATE", source)
                self.assertIn("self.clients.claim()", source)
                self.assertIn("notifyClientsAppUpdated()", source)
                self.assertIn("QuotaExceededError", source)
                self.assertIn("key.startsWith('entrenamiento-pwa-')", source)
                self.assertNotIn("cache.addAll(PRECACHE)", source)

    def test_optional_animations_are_not_in_offline_precache(self):
        self.assertNotIn("/videos/", self.service_worker)
        self.assertNotIn(".gif'", self.service_worker)

    def test_complete_cache_marker_is_written_after_download(self):
        for source in (self.service_worker, self.generator):
            with self.subTest(source=source[:40]):
                self.assertIn("__gymratik_complete__", source)
                self.assertIn("PREVIOUS_CACHE_NAME", source)


if __name__ == "__main__":
    unittest.main()
