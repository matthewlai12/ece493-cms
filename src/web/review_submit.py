from fastapi import APIRouter
from fastapi import Body

from src.services.review_submit_service import execute

router = APIRouter(tags=["web-review_submit"])


@router.get("/review-submit")
@router.get("/review_submit")
def page_review_submit() -> dict:
    return {
        "page": "review_submit",
        "fields": ["submission_id", "referee_id", "score", "comments"],
        "submit_to": "/api/reviews",
        "method": "POST",
    }


@router.post("/review-submit")
def submit_review_submit(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
