from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.notification_service import send_email

_ALLOWED_OUTCOMES = {"accept", "reject"}
_decisions: dict[int, dict[str, Any]] = {}


class DecisionRecord(TypedDict):
    submission_id: int
    outcome: str
    decided_by: str
    decided_at: str
    notes: str


def upsert_decision(
    submission_id: str,
    outcome: str,
    decided_by: str,
    notes: str = "",
) -> DecisionRecord:
    if not str(submission_id).isdigit() or int(submission_id) <= 0:
        raise ValueError("Submission ID is invalid.")
    normalized_outcome = outcome.strip().lower()
    if normalized_outcome not in _ALLOWED_OUTCOMES:
        raise ValueError("Decision outcome must be accept or reject.")
    if not decided_by.strip():
        raise ValueError("Decision maker is required.")

    sid = int(submission_id)
    decision: DecisionRecord = {
        "submission_id": sid,
        "outcome": normalized_outcome,
        "decided_by": decided_by.strip(),
        "decided_at": datetime.now(timezone.utc).isoformat(),
        "notes": notes.strip(),
    }
    _decisions[sid] = decision
    return decision


def get_decision(submission_id: str) -> DecisionRecord | None:
    if not str(submission_id).isdigit():
        return None
    decision = _decisions.get(int(submission_id))
    if decision is None:
        return None
    return dict(decision)


def notify_author_of_decision(submission_id: str, author_email: str) -> dict[str, Any]:
    decision = get_decision(submission_id)
    if decision is None:
        raise ValueError("No decision available for this submission.")

    normalized_email = author_email.strip().lower()
    if not normalized_email:
        raise ValueError("Author email is required.")

    subject = f"Paper decision for submission #{decision['submission_id']}"
    body = (
        f"Your submission has been {decision['outcome']}. "
        f"Decided by {decision['decided_by']} on {decision['decided_at']}."
    )
    delivery = send_email(normalized_email, subject, body)
    notified = bool(delivery.get("sent"))

    record_event(
        "decision_notify",
        actor=decision["decided_by"],
        details={
            "submission_id": decision["submission_id"],
            "recipient": normalized_email,
            "notified": notified,
        },
    )
    return {"decision": decision, "notified": notified, "recipient": normalized_email}


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = notify_author_of_decision(
        submission_id=str(data.get("submission_id", "")),
        author_email=str(data.get("author_email", "")),
    )
    return {"service": "decision_notify_service", **result}


def reset_decision_notify_state() -> None:
    _decisions.clear()
