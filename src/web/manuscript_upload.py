from fastapi import APIRouter, Body

from src.services.manuscript_upload_service import execute

router = APIRouter(tags=["web-manuscript_upload"])


@router.get("/manuscript-upload")
def page_manuscript_upload() -> dict:
    return {
        "page": "manuscript_upload",
        "fields": ["filename", "content_type", "content"],
        "submit_to_template": "/api/submissions/{submission_id}/files",
    }


@router.post("/manuscript-upload/{submission_id}")
def submit_manuscript_upload(submission_id: str, payload: dict = Body(default={})) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    return execute(data)
