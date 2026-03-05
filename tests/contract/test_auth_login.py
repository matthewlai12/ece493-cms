from fastapi.testclient import TestClient

from src.api.app import app
from src.services.audit_log import list_events, reset_events
from src.services.user_registration_service import create_user_account, reset_user_registration_state


def test_auth_login_endpoint() -> None:
    reset_user_registration_state()
    reset_events()
    create_user_account("user@example.com", "StrongPass1", "User")

    client = TestClient(app)
    response = client.post("/api/auth/login", json={"email": "user@example.com", "password": "StrongPass1"})

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "auth_login_service"
    assert body["authenticated"] is True
    assert body["redirect_to"] == "/dashboard"
    events = list_events("auth_login")
    assert events and events[-1]["details"]["success"] is True
