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

    def test_app_shell_is_network_first_with_offline_fallback(self):
        for source in (self.service_worker, self.generator):
            self.assertIn("const APP_SHELL = new Set", source)
            self.assertIn("progress-store.js", source)
            self.assertIn("const isAppShell = APP_SHELL.has(url.pathname)", source)
            self.assertIn("!isNavigation && !isAppShell && cached && !bypassCache", source)


if __name__ == "__main__":
    unittest.main()
