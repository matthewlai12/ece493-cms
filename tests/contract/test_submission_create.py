from src.api.submission_create import handle_submission_create
from src.services.audit_log import list_events, reset_events
from src.services.submission_create_service import reset_submission_create_state


def test_submission_create_endpoint() -> None:
    reset_submission_create_state()
    reset_events()
    body = handle_submission_create(
        {
            "author_id": "author-1",
            "title": "Paper",
            "abstract": "Paper abstract",
            "manuscript_format": "pdf",
        }
    )
    assert body["service"] == "submission_create_service"
    assert body["submission"]["status"] == "submitted"
    assert list_events("submission_create")
