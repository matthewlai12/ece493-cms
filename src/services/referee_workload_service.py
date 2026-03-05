from typing import Any

from src.services.review_invite_notify_service import list_review_invitations

_MAX_ASSIGNMENTS = 5


def check_referee_workload(referee_id: str, requested_new_assignments: int = 1) -> dict[str, Any]:
    normalized_referee_id = referee_id.strip()
    if not normalized_referee_id:
        raise ValueError("Referee ID is required.")
    if requested_new_assignments < 0:
        raise ValueError("Requested assignments cannot be negative.")

    invitations = list_review_invitations(normalized_referee_id)
    active_assignments = len([item for item in invitations if item["status"] in {"pending", "accepted"}])
    projected_total = active_assignments + requested_new_assignments
    within_limit = projected_total <= _MAX_ASSIGNMENTS
    return {
        "referee_id": normalized_referee_id,
        "active_assignments": active_assignments,
        "requested_new_assignments": requested_new_assignments,
        "max_assignments": _MAX_ASSIGNMENTS,
        "projected_total": projected_total,
        "within_limit": within_limit,
        "message": "Workload within limit." if within_limit else "Workload limit exceeded.",
    }


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = check_referee_workload(
        referee_id=str(data.get("referee_id", "")),
        requested_new_assignments=int(data.get("requested_new_assignments", 1)),
    )
    return {"service": "referee_workload_service", **result}
