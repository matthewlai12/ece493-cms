from src.api.conference_register import handle_conference_register
from src.api.payment_confirmation import handle_payment_confirmation
from src.api.registration_payment import handle_registration_payment
from src.services.payment_confirmation_service import (
    get_confirmation_ticket,
    reset_payment_confirmation_state,
)
from src.services.registration_payment_service import reset_registration_payment_state
from src.services.conference_register_service import reset_conference_registration_state


def setup_function() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_payment_confirmation_state()


def test_payment_confirmation_end_to_end() -> None:
    registration = handle_conference_register(
        payload={"attendee_id": "att-60", "attendee_email": "att60@example.com", "is_authenticated": True}
    )
    reg_id = str(registration["registration"]["id"])

    handle_registration_payment(
        registration_id=reg_id,
        payload={"amount": 150.0, "attendee_email": "att60@example.com"},
    )

    first = handle_payment_confirmation(registration_id=reg_id)
    second = handle_payment_confirmation(registration_id=reg_id)
    assert first["ticket"]["reference_code"] == second["ticket"]["reference_code"]
    stored = get_confirmation_ticket(reg_id)
    assert stored is not None
    assert stored["reference_code"] == first["ticket"]["reference_code"]
