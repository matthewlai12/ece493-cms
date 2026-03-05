from fastapi import APIRouter
from fastapi import Body

from src.services.referee_assign_service import execute

router = APIRouter(tags=["web-referee_assign"])


@router.get("/referee-assign")
@router.get("/referee_assign")
def page_referee_assign() -> dict:
    return {
        "page": "referee_assign",
        "fields": ["submission_id", "referee_id", "paper_title", "paper_abstract", "referee_email", "assigned_by"],
        "submit_to": "/api/referees/assignments",
        "method": "POST",
    }


@router.post("/referee-assign")
def submit_referee_assign(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
