from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_publish_service import publish_schedule, reset_schedule_publish_state
from src.services.schedule_view_attendee_service import execute


def setup_function() -> None:
    reset_schedule_generate_state()
    reset_schedule_publish_state()


def test_schedule_view_attendee_returns_published_schedule() -> None:
    generate_schedule(
        schedule_id="41",
        accepted_submissions=[{"submission_id": "1101", "title": "Paper 1101"}],
        rooms=["Hall A"],
        slot_start="2026-05-20T09:00:00+00:00",
        slot_minutes=30,
    )
    publish_schedule(schedule_id="41", finalized=True, recipients=[])

    body = execute({})
    assert body["service"] == "schedule_view_attendee_service"
    assert len(body["schedules"]) == 1
    assert body["schedules"][0]["id"] == 41


def test_schedule_view_attendee_requires_auth_when_configured() -> None:
    try:
        execute({"require_auth": True, "is_authenticated": False})
    except ValueError as exc:
        assert str(exc) == "Authentication required to view attendee schedule."
    else:
        raise AssertionError("Expected ValueError")


def test_schedule_view_attendee_handles_unpublished_schedule() -> None:
    body = execute({})
    assert body["schedules"] == []
    assert body["message"] == "Conference schedule has not been published yet."
