from fastapi import APIRouter
from fastapi import Body

from src.services.schedule_generate_service import execute

router = APIRouter(tags=["web-schedule_generate"])


@router.get("/schedule-generate")
@router.get("/schedule_generate")
def page_schedule_generate() -> dict:
    return {
        "page": "schedule_generate",
        "fields": ["schedule_id", "accepted_submissions", "rooms", "slot_start", "slot_minutes"],
        "submit_to": "/api/schedule/generate",
        "method": "POST",
    }


@router.post("/schedule-generate")
def submit_schedule_generate(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
