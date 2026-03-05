from typing import Any

from src.services.manuscript_upload_service import list_manuscript_files
from src.services.review_invite_notify_service import list_review_invitations


def list_assigned_papers(referee_id: str) -> list[dict[str, Any]]:
    normalized_referee_id = referee_id.strip()
    if not normalized_referee_id:
        raise ValueError("Referee ID is required.")

    invitations = list_review_invitations(normalized_referee_id)
    accepted = [item for item in invitations if item["status"] == "accepted"]

    assignments: list[dict[str, Any]] = []
    for invitation in accepted:
        submission_id = str(invitation["submission_id"])
        files = list_manuscript_files(submission_id=submission_id)
        assignments.append(
            {
                "invitation_id": invitation["id"],
                "submission_id": invitation["submission_id"],
                "paper_title": invitation["paper_title"],
                "paper_abstract": invitation["paper_abstract"],
                "manuscript_files": files,
            }
        )
    return assignments


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    assignments = list_assigned_papers(str(data.get("referee_id", "")))
    if assignments:
        message = "Assigned papers retrieved."
    else:
        message = "No papers are currently assigned to this referee."
    return {"service": "assigned_papers_service", "assignments": assignments, "message": message}
