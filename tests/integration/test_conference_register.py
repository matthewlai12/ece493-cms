from src.api.conference_register import handle_conference_register
from src.services.conference_register_service import (
    get_registration,
    reset_conference_registration_state,
)


def test_conference_register_endpoint() -> None:
    reset_conference_registration_state()
    first = handle_conference_register(payload={"attendee_id": "att-1", "is_authenticated": True})
    second = handle_conference_register(payload={"attendee_id": "att-2", "is_authenticated": True})

    assert first["registration"]["id"] == 1
    assert second["registration"]["id"] == 2
    saved = get_registration("2")
    assert saved is not None
    assert saved["attendee_id"] == "att-2"
