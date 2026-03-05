from src.api.review_submit import handle_review_submit
from src.services.review_submit_service import list_submitted_reviews, reset_review_submit_state


def test_review_submit_endpoint() -> None:
    reset_review_submit_state()
    body = handle_review_submit(
        payload={
            "submission_id": "1",
            "referee_id": "ref-2",
            "score": 5,
            "comments": "excellent",
        }
    )
    assert body["service"] == "review_submit_service"

    reviews = list_submitted_reviews("1")
    assert len(reviews) == 1
    assert reviews[0]["comments"] == "excellent"
