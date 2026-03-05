from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.notification_service import send_email
from src.services.schedule_generate_service import GeneratedSession, get_generated_schedule, set_generated_schedule

_published_schedules: dict[int, "PublishedSchedule"] = {}


class NotificationResult(TypedDict):
    recipient: str
    sent: bool


class PublishedSchedule(TypedDict):
    id: int
    status: str
    generated_at: str
    published_at: str
    sessions: list[GeneratedSession]
    public_url: str


def publish_schedule(
    schedule_id: str,
    *,
    finalized: bool,
    recipients: list[str],
    publisher_id: str = "admin",
) -> dict[str, Any]:
    if not schedule_id.isdigit() or int(schedule_id) <= 0:
        raise ValueError("Schedule ID is invalid.")
    if not finalized:
        raise ValueError("Selected schedule is not finalized.")

    schedule = get_generated_schedule(schedule_id)
    if schedule is None:
        raise ValueError("Selected schedule does not exist.")
    sessions = list(schedule.get("sessions", []))
    if not sessions:
        raise ValueError("Schedule cannot be published without sessions.")

    published: PublishedSchedule = {
        "id": int(schedule_id),
        "status": "published",
        "generated_at": str(schedule.get("generated_at", "")),
        "published_at": datetime.now(timezone.utc).isoformat(),
        "sessions": sessions,
        "public_url": f"/web/schedule/{schedule_id}",
    }
    _published_schedules[published["id"]] = published
    set_generated_schedule(
        {
            "id": published["id"],
            "status": "published",
            "generated_at": published["generated_at"],
            "sessions": published["sessions"],
        }
    )

    clean_recipients = [email.strip().lower() for email in recipients]
    sent_count = 0
    failed_count = 0
    deliveries: list[NotificationResult] = []
    for recipient in clean_recipients:
        delivery = send_email(
            recipient,
            "Conference schedule published",
            f"The final schedule has been published: {published['public_url']}",
        )
        sent = bool(delivery.get("sent"))
        deliveries.append({"recipient": recipient, "sent": sent})
        if sent:
            sent_count += 1
        else:
            failed_count += 1

    record_event(
        "schedule_publish",
        actor=publisher_id.strip() or "admin",
        details={
            "schedule_id": published["id"],
            "recipient_count": len(clean_recipients),
            "sent_count": sent_count,
            "failed_count": failed_count,
        },
    )
    message = (
        "Schedule published and notifications delivered."
        if failed_count == 0
        else "Schedule published; some notifications failed."
    )
    return {
        "schedule": published,
        "notifications": deliveries,
        "sent_count": sent_count,
        "failed_count": failed_count,
        "message": message,
    }


def get_published_schedule(schedule_id: str) -> PublishedSchedule | None:
    if not schedule_id.isdigit():
        return None
    schedule = _published_schedules.get(int(schedule_id))
    if schedule is None:
        return None
    return dict(schedule)


def list_published_schedules() -> list[PublishedSchedule]:
    schedules = [dict(item) for item in _published_schedules.values()]
    schedules.sort(key=lambda item: item["published_at"], reverse=True)
    return schedules


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = publish_schedule(
        schedule_id=str(data.get("schedule_id", "")),
        finalized=bool(data.get("finalized", False)),
        recipients=list(data.get("recipients", [])),
        publisher_id=str(data.get("publisher_id", "admin")),
    )
    return {"service": "schedule_publish_service", **result}


def reset_schedule_publish_state() -> None:
    _published_schedules.clear()
