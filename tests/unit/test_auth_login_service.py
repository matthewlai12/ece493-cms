from src.services.audit_log import list_events, reset_events
from src.services.auth_login_service import login_user
from src.services.user_registration_service import create_user_account, reset_user_registration_state


def setup_function() -> None:
    reset_user_registration_state()
    reset_events()


def test_login_user_success() -> None:
    create_user_account("user@example.com", "StrongPass1", "User")

    result = login_user("user@example.com", "StrongPass1")

    assert result["authenticated"] is True
    assert result["redirect_to"] == "/dashboard"
    assert list_events("auth_login")[-1]["details"]["success"] is True


def test_login_user_invalid_credentials() -> None:
    create_user_account("user@example.com", "StrongPass1", "User")

    try:
        login_user("user@example.com", "wrong")
    except ValueError as exc:
        assert str(exc) == "Username or password is incorrect."
    else:
        raise AssertionError("Expected login failure")
