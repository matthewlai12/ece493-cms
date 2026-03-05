from fastapi import APIRouter
from fastapi import Body

from src.services.schedule_publish_service import execute

router = APIRouter(tags=["web-schedule_publish"])


@router.get("/schedule-publish")
@router.get("/schedule_publish")
def page_schedule_publish() -> dict:
    return {
        "page": "schedule_publish",
        "fields": ["finalized", "recipients", "publisher_id"],
        "submit_to_template": "/api/schedule/{schedule_id}/publish",
        "method": "POST",
    }


@router.post("/schedule-publish/{schedule_id}")
def submit_schedule_publish(
    schedule_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["schedule_id"] = schedule_id
    return execute(data)
