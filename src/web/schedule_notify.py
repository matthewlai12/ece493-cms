from fastapi import APIRouter
from fastapi import Body

from src.services.schedule_notify_service import execute

router = APIRouter(tags=["web-schedule_notify"])


@router.get("/schedule-notify")
@router.get("/schedule_notify")
def page_schedule_notify() -> dict:
    return {
        "page": "schedule_notify",
        "fields": ["submission_id", "author_email"],
        "submit_to": "/api/schedule-notify",
        "method": "POST",
    }


@router.post("/schedule-notify")
def submit_schedule_notify(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
