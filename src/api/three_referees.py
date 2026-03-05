from fastapi import APIRouter, Body, HTTPException

from src.services.three_referees_service import execute

router = APIRouter(tags=["three_referees"])


@router.post("/referees/assignments/validate")
def handle_three_referees(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
