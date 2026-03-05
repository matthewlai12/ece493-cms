from fastapi import APIRouter
from fastapi import Body

from src.services.conference_register_service import execute

router = APIRouter(tags=["web-conference_register"])


@router.get("/conference-register")
@router.get("/conference_register")
def page_conference_register() -> dict:
    return {
        "page": "conference_register",
        "fields": ["attendee_id", "is_authenticated"],
        "submit_to": "/api/registrations",
        "method": "POST",
    }


@router.post("/conference-register")
def submit_conference_register(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
