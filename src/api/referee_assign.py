from fastapi import APIRouter, Body, HTTPException

from src.services.referee_assign_service import execute

router = APIRouter(tags=["referee_assign"])


@router.post("/referees/assignments")
def handle_referee_assign(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
