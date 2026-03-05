from fastapi import HTTPException

from src.api.schedule_generate import handle_schedule_generate
from src.services.schedule_generate_service import reset_schedule_generate_state


def test_schedule_generate_endpoint() -> None:
    reset_schedule_generate_state()

    body = handle_schedule_generate(
        payload={
            "schedule_id": "13",
            "accepted_submissions": [
                {"submission_id": "201", "title": "AI Paper"},
                {"submission_id": "202", "title": "Systems Paper"},
            ],
            "rooms": ["Room 1", "Room 2"],
            "slot_start": "2026-05-08T09:00:00+00:00",
            "slot_minutes": 45,
        }
    )
    assert body["service"] == "schedule_generate_service"
    assert body["schedule"]["id"] == 13
    assert len(body["schedule"]["sessions"]) == 2


def test_schedule_generate_endpoint_invalid_payload() -> None:
    reset_schedule_generate_state()
    try:
        handle_schedule_generate(
            payload={
                "schedule_id": "13",
                "accepted_submissions": [],
                "rooms": ["Room 1"],
                "slot_start": "2026-05-08T09:00:00+00:00",
                "slot_minutes": 45,
            }
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "At least one accepted submission is required."
    else:
        raise AssertionError("Expected HTTPException")
