from __future__ import annotations


SERVICE_NAME = "tezkatli-api"


def health_payload() -> dict[str, object]:
    """Devuelve únicamente el estado de liveness del proceso."""
    return {
        "service": SERVICE_NAME,
        "status": "ok",
        "checks": {"process": "ok"},
    }
