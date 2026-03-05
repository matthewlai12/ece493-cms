from fastapi import HTTPException

from src.api.manuscript_upload import handle_manuscript_upload
from src.services.manuscript_upload_service import reset_manuscript_upload_state


def test_manuscript_upload_endpoint() -> None:
    reset_manuscript_upload_state()

    body = handle_manuscript_upload(
        submission_id="1",
        payload={
            "filename": "paper.pdf",
            "content_type": "application/pdf",
            "content": "mock binary content",
        },
    )
    assert body["file"]["content_type"] == "application/pdf"

    try:
        handle_manuscript_upload(
            submission_id="1",
            payload={
                "filename": "paper.exe",
                "content_type": "application/x-msdownload",
                "content": "bad",
            },
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "File format is not supported."
    else:
        raise AssertionError("Expected HTTPException")
