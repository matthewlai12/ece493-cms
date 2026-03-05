from fastapi import APIRouter

from src.services.schedule_view_service import execute

router = APIRouter(tags=["web-schedule_view"])


@router.get("/schedule")
def page_schedule_view() -> dict:
    return {"page": "schedule_view", "data": execute({})}
