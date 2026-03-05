from src.api.schedule_notify import handle_schedule_notify
from src.services.schedule_notify_service import assign_presentation_slot, reset_schedule_notify_state


def test_schedule_notify_endpoint() -> None:
    reset_schedule_notify_state()
    assign_presentation_slot(
        submission_id="21",
        title="Paper 21",
        room="Room 101",
        start_time="2026-05-04T09:00:00+00:00",
        end_time="2026-05-04T09:30:00+00:00",
    )

    body = handle_schedule_notify(payload={"submission_id": "21", "author_email": "author21@example.com"})
    assert body["service"] == "schedule_notify_service"
    assert body["notified"] is True
    assert body["slot"]["submission_id"] == 21
