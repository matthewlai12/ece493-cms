from src.api.schedule_generate import handle_schedule_generate
from src.api.schedule_modify import handle_schedule_modify
from src.services.schedule_generate_service import (
    get_generated_schedule,
    reset_schedule_generate_state,
)
from src.services.schedule_modify_service import reset_schedule_modify_state


def test_schedule_modify_updates_generated_schedule() -> None:
    reset_schedule_generate_state()
    reset_schedule_modify_state()

    handle_schedule_generate(
        payload={
            "schedule_id": "24",
            "accepted_submissions": [
                {"submission_id": "701", "title": "Paper 701"},
                {"submission_id": "702", "title": "Paper 702"},
            ],
            "rooms": ["Room A", "Room B"],
            "slot_start": "2026-05-12T09:00:00+00:00",
            "slot_minutes": 30,
        }
    )

    body = handle_schedule_modify(
        schedule_id="24",
        payload={
            "sessions": [
                {
                    "submission_id": 701,
                    "title": "Paper 701",
                    "room": "Room C",
                    "start_time": "2026-05-12T10:00:00+00:00",
                    "end_time": "2026-05-12T10:30:00+00:00",
                },
                {
                    "submission_id": 702,
                    "title": "Paper 702",
                    "room": "Room D",
                    "start_time": "2026-05-12T10:35:00+00:00",
                    "end_time": "2026-05-12T11:05:00+00:00",
                },
            ],
            "admin_id": "admin-2",
        },
    )
    assert body["schedule"]["id"] == 24
    saved = get_generated_schedule("24")
    assert saved is not None
    assert saved["sessions"][0]["room"] == "Room C"
    assert saved["sessions"][1]["room"] == "Room D"
