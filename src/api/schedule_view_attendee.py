from fastapi import APIRouter, HTTPException, Query

from src.services.schedule_view_attendee_service import execute

router = APIRouter(tags=["schedule_view_attendee"])


@router.get("/schedule/attendee")
def handle_schedule_view_attendee(
    require_auth: bool = Query(default=False),
    is_authenticated: bool = Query(default=False),
) -> dict:
    data: dict = {}
    data["require_auth"] = require_auth
    data["is_authenticated"] = is_authenticated
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
