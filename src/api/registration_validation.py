from fastapi import APIRouter, Body

from src.services.registration_validation_service import validate_registration_payload

router = APIRouter(tags=["registration_validation"])


@router.post("/auth/register/validate")
def handle_registration_validation(payload: dict = Body(...)) -> dict:
    return validate_registration_payload(payload)
