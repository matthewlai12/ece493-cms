from typing import Any

from src.services.schedule_publish_service import list_published_schedules


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    require_auth = bool(data.get("require_auth", False))
    is_authenticated = bool(data.get("is_authenticated", False))
    if require_auth and not is_authenticated:
        raise ValueError("Authentication required to view attendee schedule.")

    schedules = list_published_schedules()
    if not schedules:
        return {
            "service": "schedule_view_attendee_service",
            "schedules": [],
            "message": "Conference schedule has not been published yet.",
        }

    return {
        "service": "schedule_view_attendee_service",
        "schedules": schedules,
        "message": "Published conference schedule retrieved.",
    }
