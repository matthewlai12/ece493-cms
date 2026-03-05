from fastapi import APIRouter, Body, HTTPException

from src.services.submission_create_service import execute

router = APIRouter(tags=["submission_create"])


@router.post("/submissions", status_code=201)
def handle_submission_create(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
