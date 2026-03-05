from fastapi import APIRouter, Body, HTTPException

from src.services.schedule_generate_service import execute

router = APIRouter(tags=["schedule_generate"])


@router.post("/schedule/generate")
def handle_schedule_generate(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
