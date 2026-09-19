import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
STORE = ROOT / "progress-store.js"


class ProgressStoreContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = STORE.read_text(encoding="utf-8")

    def test_progress_store_exists_and_uses_indexeddb(self):
        self.assertIn("indexedDB.open", self.source)
        self.assertIn("routineProgress", self.source)
        self.assertIn("sessions", self.source)

    def test_progress_store_has_fallback_and_migration_contract(self):
        self.assertIn("entrenamiento-progress-fallback-v1", self.source)
        self.assertIn("LEGACY_KEYS", self.source)
        self.assertIn("migrateLegacyProgress", self.source)

    def test_progress_store_exposes_dashboard_and_persistence_request(self):
        self.assertIn("getDashboard", self.source)
        self.assertIn("requestPersistence", self.source)
        self.assertIn("training-progress-updated", self.source)


if __name__ == "__main__":
    unittest.main()
