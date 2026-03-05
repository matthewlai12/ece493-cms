from datetime import datetime, timezone

from src.services.registration_prices_service import list_active_registration_prices


def test_list_active_registration_prices_filters_and_sorts() -> None:
    now = datetime(2026, 3, 1, tzinfo=timezone.utc)
    records = [
        {
            "id": 1,
            "category": "regular",
            "amount": 450,
            "currency": "USD",
            "active_from": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "active_to": datetime(2026, 12, 1, tzinfo=timezone.utc),
        },
        {
            "id": 2,
            "category": "student",
            "amount": 250,
            "currency": "USD",
            "active_from": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "active_to": datetime(2026, 12, 1, tzinfo=timezone.utc),
        },
        {
            "id": 3,
            "category": "expired",
            "amount": 100,
            "currency": "USD",
            "active_from": datetime(2025, 1, 1, tzinfo=timezone.utc),
            "active_to": datetime(2025, 12, 31, tzinfo=timezone.utc),
        },
    ]

    result = list_active_registration_prices(records=records, now=now)

    assert [item["id"] for item in result] == [2, 1]
    assert all(item["currency"] == "USD" for item in result)
