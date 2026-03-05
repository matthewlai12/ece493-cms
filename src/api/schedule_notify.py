from fastapi import APIRouter, Body, HTTPException

from src.services.schedule_notify_service import execute

router = APIRouter(tags=["schedule_notify"])


@router.post("/schedule-notify")
def handle_schedule_notify(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
