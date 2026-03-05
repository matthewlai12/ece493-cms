from src.services.schedule_notify_service import (
    assign_presentation_slot,
    notify_schedule,
    reset_schedule_notify_state,
)


def setup_function() -> None:
    reset_schedule_notify_state()


def test_notify_schedule_success() -> None:
    assign_presentation_slot(
        submission_id="12",
        title="Accepted Paper",
        room="Hall B",
        start_time="2026-05-03T10:00:00+00:00",
        end_time="2026-05-03T10:30:00+00:00",
    )
    result = notify_schedule("12", "author12@example.com")

    assert result["notified"] is True
    assert result["slot"]["submission_id"] == 12
    assert result["recipient"] == "author12@example.com"


def test_notify_schedule_delivery_failure_is_safe() -> None:
    assign_presentation_slot(
        submission_id="13",
        title="Accepted Paper",
        room="Hall C",
        start_time="2026-05-03T11:00:00+00:00",
        end_time="2026-05-03T11:30:00+00:00",
    )
    result = notify_schedule("13", "")

    assert result["notified"] is False
    assert result["message"] == "Schedule delivery failed."
