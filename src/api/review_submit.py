from fastapi import APIRouter, Body, HTTPException

from src.services.review_submit_service import execute

router = APIRouter(tags=["review_submit"])


@router.post("/reviews", status_code=201)
def handle_review_submit(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
