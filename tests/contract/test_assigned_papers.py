from src.api.assigned_papers import handle_assigned_papers
from src.services.manuscript_upload_service import reset_manuscript_upload_state, upload_manuscript
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state
from src.services.review_invite_response_service import respond_to_review_invitation


def test_assigned_papers_endpoint() -> None:
    reset_review_invite_notify_state()
    reset_manuscript_upload_state()

    invitation = create_review_invitation(
        submission_id="701",
        referee_id="ref-701",
        paper_title="Paper 701",
        paper_abstract="Abstract",
        referee_email="ref701@example.com",
    )["invitation"]
    respond_to_review_invitation(str(invitation["id"]), "accept")
    upload_manuscript("701", "paper701.pdf", "application/pdf", b"content")

    body = handle_assigned_papers(referee_id="ref-701")
    assert body["service"] == "assigned_papers_service"
    assert len(body["assignments"]) == 1
