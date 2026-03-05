from src.api.three_referees import handle_three_referees
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state


def test_three_referees_endpoint_detects_excess() -> None:
    reset_review_invite_notify_state()
    for index in range(4):
        create_review_invitation(
            submission_id="904",
            referee_id=f"ref-{index+1}",
            paper_title="Paper 904",
            paper_abstract="Abstract",
            referee_email=f"ref{index+1}@example.com",
        )

    body = handle_three_referees(payload={"submission_id": "904"})
    assert body["exactly_three"] is False
    assert body["excess"] == 1
