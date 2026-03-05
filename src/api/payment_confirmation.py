from fastapi import APIRouter, HTTPException, Query

from src.services.payment_confirmation_service import execute

router = APIRouter(tags=["payment_confirmation"])


@router.get("/registrations/{registration_id}/confirmation")
def handle_payment_confirmation(
    registration_id: str,
    attendee_email: str = Query(default=""),
) -> dict:
    data: dict = {}
    data["registration_id"] = registration_id
    data["attendee_email"] = attendee_email
    try:
        return execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
