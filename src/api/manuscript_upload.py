from fastapi import APIRouter, Body, HTTPException

from src.services.manuscript_upload_service import execute

router = APIRouter(tags=["manuscript_upload"])


@router.post("/submissions/{submission_id}/files", status_code=201)
def handle_manuscript_upload(
    submission_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
