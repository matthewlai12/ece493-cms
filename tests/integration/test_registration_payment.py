from src.api.conference_register import handle_conference_register
from src.api.registration_payment import handle_registration_payment
from src.services.conference_register_service import (
    get_registration,
    reset_conference_registration_state,
)
from src.services.registration_payment_service import reset_registration_payment_state


def test_registration_payment_endpoint() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    registration = handle_conference_register(payload={"attendee_id": "att-30", "is_authenticated": True})
    reg_id = str(registration["registration"]["id"])

    paid = handle_registration_payment(
        registration_id=reg_id,
        payload={"amount": 150.0, "attendee_email": "att30@example.com"},
    )
    assert paid["payment"]["status"] == "paid"
    assert get_registration(reg_id)["status"] == "confirmed"


def test_registration_payment_declined_then_retry_success() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    registration = handle_conference_register(payload={"attendee_id": "att-31", "is_authenticated": True})
    reg_id = str(registration["registration"]["id"])

    declined = handle_registration_payment(
        registration_id=reg_id,
        payload={"amount": 100.0, "force_decline": True},
    )
    assert declined["payment"]["status"] == "declined"
    assert get_registration(reg_id)["status"] == "payment_declined"

    retry = handle_registration_payment(
        registration_id=reg_id,
        payload={"amount": 100.0, "attendee_email": "att31@example.com"},
    )
    assert retry["payment"]["status"] == "paid"
    assert get_registration(reg_id)["status"] == "confirmed"
