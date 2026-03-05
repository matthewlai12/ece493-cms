from fastapi import APIRouter
from fastapi import Body

from src.services.schedule_view_attendee_service import execute

router = APIRouter(tags=["web-schedule_view_attendee"])


@router.get("/schedule-view-attendee")
@router.get("/schedule_view_attendee")
def page_schedule_view_attendee() -> dict:
    return {
        "page": "schedule_view_attendee",
        "fields": ["require_auth", "is_authenticated"],
        "submit_to": "/api/schedule/attendee",
        "method": "GET",
    }


@router.post("/schedule-view-attendee")
def submit_schedule_view_attendee(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
