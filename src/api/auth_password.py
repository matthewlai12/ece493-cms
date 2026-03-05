from fastapi import APIRouter, Body, HTTPException

from src.services.auth_password_service import execute

router = APIRouter(tags=["auth_password"])


@router.post("/auth/password")
def handle_auth_password(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
