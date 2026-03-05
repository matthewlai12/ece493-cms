from fastapi import APIRouter

from src.services.registration_prices_service import execute

router = APIRouter(tags=["web-registration_prices"])


@router.get("/registration-prices")
def page_registration_prices() -> dict:
    return {"page": "registration_prices", "data": execute({})}
