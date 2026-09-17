from __future__ import annotations

import sys
import unittest
from pathlib import Path

from jsonschema import ValidationError


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_contracts import build_validators  # noqa: E402


class JsonSchemaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validators = build_validators()

    def test_all_schemas_are_loaded(self) -> None:
        self.assertEqual(
            set(self.validators), {"analysis-job-v1.json", "zepp-event-v1.json"}
        )

    def test_analysis_job_rejects_invalid_uuid_and_status(self) -> None:
        document = {
            "jobId": "not-a-uuid",
            "idempotencyKey": "22222222-2222-4222-8222-222222222222",
            "status": "UNKNOWN",
            "schemaVersion": 1,
            "createdAt": "2026-08-23T12:00:00Z",
        }
        validator = self.validators["analysis-job-v1.json"]
        with self.assertRaises(ValidationError):
            validator.validate(document)

    def test_zepp_event_rejects_negative_sequence_and_extra_property(self) -> None:
        document = {
            "eventId": "33333333-3333-4333-8333-333333333333",
            "sourceDevice": "synthetic-watch",
            "capturedAt": "2026-08-23T12:00:00Z",
            "sequence": -1,
            "type": "SESSION_STARTED",
            "payloadVersion": 1,
            "payload": {},
            "unexpected": True,
        }
        validator = self.validators["zepp-event-v1.json"]
        with self.assertRaises(ValidationError):
            validator.validate(document)

    def test_valid_documents_are_accepted(self) -> None:
        analysis_job = {
            "jobId": "11111111-1111-4111-8111-111111111111",
            "idempotencyKey": "22222222-2222-4222-8222-222222222222",
            "status": "QUEUED",
            "schemaVersion": 1,
            "createdAt": "2026-08-23T12:00:00Z",
        }
        zepp_event = {
            "eventId": "33333333-3333-4333-8333-333333333333",
            "sourceDevice": "synthetic-watch",
            "capturedAt": "2026-08-23T12:00:00Z",
            "sequence": 0,
            "type": "SESSION_STARTED",
            "payloadVersion": 1,
            "payload": {},
        }
        self.validators["analysis-job-v1.json"].validate(analysis_job)
        self.validators["zepp-event-v1.json"].validate(zepp_event)


if __name__ == "__main__":
    unittest.main()
