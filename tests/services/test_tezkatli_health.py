from __future__ import annotations

import json
import sys
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "tezkatli-api" / "src"))

from tezkatli_api.health import health_payload  # noqa: E402
from tezkatli_api.server import create_server, validate_bind_host  # noqa: E402


class TezkatliHealthTests(unittest.TestCase):
    def test_health_payload_is_liveness_only(self) -> None:
        self.assertEqual(
            health_payload(),
            {
                "service": "tezkatli-api",
                "status": "ok",
                "checks": {"process": "ok"},
            },
        )

    def test_server_rejects_non_loopback_binding(self) -> None:
        with self.assertRaises(ValueError):
            validate_bind_host("0.0.0.0")

    def test_health_endpoint_and_unknown_path(self) -> None:
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address
            connection = HTTPConnection(host, port, timeout=2)
            connection.request("GET", "/healthz")
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), health_payload())
            connection.close()

            connection = HTTPConnection(host, port, timeout=2)
            connection.request("GET", "/readyz")
            response = connection.getresponse()
            self.assertEqual(response.status, 404)
            connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
