from src.api.assigned_papers import handle_assigned_papers
from src.services.manuscript_upload_service import reset_manuscript_upload_state
from src.services.review_invite_notify_service import reset_review_invite_notify_state


def test_assigned_papers_endpoint_when_none_assigned() -> None:
    reset_review_invite_notify_state()
    reset_manuscript_upload_state()

    body = handle_assigned_papers(referee_id="ref-empty")
    assert body["assignments"] == []
    assert body["message"] == "No papers are currently assigned to this referee."
