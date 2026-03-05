from fastapi import APIRouter
from fastapi import Query

from src.services.assigned_papers_service import execute

router = APIRouter(tags=["web-assigned_papers"])


@router.get("/assigned-papers")
@router.get("/assigned_papers")
def page_assigned_papers(referee_id: str | None = Query(default=None)) -> dict:
    payload: dict[str, str] = {}
    if referee_id is not None:
        payload["referee_id"] = referee_id
    result = execute(payload) if payload else {"service": "assigned_papers_service", "assignments": []}
    return {
        "page": "assigned_papers",
        "assignments": result.get("assignments", []),
        "message": result.get("message", "Provide referee_id to view assignments."),
        "query": "referee_id",
    }
