from typing import Any

from src.services.review_submit_service import list_submitted_reviews


def access_completed_reviews(editor_id: str, submission_id: str = "") -> dict[str, Any]:
    if not editor_id.strip():
        raise ValueError("Editor ID is required.")
    reviews = list_submitted_reviews(submission_id=submission_id)
    message = "Completed review forms retrieved." if reviews else "No completed reviews are available."
    return {"editor_id": editor_id.strip(), "reviews": reviews, "message": message}


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = access_completed_reviews(
        editor_id=str(data.get("editor_id", "")),
        submission_id=str(data.get("submission_id", "")),
    )
    return {"service": "review_access_service", **result}
