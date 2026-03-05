from fastapi import APIRouter, Body

from src.services.user_registration_service import create_user_account

router = APIRouter(tags=["web-user_registration"])


@router.get("/user-registration")
def page_user_registration() -> dict:
    return {
        "page": "user_registration",
        "fields": ["name", "email", "password"],
        "submit_to": "/api/auth/register",
    }


@router.post("/user-registration")
def submit_user_registration(payload: dict = Body(...)) -> dict:
    user = create_user_account(
        email=str(payload.get("email", "")),
        password=str(payload.get("password", "")),
        name=str(payload.get("name", "")),
    )
    return {"message": "registered", "redirect_to": user["redirect_to"]}
