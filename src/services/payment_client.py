def process_payment(registration_id: str, amount: float, currency: str = "USD") -> dict:
    return {
        "registration_id": registration_id,
        "amount": amount,
        "currency": currency,
        "status": "paid" if amount >= 0 else "declined",
    }
