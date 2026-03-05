from fastapi import APIRouter, Body, HTTPException

from src.services.registration_payment_service import execute

router = APIRouter(tags=["registration_payment"])


@router.post("/registrations/{registration_id}/payment")
def handle_registration_payment(
    registration_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["registration_id"] = registration_id
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
