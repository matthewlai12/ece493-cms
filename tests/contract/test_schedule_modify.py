from fastapi import HTTPException

from src.api.schedule_modify import handle_schedule_modify
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_modify_service import reset_schedule_modify_state


def test_schedule_modify_endpoint() -> None:
    reset_schedule_generate_state()
    reset_schedule_modify_state()
    generate_schedule(
        schedule_id="23",
        accepted_submissions=[{"submission_id": "601", "title": "Paper 601"}],
        rooms=["Room 1"],
        slot_start="2026-05-11T09:00:00+00:00",
        slot_minutes=30,
    )

    body = handle_schedule_modify(
        schedule_id="23",
        payload={
            "sessions": [
                {
                    "submission_id": 601,
                    "title": "Paper 601",
                    "room": "Room 2",
                    "start_time": "2026-05-11T10:00:00+00:00",
                    "end_time": "2026-05-11T10:30:00+00:00",
                }
            ],
            "notes": "Room update",
        },
    )

    assert body["service"] == "schedule_modify_service"
    assert body["schedule"]["id"] == 23
    assert body["schedule"]["sessions"][0]["room"] == "Room 2"


def test_schedule_modify_endpoint_invalid_payload() -> None:
    reset_schedule_generate_state()
    reset_schedule_modify_state()
    try:
        handle_schedule_modify(schedule_id="x", payload={"sessions": []})
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Schedule ID is invalid."
    else:
        raise AssertionError("Expected HTTPException")
