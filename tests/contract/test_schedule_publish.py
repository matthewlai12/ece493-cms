from fastapi import HTTPException

from src.api.schedule_publish import handle_schedule_publish
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_publish_service import reset_schedule_publish_state


def test_schedule_publish_endpoint() -> None:
    reset_schedule_generate_state()
    reset_schedule_publish_state()
    generate_schedule(
        schedule_id="33",
        accepted_submissions=[{"submission_id": "901", "title": "Paper 901"}],
        rooms=["Hall Z"],
        slot_start="2026-05-14T09:00:00+00:00",
        slot_minutes=30,
    )

    body = handle_schedule_publish(
        schedule_id="33",
        payload={
            "finalized": True,
            "recipients": ["author901@example.com"],
        },
    )

    assert body["service"] == "schedule_publish_service"
    assert body["schedule"]["id"] == 33
    assert body["schedule"]["status"] == "published"


def test_schedule_publish_endpoint_invalid_payload() -> None:
    reset_schedule_generate_state()
    reset_schedule_publish_state()
    try:
        handle_schedule_publish(schedule_id="x", payload={"finalized": True, "recipients": []})
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Schedule ID is invalid."
    else:
        raise AssertionError("Expected HTTPException")
