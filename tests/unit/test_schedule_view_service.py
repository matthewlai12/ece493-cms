from datetime import datetime, timezone

from src.services.schedule_view_service import get_published_schedule


def test_get_published_schedule_returns_latest_published() -> None:
    records = [
        {
            "id": 1,
            "status": "published",
            "published_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "sessions": [
                {
                    "title": "Older session",
                    "room": "A",
                    "start_time": datetime(2026, 5, 2, 9, 0, tzinfo=timezone.utc),
                    "end_time": datetime(2026, 5, 2, 10, 0, tzinfo=timezone.utc),
                }
            ],
        },
        {
            "id": 2,
            "status": "published",
            "published_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
            "sessions": [
                {
                    "title": "Later session",
                    "room": "B",
                    "start_time": datetime(2026, 5, 1, 11, 0, tzinfo=timezone.utc),
                    "end_time": datetime(2026, 5, 1, 12, 0, tzinfo=timezone.utc),
                },
                {
                    "title": "Earlier session",
                    "room": "B",
                    "start_time": datetime(2026, 5, 1, 9, 0, tzinfo=timezone.utc),
                    "end_time": datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc),
                },
            ],
        },
    ]

    schedule = get_published_schedule(records)

    assert schedule is not None
    assert schedule["id"] == 2
    assert [s["title"] for s in schedule["sessions"]] == ["Earlier session", "Later session"]


def test_get_published_schedule_returns_none_if_unpublished() -> None:
    records = [
        {"id": 1, "status": "draft", "published_at": None, "sessions": []},
    ]

    assert get_published_schedule(records) is None
