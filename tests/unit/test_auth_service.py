from src.services.auth_service import authenticate_user, hash_password, normalize_email, verify_password


def test_hash_and_verify_password_roundtrip() -> None:
    stored = hash_password("StrongPass1")
    assert verify_password("StrongPass1", stored) is True
    assert verify_password("WrongPass1", stored) is False


def test_authenticate_user_with_stored_credentials() -> None:
    stored_email = normalize_email("User@Example.com")
    stored_hash = hash_password("StrongPass1")

    assert authenticate_user(
        "user@example.com",
        "StrongPass1",
        stored_email=stored_email,
        password_hash=stored_hash,
    ) is True
    assert authenticate_user(
        "user@example.com",
        "WrongPass1",
        stored_email=stored_email,
        password_hash=stored_hash,
    ) is False
