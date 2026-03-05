from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.notification_service import send_email

_presentation_slots: dict[int, dict[str, Any]] = {}


class PresentationSlot(TypedDict):
    submission_id: int
    title: str
    room: str
    start_time: str
    end_time: str
    schedule_status: str


def assign_presentation_slot(
    submission_id: str,
    title: str,
    room: str,
    start_time: str,
    end_time: str,
) -> PresentationSlot:
    if not str(submission_id).isdigit() or int(submission_id) <= 0:
        raise ValueError("Submission ID is invalid.")
    if not title.strip():
        raise ValueError("Presentation title is required.")
    if not room.strip():
        raise ValueError("Presentation room is required.")

    slot: PresentationSlot = {
        "submission_id": int(submission_id),
        "title": title.strip(),
        "room": room.strip(),
        "start_time": start_time.strip() or datetime.now(timezone.utc).isoformat(),
        "end_time": end_time.strip() or datetime.now(timezone.utc).isoformat(),
        "schedule_status": "published",
    }
    _presentation_slots[slot["submission_id"]] = slot
    return slot


def get_presentation_slot(submission_id: str) -> PresentationSlot | None:
    if not str(submission_id).isdigit():
        return None
    slot = _presentation_slots.get(int(submission_id))
    if slot is None:
        return None
    return dict(slot)


def notify_schedule(submission_id: str, author_email: str) -> dict[str, Any]:
    slot = get_presentation_slot(submission_id)
    if slot is None:
        raise ValueError("No presentation schedule is available for this submission.")

    normalized_email = author_email.strip().lower()
    if not normalized_email:
        return {
            "slot": slot,
            "recipient": normalized_email,
            "notified": False,
            "message": "Schedule delivery failed.",
        }

    subject = f"Presentation schedule for submission #{slot['submission_id']}"
    body = (
        f"Your presentation '{slot['title']}' is scheduled in {slot['room']} "
        f"from {slot['start_time']} to {slot['end_time']}."
    )
    delivery = send_email(normalized_email, subject, body)
    notified = bool(delivery.get("sent"))
    message = "Schedule delivered." if notified else "Schedule delivery failed."
    return {
        "slot": slot,
        "recipient": normalized_email,
        "notified": notified,
        "message": message,
    }


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = notify_schedule(
        submission_id=str(data.get("submission_id", "")),
        author_email=str(data.get("author_email", "")),
    )
    return {"service": "schedule_notify_service", **result}


def reset_schedule_notify_state() -> None:
    _presentation_slots.clear()
