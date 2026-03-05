from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state
from src.services.three_referees_service import validate_three_referees


def setup_function() -> None:
    reset_review_invite_notify_state()


def test_validate_three_referees_success() -> None:
    for index in range(3):
        create_review_invitation(
            submission_id="901",
            referee_id=f"ref-{index+1}",
            paper_title="Paper 901",
            paper_abstract="Abstract",
            referee_email=f"ref{index+1}@example.com",
        )

    result = validate_three_referees("901")
    assert result["exactly_three"] is True
    assert result["can_proceed"] is True


def test_validate_three_referees_when_missing() -> None:
    create_review_invitation(
        submission_id="902",
        referee_id="ref-1",
        paper_title="Paper 902",
        paper_abstract="Abstract",
        referee_email="ref1@example.com",
    )

    result = validate_three_referees("902")
    assert result["exactly_three"] is False
    assert result["missing"] == 2
