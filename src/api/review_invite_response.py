from fastapi import APIRouter, Body, HTTPException

from src.services.review_invite_response_service import execute

router = APIRouter(tags=["review_invite_response"])


@router.post("/referee/invitations/{invitation_id}/response")
def handle_review_invite_response(
    invitation_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data: dict = dict(payload)
    data["invitation_id"] = invitation_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
