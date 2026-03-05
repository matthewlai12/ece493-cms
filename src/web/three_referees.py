from fastapi import APIRouter
from fastapi import Body

from src.services.three_referees_service import execute

router = APIRouter(tags=["web-three_referees"])


@router.get("/three-referees")
@router.get("/three_referees")
def page_three_referees() -> dict:
    return {
        "page": "three_referees",
        "fields": ["submission_id"],
        "submit_to": "/api/referees/assignments/validate",
        "method": "POST",
    }


@router.post("/three-referees")
def submit_three_referees(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
