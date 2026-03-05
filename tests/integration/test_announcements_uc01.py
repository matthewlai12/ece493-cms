from fastapi.testclient import TestClient

from src.api.app import app


def test_uc01_get_public_announcements() -> None:
    client = TestClient(app)

    response = client.get("/api/announcements")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert isinstance(body["items"], list)
    assert len(body["items"]) >= 1
    assert {"id", "title", "body", "published_at"}.issubset(body["items"][0].keys())
