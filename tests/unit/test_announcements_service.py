from datetime import datetime, timezone

from src.services.announcements_service import list_public_announcements


def test_list_public_announcements_filters_and_sorts() -> None:
    records = [
        {
            "id": 10,
            "title": "Older public",
            "body": "A",
            "published_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "is_public": True,
        },
        {
            "id": 11,
            "title": "Private",
            "body": "B",
            "published_at": datetime(2026, 1, 5, tzinfo=timezone.utc),
            "is_public": False,
        },
        {
            "id": 12,
            "title": "Newer public",
            "body": "C",
            "published_at": datetime(2026, 1, 10, tzinfo=timezone.utc),
            "is_public": True,
        },
    ]

    result = list_public_announcements(records)

    assert [item["id"] for item in result] == [12, 10]
    assert all("published_at" in item for item in result)
