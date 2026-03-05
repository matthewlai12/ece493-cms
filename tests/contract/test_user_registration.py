from fastapi.testclient import TestClient

from src.api.app import app
from src.services.user_registration_service import reset_user_registration_state


def setup_function() -> None:
    reset_user_registration_state()


def test_register_user_contract() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/auth/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "securepass1"},
    )

    assert response.status_code == 201
    body = response.json()
    assert "user" in body
    assert {"id", "email", "name", "status", "created_at", "redirect_to"}.issubset(
        body["user"].keys()
    )
    assert body["user"]["redirect_to"] == "/login"
