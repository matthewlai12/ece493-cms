from fastapi import HTTPException

from src.api.review_submit import handle_review_submit
from src.services.review_submit_service import reset_review_submit_state


def test_review_submit_endpoint() -> None:
    reset_review_submit_state()
    body = handle_review_submit(
        payload={
            "submission_id": "1",
            "referee_id": "ref-1",
            "score": 4,
            "comments": "good",
        }
    )
    assert body["service"] == "review_submit_service"
    assert body["review"]["status"] == "submitted"


def test_review_submit_endpoint_invalid_payload() -> None:
    reset_review_submit_state()
    try:
        handle_review_submit(
            payload={
                "submission_id": "1",
                "referee_id": "ref-1",
                "score": 9,
                "comments": "invalid",
            }
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Score must be between 1 and 5."
    else:
        raise AssertionError("Expected HTTPException")
