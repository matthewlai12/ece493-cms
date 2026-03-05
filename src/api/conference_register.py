from fastapi import APIRouter, Body, HTTPException

from src.services.conference_register_service import execute

router = APIRouter(tags=["conference_register"])


@router.post("/registrations")
def handle_conference_register(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
