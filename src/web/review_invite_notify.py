from fastapi import APIRouter
from fastapi import Body, Query

from src.services.review_invite_notify_service import execute

router = APIRouter(tags=["web-review_invite_notify"])


@router.get("/review-invite-notify")
@router.get("/review_invite_notify")
def page_review_invite_notify(referee_id: str | None = Query(default=None)) -> dict:
    payload: dict[str, str] = {}
    if referee_id is not None:
        payload["referee_id"] = referee_id
    return {
        "page": "review_invite_notify",
        "invitations": execute(payload).get("invitations", []),
        "fields": ["submission_id", "referee_id", "paper_title", "paper_abstract", "referee_email"],
        "submit_to": "/web/review-invite-notify",
    }


@router.post("/review-invite-notify")
def submit_review_invite_notify(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
