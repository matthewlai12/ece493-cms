from fastapi import APIRouter, Body, HTTPException

from src.services.user_registration_service import create_user_account

router = APIRouter(tags=["user_registration"])


@router.post("/auth/register", status_code=201)
def handle_user_registration(
    payload: dict = Body(...),
) -> dict:
    try:
        user = create_user_account(
            email=str(payload.get("email", "")),
            password=str(payload.get("password", "")),
            name=str(payload.get("name", "")),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"user": user}
