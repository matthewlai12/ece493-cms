from fastapi import APIRouter, Body, HTTPException

from src.services.auth_login_service import execute

router = APIRouter(tags=["auth_login"])


@router.post("/auth/login")
def handle_auth_login(
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
