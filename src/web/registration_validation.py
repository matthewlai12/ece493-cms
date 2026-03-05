from fastapi import APIRouter, Body

from src.services.registration_validation_service import validate_registration_payload

router = APIRouter(tags=["web-registration_validation"])


@router.get("/registration-validation")
def page_registration_validation() -> dict:
    return {
        "page": "registration_validation",
        "fields": ["name", "email", "password"],
        "submit_to": "/api/auth/register/validate",
    }


@router.post("/registration-validation")
def submit_registration_validation(payload: dict = Body(...)) -> dict:
    return validate_registration_payload(payload)
