from fastapi import APIRouter

from src.services.announcements_service import execute

router = APIRouter(tags=["web-announcements"])


@router.get("/announcements")
def page_announcements() -> dict:
    return {"page": "announcements", "data": execute({})}
