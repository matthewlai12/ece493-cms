from fastapi import APIRouter, Body, HTTPException

from src.services.decision_record_service import execute

router = APIRouter(tags=["decision_record"])


@router.post("/decisions/{submission_id}")
def handle_decision_record(
    submission_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["submission_id"] = submission_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
