from fastapi import HTTPException

from src.api.schedule_edit import handle_schedule_edit
from src.services.audit_log import list_events, reset_events
from src.services.schedule_edit_service import reset_schedule_edit_state


def test_schedule_edit_endpoint() -> None:
    reset_schedule_edit_state()
    reset_events()

    body = handle_schedule_edit(
        schedule_id="8",
        payload={
            "sessions": [
                {
                    "title": "Workshop",
                    "room": "Room 301",
                    "start_time": "2026-05-05T13:00:00+00:00",
                    "end_time": "2026-05-05T14:00:00+00:00",
                }
            ],
            "notes": "Updated workshop timing",
        },
    )

    assert body["service"] == "schedule_edit_service"
    assert body["schedule"]["id"] == 8
    assert body["schedule"]["sessions"][0]["title"] == "Workshop"
    assert list_events("schedule_edit")[-1]["details"]["schedule_id"] == 8


def test_schedule_edit_endpoint_invalid_payload() -> None:
    reset_schedule_edit_state()

    try:
        handle_schedule_edit(schedule_id="x", payload={"sessions": []})
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Schedule ID is invalid."
    else:
        raise AssertionError("Expected HTTPException")
