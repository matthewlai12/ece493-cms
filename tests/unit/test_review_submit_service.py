from src.services.audit_log import list_events, reset_events
from src.services.review_submit_service import reset_review_submit_state, submit_review


def setup_function() -> None:
    reset_review_submit_state()
    reset_events()


def test_submit_review_success() -> None:
    review = submit_review(
        submission_id="1",
        referee_id="ref-1",
        score=4,
        comments="Good work",
    )
    assert review["status"] == "submitted"
    assert review["score"] == 4
    assert list_events("review_submit")[-1]["details"]["review_id"] == 1


def test_submit_review_rejects_invalid_score() -> None:
    try:
        submit_review(
            submission_id="1",
            referee_id="ref-1",
            score=7,
            comments="Too high score",
        )
    except ValueError as exc:
        assert str(exc) == "Score must be between 1 and 5."
    else:
        raise AssertionError("Expected ValueError")
