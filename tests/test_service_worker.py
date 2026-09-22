import unittest
from pathlib import Path


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
            self.assertIn("if (cached && !bypassCache)", source)
            self.assertIn("event.waitUntil(refresh(request, cache).catch(() => undefined))", source)
            self.assertIn("if (cached) return cached", source)

    def test_profile_mascots_are_part_of_the_offline_precache(self):
        for asset in ("mouse-female-effort.png", "mouse-male-effort.png"):
            self.assertIn(f"data/profile/{asset}", self.service_worker)
            self.assertIn(f"data/profile/{asset}", self.generator)

    def test_shared_routine_stylesheet_is_part_of_the_offline_precache(self):
        for source in (self.service_worker, self.generator):
            self.assertIn("routine-liquid-glass-v13.css", source)

    def test_only_worker_activation_announces_an_update_to_the_page(self):
        for source in (self.service_worker, self.generator):
            with self.subTest(source=source[:40]):
                self.assertIn("refreshApplication(notifyClients = false)", source)
                self.assertIn("if (!notifyClients) return", source)
                self.assertIn("refreshApplication(true)", source)
                self.assertIn("event.waitUntil(refreshApplication())", source)


if __name__ == "__main__":
    unittest.main()
