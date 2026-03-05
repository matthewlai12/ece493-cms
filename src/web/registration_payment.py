from fastapi import APIRouter
from fastapi import Body

from src.services.registration_payment_service import execute

router = APIRouter(tags=["web-registration_payment"])


@router.get("/registration-payment")
@router.get("/registration_payment")
def page_registration_payment() -> dict:
    return {
        "page": "registration_payment",
        "fields": ["amount", "currency", "attendee_email"],
        "submit_to_template": "/api/registrations/{registration_id}/payment",
        "method": "POST",
    }


@router.post("/registration-payment/{registration_id}")
def submit_registration_payment(
    registration_id: str,
    payload: dict = Body(default={}),
) -> dict:
    data = dict(payload)
    data["registration_id"] = registration_id
    return execute(data)
