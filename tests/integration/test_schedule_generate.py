from src.api.schedule_generate import handle_schedule_generate
from src.services.schedule_generate_service import (
    get_generated_schedule,
    reset_schedule_generate_state,
)


def test_schedule_generate_persists_schedule() -> None:
    reset_schedule_generate_state()

    body = handle_schedule_generate(
        payload={
            "schedule_id": "14",
            "accepted_submissions": [
                {"submission_id": "301", "title": "Networking Paper"},
                {"submission_id": "302", "title": "Security Paper"},
                {"submission_id": "303", "title": "ML Paper"},
            ],
            "rooms": ["Hall X", "Hall Y"],
            "slot_start": "2026-05-09T10:00:00+00:00",
            "slot_minutes": 30,
        }
    )

    assert body["schedule"]["id"] == 14
    saved = get_generated_schedule("14")
    assert saved is not None
    assert len(saved["sessions"]) == 3
    assert saved["sessions"][2]["room"] == "Hall X"
