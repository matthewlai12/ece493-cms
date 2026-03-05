from fastapi import APIRouter

from src.services.registration_prices_service import list_active_registration_prices

router = APIRouter(tags=["registration_prices"])


@router.get("/registration-prices")
def handle_registration_prices() -> dict:
    prices = list_active_registration_prices()
    if not prices:
        return {"items": [], "message": "Registration price list is not available."}
    return {"items": prices}
