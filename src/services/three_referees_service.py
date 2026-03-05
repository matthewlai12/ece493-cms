from typing import Any

from src.services.review_invite_notify_service import list_review_invitations

_REQUIRED_REFEREES = 3


def validate_three_referees(submission_id: str) -> dict[str, Any]:
    if not str(submission_id).isdigit() or int(submission_id) <= 0:
        raise ValueError("Submission ID is invalid.")

    invitations = list_review_invitations()
    matching = [
        item
        for item in invitations
        if int(item["submission_id"]) == int(submission_id) and item["status"] in {"pending", "accepted"}
    ]
    unique_referees = sorted({item["referee_id"] for item in matching})
    assigned_count = len(unique_referees)
    exactly_three = assigned_count == _REQUIRED_REFEREES
    can_proceed = exactly_three
    missing = max(0, _REQUIRED_REFEREES - assigned_count)
    excess = max(0, assigned_count - _REQUIRED_REFEREES)
    if exactly_three:
        message = "Submission has exactly three referees assigned."
    elif assigned_count < _REQUIRED_REFEREES:
        message = "Submission does not yet have enough referees assigned."
    else:
        message = "Submission has too many referees assigned."
    return {
        "submission_id": int(submission_id),
        "referees": unique_referees,
        "assigned": assigned_count,
        "required": _REQUIRED_REFEREES,
        "missing": missing,
        "excess": excess,
        "exactly_three": exactly_three,
        "can_proceed": can_proceed,
        "message": message,
    }


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = validate_three_referees(str(data.get("submission_id", "")))
    return {"service": "three_referees_service", **result}
