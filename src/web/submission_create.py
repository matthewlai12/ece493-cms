from fastapi import APIRouter, Body

from src.services.submission_create_service import execute

router = APIRouter(tags=["web-submission_create"])


@router.get("/submission-create")
def page_submission_create() -> dict:
    return {
        "page": "submission_create",
        "fields": ["author_id", "title", "abstract", "manuscript_format"],
        "submit_to": "/api/submissions",
    }


@router.post("/submission-create")
def submit_submission_create(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
