from collections.abc import Iterable
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any
from typing import TypedDict


class AnnouncementView(TypedDict):
    id: int
    title: str
    body: str
    published_at: str


@lru_cache(maxsize=1)
def _default_announcements() -> list[dict]:
    return [
        {
            "id": 1,
            "title": "Conference 2026 CFP Open",
            "body": "Paper submission portal is now open.",
            "published_at": datetime(2026, 1, 20, 10, 0, tzinfo=timezone.utc),
            "is_public": True,
        },
        {
            "id": 2,
            "title": "Committee Update",
            "body": "Internal reviewer assignment timeline.",
            "published_at": datetime(2026, 1, 21, 10, 0, tzinfo=timezone.utc),
            "is_public": False,
        },
    ]


def list_public_announcements(records: Iterable[dict] | None = None) -> list[AnnouncementView]:
    source = list(records) if records is not None else _default_announcements()
    public_items = [item for item in source if item.get("is_public", False)]
    public_items.sort(key=lambda item: item["published_at"], reverse=True)
    return [
        {
            "id": int(item["id"]),
            "title": str(item["title"]),
            "body": str(item["body"]),
            "published_at": item["published_at"].isoformat(),
        }
        for item in public_items
    ]


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    records = data.get("records")
    announcements = list_public_announcements(records if isinstance(records, list) else None)
    return {"service": "announcements_service", "announcements": announcements}
