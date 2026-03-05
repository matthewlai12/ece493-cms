from src.api.schedule_generate import handle_schedule_generate
from src.api.schedule_publish import handle_schedule_publish
from src.services.schedule_publish_service import get_published_schedule, reset_schedule_publish_state


def test_schedule_publish_makes_schedule_accessible() -> None:
    reset_schedule_publish_state()
    handle_schedule_generate(
        payload={
            "schedule_id": "34",
            "accepted_submissions": [
                {"submission_id": "1001", "title": "Paper 1001"},
                {"submission_id": "1002", "title": "Paper 1002"},
            ],
            "rooms": ["Room M", "Room N"],
            "slot_start": "2026-05-15T09:00:00+00:00",
            "slot_minutes": 30,
        }
    )

    body = handle_schedule_publish(
        schedule_id="34",
        payload={
            "finalized": True,
            "recipients": ["author1001@example.com", ""],
        },
    )
    assert body["schedule"]["status"] == "published"
    assert body["failed_count"] == 1

    published = get_published_schedule("34")
    assert published is not None
    assert published["public_url"] == "/web/schedule/34"
    assert len(published["sessions"]) == 2
