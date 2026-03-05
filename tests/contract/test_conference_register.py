from fastapi import HTTPException

from src.api.conference_register import handle_conference_register
from src.services.conference_register_service import reset_conference_registration_state


def test_conference_register_endpoint() -> None:
    reset_conference_registration_state()
    body = handle_conference_register(payload={"attendee_id": "att-1", "is_authenticated": True})
    assert body["service"] == "conference_register_service"
    assert body["registration"]["status"] == "pending_payment"


def test_conference_register_endpoint_requires_authentication() -> None:
    reset_conference_registration_state()
    try:
        handle_conference_register(payload={"attendee_id": "att-1", "is_authenticated": False})
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Authentication required to register."
    else:
        raise AssertionError("Expected HTTPException")
