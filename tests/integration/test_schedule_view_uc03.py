from fastapi.testclient import TestClient

from src.api.app import app


def test_uc03_view_conference_schedule() -> None:
    client = TestClient(app)

    response = client.get("/api/schedule")

    assert response.status_code == 200
    body = response.json()
    assert "schedule" in body
    assert body["schedule"] is not None
    assert {"id", "published_at", "sessions"}.issubset(body["schedule"].keys())
