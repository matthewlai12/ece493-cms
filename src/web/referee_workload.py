from fastapi import APIRouter
from fastapi import Body

from src.services.referee_workload_service import execute

router = APIRouter(tags=["web-referee_workload"])


@router.get("/referee-workload")
@router.get("/referee_workload")
def page_referee_workload() -> dict:
    return {
        "page": "referee_workload",
        "fields": ["referee_id", "requested_new_assignments"],
        "submit_to": "/api/referees/assignments/workload",
        "method": "POST",
    }


@router.post("/referee-workload")
def submit_referee_workload(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
