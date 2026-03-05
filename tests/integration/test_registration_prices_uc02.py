from fastapi.testclient import TestClient

from src.api.app import app


def test_uc02_view_registration_prices() -> None:
    client = TestClient(app)

    response = client.get("/api/registration-prices")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert isinstance(body["items"], list)
    assert len(body["items"]) >= 1
    assert {"id", "category", "amount", "currency", "active_from", "active_to"}.issubset(
        body["items"][0].keys()
    )
