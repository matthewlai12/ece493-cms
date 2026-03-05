from src.services.user_registration_service import (
    create_user_account,
    reset_user_registration_state,
)


def setup_function() -> None:
    reset_user_registration_state()


def test_create_user_account_success() -> None:
    user = create_user_account("new@example.com", "password123", "New User")

    assert user["id"] == 1
    assert user["email"] == "new@example.com"
    assert user["redirect_to"] == "/login"


def test_create_user_account_rejects_short_password() -> None:
    try:
        create_user_account("new@example.com", "short", "New User")
    except ValueError as exc:
        assert str(exc) == "Password must be at least 8 characters."
    else:
        raise AssertionError("Expected ValueError")
