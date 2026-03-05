from src.api.referee_assign import handle_referee_assign
from src.services.review_invite_notify_service import list_review_invitations, reset_review_invite_notify_state


def test_referee_assign_endpoint() -> None:
    reset_review_invite_notify_state()
    body = handle_referee_assign(
        payload={
            "submission_id": "1",
            "referee_id": "ref-1",
            "paper_title": "Paper 1",
            "paper_abstract": "Abstract",
            "referee_email": "ref1@example.com",
            "assigned_by": "chair",
        }
    )
    assert body["service"] == "referee_assign_service"
    invitations = list_review_invitations("ref-1")
    assert len(invitations) == 1
