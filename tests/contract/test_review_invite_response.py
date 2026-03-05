from src.api.review_invite_response import handle_review_invite_response
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state


def test_review_invite_response_endpoint_accepts() -> None:
    reset_review_invite_notify_state()
    created = create_review_invitation(
        submission_id="401",
        referee_id="ref-401",
        paper_title="Paper 401",
        paper_abstract="Abstract",
        referee_email="ref401@example.com",
    )

    body = handle_review_invite_response(
        invitation_id=str(created["invitation"]["id"]),
        payload={"response": "accept"},
    )
    assert body["service"] == "review_invite_response_service"
    assert body["invitation"]["status"] == "accepted"
