from fastapi import APIRouter
from fastapi import Query

from src.services.review_access_service import execute

router = APIRouter(tags=["web-review_access"])


@router.get("/review-access")
@router.get("/review_access")
def page_review_access(editor_id: str | None = Query(default=None), submission_id: str | None = Query(default=None)) -> dict:
    if editor_id is None:
        return {
            "page": "review_access",
            "fields": ["editor_id", "submission_id"],
            "query_required": "editor_id",
        }
    payload: dict[str, str] = {"editor_id": editor_id}
    if submission_id is not None:
        payload["submission_id"] = submission_id
    result = execute(payload)
    return {
        "page": "review_access",
        "reviews": result.get("reviews", []),
        "message": result.get("message", ""),
    }
