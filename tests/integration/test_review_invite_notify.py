from src.api.review_invite_notify import handle_review_invite_notify
from src.services.review_invite_notify_service import execute, reset_review_invite_notify_state


def test_review_invite_notify_shows_safe_outcome_at_limit() -> None:
    reset_review_invite_notify_state()
    for index in range(5):
        execute(
            {
                "submission_id": str(index + 1),
                "referee_id": "ref-limit",
                "paper_title": f"Paper {index + 1}",
                "paper_abstract": "Abstract",
                "referee_email": "limit@example.com",
            }
        )

    blocked = execute(
        {
            "submission_id": "6",
            "referee_id": "ref-limit",
            "paper_title": "Overflow Paper",
            "paper_abstract": "Abstract",
            "referee_email": "limit@example.com",
        }
    )
    assert blocked["blocked"] is True
    assert "maximum allowed number" in blocked["message"]

    listed = handle_review_invite_notify(referee_id="ref-limit")
    assert len(listed["invitations"]) == 5
