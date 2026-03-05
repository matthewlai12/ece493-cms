from fastapi import APIRouter, Body, HTTPException

from src.services.submission_save_service import execute

router = APIRouter(tags=["submission_save"])


@router.patch("/submissions/{submission_id}")
def handle_submission_save(
    submission_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
