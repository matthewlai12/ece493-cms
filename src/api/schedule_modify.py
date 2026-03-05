from fastapi import APIRouter, Body, HTTPException

from src.services.schedule_modify_service import execute

router = APIRouter(tags=["schedule_modify"])


@router.patch("/schedule/{schedule_id}/modify")
def handle_schedule_modify(
    schedule_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["schedule_id"] = schedule_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
