from src.services.audit_log import list_events, reset_events
from src.services.conference_register_service import register_for_conference, reset_conference_registration_state
from src.services.payment_confirmation_service import (
    get_confirmation_ticket,
    issue_confirmation_ticket,
    reset_payment_confirmation_state,
)
from src.services.registration_payment_service import pay_registration_fee, reset_registration_payment_state


def setup_function() -> None:
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_payment_confirmation_state()
    reset_events()


def test_issue_confirmation_ticket_success() -> None:
    register_for_conference("att-40", attendee_email="att40@example.com", is_authenticated=True)
    pay_registration_fee("1", amount=120.0, attendee_email="att40@example.com")

    result = issue_confirmation_ticket("1")
    assert result["ticket"]["registration_id"] == 1
    assert result["ticket"]["reference_code"].startswith("TKT-1-")
    assert result["notification_sent"] is True
    assert get_confirmation_ticket("1") is not None
    assert list_events("payment_confirmation")[-1]["details"]["ticket_id"] == result["ticket"]["id"]


def test_issue_confirmation_ticket_requires_paid_registration() -> None:
    register_for_conference("att-41", is_authenticated=True)
    try:
        issue_confirmation_ticket("1")
    except ValueError as exc:
        assert str(exc) == "Registration is not confirmed yet."
    else:
        raise AssertionError("Expected ValueError")


def test_issue_confirmation_ticket_notification_failure_is_non_blocking() -> None:
    register_for_conference("att-42", is_authenticated=True)
    pay_registration_fee("1", amount=100.0)

    result = issue_confirmation_ticket("1")
    assert result["ticket"]["registration_id"] == 1
    assert result["notification_sent"] is False
    assert result["message"] == "Confirmation ticket available; notification delivery failed."
