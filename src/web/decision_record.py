from fastapi import APIRouter
from fastapi import Body

from src.services.decision_record_service import execute

router = APIRouter(tags=["web-decision_record"])


@router.get("/decision-record")
@router.get("/decision_record")
def page_decision_record() -> dict:
    return {
        "page": "decision_record",
        "fields": ["outcome", "decided_by", "notes", "author_email"],
        "submit_to_template": "/api/decisions/{submission_id}",
        "method": "POST",
    }


@router.post("/decision-record/{submission_id}")
def submit_decision_record(submission_id: str, payload: dict = Body(default={})) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    return execute(data)
