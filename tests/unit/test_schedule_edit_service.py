from src.services.audit_log import list_events, reset_events
from src.services.schedule_edit_service import edit_schedule, reset_schedule_edit_state


def setup_function() -> None:
    reset_schedule_edit_state()
    reset_events()


def test_edit_schedule_success() -> None:
    result = edit_schedule(
        schedule_id="5",
        sessions=[
            {
                "title": "Keynote",
                "room": "Hall A",
                "start_time": "2026-05-04T09:00:00+00:00",
                "end_time": "2026-05-04T10:00:00+00:00",
            },
            {
                "title": "Session 1",
                "room": "Hall A",
                "start_time": "2026-05-04T10:15:00+00:00",
                "end_time": "2026-05-04T11:15:00+00:00",
            },
        ],
        notes="Adjusted breaks",
        editor_id="editor-1",
    )

    assert result["id"] == 5
    assert result["status"] == "draft"
    assert len(result["sessions"]) == 2
    assert list_events("schedule_edit")[-1]["details"]["session_count"] == 2


def test_edit_schedule_rejects_room_conflicts() -> None:
    try:
        edit_schedule(
            schedule_id="6",
            sessions=[
                {
                    "title": "Session A",
                    "room": "Room 100",
                    "start_time": "2026-05-04T09:00:00+00:00",
                    "end_time": "2026-05-04T10:00:00+00:00",
                },
                {
                    "title": "Session B",
                    "room": "Room 100",
                    "start_time": "2026-05-04T09:30:00+00:00",
                    "end_time": "2026-05-04T10:30:00+00:00",
                },
            ],
        )
    except ValueError as exc:
        assert str(exc) == "Schedule conflict detected: overlapping sessions in the same room."
    else:
        raise AssertionError("Expected ValueError")


def test_edit_schedule_requires_valid_time_window() -> None:
    try:
        edit_schedule(
            schedule_id="7",
            sessions=[
                {
                    "title": "Invalid Session",
                    "room": "Room 200",
                    "start_time": "2026-05-04T11:00:00+00:00",
                    "end_time": "2026-05-04T10:00:00+00:00",
                }
            ],
        )
    except ValueError as exc:
        assert str(exc) == "Session 1 start_time must be earlier than end_time."
    else:
        raise AssertionError("Expected ValueError")
