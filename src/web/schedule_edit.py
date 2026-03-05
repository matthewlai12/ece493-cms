from fastapi import APIRouter
from fastapi import Body

from src.services.schedule_edit_service import execute

router = APIRouter(tags=["web-schedule_edit"])


@router.get("/schedule-edit")
@router.get("/schedule_edit")
def page_schedule_edit() -> dict:
    return {
        "page": "schedule_edit",
        "fields": ["sessions", "notes", "editor_id"],
        "submit_to_template": "/api/schedule/{schedule_id}",
        "method": "PATCH",
    }


@router.post("/schedule-edit/{schedule_id}")
def submit_schedule_edit(
    schedule_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["schedule_id"] = schedule_id
    return execute(data)
