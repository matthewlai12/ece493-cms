from fastapi import APIRouter, Body, HTTPException

from src.services.referee_workload_service import execute

router = APIRouter(tags=["referee_workload"])


@router.post("/referees/assignments/workload")
def handle_referee_workload(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
