from src.services.audit_log import list_events, reset_events
from src.services.conference_register_service import (
    get_registration,
    register_for_conference,
    reset_conference_registration_state,
)
from src.services.registration_payment_service import (
    pay_registration_fee,
    reset_registration_payment_state,
)


def setup_function() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_events()


def test_pay_registration_fee_success() -> None:
    registration = register_for_conference("att-10", is_authenticated=True)

    result = pay_registration_fee(
        registration_id=str(registration["id"]),
        amount=120.0,
        attendee_email="att10@example.com",
    )
    assert result["payment"]["status"] == "paid"
    assert result["registration_status"] == "confirmed"
    assert result["notification_sent"] is True
    assert get_registration("1")["status"] == "confirmed"
    assert list_events("registration_payment")[-1]["details"]["status"] == "paid"


def test_pay_registration_fee_declined_allows_retry_message() -> None:
    registration = register_for_conference("att-11", is_authenticated=True)

    result = pay_registration_fee(
        registration_id=str(registration["id"]),
        amount=120.0,
        attendee_email="",
        force_decline=True,
    )
    assert result["payment"]["status"] == "declined"
    assert result["registration_status"] == "payment_declined"
    assert result["notification_sent"] is False
    assert result["message"] == "Payment was declined. You can retry."


def test_pay_registration_fee_requires_existing_registration() -> None:
    try:
        pay_registration_fee(registration_id="999", amount=100.0)
    except ValueError as exc:
        assert str(exc) == "Registration record not found."
    else:
        raise AssertionError("Expected ValueError")
