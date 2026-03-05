from fastapi import APIRouter
from fastapi import Body

from src.services.submission_save_service import execute

router = APIRouter(tags=["web-submission_save"])


@router.get("/submission-save")
def page_submission_save() -> dict:
    return {
        "page": "submission_save",
        "fields": ["author_id", "title", "abstract"],
        "submit_to_template": "/api/submissions/{submission_id}",
        "method": "PATCH",
    }


@router.post("/submission-save/{submission_id}")
def submit_submission_save(
    submission_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    return execute(data)
