from fastapi import APIRouter

from src.services.schedule_view_service import get_published_schedule

router = APIRouter(tags=["schedule_view"])


@router.get("/schedule")
def handle_schedule_view() -> dict:
    schedule = get_published_schedule()
    if schedule is None:
        return {"schedule": None, "message": "Conference schedule has not been published."}
    return {"schedule": schedule}
