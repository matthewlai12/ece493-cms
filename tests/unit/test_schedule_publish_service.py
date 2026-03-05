from src.services.audit_log import list_events, reset_events
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_publish_service import (
    get_published_schedule,
    publish_schedule,
    reset_schedule_publish_state,
)


def setup_function() -> None:
    reset_schedule_generate_state()
    reset_schedule_publish_state()
    reset_events()


def test_publish_schedule_success() -> None:
    generate_schedule(
        schedule_id="30",
        accepted_submissions=[{"submission_id": "801", "title": "Paper 801"}],
        rooms=["Main Hall"],
        slot_start="2026-05-13T09:00:00+00:00",
        slot_minutes=30,
    )

    result = publish_schedule(
        schedule_id="30",
        finalized=True,
        recipients=["author801@example.com", "attendee1@example.com"],
        publisher_id="admin-3",
    )

    assert result["schedule"]["status"] == "published"
    assert result["sent_count"] == 2
    assert result["failed_count"] == 0
    assert get_published_schedule("30") is not None
    assert list_events("schedule_publish")[-1]["details"]["schedule_id"] == 30


def test_publish_schedule_requires_finalized_flag() -> None:
    generate_schedule(
        schedule_id="31",
        accepted_submissions=[{"submission_id": "802", "title": "Paper 802"}],
        rooms=["Main Hall"],
        slot_start="2026-05-13T10:00:00+00:00",
        slot_minutes=30,
    )

    try:
        publish_schedule(
            schedule_id="31",
            finalized=False,
            recipients=["author802@example.com"],
        )
    except ValueError as exc:
        assert str(exc) == "Selected schedule is not finalized."
    else:
        raise AssertionError("Expected ValueError")


def test_publish_schedule_keeps_publication_on_notification_failure() -> None:
    generate_schedule(
        schedule_id="32",
        accepted_submissions=[{"submission_id": "803", "title": "Paper 803"}],
        rooms=["Main Hall"],
        slot_start="2026-05-13T11:00:00+00:00",
        slot_minutes=30,
    )

    result = publish_schedule(
        schedule_id="32",
        finalized=True,
        recipients=["", "attendee2@example.com"],
    )

    assert result["schedule"]["status"] == "published"
    assert result["sent_count"] == 1
    assert result["failed_count"] == 1
    assert result["message"] == "Schedule published; some notifications failed."
    assert get_published_schedule("32") is not None
