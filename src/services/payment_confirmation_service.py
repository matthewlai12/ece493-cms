from datetime import datetime, timezone
from typing import Any, TypedDict
from uuid import uuid4

from src.services.audit_log import record_event
from src.services.conference_register_service import get_registration
from src.services.notification_service import send_email
from src.services.registration_payment_service import get_latest_payment_for_registration

_tickets_by_registration: dict[int, "ConfirmationTicket"] = {}


class ConfirmationTicket(TypedDict):
    id: int
    registration_id: int
    reference_code: str
    issued_at: str
    delivery_channel: str


def issue_confirmation_ticket(registration_id: str, *, attendee_email: str = "") -> dict[str, Any]:
    if not registration_id.isdigit() or int(registration_id) <= 0:
        raise ValueError("Registration ID is invalid.")

    registration = get_registration(registration_id)
    if registration is None:
        raise ValueError("Registration record not found.")
    if registration.get("status") != "confirmed":
        raise ValueError("Registration is not confirmed yet.")

    payment = get_latest_payment_for_registration(registration_id)
    if payment is None or payment.get("status") != "paid":
        raise ValueError("No successful payment record found for this registration.")

    reg_key = int(registration_id)
    existing = _tickets_by_registration.get(reg_key)
    if existing is None:
        ticket: ConfirmationTicket = {
            "id": len(_tickets_by_registration) + 1,
            "registration_id": reg_key,
            "reference_code": f"TKT-{reg_key}-{uuid4().hex[:8].upper()}",
            "issued_at": datetime.now(timezone.utc).isoformat(),
            "delivery_channel": "email",
        }
        _tickets_by_registration[reg_key] = ticket
    else:
        ticket = dict(existing)

    recipient = attendee_email.strip().lower() or str(registration.get("attendee_email", "")).strip().lower()
    delivery = send_email(
        recipient,
        "Your conference registration confirmation ticket",
        f"Ticket reference: {ticket['reference_code']}",
    )
    notification_sent = bool(delivery.get("sent"))

    record_event(
        "payment_confirmation",
        actor=str(registration.get("attendee_id", "attendee")),
        details={
            "registration_id": reg_key,
            "ticket_id": ticket["id"],
            "notification_sent": notification_sent,
        },
    )
    return {
        "ticket": ticket,
        "notification_sent": notification_sent,
        "message": (
            "Confirmation ticket available and delivered."
            if notification_sent
            else "Confirmation ticket available; notification delivery failed."
        ),
    }


def get_confirmation_ticket(registration_id: str) -> ConfirmationTicket | None:
    if not registration_id.isdigit():
        return None
    ticket = _tickets_by_registration.get(int(registration_id))
    if ticket is None:
        return None
    return dict(ticket)


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = issue_confirmation_ticket(
        registration_id=str(data.get("registration_id", "")),
        attendee_email=str(data.get("attendee_email", "")),
    )
    return {"service": "payment_confirmation_service", **result}


def reset_payment_confirmation_state() -> None:
    _tickets_by_registration.clear()
