from src.api.review_access import handle_review_access
from src.services.review_submit_service import reset_review_submit_state, submit_review


def test_review_access_endpoint() -> None:
    reset_review_submit_state()
    submit_review("1101", "ref-1", 4, "Solid")

    body = handle_review_access(editor_id="editor-1", submission_id="1101")
    assert body["service"] == "review_access_service"
    assert len(body["reviews"]) == 1
