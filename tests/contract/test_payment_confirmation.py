from fastapi import HTTPException

from src.api.payment_confirmation import handle_payment_confirmation
from src.services.conference_register_service import register_for_conference, reset_conference_registration_state
from src.services.payment_confirmation_service import reset_payment_confirmation_state
from src.services.registration_payment_service import pay_registration_fee, reset_registration_payment_state


def setup_function() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_payment_confirmation_state()


def test_payment_confirmation_endpoint() -> None:
    register_for_conference("att-50", attendee_email="att50@example.com", is_authenticated=True)
    pay_registration_fee("1", amount=100.0, attendee_email="att50@example.com")

    body = handle_payment_confirmation(registration_id="1")
    assert body["service"] == "payment_confirmation_service"
    assert body["ticket"]["registration_id"] == 1
    assert body["notification_sent"] is True


def test_payment_confirmation_endpoint_invalid_registration() -> None:
    try:
        handle_payment_confirmation(registration_id="x")
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Registration ID is invalid."
    else:
        raise AssertionError("Expected HTTPException")
