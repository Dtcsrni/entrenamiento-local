from __future__ import annotations

import argparse
import ipaddress
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

try:
    from .health import health_payload
except ImportError:  # Ejecución directa desde la raíz del repositorio.
    from health import health_payload


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8771


def validate_bind_host(host: str) -> None:
    """Impide que esta primera versión se exponga fuera del equipo local."""
    address = ipaddress.ip_address(host)
    if not address.is_loopback:
        raise ValueError("la API de desarrollo solo puede enlazar loopback")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - nombre impuesto por BaseHTTPRequestHandler.
        if self.path != "/healthz":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        body = json.dumps(health_payload(), separators=(",", ":")).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        # No registrar cabeceras ni consultas en esta superficie mínima.
        return


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    validate_bind_host(host)
    return ThreadingHTTPServer((host, port), HealthHandler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Liveness server local de Tezkatli")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", default=DEFAULT_PORT, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with create_server(args.host, args.port) as server:
        print(f"tezkatli-api liveness en http://{args.host}:{args.port}/healthz")
        server.serve_forever()


if __name__ == "__main__":
    main()
