from fastapi import APIRouter
from fastapi import Body

from src.services.payment_confirmation_service import execute

router = APIRouter(tags=["web-payment_confirmation"])


@router.get("/payment-confirmation")
@router.get("/payment_confirmation")
def page_payment_confirmation() -> dict:
    return {
        "page": "payment_confirmation",
        "fields": ["attendee_email"],
        "submit_to_template": "/api/registrations/{registration_id}/confirmation",
        "method": "GET",
    }


@router.post("/payment-confirmation/{registration_id}")
def submit_payment_confirmation(
    registration_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["registration_id"] = registration_id
    return execute(data)
