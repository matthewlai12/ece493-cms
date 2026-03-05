from fastapi import HTTPException

from src.api.registration_payment import handle_registration_payment
from src.services.conference_register_service import (
    register_for_conference,
    reset_conference_registration_state,
)
from src.services.registration_payment_service import reset_registration_payment_state


def test_registration_payment_endpoint() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    register_for_conference("att-20", is_authenticated=True)

    body = handle_registration_payment(
        registration_id="1",
        payload={"amount": 100.0, "attendee_email": "att20@example.com"},
    )
    assert body["service"] == "registration_payment_service"
    assert body["payment"]["status"] == "paid"
    assert body["registration_status"] == "confirmed"


def test_registration_payment_endpoint_declined() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    register_for_conference("att-21", is_authenticated=True)
    body = handle_registration_payment(
        registration_id="1",
        payload={"amount": 100.0, "force_decline": True},
    )
    assert body["payment"]["status"] == "declined"
    assert body["registration_status"] == "payment_declined"


def test_registration_payment_endpoint_invalid_payload() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    try:
        handle_registration_payment(registration_id="x", payload={"amount": 100.0})
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Registration ID is invalid."
    else:
        raise AssertionError("Expected HTTPException")
