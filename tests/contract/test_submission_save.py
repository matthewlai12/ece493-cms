from fastapi import HTTPException

from src.api.submission_save import handle_submission_save
from src.services.audit_log import list_events, reset_events
from src.services.submission_save_service import reset_submission_save_state


def test_submission_save_endpoint() -> None:
    reset_submission_save_state()
    reset_events()

    body = handle_submission_save(
        submission_id="1",
        payload={"author_id": "author-1", "title": "Draft v2"},
    )
    assert body["service"] == "submission_save_service"
    assert body["submission"]["id"] == 1
    assert body["submission"]["status"] == "draft"
    assert list_events("submission_save")[-1]["details"]["submission_id"] == 1


def test_submission_save_endpoint_invalid_payload() -> None:
    reset_submission_save_state()
    try:
        handle_submission_save(submission_id="abc", payload={"author_id": "author-1", "title": "Draft"})
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Submission ID is invalid."
    else:
        raise AssertionError("Expected HTTPException")
