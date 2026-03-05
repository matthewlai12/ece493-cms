from fastapi import APIRouter, HTTPException, Query

from src.services.assigned_papers_service import execute

router = APIRouter(tags=["assigned_papers"])


@router.get("/referee/assignments")
def handle_assigned_papers(
    referee_id: str | None = Query(default=None),
) -> dict:
    data: dict = {}
    if referee_id is not None:
        data["referee_id"] = referee_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
