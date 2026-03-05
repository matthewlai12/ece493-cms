from fastapi.testclient import TestClient

from src.api.app import app


def test_uc05_validate_registration_information() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/auth/register/validate",
        json={"name": "Eve", "email": "eve@example.com", "password": "Abcd1234"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["errors"] == []


def test_uc05_validate_registration_information_failure() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/auth/register/validate",
        json={"name": "", "email": "bad", "password": "nopass"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert len(body["errors"]) >= 1
