from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event

_registrations: list[dict[str, Any]] = []


class ConferenceRegistrationRecord(TypedDict):
    id: int
    attendee_id: str
    attendee_email: str
    status: str
    created_at: str
    next_step: str


def register_for_conference(
    attendee_id: str,
    *,
    attendee_email: str = "",
    is_authenticated: bool,
    registration_open: bool = True,
    pricing_available: bool = True,
) -> ConferenceRegistrationRecord:
    normalized_attendee = attendee_id.strip()
    if not normalized_attendee:
        raise ValueError("Attendee ID is required.")
    if not is_authenticated:
        raise ValueError("Authentication required to register.")
    if not registration_open:
        raise ValueError("Conference registration is closed.")
    if not pricing_available:
        raise ValueError("Conference pricing information is unavailable.")

    registration_id = len(_registrations) + 1
    registration: ConferenceRegistrationRecord = {
        "id": registration_id,
        "attendee_id": normalized_attendee,
        "attendee_email": attendee_email.strip().lower(),
        "status": "pending_payment",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "next_step": f"/api/registrations/{registration_id}/payment",
    }
    _registrations.append(dict(registration))
    record_event(
        "conference_register",
        actor=normalized_attendee,
        details={"registration_id": registration_id, "status": registration["status"]},
    )
    return registration


def get_registration(registration_id: str) -> ConferenceRegistrationRecord | None:
    if not registration_id.isdigit():
        return None
    target_id = int(registration_id)
    for registration in _registrations:
        if int(registration.get("id", -1)) == target_id:
            return dict(registration)
    return None


def update_registration_status(registration_id: str, status: str) -> bool:
    if not registration_id.isdigit():
        return False
    target_id = int(registration_id)
    normalized_status = status.strip()
    if not normalized_status:
        return False
    for registration in _registrations:
        if int(registration.get("id", -1)) == target_id:
            registration["status"] = normalized_status
            return True
    return False


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    registration = register_for_conference(
        attendee_id=str(data.get("attendee_id", "")),
        attendee_email=str(data.get("attendee_email", "")),
        is_authenticated=bool(data.get("is_authenticated", False)),
        registration_open=bool(data.get("registration_open", True)),
        pricing_available=bool(data.get("pricing_available", True)),
    )
    return {"service": "conference_register_service", "registration": registration}


def reset_conference_registration_state() -> None:
    _registrations.clear()
