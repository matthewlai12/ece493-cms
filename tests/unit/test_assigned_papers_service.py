from src.services.assigned_papers_service import list_assigned_papers
from src.services.manuscript_upload_service import reset_manuscript_upload_state, upload_manuscript
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state
from src.services.review_invite_response_service import respond_to_review_invitation


def setup_function() -> None:
    reset_review_invite_notify_state()
    reset_manuscript_upload_state()


def test_list_assigned_papers_returns_manuscript_access() -> None:
    invitation = create_review_invitation(
        submission_id="601",
        referee_id="ref-601",
        paper_title="Paper 601",
        paper_abstract="Abstract",
        referee_email="ref601@example.com",
    )["invitation"]
    respond_to_review_invitation(str(invitation["id"]), "accept")
    upload_manuscript("601", "paper601.pdf", "application/pdf", b"pdf")

    assignments = list_assigned_papers("ref-601")
    assert len(assignments) == 1
    assert assignments[0]["paper_title"] == "Paper 601"
    assert assignments[0]["manuscript_files"][0]["filename"] == "paper601.pdf"


def test_list_assigned_papers_safe_when_none_assigned() -> None:
    create_review_invitation(
        submission_id="602",
        referee_id="ref-602",
        paper_title="Paper 602",
        paper_abstract="Abstract",
        referee_email="ref602@example.com",
    )

    assignments = list_assigned_papers("ref-602")
    assert assignments == []
