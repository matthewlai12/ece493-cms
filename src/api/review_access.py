from fastapi import APIRouter, HTTPException, Query

from src.services.review_access_service import execute

router = APIRouter(tags=["review_access"])


@router.get("/review-access")
def handle_review_access(
    editor_id: str | None = Query(default=None),
    submission_id: str | None = Query(default=None),
) -> dict:
    data: dict = {}
    if editor_id is not None:
        data["editor_id"] = editor_id
    if submission_id is not None:
        data["submission_id"] = submission_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
