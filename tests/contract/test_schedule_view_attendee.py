from fastapi import HTTPException

from src.api.schedule_generate import handle_schedule_generate
from src.api.schedule_publish import handle_schedule_publish
from src.api.schedule_view_attendee import handle_schedule_view_attendee
from src.services.schedule_generate_service import reset_schedule_generate_state
from src.services.schedule_publish_service import reset_schedule_publish_state


def setup_function() -> None:
    reset_schedule_generate_state()
    reset_schedule_publish_state()


def test_schedule_view_attendee_endpoint() -> None:
    handle_schedule_generate(
        payload={
            "schedule_id": "42",
            "accepted_submissions": [{"submission_id": "1201", "title": "Paper 1201"}],
            "rooms": ["Hall B"],
            "slot_start": "2026-05-21T09:00:00+00:00",
            "slot_minutes": 30,
        }
    )
    handle_schedule_publish(schedule_id="42", payload={"finalized": True, "recipients": []})

    body = handle_schedule_view_attendee()
    assert body["service"] == "schedule_view_attendee_service"
    assert body["schedules"][0]["id"] == 42


def test_schedule_view_attendee_endpoint_auth_required() -> None:
    try:
        handle_schedule_view_attendee(require_auth=True, is_authenticated=False)
    except HTTPException as exc:
        assert exc.status_code == 401
        assert exc.detail == "Authentication required to view attendee schedule."
    else:
        raise AssertionError("Expected HTTPException")
