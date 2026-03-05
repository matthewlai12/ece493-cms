from src.api.schedule_generate import handle_schedule_generate
from src.api.schedule_publish import handle_schedule_publish
from src.api.schedule_view_attendee import handle_schedule_view_attendee
from src.services.schedule_generate_service import reset_schedule_generate_state
from src.services.schedule_publish_service import reset_schedule_publish_state


def setup_function() -> None:
    reset_schedule_generate_state()
    reset_schedule_publish_state()


def test_schedule_view_attendee_flow_returns_latest_published_schedule() -> None:
    handle_schedule_generate(
        payload={
            "schedule_id": "43",
            "accepted_submissions": [{"submission_id": "1301", "title": "Paper 1301"}],
            "rooms": ["Hall C"],
            "slot_start": "2026-05-22T09:00:00+00:00",
            "slot_minutes": 30,
        }
    )
    handle_schedule_publish(schedule_id="43", payload={"finalized": True, "recipients": []})

    handle_schedule_generate(
        payload={
            "schedule_id": "44",
            "accepted_submissions": [{"submission_id": "1302", "title": "Paper 1302"}],
            "rooms": ["Hall D"],
            "slot_start": "2026-05-23T09:00:00+00:00",
            "slot_minutes": 30,
        }
    )
    handle_schedule_publish(schedule_id="44", payload={"finalized": True, "recipients": []})

    body = handle_schedule_view_attendee()
    assert len(body["schedules"]) == 2
    assert body["schedules"][0]["id"] == 44
    assert body["schedules"][1]["id"] == 43
