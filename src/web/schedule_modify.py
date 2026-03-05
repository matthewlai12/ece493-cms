from fastapi import APIRouter
from fastapi import Body

from src.services.schedule_modify_service import execute

router = APIRouter(tags=["web-schedule_modify"])


@router.get("/schedule-modify")
@router.get("/schedule_modify")
def page_schedule_modify() -> dict:
    return {
        "page": "schedule_modify",
        "fields": ["sessions", "notes", "admin_id"],
        "submit_to_template": "/api/schedule/{schedule_id}/modify",
        "method": "PATCH",
    }


@router.post("/schedule-modify/{schedule_id}")
def submit_schedule_modify(
    schedule_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["schedule_id"] = schedule_id
    return execute(data)
