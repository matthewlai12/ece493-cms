from typing import Any

from src.services.use_case_engine import perform_use_case


def build_service_response(service: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return perform_use_case(service, payload or {})
