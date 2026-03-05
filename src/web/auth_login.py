from fastapi import APIRouter, Body

from src.services.auth_login_service import execute

router = APIRouter(tags=["web-auth_login"])


@router.get("/auth-login")
def page_auth_login() -> dict:
    return {
        "page": "auth_login",
        "fields": ["email", "password"],
        "submit_to": "/api/auth/login",
    }


@router.post("/auth-login")
def submit_auth_login(payload: dict = Body(default={})) -> dict:
    return execute(dict(payload))
