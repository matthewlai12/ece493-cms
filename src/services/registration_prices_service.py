from collections.abc import Iterable
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any
from typing import TypedDict


class RegistrationPriceView(TypedDict):
    id: int
    category: str
    amount: float
    currency: str
    active_from: str
    active_to: str


@lru_cache(maxsize=1)
def _default_prices() -> list[dict]:
    return [
        {
            "id": 1,
            "category": "student",
            "amount": 199.00,
            "currency": "USD",
            "active_from": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "active_to": datetime(2026, 7, 1, tzinfo=timezone.utc),
        },
        {
            "id": 2,
            "category": "regular",
            "amount": 399.00,
            "currency": "USD",
            "active_from": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "active_to": datetime(2026, 7, 1, tzinfo=timezone.utc),
        },
    ]


def list_active_registration_prices(
    records: Iterable[dict] | None = None,
    now: datetime | None = None,
) -> list[RegistrationPriceView]:
    source = list(records) if records is not None else _default_prices()
    current_time = now or datetime.now(timezone.utc)
    active = [
        item
        for item in source
        if item["active_from"] <= current_time <= item["active_to"]
    ]
    active.sort(key=lambda item: item["amount"])
    return [
        {
            "id": int(item["id"]),
            "category": str(item["category"]),
            "amount": float(item["amount"]),
            "currency": str(item["currency"]),
            "active_from": item["active_from"].isoformat(),
            "active_to": item["active_to"].isoformat(),
        }
        for item in active
    ]


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    records = data.get("records")
    prices = list_active_registration_prices(records if isinstance(records, list) else None)
    return {"service": "registration_prices_service", "prices": prices}
