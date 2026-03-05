from fastapi import APIRouter, Body

from src.services.auth_password_service import execute

router = APIRouter(tags=["web-auth_password"])


@router.get("/auth-password")
def page_auth_password() -> dict:
    return {
        "page": "auth_password",
        "fields": ["email", "current_password", "new_password"],
        "submit_to": "/api/auth/password",
    }


@router.post("/auth-password")
def submit_auth_password(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
