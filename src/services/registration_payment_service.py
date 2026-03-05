from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.conference_register_service import get_registration, update_registration_status
from src.services.notification_service import send_email
from src.services.payment_client import process_payment

_payments: list[dict[str, Any]] = []


class PaymentRecord(TypedDict):
    id: int
    registration_id: int
    amount: float
    currency: str
    status: str
    processed_at: str


def pay_registration_fee(
    registration_id: str,
    amount: float,
    *,
    currency: str = "USD",
    attendee_email: str = "",
    force_decline: bool = False,
) -> dict[str, Any]:
    if not registration_id.isdigit() or int(registration_id) <= 0:
        raise ValueError("Registration ID is invalid.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    registration = get_registration(registration_id)
    if registration is None:
        raise ValueError("Registration record not found.")
    if registration["status"] not in {"pending_payment", "payment_declined"}:
        raise ValueError("Registration is not eligible for payment.")

    payment_result = process_payment(registration_id, amount, currency)
    status = str(payment_result.get("status", "declined"))
    if force_decline:
        status = "declined"

    payment: PaymentRecord = {
        "id": len(_payments) + 1,
        "registration_id": int(registration_id),
        "amount": float(amount),
        "currency": currency,
        "status": status,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
    _payments.append(dict(payment))

    if status == "paid":
        update_registration_status(registration_id, "confirmed")
    else:
        update_registration_status(registration_id, "payment_declined")

    normalized_email = attendee_email.strip().lower()
    subject = "Conference registration payment result"
    body = f"Payment status for registration #{registration_id}: {status}"
    delivery = send_email(normalized_email, subject, body)

    record_event(
        "registration_payment",
        actor=registration["attendee_id"],
        details={
            "registration_id": int(registration_id),
            "payment_id": payment["id"],
            "status": status,
        },
    )
    return {
        "payment": payment,
        "registration_status": "confirmed" if status == "paid" else "payment_declined",
        "notification_sent": bool(delivery.get("sent")),
        "message": (
            "Payment completed and registration confirmed."
            if status == "paid"
            else "Payment was declined. You can retry."
        ),
    }


def get_payment(payment_id: str) -> PaymentRecord | None:
    if not payment_id.isdigit():
        return None
    target_id = int(payment_id)
    for payment in _payments:
        if int(payment.get("id", -1)) == target_id:
            return dict(payment)
    return None


def get_latest_payment_for_registration(registration_id: str) -> PaymentRecord | None:
    if not registration_id.isdigit():
        return None
    target_id = int(registration_id)
    matches = [payment for payment in _payments if int(payment.get("registration_id", -1)) == target_id]
    if not matches:
        return None
    return dict(matches[-1])


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = pay_registration_fee(
        registration_id=str(data.get("registration_id", "")),
        amount=float(data.get("amount", 0)),
        currency=str(data.get("currency", "USD")),
        attendee_email=str(data.get("attendee_email", "")),
        force_decline=bool(data.get("force_decline", False)),
    )
    return {"service": "registration_payment_service", **result}


def reset_registration_payment_state() -> None:
    _payments.clear()
