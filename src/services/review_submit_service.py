from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event

_reviews: list[dict[str, Any]] = []


class ReviewResult(TypedDict):
    id: int
    submission_id: int
    referee_id: str
    score: int
    comments: str
    status: str
    submitted_at: str


def submit_review(submission_id: str, referee_id: str, score: int, comments: str) -> ReviewResult:
    if not str(submission_id).isdigit() or int(submission_id) <= 0:
        raise ValueError("Submission ID is invalid.")
    if not referee_id.strip():
        raise ValueError("Referee ID is required.")
    if score < 1 or score > 5:
        raise ValueError("Score must be between 1 and 5.")
    if not comments.strip():
        raise ValueError("Comments are required.")

    review: ReviewResult = {
        "id": len(_reviews) + 1,
        "submission_id": int(submission_id),
        "referee_id": referee_id.strip(),
        "score": int(score),
        "comments": comments.strip(),
        "status": "submitted",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }
    _reviews.append(review)
    record_event("review_submit", actor=review["referee_id"], details={"review_id": review["id"]})
    return review


def list_submitted_reviews(submission_id: str = "") -> list[ReviewResult]:
    if submission_id and str(submission_id).isdigit():
        sid = int(submission_id)
        return [dict(item) for item in _reviews if int(item["submission_id"]) == sid]
    return [dict(item) for item in _reviews]


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    review = submit_review(
        submission_id=str(data.get("submission_id", "")),
        referee_id=str(data.get("referee_id", "")),
        score=int(data.get("score", 0)),
        comments=str(data.get("comments", "")),
    )
    return {"service": "review_submit_service", "review": review}


def reset_review_submit_state() -> None:
    _reviews.clear()
