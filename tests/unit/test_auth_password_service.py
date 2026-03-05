from src.services.audit_log import list_events, reset_events
from src.services.auth_login_service import login_user
from src.services.auth_password_service import change_user_password
from src.services.user_registration_service import create_user_account, reset_user_registration_state


def setup_function() -> None:
    reset_user_registration_state()
    reset_events()


def test_change_user_password_success() -> None:
    create_user_account("user@example.com", "StrongPass1", "User")

    result = change_user_password("user@example.com", "StrongPass1", "NewStrong2")

    assert result["updated"] is True
    assert login_user("user@example.com", "NewStrong2")["authenticated"] is True
    assert list_events("auth_password")[-1]["details"]["success"] is True


def test_change_user_password_failure_keeps_old_password() -> None:
    create_user_account("user@example.com", "StrongPass1", "User")

    try:
        change_user_password("user@example.com", "WrongPass1", "NewStrong2")
    except ValueError as exc:
        assert str(exc) == "Current password is incorrect."
    else:
        raise AssertionError("Expected failure")

    assert login_user("user@example.com", "StrongPass1")["authenticated"] is True
