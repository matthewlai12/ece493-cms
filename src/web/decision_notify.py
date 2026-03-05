from fastapi import APIRouter
from fastapi import Body

from src.services.decision_notify_service import execute

router = APIRouter(tags=["web-decision_notify"])


@router.get("/decision-notify")
def page_decision_notify() -> dict:
    return {
        "page": "decision_notify",
        "fields": ["author_email"],
        "submit_to_template": "/api/decisions/{submission_id}/notify",
        "method": "POST",
    }


@router.post("/decision-notify/{submission_id}")
def submit_decision_notify(submission_id: str, payload: dict = Body(default={})) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    return execute(data)
