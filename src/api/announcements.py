from fastapi import APIRouter

from src.services.announcements_service import list_public_announcements

router = APIRouter(tags=["announcements"])


@router.get("/announcements")
def handle_announcements() -> dict:
    announcements = list_public_announcements()
    if not announcements:
        return {"items": [], "message": "No public announcements available."}
    return {"items": announcements}
