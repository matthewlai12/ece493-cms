from src.services.audit_log import list_events, reset_events
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state


def setup_function() -> None:
    reset_schedule_generate_state()
    reset_events()


def test_generate_schedule_success() -> None:
    result = generate_schedule(
        schedule_id="10",
        accepted_submissions=[
            {"submission_id": "101", "title": "Paper 101"},
            {"submission_id": "102", "title": "Paper 102"},
            {"submission_id": "103", "title": "Paper 103"},
        ],
        rooms=["Hall A", "Hall B"],
        slot_start="2026-05-07T09:00:00+00:00",
        slot_minutes=30,
        generator_id="editor-3",
    )

    assert result["id"] == 10
    assert result["status"] == "draft"
    assert len(result["sessions"]) == 3
    assert result["sessions"][0]["room"] == "Hall A"
    assert result["sessions"][1]["room"] == "Hall B"
    assert list_events("schedule_generate")[-1]["details"]["session_count"] == 3


def test_generate_schedule_requires_submissions() -> None:
    try:
        generate_schedule(
            schedule_id="11",
            accepted_submissions=[],
            rooms=["Hall A"],
            slot_start="2026-05-07T09:00:00+00:00",
            slot_minutes=30,
        )
    except ValueError as exc:
        assert str(exc) == "At least one accepted submission is required."
    else:
        raise AssertionError("Expected ValueError")


def test_generate_schedule_rejects_invalid_submission_id() -> None:
    try:
        generate_schedule(
            schedule_id="12",
            accepted_submissions=[{"submission_id": "x", "title": "Paper X"}],
            rooms=["Hall A"],
            slot_start="2026-05-07T09:00:00+00:00",
            slot_minutes=30,
        )
    except ValueError as exc:
        assert str(exc) == "Submission 1 has an invalid submission_id."
    else:
        raise AssertionError("Expected ValueError")
