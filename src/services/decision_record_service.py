from typing import Any

from src.services.audit_log import record_event
from src.services.decision_notify_service import notify_author_of_decision, upsert_decision


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    decision = upsert_decision(
        submission_id=str(data.get("submission_id", "")),
        outcome=str(data.get("outcome", "")),
        decided_by=str(data.get("decided_by", "chair")),
        notes=str(data.get("notes", "")),
    )
    record_event(
        "decision_record",
        actor=decision["decided_by"],
        details={"submission_id": decision["submission_id"], "outcome": decision["outcome"]},
    )

    author_email = str(data.get("author_email", "")).strip()
    notified = False
    recipient = ""
    if author_email:
        notify_result = notify_author_of_decision(str(decision["submission_id"]), author_email)
        notified = bool(notify_result["notified"])
        recipient = str(notify_result["recipient"])

    return {
        "service": "decision_record_service",
        "decision": decision,
        "notified": notified,
        "recipient": recipient,
    }
