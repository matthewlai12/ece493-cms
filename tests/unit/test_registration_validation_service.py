from src.services.registration_validation_service import validate_registration_payload


def test_validate_registration_payload_success() -> None:
    result = validate_registration_payload(
        {"name": "Dana", "email": "Dana@Example.com", "password": "Abcd1234"}
    )

    assert result["valid"] is True
    assert result["errors"] == []
    assert result["normalized"]["email"] == "dana@example.com"


def test_validate_registration_payload_invalid() -> None:
    result = validate_registration_payload({"name": "", "email": "bad", "password": "short"})

    assert result["valid"] is False
    assert "Name is required." in result["errors"]
    assert "Invalid email format." in result["errors"]
    assert "Password must be at least 8 characters." in result["errors"]
