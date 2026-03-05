from fastapi.testclient import TestClient

from src.api.app import app
from src.services.user_registration_service import create_user_account, reset_user_registration_state


def setup_function() -> None:
    reset_user_registration_state()


def test_uc07_change_password_success() -> None:
    create_user_account("user@example.com", "StrongPass1", "User")
    client = TestClient(app)

    response = client.post(
        "/api/auth/password",
        json={
            "email": "user@example.com",
            "current_password": "StrongPass1",
            "new_password": "NewStrong2",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["updated"] is True


def test_uc07_change_password_failure() -> None:
    create_user_account("user@example.com", "StrongPass1", "User")
    client = TestClient(app)

    response = client.post(
        "/api/auth/password",
        json={
            "email": "user@example.com",
            "current_password": "bad",
            "new_password": "NewStrong2",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Current password is incorrect."
