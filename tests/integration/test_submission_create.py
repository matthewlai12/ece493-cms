from fastapi import HTTPException

from src.api.submission_create import handle_submission_create
from src.services.submission_create_service import reset_submission_create_state


def test_submission_create_endpoint() -> None:
    reset_submission_create_state()
    body = handle_submission_create(
        {
            "author_id": "author-1",
            "title": "Paper",
            "abstract": "Paper abstract",
            "manuscript_format": "pdf",
        }
    )
    assert body["submission"]["status"] == "submitted"

    try:
        handle_submission_create(
            {
                "author_id": "author-1",
                "title": "Paper",
                "abstract": "Paper abstract",
                "manuscript_format": "exe",
            }
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Uploaded file format is not supported."
    else:
        raise AssertionError("Expected HTTPException")
