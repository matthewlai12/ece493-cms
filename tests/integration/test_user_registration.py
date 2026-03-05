from fastapi.testclient import TestClient

from src.api.app import app
from src.services.user_registration_service import reset_user_registration_state


def setup_function() -> None:
    reset_user_registration_state()


def test_register_user_success_and_duplicate_rejected() -> None:
    client = TestClient(app)
    payload = {"name": "Bob", "email": "bob@example.com", "password": "password123"}

    first = client.post("/api/auth/register", json=payload)
    second = client.post("/api/auth/register", json=payload)

    assert first.status_code == 201
    assert first.json()["user"]["email"] == "bob@example.com"
    assert second.status_code == 400
    assert second.json()["detail"] == "Email already registered."


def test_register_user_invalid_email() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/auth/register",
        json={"name": "Carol", "email": "invalid", "password": "password123"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format."
