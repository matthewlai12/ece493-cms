from src.services.review_access_service import access_completed_reviews
from src.services.review_submit_service import reset_review_submit_state, submit_review


def setup_function() -> None:
    reset_review_submit_state()


def test_access_completed_reviews_returns_submitted_forms() -> None:
    submit_review("1001", "ref-1", 4, "Good")
    submit_review("1001", "ref-2", 5, "Great")

    result = access_completed_reviews(editor_id="editor-1", submission_id="1001")
    assert len(result["reviews"]) == 2
    assert result["message"] == "Completed review forms retrieved."


def test_access_completed_reviews_safe_when_none_available() -> None:
    result = access_completed_reviews(editor_id="editor-1", submission_id="1002")
    assert result["reviews"] == []
    assert result["message"] == "No completed reviews are available."
