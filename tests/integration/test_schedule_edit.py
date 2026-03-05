from src.api.schedule_edit import handle_schedule_edit
from src.services.schedule_edit_service import get_schedule, reset_schedule_edit_state


def test_schedule_edit_persists_updated_schedule() -> None:
    reset_schedule_edit_state()

    body = handle_schedule_edit(
        schedule_id="9",
        payload={
            "sessions": [
                {
                    "title": "Panel A",
                    "room": "Hall C",
                    "start_time": "2026-05-06T09:00:00+00:00",
                    "end_time": "2026-05-06T10:00:00+00:00",
                },
                {
                    "title": "Panel B",
                    "room": "Hall C",
                    "start_time": "2026-05-06T10:15:00+00:00",
                    "end_time": "2026-05-06T11:15:00+00:00",
                },
            ],
            "editor_id": "editor-2",
        },
    )
    assert body["schedule"]["id"] == 9

    saved = get_schedule("9")
    assert saved is not None
    assert len(saved["sessions"]) == 2
    assert saved["sessions"][1]["title"] == "Panel B"
