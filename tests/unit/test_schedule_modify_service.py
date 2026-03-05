from src.services.audit_log import list_events, reset_events
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_modify_service import modify_schedule, reset_schedule_modify_state


def setup_function() -> None:
    reset_schedule_generate_state()
    reset_schedule_modify_state()
    reset_events()


def test_modify_schedule_success() -> None:
    generate_schedule(
        schedule_id="20",
        accepted_submissions=[
            {"submission_id": "401", "title": "Paper 401"},
            {"submission_id": "402", "title": "Paper 402"},
        ],
        rooms=["Hall A"],
        slot_start="2026-05-10T09:00:00+00:00",
        slot_minutes=30,
    )

    modified = modify_schedule(
        schedule_id="20",
        sessions=[
            {
                "submission_id": 401,
                "title": "Paper 401",
                "room": "Hall B",
                "start_time": "2026-05-10T11:00:00+00:00",
                "end_time": "2026-05-10T11:30:00+00:00",
            },
            {
                "submission_id": 402,
                "title": "Paper 402",
                "room": "Hall B",
                "start_time": "2026-05-10T11:35:00+00:00",
                "end_time": "2026-05-10T12:05:00+00:00",
            },
        ],
        notes="Moved to Hall B",
        admin_id="admin-1",
    )

    assert modified["id"] == 20
    assert modified["sessions"][0]["room"] == "Hall B"
    assert list_events("schedule_modify")[-1]["details"]["schedule_id"] == 20


def test_modify_schedule_rejects_nonexistent_schedule() -> None:
    try:
        modify_schedule(
            schedule_id="21",
            sessions=[
                {
                    "submission_id": 500,
                    "title": "Paper 500",
                    "room": "Room 1",
                    "start_time": "2026-05-10T10:00:00+00:00",
                    "end_time": "2026-05-10T10:30:00+00:00",
                }
            ],
        )
    except ValueError as exc:
        assert str(exc) == "Selected generated schedule does not exist."
    else:
        raise AssertionError("Expected ValueError")


def test_modify_schedule_rejects_constraint_violation() -> None:
    generate_schedule(
        schedule_id="22",
        accepted_submissions=[{"submission_id": "501", "title": "Paper 501"}],
        rooms=["Hall A"],
        slot_start="2026-05-10T09:00:00+00:00",
        slot_minutes=30,
    )

    try:
        modify_schedule(
            schedule_id="22",
            sessions=[
                {
                    "submission_id": 501,
                    "title": "Paper 501",
                    "room": "Hall C",
                    "start_time": "2026-05-10T10:00:00+00:00",
                    "end_time": "2026-05-10T10:30:00+00:00",
                },
                {
                    "submission_id": 502,
                    "title": "Paper 502",
                    "room": "Hall C",
                    "start_time": "2026-05-10T10:15:00+00:00",
                    "end_time": "2026-05-10T10:45:00+00:00",
                },
            ],
        )
    except ValueError as exc:
        assert str(exc) == "Schedule conflict detected: overlapping sessions in the same room."
    else:
        raise AssertionError("Expected ValueError")
