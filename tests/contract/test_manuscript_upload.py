from src.api.manuscript_upload import handle_manuscript_upload
from src.services.audit_log import list_events, reset_events
from src.services.manuscript_upload_service import reset_manuscript_upload_state


def test_manuscript_upload_endpoint() -> None:
    reset_manuscript_upload_state()
    reset_events()

    body = handle_manuscript_upload(
        submission_id="1",
        payload={
            "filename": "paper.pdf",
            "content_type": "application/pdf",
            "content": "mock binary content",
        },
    )

    assert body["service"] == "manuscript_upload_service"
    assert body["file"]["submission_id"] == 1
    assert body["file"]["filename"] == "paper.pdf"
    assert list_events("manuscript_upload")
