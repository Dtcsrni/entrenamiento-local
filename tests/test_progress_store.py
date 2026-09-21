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
        self.assertIn("ACTIVITY_STORE", self.source)
        self.assertIn("DB_VERSION = 3", self.source)
        self.assertIn("PROFILE_STORE", self.source)
        self.assertIn("META_STORE", self.source)

    def test_progress_store_has_fallback_and_migration_contract(self):
        self.assertIn("entrenamiento-progress-fallback-v1", self.source)
        self.assertIn("LEGACY_KEYS", self.source)
        self.assertIn("migrateLegacyProgress", self.source)

    def test_progress_store_exposes_dashboard_and_persistence_request(self):
        self.assertIn("getDashboard", self.source)
        self.assertIn("requestPersistence", self.source)
        self.assertIn("training-progress-updated", self.source)
        self.assertIn("same-minute", self.source)
        self.assertIn("same-hour", self.source)
        self.assertIn("other-day", self.source)

    def test_progress_store_serializes_writes_and_merges_fallback(self):
        self.assertIn("writeQueues", self.source)
        self.assertIn("enqueueWrite", self.source)
        self.assertIn("Object.values(fallback.progress)", self.source)

    def test_progress_store_exposes_profile_history_and_backup_contract(self):
        for marker in ("getProfile", "saveProfile", "getHistory", "exportData", "importData", "gymratik-backup"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source)


if __name__ == "__main__":
    unittest.main()
