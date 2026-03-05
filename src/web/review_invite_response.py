from fastapi import APIRouter
from fastapi import Body

from src.services.review_invite_response_service import execute

router = APIRouter(tags=["web-review_invite_response"])


@router.get("/review-invite-response")
@router.get("/review_invite_response")
def page_review_invite_response() -> dict:
    return {
        "page": "review_invite_response",
        "fields": ["response"],
        "submit_to_template": "/api/referee/invitations/{invitation_id}/response",
        "method": "POST",
    }


@router.post("/review-invite-response/{invitation_id}")
def submit_review_invite_response(invitation_id: str, payload: dict = Body(default={})) -> dict:
    data = dict(payload)
    data["invitation_id"] = invitation_id
    return execute(data)
