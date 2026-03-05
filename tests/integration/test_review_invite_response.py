from src.api.review_invite_response import handle_review_invite_response
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state


def test_review_invite_response_records_rejection() -> None:
    reset_review_invite_notify_state()
    created = create_review_invitation(
        submission_id="501",
        referee_id="ref-501",
        paper_title="Paper 501",
        paper_abstract="Abstract",
        referee_email="ref501@example.com",
    )

    body = handle_review_invite_response(
        invitation_id=str(created["invitation"]["id"]),
        payload={"response": "reject"},
    )
    assert body["updated"] is True
    assert body["invitation"]["status"] == "rejected"
