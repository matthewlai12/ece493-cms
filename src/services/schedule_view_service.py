from collections.abc import Iterable
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any
from typing import TypedDict


class SessionView(TypedDict):
    title: str
    room: str
    start_time: str
    end_time: str


class ScheduleView(TypedDict):
    id: int
    published_at: str
    sessions: list[SessionView]


@lru_cache(maxsize=1)
def _default_schedules() -> list[dict]:
    return [
        {
            "id": 1,
            "status": "published",
            "published_at": datetime(2026, 2, 15, 12, 0, tzinfo=timezone.utc),
            "sessions": [
                {
                    "title": "Keynote",
                    "room": "Hall A",
                    "start_time": datetime(2026, 5, 1, 9, 0, tzinfo=timezone.utc),
                    "end_time": datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc),
                },
                {
                    "title": "Paper Session 1",
                    "room": "Room 201",
                    "start_time": datetime(2026, 5, 1, 10, 30, tzinfo=timezone.utc),
                    "end_time": datetime(2026, 5, 1, 12, 0, tzinfo=timezone.utc),
                },
            ],
        },
        {
            "id": 2,
            "status": "draft",
            "published_at": None,
            "sessions": [],
        },
    ]


def get_published_schedule(records: Iterable[dict] | None = None) -> ScheduleView | None:
    source = list(records) if records is not None else _default_schedules()
    published = [item for item in source if item.get("status") == "published"]
    if not published:
        return None

    latest = max(published, key=lambda item: item["published_at"])
    sessions = sorted(latest["sessions"], key=lambda item: item["start_time"])
    return {
        "id": int(latest["id"]),
        "published_at": latest["published_at"].isoformat(),
        "sessions": [
            {
                "title": str(session["title"]),
                "room": str(session["room"]),
                "start_time": session["start_time"].isoformat(),
                "end_time": session["end_time"].isoformat(),
            }
            for session in sessions
        ],
    }


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    records = data.get("records")
    schedule = get_published_schedule(records if isinstance(records, list) else None)
    return {"service": "schedule_view_service", "schedule": schedule}
