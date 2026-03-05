from src.services.audit_log import list_events, reset_events
from src.services.conference_register_service import (
    get_registration,
    register_for_conference,
    reset_conference_registration_state,
)


def setup_function() -> None:
    reset_conference_registration_state()
    reset_events()


def test_register_for_conference_success() -> None:
    registration = register_for_conference(
        "att-1",
        is_authenticated=True,
    )

    assert registration["id"] == 1
    assert registration["status"] == "pending_payment"
    assert registration["next_step"] == "/api/registrations/1/payment"
    assert get_registration("1") is not None
    assert list_events("conference_register")[-1]["details"]["registration_id"] == 1


def test_register_for_conference_requires_authentication() -> None:
    try:
        register_for_conference("att-2", is_authenticated=False)
    except ValueError as exc:
        assert str(exc) == "Authentication required to register."
    else:
        raise AssertionError("Expected ValueError")


def test_register_for_conference_rejects_closed_registration() -> None:
    try:
        register_for_conference(
            "att-3",
            is_authenticated=True,
            registration_open=False,
        )
    except ValueError as exc:
        assert str(exc) == "Conference registration is closed."
    else:
        raise AssertionError("Expected ValueError")
