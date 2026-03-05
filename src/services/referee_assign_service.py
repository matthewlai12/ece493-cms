from typing import Any

from src.services.audit_log import record_event
from src.services.review_invite_notify_service import create_review_invitation


def assign_referee(
    submission_id: str,
    referee_id: str,
    paper_title: str,
    paper_abstract: str,
    referee_email: str,
    assigned_by: str,
) -> dict[str, Any]:
    result = create_review_invitation(
        submission_id=submission_id,
        referee_id=referee_id,
        paper_title=paper_title,
        paper_abstract=paper_abstract,
        referee_email=referee_email,
    )

    invitation = result.get("invitation")
    if invitation is not None:
        record_event(
            "referee_assign",
            actor=assigned_by.strip() or "chair",
            details={
                "submission_id": invitation["submission_id"],
                "referee_id": invitation["referee_id"],
                "invitation_id": invitation["id"],
            },
        )
    return result


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = assign_referee(
        submission_id=str(data.get("submission_id", "")),
        referee_id=str(data.get("referee_id", "")),
        paper_title=str(data.get("paper_title", "")),
        paper_abstract=str(data.get("paper_abstract", "")),
        referee_email=str(data.get("referee_email", "")),
        assigned_by=str(data.get("assigned_by", "chair")),
    )
    return {"service": "referee_assign_service", **result}
