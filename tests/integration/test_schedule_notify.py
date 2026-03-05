from src.api.schedule_notify import handle_schedule_notify
from src.services.schedule_notify_service import (
    assign_presentation_slot,
    get_presentation_slot,
    reset_schedule_notify_state,
)


def test_schedule_notify_uses_published_slot() -> None:
    reset_schedule_notify_state()
    assign_presentation_slot(
        submission_id="22",
        title="Paper 22",
        room="Room 102",
        start_time="2026-05-04T10:00:00+00:00",
        end_time="2026-05-04T10:30:00+00:00",
    )

    body = handle_schedule_notify(payload={"submission_id": "22", "author_email": "author22@example.com"})
    assert body["notified"] is True
    slot = get_presentation_slot("22")
    assert slot is not None
    assert slot["room"] == "Room 102"
