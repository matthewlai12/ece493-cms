from src.api.review_invite_notify import handle_review_invite_notify
from src.services.review_invite_notify_service import execute, reset_review_invite_notify_state


def test_review_invite_notify_endpoint_lists_referee_invitations() -> None:
    reset_review_invite_notify_state()
    execute(
        {
            "submission_id": "7",
            "referee_id": "ref-7",
            "paper_title": "Paper 7",
            "paper_abstract": "Abstract",
            "referee_email": "ref7@example.com",
        }
    )

    body = handle_review_invite_notify(referee_id="ref-7")
    assert body["service"] == "review_invite_notify_service"
    assert len(body["invitations"]) == 1
    assert body["invitations"][0]["submission_id"] == 7
