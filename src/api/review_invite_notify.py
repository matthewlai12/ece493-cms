from fastapi import APIRouter, HTTPException, Query

from src.services.review_invite_notify_service import execute

router = APIRouter(tags=["review_invite_notify"])


@router.get("/referee/invitations")
def handle_review_invite_notify(
    referee_id: str | None = Query(default=None),
) -> dict:
    data: dict = {}
    if referee_id is not None:
        data["referee_id"] = referee_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
