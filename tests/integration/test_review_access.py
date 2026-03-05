from src.api.review_access import handle_review_access
from src.services.review_submit_service import reset_review_submit_state


def test_review_access_endpoint_when_no_completed_reviews() -> None:
    reset_review_submit_state()
    body = handle_review_access(editor_id="editor-2", submission_id="1201")
    assert body["reviews"] == []
    assert body["message"] == "No completed reviews are available."
